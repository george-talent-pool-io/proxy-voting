"""Explicit opt-in application bridge to the frozen selected cascade."""
import os,time
from pathlib import Path
from semantic_pipeline.fallback import DisabledFallback
from cascade.study import ROOT,verify_core,read
from cascade.models import CapableSpecialist
from cascade.aggregation import AggregationConfig
from cascade.routing import Policy
from cascade.pipeline import execute
from cascade.fallback import CommonFallback

def classify(text,architecture,*,model=None,fallback=None):
    started=time.perf_counter()
    if architecture not in ('C','E'):raise ValueError('Selective v2 supports C/E application paths')
    if not (ROOT/'FINAL-SELECTION-FREEZE.json').exists():raise RuntimeError('Selective cascade selection is not frozen yet; experiment still running')
    verify_core()
    final=read(ROOT/'FINAL-SELECTION-FREEZE.json')
    from semantic_pipeline.experiment import sha
    for p,digest in final['selection_files'].items():
        if sha(p)!=digest:raise RuntimeError('Frozen selective-cascade selection changed')
    if model is None:
        baseline=read(ROOT/'PRE_AGGREGATION_FIX_BASELINE.json')
        for path,digest in baseline['existing_checkpoint_and_inference_freeze']['files'].items():
            if str(path).startswith('data/models/') and sha(path)!=digest:raise RuntimeError('Frozen Laya checkpoint bytes changed')
        model=CapableSpecialist(AggregationConfig(**read(ROOT/'AGGREGATION-SELECTION-v2.json')['selected']['config']))
    if fallback is None:
        enabled=os.environ.get('LLM_ENABLED','false').lower()=='true'
        cfg=read(ROOT/'LLM-CONFIGS-v3.json')[final['primary_model']['selected']]
        fallback=CommonFallback(cfg) if enabled else DisabledFallback()
    requested_parser=architecture=='E';detected=None;use_parser=False
    if requested_parser:
        import re
        from hybrid.parser import parse
        from semantic_pipeline.pipeline import prepare
        hint=bool(re.search(r'(?:^|[\r\n]):\d{2}[A-Z]?:',text) or '{2:' in text)
        detected=parse(text) if hint else None
        use_parser=bool(detected and detected['kind'] in ('VALID_ISO15022','PARTIAL_ISO15022'))
        narrative=prepare(text,use_parser)['narrative']
    else:narrative=text
    if narrative:r=execute(text,precomputed=model.analyse(narrative),fallback=fallback,policy=Policy(**final['routing']['policy']),use_parser=use_parser)
    else:r=execute(text,fallback=fallback,policy=Policy(**final['routing']['policy']),use_parser=use_parser)
    if requested_parser and not use_parser:
        r['architecture']='E';r['parser_status']='NOT_APPLICABLE'
        r['input_routing_reason']='Full notice retained: no supported valid/partial ISO structure'
        if detected:r['input_detection']={'kind':detected['kind'],'tags':[f['tag'] for f in detected['fields']]}
    r['latencies']['cold_application_total_ms']=(time.perf_counter()-started)*1000
    r['latencies']['total_ms']=r['latencies']['cold_application_total_ms']
    r['latencies']['timing_scope']='Application request includes model construction and inference; separate from warmed study benchmark'
    r['selection_freeze_sha256']=sha(ROOT/'FINAL-SELECTION-FREEZE.json');r['customer_accuracy']=None
    return r
