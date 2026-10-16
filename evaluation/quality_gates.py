"""Conservative proposed research gates, not regulatory requirements or an activation API."""
import json,math
from pathlib import Path
from evaluation.metrics import wilson_lower

def load_gates(path=None):
    cfg=json.loads(Path(path or Path(__file__).with_name('quality_gates.json')).read_text())
    for k,v in cfg.items():
        if k=='version':continue
        if not isinstance(v,(int,float)) or not math.isfinite(v) or v<0:raise ValueError('Invalid quality gate')
        if any(s in k for s in ['RECALL','F1','RATE','PRECISION','COVERAGE','THRESHOLD']) and v>1:raise ValueError('Quality rate outside [0,1]')
    return cfg

def assess(rows,metrics,frozen_labels=False,validation_threshold=None,config=None):
    cfg=config or load_gates();reasons=[];evidence={}
    def minimum(name,value,key):
        evidence[name]=value
        if value is None or not math.isfinite(value) or value<cfg[key]:reasons.append(f'{name}: {value if value is not None else "not measured"}; requires ≥ {cfg[key]}')
    if not frozen_labels:reasons.append('Independent expert-reviewed frozen test labels are not locked')
    minimum('Test size',len(rows),'MIN_TEST_SIZE');minimum('Independent test groups',len({r.get('group_id',r['id']) for r in rows}),'MIN_INDEPENDENT_TEST_GROUPS')
    minimum('Votable support',sum(r.get('true_votable')=='YES' for r in rows),'MIN_VOTABLE_SUPPORT')
    for flag in ['share_blocking','poa_required','other_restriction']:
        minimum(flag+' support',sum(r.get('true_decision',{}).get(flag) is True for r in rows),'MIN_RESTRICTION_SUPPORT')
    minimum('Votable recall',metrics.get('actionable_voting_recall'),'MIN_VOTABLE_RECALL');minimum('Macro F1',metrics.get('macro_f1'),'MIN_MACRO_F1')
    factors=['votable','share_blocking','poa_required','other_restriction','deadline_status']
    exact=lambda r:all(r['true_decision'][k]==r['decision'][k] for k in factors)
    high=[r for r in rows if r['confidence']>=cfg['HIGH_CONFIDENCE_THRESHOLD']]
    rate=sum(not exact(r) for r in high)/len(high) if high else None
    evidence['High confidence error rate']=rate
    if rate is None or rate>cfg['MAX_HIGH_CONFIDENCE_ERROR_RATE']:reasons.append('High confidence error rate is unmeasured or exceeds maximum')
    if validation_threshold is None or not 0<=validation_threshold<=1:
        reasons.append('No automation threshold has qualified on validation data');auto=[]
    else:auto=[r for r in rows if r['eligible'] and r['confidence']>=validation_threshold]
    # Treat any incorrect member of a source group as an incorrect group.
    groups={}
    for r in auto:
        g=r.get('group_id',r['id']);groups[g]=groups.get(g,True) and exact(r)
    lower=wilson_lower(sum(groups.values()),len(groups))
    minimum('Automation precision 95% lower bound',lower,'MIN_AUTOMATION_PRECISION')
    minimum('Automation coverage',len(auto)/len(rows) if rows else None,'MIN_AUTOMATION_COVERAGE')
    return {'status':'QUALITY GATE NOT MET' if reasons else 'QUALITY GATE PASSED','passed':not reasons,'reasons':reasons,'evidence':evidence,'configuration':cfg,'automation_enabled':False,'note':'Proposed research criteria; not regulatory requirements. Passing this report does not activate automation.'}
