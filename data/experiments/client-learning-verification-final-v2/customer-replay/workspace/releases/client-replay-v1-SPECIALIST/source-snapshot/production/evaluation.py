"""Input-only capability for protected prediction generation. No review queries."""
import json
import os
import uuid
from pathlib import Path
from apps.api import store
from training.framework import releases
from training.framework.event_data import load_inputs
from training.framework.bundle import write, sha
from semantic_pipeline.schema import PREDICATES


def input_metadata(row):
    with store.connect() as c: found = c.execute('SELECT * FROM client_metadata WHERE event_id=?', (row['id'],)).fetchone()
    meta = dict(found) if found else {'language': 'UNKNOWN', 'population': 'UNDECLARED'}
    meta['input_type'] = ('LENIENT_ISO_RECOVERABLE' if row.get('context_kind') == 'RECOVERED_REVIEW_CONTEXT' else
                          'PROWIDE_PARSEABLE' if (row.get('active_structure') or {}).get('parser') == 'PROWIDE' or
                          any(m.get('parser') == 'PROWIDE' for m in row['messages']) else 'UNSTRUCTURED_NOTICE')
    return meta


def predict(dataset, role, release, output, reference, check=None, *, calibration_partition=None):
    """Persist complete immutable prediction rows before returning to a scorer."""
    manifest, rows = load_inputs(dataset, role)
    if calibration_partition:
        if role!='CALIBRATION':raise ValueError('Calibration partition requires CALIBRATION role')
        entry=manifest.get('calibration_parts',{}).get(calibration_partition)
        if not entry:raise ValueError('Calibration partition missing; freeze a new dataset')
        ids=set(entry['ids']);rows=[r for r in rows if r['id'] in ids]
        if {r['id'] for r in rows}!=ids:raise ValueError('Calibration partition input mismatch')
    if not rows: raise ValueError('Empty evaluation role')
    if any('raw_source' not in message for row in rows for message in row.get('messages', [])):
        raise ValueError('Legacy event snapshot lacks raw-message provenance; explicitly freeze a new dataset before evaluation')
    output = Path(output); output.mkdir(parents=True, exist_ok=False)
    model = releases.ReleaseModel(release, sealed=role != 'VALIDATION'); predictions = []
    try:
        with (output / 'predictions.jsonl').open('x') as f:
            for row in rows:
                if check: check()
                from iso_adapter.facts import semantic_facts, deadline
                structure = row.get('active_structure')
                d = deadline(structure, reference) if structure else None
                meta=input_metadata(row)
                routing_context={k:meta[k] for k in ('language','population')} if getattr(getattr(model,'spec',None),'laya_calibrator_id',None) else {}
                if routing_context:routing_context['input_type_context']=meta['input_type']
                result = model.analyse(row['text'], use_iso=False, reference=reference,
                            structured_context=semantic_facts(structure) if structure else {},
                            deadline_override=d if d and d['comparisons'] else None, **routing_context)
                conflicts = result['reconciliation']['conflicts']
                for key in PREDICATES:
                    pred = result['predicates'][key]
                    for ev in pred.get('evidence', []):
                        quote = ev.get('text'); links = []
                        if quote and (quote in row['text'] or pred.get('source', '').startswith('PROWIDE')):
                            for message in row['messages']:
                                # Structure evidence must come from the frozen
                                # active notification, never a superseded value.
                                if pred.get('source', '').startswith('PROWIDE') and (not structure or message['raw_source'] != structure['raw_source']): continue
                                start = message['raw_source'].find(quote)
                                if start >= 0: links.append({'message_id': message['id'], 'source_hash': message['source_hash'], 'start': start, 'end': start + len(quote), 'text': quote, 'valid': True})
                        ev['event_source_links'] = links; ev['valid'] = bool(links)
                        if not links: conflicts.append(key + ':EVENT_EVIDENCE_INVALID')
                if row.get('context_kind') == 'RECOVERED_REVIEW_CONTEXT': conflicts.append('RECOVERED_CONTEXT_NOT_AUTHORITATIVE')
                if conflicts:
                    from semantic_pipeline.decision import decide
                    result['decision'] = decide(result['predicates'], result['deadline'], conflicts)
                result['event_context_kind'] = row.get('context_kind')
                value = {'id': row['id'], 'snapshot_hash': row['snapshot_hash'], 'group': row['group_id'],
                         'family': row['generation_family'], 'text': row['text'], 'meta': input_metadata(row), 'result': result}
                f.write(store.dumps(value) + '\n'); f.flush(); os.fsync(f.fileno()); predictions.append(value)
    finally: model.close()
    write(output / 'PREDICTIONS_SAVED.json', {'sha256': sha(output / 'predictions.jsonl'), 'count': len(predictions),
          'created_at': store.now(), 'dataset_sha256': sha(Path(dataset) / 'manifest.json'), 'reference': reference,
          'calibration_partition':calibration_partition, 'answer_keys_opened': False})
    return manifest, rows, predictions
