"""Evidence locators never replace the specialist's semantic decision."""
from types import SimpleNamespace
from production.evidence_basis import negative_basis
from production.confidence import feature_row
from training.framework.whole_runtime import WholeNotice
from tests.unit.test_learning_comparison import result
from semantic_pipeline.schema import PREDICATES


def model(value):
    class NativeDocumentDouble:
        spec=SimpleNamespace(backend='LAYA_SDK')
        calls=0
        def __init__(self,*a):pass
        def analyse(self,text,**kw):
            self.calls+=1;r=result()
            for key in PREDICATES:
                p=r['predicates'][key]
                v='VOTABLE' if key=='votability' else value if key=='share_blocking' else 'NO'
                choices=('VOTABLE','NOT_VOTABLE','UNCERTAIN') if key=='votability' else ('YES','NO','UNKNOWN')
                p.update(value=v,scores={c:.98 if c==v else .01 for c in choices},source='EXPLICIT_TEST_NATIVE',evidence=[])
                if v=='NO':p['negative_basis']=negative_basis(text,'TEST_ONLY_NATIVE')
            return r
        def close(self):pass
    return WholeNotice('EXPLICIT_TEST_DOUBLE',model_factory=NativeDocumentDouble)


def test_whole_notice_one_native_call_and_exact_evidence():
    runtime=model('YES');text='Shareholders may vote. Voting instructions immobilise the instructed shares until the meeting ends.'
    out=runtime.analyse(text)
    assert runtime.model.calls==1 and not out['passage_inference_invoked']
    assert out['predicates']['share_blocking']['value']=='YES'
    quote=out['predicates']['share_blocking']['evidence'][0]
    assert quote['text'] in text and not quote['entailment_independently_verified']


def test_locator_flags_negation_conflict_without_flipping_native_label():
    out=model('YES').analyse('Shareholders may vote. Shares will not be blocked.')
    p=out['predicates']['share_blocking']
    assert p['value']=='YES' and p['conflict'] and p['evidence']==[]
    assert out['decision']['manual_review_required']
    f=feature_row('Shareholders may vote. Shares will not be blocked.','share_blocking',p,language='en',input_type='UNSTRUCTURED_NOTICE')
    assert f['force_review'] and f['confidence'] is None


def test_unmentioned_negative_is_a_complete_source_basis_not_a_quote():
    text='Shareholders may vote on the resolutions.'
    p=model('NO').analyse(text)['predicates']['share_blocking']
    assert p['value']=='NO' and not p['evidence'] and p['negative_basis']['complete_source_processed']
    f=feature_row(text,'share_blocking',p,language='en',input_type='UNSTRUCTURED_NOTICE')
    assert f['features']['evidence_mode']=='COMPLETE_SOURCE_NEGATIVE'


def test_opposing_current_passages_remain_visible_and_force_review():
    text='Shareholders may vote. Shares will be blocked. Shares will not be blocked.'
    out=model('YES').analyse(text);p=out['predicates']['share_blocking']
    assert p['value']=='YES'  # Locator does not substitute for semantic inference.
    assert p['supporting_passage_count']==1 and p['contradicting_passage_count']==1
    assert out['evidence_locator']['share_blocking']['current_contradiction']
    assert p['conflict'] and out['reconciliation']['conflicts']


def test_unnecessary_requirement_is_not_treated_as_positive():
    text='Shareholders may vote. Share blocking is unnecessary for this vote.'
    p=model('NO').analyse(text)['predicates']['share_blocking']
    assert p['value']=='NO' and not p.get('conflict')
    assert p['evidence'][0]['text']=='Share blocking is unnecessary for this vote.'


def test_topic_mention_alone_does_not_contradict_document_negative():
    text='Shareholders may vote. The helpdesk answers questions about share blocking.'
    p=model('NO').analyse(text)['predicates']['share_blocking']
    assert p['value']=='NO' and not p.get('conflict')
    assert not p['evidence']  # No invented negative quotation.


def test_unsealed_bootstrap_cannot_smuggle_automation_qualification():
    import pytest
    from apps.api.production import Inference
    with pytest.raises(ValueError,match='cannot attach'):
        Inference(release_id='base',event_ids=['a'],review_only_unsealed=True,qualification_id='promoted')
    request=Inference(release_id='base',event_ids=['a'],review_only_unsealed=True)
    assert not request.qualification_id
