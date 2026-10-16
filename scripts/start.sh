#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
command -v uv >/dev/null || { echo 'Install uv first: https://docs.astral.sh/uv/'; exit 1; }
uv sync --frozen
exec uv run --frozen python -m uvicorn apps.api.main:app --host 127.0.0.1 --port "${PORT:-8000}"
