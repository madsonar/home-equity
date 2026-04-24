.PHONY: help setup install dev test test-unit test-integration test-endpoints \
        docker-build docker-up docker-down docker-logs docker-clean docker-restart docker-shell \
        monitoring-up monitoring-down monitoring-logs monitoring-status \
        langfuse-up langfuse-down \
        devtools-up devtools-down devtools-logs devtools-status \
        full-up full-down up-all up-all-build down-all start-all stop-all urls \
        web-install web-dev web-build web-clean \
        train-model ingest-kb lint fmt clean

PYTHON   := .venv/bin/python
PIP      := .venv/bin/pip
UVICORN  := .venv/bin/uvicorn
PYTEST   := .venv/bin/pytest

# ──────────────────────────────────────────────
#  help
# ──────────────────────────────────────────────
help:
	@printf "\nCashMe Credit Intelligence Agent v2 (Clean Architecture)\n\n"
	@printf "  \033[1;36m⚡ ATALHO\033[0m\n"
	@printf "    make up-all             Sobe TUDO (usa cache de imagens, NÃO faz rebuild)\n"
	@printf "    make up-all-build       Sobe TUDO forçando rebuild da imagem da API\n"
	@printf "    make start-all          Liga containers já criados (segundos, sem build)\n"
	@printf "    make stop-all           Desliga sem remover containers (retoma com start-all)\n"
	@printf "    make down-all           Derruba tudo (remove containers)\n"
	@printf "    make urls               Imprime lista de endereços de acesso\n\n"
	@printf "  SETUP\n"
	@printf "    make setup              Cria venv + instala dependencias\n"
	@printf "    make install            Atualiza dependencias no venv existente\n\n"
	@printf "  DEV (local, sem Docker)\n"
	@printf "    make dev                Sobe a API localmente (porta 8000, reload)\n"
	@printf "    make train-model        Treina/retreina o modelo de credit scoring\n"
	@printf "    make ingest-kb          Indexa data/knowledge_base no ChromaDB + FAISS\n\n"
	@printf "  TESTES\n"
	@printf "    make test               Roda todos os testes (unit + integration)\n"
	@printf "    make test-unit          Apenas testes unitarios\n"
	@printf "    make test-integration   Apenas testes de integracao\n"
	@printf "    make test-endpoints     Testa endpoints REST (requer servidor em :8000)\n\n"
	@printf "  DOCKER\n"
	@printf "    make docker-build       Build da imagem Docker\n"
	@printf "    make docker-up          Sobe app + chromadb + redis\n"
	@printf "    make docker-down        Para todos os servicos\n"
	@printf "    make docker-logs        Exibe logs em tempo real\n"
	@printf "    make docker-restart     Reinicia apenas o container app\n"
	@printf "    make docker-shell       Abre shell no container app\n"
	@printf "    make docker-clean       Remove containers, volumes e imagens locais\n\n"
	@printf "  OBSERVABILIDADE\n"
	@printf "    make monitoring-up      Sobe Prometheus+Grafana+Tempo+Loki+OTel Collector\n"
	@printf "    make monitoring-down    Para a stack de monitoring\n"
	@printf "    make monitoring-logs    Logs da stack de monitoring\n"
	@printf "    make monitoring-status  Status dos containers de monitoring\n"
	@printf "    make langfuse-up        Sobe Langfuse (LLM tracing)\n"
	@printf "    make langfuse-down      Para o Langfuse\n"
	@printf "    make full-up            Sobe tudo (app + monitoring + langfuse)\n"
	@printf "    make full-down          Para tudo\n\n"
	@printf "  DEV TOOLS (inspecao de dados)\n"
	@printf "    make devtools-up        RedisInsight+ChromaAdmin+Phoenix+MLflow+Jupyter\n"
	@printf "    make devtools-down      Para devtools\n"
	@printf "    make devtools-logs      Logs devtools\n"
	@printf "    make devtools-status    Status devtools\n\n"
	@printf "  FRONTEND (React SPA)\n"
	@printf "    make web-install        Instala dependencias npm em app/presentation/web\n"
	@printf "    make web-dev            Vite dev server (http://localhost:5173)\n"
	@printf "    make web-build          Build de producao (gera dist/ servido em /ui)\n"
	@printf "    make web-clean          Remove node_modules e dist\n\n"
	@printf "  QUALIDADE\n"
	@printf "    make lint               Verifica codigo com ruff\n"
	@printf "    make fmt                Formata codigo com ruff\n"
	@printf "    make clean              Remove cache Python\n\n"

# ──────────────────────────────────────────────
#  setup / install
# ──────────────────────────────────────────────
setup:
	python3 -m venv .venv
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt
	@printf "\n✓ Ambiente pronto. Configure o .env:\n  cp .env.example .env\n"

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# ──────────────────────────────────────────────
#  dev (local)
# ──────────────────────────────────────────────
.env:
	@printf "ERRO: .env nao encontrado. Crie com: cp .env.example .env\n"
	@exit 1

