"""Explicit reload/repeat check, run only after timed A–E inference completes."""
import gc
import json
import time
from pathlib import Path
from semantic_pipeline.models import WholeLaya,NarrowAdapter
from semantic_pipeline.fallback import OllamaFallback
from semantic_pipeline.experiment import ROOT,lines,read,write,verify,now


def canonical_laya(value):
    return {'model_version':value['model_version'],'configuration_version':value['configuration_version'],
        'predicates':{k:{q:v for q,v in a.items() if q in ('value','scores','confidence','margin','evidence','conflict')}
            for k,a in value['predicates'].items()}}


def run_checks(root):
    verify();assert (root/'PREDICTION-COMMIT.json').exists()
    selected=read(root/'validation.json')[:3];out={'checked_at':now(),'scope':'Three validation notices, not proof of global GPU bitwise determinism','laya':{},'llm':{}}
    for name,arm,factory in [('whole-fine','C',lambda:WholeLaya(fine=True)),('narrow-fine','E',NarrowAdapter)]:
        expected={r['id']:r['result']['laya'] for r in lines(root/f'validation-{arm}.jsonl')}
        model=factory();checks=[]
        for row in selected:
            actual=model.analyse(row['text']);checks.append({'id':row['id'],
                'native_predictions_scores_evidence_identical':canonical_laya(actual)==canonical_laya(expected[row['id']])})
        out['laya'][name]=checks;del model;gc.collect()
        import torch
        if torch.backends.mps.is_available():torch.mps.empty_cache()
    llm=OllamaFallback();expected={r['id']:r['result']['llm'] for r in lines(root/'validation-D.jsonl')}
    # Unload only the selected checkpoint after timed work; next request reloads it.
    unload=llm.http('/api/generate',{'model':llm.config['model'],'keep_alive':0})
    out['llm']['unload_response']=unload;checks=[]
    for row in selected:
        actual=llm.analyse(original_text=row['text'],narrative_text=row['text'],structured_facts={},mode='INDEPENDENT')
        old=expected[row['id']]
        checks.append({'id':row['id'],'valid':actual['valid'],'request_hash_identical':actual['request_hash']==old['request_hash'],
            'structured_output_identical':actual['parsed']==old['parsed'],
            'factor_labels_identical':actual.get('parsed') is not None and all(actual['parsed'][k]==old['parsed'][k] for k in ['votability','share_blocking','poa_required','registration_required','beneficial_owner_disclosure_required','holding_confirmation_required','split_voting_restricted','securities_lending_recall_required','other_voting_restriction']),
            'actual':actual})
    out['llm']['checks']=checks
    write(root/'RELOAD-REPRODUCIBILITY.json',out)
    print('Laya reload:',{k:[x['native_predictions_scores_evidence_identical'] for x in v] for k,v in out['laya'].items()})
    print('LLM reload:',[{k:x[k] for k in ('id','valid','request_hash_identical','structured_output_identical','factor_labels_identical')} for x in checks])
    return out

if __name__=='__main__':run_checks(ROOT)
