"""Render preserved model evidence; never changes challenge expectations."""
import json
from collections import Counter
from pathlib import Path

REASONS = {
'agm':('Unsupported restriction','Blocking is asserted although no blocking language appears; the error is in a factor, not status precedence.'),
'blocking':('Votability under restriction','Blocking is detected, but the explicit permission to vote is classified UNCERTAIN. A restriction appears to compete with the voting-opportunity decision.'),
'poa':('Votability under restriction','Required POA is detected; conditional permission to vote is missed. An additional blocking assertion has no textual support.'),
'past-deadline':('Temporal reasoning','An explicit dated instruction deadline is not resolved; votability is also lost. Calendar comparison and opportunity semantics are conflated.'),
'blocked-and-poa':('Votability under restriction','Both named restrictions are detected, but conditional participation becomes UNCERTAIN. The derived status follows that erroneous factor.'),
'two-dates':('Votability under restriction','Deadline selection is correct, but a notice requesting instructions becomes UNCERTAIN; unsupported restrictions are also present.'),
'record-date':('Record date / blocking confusion','A record date is treated as blocking and the explicit vote as NO. Record ownership eligibility is different from immobilising shares.'),
'quoted-old':('Historical context','The expired archived deadline overrides the current future deadline despite the explicit current-year distinction; voting opportunity is also missed.'),
'voluntary-tender':('Negation / event confusion','An explicit exclusion of a ballot is ignored. A voluntary election appears to be mistaken for a shareholder vote.'),
'historical-results':('Deadline without evidence','Historical results are correctly non-votable but a current passed deadline is asserted without an instruction deadline.'),
'eligibility':('Other restriction omission','Class-specific entitlement is missed. Blocking and a passed deadline are also asserted without supporting language.'),
'partial':('Other restriction omission','The explicit prohibition on split voting is missed and the accompanying voting permission becomes UNCERTAIN.'),
'record-ordinary':('Record date / blocking confusion','The model asserts blocking despite an explicit statement that trading is not blocked.'),
'contradiction':('Conflict handling','The model chooses YES despite equally scoped incompatible statements and no supersession evidence.'),
'same-day':('Temporal reasoning','A date-only reference cannot determine whether a timezone-specific same-day cutoff has elapsed. PASSED is unjustified.'),
'historic-fiscal':('Historical context','The non-deadline fiscal date appears to distract from the explicit upcoming instruction cutoff; voting opportunity is also missed.'),
'non-voting-bond':('Negation / event confusion','Mandatory interest payment and explicit denial of any ballot are classified as a voting opportunity.'),
'poa-waived':('Historical context','The waiver factor is correct, but the current-year permission to vote is lost amid historical/current contrast.'),
'historic-quote-only':('Historical context','The explicitly archived proxy invitation is not resolved as no current opportunity.'),
'false-urgency':('Negation / event confusion','Repetition of vote in an explicitly non-actionable marketing archive produces uncertainty and unsupported restrictions.'),
'de-vote':('Multilingual understanding','The German sentence grants voting/instruction rights; the model misses this. Translation/domain coverage is a hypothesis, not established causation.'),
'fr-poa':('Multilingual understanding','The French sentence explicitly requires a notarised proxy to vote; both the voting permission and POA factor are missed.'),
'no-date':('Deadline without evidence','A referral to the custodian supplies no actual cutoff. OPEN has no supporting date.'),
'today-date':('Temporal reasoning','With only a date and no cutoff time on the reference day, OPEN is unjustified.'),
'negotiation':('Negation / event confusion','A completed board vote is different from a requested shareholder ballot; the explicit exclusion is not resolved to NO.'),
'foreign-restriction':('Other restriction omission','Local regulatory permission for foreign holders is an explicit eligibility restriction; it is missed alongside voting permission.'),
'blank-like':('Insufficient context','TBD fields cannot establish either a voting opportunity or blocking. The model supplies both rather than abstaining.'),
}

def main():
    source=Path('data/reports/semantic-challenge.json');p=json.loads(source.read_text());bad=[x for x in p['examples'] if not x['passed']]
    assert {x['id'] for x in bad}==set(REASONS)
    counts=Counter(REASONS[x['id']][0] for x in bad)
    failed_fields=Counter(k for x in bad for k,v in x['checks'].items() if not v)
    lines=['# Laya baseline failure analysis','',f"Preserved baseline: {p['passed']}/{p['cases']} authored cases pass; {len(bad)} fail. Reference date: {p['reference_date']}. These are partial-field assertions on authored adversarial examples, not customer accuracy.",'','## Primary diagnostic categories','', '| Diagnostic category | Failed cases |','|---|---:|']
    lines += [f'| {k} | {v} |' for k,v in counts.most_common()]
    lines += ['', 'Counts assign one primary diagnostic per failed case and sum to 27. They describe observable error patterns; they do not establish neural causes. Several cases have multiple errors.', '',f'Failed asserted fields (overlap): `{dict(failed_fields)}`.', '', '## Findings before any new training', '', 'The baseline already uses five independent native Laya choice questions. It is not a seven-way softmax. The seven labels are derived display statuses. Factorisation alone therefore cannot be claimed as a new remedy or explain these failures. There are several error families, with recurring failure to retain YES votability when restrictions or historical context appear. Unsupported restrictions and invented deadline states also occur.', '', 'The minimum winning probability is a policy score, not a probability that every factor is correct. High-confidence factor errors can hide behind a low aggregate score. Native SDK confidence is retained below separately; it is not the winner–runner-up margin.', '', 'No expected answer has been changed. Unasserted factors are shown but are not scored as verified truths. All five factors were evaluated without truncation on these failed examples. Likely reasons below are testable hypotheses inferred from the text and outputs, not model-generated explanations.', '', 'Model revision: `'+p['model_version']+'`; config: `'+p['configuration_version']+'`.', '', '## All 27 failures','']
    for x in bad:
        cat,reason=REASONS[x['id']];r=x['result']
        lines += [f"### {x['id']} — {cat}",'','**Source text**','', '> '+x['text'],'','**Expected asserted fields**', '```json',json.dumps(x['expected'],ensure_ascii=False,indent=2),'```','**Observed factors and derived status**','```json',json.dumps(x['observed'],ensure_ascii=False,indent=2),'```',f"Failed assertions: {', '.join(k for k,v in x['checks'].items() if not v)}. Aggregate policy score: {r['confidence']:.4f}.",'','| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |','|---|---|---|---:|---:|']
        for f,s in r['scores'].items():
            a=sorted(s.items(),key=lambda v:-v[1]);raw=r['raw_answers'][f]
            lines.append(f"| {f} | {', '.join(f'{k}={v:.4f}' for k,v in s.items())} | {a[0][0]} | {a[0][1]-a[1][1]:.4f} | {raw.get('confidence',0):.4f} |")
        lines += ['', '**Likely reason / next discriminating check:** '+reason+' Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.','']
    lines += ['## Challenge contamination audit','','The earlier `data/models/synthetic-smoke-v1` mechanics checkpoint used challenge fixtures. It is excluded from candidate comparison and must never be reported against the challenge as independent evidence. The official base checkpoint was not changed by that smoke run. No domain fine-tuned candidate exists yet.']
    Path('data/reports/LAYA_BASELINE_FAILURE_ANALYSIS.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'primary_patterns':counts,'failed_fields':failed_fields}))
if __name__=='__main__':main()
