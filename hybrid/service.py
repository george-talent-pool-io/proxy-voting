"""Service-facing safety guards around the preserved experimental pipeline.
The frozen v1 benchmark remains in pipeline.py. No model/aggregation criterion is
changed here. Unknown event codes must not become a negative meeting assertion.
"""
from hybrid.pipeline import analyse as frozen_analyse
from hybrid.parser import facts,MEETINGS
VERSION='hybrid-service-1'
KNOWN_NONMEETINGS={'DVCA','TEND','INFO','DSCL','RHTS'}

def inspect(raw,model=None,message_type=None,evaluation_time='2026-10-16T12:00:00+00:00'):
    result=frozen_analyse(raw,model,message_type,evaluation_time)
    codes={f['value'] for f in facts(result['parsed'],'caev')}
    if codes and not codes<=MEETINGS|KNOWN_NONMEETINGS:
        result['structured_facts']['meeting_event']='UNKNOWN'
        result['review_reasons'].append('Unrecognised CAEV: literal value preserved; no negative meeting inference')
    result['service_version']=VERSION
    return result
