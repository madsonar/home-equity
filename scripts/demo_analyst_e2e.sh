#!/usr/bin/env bash
# Demo E2E do fluxo de análise (cliente → fila → analista → agentes → decisão).
# Uso: ./scripts/demo_analyst_e2e.sh
set -euo pipefail
BASE="${BASE:-http://localhost:8000}"

say() { echo -e "\n\033[1;36m▸ $*\033[0m"; }

login() {
  local email="$1" pwd="$2"
  curl -sS -X POST "$BASE/api/v1/auth/login" \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode "username=$email" --data-urlencode "password=$pwd" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])"
}

say "1) Seed de usuários"
APP_CONTAINER=$(docker ps --format '{{.Names}}' | grep -E '_?cashme-agent$' | head -1)
docker exec "$APP_CONTAINER" python -m scripts.seed_users || true

say "2) Login cliente1"
CTOKEN=$(login cliente1@cashme.local cliente123)
echo "ok"

say "3) Cliente envia simulação de R$ 280.000 (> threshold)"
SIM=$(curl -sS -X POST "$BASE/api/v1/client/simulations" \
  -H "Authorization: Bearer $CTOKEN" -H 'Content-Type: application/json' \
  -d '{"monthly_income":14000,"property_value":850000,"requested_amount":280000,"age":41,"employment_years":12,"has_other_debts":false,"profession":"Engenheira","loan_purpose":"reforma"}')
echo "$SIM" | python3 -m json.tool
REQ_ID=$(echo "$SIM" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
STATUS=$(echo "$SIM" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
echo "→ request_id=$REQ_ID status=$STATUS"
[[ "$STATUS" == "pending_analyst" ]] || { echo "FAIL: esperava pending_analyst"; exit 1; }

say "4) Login analista1"
ATOKEN=$(login analista1@cashme.local analista123)
echo "ok"

say "5) Analista lista fila"
curl -sS "$BASE/api/v1/analyst/queue?status_filter=pending_analyst" \
  -H "Authorization: Bearer $ATOKEN" | python3 -m json.tool | head -40

say "6) Analista reivindica a solicitação"
SESS=$(curl -sS -X POST "$BASE/api/v1/analyst/queue/$REQ_ID/claim" \
  -H "Authorization: Bearer $ATOKEN")
echo "$SESS" | python3 -m json.tool
SESS_ID=$(echo "$SESS" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

say "7) Analista pergunta ao supervisor via WS e aprova"
python3 - <<PY
import asyncio, json, sys
import websockets

async def run():
    uri = f"ws://localhost:8000/ws/analyst/sessions/$SESS_ID?token=$ATOKEN"
    async with websockets.connect(uri) as ws:
        # recebe history
        hist = json.loads(await ws.recv())
        print(f"◉ history: {hist.get('type')} ({len(hist.get('messages',[]))} msgs)")
        # envia pergunta
        await ws.send(json.dumps({"type": "user_message",
          "message": "Esta solicitação atende aos limites de LTV do BACEN? Recomenda aprovar?"}))
        awaiting = False
        decisionApplied = False
        agents_seen = set()
        while True:
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=90)
            except asyncio.TimeoutError:
                print("⚠ timeout aguardando eventos"); break
            e = json.loads(raw)
            t = e.get("type")
            if t == "agent_started":
                agents_seen.add(e.get("agent"))
                print(f"  · agent_started: {e.get('agent')}")
            elif t == "agent_result":
                print(f"  ✓ agent_result: {e.get('agent')} — {(e.get('summary','') or '')[:80]}...")
            elif t == "supervisor_answer":
                print(f"\n🧠 SUPERVISOR: {e.get('content','')[:300]}\n")
            elif t == "awaiting_human_decision":
                print("⏸ aguardando decisão do analista → aprovando...")
                awaiting = True
                await ws.send(json.dumps({"type": "human_decision",
                  "decision": "approved", "rationale": "LTV 33%, renda compatível, sem restrições."}))
            elif t == "decision_applied":
                print(f"✓ decision_applied: {e.get('decision')}")
                decisionApplied = True
                break
            elif t == "error":
                print(f"✗ erro: {e.get('message')}"); break
        print(f"\nAgentes acionados: {sorted(agents_seen)}")
        assert awaiting, "FAIL: não entrou em awaiting_human_decision"
        assert decisionApplied, "FAIL: decisão não aplicada"

asyncio.run(run())
PY

say "8) Cliente vê notificação de aprovação"
curl -sS "$BASE/api/v1/client/notifications" \
  -H "Authorization: Bearer $CTOKEN" | python3 -m json.tool

say "9) Cliente consulta status da solicitação"
curl -sS "$BASE/api/v1/client/simulations/$REQ_ID" \
  -H "Authorization: Bearer $CTOKEN" | python3 -m json.tool

echo -e "\n\033[1;32m✓ Demo E2E concluída.\033[0m"
