#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
uv sync --frozen
uv run --frozen python scripts/source_public_data.py
uv run --frozen python -m scripts.profile_data
uv run --frozen python -m scripts.import_data data/normalised/public.jsonl
uv run --frozen python scripts/download_model.py
uv run --frozen python -m scripts.run_batch
