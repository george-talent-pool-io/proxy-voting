"""Append-only artifacts, exact pins and capability-limited dataset access."""
import hashlib,json,os,subprocess
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
STUDY=ROOT/'data/experiments/qwen-domain-v1'
CORPUS=ROOT/'data/domain-corpus/v4'
def now():return datetime.now(timezone.utc).isoformat()
def digest(s):
    payload=s if isinstance(s,str) else json.dumps(s,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False)
    return hashlib.sha256(payload.encode()).hexdigest()
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(2**20),b''):h.update(b)
    return h.hexdigest()
def read(p):return json.loads(Path(p).read_text())
def rows(p):
    with Path(p).open() as f:return [json.loads(line) for line in f if line.strip()]
def write(p,value):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:json.dump(value,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
def append(p,value):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('a') as f:f.write(json.dumps(value,ensure_ascii=False,allow_nan=False)+'\n');f.flush();os.fsync(f.fileno())
def freeze_baseline():
    from cascade.study import verify_core
    verify_core();p=STUDY/'QWEN_DIRECT_PRE_DOMAIN_TRAINING.json'
    if p.exists():
        old=read(p)
        for name,h in old['files'].items():assert sha(ROOT/name)==h,name
        return old
    names=['cascade/fallback.py','cascade/proxy_semantic_common_v1.txt','semantic_pipeline/schema.py','semantic_pipeline/pipeline.py','semantic_pipeline/reconcile.py','semantic_pipeline/decision.py','semantic_pipeline/evidence.py','classifier/preprocessing.py','hybrid/parser.py','classifier/deadlines.py','tests/fixtures/semantic.json','data/experiments/cascade-v2/challenge-D2.jsonl','data/experiments/cascade-v2/LLM-CONFIGS-v3.json','data/experiments/cascade-v2/COMMON-CONDITION-FREEZE.json']
    from cascade.reporting import load
    from semantic_pipeline.metrics import summarize
    metrics=summarize(load('challenge','D2'));assert metrics['correct_assertions']==92
    value={'created_at':now(),'name':'QWEN_DIRECT_PRE_DOMAIN_TRAINING','git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'model_config':read(ROOT/'data/experiments/cascade-v2/LLM-CONFIGS-v3.json')['QWEN_DIRECT'],
        'normalisation':'Historical Direct receives original text; evidence offsets refer to original text. New NFC views must retain original separately.',
        'files':{name:sha(ROOT/name) for name in names},'challenge_assertions':95,'challenge_correct':92,'partial_cases':54,'final_status_labelled_cases':4,
        'automation_enabled':False,'customer_accuracy':None}
    write(p,value);return value
def load_training(manifest_path,split='TRAIN'):
    if split not in ('TRAIN','VALIDATION'):raise ValueError('Training/model-selection can only access TRAIN or VALIDATION')
    m=read(manifest_path);entry=m['splits'][split];base=Path(manifest_path).parent.resolve();p=(base/entry['labels']).resolve()
    try:relative=p.relative_to(base)
    except ValueError:raise ValueError('Protected labels cannot enter training: dataset boundary escape')
    if 'private' in relative.parts or any(w in str(relative).casefold() for w in ('frozen','answer_key','calibration','adversarial','ood_test')):raise ValueError('Protected labels cannot enter training')
    if sha(p)!=entry['labels_sha256']:raise ValueError('Dataset hash changed')
    out=rows(p);allowed=set(entry['ids'])
    if len(out)!=len(allowed) or {r['id'] for r in out}!=allowed or any(r['split']!=split for r in out):raise ValueError('Split membership changed')
    return out
def load_inputs(manifest_path,split):
    m=read(manifest_path);e=m['splits'][split];p=Path(manifest_path).parent/e['inputs']
    if sha(p)!=e['inputs_sha256']:raise ValueError('Input hash changed')
    out=rows(p)
    forbidden={'expected','facts','fact_specification','evidence_truth','calibration_target'}
    if any(forbidden & r.keys() for r in out):raise ValueError('Labels leaked into inference inputs')
    return out
