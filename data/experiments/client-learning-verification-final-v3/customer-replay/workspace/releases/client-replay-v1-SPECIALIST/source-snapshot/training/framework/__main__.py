"""python -m training.framework --help"""
import argparse
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description='Auditable Laya and local-LLM development training')
    sub = p.add_subparsers(dest='command', required=True)
    c = sub.add_parser('export-corpus')
    c.add_argument('manifest'); c.add_argument('output')
    c.add_argument('--language', default='en'); c.add_argument('--limit-per-split', type=int)
    c = sub.add_parser('export-reviews')
    c.add_argument('output'); c.add_argument('--database')
    c = sub.add_parser('prepare')
    c.add_argument('bundle'); c.add_argument('spec'); c.add_argument('output')
    for name in ['execute', 'status']:
        sub.add_parser(name).add_argument('job')
    c = sub.add_parser('evaluate-validation')
    c.add_argument('job'); c.add_argument('output')
    sub.add_parser('capabilities')
    c = sub.add_parser('freeze-starting-checkpoint'); c.add_argument('spec'); c.add_argument('output')
    c = sub.add_parser('verify-starting-checkpoint'); c.add_argument('checkpoint')
    c = sub.add_parser('prepare-from-checkpoint'); c.add_argument('checkpoint'); c.add_argument('bundle'); c.add_argument('overrides'); c.add_argument('output')
    c = sub.add_parser('prepare-campaign'); c.add_argument('spec'); c.add_argument('id')
    c = sub.add_parser('run-campaign'); c.add_argument('id')
    c = sub.add_parser('campaign-status'); c.add_argument('id')
    c = sub.add_parser('separate-answers'); c.add_argument('source_id'); c.add_argument('new_id')
    args = p.parse_args()
    if args.command == 'freeze-starting-checkpoint':
        from training.framework.seeds import freeze
        result = freeze(json.loads(Path(args.spec).read_text()), args.output)
    elif args.command == 'verify-starting-checkpoint':
        from training.framework.seeds import verify
        result = verify(args.checkpoint)
    elif args.command == 'prepare-from-checkpoint':
        from training.framework.seeds import training_spec
        from training.framework.jobs import prepare
        result = prepare(args.bundle, training_spec(args.checkpoint, json.loads(Path(args.overrides).read_text())), args.output)
    elif args.command == 'export-corpus':
        from training.framework.bundle import from_domain_corpus
        result = from_domain_corpus(args.manifest, args.output, language=args.language,
                                    limit_per_split=args.limit_per_split)
    elif args.command == 'export-reviews':
        from training.framework.reviews import export_reviews
        result = export_reviews(args.output, args.database)
    elif args.command == 'prepare':
        from training.framework.jobs import prepare
        result = prepare(args.bundle, json.loads(Path(args.spec).read_text()), args.output)
    elif args.command == 'execute':
        from training.framework.jobs import execute
        result = execute(args.job)
    elif args.command == 'status':
        from training.framework.jobs import status
        result = status(args.job)
    elif args.command == 'evaluate-validation':
        from training.framework.evaluate import evaluate_validation
        result = evaluate_validation(args.job, args.output)
    elif args.command == 'separate-answers':
        from training.framework import jobs
        from training.framework.event_data import separate_answers
        result = separate_answers(jobs.member('event-datasets', args.source_id), jobs.member('event-datasets', args.new_id))
    elif args.command in ('prepare-campaign', 'run-campaign', 'campaign-status'):
        from training.framework import campaigns, jobs
        root = jobs.member('campaigns', args.id)
        if args.command == 'prepare-campaign': result = campaigns.prepare(json.loads(Path(args.spec).read_text()), root)
        elif args.command == 'run-campaign': result = campaigns.run(root)
        else: result = campaigns.status(root)
    else:
        from training.framework.trainers import versions
        result = {'versions': versions(), 'backends': ['LAYA_SDK', 'TRANSFORMERS_PEFT', 'MLX_QLORA'],
                  'llm_families': ['QWEN', 'GLM', 'OTHER_CAUSAL_LM'],
                  'network_inference': False, 'automatic_download': False,
                  'exact_checkpoint_compatibility_requires_smoke_test': True}
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == '__main__':
    main()
