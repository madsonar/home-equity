# Arquitetura de produção — HomeEquity

Estado da infraestrutura que serve <https://homeequity.digitalcodigos.com.br>.
Atualizado em 18/09/2026.

Diagrama: [`.doc/flows/infra-highlevel.mmd`](../.doc/flows/infra-highlevel.mmd)
(fonte Mermaid), [`.drawio`](../.doc/flows/infra-highlevel.drawio) (editável) e
[`.png`](../.doc/flows/infra-highlevel.png) (renderizado).

> O `.drawio` e o `.mmd` são **fontes paralelas**: o `.drawio` é a versão
> editável à mão, o `.mmd` é a que gera o PNG. Ao mudar a topologia, atualize os
> dois e regenere o PNG (ver `.arch/04-runbook.md`).

---

## 1. Por que uma VM única

A aplicação roda como ~22 containers numa única EC2, atrás de um proxy reverso,
em vez de ECS/EKS. A justificativa está em [`01-cloud-plan.md`](01-cloud-plan.md):
é uma demonstração técnica, e a stack inclui seis serviços com estado
(Postgres, Chroma, Redis, ClickHouse, MinIO, Postgres do Langfuse). Em Fargate,
cada um viraria um serviço gerenciado — o custo sairia de ~US$91 para
US$250–500/mês sem ganho didático.

O preço dessa escolha é explícito: **não há alta disponibilidade**. A VM é um
ponto único de falha, e um `docker compose down` derruba tudo.

## 2. Camada AWS

| Recurso | Valor | Observação |
|---|---|---|
| Conta / região | `120414880525` / `sa-east-1` | AZ `sa-east-1c` |
| EC2 | `i-0d89e9370f6cf6819`, t4g.large | ARM Graviton2, 2 vCPU / 8 GB |
| AMI | Ubuntu 24.04 LTS ARM64 | resolvida via SSM Parameter Store |
| Disco | 60 GB gp3, criptografado | + 4 GB de swap em `/swapfile` |
| Elastic IP | `56.126.112.30` | sobrevive a stop/start |
| Security Group | `sg-01c8b33e109842777` (`homeequity-sg`) | 22/tcp, 80/tcp, 443/tcp, 443/udp |
| Key pair | `homeequity-ops` | ver ressalva abaixo |
| Rede | VPC **default** | sem VPC dedicada, sem NAT |

> **Ressalva sobre o `KeyName` da instância.** `aws ec2 describe-instances` ainda
> mostra `KeyName: cashme-ops`, e isso está correto. O atributo é imutável depois
> do lançamento — mudá-lo recriaria a VM, e por isso ele está em
> `ignore_changes`. O que de fato controla o acesso é o `authorized_keys` no
> disco, que contém as duas chaves. A key pair `homeequity-ops` existe na AWS
> para futuras instâncias.

Hardening aplicado: IMDSv2 obrigatório, volume raiz criptografado,
`lifecycle.ignore_changes` no `ami` para a instância não ser recriada quando a
Canonical publica uma imagem nova.

Pontos fracos conhecidos: SSH aberto para `0.0.0.0/0` (restrinja
`allowed_ssh_cidrs` para o seu IP em uso real), state do Terraform local e sem
lock, e nenhuma IAM role anexada à instância.

## 3. Borda: DNS e TLS

```
Cloudflare (zona digitalcodigos.com.br)
  A  homeequity     → 56.126.112.30   proxy DESLIGADO
  A  *.homeequity   → 56.126.112.30   proxy DESLIGADO
                          │
                          ▼
                    Caddy 2 (:80, :443 tcp+udp)
```

O proxy laranja da Cloudflare fica **desligado** de propósito: ele terminaria o
TLS antes do Caddy e atrapalharia os WebSockets do fluxo do analista.

O Caddy usa uma imagem própria (`Dockerfile.caddy`, via `xcaddy`) com o plugin
`caddy-dns/cloudflare`, e emite os certificados Let's Encrypt por **DNS-01**.
Como o `Caddyfile` declara os 10 hostnames nominalmente (não há site wildcard),
são **10 certificados independentes**. Eles persistem em
`/srv/homeequity/volumes/caddy/data` — apagar esse diretório força reemissão e
consome cota do Let's Encrypt.

### Os 10 vhosts

| Hostname | Destino | Basic-Auth |
|---|---|---|
| `homeequity.…` | `app:8000` | só em `/` e `/ui/*` |
| `grafana.…` | `grafana:3000` | sim |
| `langfuse.…` | `langfuse:3000` | sim |
| `prometheus.…` | `prometheus:9090` | sim |
| `phoenix.…` | `phoenix:6006` | sim |
| `mlflow.…` | `mlflow:5000` | sim |
| `chroma.…` | `chromadb:8000` | sim |
| `redisinsight.…` | `redisinsight:5540` | sim |
| `chroma-admin.…` | `chroma-admin:3001` | sim |
| `pgadmin.…` | `pgadmin:80` | sim |

No vhost principal, `/api/*`, `/ws/*`, `/metrics`, `/docs`, `/openapi.json` e
`/redoc` ficam livres de Basic-Auth — a autenticação ali é o JWT da aplicação.

## 4. Aplicação

Um único container serve API e front: o `Dockerfile` é multi-stage, com um
estágio `node:20-alpine` que compila a SPA React/Vite e copia o `dist/` para a
imagem Python, onde o FastAPI o monta em `/ui`. **Não existe container de
frontend separado.**

