"""Dataset-free frozen starting checkpoints, distinct from customer derivatives.

Manifests contain hashes, serving criteria and model provenance, never notices,
labels or optimiser state. Model locations may change only if every byte matches.
Freezing an artifact certifies its identity, not its classification quality.
"""
import copy
import json
from pathlib import Path

from training.framework.bundle import sha, write, laya_questions, PROMPT
from training.framework.schema import TrainSpec
from training.framework.trainers import snapshot
from production.storage import digest

VERSION = 'frozen-starting-checkpoint-v1'


def freeze(spec, output, *, origin='OFFICIAL_FOUNDATION', adapter=None, quality_receipt=None,
           prompt_path=None, questions_path=None, lineage=None):
    spec = TrainSpec.model_validate(spec)
    if origin not in ('OFFICIAL_FOUNDATION', 'CUSTOMER_DERIVATIVE', 'AI_TEST_DERIVATIVE'):
        raise ValueError('Explicit checkpoint origin required')
    if origin == 'OFFICIAL_FOUNDATION' and adapter is not None:
        raise ValueError('Foundation checkpoints cannot contain a customer/test adapter')
    model = Path(spec.model_path).resolve()
    files = snapshot(model)
    if not files or not any(n.endswith('.safetensors') for n in files):
        raise ValueError('A complete local checkpoint is required')
    if origin == 'OFFICIAL_FOUNDATION' and (model / 'semantic-training-contract.json').exists():
        raise ValueError('A trained Laya checkpoint is not an official foundation')
    adapter_files = snapshot(adapter) if adapter is not None else None
    if adapter is not None and not adapter_files:
        raise ValueError('Empty adapter')
    questions=json.loads(Path(questions_path).read_text()) if questions_path else laya_questions()
    if not isinstance(questions,dict) or set(questions)!=set(laya_questions()):raise ValueError('Frozen starting criteria must cover all nine predicates')
    for key,q in questions.items():
        choices={'VOTABLE','NOT_VOTABLE','UNCERTAIN'} if key=='votability' else {'YES','NO','UNKNOWN'}
        if (not isinstance(q,dict) or q.get('type')!='choice' or not isinstance(q.get('criteria'),dict) or
            set(q['criteria'])!=choices or not isinstance(q.get('instructions'),str) or not q['instructions'].strip() or
            any(not isinstance(v,str) or not v.strip() for v in q['criteria'].values())):
            raise ValueError('Frozen criteria must preserve the typed classification schema: '+key)
    root = Path(output); root.mkdir(parents=True, exist_ok=False)
    (root / 'semantic-prompt.txt').write_text(Path(prompt_path or PROMPT).read_text())
    write(root / 'laya-questions.json', questions)
    condition = {'version': VERSION, 'origin': origin, 'spec': spec.model_dump(),
                 'model_files': files, 'adapter_files': adapter_files,
                 'prompt_sha256': sha(root / 'semantic-prompt.txt'),
                 'questions_sha256': sha(root / 'laya-questions.json'),
                 'quality_receipt': quality_receipt, 'lineage': lineage, 'contains_corpus': False,
                 'automation_enabled': False, 'quality_receipt_supplied': quality_receipt is not None}
    value = {**condition, 'identity': digest(condition), 'model_location': str(model),
             'adapter_location': str(Path(adapter).resolve()) if adapter is not None else None}
    write(root / 'seed.json', value)
    return value


def verify(root, *, model_location=None, adapter_location=None):
    root = Path(root)
    value = json.loads((root / 'seed.json').read_text())
    condition = {k: v for k, v in value.items() if k not in ('identity', 'model_location', 'adapter_location')}
    if value['version'] != VERSION or digest(condition) != value['identity']:
        raise ValueError('Frozen starting checkpoint identity changed')
    bindings = json.loads((root/'LOCAL_BINDINGS.json').read_text()) if (root/'LOCAL_BINDINGS.json').exists() else {}
    model = Path(model_location or bindings.get('model_location') or value['model_location']).resolve()
    adapter = adapter_location or bindings.get('adapter_location') or value['adapter_location']
    if snapshot(model) != value['model_files']:
        raise ValueError('Frozen starting weights changed')
    if (snapshot(adapter) if adapter is not None else None) != value['adapter_files']:
        raise ValueError('Frozen adapter changed')
    if sha(root / 'semantic-prompt.txt') != value['prompt_sha256'] or sha(root / 'laya-questions.json') != value['questions_sha256']:
        raise ValueError('Frozen criteria/prompt changed')
    return {**value, 'model_location': str(model), 'adapter_location': str(adapter) if adapter else None}


def bind(root, *, model_location, adapter_location=None):
    """Explicit installation-local relocation, verified against frozen bytes."""
    value=verify(root,model_location=model_location,adapter_location=adapter_location)
    write(Path(root)/'LOCAL_BINDINGS.json',{'model_location':value['model_location'],
                                        'adapter_location':value['adapter_location'],'identity':value['identity']})
    return value


def training_spec(root, overrides=None):
    """New optimiser, immutable parent; never resume private optimiser/data state."""
    value = verify(root)
    updates = dict(overrides or {})
    protected = {'backend', 'family', 'model_path', 'base_model_id', 'base_revision',
                 'parent_seed_path', 'initial_adapter_path','semantic_output_format'}
    if protected & updates.keys():
        raise ValueError('Training cannot override frozen parent identity')
    spec = {**value['spec'], **updates, 'model_path': value['model_location'],
            'parent_seed_path': str(Path(root).resolve()), 'initial_adapter_path': value['adapter_location']}
    return TrainSpec.model_validate(spec)


def export_derivative(job, output, *, origin):
    if origin not in ('CUSTOMER_DERIVATIVE', 'AI_TEST_DERIVATIVE'):
        raise ValueError('A trained model must remain a derivative')
    from training.framework.runtime import verify_checkpoint
    path, plan, manifest = verify_checkpoint(job)
    if origin == 'CUSTOMER_DERIVATIVE' and any(k.startswith('AI') for k in manifest['label_origins']):
        raise ValueError('AI-trained test weights cannot become a customer-qualified derivative')
    spec = copy.deepcopy(plan['spec'])
    if spec['backend'] == 'LAYA_SDK': spec['model_path'] = str(path / 'checkpoint')
    spec.update(parent_seed_path=None, initial_adapter_path=None)
    return freeze(spec, output, origin=origin,
                  adapter=None if spec['backend'] == 'LAYA_SDK' else path / 'checkpoint',
                  prompt_path=Path(plan['bundle'])/'semantic-prompt.txt',
                  questions_path=Path(plan['bundle'])/'laya-questions.json',
                  lineage={'job_manifest_sha256':sha(path/'model-manifest.json'),
                           'training_bundle_sha256':plan['bundle_manifest_sha256'],
                           'parent_checkpoint_identity':plan['preflight'].get('parent_checkpoint_identity')})


class FrozenModel:
    """Serve a frozen starting artifact without access to any training corpus."""
    def __new__(cls, root):
        from training.framework.runtime import RegisteredModel
        value = verify(root)
        model = RegisteredModel.__new__(RegisteredModel)
        model.root = Path(root)
        model.plan = {'job_id': 'FROZEN:' + value['identity'], 'bundle': str(model.root),
                      'spec': {**value['spec'], 'model_path': value['model_location']}}
        model.manifest = value
        model.spec = TrainSpec.model_validate(model.plan['spec'])
        model.checkpoint_path = Path(value['adapter_location'] or value['model_location'])
        model.checkpoint_manifest_path = model.root / 'seed.json'
        model._load_backend(adapter_path=value['adapter_location'])
        return model
