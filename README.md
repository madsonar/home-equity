# CashMe Credit Intelligence Agent

Agente conversacional de análise de crédito imobiliário (**Home Equity**) que combina **múltiplos LLMs**, **RAG**, **web scraping**, **parsing de documentos**, **Machine Learning** e uma **SPA React** (admin + área do cliente) para apoiar originação e análise de crédito com garantia de imóvel.

Projeto construído como POC técnica para a vaga de **Engenheiro de IA – CashMe (Grupo Cyrela)**, cobrindo de ponta a ponta o stack descrito na descrição da vaga, com infra observável, interface web e limites de recursos configurados para rodar em uma workstation.

> 📖 **[Guia passo-a-passo para subir e testar tudo](./GUIDE.md)** &nbsp;·&nbsp;
> 🏗️ **[Diagrama de arquitetura (drawio)](./.arch/architecture.drawio)**
> &nbsp;·&nbsp; 🔧 Zero hardcode: tudo em `.env` + factory em
> [app/infrastructure/llm/providers.py](app/infrastructure/llm/providers.py)

## 📑 Sumário

1. [Contexto de negócio](#1-contexto-de-negócio)
2. [Arquitetura técnica](#2-arquitetura-técnica)
3. [Stack tecnológico](#3-stack-tecnológico)
4. [Endpoints REST](#4-endpoints)
5. [Como rodar](#5-como-rodar)
6. [Estrutura do projeto](#6-estrutura-do-projeto)
7. [Interface web (SPA React)](#7-interface-web-spa-react) ⭐ NOVO
8. [Aderência à vaga](#8-aderência-à-vaga)
9. [Observabilidade](#9-observabilidade--stack-local)
10. [Dev Tools](#10-dev-tools--inspeção-de-dados--ml-observability)
11. [Resource limits](#11-resource-limits-docker) ⭐ NOVO
12. [Todas as URLs de acesso](#12-todas-as-urls-de-acesso)
13. [Deploy na AWS](#13-deploy-na-aws--opções)
14. [Licença](#14-licença)

---

## 1. Contexto de Negócio

A **CashMe** é a maior fintech de crédito com garantia imobiliária do Brasil (Grupo Cyrela). O produto principal — **Home Equity** — permite ao cliente usar seu imóvel como garantia para obter crédito com taxas mais baixas e prazos maiores que modalidades tradicionais.

Este agente resolve dores concretas da jornada de crédito:

| Dor do negócio | Como o agente resolve |
|---|---|
| Cliente não entende o produto Home Equity | Agente conversacional com RAG sobre base de conhecimento institucional |
| Analistas consultam múltiplas fontes (PDFs, sites, normas) | Ingestão automática via scraping (Crawl4AI) e parsing de docs (Docling) |
| Pré-análise de crédito manual e demorada | Endpoint `/score` com modelo de ML + regras (LTV, comprometimento de renda) |
| Necessidade de explicabilidade regulatória | Resposta do score inclui `risk_factors` e `explanation` em linguagem natural |
| Experimentação com múltiplos LLMs | Abstração unificada OpenAI / Gemini / DeepSeek / Cohere |

**Personas atendidas:** cliente final (simulação e dúvidas), analista de crédito (consulta rápida a normas e documentos), time de produto (experimentação com LLMs e fontes).

---

## 2. Arquitetura Técnica

```
                           ┌──────────────────────────────┐
   Usuário  ──────────────▶│      FastAPI (app/main)      │
   (Web / WhatsApp)        │       /api/v1/*              │
                           └───────────────┬──────────────┘
                                           │
              ┌────────────────────────────┼────────────────────────────┐
              ▼                            ▼                            ▼
     ┌────────────────┐          ┌────────────────┐          ┌────────────────┐
     │  Agents Layer  │          │   RAG Layer    │          │   ML Layer     │
     │ LangChain/Agno │◀────────▶│ Chroma / FAISS │          │ scikit-learn   │
     │ (tools + mem.) │          │   LlamaIndex   │          │ credit scorer  │
     └────────┬───────┘          └────────┬───────┘          └────────────────┘
              │                           │
              ▼                           ▼
     ┌────────────────┐          ┌────────────────┐
     │  LLM Providers │          │   Ingestion    │
     │ OpenAI/Gemini/ │          │ Crawl4AI +     │
     │ DeepSeek/Cohere│          │ Docling        │
     └────────────────┘          └────────────────┘
                                           │
                                           ▼
                           ┌──────────────────────────────┐
                           │  Redis (cache/sessão)        │
                           │  ChromaDB (vector store)     │
                           └──────────────────────────────┘
```

### Camadas

- **API (`app/api`)** – FastAPI com endpoints REST e documentação OpenAPI automática em `/docs`.
- **Agents (`app/agents`)** – Dois agentes intercambiáveis:
  - `langchain_agent.py` – ReAct Agent (LangGraph) com ferramentas de busca, score e scraping.
  - `agno_agent.py` – Agente via framework **Agno** (ex-Phidata), com memória e tool-use.
- **LLM (`app/llm/providers.py`)** – Factory unificada para OpenAI, Gemini, DeepSeek, Cohere.
- **RAG (`app/rag`)** – Três estratégias coexistindo para benchmark:
  - `chroma_store.py` – ChromaDB persistente (produção).
  - `faiss_store.py` – FAISS local (baixa latência, in-memory).
  - `llama_rag.py` – LlamaIndex com query engine.
- **Ingestion (`app/ingestion`)** – `scraper.py` (Crawl4AI, suporte a JS) e `doc_parser.py` (Docling para PDF/DOCX/HTML).
- **ML (`app/ml/credit_scorer.py`)** – Pipeline scikit-learn com feature engineering (LTV, DTI, idade), treino automático no startup e explicabilidade.
- **Memory (`app/memory/conversation.py`)** – Histórico de conversa por `session_id` (curto prazo in-memory, longo prazo via Redis).

---

## 3. Stack Tecnológico

Cada ferramenta da stack foi escolhida por uma razão específica. Abaixo, **o que é, por que está aqui e onde toca o código**.

### 3.1. Backend — API & Agentes

#### FastAPI 0.115
- **O que é:** framework web assíncrono em Python, baseado em Starlette + Pydantic.
- **Por que aqui:** performance próxima de Node/Go, type-hints convertidos em validação e documentação OpenAPI automaticamente, suporte nativo a WebSockets (futuro chat streaming), e ecossistema excelente de middlewares para OpenTelemetry.
- **Onde:** [app/main.py](app/main.py), [app/presentation/api/v1/](app/presentation/api/v1/).

#### Uvicorn 0.30
- **O que é:** servidor ASGI de alta performance.
- **Por que aqui:** é o runner recomendado do FastAPI; usa `uvloop` (libuv) e `httptools` para throughput alto. Em dev roda com `--reload`; em produção, 2-4 workers.
- **Onde:** invocado em [Makefile](Makefile) (`make dev`) e no `CMD` do [Dockerfile](Dockerfile).

#### Pydantic v2
- **O que é:** biblioteca de validação de dados com type-hints; o core é escrito em Rust (`pydantic-core`) e é ~10× mais rápido que a v1.
- **Por que aqui:** define os schemas de cada endpoint (`ChatRequest`, `ScoreResponse`…) com validação automática e mensagens de erro claras; também suporta `pydantic-settings` para ler `.env`.
- **Onde:** [app/config.py](app/config.py) (settings), [app/presentation/api/v1/routes/](app/presentation/api/v1/routes/) (schemas).

#### LangChain + LangGraph 1.x
- **O que é:** LangChain é um framework para compor LLMs com tools, memória e retrievers. LangGraph adiciona **grafos de estado** para agentes cíclicos (ReAct, multi-agent, HITL).
- **Por que aqui:** é o padrão de facto em agentes Python, enorme catálogo de integrações (Chroma, FAISS, OpenAI, Gemini…). O agente aqui é um `ReAct Agent` (pensamento → ação → observação) com 3 tools: `search_knowledge_base`, `score_credit`, `scrape_url`.
- **Onde:** [app/infrastructure/agents/langchain_agent.py](app/infrastructure/agents/langchain_agent.py).

#### Agno (ex-Phidata) 1.x
- **O que é:** framework alternativo de agentes, focado em **simplicidade e performance** (sem camadas de abstração pesadas do LangChain).
- **Por que aqui:** permite comparar a mesma tarefa executada por dois frameworks distintos — útil para decidir qual vai para produção. Nativamente integra memory (Redis) e tool-use.
- **Onde:** [app/infrastructure/agents/agno_agent.py](app/infrastructure/agents/agno_agent.py). O endpoint `/api/v1/chat` aceita `agent=langchain|agno`.

#### NeMo Guardrails (NVIDIA)
- **O que é:** DSL (`.co` — Colang) para definir **rails de conversa**: bloquear temas proibidos, forçar rotas, validar saídas do LLM, prevenir jailbreak.
- **Por que aqui:** crédito é setor regulado (LGPD + Bacen). Guardrails impedem que o agente dê aconselhamento financeiro personalizado indevido, vaze dados, ou seja manipulado para aprovar crédito fora das políticas.
- **Onde:** [guardrails/config.yml](guardrails/config.yml), [guardrails/main.co](guardrails/main.co), integrado em [app/infrastructure/guardrails/nemo_guardrails.py](app/infrastructure/guardrails/nemo_guardrails.py).

### 3.2. LLMs & Embeddings

#### OpenAI (GPT-4o / GPT-4o-mini)
- **Para que serve:** LLM principal do agente conversacional + geração de embeddings (`text-embedding-3-small`, 1536 dim).
- **Por que aqui:** maturidade de API, function calling estável, melhor custo/benefício do GPT-4o-mini para prod. Embeddings proprietários superam a maioria dos modelos abertos no benchmark MTEB em português.

#### Google Gemini (1.5 Pro / Flash)
- **Para que serve:** alternativa com **contexto longo** (1M tokens no Pro) — útil para colocar regulamentações inteiras no prompt sem chunking.
- **Por que aqui:** dá flexibilidade e evita lock-in em um único fornecedor. Integrado via `langchain-google-genai`.

#### DeepSeek (V3 / R1)
- **Para que serve:** alternativa **custo-eficiente** (~10× mais barato que GPT-4o) para tarefas de alta volumetria (classificação, extração).
- **Por que aqui:** R1 tem raciocínio comparável ao o1; ótima opção para score explicado em produção.

#### Cohere (Command R+ / Rerank)
- **Para que serve:** LLM para RAG + **reranker nativo** (`rerank-multilingual-v3`).
- **Por que aqui:** o Rerank melhora muito a precisão do RAG com custo baixo — re-ordena top-50 do Chroma para top-5 que efetivamente alimentam o prompt.

#### sentence-transformers
- **Para que serve:** embeddings **locais** (sem API key) via modelos como `all-MiniLM-L6-v2` ou `paraphrase-multilingual-MiniLM`.
- **Por que aqui:** fallback quando não há internet/API-key, e para dev local rápido. Também é a opção recomendada para dados sensíveis que não devem sair da rede interna.

> **Factory unificada:** [app/infrastructure/llm/providers.py](app/infrastructure/llm/providers.py) — trocar de provider = mudar `LLM_PROVIDER` no `.env`.

### 3.3. RAG & Ingestão

#### ChromaDB 0.5 (porta 8001)
- **O que é:** vector database open-source com API simples, persistência em SQLite+parquet, e servidor HTTP opcional.
- **Por que aqui:** é o vector store "serverless" mais prático para começar — zero config, deploy trivial, suporta filtros por metadata. Coleção principal: `cashme_kb`.
- **Onde:** [app/infrastructure/rag/chroma_store.py](app/infrastructure/rag/chroma_store.py); dados persistidos em `./data/chroma_db/`.

#### FAISS (Facebook AI Similarity Search)
- **O que é:** biblioteca C++ da Meta para busca de vizinhos mais próximos (k-NN) em alta dimensionalidade; CPU e GPU.
- **Por que aqui:** benchmark de **latência**. FAISS in-memory é 5-20× mais rápido que Chroma HTTP em queries pequenas. Usado para comparação e para casos que exijam sub-ms.
- **Onde:** [app/infrastructure/rag/faiss_store.py](app/infrastructure/rag/faiss_store.py); índice em `./data/faiss_index/index.faiss`.

#### LlamaIndex 0.11
- **O que é:** framework de RAG com abstrações de alto nível (nós, query engines, response synthesizers).
- **Por que aqui:** oferece recursos avançados que LangChain não tem out-of-the-box: **query routing**, **sub-question decomposition**, **tree summarization**. Útil para perguntas complexas que exigem múltiplas recuperações.
- **Onde:** [app/infrastructure/rag/llama_rag.py](app/infrastructure/rag/llama_rag.py).

#### Crawl4AI
- **O que é:** web scraper open-source com Playwright embutido, extração estruturada (schema via LLM) e saída direta em Markdown limpo.
- **Por que aqui:** sites de crédito dependem de JS (SPAs React/Vue) — scrapers simples (requests+bs4) falham. Crawl4AI renderiza a página como um navegador real, cache local, paralelismo, e já entrega o conteúdo pronto para chunking.
- **Onde:** [app/infrastructure/ingestion/scraper.py](app/infrastructure/ingestion/scraper.py), endpoint `POST /api/v1/ingest/url`.

#### Docling (IBM Research)
- **O que é:** parser de documentos (PDF, DOCX, HTML, PPTX) que preserva **estrutura**: tabelas, listas, títulos, reading order. Usa modelos de ML (layout detection) para PDFs difíceis.
- **Por que aqui:** documentos de crédito (contratos, certidões, matrículas) vêm em PDFs com tabelas complexas. PyPDF2/pdfplumber perdem estrutura; o Docling gera um `DoclingDocument` rico que converte limpo para Markdown.
- **Onde:** [app/infrastructure/ingestion/doc_parser.py](app/infrastructure/ingestion/doc_parser.py), endpoint `POST /api/v1/ingest/doc`.

### 3.4. Machine Learning — Credit Scoring

#### scikit-learn
- **O que é:** biblioteca canônica de ML clássico em Python.
- **Por que aqui:** o scorer é um `GradientBoostingClassifier` + `StandardScaler` num `Pipeline`. Simples, explicável, rápido em CPU, e com **feature importance** nativa — requisito regulatório (BACEN Resolução 4.557 exige explicabilidade de decisões de crédito).
- **Onde:** [app/infrastructure/ml/credit_scorer.py](app/infrastructure/ml/credit_scorer.py). Modelo salvo em `./data/credit_model.pkl`.

#### Feature engineering
- **LTV** (Loan-to-Value) = `requested_amount / property_value` — principal indicador de risco de garantia.
- **DTI** (Debt-to-Income) = `monthly_installment / monthly_income` — comprometimento de renda.
- **Age bucket** (faixa etária), **employment stability** (anos de emprego).
- **Onde:** função `_build_features()` no mesmo arquivo.

#### Explicabilidade
- Cada response de `/score` inclui `risk_factors` (lista de strings) e `explanation` (texto em português) — gerados a partir da feature importance e regras de negócio (ex.: `LTV > 0.6` → "alto comprometimento da garantia").

### 3.5. Frontend — SPA React

Interface web single-page em [app/presentation/web/](app/presentation/web/), servida pelo próprio FastAPI em **`/ui`** após build.

#### React 18.3
- **Por que aqui:** ecossistema gigante, time de front/full-stack onboarda em horas, e `Suspense` + `concurrent rendering` dão UX responsiva para a área do cliente.

#### Vite 5.4
- **O que é:** bundler que usa ESM nativo em dev (sem "bundling de dev") e Rollup em prod.
- **Por que aqui:** dev-server sobe em <1s, HMR instantâneo. Build de prod em ~3s gera ~195kB JS (61kB gzipped).

#### TypeScript 5.5
- **Por que aqui:** os schemas do backend (Pydantic) mapeiam 1:1 para interfaces TS em [src/lib/api.ts](app/presentation/web/src/lib/api.ts), prevenindo erros de contrato.

#### Tailwind CSS 3.4
- **Por que aqui:** utility-first elimina CSS órfão, gera bundle mínimo (só classes usadas), e o `theme.extend.colors.brand` replica o verde CashMe.

#### React Router 6.26
- **Por que aqui:** roteamento declarativo com **nested routes** — o `Layout` com sidebar é uma rota pai, e cada página é `<Outlet />`. `basename="/ui"` para co-hospedar com a API.

> Estrutura completa de rotas e payloads em [§7](#7-interface-web-spa-react).

### 3.6. Dados & Cache

#### Redis 7 (porta 6379)
- **O que é:** in-memory key-value store + estruturas (streams, sorted sets, pub/sub).
- **Por que aqui:** 3 usos — (a) **sessões de chat** por `session_id` com TTL; (b) **cache de embeddings** (evita re-chamar OpenAI para o mesmo texto); (c) **memory backend** do Agno agent.
- **Onde:** [app/infrastructure/memory/conversation.py](app/infrastructure/memory/conversation.py).

#### Snowflake (opcional)
- **O que é:** data warehouse cloud.
- **Por que aqui:** em produção, a CashMe/Cyrela tem Snowflake com dados reais de originação — o conector permite alimentar fine-tuning do scorer com dados históricos, sem ETL manual.
- **Onde:** [app/infrastructure/data/snowflake.py](app/infrastructure/data/snowflake.py).

#### PostgreSQL 16 (langfuse-db)
- **Para que serve:** backend relacional do Langfuse (traces, projetos, users). Sobe apenas com profile `langfuse`.

### 3.7. Observabilidade (profile `monitoring`)

#### OpenTelemetry Collector (portas 4317 gRPC / 4318 HTTP)
- **O que é:** proxy vendor-neutro que **recebe telemetria** (traces, métricas, logs) e roteia para backends.
- **Por que aqui:** desacopla a app dos backends — hoje Tempo+Prometheus, amanhã X-Ray+CloudWatch, zero mudança no código.
- **Onde:** configuração em [monitoring/otel-collector/config.yml](monitoring/otel-collector/config.yml).

#### Grafana Tempo 2.5 (porta 3200)
- **O que é:** distributed tracing storage do Grafana Labs (equivalente ao Jaeger, mas com melhor integração).
- **Por que aqui:** `metrics_generator` gera automaticamente **RED metrics** (Rate/Errors/Duration) e **service graph** a partir dos spans — sem código adicional na app.

#### Prometheus 2.54 (porta 9090)
- **O que é:** time-series database + linguagem de query (PromQL) + scraper.
- **Por que aqui:** stack de observabilidade padrão em K8s. Faz scrape do `/metrics` da app (via `prometheus-fastapi-instrumentator`) e recebe span metrics do Tempo via `remote_write`.

#### Grafana Loki 3.1 (porta 3100)
- **O que é:** "Prometheus para logs" — indexa apenas labels, comprime o conteúdo.
- **Por que aqui:** custo de armazenamento de logs ~10× menor que Elasticsearch. Promtail coleta logs dos containers Docker e encaminha via push.

#### Promtail
- **O que é:** agente oficial de envio de logs para Loki (equivalente ao Filebeat).
- **Por que aqui:** lê `/var/lib/docker/containers` e já adiciona labels `container_name`, `compose_service`, `stream` automaticamente.

#### Grafana 11.1 (porta 3001)
- **O que é:** UI unificada para métricas, traces e logs.
- **Por que aqui:** 3 datasources provisionadas (Prom/Tempo/Loki) + dashboard `CashMe — API Overview` já carregado no boot via [monitoring/grafana/provisioning/](monitoring/grafana/provisioning/).
- **Credenciais:** `admin / cashme123`.

#### Langfuse 2 (porta 3002)
- **O que é:** observabilidade **específica para LLMs** — captura cada prompt, resposta, tokens consumidos, custo em USD, latência.
- **Por que aqui:** Prometheus/Tempo não entendem o que é um "prompt" — o Langfuse dá visualização de conversas inteiras, eval automática e comparação entre modelos (ideal para decidir entre GPT-4o e Gemini).

### 3.8. Dev Tools (profile `devtools`)

#### RedisInsight 2 (porta 5540)
- **Para que serve:** UI oficial da Redis Inc. Mostra keys, TTL, memória por tipo, slow-log, CLI integrada.
- **Por que aqui:** debugar sessões de chat perdidas ou cache de embeddings em minutos (vs. `redis-cli KEYS *`).

#### Chromadb Admin (porta 3500)
- **Para que serve:** UI web (Next.js) para inspecionar coleções do Chroma — lista documentos, metadados, permite busca por similaridade.
- **Por que aqui:** validar visualmente se a ingestão funcionou (ex.: "o chunk do capítulo X foi indexado?").

#### Phoenix (Arize AI, porta 6006)
- **Para que serve:** plataforma OSS de LLM observability + **visualização de embeddings em 2D** via UMAP/t-SNE, trace detalhado de agent-tool-use, e eval LLM-as-judge.
- **Por que aqui:** é a **única** ferramenta que combina trace de agente e UMAP de embeddings. Quando o RAG retorna chunk "errado", o UMAP mostra por que (similaridade semântica com o query).

#### MLflow 2.16 (porta 5500)
- **Para que serve:** experiment tracking (params, metrics, artifacts), model registry, serving.
- **Por que aqui:** quando o fine-tuning do scorer for para produção, cada run vira um experimento versionado — auditoria regulatória exige isso.

#### Jupyter Lab 4 (porta 8888)
- **Para que serve:** notebooks com o **repo inteiro montado** como volume (`/home/jovyan/work`).
- **Por que aqui:** prototipar prompt, inspecionar `credit_model.pkl`, testar queries Chroma sem precisar refazer o fluxo inteiro da app.
- **Token:** `cashme`.

### 3.9. Integrações & Ferramentas Transversais

#### Twilio / Meta Cloud API (WhatsApp)
- **Para que serve:** canal de chat por WhatsApp — webhook em `/webhooks/whatsapp`.
- **Por que aqui:** 75% dos brasileiros usam WhatsApp — canal obrigatório para crédito B2C.
- **Onde:** [app/infrastructure/messaging/whatsapp.py](app/infrastructure/messaging/whatsapp.py), [app/presentation/webhooks/whatsapp.py](app/presentation/webhooks/whatsapp.py).

#### Docker + Docker Compose v2
- **Para que serve:** orquestração de 16 containers em 4 profiles (`default`/`monitoring`/`langfuse`/`devtools`).
- **Por que aqui:** paridade dev↔prod (AWS ECS/EKS aceita o mesmo `Dockerfile`), e profiles permitem rodar só o necessário em máquinas pequenas.

#### Loguru
- **Para que serve:** logs Python com API simples (`logger.info(...)`, sem `logger = logging.getLogger(...)`), formatação colorida em dev, JSON em prod.
- **Por que aqui:** integra fácil com OTel — o middleware de tracing injeta `trace_id` em cada log, permitindo correlação no Grafana.

#### Ruff
- **Para que serve:** linter + formatter Python escrito em Rust. Substitui `black` + `isort` + `flake8` + `pylint` — 10-100× mais rápido.
- **Por que aqui:** CI roda em <1s; dev pode rodar em cada save.

---

## 4. Endpoints

A documentação interativa completa fica em **http://localhost:8000/docs** após subir a aplicação.

| Método | Rota | Descrição |
|---|---|---|
| `GET`  | `/api/v1/health`      | Healthcheck |
| `POST` | `/api/v1/chat`        | Conversa com o agente (escolha `langchain` ou `agno`, provider e model) |
| `POST` | `/api/v1/ingest/url`  | Scraping de URL e indexação na base vetorial |
| `POST` | `/api/v1/ingest/doc`  | Upload de PDF/DOCX/MD para indexação |
| `GET`  | `/api/v1/search?q=`   | Busca semântica direta no ChromaDB |
| `POST` | `/api/v1/score`       | Análise de crédito (score + aprovação + fatores de risco) |

### Exemplos rápidos

**Chat:**
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Como funciona o Home Equity da CashMe?", "session_id": "user-123"}'
```

**Score de crédito:**
```bash
curl -X POST http://localhost:8000/api/v1/score \
  -H "Content-Type: application/json" \
  -d '{
    "monthly_income": 15000,
    "property_value": 800000,
    "requested_amount": 300000,
    "employment_years": 5,
    "age": 38
  }'
```

**Ingestão de URL:**
```bash
curl -X POST http://localhost:8000/api/v1/ingest/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.cashme.com.br/home-equity"}'
```

---

## 5. Como Rodar

### Pré-requisitos

- Python 3.11+
- Docker e Docker Compose (recomendado)
- Chave de API de ao menos um LLM (OpenAI recomendado)

### 5.1. Configuração do `.env`

```bash
cp .env.example .env
# edite .env e preencha OPENAI_API_KEY (mínimo)
```

### 5.2. Opção A — Docker Compose (recomendado)

**Atalho para subir a stack COMPLETA (app + observabilidade + devtools + langfuse):**

```bash
make up-all
```

Esse comando sobe todos os 16 containers e imprime automaticamente a lista de endereços de acesso no terminal. Para re-imprimir sem reiniciar: `make urls`. Para derrubar: `make down-all`.

---

Se preferir controle granular, pode subir em camadas. Primeiro a app mínima (`app` + `chromadb` + `redis`):

```bash
make docker-up
# ou: docker compose up -d
```

Acesse:
- API: http://localhost:8000
- SPA: http://localhost:8000/ui
- Swagger: http://localhost:8000/docs
- ChromaDB: http://localhost:8001

Outros comandos úteis:
```bash
make docker-logs      # logs em tempo real
make docker-restart   # reinicia apenas o app
make docker-shell     # shell no container
make docker-down      # para tudo
make docker-clean     # remove volumes e imagens locais

# Camadas opcionais (ver seção 10)
make monitoring-up    # Prometheus + Grafana + Tempo + Loki + OTel Collector
make langfuse-up      # Langfuse (LLM observability)
make devtools-up      # RedisInsight + Chroma Admin + Phoenix + MLflow + Jupyter
make full-up          # app + monitoring + langfuse (sem devtools)
```

### 5.3. Opção B — Local (sem Docker)

```bash
make setup            # cria .venv e instala dependências
make dev              # sobe uvicorn na porta 8000 com reload
```

> Em modo local, ajuste `CHROMA_HOST=localhost` no `.env` (ou rode apenas o ChromaDB via `docker compose up -d chromadb redis`).

### 5.4. Comandos de desenvolvimento

```bash
make train-model      # treina/retreina o modelo de credit scoring
make ingest-kb        # indexa data/knowledge_base no ChromaDB + FAISS
make test             # valida imports e lógica de todos os módulos
make test-endpoints   # testa endpoints REST (requer server em :8000)
make lint             # ruff check
make fmt              # ruff format
make clean            # limpa __pycache__
```

### 5.5. Frontend (SPA React)

```bash
make web-install      # npm install em app/presentation/web
make web-dev          # Vite dev-server em http://localhost:5173 (proxy /api → :8000)
make web-build        # gera dist/ servido automaticamente em http://localhost:8000/ui
make web-clean        # remove node_modules/ e dist/
```

> O **Dockerfile** já faz o build do SPA via stage Node (multi-stage) — `make docker-build` produz uma imagem com o frontend embutido. O backend monta `dist/` em `/ui` via `StaticFiles` (ver [app/main.py](app/main.py)).

---

## 6. Estrutura do Projeto

```
cashme/
├── app/
│   ├── main.py                 # Entrypoint FastAPI + lifespan
│   ├── config.py               # Settings via pydantic-settings
│   ├── api/routes.py           # Endpoints REST
│   ├── agents/
│   │   ├── langchain_agent.py  # Agente ReAct (LangGraph)
│   │   └── agno_agent.py       # Agente Agno
│   ├── llm/providers.py        # Factory multi-LLM
│   ├── rag/
│   │   ├── chroma_store.py     # ChromaDB
│   │   ├── faiss_store.py      # FAISS
│   │   └── llama_rag.py        # LlamaIndex
│   ├── ingestion/
│   │   ├── scraper.py          # Crawl4AI
│   │   └── doc_parser.py       # Docling
│   ├── ml/credit_scorer.py     # Pipeline sklearn + regras
│   └── memory/conversation.py  # Histórico por sessão
├── data/
│   ├── knowledge_base/         # Docs institucionais (md)
│   └── sample_docs/            # Exemplos para testes
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── requirements.txt
└── .env.example
```

---

## 7. Interface Web (SPA React)

A camada `presentation/web` é uma SPA React + Vite + TypeScript + Tailwind que consome a própria API REST (`/api/v1/*`). Pensada para duas audiências:

- **`/admin`** — backoffice do time CashMe (ingestão de KB, busca semântica, gestão do modelo).
- **`/cliente`** — área do cliente final (simulação, chat, envio de documentos, propostas).

### 7.1. Rotas

#### Backoffice (`/ui/admin`)

| Rota | Função | API consumida |
|---|---|---|
| `/admin` | Dashboard com healthcheck + links para Grafana/Prometheus/Langfuse/Phoenix/MLflow | `GET /api/v1/health` |
| `/admin/kb` | Ingestão de **URL** (Crawl4AI) e upload de **arquivo** (Docling) | `POST /api/v1/ingest/url`, `POST /api/v1/ingest/doc` |
| `/admin/search` | Busca semântica com top-K configurável, score de similaridade por resultado | `GET /api/v1/search?q=…&k=…` |
| `/admin/model` | Retreinamento manual do credit scorer + AUC-ROC da última rodada | `POST /api/v1/score/retrain` |

#### Área do cliente (`/ui/cliente`)

| Rota | Função | API consumida |
|---|---|---|
| `/cliente` | Landing com cards de jornada | — |
| `/cliente/simulador` | Formulário de score (renda, imóvel, valor solicitado, idade, profissão). Exibe **score, LTV, parcela (BRL)**, fatores de risco e explicação. Botão "salvar como proposta" | `POST /api/v1/score` |
| `/cliente/chat` | Chat com histórico em `localStorage`, session_id por usuário, sugestões de perguntas | `POST /api/v1/chat` |
| `/cliente/documentos` | Envio de RG / comprovante de renda / matrícula com checklist visual | `localStorage` (POC) |
| `/cliente/propostas` | Lista de simulações salvas com status (aprovada/em análise/reprovada) | `localStorage` (POC) |

### 7.2. Como é servida

**Em produção (Docker):**
- Stage 1 do [Dockerfile](Dockerfile) (`node:20-alpine`) faz `npm ci && npm run build` e produz `dist/`.
- Stage 2 (Python) faz `COPY --from=web-builder` para `app/presentation/web/dist`.
- [app/main.py](app/main.py) monta `StaticFiles(directory=dist, html=True)` em **`/ui`** — React Router em `BrowserRouter` com `basename="/ui"` cuida do resto.
- Acesso: **http://localhost:8000/ui/** (mesma origem da API → sem CORS).

**Em desenvolvimento:**
- `make web-dev` sobe o Vite dev-server em **http://localhost:5173** com proxy `/api → http://localhost:8000`.
- Backend pode rodar via `make dev` (local) ou `make docker-up` — o SPA se conecta a ambos transparentemente.

### 7.3. Cliente HTTP tipado

Em [app/presentation/web/src/lib/api.ts](app/presentation/web/src/lib/api.ts) — `fetch` wrapper com interfaces TS alinhadas aos schemas Pydantic do backend:

```ts
api.chat({ message, session_id, agent: 'langchain' })
api.score({ monthly_income, property_value, requested_amount, ... })
api.ingestUrl({ url })
api.ingestDoc(file)  // multipart/form-data
api.search(q, k)
api.retrain()
```

---

## 8. Aderência à Vaga

| Requisito da vaga | Onde está implementado |
|---|---|
| Agentes autônomos com LangChain e Agno | [app/agents/langchain_agent.py](app/agents/langchain_agent.py), [app/agents/agno_agent.py](app/agents/agno_agent.py) |
| Memória de curto e longo prazo | [app/memory/conversation.py](app/memory/conversation.py) + Redis |
| Múltiplos LLMs (OpenAI/Gemini/DeepSeek/Cohere) | [app/llm/providers.py](app/llm/providers.py) |
| Bancos vetoriais (ChromaDB, FAISS) + RAG | [app/rag/](app/rag/) |
| Web scraping (Crawl4AI) | [app/ingestion/scraper.py](app/ingestion/scraper.py) |
| Parsing de documentos (Docling) | [app/ingestion/doc_parser.py](app/ingestion/doc_parser.py) |
| Integração via APIs (FastAPI + requests) | [app/api/routes.py](app/api/routes.py) |
| Machine Learning (scikit-learn) | [app/ml/credit_scorer.py](app/ml/credit_scorer.py) |
| LlamaIndex | [app/rag/llama_rag.py](app/rag/llama_rag.py) |
| Deployment / containerização | [Dockerfile](Dockerfile), [docker-compose.yml](docker-compose.yml) |

---

## 9. Roadmap / Próximos Passos

- [x] Observabilidade com OpenTelemetry + Langfuse para tracing de agentes
- [x] Integração WhatsApp (Twilio/Meta Cloud API)
- [x] Conector Snowflake para dados corporativos
- [x] Fine-tuning de modelo de score com dados reais da CashMe
- [x] Guardrails (NeMo Guardrails) para compliance regulatório
- [ ] CI/CD com GitHub Actions e registry privado
- [ ] Deploy na AWS (ver seção 10)

---

## 10. Observabilidade — Stack Local

A stack de observabilidade é opcional e ativada via **profiles** do Docker Compose.
Toda a infra roda em containers — zero configuração externa.

### 9.1. Componentes

| Componente        | Porta | Responsabilidade                                                   |
|-------------------|------:|---------------------------------------------------------------------|
| **OTel Collector**| 4317 (gRPC) / 4318 (HTTP) | Recebe traces e métricas OTLP da app e encaminha        |
| **Tempo**         |  3200 | Distributed tracing (storage local). Gera *span metrics* + *service graph* |
| **Prometheus**    |  9090 | Métricas (scrape da app via `/metrics` + remote-write do Tempo)    |
| **Loki**          |  3100 | Agregação de logs                                                   |
| **Promtail**      |     – | Envia logs dos containers Docker para Loki                          |
| **Grafana**       |  3001 | UI unificada. Datasources + dashboard CashMe provisionados          |
| **Langfuse**      |  3000 | Tracing específico de chamadas LLM (prompts, tokens, custo)         |

### 9.2. Fluxo de telemetria

```
 ┌────────────────┐   OTLP    ┌──────────────────┐   push     ┌──────────┐
 │  FastAPI app   │ ────────▶ │ OTel Collector   │ ─────────▶ │  Tempo   │
 │ OTEL SDK       │  :4317    │  :4317/:4318     │            │  :3200   │
 │                │           │                  │            └─────┬────┘
 │ /metrics       │           │ prom exporter    │                  │ remote_write
 │  prom-fastapi  │           │ :8889            │                  ▼
 └─────┬──────────┘           └────────┬─────────┘            ┌──────────┐
       │ scrape                         │ scrape              │Prometheus│
       └───────────────────────────────▶└───────────────────▶ │  :9090   │
                                                              └─────┬────┘
 ┌────────────────┐        ┌──────────┐      ┌──────────┐          │
 │ Docker logs    │──────▶ │ Promtail │────▶ │   Loki   │          │
 │ /var/lib/...   │        └──────────┘      │  :3100   │          │
 └────────────────┘                          └─────┬────┘          │
                                                   │               │
                                                   ▼               ▼
                                             ┌───────────────────────────┐
                                             │         Grafana :3001     │
                                             │  dashboards + explore UI  │
                                             └───────────────────────────┘
                                                   ▲
 ┌────────────────┐   SDK    ┌──────────┐          │ (link opcional)
 │ LLM calls      │ ────────▶│ Langfuse │──────────┘
 │ (chat/score)   │  :3000   │  :3000   │  UI própria
 └────────────────┘          └──────────┘
```

### 9.3. Como subir

```bash
# Apenas stack de observabilidade (app fica separada)
make monitoring-up

# Apenas Langfuse (LLM observability)
make langfuse-up

# Tudo junto: app + monitoring + langfuse
make full-up
```

Depois de subir:

| URL                           | Descrição                                  |
|-------------------------------|--------------------------------------------|
| http://localhost:3001         | Grafana (admin / cashme123)                |
| http://localhost:9090         | Prometheus UI (queries, targets)           |
| http://localhost:3200         | Tempo API                                  |
| http://localhost:3100/ready   | Loki readiness                             |
| http://localhost:3000         | Langfuse (criar projeto + copiar keys)     |
| http://localhost:8000/metrics | Métricas Prometheus da app                 |

### 9.4. Métricas de negócio expostas

Além das métricas HTTP padrão (`http_requests_total`, `http_request_duration_seconds`),
a app expõe contadores customizados em [app/infrastructure/observability/metrics.py](app/infrastructure/observability/metrics.py):

| Métrica                              | Labels            | Propósito                                  |
|--------------------------------------|-------------------|--------------------------------------------|
| `cashme_credit_score_total`          | `result`          | Aprovações vs reprovações do scoring       |
| `cashme_agent_requests_total`        | `agent_type`      | Qual agente foi usado (langchain/agno)     |
| `cashme_rag_queries_total`           | `store`           | Buscas semânticas por backend (chroma/faiss) |
| `cashme_ingest_chunks_total`         | `source_type`     | Chunks indexados (url/document)            |
| `cashme_model_prediction_seconds`    | –                 | Latência de inferência do modelo ML        |

Essas métricas alimentam o dashboard **CashMe — API Overview**, provisionado automaticamente no Grafana (pasta *CashMe*).

### 9.5. Span metrics automáticas (Tempo)

O Tempo está com `metrics_generator` ligado — para cada span recebido ele gera automaticamente:

- `traces_spanmetrics_calls_total` — RED: request rate
- `traces_spanmetrics_latency_*` — RED: latency histograms
- `traces_service_graph_request_*` — service graph (dependências entre serviços)

Tudo isso é enviado para o Prometheus via `remote_write` — sem configuração adicional.

### 9.6. Validação end-to-end (testada)

Teste realizado durante a implementação:

```bash
# 1. Subir a stack
make monitoring-up

# 2. Enviar um trace OTLP via HTTP direto (simula a app)
curl -X POST http://localhost:4318/v1/traces \
  -H 'Content-Type: application/json' \
  -d @tests/fixtures/sample_trace.json

# 3. Ler o trace de volta no Tempo
curl http://localhost:3200/api/traces/<TRACE_ID>

# 4. Conferir span metric no Prometheus
curl 'http://localhost:9090/api/v1/query?query=traces_spanmetrics_calls_total'
```

Resultados verificados:
- OTLP gRPC/HTTP recebe (200 OK no collector)
- Tempo retorna o trace por ID
- Prometheus expõe `traces_spanmetrics_*` e `traces_service_graph_*`
- Loki indexa logs de todos containers (labels `job=docker`, `stream`)
- Grafana provisionou as 3 datasources e o dashboard CashMe

---

## 11. Dev Tools — Inspeção de Dados + ML Observability

Stack opcional (perfil `devtools`) com **UIs web para inspecionar** cada peça
de dados da aplicação, visualizar iteração dos agentes e acompanhar treinos
do modelo de credit scoring. Tudo local, zero API key necessária.

### 10.1. Componentes

| Ferramenta        | Porta | O que permite ver                                                   |
|-------------------|------:|----------------------------------------------------------------------|
| **RedisInsight**  | 5540  | Keys, TTL, memória, streams, slow log, CLI do `cashme-redis`         |
| **Chroma Admin**  | 3500  | Coleções, documentos indexados, metadados, queries vetoriais ad-hoc  |
| **Phoenix (Arize)** | 6006 | Traces de agentes (tool-use step-by-step), visualização de embeddings com UMAP/t-SNE, eval LLM-as-judge |
| **MLflow**        | 5500  | Experiment tracking para fine-tuning do credit scorer (params, métricas, artefatos, comparação de runs) |
| **Jupyter Lab**   | 8888  | Notebooks com volume montado no projeto — testar prompts, debugar FAISS, analisar dataset (token: `cashme`) |

```
  ┌──────────────┐         ┌─────────────────┐       ┌────────────────────┐
  │ cashme-redis │◀────────│  RedisInsight   │ :5540 │ keys/streams/slow  │
  └──────┬───────┘         └─────────────────┘       └────────────────────┘
         │
  ┌──────┴───────┐         ┌─────────────────┐       ┌────────────────────┐
  │  chromadb    │◀────────│  Chroma Admin   │ :3500 │ colecoes + docs    │
  └──────────────┘         └─────────────────┘       └────────────────────┘

  ┌──────────────┐  OTLP   ┌─────────────────┐       ┌────────────────────┐
  │  FastAPI     │────────▶│  Phoenix :6006  │       │ agent trace + UMAP │
  │  (agentes)   │  :4319  │  (Arize)        │       │ embeddings viz     │
  └──────────────┘         └─────────────────┘       └────────────────────┘

  ┌──────────────┐ mlflow  ┌─────────────────┐       ┌────────────────────┐
  │ train_model  │────────▶│  MLflow :5500   │       │ params/metrics/art │
  │   .py        │  API    │                 │       │ comparacao de runs │
  └──────────────┘         └─────────────────┘       └────────────────────┘

  ┌──────────────┐ volume  ┌─────────────────┐       ┌────────────────────┐
  │  ./ (repo)   │────────▶│  Jupyter :8888  │       │ notebooks ad-hoc   │
  └──────────────┘ :rw     └─────────────────┘       └────────────────────┘
```

### 10.2. Como subir

```bash
make devtools-up       # sobe só os devtools
make full-up           # sobe tudo (app + monitoring + langfuse)
```

Em seguida acesse pelo navegador:

| URL                              | Ação inicial                                               |
|----------------------------------|-------------------------------------------------------------|
| http://localhost:5540            | RedisInsight conecta automático em `cashme-redis:6379`     |
| http://localhost:3500            | Chroma Admin já aponta para `http://chromadb:8000`         |
| http://localhost:6006            | Phoenix abre direto em `/projects`                          |
| http://localhost:5500            | MLflow UI                                                   |
| http://localhost:8888?token=cashme | Jupyter Lab — root `/home/jovyan/work` = repo montado    |

### 10.3. O que cada um resolve na prática

- **RedisInsight** — inspecionar sessões de chat por `session_id`, debugar cache de embeddings, ver TTL de tokens de agente, monitorar memória e comandos lentos.
- **Chroma Admin** — listar coleções (`cashme_kb`, etc.), ver chunks indexados, inspecionar metadados (source/url), rodar busca por similaridade sem código.
- **Phoenix** — única ferramenta open-source que combina **trace de agente** (cada tool call, cada prompt LLM) com **visualização 2D/3D de embeddings** (UMAP). Excelente para entender por que o agente escolheu uma tool ou por que o RAG retornou um chunk "errado". Aceita OTLP direto em `:4319` (mapeado para não colidir com o otel-collector principal).
- **MLflow** — quando subir o fine-tuning real do credit scorer, cada execução vira um *run* com params (learning rate, features), métricas (AUC, KS, PSI) e artefatos (modelo `.pkl`, feature importance). Comparação visual entre runs.
- **Jupyter** — prototipar rapidamente: ler o `faiss_index/index.faiss`, inspecionar `data/credit_model.pkl`, testar prompts diretamente contra a API.

### 10.4. Validação (testada)

```bash
# 1. Subir
docker compose up -d redis chromadb
make devtools-up

# 2. Smoke test HTTP (cada UI)
curl -o /dev/null -w "RedisInsight %{http_code}\n" http://localhost:5540/api/health   # 200
curl -o /dev/null -w "ChromaAdmin  %{http_code}\n" http://localhost:3500/             # 200
curl -o /dev/null -w "Phoenix      %{http_code}\n" http://localhost:6006/             # 200
curl -o /dev/null -w "MLflow       %{http_code}\n" http://localhost:5500/health       # 200
curl -o /dev/null -w "Jupyter      %{http_code}\n" "http://localhost:8888/api?token=cashme"  # 200

# 3. RedisInsight conecta automaticamente (via env RI_REDIS_HOST=redis)
curl http://localhost:5540/api/databases   # retorna cashme-redis cadastrado

# 4. Popular dados para ver na UI
docker exec cashme-redis redis-cli SET "cashme:session:demo" '{"turns":3}' EX 3600
# agora a key aparece no RedisInsight (Browser → cashme-redis)
```

Todos os serviços sobem em ~20s (Phoenix/Jupyter são os mais pesados). As UIs persistem configuração em volumes Docker (`redisinsight_data`, `phoenix_data`, `mlflow_data`, `jupyter_data`) — estado preservado entre restarts.

### 10.5. Integração opcional com o código

- **Phoenix no lugar de Tempo** (para debug local rápido): basta trocar `OTLP_ENDPOINT=http://phoenix:4317` no `.env` e a app passa a enviar traces direto pro Phoenix em vez do collector.
- **MLflow no `train_model.py`**: adicionar `mlflow.set_tracking_uri("http://localhost:5500")` + `mlflow.log_params()` / `log_metrics()` / `log_artifact()` no script de treino.
- **Phoenix instrumentation automática**: `pip install openinference-instrumentation-langchain` liga tracing de cada step dos agentes LangChain sem mexer no código.

---

## 12. Resource Limits (Docker)

Todos os 16 containers do `docker-compose.yml` declaram **limits** e **reservations** de CPU/memória via anchors YAML (`x-res-xs/s/m/l`). Isso evita que algum container (p.ex. Phoenix com UMAP) consuma toda a RAM e derrube a workstation.

### 12.1. Tiers

| Anchor | CPU limit | Mem limit | CPU reserva | Mem reserva | Usado por |
|---|---:|---:|---:|---:|---|
| `x-res-xs` | 0.25 | 192 MiB | 0.05 | 64 MiB | `promtail`, `redisinsight`, `chroma-admin` |
| `x-res-s`  | 0.50 | 384 MiB | 0.10 | 128 MiB | `redis`, `otel-collector`, `loki`, `langfuse-db` |
| `x-res-m`  | 1.00 | 768 MiB | 0.25 | 384 MiB | `chromadb`, `prometheus`, `grafana`, `tempo`, `phoenix`, `mlflow` |
| `x-res-l`  | 2.00 | 2 GiB   | 0.50 | 1 GiB   | `app`, `langfuse`, `jupyter` |

### 12.2. Totais

Com **todos os profiles** ativos simultaneamente (`make full-up && make devtools-up`):

- **Limites somados (teto):** ~15 CPU / ~13 GiB RAM
- **Reservas somadas (piso):** ~3.3 CPU / ~3.8 GiB RAM

Como os limites quase nunca saturam ao mesmo tempo, uma workstation com **4 cores / 8 GiB** já roda a stack completa confortavelmente. Em máquinas menores, rode apenas os profiles necessários:

```bash
make docker-up         # só app + redis + chromadb          (~3 CPU / 3 GiB)
make monitoring-up     # + stack observabilidade            (+4 CPU / 3 GiB)
make devtools-up       # + UIs de inspeção                  (+3 CPU / 3 GiB)
make langfuse-up       # + Langfuse                          (+2.5 CPU / 2.4 GiB)
```

### 12.3. Ajuste fino

Se precisar dar mais folga a um container (ex.: ingestão pesada no Jupyter), edite o anchor no topo do `docker-compose.yml`:

```yaml
x-res-l: &res-l
  resources:
    limits:
      cpus: '3.0'      # <<< aumentar aqui
      memory: 3G
```

Mudança afeta todos os serviços do mesmo tier — para um ajuste pontual, substitua `deploy: *res-l` pelo bloco inline no serviço específico.

---

## 13. Todas as URLs de Acesso

Após `make full-up && make devtools-up`:

### 13.1. Aplicação

| URL | O que é |
|---|---|
| **http://localhost:8000/** | API root (info + links) |
| **http://localhost:8000/ui** | ⭐ **SPA React** (admin + área do cliente) |
| http://localhost:8000/docs | Swagger/OpenAPI interativo |
| http://localhost:8000/redoc | ReDoc (documentação alternativa) |
| http://localhost:8000/metrics | Métricas Prometheus da app |
| http://localhost:8000/api/v1/health | Healthcheck JSON |

### 13.2. Dados

| URL | Credenciais | O que é |
|---|---|---|
| http://localhost:8001 | — | ChromaDB (vector store, API v2) |
| redis://localhost:6379 | — | Redis (conectar via `redis-cli` ou RedisInsight) |

### 13.3. Observabilidade (profile `monitoring` + `langfuse`)

| URL | Credenciais | O que é |
|---|---|---|
| http://localhost:3001 | admin / `cashme123` | **Grafana** — dashboard CashMe provisionado |
| http://localhost:9090 | — | Prometheus UI (queries + targets) |
| http://localhost:3200 | — | Tempo API (ler trace por ID) |
| http://localhost:3100/ready | — | Loki readiness |
| http://localhost:3002 | crie user no 1º acesso | **Langfuse** — LLM tracing (prompts/tokens/custo) |
| http://localhost:4317 | gRPC | OTLP ingestion (interno — app envia para cá) |
| http://localhost:4318 | HTTP | OTLP ingestion HTTP (debug com `curl`) |

### 13.4. Dev tools (profile `devtools`)

| URL | Credenciais | O que é |
|---|---|---|
| http://localhost:5540 | — | **RedisInsight** (Redis já pré-configurado) |
| http://localhost:3500 | — | **Chroma Admin** (aponta para `chromadb:8000`) |
| http://localhost:6006 | — | **Phoenix** (Arize) — agent traces + embeddings UMAP |
| http://localhost:5500 | — | **MLflow** — experiment tracking |
| http://localhost:8888/?token=cashme | token `cashme` | **Jupyter Lab** — notebooks ad-hoc (volume do repo montado) |

### 13.5. Frontend dev-only

| URL | Quando |
|---|---|
| http://localhost:5173 | `make web-dev` (Vite dev-server com HMR) |

---

## 14. Deploy na AWS — Opções

A aplicação foi desenhada *cloud-agnostic*: toda dependência externa é um container
ou service com endpoint HTTP. Existem três caminhos principais para rodar na AWS,
ordenados do mais simples ao mais completo:

### 11.1. Opção A — ECS Fargate  *(recomendada para MVP/POC)*

**Quando usar:** validar em produção rápido, sem time de SRE dedicado.

| Camada              | Serviço AWS                                        | Observação                                      |
|---------------------|----------------------------------------------------|-------------------------------------------------|
| API FastAPI         | **ECS Fargate** atrás de **ALB**                   | Auto-scaling por CPU/RPS, TLS no ALB            |
| Imagem              | **ECR**                                            | Build via GitHub Actions → push ECR             |
| Redis               | **ElastiCache for Redis** (t4g.micro)              | Sessão/cache                                    |
| Vector store        | **ECS sidecar Chroma** *ou* **OpenSearch Serverless** (com k-NN) | OpenSearch é mais gerenciado, Chroma é mais barato |
| Segredos            | **Secrets Manager** (API keys LLM, Twilio, Snowflake) | Injetados via `secrets` da task definition     |
| Storage (modelos, docs) | **S3** (bucket versionado)                      | Substitui volume `./data`                       |
| Logs                | **CloudWatch Logs** (awslogs driver)               | Nativo no Fargate                               |
| Métricas            | **CloudWatch Container Insights** + **AMP** (Managed Prometheus) | AMP ingere `/metrics`          |
| Traces              | **AWS X-Ray** via **ADOT Collector** sidecar       | ADOT = OTel Collector distro da AWS             |
| Dashboards          | **AMG** (Grafana gerenciado)                       | Mesma config do compose, datasources para AMP/X-Ray/CWL |
| LLM Observability   | **Langfuse Cloud** *ou* ECS task própria + RDS Postgres | Cloud é plug-and-play                      |

**Esforço estimado:** Terraform de ~400 linhas; migração do compose é praticamente 1:1.

**Pontos de atenção:**
- Fargate não suporta GPU → inferência de modelos locais (sentence-transformers) fica no CPU.
  Para embeddings em escala, usar **Bedrock** (Titan Embeddings) ou **SageMaker Endpoint**.
- Volumes efêmeros → modelos `.pkl` devem vir do S3 no startup (já abstraído em [app/infrastructure/ml/credit_scorer.py](app/infrastructure/ml/credit_scorer.py)).

### 11.2. Opção B — EKS *(quando já existe Kubernetes na casa)*

**Quando usar:** CashMe/Cyrela já tem EKS; múltiplos times compartilham o cluster.

- Todos os containers do `docker-compose.yml` viram **Deployments** + **Services**.
- Stack de observabilidade: usar **kube-prometheus-stack** (Helm) — já traz Prometheus, Grafana, Alertmanager.
  Substituir Tempo/Loki por **Grafana Tempo/Loki via Helm** (mesmos YAMLs de config que usamos).
- Alternativa gerenciada: **AMP** + **AMG** + **CloudWatch** (mesmas peças da opção A, só muda o compute).
- Ingress: **AWS Load Balancer Controller** (ALB ingress).
- GPU opcional: node group com `g5.xlarge` para fine-tuning de modelos locais.

**Esforço:** Helm charts (app + monitoring-stack) ~300 linhas; mais setup, menos lock-in AWS.

### 11.3. Opção C — Serverless nativo AWS  *(para tráfego esporádico)*

**Quando usar:** baixo volume, muitos picos, custo variável.

| Camada       | Serviço                                              |
|--------------|------------------------------------------------------|
| API          | **Lambda + API Gateway** (FastAPI com *Mangum*)      |
| Agentes LLM  | **Bedrock Agents** (substitui LangChain/Agno)        |
| RAG          | **Bedrock Knowledge Bases** (OpenSearch Serverless + Titan embeddings) |
| Ingestão     | **Step Functions** + **Lambda** + **S3 events**      |
| Vetor        | **OpenSearch Serverless** (k-NN)                     |
| Cache        | **DynamoDB** ou **ElastiCache Serverless**           |
| Obs.         | **CloudWatch** + **X-Ray** (nativos no Lambda)       |

**Trade-off:** perde o controle fino sobre agentes (Bedrock Agents substitui LangChain), ganha em simplicidade operacional e custo zero quando ocioso. Recomendado só se a governança aceitar *vendor lock-in* em Bedrock.

### 11.4. Resumo — qual escolher?

```
    Time ops / flexibilidade ↑
         │
    EKS  ┤●                 ◐ ECS Fargate
         │                      (recomendada)
         │
    Lambda+Bedrock  ●
         │
         └─────────────────────▶ custo fixo mensal ↑
```

**Recomendação para CashMe:** começar em **ECS Fargate** (opção A) — Terraform do `docker-compose.yml`
é quase mecânico, time de 1-2 engenheiros sobe em ~2 semanas, e migrar para EKS depois é tranquilo
porque a app é stateless e cada dependência é trocável por um service equivalente.

Para a parte de **IA/LLM**, independentemente da opção de compute, avaliar:
- **Bedrock** para inferência de LLMs (Claude/Titan/Llama) — evita sair com tráfego para OpenAI.
- **SageMaker** para fine-tuning do modelo de credit scoring quando houver dados reais.

---

## 15. Licença

Projeto de estudo/POC. Uso interno.
