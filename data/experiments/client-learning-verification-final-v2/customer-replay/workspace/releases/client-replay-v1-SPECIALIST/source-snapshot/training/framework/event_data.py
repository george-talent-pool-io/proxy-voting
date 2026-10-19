"""Versioned event datasets; held-out labels never enter training bundles."""
import fcntl
import json
import os
import re
from collections import Counter
from pathlib import Path

from classifier.preprocessing import source_hash, normalise, shingles
from training.framework import jobs
from training.framework.bundle import create_bundle, write, jsonl, sha
from training.framework.schema import Example
from training.framework import events
from apps.api import store

PROTECTED = {'CALIBRATION', 'FROZEN_TEST'}


def content(text):
    return re.sub(r'^\[Message [^\n]+\]\n', '', text, flags=re.MULTILINE)


def fingerprint(text):
    return {source_hash(s) for s in shingles(content(text))}


def register_protected(rows):
    path = jobs.WORKSPACE / 'protected-inputs.jsonl'
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        existing = {json.loads(line)['identity'] for line in f if line.strip()}
        for row in rows:
            if row['split'] not in PROTECTED: continue
            value = {'identity': row['id'] + ':' + row['snapshot_hash'] + ':v2', 'role': row['split'],
                     'source_hash': row['current_text_hash'], 'normalised_hash': source_hash(normalise(row['current_text'])),
                     'message_hashes': [m['source_hash'] for m in row['messages']],
                     'group_id': row['group_id'], 'family': row['family'], 'lexical_fingerprint': sorted(fingerprint(row['current_text']))}
            if value['identity'] not in existing:
                f.write(store.dumps(value) + '\n'); existing.add(value['identity'])
        f.flush(); os.fsync(f.fileno())


def reject_protected(examples):
    paths = [jobs.WORKSPACE / 'protected-inputs.jsonl', jobs.ROOT / 'data/training/exclusions/challenge57-input-fingerprints-v1.jsonl']
    rows = []
    for path in paths:
        if not path.exists(): continue
        with path.open() as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            rows.extend(json.loads(line) for line in f if line.strip())
    hashes = {v for r in rows for v in [r['source_hash'], r['normalised_hash'], *r['message_hashes']]}
    groups = {r['group_id'] for r in rows}; families = {r['family'] for r in rows}
    for e in examples:
        if (e.source_hash in hashes or source_hash(normalise(e.text)) in hashes or
                e.group_id in groups or e.generation_family in families):
            raise ValueError('Protected event input/family cannot enter training or model selection')
        candidate = fingerprint(e.text)
        for r in rows:
            heldout = set(r.get('lexical_fingerprint', []))
            if heldout and len(candidate & heldout) / max(1, len(candidate | heldout)) >= .85:
                raise ValueError('Protected event near-duplicate cannot enter training or model selection')


def freeze_dataset(output, database=None, *, event_ids=None):
    """Snapshot reviews once; no model or training capability reads private keys."""
    views = [events.get(r['id'], database) for r in events.listing(database) if event_ids is None or r['id'] in event_ids]
    if not views: raise ValueError('No learning events')
    selected = []
    for v in views:
        revisions = [r for r in v['reviews'] if r['snapshot_hash'] == v['snapshot_hash']]
        if not revisions: continue
        r = revisions[-1]
        selected.append((v, r))
    if not selected: raise ValueError('No current reviewed events')
    # Verify exact/lexical grouping across ALL roles, not just training material.
    from training.split import duplicate_groups
    groups = duplicate_groups([{'text': content(v['current_text'])} for v, _ in selected])
    seen = {}
    for (v, _), group in zip(selected, groups):
        for identity in [('duplicate', group), ('group', v['group_id']), ('family', v['family'])]:
            if identity in seen and seen[identity] != v['split']:
                raise ValueError('Dataset split leakage; regroup whole families before freezing')
            seen[identity] = v['split']
    root = Path(output); root.mkdir(parents=True, exist_ok=False)
    public = []; answers = []
    for v, r in selected:
        base = {'id': v['id'], 'snapshot_hash': v['snapshot_hash'], 'source_hash': v['current_text_hash'],
                'text': v['current_text'], 'split': v['split'], 'group_id': v['group_id'],
                'generation_family': v['family'], 'review_revision': r['id'],
                'context_kind': v['context_kind'],
                'messages': [{'id': m['id'], 'source_hash': m['source_hash'], 'raw_source': m['raw_source'],
                              'source_type': m['payload']['source_type'], 'source_reference': m['payload']['source_reference'],
                              'parser': m['payload']['parser'], 'state': m['state']}
                             for m in v['messages']]}
        active = next((m for m in v['messages'] if m['id'] == v['active_notification_id']), None)
        base['active_structure'] = active['payload'].get('structure') if active and active['payload']['parser'] == 'PROWIDE' else None
        public.append(base)
        answers.append({'id': v['id'], 'snapshot_hash': v['snapshot_hash'], 'target': r['payload']['target'],
                        'split': v['split'],
                        'expected_deadline_status': r['payload'].get('expected_deadline_status'),
                        'expected_final_status': r['payload'].get('expected_final_status'),
                        'provenance': r['payload']['provenance']})
    jsonl(root / 'inputs.jsonl', public)
    private = root / 'private'; private.mkdir(mode=0o700)
    answer_files = write_role_answers(root, public, answers)
    calibration_parts = write_calibration_parts(root, public, answers)
    manifest = {'version': 'event-dataset-v2', 'created_at': jobs.now(), 'input_file': 'inputs.jsonl',
                'input_sha256': sha(root / 'inputs.jsonl'),
                'answer_files': answer_files,
                'calibration_parts': calibration_parts,
                'roles': dict(Counter(v['split'] for v, _ in selected)),
                'origins': dict(Counter(r['payload']['provenance']['origin'] for _, r in selected)),
                'event_state_policy': events.VERSION, 'automation_enabled': False, 'customer_accuracy': None}
    write(root / 'manifest.json', manifest)
    register_protected([v for v, _ in selected])
    return manifest


