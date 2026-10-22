"""Explicit shared customer-status policy, independent from automation permission."""
from semantic_pipeline.schema import RESTRICTIONS
VERSION='semantic-decision-3'

def decide(factors, deadline, conflicts=(), quarantined=False):
    def out(status, rule, reasons=()):
        return {'classification':status,'rule':rule,'rule_version':VERSION,
            'manual_review_required':status=='UNCERTAIN_MANUAL_REVIEW','automation_enabled':False,
            'review_reasons':list(reasons)+(['SEMANTIC_DECISION_UNRESOLVED'] if status=='UNCERTAIN_MANUAL_REVIEW' else [])}
    if quarantined: return out('UNCERTAIN_MANUAL_REVIEW','R0 unresolved lifecycle/invalid structure')
    if conflicts: return out('UNCERTAIN_MANUAL_REVIEW','R1 unresolved conflicts',conflicts)
    vote=factors.get('votability',{}).get('value','UNCERTAIN')
    if vote=='NOT_VOTABLE': return out('NOT_VOTABLE','R2 no current voting opportunity')
    if vote!='VOTABLE': return out('UNCERTAIN_MANUAL_REVIEW','R3 voting opportunity unresolved')
    if deadline['status']=='PASSED': return out('DEADLINE_PASSED','R4 controlling deadline passed')
    values=[factors.get(k,{}).get('value','NOT_SUPPORTED') for k in RESTRICTIONS]
    if 'YES' in values: return out('VOTABLE_WITH_RESTRICTION','R5 one or more voting restrictions')
    if any(v!='NO' for v in values): return out('UNCERTAIN_MANUAL_REVIEW','R6 restriction facts incomplete')
    if deadline['status']!='OPEN': return out('UNCERTAIN_MANUAL_REVIEW','R7 deadline unresolved')
    return out('VOTABLE','R8 voting opportunity, open deadline, no stated restriction')
