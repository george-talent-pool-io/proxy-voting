"""Train/validation-only exports. No frozen/test answers enter this capability."""
import hashlib
import json
from collections import Counter
from pathlib import Path

from classifier.preprocessing import normalise, source_hash
from semantic_pipeline.schema import PREDICATES, SemanticResult
from training.framework import VERSION
from training.framework.schema import Example, Provenance

ROOT = Path(__file__).resolve().parents[2]
PROMPT = ROOT / 'cascade/proxy_semantic_common_v1.txt'
PROTECTED = ('frozen', 'answer_key', 'semantic_challenge', 'semantic.json',
             'synthetic_all', 'calibration', 'adversarial', 'ood_test', 'private')


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(2 ** 20), b''):
            h.update(block)
    return h.hexdigest()


def write(path, value):
    with Path(path).open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n')


def jsonl(path, values):
    with Path(path).open('x', encoding='utf-8') as f:
        for value in values:
            f.write(json.dumps(value, ensure_ascii=False, allow_nan=False) + '\n')


def allowed_path(path):
    p = Path(path).resolve()
    # macOS canonical temporary paths start /private/var; this is an OS
    # location, not the repository's protected answer-key directory.
    view = p.as_posix().casefold().removeprefix('/private/var/')
    if any(word in view for word in PROTECTED):
        raise ValueError('Protected evaluation/calibration material is forbidden in training')
    return p


def laya_questions():
    from hybrid.semantics import questions
    q = questions()
    q['holding_confirmation_required'] = {
        'type': 'choice',
        'instructions': 'Does the current vote require a holdings certificate or ownership confirmation? '
                        'Distinguish ordinary record dates, optional services and superseded terms.',
        'criteria': {'YES': 'Current mandatory holdings evidence is required',
                     'NO': 'Not stated, explicitly waived or optional',
                     'UNKNOWN': 'Genuinely ambiguous or conflicting requirement'},
    }
    # Canonical names/choices are the same at training and inference boundaries.
    q['votability'] = q.pop('votable')
    q['votability']['criteria'] = {
        'VOTABLE': 'A current shareholder voting opportunity exists',
        'NOT_VOTABLE': 'This notice offers no shareholder voting opportunity',
        'UNCERTAIN': 'The voting opportunity cannot be established',
    }
    return {k: q[k] for k in PREDICATES}


def messages(example, prompt):
    e = example if isinstance(example, Example) else Example.model_validate(example)
    context = {'mode': 'INDEPENDENT', 'original_notice': e.text, 'narrative': e.text,
               'authoritative_structured_facts': e.structured_context}
    # The inference API supplies this schema via constrained format; a trainer
    # needs it in the prompt as well. This is a new, versioned training condition.
    system = prompt + '\n\nRequired JSON schema:\n' + json.dumps(SemanticResult.model_json_schema(), sort_keys=True)
    return [{'role': 'system', 'content': system},
            {'role': 'user', 'content': json.dumps(context, ensure_ascii=False)},
            {'role': 'assistant', 'content': e.target.model_dump_json()}]


def check_isolation(examples, *, check_near_duplicates=True):
    from training.framework.event_data import reject_protected
    reject_protected(examples)
    seen_ids = set()
    identities = {}
    for e in examples:
        if e.id in seen_ids:
            raise ValueError('Duplicate example ID')
        seen_ids.add(e.id)
        for key, value in [('group', e.group_id), ('hash', e.source_hash),
                           ('normalised_hash', source_hash(normalise(e.text))),
                           ('family', e.generation_family)]:
            if value is None:
                continue
            identity = (key, value)
            if identity in identities and identities[identity] != e.split:
                raise ValueError(f'Train/validation leakage: {identity}')
            identities[identity] = e.split
    if check_near_duplicates:
        from training.split import duplicate_groups
        groups = duplicate_groups([{'text': e.text} for e in examples])
        seen = {}
        for e, group in zip(examples, groups):
            if group in seen and seen[group] != e.split:
                raise ValueError('Near-duplicate train/validation leakage')
            seen[group] = e.split


def create_bundle(examples, output, *, source_manifest=None):
    output = allowed_path(output)
    data = [Example.model_validate(e.model_dump(mode='json') if isinstance(e, Example) else e) for e in examples]
    # A source manifest may certify previous global near-duplicate grouping.
    # Only the dedicated, checksum-verifying domain-corpus importer supplies it.
    check_isolation(data, check_near_duplicates=True)
    counts = Counter(e.split for e in data)
    if not counts['TRAIN'] or not counts['VALIDATION']:
        raise ValueError('Both TRAIN and VALIDATION are required')
    output.mkdir(parents=True, exist_ok=False)
    prompt = PROMPT.read_text()
    (output / 'semantic-prompt.txt').write_text(prompt)
    qs = laya_questions()
    write(output / 'laya-questions.json', qs)
    jsonl(output / 'examples.jsonl', [e.model_dump(mode='json') for e in data])
    for split, name in [('TRAIN', 'train'), ('VALIDATION', 'validation')]:
        subset = [e for e in data if e.split == split]
        jsonl(output / f'laya-{name}.jsonl', [
            {'state': e.text, 'questions': qs,
             'expected': {k: getattr(e.target, k) for k in PREDICATES}} for e in subset])
        jsonl(output / f'llm-{name}.jsonl', [{'messages': messages(e, prompt)} for e in subset])
    files = {p.name: sha(p) for p in sorted(output.iterdir()) if p.is_file()}
    manifest = {'version': VERSION, 'schema': 'nine-semantic-predicates-v1',
                'prompt_version': 'proxy_semantic_training_v1', 'files': files,
                'counts': dict(counts), 'label_origins': dict(Counter(e.provenance.origin.value for e in data)),
                'languages': dict(Counter(e.language for e in data)),
                'source_manifest': source_manifest, 'predicates': list(PREDICATES),
                'temporal_comparison': 'DETERMINISTIC_ONLY; no deadline-status training target',
                'leakage_check': 'Exact, NFC/HTML-normalised, numeric-masked 5-word Jaccard>=0.85, group and generation-family separation',
                'leakage_limitations': 'Lexical grouping is not a guarantee against semantic paraphrases; retain source corpus semantic/family grouping.',
                'automation_enabled': False, 'customer_accuracy': None}
    write(output / 'manifest.json', manifest)
    return manifest