dev: .env
	PYTHONPATH=. $(UVICORN) app.main:app --host 0.0.0.0 --port 8000 --reload

train-model: .env
	PYTHONPATH=. $(PYTHON) scripts/train_model.py

ingest-kb: .env
	PYTHONPATH=. $(PYTHON) scripts/ingest_kb.py

# ──────────────────────────────────────────────
#  testes
# ──────────────────────────────────────────────
test:
	PYTHONPATH=. $(PYTEST) tests/ -v --tb=short

test-unit:
	PYTHONPATH=. $(PYTEST) tests/unit/ -v --tb=short

test-integration:
	PYTHONPATH=. $(PYTEST) tests/integration/ -v --tb=short

test-endpoints:
	@bash scripts/test_endpoints.sh http://127.0.0.1:8000/api/v1

# ──────────────────────────────────────────────
#  docker
# ──────────────────────────────────────────────
docker-build:
	docker compose build

docker-up: .env
	docker compose up -d --no-build --pull missing
	@printf "\nServicos subindo (sem rebuild; use 'make docker-build' para recompilar)...\n"
	@printf "  API:      http://localhost:8000\n"
	@printf "  Docs:     http://localhost:8000/docs\n"
	@printf "  ChromaDB: http://localhost:8001\n"
	@printf "\nAguarde ~30s para o primeiro start.\n"

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f app

docker-restart:
	docker compose restart app

docker-shell:
	docker compose exec app bash

docker-clean:
	docker compose down -v --rmi local
	@printf "Containers, volumes e imagens locais removidos.\n"

# ──────────────────────────────────────────────
#  observabilidade  (Prometheus/Grafana/Tempo/Loki + Langfuse)
# ──────────────────────────────────────────────
monitoring-up: .env
	docker compose --profile monitoring up -d
	@printf "\nStack de observabilidade subindo...\n"
	@printf "  Grafana:    http://localhost:3001  (login: admin / $${GRAFANA_PASSWORD:-cashme123})\n"
	@printf "  Prometheus: http://localhost:9090\n"
	@printf "  Tempo:      http://localhost:3200  (via Grafana)\n"
	@printf "  Loki:       http://localhost:3100  (via Grafana)\n"
	@printf "  OTel OTLP:  grpc://localhost:4317  http://localhost:4318\n"

monitoring-down:
	docker compose --profile monitoring down

monitoring-logs:
	docker compose --profile monitoring logs -f --tail=100 otel-collector prometheus grafana tempo loki promtail

monitoring-status:
	docker compose --profile monitoring ps

langfuse-up: .env
	docker compose --profile langfuse up -d
	@printf "\nLangfuse subindo em http://localhost:3000\n"
	@printf "  1. Crie usuario e projeto pela UI\n"
	@printf "  2. Copie public/secret keys para LANGFUSE_PUBLIC_KEY / LANGFUSE_SECRET_KEY no .env\n"
	@printf "  3. Rode: make docker-restart\n"

langfuse-down:
	docker compose --profile langfuse down

full-up: .env
	docker compose --profile monitoring --profile langfuse up -d
	@printf "\nStack completa subindo...\n"
	@printf "  API:        http://localhost:8000/docs\n"
	@printf "  Grafana:    http://localhost:3001\n"
	@printf "  Prometheus: http://localhost:9090\n"
	@printf "  Langfuse:   http://localhost:3000\n"

full-down:
	docker compose --profile monitoring --profile langfuse down

# ──────────────────────────────────────────────
#  devtools  (inspecao de dados + ML observability)
# ──────────────────────────────────────────────
devtools-up: .env
	docker compose --profile devtools up -d
	@printf "\nDev tools subindo...\n"
	@printf "  RedisInsight:   http://localhost:5540  (Redis: cashme-redis ja pre-configurado)\n"
	@printf "  Chroma Admin:   http://localhost:3500  (aponta para http://chromadb:8000)\n"
	@printf "  Phoenix:        http://localhost:6006  (LLM tracing + embeddings viz)\n"
	@printf "  MLflow:         http://localhost:5500  (experiment tracking)\n"
	@printf "  Jupyter Lab:    http://localhost:8888  (token: cashme)\n"

devtools-down:
	docker compose --profile devtools down

devtools-logs:
	docker compose --profile devtools logs -f --tail=100 redisinsight chroma-admin phoenix mlflow jupyter

devtools-status:
	docker compose --profile devtools ps

# ──────────────────────────────────────────────
#  frontend (React SPA)
# ──────────────────────────────────────────────
WEB_DIR := app/presentation/web

web-install:
	cd $(WEB_DIR) && npm install --no-audit --no-fund

web-dev:
	cd $(WEB_DIR) && npm run dev

web-build:
	cd $(WEB_DIR) && npm run build
	@printf "\n✓ SPA construida em $(WEB_DIR)/dist\n"
	@printf "  Sera servida pelo FastAPI em http://localhost:8000/ui apos restart.\n"

web-clean:
	rm -rf $(WEB_DIR)/node_modules $(WEB_DIR)/dist

