FROM python:3.12-slim
RUN pip install --no-cache-dir uv==0.9.4
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .
ENV HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1 USE_TF=0 LAYA_DEVICE=cpu
EXPOSE 8000
CMD ["uv", "run", "--frozen", "--no-dev", "python", "-m", "uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
