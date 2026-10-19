"""Export latest complete revisions; human review is not a prerequisite for R&D."""
import json

from apps.api import store
from training.framework.bundle import create_bundle
from training.framework.schema import Example, Provenance
from semantic_pipeline.schema import PREDICATES


def export_reviews(output, database=None):
    with store.connect(database) as c:
        exists = c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='domain_reviews'").fetchone()
        if not exists:
            raise ValueError('No complete-schema reviews exist')
        # Do not even fetch test labels into this training export process.
        rows = [dict(r) for r in c.execute('''SELECT n.id,n.text,n.source_hash,n.group_id,n.split,n.metadata,
            r.id AS revision,r.reviewer,r.created_at,r.label,r.context
            FROM notices n JOIN domain_reviews r ON r.id=(
                SELECT max(id) FROM domain_reviews WHERE record_id=n.id)
            WHERE n.split IN ('train','validation') ORDER BY n.id''')]
    examples = []
    for r in rows:
        label = json.loads(r['label'])
        context = json.loads(r['context'])
        target = {k: label[k] for k in PREDICATES}
        target.update(evidence={k: context.get('semantic_evidence', {}).get(k, []) for k in PREDICATES},
                      deadline_information=context.get('deadline_information', {'deadline_mentioned': False, 'deadline_text': None}),
                      ambiguities=[])
        examples.append(Example(id=r['id'], text=r['text'], source_hash=r['source_hash'],
             group_id=r['group_id'], split=r['split'].upper(), language=json.loads(r['metadata']).get('language', 'en'),
             target=target, provenance=Provenance(origin=context.get('label_origin', 'HUMAN_REVIEWED'),
                 author=r['reviewer'], model_id=context.get('reviewer_model'),
                 method=context.get('validation_type', 'Historical UI review; expertise not independently authenticated'),
                 reviewed_at=r['created_at'], expert_attested=context.get('domain_expert_attested', False),
                 source_reference='domain_reviews:' + r['id'], revision=str(r['revision']))))
    return create_bundle(examples, output, source_manifest={'source': 'append-only domain_reviews',
        'revision_count': len(rows), 'roles_read': ['TRAIN', 'VALIDATION'], 'held_out_answers_opened': False})