def write_role_answers(root, inputs, answers):
    """Curation-only writer; no aggregate cross-role answer file is emitted."""
    by_id = {r['id']: r for r in answers}
    if len(by_id) != len(answers) or set(by_id) != {r['id'] for r in inputs}:
        raise ValueError('Answer/input membership mismatch')
    files = {}
    for role in sorted({r['split'] for r in inputs}):
        path = Path(root) / 'private' / (role.lower() + '-answers.jsonl')
        selected = [{**by_id[r['id']], 'split': role} for r in inputs if r['split'] == role]
        jsonl(path, selected); path.chmod(0o600)
        files[role] = {'file': 'private/' + path.name, 'sha256': sha(path), 'count': len(selected)}
    return files


def write_calibration_parts(root, inputs, answers):
    """Curation-only, physical separation for nested cascade calibration."""
    selected=[r for r in inputs if r['split']=='CALIBRATION']
    if not selected:return {}
    from production.qualification import independent_groups
    groups=independent_groups(selected);members={}
    for row in selected:members.setdefault(groups[row['id']],[]).append(row['id'])
    group_key={g:source_hash(json.dumps(sorted(ids))) for g,ids in members.items()}
    partition={r['id']:('LAYA_STAGE' if int(group_key[groups[r['id']]][:8],16)%2==0 else 'CASCADE_FINAL') for r in selected}
    by_id={r['id']:r for r in answers};result={}
    for part in ('LAYA_STAGE','CASCADE_FINAL'):
        rows=[r for r in selected if partition[r['id']]==part]
        path=Path(root)/'private'/('calibration-'+part.lower()+'-answers.jsonl')
        jsonl(path,[by_id[r['id']] for r in rows]);path.chmod(0o600)
        result[part]={'file':'private/'+path.name,'sha256':sha(path),'ids':[r['id'] for r in rows],
                      'groups':len({groups[r['id']] for r in rows})}
    return result


def load_calibration_answers(dataset,manifest,part,inputs):
    if part not in ('LAYA_STAGE','CASCADE_FINAL'):raise ValueError('Unknown calibration partition')
    entry=manifest.get('calibration_parts',{}).get(part)
    expected='private/calibration-'+part.lower()+'-answers.jsonl'
    if not entry or entry['file']!=expected:raise ValueError('Explicit calibration partition migration required')
    path=Path(dataset)/expected
    if sha(path)!=entry['sha256']:raise ValueError('Calibration partition changed')
    rows=[json.loads(line) for line in path.read_text().splitlines()];keys={r['id']:r for r in rows}
    if len(keys)!=len(rows) or set(keys)!=set(entry['ids']) or set(keys)!={r['id'] for r in inputs}:
        raise ValueError('Calibration partition membership mismatch')
    if any(keys[r['id']]['snapshot_hash']!=r['snapshot_hash'] or r['split']!='CALIBRATION' for r in inputs):
        raise ValueError('Calibration partition source mismatch')
    return keys