A SPA chama a API por caminho relativo (`/api/v1`), então não depende do
domínio. O build arg `VITE_PANEL_BASE` só alimenta os links para os painéis nas
telas de admin — mas, por entrar na imagem em tempo de build, trocar o domínio
exige rebuild.

No boot (`lifespan` em `app/main.py`) a aplicação cria o schema do Postgres,
**treina o modelo de crédito se `credit_model.pkl` não existir** e indexa a
knowledge base no Chroma caso o diretório não esteja vazio.

> Detalhe que já causou RAG vazio: o bind mount `app-data:/app/data` **esconde**
> a `data/knowledge_base` que vem dentro da imagem. Por isso o role `project`
> tem uma task que semeia a KB no volume. Sem ela, o diretório sobe vazio, a
> indexação é pulada silenciosamente e a busca não retorna nada.

## 5. Dados

| Serviço | Papel | Volume |
|---|---|---|
| `homeequity-db` | Postgres 16 + pgvector — usuários, simulações, propostas | `volumes/postgres` |
| `homeequity-chromadb` | Chroma 0.6.3 — vetores do RAG | `volumes/chromadb` |
| `homeequity-redis` | cache, memória de conversa, fila do Langfuse | `volumes/redis` |

Tudo em **bind mounts** sob `/srv/homeequity/volumes/`, não em volumes nomeados.
Isso torna backup e inspeção triviais, e faz com que `docker system prune
--volumes` não apague dados de produção.

Cada diretório é criado pelo Ansible com o UID que a imagem correspondente
espera (Postgres 999, Grafana 472, Prometheus 65534, Loki/Tempo 10001,
Postgres do Langfuse 70, ClickHouse 101, pgAdmin 5050).

## 6. Observabilidade

Três camadas distintas, que costumam ser confundidas:

**Infraestrutura** (`profile=monitoring`) — a aplicação emite OTLP para o
OTel Collector, que distribui traces para o Tempo e métricas para o Prometheus;
o Promtail envia logs para o Loki; o Grafana lê os três. cAdvisor e
node-exporter alimentam o Prometheus com métricas de container e de host. São
7 jobs de scrape e 7 dashboards provisionados por arquivo — ou seja, o Grafana
volta configurado mesmo com o volume zerado.

Métricas de negócio expostas em `/metrics`: `homeequity_credit_score_total`,
`homeequity_agent_requests_total`, `homeequity_rag_queries_total`,
`homeequity_ingest_chunks_total`, `homeequity_model_prediction_seconds`.

**LLM** (`profile=langfuse`) — Langfuse 3, com Postgres próprio, ClickHouse para
analytics e MinIO para blobs. Sobe com inicialização headless
(`LANGFUSE_INIT_*`): org, projeto e usuário admin são criados no primeiro boot
já com as chaves de API do `.env.prod`, dispensando configuração manual na UI.

**Experimentos** (`profile=devtools`) — MLflow registra o treino do modelo de
crédito no experimento `homeequity-credit-scorer`.

> O Phoenix sobe e é publicado, mas **não há instrumentação OpenInference no
> código**. Ele funciona como painel provisionado, sem traces próprios.

## 7. Deploy

```
máquina local                          AWS
─────────────                          ───
terraform  ──── provisiona ──────────► EC2 + EIP + SG + key pair
ansible    ──── SSH ─────────────────► bootstrap → docker → project → deploy
.env.prod  ──── copy (0600) ─────────► /srv/homeequity/repo/.env
                                              ▲
GitHub (madsonar/home-equity, main) ──────────┘  git clone
```

O ponto importante: **o código vem do GitHub, não da máquina local**. O role
`project` faz `git clone` da branch `main` com `force: true`. Alterações locais
não commitadas não chegam à produção — o único arquivo que viaja da máquina
local é o `.env.prod`.

O build das imagens `app` e `caddy` acontece **na própria VM**, em ARM64.

## 8. Limites conhecidos

| Limite | Detalhe |
|---|---|
| **RAM** | A soma dos limites declarados nos serviços ativos passa de 14 GB, contra 8 GB físicos. Limites são teto, não reserva, e o uso real fica em 6–7 GB — mas é apertado. O swap de 4 GB absorve picos. ClickHouse é o maior candidato a OOM. |
| **Sem HA** | Instância única. Um reboot derruba o serviço por alguns minutos. |
| **State local** | `terraform.tfstate` em disco, sem backend remoto nem lock. |
| **Portas no host** | `otel-collector`, `cadvisor` e `node-exporter` publicam portas no host sem override de produção. O Security Group não as expõe, mas falta defesa em profundidade. |
| **cAdvisor sem métricas por container** | O Docker 29 usa o snapshotter `overlayfs`/containerd, que não tem a estrutura `image/*/layerdb` que o cAdvisor v0.49 procura. Ele registra `failed to identify the read-write layer ID` e deixa de emitir o label `name`, então o dashboard *Containers — cAdvisor* fica vazio. Métricas de host (node-exporter), Postgres, Redis e da aplicação não são afetadas. Testado: `--docker_only` e `--disable_metrics=disk,diskIO` não resolvem, e não há imagem ARM64 mais recente. Alternativa seria expor as métricas nativas do daemon Docker (`metrics-addr` em `daemon.json`). |
