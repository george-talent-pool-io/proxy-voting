from typing import Protocol
class SemanticFallback(Protocol):
    def analyse(self,narrative,structured_context,requested_predicates)->dict: ...
class DisabledFallback:
    enabled=False
    def analyse(self,narrative,structured_context,requested_predicates):
        return {'enabled':False,'external_calls':0,'predicates':{p:{'value':'UNKNOWN','scores':{},'confidence':None,'evidence':None} for p in requested_predicates},'reason':'LLM fallback disabled; no local LLM configured'}
