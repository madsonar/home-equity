#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# CashMe — smoke-test E2E
# Cria clientes fictícios realistas, ingere conteúdo público do site CashMe,
# faz upload de PDF regulatório e exercita todos os endpoints REST.
#
# Uso:
#   bash scripts/demo_e2e.sh             # tudo contra http://localhost:8000
#   API=http://localhost:8000 bash ...   # override
# ──────────────────────────────────────────────────────────────────────────────
set -u
API="${API:-http://localhost:8000}"
BASE="$API/api/v1"

c_reset="\033[0m"; c_g="\033[1;32m"; c_b="\033[1;34m"; c_y="\033[1;33m"; c_r="\033[1;31m"
ok()   { echo -e "${c_g}✓${c_reset} $*"; }
info() { echo -e "${c_b}▸${c_reset} $*"; }
warn() { echo -e "${c_y}!${c_reset} $*"; }
fail() { echo -e "${c_r}✗${c_reset} $*"; }
sep()  { echo -e "\n${c_b}══════════════════════════════════════════════════════════════${c_reset}\n"; }

hit() {
    local method="$1" path="$2" body="${3:-}"
    if [[ -n "$body" ]]; then
        curl -sS -X "$method" "$BASE$path" \
            -H 'Content-Type: application/json' -d "$body"
    else
        curl -sS -X "$method" "$BASE$path"
    fi
    echo
}

sep
info "1. Healthcheck ($API)"
hit GET /health

sep
info "2. Score de crédito — 3 clientes reais"

# ── Cliente A — perfil favorável ──
info "Cliente A · Ana Ferreira (Eng. civil, SP) — imóvel R$ 850k, renda R$ 14k, solicita R$ 280k"
hit POST /score '{
  "monthly_income": 14000,
  "property_value": 850000,
  "requested_amount": 280000,
  "age": 41,
  "employment_years": 12,
  "has_other_debts": false,
  "profession": "Engenheira civil",
  "loan_purpose": "reforma"
}'

# ── Cliente B — perfil limítrofe ──
info "Cliente B · Bruno Martins (Comerciante, RJ) — imóvel R$ 450k, renda R$ 6.5k, solicita R$ 320k"
hit POST /score '{
  "monthly_income": 6500,
  "property_value": 450000,
  "requested_amount": 320000,
  "age": 52,
  "employment_years": 8,
  "has_other_debts": true,
  "profession": "Comerciante",
  "loan_purpose": "capital de giro"
}'

# ── Cliente C — perfil de alto risco ──
info "Cliente C · Carla Souza (Autônoma, MG) — imóvel R$ 320k, renda R$ 4k, solicita R$ 240k, com restrição"
hit POST /score '{
  "monthly_income": 4000,
  "property_value": 320000,
  "requested_amount": 240000,
  "age": 58,
  "employment_years": 3,
  "has_other_debts": true,
  "profession": "Autônoma",
  "loan_purpose": "quitar dívidas"
}'

sep
info "3. Ingestão de conteúdo público do site CashMe"
for URL in \
    "https://www.cashme.com.br/home-equity" \
    "https://www.cashme.com.br/emprestimo-com-garantia-de-imovel" \
    "https://www.cashme.com.br/blog"
do
    info "  → ingestando: $URL"
    hit POST /ingest/url "{\"url\": \"$URL\"}"
    sleep 65  # rate-limit do Gemini embeddings free tier: 100 req/min
done

sep
info "4. Upload do PDF regulatório (BACEN)"
PDF="data/sample_docs/regulacao_home_equity_bacen.pdf"
if [[ ! -f "$PDF" ]]; then
    warn "PDF não encontrado; gerando..."
    if command -v python >/dev/null 2>&1; then
        python scripts/gen_regulation_pdf.py || \
            docker exec cashme-agent python scripts/gen_regulation_pdf.py
    else
        docker exec cashme-agent python scripts/gen_regulation_pdf.py
    fi
fi
info "  → upload: $PDF"
curl -sS -X POST "$BASE/ingest/doc" -F "file=@${PDF}"
echo

sep
info "5. Busca semântica na base"
for Q in \
    "qual o LTV máximo permitido pelo BACEN para Home Equity?" \
    "como funciona a alienação fiduciária?" \
    "quanto tempo leva para aprovar crédito com garantia de imóvel?"
do
    info "  → query: $Q"
    curl -sS -G "$BASE/search" --data-urlencode "q=$Q" --data-urlencode "k=3" | \
        python -m json.tool 2>/dev/null | head -40
    echo
done

sep
info "6. Chat com memória (sessão demo-e2e)"
SESS="demo-e2e-$(date +%s)"

for MSG in \
    "Olá, sou a Ana Ferreira. Quanto consigo de crédito com um imóvel de 850 mil?" \
    "Minha renda mensal é R$ 14.000. Qual o valor máximo que eu conseguiria?" \
    "E em quantas parcelas eu posso pagar, considerando a regulação do BACEN?"
do
    info "  → $MSG"
    curl -sS -X POST "$BASE/chat" \
        -H 'Content-Type: application/json' \
        -d "{\"session_id\": \"$SESS\", \"message\": \"$MSG\"}" | \
        python -m json.tool 2>/dev/null | head -30
    echo
done

sep
ok "E2E concluído. Dados persistidos em:"
echo "   • ChromaDB (volume 'chroma_data')"
echo "   • Redis    (volume 'redis_data', sessão: $SESS)"
echo "   • ./data/  (knowledge base + uploads + modelos)"
echo
echo "Veja traces em:"
echo "   • Grafana/Tempo:   http://localhost:3001"
echo "   • Langfuse:        http://localhost:3002"
echo "   • Phoenix:         http://localhost:6006"
