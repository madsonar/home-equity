# Plano AWS — 3 opções (referência)

> Documento de referência. **A opção escolhida foi `02-vm-single-deploy.md` (VM única).**

## Inventário de serviços (do compose)

| Categoria | Serviço | Stateful? | Sugestão AWS |
|---|---|---|---|
| App | `app` (FastAPI + LangGraph + WS) | não (state em DB/Redis) | ECS Fargate / EKS / App Runner |
| DB relacional | `cashme-db` (Postgres 16) | sim | RDS Postgres / Aurora Serverless v2 |
| Vector store | `chromadb` | sim | EFS+ECS, ou trocar por OpenSearch Serverless / pgvector |
| Cache/sessão | `redis` | sim | ElastiCache Redis |
| Storage docs/anexos | volumes locais (`./data`, FAISS) | sim | S3 + EFS ou pgvector |
| Tracing/Métricas/Logs | otel collector, prometheus, tempo, loki, grafana, promtail | parcial | AWS Managed Grafana + Managed Prometheus + X-Ray + CloudWatch |
| LLM observability | Langfuse + Postgres | sim | ECS+RDS dedicado, ou Langfuse Cloud |
| Dev tools | RedisInsight, Chroma admin, Phoenix, MLflow, Jupyter | dev-only | NÃO subir em prod |
| Modelo ML | credit_scorer (joblib) | artefato | S3 + carregar no boot, ou SageMaker Endpoint |
| LLM | OpenAI/Gemini/Anthropic | externo | manter SaaS ou Bedrock |
| Frontend SPA | React build estático | sim (assets) | S3 + CloudFront |

---

## Opção A — App Runner + RDS + ElastiCache + S3 (POC)

- App Runner: build do Dockerfile, autoscale 1→N, HTTPS automático, deploy via ECR.
- RDS Postgres (db.t4g.micro com pgvector → resolve Postgres + Chroma).
- ElastiCache Redis cache.t4g.micro.
- S3 para anexos + artefato ML + frontend (CloudFront na frente).
- CloudWatch para logs/métricas; sem Tempo/Loki/Grafana próprios.
- Secrets em Secrets Manager.

**Limitações:** App Runner tem restrição em WebSockets longos e em workloads com state em memória (FAISS efêmero).

**Custo estimado:** ~US$ 80–150/mês (ex-LLM).

---

## Opção B — ECS Fargate + ALB + RDS + ElastiCache + OpenSearch/pgvector + S3 + CloudFront (recomendado)

- ECS Fargate Service (1 task definition para o `app`), autoscaling por CPU/RPS.
- ALB com sticky sessions e suporte a WebSocket (`/ws/*` no mesmo target group).
- RDS Postgres Multi-AZ db.t4g.small (ou Aurora Serverless v2).
- ElastiCache Redis Multi-AZ.
- OpenSearch Serverless (k-NN) ou pgvector para o RAG (recomendo pgvector).
- EFS opcional para FAISS persistente entre tasks.
- S3 + CloudFront para frontend.
- Secrets Manager + Parameter Store.
- CloudWatch Logs (com FireLens) + AWS Distro for OpenTelemetry → AWS Managed Prometheus + AWS Managed Grafana + X-Ray.
- CI/CD: GitHub Actions → ECR → ECS deploy (rolling).

**Custo estimado:** ~US$ 250–500/mês (ex-LLM).

---

## Opção C — EKS + Karpenter + Aurora + Bedrock (enterprise)

- EKS com Karpenter (spot para experts), namespaces por ambiente.
- Helm charts: app, langfuse, chroma StatefulSet ou substituir por pgvector.
- Aurora Postgres (HA + read replicas).
- ElastiCache Redis Cluster Mode (sharded).
- SQS ou MSK (Kafka) para a fila de simulações.
- Bedrock para LLM (compliance/locale BR-São Paulo) + Bedrock Knowledge Bases ou OpenSearch Serverless.
- SageMaker Endpoint para o credit scorer.
- WAF + Shield + Cognito (substitui JWT caseiro).
- AWS Managed Grafana / Prometheus / X-Ray + CloudWatch + Datadog/Langfuse Cloud.
- CI/CD: GitHub Actions → ECR → ArgoCD/Flux.

**Custo estimado:** US$ 1.5k–5k/mês baseline (ex-LLM, Bedrock).

---

## Mudanças de código necessárias (qualquer opção gerenciada)

1. Frontend separado: servir `dist/` em S3+CloudFront.
2. Storage de anexos (FAISS upload): hoje em memória → S3 (presigned URLs).
3. LangGraph: trocar `MemorySaver` por `PostgresSaver`.
4. Chroma → pgvector (recomendado).
5. Secrets vindos de Secrets Manager.
6. Healthcheck em `/api/v1/health` (já existe) → target group ALB.
7. WebSocket no ALB: `idle_timeout >= 600s`.
8. Build multi-stage no Dockerfile (~1.37 GB → meta < 600 MB).
9. CORS / CSRF / HTTPS only e remover `JWT_SECRET_KEY` default.
10. Migrações com Alembic (hoje é `Base.metadata.create_all`).
