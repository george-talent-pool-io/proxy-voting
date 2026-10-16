from apps.api.decision_evidence import decision_evidence

def prediction(**updates):
    d=dict(votable='YES',deadline_status='OPEN',share_blocking=False,poa_required=False,other_restriction=True)
    return {'decision':{**d,**updates},'usage':{}}

def test_model_assessment_does_not_invent_iso_or_verified_deadline():
    result=decision_evidence('Shareholders may vote.',{'event_type':'Proxy excerpt'},prediction(),'2026-10-16')
    assert result[0]['message']=='Source document type: Proxy excerpt.'
    assert not any('ISO15022' in r['message'] for r in result)
    deadline=next(r for r in result if 'deadline as open' in r['message'])
    assert deadline['basis']=='Laya assessment; no independently verified deadline'
    assert any(r['message']=='No share-blocking requirement detected by Laya.' for r in result)

def test_registration_is_quoted_without_invented_requirement():
    text='Last year registration was required. This year registration is not required.'
    result=decision_evidence(text,{},prediction(),'2026-10-16')
    excerpt=next(r for r in result if 'quote' in r)
    assert excerpt['quote'] in text and excerpt['message']=='Registration reference in the narrative:'
    assert 'requires review' in excerpt['basis']
    assert not any('Narrative states that registration is required' in r['message'] for r in result)

def test_deterministic_deadline_has_evidence_and_reference():
    p=prediction();p['deadline_evidence']={'reason':'Deterministic comparison of extracted deadline','status':'OPEN','reference':'2026-10-16','candidates':[{'text':'Vote by 20 October 2026'}]}
    result=decision_evidence('Vote by 20 October 2026',{},p,'2026-10-16')
    assert any(r['basis']=='Deterministic deadline comparison' and r['quote']=='Vote by 20 October 2026' for r in result)

def test_no_prediction_no_explanation():assert decision_evidence('registration required',{},None,'2026-10-16')==[]

def test_unknown_and_truncation_are_not_certainty():
    p=prediction(votable='UNCERTAIN',share_blocking=None,deadline_status='UNKNOWN');p['usage']['truncated']=True
    result=decision_evidence('Meeting TBD',{},p,'2026-10-16')
    assert any('could not determine' in r['message'] for r in result)
    assert any('uncertain' in r['message'] for r in result)
    assert any('truncated' in r['message'] for r in result)


def test_every_statement_links_to_its_actual_evidence():
    text='🔎 Café. Registration is not required.'
    result=decision_evidence(text,{'event_type':'Proxy excerpt'},prediction(),'2026-10-16')
    assert all(r['links'] for r in result)
    for item in result:
        for ref in item['links']:
            if ref['kind']=='source':
                assert ref['offset_unit']=='unicode_codepoints'
                assert text[ref['start']:ref['end']]==item['quote']
            elif ref['kind']=='model':assert ref['factor'] in prediction()['decision']
            elif ref['kind']=='metadata':assert ref['key']=='event_type'


def test_calculation_links_preserve_each_candidate_span():
    p=prediction();p['deadline_evidence']={'reason':'Deterministic comparison of extracted deadline','status':'OPEN','reference':'2026-10-16','candidates':[{'text':'Vote by 20 October 2026'},{'text':'Custodian instructions by 19 October 2026'}]}
    text='Vote by 20 October 2026. Custodian instructions by 19 October 2026.'
    item=next(r for r in decision_evidence(text,{},p,'2026-10-16') if r['basis']=='Deterministic deadline comparison')
    assert item['links'][0]['kind']=='deadline'
    assert [text[r['start']:r['end']] for r in item['links'][1:]]==[r['text'] for r in p['deadline_evidence']['candidates']]
