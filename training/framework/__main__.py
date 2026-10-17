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
    args = p.parse_args()
    if args.command == 'export-corpus':
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
    else:
        from training.framework.trainers import versions
        result = {'versions': versions(), 'backends': ['LAYA_SDK', 'TRANSFORMERS_PEFT', 'MLX_QLORA'],
                  'llm_families': ['QWEN', 'GLM', 'OTHER_CAUSAL_LM'],
                  'network_inference': False, 'automatic_download': False,
                  'exact_checkpoint_compatibility_requires_smoke_test': True}
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == '__main__':
    main()
