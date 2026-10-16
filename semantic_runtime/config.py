import os
ARCHITECTURES={'LEGACY_LAYA':'A','FT_LAYA':'B','LAYA_LLM':'C','LLM_ONLY':'D','FULL_HYBRID':'E'}
def configured_architecture():
    name=os.environ.get('CLASSIFICATION_ARCHITECTURE','LEGACY_LAYA')
    if name not in ARCHITECTURES:raise ValueError('Unknown CLASSIFICATION_ARCHITECTURE')
    return name,ARCHITECTURES[name]
