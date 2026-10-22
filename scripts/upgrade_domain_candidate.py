"""Bounded AI-only learning candidate, selected on development data alone.

This is an engineering experiment, not a supplied/qualified customer model.
No challenge, calibration or frozen-test answers are opened by this driver.
"""
import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

from semantic_pipeline.schema import PREDICATES
from semantic_pipeline.metrics import summarize
from training.framework import jobs, seeds
from training.framework.bundle import create_bundle, load_bundle, sha, write
from training.framework.resources import model_resource
from training.framework.trainers import training_label_support
from training.framework.whole_runtime import WholeNotice
from scripts.qualify_frozen_learning import benchmark

CRITICAL = ('votability', 'share_blocking', 'poa_required', 'registration_required')


def diverse_sample(rows, count, role):
    """Deterministic label/family coverage; only a declared development role."""
    if role not in ('TRAIN', 'VALIDATION') or any(e.split != role for e in rows):
        raise ValueError('Only a single declared TRAIN or VALIDATION role is allowed')
    if count < 1 or count > len(rows):
        raise ValueError('Sample exceeds available development support')
    remaining = sorted(rows, key=lambda e: e.source_hash)
    selected = []; counts = Counter()
    def bins(e):
        return [(k, getattr(e.target, k)) for k in PREDICATES] + [('family', e.generation_family)]
    for _ in range(count):
        best = max(remaining, key=lambda e: sum(1 / (1 + counts[b]) for b in bins(e)))
        selected.append(best); remaining.remove(best); counts.update(bins(best))
    return selected


def run(ident, *, execute=False):
    output = Path('data/experiments') / ident
    output.mkdir(parents=True, exist_ok=False)
    source = jobs.member('bundles', 'ai-domain-development-v1')
    manifest, rows = load_bundle(source)
    train = diverse_sample([e for e in rows if e.split == 'TRAIN'], 128, 'TRAIN')
    validation = diverse_sample([e for e in rows if e.split == 'VALIDATION'], 120, 'VALIDATION')
    _, replay = load_bundle(jobs.member('bundles', 'customer-domain-adaptation-v1'))
    source_ids={e.id for e in rows};source_hashes={e.source_hash for e in rows}
    # The earlier adaptation cohort already contains replay from this domain
    # corpus. Do not count those notices twice or move a development example.
    train += diverse_sample([e for e in replay if e.split == 'TRAIN' and
                             e.id not in source_ids and e.source_hash not in source_hashes], 32, 'TRAIN')
    bundle = jobs.member('bundles', ident)
    bundle_manifest = create_bundle(train + validation, bundle, source_manifest={
        'source_bundle_sha256': sha(source/'manifest.json'), 'roles_read':['TRAIN','VALIDATION'],
        'held_out_answers_opened': False, 'scope':'AI_AUTHORED_DEVELOPMENT_ONLY'})
    parent_job = jobs.member('jobs', 'customer-adaptation-uncontended-v1-8epoch')
    parent = jobs.member('seeds', ident + '-parent')
    seeds.export_derivative(parent_job, parent, origin='AI_TEST_DERIVATIVE')
    spec = seeds.training_spec(parent, {
        'epochs':1, 'learning_rate':.00005, 'encoder_learning_rate':.0000125,
        'batch_size':8, 'gradient_accumulation':2, 'freeze_encoder':False,
        'max_length':2048, 'seed':42, 'laya_gradient_checkpointing':True,
        'laya_sdk_validation':False, 'mps_memory_fraction':.45, 'training_timeout_seconds':1800})
    job = jobs.member('jobs', ident)
    plan = jobs.prepare(bundle, spec, job)
    write(output/'PLAN.json', {
        'scope':'AI_AUTHORED_DEVELOPMENT_PILOT_NOT_CUSTOMER_QUALIFICATION',
        'source_manifest_sha256':sha(source/'manifest.json'),
        'bundle_sha256':sha(bundle/'manifest.json'), 'counts':bundle_manifest['counts'],
        'source_counts':manifest['counts'], 'label_support':training_label_support(train+validation),
        'parent_identity':plan['preflight']['parent_checkpoint_identity'],
        'job':str(job), 'training_budget':'One full-encoder epoch; no further run selected from these results',
        'selection':'Most validation assertions with no new critical positive misses versus parent',
        'roles_read':['TRAIN','VALIDATION'], 'protected_answers_opened':False,
        'shipped_model':False, 'automation_enabled':False, 'customer_accuracy':None})
    if not execute:
        return {'prepared':str(job),'execution_started':False}
    with (output/'training.log').open('xb') as log:
        subprocess.run([sys.executable,'-m','training.framework','execute',str(job)],
                       stdout=log,stderr=subprocess.STDOUT,check=True,timeout=2100)
    inputs = [{'id':e.id,'text':e.text,'group':e.group_id,'evaluation_time':'2026-10-18T12:00:00+00:00'}
              for e in validation]
    truth = {e.id:{k:getattr(e.target,k) for k in PREDICATES} for e in validation}
    conditions = {
        'FOUNDATION':lambda:WholeNotice(jobs.member('seeds','frozen-learning-v3-laya'),model_factory=seeds.FrozenModel),
        'PREVIOUS_DOMAIN_CHECKPOINT':lambda:WholeNotice(parent_job),
        'BROADER_DOMAIN_CANDIDATE':lambda:WholeNotice(job)}
    reports = {}
    with model_resource('bounded-domain-candidate-validation'):
        for name, factory in conditions.items():
            out = output/name
            predictions = benchmark(factory,inputs,out)
            report = summarize([{**r,'expected':truth[r['id']]} for r in predictions])
            write(out/'metrics.json',report); reports[name]=report
    def missed(report):
        return {(e['id'],e['field']) for e in report['failures']
                if e['field'] in CRITICAL and e['expected'] in ('YES','VOTABLE')}
    previous=reports['PREVIOUS_DOMAIN_CHECKPOINT'];candidate=reports['BROADER_DOMAIN_CANDIDATE']
    new_misses=sorted(missed(candidate)-missed(previous))
    selected='BROADER_DOMAIN_CANDIDATE' if not new_misses and candidate['correct_assertions']>previous['correct_assertions'] else 'PREVIOUS_DOMAIN_CHECKPOINT'
    result={'scope':'AI_AUTHORED_DEVELOPMENT_ONLY', 'validation':reports,'selected':selected,
            'new_critical_false_negatives':[{'id':i,'predicate':p} for i,p in new_misses],
            'training_result':json.loads((job/'result.json').read_text()),
            'protected_answers_opened':False,'shipped_model':False,
            'automation_enabled':False,'customer_accuracy':None}
    write(output/'result.json',result)
    return {'selected':selected,'report':str(output/'result.json')}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('id');parser.add_argument('--execute',action='store_true')
    args=parser.parse_args();print(json.dumps(run(args.id,execute=args.execute)))
