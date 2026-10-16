"""Score a NEW run into its own directory; never overwrite another run's report."""
import argparse
from semantic_pipeline.experiment import ROOT,verify
from semantic_pipeline.reporting import report
from evaluation.ae_scoring import correct
from evaluation.ae_analysis import analyse
from evaluation.ae_date_ablation import analyse as dates

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--oracle',action='store_true');args=parser.parse_args()
    verify();path=ROOT/'EVALUATION.md'
    if path.exists():raise FileExistsError('Report exists; use a new experiment directory')
    report(ROOT,report_path=path);correct(ROOT,report_path=path);analyse(ROOT,report_path=path);dates(ROOT,report_path=path)
    if args.oracle:
        from evaluation.ae_oracle import analyse as oracle
        oracle(ROOT,report_path=path)
    print('Report:',path)
