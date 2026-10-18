"""Conservative admission checks, not a substitute for a measured load test."""
from pathlib import Path


def memory_limit():
    import psutil
    total=psutil.virtual_memory().total
    path=Path('/sys/fs/cgroup/memory.max')
    if path.exists():
        value=path.read_text().strip()
        if value.isdecimal():total=min(total,int(value))
    return total


def training_admission(spec):
    if spec.device == 'mps':raise ValueError('MPS/MLX is not a Linux training device')
    import torch
    if spec.device == 'cuda' and not torch.cuda.is_available():raise ValueError('Selected image/device has no qualified CUDA runtime')
    # This is an explicit service floor. Longer contexts/batches may need much
    # more, and must pass the installation's actual checkpoint smoke/load test.
    floor=8*1024**3 if spec.max_length<=512 else 16*1024**3
    weights=sum(p.stat().st_size for p in Path(spec.model_path).glob('*.safetensors'))
    floor=max(floor,weights*2+4*1024**3)
    limit=memory_limit()
    if limit<floor:raise ValueError(f'Training memory admission failed: limit={limit}, conservative minimum={floor}; qualify a larger host/container')
    return {'memory_limit_bytes':limit,'minimum_bytes':floor,'scope':'Admission floor, not measured peak-memory guarantee'}


def inference_admission(release):
    import json
    import torch
    from training.framework import jobs
    manifest=json.loads((Path(release)/'release.json').read_text())
    required=2*1024**3
    for model in manifest['models'].values():
        job=jobs.member('jobs',model['job_id']);spec=json.loads((job/'plan.json').read_text())['spec']
        if spec['backend']=='MLX_QLORA':raise ValueError('MLX checkpoint is not a Linux serving artifact; qualify a local Transformers checkpoint')
        if spec['device']=='cuda' and not torch.cuda.is_available():raise ValueError('Serving checkpoint requires an unavailable CUDA runtime')
        size=sum(p.stat().st_size for p in (job/'checkpoint').rglob('*.safetensors'))
        if spec['backend']!='LAYA_SDK':size+=sum(p.stat().st_size for p in Path(spec['model_path']).rglob('*.safetensors'))
        required+=max(6*1024**3,2*size)
    if memory_limit()<required:raise ValueError(f'Model-serving memory admission failed; minimum floor={required}; qualify the checkpoint on a larger container')
    return {'minimum_bytes':required,'scope':'Conservative admission, not measured peak memory or throughput'}
