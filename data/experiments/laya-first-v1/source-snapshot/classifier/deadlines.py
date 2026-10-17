"""Conservative English deadline extraction. Never guesses missing timezones or years.
A date-only reference compares whole dates; same-day cutoffs remain UNKNOWN.
Ambiguous, historic, negated or unsupported formats abstain for human review.
"""
import re
from datetime import date,datetime,time,timedelta,timezone

VERSION='deadline-rules-v1.1'
MONTHS={name:i for i,name in enumerate(['January','February','March','April','May','June','July','August','September','October','November','December'],1)}
DATE=re.compile(r'\b(?P<day>\d{1,2})\s+(?P<month>'+ '|'.join(MONTHS)+r')\s+(?P<year>20\d{2})\b',re.I)
CUE=re.compile(r'(?:vot(?:e|es|ing)\s+(?:instructions?\s+)?(?:deadline|closes?|closed|by)|(?:voting\s+)?instructions?\b[^.;\n]{0,100}\b(?:by|due|before|deadline)|custodian\s+(?:deadline|cutoff))',re.I)
NEGATED=re.compile(r'\b(?:no|not|unspecified|unknown)\b[^.;]{0,35}\b(?:deadline|cutoff)\b|\b(?:historic|historical|archive|archived|last year|fiscal year)\b',re.I)
OFFSETS={'UTC':0,'GMT':0,'CET':1,'CEST':2,'JST':9,'TOKYO TIME':9}

def extract_deadline(text,reference,deadline_present='YES'):
    ref=datetime.fromisoformat(reference.replace('Z','+00:00')) if 'T' in reference else date.fromisoformat(reference)
    if isinstance(ref,datetime) and ref.tzinfo is None:raise ValueError('Evaluation timestamp must include timezone')
    evidence=[];rejected=[]
    for sentence in re.split(r'[.;\n]+',text):
        if not CUE.search(sentence):continue
        if NEGATED.search(sentence):rejected.append(sentence.strip());continue
        for match in DATE.finditer(sentence):
            try:d=date(int(match['year']),MONTHS[match['month'].title()],int(match['day']))
            except ValueError:rejected.append(sentence.strip());continue
            # A clause with several dates is not resolved by taking its first/earliest date.
            if len(list(DATE.finditer(sentence)))!=1:rejected.append(sentence.strip());continue
            tail=sentence[match.end():]
            clock=re.search(r'\b(\d{1,2}):(\d{2})\s*(UTC|GMT|CET|CEST|JST|Tokyo time)\b',tail,re.I)
            instant=None
            if clock:
                try:instant=datetime.combine(d,time(int(clock[1]),int(clock[2])),timezone(timedelta(hours=OFFSETS[clock[3].upper()])))
                except ValueError:rejected.append(sentence.strip());continue
            kind='custodian' if re.search(r'custod(?:ian|y)|our\s+(?:desk|cutoff)',sentence,re.I) else 'unspecified'
            evidence.append({'date':d.isoformat(),'instant':instant.isoformat() if instant else None,'kind':kind,'text':sentence.strip()})
    result={'status':'UNKNOWN','rule_version':VERSION,'reference':reference,'candidates':evidence,'rejected_clauses':rejected,'reason':'No unambiguous current voting deadline'}
    if deadline_present!='YES':result['reason']='Semantic deadline presence is not YES';return result
    # Custodian precedence applies only when explicit. Conflicting same-scope candidates abstain.
    candidates=[e for e in evidence if e['kind']=='custodian'] or evidence
    if not candidates or len({(e['date'],e['instant']) for e in candidates})!=1:return result
    e=candidates[0];d=date.fromisoformat(e['date']);refdate=ref.date() if isinstance(ref,datetime) else ref
    if isinstance(ref,datetime) and e['instant']:
        result['status']='PASSED' if datetime.fromisoformat(e['instant'])<ref else 'OPEN'
    elif e['instant']:
        # A UTC reference date represents an interval, not an invented midnight instant.
        instant=datetime.fromisoformat(e['instant']);start=datetime.combine(refdate,time(),timezone.utc)
        if instant<start:result['status']='PASSED'
        elif instant>=start+timedelta(days=1):result['status']='OPEN'
        else:result['reason']='Cutoff falls inside the reference UTC day; reference time is missing';return result
    elif d<refdate:result['status']='PASSED'
    elif d>refdate:result['status']='OPEN'
    else:result['reason']='Same day without comparable timestamp and cutoff';return result
    result['reason']='Deterministic comparison of extracted deadline';return result
