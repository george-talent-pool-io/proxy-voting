"""One Laya document decision, with cheap source-exact evidence candidates.

The locator never determines or changes a semantic label. Candidate passages
are not an independent entailment verification. Conflicts/conditions are review
signals. Missing positive evidence cannot qualify for automatic acceptance.
"""
import hashlib
import re
import time
from pathlib import Path
from cascade.aggregation import ANCHORS, HISTORY, SUPERSEDE
from hybrid.semantics import passages
from semantic_pipeline.schema import PREDICATES
from semantic_pipeline.evidence import verify_evidence
from semantic_pipeline.decision import decide
from training.framework.runtime import RegisteredModel

VERSION='whole-notice-scoped-evidence-v3'
SOURCE_SHA256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
NEGATIVE=re.compile(r'not (?:be )?(?:required|mandatory|necessary|needed|applicable|a condition|block|immobili|restrict)|no .{0,65}(?:requirement|required|applies|condition|blocking)|need not|does not|do not|waiv|exempt|optional|voluntar|without|freely|unrestricted|unnecessary|no longer',re.I)
REQUIRED=re.compile(r'cannot.{0,60}without|reject.{0,50}unless|not.{0,40}accept.{0,40}unless|only after',re.I)
AFFIRMATIVE=re.compile(r'\b(?:must|shall|mandatory|required|prerequisite|eligible|only)\b|will be.{0,25}(?:block|immobili|froze)|cannot.{0,30}(?:sell|transfer)',re.I)
CONDITIONAL=re.compile(r'depending on|only if.{0,50}(?:physical|residen|attendance)|which route.{0,30}not',re.I)
OTHER=r'professional.investor|retail holder|residen|minimum (?:position|holding)|paper.only|wet.signature|in.person.only|notari[sz].{0,20}signature'
ALIASES={
 'share_blocking':r'block|immobili|freez|froz|lock|dispos|transfer|cannot sell|prevent.{0,20}sale',
 'poa_required':r'power.of.attorney|\bpoa\b|attorney.{0,20}(?:document|mandate|authori)|notari[sz]ed.{0,20}voting authority',
 'split_voting_restricted':r'split|divid.{0,35}vot|different.{0,25}vot|one voting direction|cast.{0,30}identical|voted.{0,25}same way',
}


class WholeNotice:
    def __init__(self,job,*,model_factory=RegisteredModel):
        self.model=model_factory(job)
        if self.model.spec.backend!='LAYA_SDK':raise ValueError('WholeNotice requires official Laya')

    def analyse(self,text,**kwargs):
        began=time.perf_counter();result=self.model.analyse(text,**kwargs)
        spans=list(passages(text))
        if len(spans)>10000:raise ValueError('Too many source passages; no silent truncation')
        conflicts=list(result['reconciliation']['conflicts']);trace={}
        for key in PREDICATES:
            pred=result['predicates'][key]
            if str(pred.get('source','')).startswith('PROWIDE'):continue
            value=pred['value'];candidate=[];positive=[];negative=[]
            anchor=(r'vot|ballot|shareholder|meeting|dividend|redemption|tender|distribution|stock split' if key=='votability' else OTHER if key=='other_voting_restriction' else ALIASES.get(key,ANCHORS[key]))
            for span in spans:
                words=span['text']
                if not re.search(anchor,words,re.I) or HISTORY.search(words):continue
                context=text[max(0,span['start']-80):span['start']]
                if re.search(r'PRELIMINARY CONDITION|Historical illustration',context,re.I) and not SUPERSEDE.search(words):continue
                neg=bool(NEGATIVE.search(words)) and not REQUIRED.search(words)
                (negative if neg else positive).append(span)
            if value in ('YES','VOTABLE'):candidate=positive
            elif value in ('NO','NOT_VOTABLE'):candidate=negative if key!='votability' else positive+negative
            conditional=any(CONDITIONAL.search(s['text']) for s in positive+negative)
            # A topic mention (an address for POAs, for example) is not an
            # affirmative requirement. The locator cannot contradict a native
            # NO solely because a keyword appears without an obligation.
            asserted_positive=[s for s in positive if AFFIRMATIVE.search(s['text']) or REQUIRED.search(s['text'])]
            contrary=(value=='NO' and asserted_positive and not negative or value=='YES' and negative and not asserted_positive)
            opposing=negative if value in ('YES','VOTABLE') else positive if value in ('NO','NOT_VOTABLE') else []
            current_contradiction=key!='votability' and bool(asserted_positive and negative)
            if conditional or contrary or current_contradiction:
                pred['conflict']=True;conflicts.append(key+':SCOPED_EVIDENCE_CONFLICT_OR_CONDITION')
            # Later definitive source wording is a candidate, not a label rule.
            chosen=candidate[-1:] if not conditional else []
            pred['evidence']=[{**verify_evidence(text,s['text']), 'source':'SCOPED_SOURCE_CANDIDATE',
                              'entailment_independently_verified':False} for s in chosen]
            rank=sorted(pred['scores'].values(),reverse=True)
            pred.update(source='REGISTERED_LAYA_WHOLE_SCOPED_EVIDENCE',
                        margin=rank[0]-rank[1],candidate_passage_count=len(candidate),
                        supporting_passage_count=len(candidate),contradicting_passage_count=len(opposing),
                        evidence_status='EXACT_SOURCE_CANDIDATE' if chosen else 'UNAVAILABLE',
                        evidence_method=VERSION)
            trace[key]={'candidates':[{'start':s['start'],'end':s['end']} for s in candidate],
                        'conditional':conditional,'contrary_signal':bool(contrary),'current_contradiction':current_contradiction,
                        'model_label_unchanged':True}
        result['reconciliation']={'predicates':{k:result['predicates'][k] for k in PREDICATES},'conflicts':sorted(set(conflicts))}
        result['decision']=decide(result['predicates'],result['deadline'],conflicts)
        result.update(evidence_locator=trace,passage_inference_invoked=False,
                      evidence_runtime_version=VERSION,evidence_runtime_sha256=SOURCE_SHA256)
        result['latencies']['total_ms']=(time.perf_counter()-began)*1000
        return result

    def close(self):self.model.close()
