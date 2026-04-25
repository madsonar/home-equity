import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api, QueueItem } from '../../lib/api';

type Filter = 'pending_analyst' | 'mine' | 'all_open';

export default function Fila() {
  const [tab, setTab] = useState<Filter>('pending_analyst');
  const [rows, setRows] = useState<QueueItem[]>([]);
  const [loading, setLoading] = useState(true);
  const nav = useNavigate();

  const load = () => {
    setLoading(true);
    api.listQueue(tab).then(setRows).finally(() => setLoading(false));
  };
  useEffect(() => { load(); }, [tab]);

  const claim = async (reqId: number) => {
    const s = await api.claim(reqId);
    nav(`/analista/analise/${s.id}`);
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Fila de análise</h2>
        <button onClick={load} className="btn bg-slate-100 hover:bg-slate-200 text-sm">↻ Recarregar</button>
      </div>
      <div className="flex gap-2">
        {(['pending_analyst', 'mine', 'all_open'] as Filter[]).map((f) => (
          <button key={f} onClick={() => setTab(f)}
            className={`btn text-sm ${tab === f ? 'bg-brand-600 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'}`}>
            {f === 'pending_analyst' ? 'Pendentes' : f === 'mine' ? 'Minhas' : 'Todas abertas'}
          </button>
        ))}
      </div>
      <div className="card overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 text-slate-600">
            <tr>
              <th className="p-3 text-left">#</th>
              <th className="p-3 text-left">Cliente</th>
              <th className="p-3 text-right">Valor solicitado</th>
              <th className="p-3 text-right">Score</th>
              <th className="p-3 text-right">LTV</th>
              <th className="p-3 text-left">Criada em</th>
              <th className="p-3"></th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {loading && <tr><td colSpan={7} className="p-4 text-center text-slate-400">Carregando...</td></tr>}
            {!loading && rows.length === 0 && (
              <tr><td colSpan={7} className="p-4 text-center text-slate-400">Nenhuma solicitação.</td></tr>
            )}
            {rows.map((r) => (
              <tr key={r.id} className="hover:bg-slate-50">
                <td className="p-3">{r.id}</td>
                <td className="p-3">
                  <div className="font-medium">{r.client_name}</div>
                  <div className="text-xs text-slate-500">{r.client_email}</div>
                </td>
                <td className="p-3 text-right">R$ {r.amount_requested.toLocaleString('pt-BR')}</td>
                <td className="p-3 text-right">
                  {r.score_snapshot ? (r.score_snapshot.score * 100).toFixed(0) + '%' : '—'}
                </td>
                <td className="p-3 text-right">
                  {r.score_snapshot ? (r.score_snapshot.ltv * 100).toFixed(1) + '%' : '—'}
                </td>
                <td className="p-3">{new Date(r.created_at).toLocaleString('pt-BR')}</td>
                <td className="p-3 text-right">
                  <button onClick={() => claim(r.id)} className="btn bg-brand-600 text-white text-xs hover:bg-brand-700">
                    {r.status === 'pending_analyst' ? 'Analisar' : 'Abrir'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
