import copy
import json
import math
import pytest
from pydantic import ValidationError
from classifier.preprocessing import normalise,source_hash,shingles
from classifier.schema import Decision,Status,ClassificationResult
from classifier.thresholds import Thresholds
from classifier.laya_classifier import config_version,load_config,LayaClassifier
from training.split import duplicate_groups,partition,verify_isolation

@pytest.mark.parametrize('text,expected',[
 ('<p>Vote <b>now</b></p><script>ignore()</script>','Vote now'),
 ('<html><style>p{}</style><body>AGM&nbsp;notice</body></html>','AGM notice'),
 ('\t AGM\n\r notice  ','AGM notice'),('Cafe\u0301','Café'),
 ('股東は議決権を行使できます。','股東は議決権を行使できます。'),
 ('',''),('   ',''),('Votes < 10 and > 2','Votes < 10 and > 2'),
 ('Do not block shares.','Do not block shares.'),('<p>hello <invalid>world','hello world')])
def test_normalise(text,expected):assert normalise(text)==expected

@pytest.mark.parametrize('text',[None,{},[],42,True,b'bytes'])
def test_malformed(text):
    with pytest.raises(TypeError):normalise(text)

def test_hash_source_unchanged():
    assert source_hash('a  b')!=source_hash('a b')
    assert source_hash('Café')!=source_hash('Cafe\u0301')
    assert source_hash('hello')=='2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'

def test_long_notice():
    text='Meeting notice. '*100000
    assert len(normalise(text))==len(text)-1

def test_idempotent():
    for x in ['<p>AGM&nbsp;test</p>','Cafe\u0301',' a\t b ']:assert normalise(normalise(x))==normalise(x)

@pytest.mark.parametrize('kwargs,status',[
 ({'votable':'YES'},Status.VOTABLE),({'votable':'NO'},Status.NOT_VOTABLE),({'votable':'UNCERTAIN'},Status.UNCERTAIN_MANUAL_REVIEW),
 ({'votable':'YES','share_blocking':True},Status.SHARE_BLOCKING),
 ({'votable':'YES','poa_required':True},Status.POA_REQUIRED),
 ({'votable':'YES','share_blocking':True,'poa_required':True},Status.VOTABLE_WITH_RESTRICTION),
 ({'votable':'YES','other_restriction':True},Status.VOTABLE_WITH_RESTRICTION),
 ({'votable':'YES','deadline_status':'PASSED','poa_required':True},Status.DEADLINE_PASSED),
 ({'votable':'YES','poa_required':None},Status.UNCERTAIN_MANUAL_REVIEW),
 ({'votable':'NO','deadline_status':'PASSED'},Status.NOT_VOTABLE)])
def test_mapping(kwargs,status):assert Decision(**kwargs).status()==status

@pytest.mark.parametrize('confidence,expected',[(.99,'AUTO_CLASSIFY'),(.98,'AUTO_CLASSIFY'),(.7,'CLASSIFY_AND_REVIEW'),(.6999,'MANUAL_REVIEW'),(None,'MANUAL_REVIEW'),(float('nan'),'MANUAL_REVIEW'),(float('inf'),'MANUAL_REVIEW'),(-.1,'MANUAL_REVIEW'),(1.1,'MANUAL_REVIEW')])
def test_thresholds(confidence,expected):assert Thresholds(automation_enabled=True).action(confidence)==expected

def test_disabled_policy():assert Thresholds().action(.999)=='CLASSIFY_AND_REVIEW'
def test_guardrail():assert Thresholds(automation_enabled=True).action(.999,blocked=True)=='MANUAL_REVIEW'
@pytest.mark.parametrize('high,review',[(.5,.7),(-1,0),(2,.5),(float('nan'),.1)])
def test_bad_thresholds(high,review):
    with pytest.raises(ValueError):Thresholds(high,review)

def test_configuration(config,tmp_path):
    c=copy.deepcopy(config); c['evaluation_date']='2025-10-11'
    assert config_version(c)!=config_version(config)
    p=tmp_path/'config.json';p.write_text(json.dumps(c));assert load_config(p)['evaluation_date']=='2025-10-11'
    c['evaluation_date']='not-a-date';p.write_text(json.dumps(c))
    with pytest.raises(ValueError):load_config(p)

def test_grouping_transitive():
    base='Shareholders may submit voting instructions for the Annual General Meeting of the company held on 10 October 2025. Shares will be blocked until the meeting concludes.'
    records=[{'text':base},{'text':base.replace('2025','2026')},{'text':base+' Contact the bank.'},{'text':'Information about debt obligations unrelated to shareholders.'}]
    groups=duplicate_groups(records)
    assert groups[0]==groups[1]==groups[2] and groups[0]!=groups[3]
    assert groups==duplicate_groups(records)

def test_filing_group():assert len(set(duplicate_groups([{'text':'AGM voting','source_file':'same'},{'text':'Unrelated compensation','source_file':'same'}])))==1

