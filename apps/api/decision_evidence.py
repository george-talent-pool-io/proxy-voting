"""Source-linked display summary. Does not alter inference or invent model reasoning."""
import re

VERSION='source-summary-v2'

def decision_evidence(text,metadata,prediction,reference_date):
    if not prediction:return []
    items=[]
    def source_link(quote):
        start=text.find(quote)
        return [{'kind':'source','start':start,'end':start+len(quote),'offset_unit':'unicode_codepoints','label':'View source passage'}] if start>=0 else []
    def add(message,basis,quote=None,factor=None,links=None):
        refs=links if links is not None else [{'kind':'model','factor':factor,'label':'View model scores and criteria'}]
        items.append({'message':message,'basis':basis,'links':refs,**({'quote':quote} if quote else {})})
    document_type=metadata.get('event_type')
    if document_type and document_type!='UNKNOWN':
        add(f'Source document type: {document_type}.','Source metadata; not a verified ISO15022 event field',links=[{'kind':'metadata','key':'event_type','label':'View source field'}])
    d=prediction['decision']
    voting={'YES':'Laya identified a shareholder voting opportunity.','NO':'Laya found no current shareholder voting opportunity.','UNCERTAIN':'Laya could not determine whether a voting opportunity exists.'}
    add(voting[d['votable']],'Laya assessment',factor='votable')
    deadline=prediction.get('deadline_evidence')
    if deadline and deadline.get('reason')=='Deterministic comparison of extracted deadline' and deadline.get('status')==d['deadline_status'] and deadline.get('candidates'):
        status={'OPEN':'open','PASSED':'passed'}.get(d['deadline_status'])
        if status:
            quotes=[c['text'] for c in deadline['candidates']]
            add(f'The extracted voting deadline is {status} at reference {deadline["reference"]}.','Deterministic deadline comparison',quote=' | '.join(quotes),links=[{'kind':'deadline','label':'View deadline comparison'}]+[link for q in quotes for link in source_link(q)])
    elif d['deadline_status']!='UNKNOWN':
        add(f'Laya assessed the voting deadline as {d["deadline_status"].lower()} at reference date {reference_date}.','Laya assessment; no independently verified deadline',factor='deadline_status')
    else:add('The voting deadline could not be established.','Laya assessment' if not deadline else 'Deadline extraction/comparison result',links=[{'kind':'deadline','label':'View unresolved deadline evidence'}] if deadline else [{'kind':'model','factor':'deadline_status','label':'View model scores and criteria'}])
    for key,label in [('other_restriction','an additional voting restriction'),('poa_required','a power-of-attorney requirement'),('share_blocking','a share-blocking requirement')]:
        if d[key] is True:add(f'Laya detected {label}.','Laya assessment',factor=key)
        elif key=='share_blocking':
            add('No share-blocking requirement detected by Laya.' if d[key] is False else 'The share-blocking requirement is uncertain.','Laya assessment; absence of detection is not proof of absence',factor=key)
    # Quote source text literally; do not interpret negation, historic scope or registration
    # applicability through keyword matching, or claim the model attended to this sentence.
    registration=next((s.strip() for s in re.split(r'(?<=[.!?])\s+|\n+',text) if re.search(r'\b(?:registration|register(?:ed|ing)?)\b',s,re.I) and len(s.strip())<=500),None)
    if registration:add('Registration reference in the narrative:','Literal source excerpt; applicability requires review',quote=registration,links=source_link(registration))
    if prediction.get('usage',{}).get('truncated'):
        add('The model processed a truncated notice; review the complete source.','Recorded model token usage',links=[{'kind':'usage','label':'View processing record'}])
    return items
