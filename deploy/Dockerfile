FROM python:3.12-slim-bookworm@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258 AS prowide
RUN apt-get update && apt-get install -y --no-install-recommends default-jdk-headless maven && rm -rf /var/lib/apt/lists/*
WORKDIR /build
COPY tools/prowide/pom.xml ./pom.xml
COPY tools/prowide/src ./src
RUN mvn -B -q package

FROM python:3.12-slim-bookworm@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258
ARG SOURCE_REVISION=UNSPECIFIED
LABEL org.opencontainers.image.title="Voting Intelligence Framework" org.opencontainers.image.revision=$SOURCE_REVISION org.opencontainers.image.licenses="PolyForm-Noncommercial-1.0.0"
RUN apt-get update && apt-get install -y --no-install-recommends default-jre-headless git libgomp1 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir uv==0.9.4
WORKDIR /app
COPY deploy/requirements.lock /tmp/requirements.lock
RUN uv venv /opt/venv && uv pip sync --python /opt/venv/bin/python /tmp/requirements.lock && rm -rf /root/.cache
COPY deploy/torch-cpu.lock /tmp/torch-cpu.lock
RUN uv pip install --python /opt/venv/bin/python --no-deps --force-reinstall -r /tmp/torch-cpu.lock && /opt/venv/bin/python -c "import torch; assert torch.version.cuda is None; print(torch.__version__)" && rm -rf /root/.cache
COPY . /app
COPY --from=prowide /build/target/prowide-helper-1.0.0.jar /app/tools/prowide/target/prowide-helper-1.0.0.jar
# Jobs record the actual installed source tree's commit. The upstream revision
# is also retained separately; this is not a fabricated upstream commit.
RUN git init -q && git -c user.name='Installed source snapshot' -c user.email='build@localhost' add . && git -c user.name='Installed source snapshot' -c user.email='build@localhost' commit -qm "Installed source snapshot" && printf '%s\n' "$SOURCE_REVISION" > UPSTREAM_REVISION
RUN groupadd -g 10001 voting && useradd -u 10001 -g voting -M -s /usr/sbin/nologin voting && mkdir -p /srv/voting/state/workspace /srv/voting/logs /srv/voting/models && rm -rf /app/artifacts && ln -s /srv/voting/logs /app/artifacts && chown -R voting:voting /srv/voting && git config --system --add safe.directory /app
ENV PATH=/opt/venv/bin:$PATH PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1 USE_TF=0 HF_HOME=/tmp/huggingface XDG_CACHE_HOME=/tmp/cache TOKENIZERS_PARALLELISM=false VOTING_DB=/srv/voting/state/voting.sqlite VOTING_TRAINING_WORKSPACE=/srv/voting/state/workspace VOTING_MODELS_ROOT=/srv/voting/models AUTOMATION_ENABLED=false TRAINING_EXECUTION_ENABLED=false LAYA_DEVICE=cpu
ENV VOTING_REQUIRE_WORKER=true
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health/live', timeout=3)"
ENTRYPOINT ["/bin/sh", "/app/deploy/entrypoint.sh"]
CMD ["python", "-m", "uvicorn", "apps.api.production:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--no-proxy-headers", "--no-access-log", "--limit-concurrency", "32", "--timeout-keep-alive", "5"]