def test_split():
    assert partition('same')==partition('same')
    rows=[{'group_id':'same','split':'train'},{'group_id':'same','split':'test'}]
    with pytest.raises(ValueError,match='Leakage'):verify_isolation(rows)

@pytest.mark.parametrize('key',['group_id','source_file','source_hash'])
def test_each_leakage_key(key):
    with pytest.raises(ValueError):verify_isolation([{key:'same','split':'train'},{key:'same','split':'test'}])

def test_serialization(classifier):
    r=classifier.classify('AGM notice')
    assert ClassificationResult.model_validate_json(r.model_dump_json())==r
    assert r.confidence==.99
    assert r.raw_answers['votable']['confidence']==.94 # SDK entropy preserved, not used as probability.
    assert isinstance(r.scores['votable'],dict)
    assert r.action!='AUTO_CLASSIFY'

@pytest.mark.parametrize('value',[float('nan'),float('inf'),-.1,1.1])
def test_invalid_score_rejected(classifier,value):
    r=classifier.classify('notice').model_dump();r['scores']['votable']['YES']=value
    with pytest.raises(ValidationError):ClassificationResult.model_validate(r)

def test_score_sum_rejected(classifier):
    r=classifier.classify('notice').model_dump();r['scores']['votable']['YES']=.5
    with pytest.raises(ValidationError):ClassificationResult.model_validate(r)

def test_empty_classifier(classifier):
    with pytest.raises(ValueError):classifier.classify(' ')

def test_over_limit(classifier):
    with pytest.raises(ValueError):classifier.classify('x'*2_000_001)

def test_truncated_guard(classifier):
    raw=classifier.agent.predict_batch(['notice'],classifier.config['questions'])[0];raw['usage']['truncated']=True
    r=classifier._decode(raw,1)
    assert r.action=='MANUAL_REVIEW' and any('truncated' in x for x in r.review_reasons)

def test_unknown_deadline_guard(classifier):
    raw=classifier.agent.predict_batch(['notice'],classifier.config['questions'])[0]
    raw['answers']['deadline_status']['choice']='UNKNOWN';raw['answers']['deadline_status']['probabilities']={'OPEN':.005,'PASSED':.005,'UNKNOWN':.99}
    assert classifier._decode(raw,1).action=='MANUAL_REVIEW'

def test_option_order_survives_json_storage(config):
    from classifier.laya_classifier import prepare_config
    stored=json.loads(json.dumps(config,sort_keys=True))
    assert list(stored['questions']['votable']['criteria'])!=list(config['questions']['votable']['criteria'])
    restored=prepare_config(stored)
    assert list(restored['questions'])==list(config['questions'])
    assert list(restored['questions']['votable']['criteria'])==['YES','NO','UNCERTAIN']
    assert config_version(restored)==config_version(config)

def test_order_changes_config_hash(config):
    from classifier.laya_classifier import prepare_config
    changed=copy.deepcopy(config);changed['option_order']['votable'].reverse()
    assert config_version(prepare_config(changed))!=config_version(config)

def test_legacy_order_refused(config):
    from classifier.laya_classifier import prepare_config
    config.pop('option_order')
    with pytest.raises(ValueError,match='option_order'):prepare_config(config)

@pytest.mark.parametrize('numerator,denominator',[(1,2),(17,20),(1,1)])
def test_exact_prefix_join_matches_brute_force(numerator,denominator):
    from training.split import exact_pairs
    import random
    rng=random.Random(42);sets=[]
    for i in range(30):
        s=set(rng.sample(range(100),rng.randint(10,60)));sets.extend([s,s|set(rng.sample(range(100,110),rng.randint(0,5)))])
    actual={(min(i,j),max(i,j)) for i,j,_ in exact_pairs(sets,numerator,denominator)}
    expected={(i,j) for i in range(len(sets)) for j in range(i+1,len(sets)) if denominator*len(sets[i]&sets[j])>=numerator*len(sets[i]|sets[j])}
    assert actual==expected

def test_issuer_metadata_enrichment_is_explicit():
    from scripts.profile_data import enrich_publishers
    records=[{'id':'a','source_file':'one','issuer':'Known','provenance_metadata':{'company':'Known'}},
             {'id':'b','source_file':'one','issuer':'Unknown','provenance_metadata':{}},
             {'id':'c','source_file':'conflict','issuer':'First','provenance_metadata':{'company':'First'}},
             {'id':'d','source_file':'conflict','issuer':'Second','provenance_metadata':{'company':'Second'}},
             {'id':'e','source_file':'conflict','issuer':'Unknown','provenance_metadata':{}}]
    assert enrich_publishers(records)==1
    assert records[1]['issuer']=='Known' and records[1]['issuer_provenance']['record_id']=='a'
    assert records[1]['provenance_metadata']=={} and records[4]['issuer']=='Unknown'
