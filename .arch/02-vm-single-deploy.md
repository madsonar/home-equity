# Deploy CashMe em VM única na AWS — Plano executivo

## TL;DR
EC2 **t4g.large** (ARM 2 vCPU / 8 GB) em **sa-east-1**, com **Elastic IP** (endereço fixo), 30 GB **gp3**. Acesso SSH **só por chave dedicada** (`~/.ssh/cashme-ops-ed25519`). Security Group abre **22** (admin) e **80** (Caddy reverse-proxy com **Basic-Auth global**). Stack roda via **docker-compose.yml + docker-compose.prod.yml** (overlay com bind mounts em `/srv/cashme/volumes/*`). Provisionamento via **Terraform** (rede/VM) e **Ansible** (instala docker, clona repo, copia `.env.prod` local → VM, builda e sobe). Tudo orquestrado pelo **Makefile** (`make deploy-init`, `make deploy`). AWS CLI profile `cashme-ops`.

## Baseline de consumo (medido local 2026-04-24)

Profile **default** (app + db + redis + chromadb):

| Serviço | CPU% | Mem |
|---|---|---|
| cashme-agent (app) | 0.5% | 750 MiB |
| cashme-db | 0.0% | 30 MiB |
| cashme-chromadb | 0.1% | 117 MiB |
| cashme-redis | 0.5% | 10 MiB |
| **Total default** | **~1%** | **~907 MiB** |

Adicionando **monitoring + langfuse**:

| Serviço | Mem |
|---|---|
| otel-collector | 60 MiB |
| prometheus | 71 MiB |
| grafana | 122 MiB |
| tempo | 202 MiB |
| loki | 77 MiB |
| promtail | 44 MiB |
| langfuse | 208 MiB |
| langfuse-db | 23 MiB |
| **Subtotal extras** | **~807 MiB** |
| **Total default + monitoring + langfuse** | **~1.7 GiB** |

→ **t4g.large (8 GB)** comporta tudo com folga (~75% livre). Recomendação: subir só **default** em prod e ligar `monitoring`/`langfuse` sob demanda alterando `COMPOSE_PROFILES` em `.env.prod`.

## Decisões fixadas

| Item | Valor |
|---|---|
| Região | `sa-east-1` |
| AMI | Ubuntu 24.04 LTS ARM64 (canonical, via SSM) |
| Instância | `t4g.large` |
| Disco root | 30 GB gp3 |
| EIP | sim (endereço fixo) |
| Usuário SSH | `cashme` |
| Chave SSH | `~/.ssh/cashme-ops-ed25519` (gerada no `make ssh-keygen`) |
| Profile compose prod | `default` (`monitoring`/`langfuse` opt-in) |
| Volumes | bind mounts em `/srv/cashme/volumes/{postgres,chromadb,redis,app-data,caddy}` |
| Reverse-proxy | Caddy 2 (Basic-Auth global) |
| SSL | desativado (sem domínio) |
| AWS CLI profile | `cashme-ops` |

## Arquitetura

```
[Internet]
  │ :22 (SSH key-only)
  │ :80 (HTTP — Caddy Basic-Auth)
  ▼
EC2 t4g.large (sa-east-1a · Ubuntu 24.04 ARM)
  ├── /srv/cashme/repo/                      ← git clone do projeto
  ├── /srv/cashme/volumes/{...}              ← bind mounts persistentes
  ├── docker + docker compose v2
  ├── caddy (container) :80
  └── cashme stack (compose overlay prod)
[EIP estático]
```

## Rotas Caddy (porta 80, Basic-Auth para tudo)

| Path | Backend |
|---|---|
| `/` (default) | `app:8000` (UI + API + WS) |
| `/grafana/*` | `grafana:3000` (se ativo) |
| `/langfuse/*` | `langfuse:3000` (se ativo) |
| `/prometheus/*` | `prometheus:9090` (se ativo) |
| `/chroma/*` | `chromadb:8000` |

> Painéis off-default ficam em rota stub (502 amigável) até o profile correspondente ser ativado.

## Comandos (Makefile)

| Target | Função |
|---|---|
| `make ssh-keygen` | Gera `~/.ssh/cashme-ops-ed25519` (idempotente) |
| `make tf-init` / `tf-plan` / `tf-apply` / `tf-destroy` | Terraform |
| `make ansible-check` | `--check --diff` |
| `make ansible-apply` | Roda playbook completo |
| `make deploy-init` | TF apply + aguarda SSH + Ansible apply (first-time) |
| `make deploy` | Apenas redeploy: git pull + rebuild + restart no servidor |
| `make ssh` | SSH na VM via EIP |
| `make logs SERVICE=app` | tail dos logs remotos |
| `make status` | `docker compose ps` remoto |
| `make panel-pass` | imprime senha do Caddy (gerada e salva localmente) |

## Fluxo `deploy-init` (first time)

1. `make ssh-keygen`
2. Editar `infra/terraform/terraform.tfvars` (ou usar defaults).
3. Editar `.env.prod` com valores reais (cópia de `.env.prod.example`).
4. `make deploy-init` →
   - `terraform apply` → cria SG, EC2, EIP.
   - Espera 22/tcp aberto.
   - Gera `infra/ansible/inventory/hosts.ini` a partir do output TF.
   - `ansible-playbook playbook.yml` → bootstrap, docker, project, deploy.
5. Acessar `http://<EIP>/` → Basic-Auth (user `admin`, senha em `~/.cashme-ops/panel-password.txt`).

## Fluxo `deploy` (atualização rápida)

```
ansible-playbook --tags deploy playbook.yml
```
Faz `git pull` + `docker compose -f ... -f ... build app` + `up -d`. Volumes intactos.

## Persistência (sobreviver a restart/recreate)

- Postgres data: `/srv/cashme/volumes/postgres` (bind, owner UID 999).
- ChromaDB: `/srv/cashme/volumes/chromadb` (bind).
- Redis AOF: `/srv/cashme/volumes/redis` (bind).
- App data (knowledge base, faiss artifacts): `/srv/cashme/volumes/app-data` (bind).
- Caddy data + certs (futuro SSL): `/srv/cashme/volumes/caddy` (bind).

`docker compose down` e até `docker system prune -a` **não** apagam o que está em `/srv/cashme/volumes/*`.

## Custo estimado

| Item | US$/mês |
|---|---|
| EC2 t4g.large on-demand sa-east-1 | ~49,00 |
| EBS 30 GB gp3 | ~2,40 |
| EIP (associado) | 0,00 |
| Transferência out ≤10 GB | ~1,00 |
| **Total** | **~52,40** |

Pode reduzir 30% com Savings Plan 1y.

## Riscos & mitigações

| Risco | Mitigação |
|---|---|
| Imagem docker grande (1.4 GB) demora no build | `make deploy` reusa cache; primeira build longa, OK |
| OOM em 8 GB se ligar `devtools` | Profile `devtools` desabilitado por padrão |
| Perda da chave SSH | Backup da chave em local seguro fora do repo |
| EIP perdido em destroy | EIP fixa enquanto não rodar `tf-destroy` |
| Sem SSL (HTTP claro) | Aceitável para teste; trocar Caddy por bloco com `tls` quando houver domínio |
| Quem souber o EIP tenta força-bruta no `/` | Caddy Basic-Auth + fail2ban opcional (TODO próx. iteração) |