# ──────────────────────────────────────────────
#  up-all  (sobe a stack completa + imprime URLs)
#  • up-all        : sobe usando imagem existente (não rebuilda a API)
#  • up-all-build  : força rebuild da imagem da API antes de subir
#  • start-all     : apenas liga containers já criados (segundos)
#  • stop-all      : apenas desliga (containers ficam criados)
#  • down-all      : remove containers
# ──────────────────────────────────────────────
up-all: .env
	@printf "\n\033[1;32m▶ Subindo stack COMPLETA (cache de imagens, sem rebuild)...\033[0m\n\n"
	docker compose --profile monitoring --profile langfuse --profile devtools up -d --no-build --pull missing
	@printf "\n\033[1;33m⏳ Aguardando serviços ficarem saudáveis (~15s)...\033[0m\n"
	@sleep 15
	@$(MAKE) --no-print-directory urls

up-all-build: .env
	@printf "\n\033[1;32m▶ REBUILD da imagem da API + subindo stack completa...\033[0m\n\n"
	docker compose --profile monitoring --profile langfuse --profile devtools up -d --build
	@printf "\n\033[1;33m⏳ Aguardando serviços ficarem saudáveis (~15s)...\033[0m\n"
	@sleep 15
	@$(MAKE) --no-print-directory urls

start-all:
	@printf "\n\033[1;32m▶ Ligando containers existentes (sem recriar)...\033[0m\n"
	docker compose --profile monitoring --profile langfuse --profile devtools start
	@$(MAKE) --no-print-directory urls

stop-all:
	@printf "\n\033[1;33m▶ Desligando containers (sem remover)...\033[0m\n"
	docker compose --profile monitoring --profile langfuse --profile devtools stop

down-all:
	docker compose --profile monitoring --profile langfuse --profile devtools down

urls:
	@printf "\n"
	@printf "╔══════════════════════════════════════════════════════════════════════════════╗\n"
	@printf "║  \033[1;36mCashMe Credit Intelligence Agent — endereços de acesso\033[0m                    ║\n"
	@printf "╚══════════════════════════════════════════════════════════════════════════════╝\n\n"
	@printf "  \033[1;32m▸ APLICAÇÃO\033[0m\n"
	@printf "    🌐 SPA (admin + cliente)   http://localhost:8000/ui\n"
	@printf "    📘 Swagger / OpenAPI       http://localhost:8000/docs\n"
	@printf "    📕 ReDoc                   http://localhost:8000/redoc\n"
	@printf "    📊 Metrics (Prometheus)    http://localhost:8000/metrics\n"
	@printf "    ❤️  Healthcheck             http://localhost:8000/api/v1/health\n\n"
	@printf "  \033[1;32m▸ DADOS\033[0m\n"
	@printf "    🧠 ChromaDB (vector DB)    http://localhost:8001\n"
	@printf "    🔴 Redis                   redis://localhost:6379\n\n"
	@printf "  \033[1;32m▸ OBSERVABILIDADE\033[0m\n"
	@printf "    📈 Grafana                 http://localhost:3001           (admin / cashme123)\n"
	@printf "    📉 Prometheus              http://localhost:9090\n"
	@printf "    🔭 Tempo (traces)          http://localhost:3200\n"
	@printf "    📜 Loki (logs)             http://localhost:3100/ready\n"
	@printf "    🤖 Langfuse (LLM traces)   http://localhost:3002           (criar user no 1º acesso)\n"
	@printf "    📡 OTLP gRPC               grpc://localhost:4317\n"
	@printf "    📡 OTLP HTTP               http://localhost:4318\n\n"
	@printf "  \033[1;32m▸ DEV TOOLS\033[0m\n"
	@printf "    🔍 RedisInsight            http://localhost:5540\n"
	@printf "    🗂  Chroma Admin            http://localhost:3500\n"
	@printf "    🎯 Phoenix (Arize)         http://localhost:6006\n"
	@printf "    🧪 MLflow                  http://localhost:5500\n"
	@printf "    📓 Jupyter Lab             http://localhost:8888/?token=cashme\n\n"
	@printf "  \033[1;33m💡 Comandos úteis:\033[0m\n"
	@printf "    make urls           re-imprime esta lista\n"
	@printf "    make docker-logs    logs da app em tempo real\n"
	@printf "    make down-all       derruba tudo\n\n"

# ──────────────────────────────────────────────
#  qualidade
# ──────────────────────────────────────────────
lint:
	$(PYTHON) -m ruff check app/ tests/ || ($(PIP) install ruff -q && $(PYTHON) -m ruff check app/ tests/)

fmt:
	$(PYTHON) -m ruff format app/ tests/ || ($(PIP) install ruff -q && $(PYTHON) -m ruff format app/ tests/)

# ──────────────────────────────────────────────
#  limpeza
# ──────────────────────────────────────────────
clean:
	find . -type d -name "__pycache__" -not -path "./.venv/*" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -not -path "./.venv/*" -delete 2>/dev/null || true
	@printf "Cache Python removido.\n"
