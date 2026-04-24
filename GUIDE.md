# 🚀 Guia de Uso — CashMe Credit Intelligence Agent

Passo-a-passo para subir **toda** a stack (API + SPA + observabilidade + dev tools)
e testar cada ferramenta isoladamente. Complementa o [README.md](./README.md).

> **TL;DR** — `cp .env.example .env` → preencha `GOOGLE_API_KEY` → `make up-all` →
> abra <http://localhost:8000/ui>. Pronto.

---

## 📑 Índice

1. [Pré-requisitos](#1-pré-requisitos)
2. [Configuração inicial (.env)](#2-configuração-inicial-env)
3. [Subindo a stack completa](#3-subindo-a-stack-completa)
4. [Testando a API (curl + Swagger)](#4-testando-a-api-curl--swagger)
5. [Testando a SPA React](#5-testando-a-spa-react-admin--cliente)
6. [Observabilidade](#6-observabilidade)
   - [Grafana](#61-grafana) · [Prometheus](#62-prometheus) ·
     [Tempo (traces)](#63-tempo-traces) · [Loki (logs)](#64-loki-logs) ·
     [Langfuse (LLM)](#65-langfuse-llm-traces) · [Phoenix](#66-phoenix-arize)
7. [Dev Tools](#7-dev-tools)
   - [RedisInsight](#71-redisinsight) · [Chroma Admin](#72-chroma-admin) ·
     [MLflow](#73-mlflow) · [Jupyter Lab](#74-jupyter-lab)
8. [WhatsApp (Twilio sandbox)](#8-whatsapp-via-twilio-sandbox)
9. [Trocar de provider / vector store (zero código)](#9-trocar-de-provider--vector-store-zero-código)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Pré-requisitos

| Ferramenta          | Versão mínima | Observação                               |
|---------------------|---------------|------------------------------------------|
| Docker + Compose v2 | 24 / 2.20     | Engine ou Desktop                        |
| Python              | 3.11+         | Apenas para rodar scripts locais         |
| Node.js             | 20+           | Apenas para desenvolver a SPA            |
| Make                | 4+            | Usado para atalhos                       |
| 8 GB RAM livres     | —             | stack completa chega a ~6 GB             |

Portas usadas: **8000** (API), **8001** (Chroma), **6379** (Redis), **3001**
(Grafana), **3002** (Langfuse), **9090** (Prometheus), **3200** (Tempo), **3100**
(Loki), **4317/4318** (OTel), **5540** (RedisInsight), **3500** (Chroma Admin),
**6006** (Phoenix), **5500** (MLflow), **8888** (Jupyter).

---

## 2. Configuração inicial (`.env`)

```bash
cp .env.example .env
```

Edite e preencha **pelo menos** a chave do provider ativo
(`DEFAULT_LLM_PROVIDER`). Com as variáveis padrão basta:

```dotenv
GOOGLE_API_KEY=AIza...seu-token-aqui
DEFAULT_LLM_PROVIDER=google
DEFAULT_LLM_MODEL=gemini-2.5-pro
EMBEDDING_PROVIDER=google
EMBEDDING_MODEL=models/text-embedding-004
```

> ✅ **Zero hardcode.** Todos os providers, modelos, embeddings, vector store,
> prefixos de memória, path do modelo ML e janelas de contexto são lidos de
> `.env` via [app/config.py](app/config.py) e resolvidos pela factory
> [app/infrastructure/llm/providers.py](app/infrastructure/llm/providers.py).

---

## 3. Subindo a stack completa

```bash
make up-all          # app + monitoring + langfuse + devtools
make urls            # imprime todas as URLs
```

> ⚡ **Build acontece só na 1ª vez.** `make up-all` usa `--no-build` — se a
> imagem `cashme-agent:local` já existe, sobe em segundos. Para forçar rebuild
> (após alterar `requirements.txt` / `Dockerfile`): `make up-all-build`.
>
> Depois que os containers já foram criados, prefira:
> ```bash
> make stop-all       # desliga (mantém containers)
> make start-all      # religa em segundos
> ```
> Só use `make down-all` se quiser remover containers de verdade.

Alternativas granulares:

```bash
make docker-up          # só API + Chroma + Redis
make monitoring-up      # adiciona Prometheus / Grafana / Tempo / Loki
make langfuse-up        # adiciona Langfuse + Postgres
make devtools-up        # adiciona RedisInsight / Chroma Admin / Phoenix / MLflow / Jupyter
```

Derrubar tudo:

```bash
make stop-all     # ⏸️  desliga sem remover (retome com start-all)
make down-all     # 🗑️  remove containers (rede/volumes mantidos)
```

Logs:

```bash
make docker-logs           # API
make monitoring-logs       # stack de observabilidade
make devtools-logs         # ferramentas de dev
```

---

## 4. Testando a API (curl + Swagger)

📘 **Swagger interativo:** <http://localhost:8000/docs>

### 4.1. Health

```bash
curl http://localhost:8000/api/v1/health
```

### 4.2. Score de crédito

```bash
curl -X POST http://localhost:8000/api/v1/score \
  -H 'Content-Type: application/json' \
  -d '{
    "client_id": "cli-001",
    "features": {
      "monthly_income": 12000,
      "property_value": 800000,
      "loan_amount": 300000,
      "age": 38,
      "has_restrictions": false
    }
  }' | jq
```

### 4.3. Chat (agente com RAG + tools)

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "session_id": "demo-1",
    "message": "Quanto consigo de crédito com imóvel de 800 mil?"
  }' | jq
```

### 4.4. Ingestão de URL

```bash
curl -X POST http://localhost:8000/api/v1/ingest/url \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://www.cashme.com.br/blog/home-equity"}'
```

### 4.5. Ingestão de documento local

```bash
curl -X POST http://localhost:8000/api/v1/ingest/doc \
  -F "file=@data/sample_docs/exemplo_simulacao.txt"
```

### 4.6. Busca semântica

```bash
curl "http://localhost:8000/api/v1/search?q=home%20equity&k=4" | jq
```

### 4.7. Script agregador

```bash
bash scripts/test_endpoints.sh
```

---

## 5. Testando a SPA React (admin + cliente)

URL: <http://localhost:8000/ui>

| Página                     | URL                                   | O que testar                                        |
|----------------------------|---------------------------------------|-----------------------------------------------------|
| **Home**                   | `/ui`                                 | Seleção de perfil (admin / cliente)                 |
| **Simulador do cliente**   | `/ui/cliente/simulador`               | Preencher renda / imóvel → chama `/api/v1/score`    |
| **Chat do cliente**        | `/ui/cliente/chat`                    | Conversa livre → `/api/v1/chat`                     |
| **Admin · KPIs**           | `/ui/admin/kpis`                      | Gráficos a partir de `/metrics`                     |
| **Admin · Ingestão**       | `/ui/admin/ingestao`                  | Upload de URL + PDF                                 |
| **Admin · Base**           | `/ui/admin/base`                      | Busca vetorial (`/api/v1/search`)                   |
| **Admin · Modelos**        | `/ui/admin/modelos`                   | Stats do scorer + retreino                          |

Dev com hot-reload da SPA (opcional):

```bash
make web-install
make web-dev     # http://localhost:5173 (proxy para API em :8000)
```

---

## 6. Observabilidade

### 6.1. Grafana
🔗 <http://localhost:3001> — `admin` / `cashme123`

1. Menu **Dashboards** → **CashMe · Overview**.
2. Painéis: latência p95/p99, taxa de score, uso de tokens LLM, erros.
3. **Explore** → data source **Tempo** para traces, **Loki** para logs.

### 6.2. Prometheus
🔗 <http://localhost:9090>

Queries úteis:

```promql
sum(rate(cashme_credit_score_total[5m])) by (decision)
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
sum(rate(cashme_llm_tokens_total[5m])) by (provider, model)
```

### 6.3. Tempo (traces)
Via Grafana → **Explore** → datasource **Tempo** → filtre por `service.name = cashme-api`.
Cada request tem spans de: `FastAPI → UseCase → Agent → LLM → VectorStore`.

### 6.4. Loki (logs)
Via Grafana → **Explore** → datasource **Loki**:

```logql
{container="cashme-api"} |= "ERROR"
{container=~"cashme-.*"} | json | trace_id != ""
```

### 6.5. Langfuse (LLM traces)
🔗 <http://localhost:3002>

1. Crie usuário no 1º acesso.
2. Crie um projeto → copie `Public Key` e `Secret Key`.
3. Cole em `.env`:
   ```dotenv
   LANGFUSE_PUBLIC_KEY=pk-lf-...
   LANGFUSE_SECRET_KEY=sk-lf-...
   LANGFUSE_HOST=http://langfuse-web:3000
   ```
4. `make docker-restart` → cada chamada LLM aparece com prompt/completion/tokens/custo.

### 6.6. Phoenix (Arize)
🔗 <http://localhost:6006>

Traces de agente + visualização de embeddings. Recebe OTLP do OTel Collector.
Abra a aba **Traces** para ver cadeias LangChain/Agno.

---

## 7. Dev Tools

### 7.1. RedisInsight
🔗 <http://localhost:5540> — conexão `cashme-redis` já pré-configurada.

Inspeciona: memória curta (`memory_<session_id>`), cache de sessão, rate-limit.

### 7.2. Chroma Admin
🔗 <http://localhost:3500> (backend: `http://chromadb:8000`)

Liste coleções (`credit_knowledge_base`, `memory_*`), documentos e embeddings.

### 7.3. MLflow
🔗 <http://localhost:5500>

Retreinar o modelo e ver runs:

```bash
make train-model    # dispara scripts/train_model.py com logging MLflow
```

### 7.4. Jupyter Lab
🔗 <http://localhost:8888> — **token:** `cashme`

Volume `./notebooks` montado. Útil para explorar embeddings e testar providers.

---

## 8. WhatsApp (via Twilio Sandbox)

1. Crie conta em <https://www.twilio.com/try-twilio> e ative o **WhatsApp Sandbox**.
2. Preencha no `.env`:
   ```dotenv
   TWILIO_ACCOUNT_SID=AC...
   TWILIO_AUTH_TOKEN=...
   TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
   ```
3. Exponha a API com ngrok: `ngrok http 8000`.
4. No console Twilio, em *Sandbox settings*, configure:
   `WHEN A MESSAGE COMES IN` → `https://<ngrok>.ngrok.io/webhooks/whatsapp`.
5. Envie **"join <palavra-chave>"** do seu WhatsApp → depois qualquer mensagem.
   Verá o agente respondendo.

---

## 9. Trocar de provider / vector store (zero código)

**Trocar LLM (chat + score):** edite `.env`:

```dotenv
DEFAULT_LLM_PROVIDER=openai        # google | openai | deepseek | cohere
DEFAULT_LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-...
```

**Trocar embeddings:**

```dotenv
EMBEDDING_PROVIDER=local           # google | openai | cohere | local
LOCAL_EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

**Trocar agente default do `/chat`:**

```dotenv
DEFAULT_AGENT=agno                 # langchain | agno
```

**Trocar vector store:**

```dotenv
VECTOR_STORE_BACKEND=faiss         # chroma | faiss
```

Sempre `make docker-restart` depois. Tudo é resolvido pela factory em
[providers.py](app/infrastructure/llm/providers.py) — **nenhum código é
alterado**.

---

## 10. Troubleshooting

| Sintoma                                                | Causa / Solução                                                                 |
|--------------------------------------------------------|---------------------------------------------------------------------------------|
| `cashme-api` reinicia em loop                          | Falta `GOOGLE_API_KEY` (ou chave do provider ativo) → revisar `.env`            |
| `/api/v1/chat` retorna 500 com "embedding dim"         | Trocou de provider de embedding sem limpar Chroma → `rm -rf data/chroma_db`     |
| SPA 404 em `/ui`                                       | Rode `make web-build` e depois `make docker-restart`                            |
| Grafana sem dados                                      | Stack de monitoring não subiu → `make monitoring-up` + aguardar 30 s            |
| Langfuse sem traces                                    | Keys não preenchidas no `.env` → ver passo 6.5                                  |
| Playwright (Crawl4AI) falha no ingest URL              | Falta browser no container → `docker exec cashme-api playwright install chromium` |
| Porta 8000 ocupada                                     | `lsof -i:8000` → matar processo ou mudar porta no `docker-compose.yml`          |
| `make up-all` lento na 1ª vez                          | Pull de ~10 imagens Docker (~5 GB). Normal.                                     |

---

📐 Arquitetura visual: [`.arch/architecture.drawio`](.arch/architecture.drawio)
(abra em <https://app.diagrams.net> ou na extensão *Draw.io Integration* do VS
Code).
