"""Internal aggregation/Qwen/cascade progress, separate from historical A–E results."""
import json
from pathlib import Path
from fastapi import APIRouter
router=APIRouter(prefix='/api/cascade');ROOT=Path(__file__).resolve().parents[2]/'data/experiments/cascade-v2'
def load(name):
    p=ROOT/name
    try:return json.loads(p.read_text()) if p.exists() else None
    except (json.JSONDecodeError,FileNotFoundError):return None  # Writer may be publishing an immutable artifact.
@router.get('/experiment')
def summary():
    def count(name):
        p=ROOT/name
        return sum(1 for line in p.open() if line.endswith('\n')) if p.exists() else 0
    return {'status':load('LIVE-STATUS.json'),'summary':load('SUMMARY.json'),'primary':load('PRIMARY-MODEL-SELECTION.json'),
        'routing':load('ROUTING-SELECTION.json'),'aggregation':load('AGGREGATION-BLOCKING-DELTA-v2.json'),
        'baseline':load('PRE_AGGREGATION_FIX_BASELINE.json')['correct_assertions'] if (ROOT/'PRE_AGGREGATION_FIX_BASELINE.json').exists() else None,
        'progress':{d:{a:count(f'{d}-{a}.jsonl') for a in ['D1','D2','D3','C1','C2','C3','A','B','C_SELECTIVE','E_SELECTIVE']} for d in ['validation','challenge','complete']},
        'automation_enabled':False,'customer_accuracy':None,'scope':'Synthetic/authored research only; no production/customer accuracy established'}