def load_answers(dataset, manifest, role, inputs):
    """Open only the requested role, after the caller's prediction receipt."""
    root = Path(dataset)
    if 'answer_files' in manifest:
        entry = manifest['answer_files'].get(role)
        expected_name = f'private/{role.lower()}-answers.jsonl'
        if not entry or entry['file'] != expected_name: raise ValueError('Missing/invalid role answer file')
        path = root / entry['file']
        if sha(path) != entry['sha256']: raise ValueError('Role answer-key checksum changed')
    else:
        # Old single-role fixtures are intrinsically isolated. Multi-role v1
        # archives must be explicitly migrated; never read their mixed labels.
        if set(manifest['roles']) != {role}:
            raise ValueError('Mixed-role legacy keys require explicit separate_answers migration')
        if manifest['answer_file'] != 'private/answer_keys.jsonl': raise ValueError('Invalid legacy answer path')
        path = root / manifest['answer_file']
        if sha(path) != manifest['answer_sha256']: raise ValueError('Answer-key checksum changed')
    rows = [json.loads(s) for s in path.read_text().splitlines()]
    keys = {r['id']: r for r in rows}
    if len(keys) != len(rows) or set(keys) != {r['id'] for r in inputs}:
        raise ValueError('Role answer membership mismatch')
    for r in inputs:
        if keys[r['id']]['snapshot_hash'] != r['snapshot_hash'] or keys[r['id']].get('split', role) != role:
            raise ValueError('Role answer snapshot/split mismatch')
    return keys


def separate_answers(source, output):
    """Explicit data-curation migration. Preserves v1 unchanged; not training.

    The curator necessarily reads existing labels. It grants no blindness claim.
    New scoring processes can thereafter access one role without others.
    """
    import shutil
    source = Path(source); manifest = json.loads((source / 'manifest.json').read_text())
    inputs = []
    for role in manifest['roles']:
        _, rows = load_inputs(source, role); inputs.extend(rows)
    if 'answer_files' in manifest: raise ValueError('Dataset already has role-isolated keys')
    if manifest['answer_file'] != 'private/answer_keys.jsonl' or sha(source / manifest['answer_file']) != manifest['answer_sha256']:
        raise ValueError('Original answer-key checksum changed')
    answers = list(map(json.loads, (source / manifest['answer_file']).read_text().splitlines()))
    root = Path(output); root.mkdir(parents=True, exist_ok=False); (root / 'private').mkdir(mode=0o700)
    shutil.copyfile(source / 'inputs.jsonl', root / 'inputs.jsonl')
    files = write_role_answers(root, inputs, answers)
    new = {k: v for k, v in manifest.items() if k not in ('answer_file', 'answer_sha256')}
    new.update(version='event-dataset-v2', answer_files=files, created_at=jobs.now(),
               migrated_from_manifest_sha256=sha(source / 'manifest.json'),
               migration_scope='Explicit curation; no model training/tuning; not a new blind dataset')
    write(root / 'manifest.json', new)
    return new


def export_reviews(output, database=None):
    """SQL selects development roles before reading ANY target payload."""
    events.initialise(database)
    with store.connect(database) as c:
        ids = [r['id'] for r in c.execute("SELECT id FROM learning_events WHERE split IN ('TRAIN','VALIDATION') ORDER BY id")]
    examples = []
    revisions = []
    for ident in ids:
        v = events.get(ident, database)
        current = [r for r in v['reviews'] if r['snapshot_hash'] == v['snapshot_hash']]
        if not current: continue
        r = current[-1]
        active = next((m for m in v['messages'] if m['id'] == v['active_notification_id']), None)
        from iso_adapter.facts import semantic_facts
        context = semantic_facts(active['payload']['structure']) if active and active['payload']['parser'] == 'PROWIDE' else {}
        examples.append(Example(id=ident, text=v['current_text'], source_hash=v['current_text_hash'],
                        group_id=v['group_id'], generation_family=v['family'], split=v['split'],
                        structured_context=context, target=r['payload']['target'], provenance=r['payload']['provenance']))
        revisions.append({'event_id': ident, 'snapshot_hash': v['snapshot_hash'], 'revision': r['id']})
    reject_protected(examples)
    return create_bundle(examples, output, source_manifest={'type': 'VERSIONED_EVENT_REVIEWS',
                         'roles_read': ['TRAIN', 'VALIDATION'], 'held_out_answers_opened': False,
                         'event_revisions': revisions, 'event_state_policy': events.VERSION})


def load_inputs(dataset, role):
    if role not in events.ROLES: raise ValueError('Unknown dataset role')
    root = Path(dataset); m = json.loads((root / 'manifest.json').read_text())
    if m['input_file'] != 'inputs.jsonl' or sha(root / 'inputs.jsonl') != m['input_sha256']:
        raise ValueError('Frozen input manifest changed')
    rows = [json.loads(line) for line in (root / 'inputs.jsonl').read_text().splitlines()]
    if dict(Counter(r['split'] for r in rows)) != m['roles']: raise ValueError('Frozen role membership changed')
    if len({r['id'] for r in rows}) != len(rows): raise ValueError('Duplicate frozen event ID')
    for r in rows:
        if source_hash(r['text']) != r['source_hash']: raise ValueError('Frozen source changed')
        for message in r.get('messages', []):
            if 'raw_source' in message and source_hash(message['raw_source']) != message['source_hash']:
                raise ValueError('Archived raw-message hash mismatch')
    return m, [r for r in rows if r['split'] == role]
