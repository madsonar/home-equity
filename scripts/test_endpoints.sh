#!/usr/bin/env bash
# Testa os endpoints REST. Requer servidor rodando.

BASE="${1:-http://127.0.0.1:8000/api/v1}"
PASS=0
FAIL=0

check() {
    local label="$1"
    local code="$2"
    local expected="${3:-200}"
    if [ "$code" = "$expected" ]; then
        echo "  ✓ $label"
        ((PASS++))
    else
        echo "  ✗ $label — HTTP $code (esperado $expected)"
        ((FAIL++))
    fi
}

echo "=== Testando $BASE ==="

CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/health")
check "GET  /health" "$CODE"

CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/search?q=LTV+home+equity&k=2")
check "GET  /search?q=LTV" "$CODE"

CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/score" \
  -H "Content-Type: application/json" \
  -d '{"monthly_income":20000,"property_value":800000,"requested_amount":250000,"employment_years":8,"age":42,"has_other_debts":false}')
check "POST /score (aprovado)" "$CODE"

CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/score" \
  -H "Content-Type: application/json" \
  -d '{"monthly_income":3500,"property_value":300000,"requested_amount":270000,"employment_years":0.3,"age":20,"has_other_debts":true}')
check "POST /score (reprovado)" "$CODE"

CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/ingest/doc" \
  -F "file=@data/sample_docs/exemplo_simulacao.txt")
check "POST /ingest/doc (.txt)" "$CODE"

CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/ingest/url" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}')
check "POST /ingest/url (503 sem crawl4ai)" "$CODE" "503"

echo ""
echo "Resultados: $PASS passaram, $FAIL falharam"
BASE_HOST=$(echo "$BASE" | grep -oP 'http://[^/]+')
echo "Documentação: ${BASE_HOST}/docs"
[ "$FAIL" -eq 0 ]
