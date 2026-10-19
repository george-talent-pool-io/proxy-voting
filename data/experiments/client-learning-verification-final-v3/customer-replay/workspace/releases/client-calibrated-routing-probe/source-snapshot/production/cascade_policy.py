"""Calibrated specialist routing is separate from final-output calibration."""
import json
from pathlib import Path
from production.storage import digest
from production import confidence
from training.framework.bundle import sha


def stage_identity(manifest):
    if 'laya' not in manifest['models']: raise ValueError('Laya stage required')
    return digest({'version':'laya-stage-confidence-v1','model':manifest['models']['laya'],
                   'aggregation':manifest['spec']['aggregation'],
                   'inference':manifest['spec'].get('laya_inference','PASSAGES'),
                   'sources':manifest['sources'],'schema':manifest['schema_sha256']})


def load(calibrator_path, point_path, manifest):
    identity=stage_identity(manifest)
    cal=confidence.load(calibrator_path,identity)
    if (cal.get('context') or {}).get('calibration_partition')!='LAYA_STAGE':
        raise ValueError('Cascade routing requires specialist-only partitioned calibration')
    point=json.loads(Path(point_path).read_text())
    if point.get('identity')!=identity or point.get('calibrator_sha256')!=cal['sha256'] or point.get('sha256')!=digest({k:v for k,v in point.items() if k!='sha256'}):
        raise ValueError('Stage routing policy identity mismatch')
    return cal,point


def assess(text,result,cal,point,*,language,input_type,population):
    """All fields + final trust must pass before avoiding the generative model."""
    from production.qualification import assess as assess_output
    if point['selection'] is None:
        return {'accept':False,'reasons':['NO_SUPPORTED_STAGE_OPERATING_POINT'],'confidence':None}
    outcome=assess_output(text,result,{'language':language,'input_type':input_type,'population':population},cal,
                          point['identity'],point['selection']['threshold'])
    return {'accept':outcome['eligible'],'reasons':outcome['review_reasons'],
            'confidence':outcome['final_decision_confidence'],'assessment':outcome,
            'policy_sha256':point['sha256'],'scope':population}
