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


def training_base_admission(spec, models):
    """Foundations stay in the model volume; continuation uses verified jobs.

    An arbitrary workspace path or a self-declared derivative is insufficient.
    The frozen seed must bind a completed registered job's exact lineage/bytes.
    """
    from training.framework import jobs, seeds
    from training.framework.bundle import sha
    from training.framework.runtime import verify_checkpoint
    path=Path(spec.model_path).resolve();models=Path(models).resolve()
    if models in path.parents:
        return {'source':'MANAGED_MODEL_VOLUME'}
    if spec.parent_seed_path:
        seed_root=Path(spec.parent_seed_path).resolve()
        if seed_root.parent==(jobs.WORKSPACE/'seeds').resolve():
            seed=seeds.verify(seed_root)
            job=path.parent
            if (path.name=='checkpoint' and job.parent==(jobs.WORKSPACE/'jobs').resolve() and
                seed['origin'] in ('AI_TEST_DERIVATIVE','CUSTOMER_DERIVATIVE') and
                path==Path(seed['model_location']).resolve()):
                registered,plan,manifest=verify_checkpoint(jobs.member('jobs',job.name))
                lineage=seed.get('lineage') or {}
                if (lineage.get('job_manifest_sha256')==sha(registered/'model-manifest.json') and
                    lineage.get('training_bundle_sha256')==plan['bundle_manifest_sha256']):
                    return {'source':'REGISTERED_FROZEN_DERIVATIVE','origin':seed['origin'],
                            'parent_identity':seed['identity'],'job':job.name}
    raise ValueError('Training base must be inside the managed model volume or a verified frozen registered derivative')


def inference_admission(release):
    import json
    import torch
    from training.framework import jobs
    manifest=json.loads((Path(release)/'release.json').read_text())
    required=2*1024**3
    for model in manifest['models'].values():
        if model.get('seed_id'):
            from training.framework.seeds import verify
            seed=verify(jobs.member('seeds',model['seed_id']));spec=seed['spec']
            checkpoint=Path(seed['model_location'])
        else:
            job=jobs.member('jobs',model['job_id']);spec=json.loads((job/'plan.json').read_text())['spec']
            checkpoint=job/'checkpoint'
        if spec['backend']=='MLX_QLORA':raise ValueError('MLX checkpoint is not a Linux serving artifact; qualify a local Transformers checkpoint')
        if spec['device']=='cuda' and not torch.cuda.is_available():raise ValueError('Serving checkpoint requires an unavailable CUDA runtime')
        size=sum(p.stat().st_size for p in checkpoint.rglob('*.safetensors'))
        if spec['backend']!='LAYA_SDK' and not model.get('seed_id'):size+=sum(p.stat().st_size for p in Path(spec['model_path']).rglob('*.safetensors'))
        required+=max(6*1024**3,2*size)
    if memory_limit()<required:raise ValueError(f'Model-serving memory admission failed; minimum floor={required}; qualify the checkpoint on a larger container')
    return {'minimum_bytes':required,'scope':'Conservative admission, not measured peak memory or throughput'}
