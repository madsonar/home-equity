import { useEffect, useMemo, useRef, useState } from 'react';
import { useParams } from 'react-router-dom';
import { api, SessionDetail } from '../../lib/api';
import { useAnalystWS } from '../../hooks/useAnalystWS';
import AgentThinkingPanel from '../../components/AgentThinkingPanel';

export default function Analise() {
  const { id } = useParams<{ id: string }>();
  const sessId = Number(id);
  const [detail, setDetail] = useState<SessionDetail | null>(null);
  const [msg, setMsg] = useState('');
  const [rationale, setRationale] = useState('');
  const [uploading, setUploading] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  const { events, connected, send } = useAnalystWS(sessId);

  useEffect(() => { api.getSession(sessId).then(setDetail); }, [sessId]);
  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [events]);

  const awaitingDecision = useMemo(
    () => [...events].reverse().find((e) => e.type === 'awaiting_human_decision' || e.type === 'decision_applied')?.type === 'awaiting_human_decision',
    [events],
  );

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!msg.trim()) return;
    send({ type: 'user_message', content: msg });
    setMsg('');
  };

  const decide = (decision: 'approved' | 'rejected') => {
    send({ type: 'human_decision', decision, rationale });
    setRationale('');
  };

  const uploadFile = async (f: File) => {
    setUploading(true);
    try {
      await api.uploadAttachment(sessId, f);
      const d = await api.getSession(sessId);
      setDetail(d);
    } finally { setUploading(false); }
  };

  if (!detail) return <p className="text-slate-500">Carregando...</p>;

  const req = detail.request as Record<string, unknown>;
  const client = detail.client as Record<string, unknown>;
  const payload = (req.payload as Record<string, unknown>) || {};
  const score = (req.score_snapshot as Record<string, unknown>) || {};

  // Mensagens de chat visíveis (humanas + resposta final supervisor)
  const chat = events.filter((e) =>
    ['analyst_message', 'supervisor_answer', 'decision_applied'].includes(e.type as string)
  );

  return (
    <div className="grid grid-cols-12 gap-4 h-[calc(100vh-8rem)]">
      {/* Dossiê */}
      <aside className="col-span-3 card p-4 overflow-auto">
        <h3 className="text-sm font-semibold text-slate-600 uppercase tracking-wider mb-3">📋 Dossiê</h3>
        <div className="text-xs space-y-3">
          <div>
            <div className="text-slate-500">Cliente</div>
            <div className="font-medium">{client.full_name as string}</div>
            <div className="text-slate-500">{client.email as string}</div>
          </div>
          <Row label="Solicitação #" v={String(req.id)} />
          <Row label="Status" v={String(req.status)} />
          <Row label="Valor solicitado" v={`R$ ${Number(req.amount_requested).toLocaleString('pt-BR')}`} />
          <Row label="Renda mensal" v={`R$ ${Number(payload.monthly_income ?? 0).toLocaleString('pt-BR')}`} />
          <Row label="Imóvel" v={`R$ ${Number(payload.property_value ?? 0).toLocaleString('pt-BR')}`} />
          {score.score !== undefined && (
            <>
              <Row label="Score ML" v={`${(Number(score.score) * 100).toFixed(0)}%`} />
              <Row label="LTV" v={`${(Number(score.ltv) * 100).toFixed(1)}%`} />
              <Row label="Parcela" v={`R$ ${Number(score.monthly_installment).toFixed(2)}`} />
            </>
          )}
          <div>
            <div className="text-slate-500 mb-1">Anexos ({detail.attachments.length})</div>
            {detail.attachments.map((a) => (
              <div key={a.id} className="truncate">📎 {a.filename} <span className="text-slate-400">({a.chunks_indexed} chunks)</span></div>
            ))}
            <button onClick={() => fileRef.current?.click()}
              className="btn bg-slate-100 hover:bg-slate-200 text-xs mt-2 w-full">
              {uploading ? 'Enviando...' : '+ Anexar documento'}
            </button>
            <input ref={fileRef} type="file" className="hidden"
              onChange={(e) => { const f = e.target.files?.[0]; if (f) uploadFile(f); }} />
          </div>
        </div>
      </aside>

      {/* Chat */}
      <section className="col-span-6 card flex flex-col">
        <header className="px-4 py-3 border-b flex items-center justify-between">
          <div>
            <div className="font-semibold text-slate-800">Análise #{sessId}</div>
            <div className="text-xs text-slate-500">thread: {detail.session.thread_id}</div>
          </div>
          <span className={`badge ${connected ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-500'}`}>
            {connected ? '● conectado' : '○ offline'}
          </span>
        </header>
        <div className="flex-1 overflow-auto p-4 space-y-3">
          {chat.map((e, i) => {
            if (e.type === 'analyst_message') {
              return (
                <div key={i} className="flex justify-end">
                  <div className="max-w-[80%] bg-brand-600 text-white rounded-lg px-3 py-2 text-sm whitespace-pre-wrap">
                    {e.content as string}
                  </div>
                </div>
              );
            }
            if (e.type === 'supervisor_answer') {
              return (
                <div key={i} className="flex justify-start">
                  <div className="max-w-[80%] bg-slate-100 text-slate-800 rounded-lg px-3 py-2 text-sm whitespace-pre-wrap">
                    <div className="text-xs font-semibold text-brand-700 mb-1">🤖 Supervisor</div>
                    {e.content as string}
                  </div>
                </div>
              );
            }
            if (e.type === 'decision_applied') {
              return (
                <div key={i} className="text-center text-xs text-slate-500 py-2">
                  — decisão: <strong>{e.decision as string}</strong> —
                </div>
              );
            }
            return null;
          })}
          <div ref={bottomRef} />
        </div>
        <form onSubmit={submit} className="p-3 border-t flex gap-2">
          <input className="input flex-1" placeholder="Pergunte ao supervisor..."
            value={msg} onChange={(e) => setMsg(e.target.value)} />
          <button className="btn bg-brand-600 text-white hover:bg-brand-700">Enviar</button>
        </form>
        {awaitingDecision && (
          <div className="border-t bg-purple-50 p-3 space-y-2">
            <div className="text-sm font-semibold text-purple-800">⏸ Aguardando sua decisão</div>
            <textarea className="input w-full text-sm" rows={2} placeholder="Justificativa (opcional)..."
              value={rationale} onChange={(e) => setRationale(e.target.value)} />
            <div className="flex gap-2">
              <button onClick={() => decide('approved')} className="btn bg-emerald-600 text-white hover:bg-emerald-700 text-sm">✓ Aprovar</button>
              <button onClick={() => decide('rejected')} className="btn bg-red-600 text-white hover:bg-red-700 text-sm">✗ Reprovar</button>
            </div>
          </div>
        )}
      </section>

      {/* Agentes */}
      <aside className="col-span-3 card p-4 overflow-auto">
        <AgentThinkingPanel events={events} />
      </aside>
    </div>
  );
}

function Row({ label, v }: { label: string; v: string }) {
  return (
    <div className="flex justify-between gap-2">
      <span className="text-slate-500">{label}</span>
      <span className="font-medium text-right truncate">{v}</span>
    </div>
  );
}
