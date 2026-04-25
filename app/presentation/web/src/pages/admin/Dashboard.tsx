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
          {(() => {
            const base = (import.meta.env.VITE_PANEL_BASE as string | undefined)?.trim();
            // Em prod (com domínio): https://<sub>.<base>; em dev: http://localhost:<port>
            const u = (sub: string, port: number, path = '') =>
              base ? `https://${sub}.${base}${path}` : `http://localhost:${port}${path}`;
            const grafana = (path = '') => u('grafana', 3001, path);
            return [
              ['Swagger / OpenAPI', '/docs', 'Documentação interativa da API'],
              ['Grafana — CashMe Overview', grafana('/d/cashme-overview/cashme-e28094-api-overview?orgId=1&refresh=30s'), 'Dashboard com requests, latência, scores e logs'],
              ['Grafana (home)', grafana(), 'admin / cashme123'],
              ['Prometheus UI', u('prometheus', 9090, '/graph'), 'Queries PromQL · cashme_credit_score_total'],
              ['Tempo (traces)', grafana('/explore?left=%7B%22datasource%22:%22tempo%22%7D'), 'Distributed tracing via Grafana Explore'],
              ['Loki (logs)', grafana('/explore?left=%7B%22datasource%22:%22loki%22%7D'), 'Logs estruturados de containers'],
              ['Langfuse (LLM traces)', u('langfuse', 3000), 'Prompts, tokens e custo de LLMs'],
              ['Phoenix (agent traces)', u('phoenix', 6006), 'OTel traces + UMAP de embeddings'],
              ['MLflow (experiments)', u('mlflow', 5500), 'Histórico de retreinos do scorer'],
              ['RedisInsight', u('redisinsight', 5540), 'Sessions Redis, embeddings cache'],
              ['Chroma Admin', u('chroma-admin', 3500), 'Coleções e documentos do vector DB'],
              ['Métricas Prometheus (raw)', '/metrics', '/metrics da app'],
            ] as const;
          })().map(([lbl, url, hint]) => (
            <a key={url} href={url} target="_blank" rel="noreferrer"
               className="block p-3 rounded-lg border border-slate-200 hover:border-brand-500 hover:bg-brand-50/30 transition">
              <div className="font-medium text-slate-800">{lbl}</div>
              <div className="text-xs text-slate-500 truncate">{hint}</div>
              <div className="text-[10px] text-slate-400 truncate mt-0.5">↗ {url}</div>
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
