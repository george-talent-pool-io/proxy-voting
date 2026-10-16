"""Same checkpoint weights; configurable evidence reduction and a declared composite specialist."""
import copy,time
from dataclasses import asdict
from semantic_pipeline.models import NarrowAdapter,WholeLaya
from semantic_pipeline.fallback import digest
from semantic_pipeline.schema import RESTRICTIONS
from cascade.aggregation import aggregate,AggregationConfig,VERSION

class EvidenceNarrow:
    def __init__(self,config=None,model=None):
        self.config=config or AggregationConfig();self.base=model or NarrowAdapter()
    @staticmethod
    def project(text,result,config):
        result=copy.deepcopy(result);native=result['raw']['passage_predictions']
        for key in RESTRICTIONS:
            result['predicates'][key]={**aggregate(text,key,native[key],config),'source':'LAYA_EVIDENCE_AGGREGATION'}
        result['legacy_predicates']=result['raw']['predicates']
        result['configuration_version']=digest({'native_configuration':result['configuration_version'],'aggregation':asdict(config),'version':VERSION})
        result['aggregation_version']=VERSION
        return result
    def analyse(self,text):
        start=time.perf_counter();result=self.project(text,self.base.analyse(text),self.config)
        result['latency_ms']=(time.perf_counter()-start)*1000;return result

class CapableSpecialist:
    """Whole-notice FT votability + evidence-aggregated narrow restrictions.
    Expanded questions remain transfer-only; additional inference is NOT training.
    Both native checkpoints/views are preserved, never presented as one new trained model.
    """
    def __init__(self,config=None,whole=None,narrow=None):
        self.whole=whole or WholeLaya(fine=True);self.narrow=narrow or EvidenceNarrow(config)
    @staticmethod
    def combine(whole,narrow):
        result=copy.deepcopy(narrow);result['predicates']['votability']=copy.deepcopy(whole['predicates']['votability'])
        vote=result['predicates']['votability'];support=narrow['predicates']['votability']
        if support['value']==vote['value']:
            vote['evidence']=copy.deepcopy(support.get('evidence',[]))
            vote['supporting_passage_count']=len(vote['evidence'])
            vote['contradicting_passage_count']=int(bool(support.get('conflict')))
            vote['evidence_source']='Independent narrow passage support agrees with whole-notice label; candidate evidence, not expert explanation'
        result['whole_notice_view']=whole;result['checkpoint']={'whole':whole['checkpoint'],'narrow':narrow['checkpoint']}
        result['model_version']=digest({'whole':whole['model_version'],'narrow':narrow['model_version']})
        result['configuration_version']=digest({'whole':whole['configuration_version'],'narrow':narrow['configuration_version'],'composition':'whole-votability-narrow-restrictions-v1'})
        result['latency_ms']=whole['latency_ms']+narrow['latency_ms'];result['truncated']=whole['truncated'] or narrow['truncated']
        result['composition']='Whole FT votability + narrow FT/transfer restrictions; no retraining'
        return result
    def analyse(self,text):
        start=time.perf_counter();result=self.combine(self.whole.analyse(text),self.narrow.analyse(text));result['latency_ms']=(time.perf_counter()-start)*1000
        return result
