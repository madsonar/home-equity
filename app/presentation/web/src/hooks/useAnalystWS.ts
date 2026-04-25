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
          setEvents((data as unknown as { messages: WSEvent[] }).messages);
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
