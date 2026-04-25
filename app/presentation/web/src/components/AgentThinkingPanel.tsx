import { WSEvent } from '../hooks/useAnalystWS';

const AGENT_LABELS: Record<string, string> = {
  supervisor: '🧭 Supervisor (planner)',
  rag: '📚 RAG (base + anexos)',
  regulation: '⚖️ Regulação BACEN',
  credit: '💳 Crédito / ML',
  viability: '🎯 Viabilidade',
  web: '🌐 Pesquisa Web',
  compose_answer: '🧠 Consolidação',
};

export default function AgentThinkingPanel({ events }: { events: WSEvent[] }) {
  // pega só eventos relacionados aos agentes
  const items = events.filter((e) =>
    ['agent_started', 'agent_result', 'supervisor_answer', 'awaiting_human_decision', 'decision_applied']
      .includes(e.type as string)
  );
  return (
    <div className="space-y-3">
      <h3 className="text-sm font-semibold text-slate-600 uppercase tracking-wider">
        🤖 Pensamento dos agentes
      </h3>
      {items.length === 0 && <p className="text-xs text-slate-400">Aguardando mensagem do analista...</p>}
      {items.map((e, i) => {
        const agent = (e.agent as string) || '';
        const label = AGENT_LABELS[agent] ?? agent;
        if (e.type === 'agent_started') {
          return (
            <div key={i} className="flex items-center gap-2 text-sm text-slate-600">
              <span className="inline-block w-2 h-2 bg-amber-400 rounded-full animate-pulse"></span>
              <span>{label} analisando...</span>
            </div>
          );
        }
        if (e.type === 'agent_result') {
          const summary = (e.summary as string) || '';
          const rawSources = (e.sources as unknown[]) || [];
          const sources = rawSources.map((s) => {
            if (typeof s === 'string') return s;
            if (s && typeof s === 'object') {
              const o = s as Record<string, unknown>;
              const title = typeof o.title === 'string' ? o.title : '';
              const source = typeof o.source === 'string' ? o.source
                : typeof o.url === 'string' ? o.url
                : typeof o.path === 'string' ? o.path : '';
              return [title, source].filter(Boolean).join(' — ') || JSON.stringify(o);
            }
            return String(s);
          });
          return (
            <div key={i} className="card p-3 border-l-4 border-emerald-500">
              <div className="text-xs font-semibold text-emerald-700 mb-1">{label}</div>
              <div className="text-xs text-slate-700 whitespace-pre-wrap line-clamp-6">{summary}</div>
              {sources.length > 0 && (
                <details className="mt-2">
                  <summary className="text-xs text-slate-500 cursor-pointer">{sources.length} fontes</summary>
                  <ul className="text-xs text-slate-500 mt-1 space-y-0.5">
                    {sources.slice(0, 8).map((s, j) => <li key={j} className="truncate">• {s}</li>)}
                  </ul>
                </details>
              )}
            </div>
          );
        }
        if (e.type === 'supervisor_answer') {
          return (
            <div key={i} className="card p-3 border-l-4 border-brand-500 bg-brand-50">
              <div className="text-xs font-semibold text-brand-700 mb-1">🧠 Resposta do supervisor</div>
              <div className="text-xs text-slate-800 whitespace-pre-wrap">{(e.content as string) || ''}</div>
            </div>
          );
        }
        if (e.type === 'awaiting_human_decision') {
          return (
            <div key={i} className="card p-3 border-l-4 border-purple-500 bg-purple-50">
              <div className="text-xs font-semibold text-purple-700">⏸ Aguardando decisão do analista</div>
            </div>
          );
        }
        if (e.type === 'decision_applied') {
          return (
            <div key={i} className="card p-3 border-l-4 border-slate-500">
              <div className="text-xs font-semibold text-slate-700">
                ✓ Decisão registrada: {e.decision as string}
              </div>
              {typeof e.rationale === 'string' && e.rationale && (
                <div className="text-xs text-slate-600 mt-1">{e.rationale}</div>
              )}
            </div>
          );
        }
        return null;
      })}
    </div>
  );
}
