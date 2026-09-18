import { useState } from 'react';
import { api } from '../../lib/api';

const PANEL_BASE = (import.meta.env.VITE_PANEL_BASE as string | undefined)?.trim();
const MLFLOW_URL = PANEL_BASE ? `https://mlflow.${PANEL_BASE}` : 'http://localhost:5500';

export default function ModelPage() {
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<Record<string, unknown> | null>(null);
  const [err, setErr] = useState<string | null>(null);

  async function retrain() {
    if (!confirm('Retreinar o modelo de credit scoring? Isso substitui data/credit_model.pkl.')) return;
    setBusy(true);
    setErr(null);
    try {
      setResult(await api.retrain());
    } catch (e) {
      setErr(String(e));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-6 max-w-3xl">
      <div className="card">
        <h2 className="font-semibold">🎯 Modelo de credit scoring</h2>
        <p className="text-sm text-slate-500 mt-1">
          Pipeline scikit-learn com feature engineering (LTV, DTI, idade).<br />
          Ao retreinar, a API usa dados do Snowflake se configurado — caso contrário, dataset sintético.
        </p>
        <div className="mt-4">
          <button onClick={retrain} className="btn-primary" disabled={busy}>
            {busy ? 'Treinando…' : 'Retreinar agora'}
          </button>
          <a href={MLFLOW_URL} target="_blank" rel="noreferrer" className="btn-secondary ml-2">
            Abrir MLflow ↗
          </a>
        </div>
      </div>

      {err && <div className="card bg-rose-50 border-rose-200 text-rose-700 text-sm">{err}</div>}
      {result && (
        <div className="card">
          <h3 className="font-semibold mb-2">Resultado</h3>
          <pre className="text-xs bg-slate-50 p-3 rounded-lg overflow-x-auto">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}

      <div className="card">
        <h3 className="font-semibold mb-2">Observabilidade</h3>
        <ul className="text-sm text-slate-600 space-y-1 list-disc list-inside">
          <li>Latência de inferência: métrica Prometheus <code>cashme_model_prediction_seconds</code></li>
          <li>Contador de aprovados/reprovados: <code>cashme_credit_score_total{`{result=...}`}</code></li>
          <li>Dashboards Grafana → pasta <em>Equity</em></li>
        </ul>
      </div>
    </div>
  );
}
