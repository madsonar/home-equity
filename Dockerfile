# ──────────────────────────────────────────────────────────────────────────
# Stage 1 — build do SPA React (Vite) em app/presentation/web
# ──────────────────────────────────────────────────────────────────────────
FROM node:20-alpine AS web-builder
WORKDIR /web
ARG VITE_PANEL_BASE=
ENV VITE_PANEL_BASE=${VITE_PANEL_BASE}
COPY app/presentation/web/package.json app/presentation/web/package-lock.json* ./
RUN npm install --no-audit --no-fund
COPY app/presentation/web/ ./
RUN npm run build

# ──────────────────────────────────────────────────────────────────────────
# Stage 2 — runtime Python
# ──────────────────────────────────────────────────────────────────────────
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# --- dependências do sistema ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# --- dependências Python (com cache mount: próximos rebuilds reutilizam wheels) ---
# Usa o índice de wheels CPU-only do PyTorch para não baixar CUDA (~2 GB).
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install --extra-index-url https://download.pytorch.org/whl/cpu \
                -r requirements.txt

# Playwright para Crawl4AI (scraping com JS)
RUN crawl4ai-setup || true

# --- código da aplicação ---
COPY . .

# --- SPA buildada do stage 1 ---
COPY --from=web-builder /web/dist ./app/presentation/web/dist

# --- diretórios de dados ---
RUN mkdir -p data/knowledge_base data/chroma_db data/faiss_index data/sample_docs

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
