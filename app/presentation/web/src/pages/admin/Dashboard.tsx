import { useEffect, useState } from 'react';
import { api } from '../../lib/api';

interface Metric {
  label: string;
  value: string;
  hint?: string;
}

export default function AdminDashboard() {
  const [metrics, setMetrics] = useState<Metric[]>([
    { label: 'API', value: '…' },
    { label: 'Chunks indexados', value: '—' },
    { label: 'Score médio (hoje)', value: '—' },
    { label: 'Sessões ativas', value: '—' },
  ]);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    api
      .health()
      .then((h) =>
        setMetrics((m) => [
          { ...m[0], value: h.status ?? 'ok', hint: 'FastAPI /api/v1/health' },
          ...m.slice(1),
        ]),
      )
      .catch((e) => setErr(String(e)));
  }, []);

  return (
    <div className="space-y-6">
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {metrics.map((m) => (
          <div key={m.label} className="card">
            <div className="text-xs uppercase tracking-wider text-slate-500">{m.label}</div>
            <div className="text-2xl font-bold mt-1">{m.value}</div>
            {m.hint && <div className="text-xs text-slate-400 mt-1">{m.hint}</div>}
          </div>
        ))}
      </div>

      <div className="card">
        <h2 className="text-lg font-semibold mb-3">Links rápidos</h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3 text-sm">
          {[
            ['Swagger / OpenAPI', '/docs'],
            ['Métricas Prometheus', '/metrics'],
            ['Grafana Dashboard', 'http://localhost:3001'],
            ['Prometheus UI', 'http://localhost:9090'],
            ['Langfuse (LLM traces)', 'http://localhost:3000'],
            ['Phoenix (agent traces)', 'http://localhost:6006'],
            ['MLflow (experiments)', 'http://localhost:5500'],
            ['RedisInsight', 'http://localhost:5540'],
            ['Chroma Admin', 'http://localhost:3500'],
          ].map(([lbl, url]) => (
            <a key={url} href={url} target="_blank" rel="noreferrer"
               className="block p-3 rounded-lg border border-slate-200 hover:border-brand-500 hover:bg-brand-50/30 transition">
              <div className="font-medium text-slate-800">{lbl}</div>
              <div className="text-xs text-slate-500 truncate">{url}</div>
            </a>
          ))}
        </div>
      </div>

      {err && (
        <div className="card bg-rose-50 border-rose-200 text-rose-700 text-sm">
          Erro ao consultar health: {err}
        </div>
      )}
    </div>
  );
}
