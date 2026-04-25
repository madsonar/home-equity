import { useEffect, useState } from 'react';
import { api, ClientNotificationT } from '../../lib/api';

export default function Notificacoes() {
  const [rows, setRows] = useState<ClientNotificationT[]>([]);
  const [loading, setLoading] = useState(true);

  const load = () => api.listNotifications().then(setRows).finally(() => setLoading(false));
  useEffect(() => { load(); }, []);

  const mark = async (id: number) => {
    await api.markNotificationRead(id);
    load();
  };

  if (loading) return <p className="text-slate-500">Carregando...</p>;

  return (
    <div className="space-y-3 max-w-2xl">
      <h2 className="text-xl font-semibold">Notificações</h2>
      {rows.length === 0 && <p className="text-slate-500">Sem notificações.</p>}
      {rows.map((n) => (
        <div key={n.id} className={`card p-4 ${n.read ? 'opacity-60' : ''}`}>
          <div className="flex items-start justify-between gap-4">
            <div>
              <div className="font-medium">{n.title}</div>
              <div className="text-sm text-slate-600 mt-1">{n.body}</div>
              <div className="text-xs text-slate-400 mt-2">
                {new Date(n.created_at).toLocaleString('pt-BR')}
              </div>
            </div>
            {!n.read && (
              <button onClick={() => mark(n.id)} className="btn bg-slate-100 text-sm hover:bg-slate-200">
                Marcar lida
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
