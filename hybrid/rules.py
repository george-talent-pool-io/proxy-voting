"""Explicit experimental business policy. All decisions remain human reviewed."""
VERSION='hybrid-policy-1'
RESTRICTIONS=('share_blocking','poa_required','registration_required','beneficial_owner_disclosure_required','split_voting_restricted','securities_lending_recall_required','other_voting_restriction')

def decide(facts):
    def out(status,rule):return {'classification':status,'rule':rule,'rule_version':VERSION,'automation_enabled':False,'manual_review_required':True}
    if facts.get('conflict') or facts.get('quarantined'):return out('UNCERTAIN_MANUAL_REVIEW','R1 conflicting, malformed or unresolved lifecycle evidence')
    if facts.get('cancelled'):return out('NOT_VOTABLE','R2 current event cancellation; retain history')
    if facts.get('votable')=='NO':return out('NOT_VOTABLE','R3 no current voting opportunity')
    if facts.get('votable')!='YES':return out('UNCERTAIN_MANUAL_REVIEW','R4 current voting opportunity not established')
    if facts.get('deadline_status')=='PASSED':return out('DEADLINE_PASSED','R5 controlling response deadline passed')
    if any(facts.get(k)=='YES' for k in RESTRICTIONS):return out('VOTABLE_WITH_RESTRICTION','R6 one or more independently supported restrictions')
    if facts.get('deadline_status')!='OPEN' or any(facts.get(k,'UNKNOWN')=='UNKNOWN' for k in RESTRICTIONS):return out('UNCERTAIN_MANUAL_REVIEW','R7 incomplete deadline/restriction information')
    return out('VOTABLE','R8 actionable vote; open response deadline; no detected restriction')
