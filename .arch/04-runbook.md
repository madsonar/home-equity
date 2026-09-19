# Runbook — deploy e troubleshooting

Como subir, atualizar e diagnosticar a stack do HomeEquity.
Credenciais **não** estão aqui — elas ficam em `.docs/acesso.md` (fora do git).

---

## Pré-requisitos na máquina de operação

| Ferramenta | Versão testada |
|---|---|
| Terraform | 1.13.4 |
| ansible-core | 2.20.5 |
| AWS CLI | 2.35.21 |
| Docker | 29.5.0 (só para validar o compose localmente) |
| jq, curl, python3 | — |

Também é preciso:

- perfil AWS `homeequity-ops` em `~/.aws/credentials` (região `sa-east-1`);
- chave `~/.ssh/homeequity-ops-ed25519` (gere com `make ssh-keygen`);
- `.env.prod` preenchido na raiz do projeto (partindo de `.env.prod.example`);
- `bcrypt` instalado no ambiente do Ansible — o `Caddyfile.j2` usa o filtro
  `password_hash('bcrypt')` para gerar o hash do Basic-Auth.

---

## Subir do zero

```bash
make ssh-keygen                 # chave SSH dedicada
cd infra/terraform
terraform init -upgrade
terraform plan -out=tfplan      # LEIA o plano antes de aplicar
terraform apply tfplan
cd ../..
make ansible-inventory          # gera hosts.ini a partir dos outputs
make cf-create-records          # cria A e wildcard A no Cloudflare
make ansible-apply              # provisiona e sobe a stack
make panel-pass                 # mostra a senha do Basic-Auth
```

**Ordem importa.** O DNS precisa estar no ar **antes** do Caddy subir. Se o
Caddy tentar emitir certificado sem os registros, ele falha o desafio DNS-01 e
consome a cota do Let's Encrypt (5 falhas de validação por hora por hostname).

Confirme a propagação antes de seguir (`dig` não está disponível em toda
máquina):

```bash
python3 -c "import socket;print(socket.gethostbyname('homeequity.digitalcodigos.com.br'))"
curl -s -H 'accept: application/dns-json' \
  'https://cloudflare-dns.com/dns-query?name=grafana.homeequity.digitalcodigos.com.br&type=A' | jq -r '.Answer[].data'
```

## Atualizar a aplicação

```bash
git push origin main            # OBRIGATÓRIO: a VM clona do GitHub
make deploy                     # git pull + build + up -d + seed
```

O role `project` faz `git clone … force: true` na VM. **O que roda em produção é
o HEAD da `main` no GitHub**, não o seu working tree. A única exceção é o
`.env.prod`, copiado da máquina local.

## Ligar e desligar (economia)

```bash
make vm-stop     # ~US$91/mês → ~US$13/mês
make vm-start    # liga e faz polling do health check
make vm-status
```

A VM parada preserva disco, Elastic IP e certificados. Os containers têm
`restart: always` e voltam sozinhos no boot — espere ~2 minutos.

---

## Troubleshooting

### Diagnóstico em ordem

```bash
make vm-status                     # 1. a instância está running?
make remote-status                 # 2. os containers subiram?
make remote-logs SERVICE=app       # 3. o que a aplicação diz
make vm-disk                       # 4. tem espaço?
```

