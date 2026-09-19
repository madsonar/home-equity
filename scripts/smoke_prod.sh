#!/usr/bin/env bash
# Smoke test da stack em produção.
#
#   bash scripts/smoke_prod.sh
#
# Lê o domínio e as credenciais do .env.prod. Não recebe segredo por argumento
# para não deixá-lo no histórico do shell.
set -uo pipefail

ENV_FILE="${ENV_FILE:-.env.prod}"
[ -f "$ENV_FILE" ] || { echo "ERRO: $ENV_FILE não encontrado"; exit 1; }
# shellcheck disable=SC1090
set -a; . "./$ENV_FILE"; set +a

B="${PANEL_DOMAIN_BASE:?PANEL_DOMAIN_BASE não definido}"
AUTH="${PANEL_BASIC_AUTH_USER:-admin}:${PANEL_BASIC_AUTH_PASS:?}"
ok=0; fail=0

chk() { # nome, codigo_esperado, url, [-u auth]
  local nome="$1" want="$2" url="$3"; shift 3
  local got
  got=$(curl -sS -o /dev/null -w '%{http_code}' --max-time 25 "$@" "$url" 2>/dev/null)
  if [ "$got" = "$want" ]; then
    printf '  \033[32m✓\033[0m %-34s %s\n' "$nome" "$got"; ok=$((ok+1))
  else
    printf '  \033[31m✗\033[0m %-34s %s (esperado %s)\n' "$nome" "$got" "$want"; fail=$((fail+1))
  fi
}

echo "── Endpoints públicos (sem Basic-Auth) ──────────────────────────"
chk "health"        200 "https://$B/api/v1/health"
chk "swagger"       200 "https://$B/docs"
chk "métricas"      200 "https://$B/metrics"

echo "── SPA (atrás do Basic-Auth) ────────────────────────────────────"
chk "/ui/login sem auth"  401 "https://$B/ui/login"
chk "/ui/login com auth"  200 "https://$B/ui/login" -u "$AUTH"

echo "── Painéis (Basic-Auth) ─────────────────────────────────────────"
# O Chroma 0.6.x não serve nada em "/" — o health fica em /api/v1/heartbeat.
for s in grafana langfuse prometheus phoenix mlflow chroma redisinsight chroma-admin pgadmin; do
  path="/"; [ "$s" = "chroma" ] && path="/api/v1/heartbeat"
  code=$(curl -sS -o /dev/null -w '%{http_code}' --max-time 25 -u "$AUTH" "https://$s.$B$path" 2>/dev/null)
  case "$code" in
    200|302|303|307|308) printf '  \033[32m✓\033[0m %-34s %s\n' "$s" "$code"; ok=$((ok+1)) ;;
    *)                   printf '  \033[31m✗\033[0m %-34s %s\n' "$s" "$code"; fail=$((fail+1)) ;;
  esac
done

echo "── TLS ──────────────────────────────────────────────────────────"
for h in "$B" "grafana.$B"; do
  if echo | openssl s_client -servername "$h" -connect "$h:443" 2>/dev/null \
       | openssl x509 -noout -checkend 0 >/dev/null 2>&1; then
    printf '  \033[32m✓\033[0m %-34s certificado válido\n' "$h"; ok=$((ok+1))
  else
    printf '  \033[31m✗\033[0m %-34s certificado inválido/ausente\n' "$h"; fail=$((fail+1))
  fi
done

echo "── Login da aplicação (JWT) ─────────────────────────────────────"
for u in "admin@homeequity.local:${SEED_ADMIN_PASSWORD:-}" \
         "analista1@homeequity.local:${SEED_ANALISTA_PASSWORD:-}" \
         "cliente1@homeequity.local:${SEED_CLIENTE_PASSWORD:-}"; do
  email="${u%%:*}"; pwd="${u#*:}"
  tok=$(curl -sS --max-time 25 -X POST "https://$B/api/v1/auth/login" \
        -d "username=$email" -d "password=$pwd" 2>/dev/null \
        | python3 -c 'import sys,json; print(json.load(sys.stdin).get("access_token",""))' 2>/dev/null)
  if [ -n "$tok" ]; then
    printf '  \033[32m✓\033[0m %-34s token obtido\n' "$email"; ok=$((ok+1))
  else
    printf '  \033[31m✗\033[0m %-34s falhou\n' "$email"; fail=$((fail+1))
  fi
done

echo
printf 'Resultado: \033[32m%d passaram\033[0m, \033[31m%d falharam\033[0m\n' "$ok" "$fail"
[ "$fail" -eq 0 ]
