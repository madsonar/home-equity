import { useState } from 'react';
import { api, ScoreResponse } from '../../lib/api';

const brl = (v: number) => v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

const PROPOSALS_KEY = 'cashme.proposals';

export default function Simulador() {
  const [form, setForm] = useState({
    monthly_income: 15000,
    property_value: 800000,
    requested_amount: 300000,
    employment_years: 5,
    age: 38,
    has_other_debts: false,
    profession: '',
    loan_purpose: '',
  });
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<ScoreResponse | null>(null);
  const [err, setErr] = useState<string | null>(null);

  function upd<K extends keyof typeof form>(k: K, v: (typeof form)[K]) {
    setForm((f) => ({ ...f, [k]: v }));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    setErr(null);
    setResult(null);
    try {
      setResult(await api.score(form));
    } catch (e2) {
      setErr(String(e2));
    } finally {
      setBusy(false);
    }
  }

  function saveProposal() {
    if (!result) return;
    const list = JSON.parse(localStorage.getItem(PROPOSALS_KEY) || '[]');
    list.unshift({
      id: Date.now(),
      created_at: new Date().toISOString(),
      status: result.approved ? 'aprovada' : 'em_analise',
      request: form,
      result,
    });
    localStorage.setItem(PROPOSALS_KEY, JSON.stringify(list.slice(0, 20)));
    alert('✅ Proposta salva em "Minhas propostas".');
  }

  return (
    <div className="grid lg:grid-cols-2 gap-6 max-w-6xl">
      <form onSubmit={submit} className="card space-y-3">
        <h2 className="font-semibold">💰 Simular crédito</h2>
        <div className="grid grid-cols-2 gap-3">
          <Field label="Renda mensal (R$)" value={form.monthly_income} onChange={(v) => upd('monthly_income', v)} />
          <Field label="Valor do imóvel (R$)" value={form.property_value} onChange={(v) => upd('property_value', v)} />
          <Field label="Valor solicitado (R$)" value={form.requested_amount} onChange={(v) => upd('requested_amount', v)} />
          <Field label="Idade" value={form.age} onChange={(v) => upd('age', v)} />
          <Field label="Anos de emprego" value={form.employment_years} onChange={(v) => upd('employment_years', v)} step="0.5" />
          <div>
            <label className="label">Profissão</label>
            <input className="input" value={form.profession} onChange={(e) => upd('profession', e.target.value)} />
          </div>
          <div className="col-span-2">
            <label className="label">Finalidade do crédito</label>
            <input className="input" value={form.loan_purpose} placeholder="reforma, capital de giro…" onChange={(e) => upd('loan_purpose', e.target.value)} />
          </div>
          <label className="col-span-2 flex items-center gap-2 text-sm">
            <input type="checkbox" checked={form.has_other_debts} onChange={(e) => upd('has_other_debts', e.target.checked)} />
            Possuo outras dívidas ativas
          </label>
        </div>
        <button type="submit" className="btn-primary w-full" disabled={busy}>
          {busy ? 'Calculando…' : 'Calcular score'}
        </button>
      </form>

      <div className="space-y-3">
        {err && <div className="card bg-rose-50 border-rose-200 text-rose-700 text-sm">{err}</div>}
        {!result && !err && !busy && (
          <div className="card text-sm text-slate-500">
            Preencha os dados ao lado e clique em <strong>Calcular</strong> para ver o score, LTV e parcela estimada.
          </div>
        )}
        {result && (
          <>
            <div className="card">
              <div className="flex items-center justify-between mb-3">
                <div>
                  <div className="text-xs uppercase text-slate-500">Status</div>
                  <div className="text-xl font-bold">
                    {result.approved ? (
                      <span className="text-emerald-600">✅ Pré-aprovado</span>
                    ) : (
                      <span className="text-rose-600">❌ Não aprovado</span>
                    )}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-xs uppercase text-slate-500">Score</div>
                  <div className="text-3xl font-bold">{(result.score * 1000).toFixed(0)}</div>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <Stat label="LTV" value={`${(result.ltv * 100).toFixed(1)}%`} />
                <Stat label="Parcela estimada" value={brl(result.monthly_installment)} />
              </div>
            </div>
            <div className="card">
              <h3 className="font-semibold mb-2">📊 Fatores de risco</h3>
              {result.risk_factors.length === 0 ? (
                <p className="text-sm text-slate-500">Nenhum fator negativo identificado.</p>
              ) : (
                <ul className="list-disc list-inside text-sm text-slate-700 space-y-1">
                  {result.risk_factors.map((f, i) => <li key={i}>{f}</li>)}
                </ul>
              )}
            </div>
            <div className="card">
              <h3 className="font-semibold mb-2">💡 Explicação</h3>
              <p className="text-sm text-slate-700 whitespace-pre-wrap">{result.explanation}</p>
            </div>
            <button onClick={saveProposal} className="btn-primary w-full">
              💾 Salvar como proposta
            </button>
          </>
        )}
      </div>
    </div>
  );
}

function Field({
  label, value, onChange, step,
}: { label: string; value: number; onChange: (v: number) => void; step?: string }) {
  return (
    <div>
      <label className="label">{label}</label>
      <input
        type="number"
        className="input"
        value={value}
        step={step}
        onChange={(e) => onChange(Number(e.target.value) || 0)}
      />
    </div>
  );
}
function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-slate-50 rounded-lg p-3">
      <div className="text-xs uppercase text-slate-500">{label}</div>
      <div className="font-semibold text-slate-800">{value}</div>
    </div>
  );
}