### Matriz de sintomas

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| `curl` dá timeout / código `000` | DNS não propagou, VM parada ou SG fechado | `make vm-status`; conferir resolução do nome; `aws ec2 describe-security-groups` |
| Certificado inválido ou TLS falha | ACME não concluiu o DNS-01 | `make remote-logs SERVICE=caddy` e procurar `certificate obtained` / `challenge`; testar o token com `make cf-verify` |
| `401` em `/ui` ou nos painéis | Basic-Auth do Caddy | `make panel-pass`; usuário é `admin` |
| `502` num painel | o profile correspondente não subiu | `make remote-status`; conferir `COMPOSE_PROFILES` no `.env.prod` |
| `503` ou app fora | container `app` caiu ou ainda inicializa | `make remote-logs SERVICE=app`; no primeiro boot ele treina o modelo e indexa a KB, o que leva alguns minutos |
| Container em `Restarting` | OOM | `docker inspect <container> --format '{{.State.OOMKilled}}'`; `free -h`; conferir se o swap está ativo |
| Grafana sem dados | scrape falhando | `https://prometheus.<domínio>/targets` — os 7 jobs devem estar `up` |
| Langfuse sem traces | chaves de API divergentes | conferir `LANGFUSE_PUBLIC_KEY`/`SECRET_KEY` no `.env.prod` contra o projeto na UI; lembre que trocar `LANGFUSE_SALT` invalida chaves existentes |
| Busca do RAG vazia | knowledge base não semeada | `ls /srv/homeequity/volumes/app-data/knowledge_base/` — se estiver vazio, rode `make deploy` (o role `project` semeia) |
| `port is already allocated` | stack antiga ainda de pé | `docker ps | grep -v homeequity`; derrubar com `docker compose down` no diretório antigo |
| Disco cheio | cache de build acumulado | `make vm-disk` → `make vm-clean` |
| Ansible não acha host | inventário desatualizado | `make ansible-inventory` |
| `make cf-verify` falha com token válido | falta o escopo `User:API Tokens:Read` | já contornado: o target lê a zona em vez de `/user/tokens/verify` |

### Perda de acesso SSH

A instância aceita **três** usuários: `homeequity` (principal), `cashme`
(legado) e `ubuntu` (padrão da AMI). Todos com a mesma `authorized_keys`
original. Se a chave nova falhar, tente:

```bash
ssh -i ~/.ssh/cashme-ops-ed25519 ubuntu@56.126.112.30
```

Último recurso: EC2 Serial Console pelo painel da AWS.

### Espaço em disco

O maior consumidor é o cache de build do Docker. Do mais seguro ao mais
agressivo:

```bash
make vm-clean        # prune de cache e imagens dangling — seguro
docker image prune -a    # remove imagens sem container — força re-download
make vm-clean-deep       # docker system prune -af --volumes — CUIDADO
```

`vm-clean-deep` não apaga dados de produção (são bind mounts em `/srv`, não
volumes nomeados), mas remove volumes nomeados órfãos. Prefira `make vm-clean`.

---

## Regenerar os diagramas

O `drawio` não precisa estar instalado. O PNG sai do arquivo Mermaid:

```bash
npx -y -p @mermaid-js/mermaid-cli mmdc \
  -i .doc/flows/infra-highlevel.mmd \
  -o .doc/flows/infra-highlevel.png -b white -w 2400
```

Alternativa sem instalar nada (falha em diagramas muito grandes):

```bash
curl -sS -X POST https://kroki.io/mermaid/png \
  --data-binary @.doc/flows/infra-highlevel.mmd -o .doc/flows/infra-highlevel.png
```

O `.drawio` é a fonte editável e é mantido em paralelo — atualize os dois.

---

## Mudanças perigosas no Terraform

`user_data` e `key_name` são **ForceNew** em `aws_instance`: qualquer mudança
neles recria a instância e **destrói o disco de 60 GB junto**. Como o
`user_data` interpola `project_name` e `ssh_user`, renomear o projeto dispara
exatamente isso.

Por esse motivo o recurso tem:

```hcl
lifecycle {
  ignore_changes = [ami, user_data, key_name, subnet_id]
}
```

Antes de qualquer `apply`, confirme que a instância não será recriada:

```bash
terraform show -json tfplan | jq -r '
  .resource_changes[] | select(.type=="aws_instance")
  | "\(.address): \(.change.actions|join("+")) replace_paths=\(.change.replace_paths//[])"'
```

O resultado precisa ser `update` com `replace_paths=[]`. Se aparecer
`must be replaced`, **pare** — a blindagem foi perdida.

`terraform destroy` está na lista de `deny` em `.claude/settings.json`,
justamente para não ser executado por engano.