def load_bundle(path):
    root = allowed_path(path)
    manifest = json.loads((root / 'manifest.json').read_text())
    required = {'examples.jsonl', 'semantic-prompt.txt', 'laya-questions.json',
                'laya-train.jsonl', 'laya-validation.jsonl', 'llm-train.jsonl', 'llm-validation.jsonl'}
    if set(manifest.get('files', {})) != required:
        raise ValueError('Unexpected or missing training bundle files')
    for name, expected in manifest['files'].items():
        p = (root / name).resolve()
        if p.parent != root or sha(p) != expected:
            raise ValueError('Training bundle checksum or path mismatch')
    data = [Example.model_validate_json(line) for line in (root / 'examples.jsonl').read_text().splitlines()]
    check_isolation(data, check_near_duplicates=False)  # grouped again when constructing any new bundle
    if dict(Counter(e.split for e in data)) != manifest['counts']:
        raise ValueError('Bundle counts differ from source examples')
    if dict(Counter(e.provenance.origin.value for e in data)) != manifest.get('label_origins'):
        raise ValueError('Bundle label provenance differs from source annotations')
    if dict(Counter(e.language for e in data)) != manifest.get('languages'):
        raise ValueError('Bundle language counts differ from source annotations')
    qs = json.loads((root / 'laya-questions.json').read_text())
    if list(qs) != list(PREDICATES):
        raise ValueError('Predicate ordering changed')
    prompt = (root / 'semantic-prompt.txt').read_text()
    # Checksums alone do not prevent a dishonest exporter from changing targets.
    for split, name in [('TRAIN', 'train'), ('VALIDATION', 'validation')]:
        subset = [e for e in data if e.split == split]
        for kind in ['laya', 'llm']:
            exported = [json.loads(line) for line in (root / f'{kind}-{name}.jsonl').read_text().splitlines()]
            expected = ([{'state': e.text, 'questions': qs, 'expected': {k: getattr(e.target, k) for k in PREDICATES}} for e in subset]
                        if kind == 'laya' else [{'messages': messages(e, prompt)} for e in subset])
            if exported != expected:
                raise ValueError('Rendered training content differs from annotated examples')
    return manifest, data


def from_domain_corpus(manifest_path, output, *, language='en', limit_per_split=None):
    from qwen_domain.protocol import load_training
    from classifier.deadlines import extract_deadline
    manifest_path = allowed_path(manifest_path)
    if limit_per_split is not None and limit_per_split < 1:
        raise ValueError('limit_per_split must be positive')
    data = []
    for split in ['TRAIN', 'VALIDATION']:
        rows = [r for r in load_training(manifest_path, split) if language == 'all' or r['language'] == language]
        rows = sorted(rows, key=lambda r: source_hash(r['id']))
        if limit_per_split is not None:
            rows = rows[:limit_per_split]
        for r in rows:
            target = {k: r['expected'][k] for k in PREDICATES}
            deadline = None
            if r.get('deadline_iso_truth'):
                result = extract_deadline(r['text'], r['evaluation_time'])
                candidates = [c for c in result['candidates'] if c['instant'] == r['deadline_iso_truth']]
                if not candidates:
                    raise ValueError(f'No verified training deadline span: {r["id"]}')
                deadline = candidates[-1]['text']
            target.update(deadline_information={'deadline_mentioned': deadline is not None, 'deadline_text': deadline},
                          evidence={k: r['evidence_truth'].get(k, []) for k in PREDICATES}, ambiguities=[])
            data.append(Example(id=r['id'], text=r['text'], source_hash=r['source_hash'],
                        group_id=r['duplicate_group'], generation_family=r['generation_family'], split=split,
                        language=r['language'], target=target,
                        provenance=Provenance(origin='AI_AUTHORED', author=r['generator_model'], model_id=r['generator_model'],
                            method=r['generation_method'], source_reference=str(manifest_path), revision=r['prompt_version'])))
    return create_bundle(data, output, source_manifest={'path': str(manifest_path), 'sha256': sha(manifest_path),
        'roles_read': ['TRAIN', 'VALIDATION'], 'held_out_answers_opened': False})
