"""Intentional real Qwen Direct/xhigh plumbing tests; quality is measured separately."""
import os,json
from pathlib import Path
import pytest
from cascade.fallback import CommonFallback
from semantic_pipeline.reconcile import llm_factors
pytestmark=[pytest.mark.qwen_local,pytest.mark.skipif(os.environ.get('RUN_QWEN_LOCAL')!='1',reason='RUN_QWEN_LOCAL=1 executes pinned local Qwen; Thinking is intentionally slow')]

@pytest.mark.parametrize('condition',['QWEN_DIRECT','QWEN_THINKING'])
def test_real_qwen_supported_modes_schema_and_reasoning_privacy(condition):
    configs=json.loads(Path('data/experiments/cascade-v2/LLM-CONFIGS-v3.json').read_text());model=CommonFallback(configs[condition])
    source='A current shareholder vote is offered. Owners must provide a notarised power of attorney. Shares will not be blocked.'
    r=model.analyse(original_text=source,narrative_text=source,structured_facts={},mode='INDEPENDENT')
    assert r['invoked'] and r['valid'],r.get('error')
    assert r['raw_response']['eval_count']>0
    assert 'laya_diagnostic' not in json.loads(r['request']['messages'][1]['content'])
    d=r['raw_response']['thinking_diagnostics'];assert not d['raw_reasoning_stored']
    assert (d['characters']>0)==(condition=='QWEN_THINKING')
    assert 'thinking' not in r['raw_response']['message']
    facts=llm_factors(r)
    for k,quotes in r['evidence_validation']['predicates'].items():
        for q in quotes:
            if q['valid']:assert source[q['start']:q['end']]==q['text']
            else:assert facts[k]['value'] in ('UNKNOWN','UNCERTAIN')
