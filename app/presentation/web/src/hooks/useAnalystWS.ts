import { useEffect, useRef, useState } from 'react';
import { getToken, wsUrl } from '../lib/api';

export interface WSEvent { type: string; [k: string]: unknown; }

export function useAnalystWS(sessionId: number | null) {
  const [events, setEvents] = useState<WSEvent[]>([]);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!sessionId || !getToken()) return;
    const ws = new WebSocket(wsUrl(sessionId));
    wsRef.current = ws;
    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    ws.onerror = () => setConnected(false);
    ws.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data) as WSEvent;
        if (data.type === 'history' && Array.isArray((data as { messages?: unknown[] }).messages)) {
          const raw = (data as unknown as { messages: Array<Record<string, unknown>> }).messages;
          // Re-hidrata histórico em eventos com `type` consumível pela UI
          const hydrated: WSEvent[] = raw.map((m) => {
            const evtType = (m.event_type as string) || '';
            if (evtType === 'user_message') return { type: 'analyst_message', content: m.content as string };
            if (evtType === 'supervisor_answer') return {
              type: 'supervisor_answer', content: m.content as string,
              sources: (m.metadata as { sources?: unknown[] } | null)?.sources ?? [],
            };
            if (evtType === 'agent_result') return {
              type: 'agent_result', agent: m.agent_name as string, summary: m.content as string,
              sources: (m.metadata as { sources?: unknown[] } | null)?.sources ?? [],
            };
            if (evtType === 'decision_applied') {
              const meta = (m.metadata as { decision?: string; rationale?: string } | null) || {};
              return { type: 'decision_applied', decision: meta.decision || '', rationale: meta.rationale || '' };
            }
            // outros eventos (agent_started, error, awaiting_human_decision) – mantém type
            return { type: evtType || 'history_item', ...m };
          });
          setEvents(hydrated);
        } else {
          setEvents((prev) => [...prev, data]);
        }
      } catch { /* ignora frames não-JSON */ }
    };
    return () => { ws.close(); };
  }, [sessionId]);

  const send = (payload: Record<string, unknown>) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(payload));
    }
  };

  const appendLocal = (e: WSEvent) => setEvents((prev) => [...prev, e]);

  return { events, connected, send, appendLocal };
}
