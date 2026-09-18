import { useEffect, useState } from 'react';
import { api, SimulationResponse } from '../../lib/api';

const STATUS_LABEL: Record<string, string> = {
  auto_approved: '✅ Aprovada automaticamente',
  auto_rejected: '❌ Reprovada automaticamente',
  pending_analyst: '⏳ Em análise por analista',
  analyst_reviewing: '🔎 Analista revisando',
  approved: '✅ Aprovada pelo analista',
  rejected: '❌ Reprovada pelo analista',
};

export default function MinhasSimulacoes() {
  const [rows, setRows] = useState<SimulationResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.listMySimulations().then(setRows).finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="text-slate-500">Carregando...</p>;
  if (!rows.length) return <p className="text-slate-500">Nenhuma simulação registrada.</p>;

  return (
    <div className="space-y-3">
      <h2 className="text-xl font-semibold">Minhas simulações</h2>
      <div className="card divide-y">
        {rows.map((r) => (
          <div key={r.id} className="p-4 flex items-center justify-between">
            <div>
              <div className="font-medium">Solicitação #{r.id}</div>
              <div className="text-sm text-slate-500">
                R$ {r.amount_requested.toLocaleString('pt-BR')} ·{' '}
                {new Date(r.created_at).toLocaleString('pt-BR')}
              </div>
              {r.public_message && <div className="text-xs text-slate-500 mt-1">{r.public_message}</div>}
            </div>
            <span className="badge bg-slate-100 text-slate-700">{STATUS_LABEL[r.status] ?? r.status}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
