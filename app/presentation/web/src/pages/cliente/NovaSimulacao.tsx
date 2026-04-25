import { useState } from 'react';
import { api, ScoreRequest, SimulationResponse } from '../../lib/api';

export default function NovaSimulacao() {
  const [form, setForm] = useState<ScoreRequest>({
    monthly_income: 12000,
    property_value: 850000,
    requested_amount: 280000,
    employment_years: 8,
    age: 40,
    has_other_debts: false,
    profession: 'Analista',
    loan_purpose: 'reforma',
  });
  const [res, setRes] = useState<SimulationResponse | null>(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  const upd = <K extends keyof ScoreRequest>(k: K, v: ScoreRequest[K]) =>
    setForm((f) => ({ ...f, [k]: v }));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true); setErr(null); setRes(null);
    try {
      const r = await api.submitSimulation(form);
      setRes(r);
    } catch (e: unknown) {
      setErr((e as Error).message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <h2 className="text-xl font-semibold mb-1">Nova simulação de crédito</h2>
        <p className="text-sm text-slate-500">
          Valores acima de R$ 100.000 entram em <strong>análise manual</strong> por um de nossos analistas.
        </p>
      </div>
      <form onSubmit={submit} className="card p-5 grid grid-cols-2 gap-4">
        <Field label="Renda mensal (R$)">
          <input type="number" className="input w-full" value={form.monthly_income}
            onChange={(e) => upd('monthly_income', +e.target.value)} required />
        </Field>
        <Field label="Valor do imóvel (R$)">
          <input type="number" className="input w-full" value={form.property_value}
            onChange={(e) => upd('property_value', +e.target.value)} required />
        </Field>
        <Field label="Valor solicitado (R$)">
          <input type="number" className="input w-full" value={form.requested_amount}
            onChange={(e) => upd('requested_amount', +e.target.value)} required />
        </Field>
        <Field label="Idade">
          <input type="number" className="input w-full" value={form.age ?? 0}
            onChange={(e) => upd('age', +e.target.value)} />
        </Field>
        <Field label="Anos de emprego">
          <input type="number" className="input w-full" value={form.employment_years ?? 0}
            onChange={(e) => upd('employment_years', +e.target.value)} />
        </Field>
        <Field label="Profissão">
          <input className="input w-full" value={form.profession ?? ''}
            onChange={(e) => upd('profession', e.target.value)} />
        </Field>
        <Field label="Finalidade">
          <input className="input w-full" value={form.loan_purpose ?? ''}
            onChange={(e) => upd('loan_purpose', e.target.value)} />
        </Field>
        <Field label="Possui outras dívidas?">
          <select className="input w-full" value={form.has_other_debts ? '1' : '0'}
            onChange={(e) => upd('has_other_debts', e.target.value === '1')}>
            <option value="0">Não</option>
            <option value="1">Sim</option>
          </select>
        </Field>
        <div className="col-span-2 flex gap-3">
          <button className="btn bg-brand-600 text-white hover:bg-brand-700" disabled={busy}>
            {busy ? 'Enviando...' : 'Simular'}
          </button>
          {err && <span className="text-red-600 text-sm self-center">{err}</span>}
        </div>
      </form>

      {res && (
        <div className="card p-5">
          {res.status === 'pending_analyst' ? (
            <>
              <h3 className="text-lg font-semibold text-amber-600 mb-2">⏳ Em análise por um especialista</h3>
              <p className="text-sm text-slate-600">{res.public_message}</p>
              <p className="text-xs text-slate-400 mt-2">Solicitação #{res.id} — status: {res.status}</p>
            </>
          ) : res.score_snapshot ? (
            <>
              <h3 className="text-lg font-semibold mb-2">
                {res.score_snapshot.approved ? '✅ Pré-aprovado' : '❌ Reprovado automaticamente'}
              </h3>
              <div className="grid grid-cols-3 gap-4 text-sm">
                <Info label="Score" value={(res.score_snapshot.score * 100).toFixed(0) + '%'} />
                <Info label="LTV" value={(res.score_snapshot.ltv * 100).toFixed(1) + '%'} />
                <Info label="Parcela" value={'R$ ' + res.score_snapshot.monthly_installment.toFixed(2)} />
              </div>
              <p className="text-sm text-slate-600 mt-3">{res.score_snapshot.explanation}</p>
            </>
          ) : null}
        </div>
      )}
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <label className="block text-sm text-slate-600 mb-1">{label}</label>
      {children}
    </div>
  );
}
function Info({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-slate-50 rounded-md p-3">
      <div className="text-xs text-slate-500">{label}</div>
      <div className="text-lg font-semibold">{value}</div>
    </div>
  );
}
