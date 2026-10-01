# syntax=docker/dockerfile:1.7
# Build context: repository root. Long-running worker: never deploy as a short-lived serverless function.
FROM python:3.12-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 UV_LINK_MODE=copy
# Node is needed only by the Phosphor metadata adapter during catalog imports.
RUN apt-get update && apt-get install -y --no-install-recommends nodejs ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:0.12 /uv /usr/local/bin/uv
WORKDIR /repo
COPY pyproject.toml uv.lock ./
COPY tools/font-builder tools/font-builder
COPY tools/importers tools/importers
COPY apps/worker apps/worker
RUN uv sync --frozen --all-packages --no-dev
COPY assets assets
COPY tools/core-authoring tools/core-authoring
RUN useradd --system --uid 1001 worker && mkdir -p .cache build dist .data && chown -R worker /repo
USER worker
ENV PATH="/repo/.venv/bin:$PATH" TYPEICON_ROOT=/repo
COPY --chmod=755 <<'SH' /usr/local/bin/catalog-init
#!/bin/sh
# Build the catalog from pinned sources, compile + validate the release, load DB and storage.
set -e
typeicon-import build
typeicon-import release --version "${RELEASE_VERSION:-0.1.0}" --date "${RELEASE_DATE:-2026-09-30}"
typeicon-import db-load --release "${RELEASE_VERSION:-0.1.0}"
typeicon-import audit --raster
SH
ENTRYPOINT []
CMD ["typeicon-worker"]
