"""Explicit, resumable download of the pinned trainable Qwen MLX artifact.

Downloads public weights only. Never invoked by inference or application startup.
"""
import argparse
import json
from pathlib import Path

REPOSITORY = 'mlx-community/Qwen3.8-27B-4bit'
REVISION = '10c35caafbb80f7dc6a7a432cdd11af10a6d4818'


def setup(output):
    from huggingface_hub import HfApi, snapshot_download
    info = HfApi().model_info(REPOSITORY, revision=REVISION)
    card = info.card_data.to_dict()
    if card.get('base_model') != 'Qwen/Qwen3.8-27B' or card.get('license') != 'apache-2.0':
        raise ValueError('Published base-model lineage/licence differs from the qualified artifact')
    path = snapshot_download(REPOSITORY, revision=REVISION, local_dir=output,
        allow_patterns=['*.json','*.safetensors','*.jinja','*.txt','*.model','README.md','LICENSE*'], max_workers=3)
    return {'repository': REPOSITORY, 'revision': REVISION, 'path': str(path),
            'published_base_model': card['base_model'], 'licence': card['license'],
            'base_conversion_commit': 'Not pinned by conversion card; not independently established',
            'network_inference': False}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--output', default='data/models/trainable-qwen38-mlx4')
    print(json.dumps(setup(p.parse_args().output), indent=2))
