import { useEffect, useRef, useState } from 'react';
import { api } from '../../lib/api';

interface Msg {
  role: 'user' | 'assistant';
  content: string;
}

const SESSION_KEY = 'cashme.chat.session_id';
const HISTORY_KEY = 'cashme.chat.history';

export default function Chat() {
  const [messages, setMessages] = useState<Msg[]>(() => {
    try {
      return JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]');
    } catch {
      return [];
    }
  });
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const [sessionId] = useState(() => {
    let s = localStorage.getItem(SESSION_KEY);
    if (!s) {
      s = `web-${Math.random().toString(36).slice(2, 10)}`;
      localStorage.setItem(SESSION_KEY, s);
    }
    return s;
  });
  const endRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    localStorage.setItem(HISTORY_KEY, JSON.stringify(messages));
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  async function send(e: React.FormEvent) {
    e.preventDefault();
    const text = input.trim();
    if (!text || busy) return;
    setInput('');
    setMessages((m) => [...m, { role: 'user', content: text }]);
    setBusy(true);
    try {
      const r = await api.chat({ message: text, session_id: sessionId, agent: 'langchain' });
      setMessages((m) => [...m, { role: 'assistant', content: r.response }]);
    } catch (err) {
      setMessages((m) => [...m, { role: 'assistant', content: `⚠️ Erro: ${err}` }]);
    } finally {
      setBusy(false);
    }
  }

  function clear() {
    if (!confirm('Limpar conversa?')) return;
    setMessages([]);
    localStorage.removeItem(HISTORY_KEY);
  }

  return (
    <div className="flex flex-col h-[calc(100vh-10rem)] max-w-3xl">
      <div className="card flex-1 overflow-y-auto space-y-3 mb-3">
        {messages.length === 0 && (
          <div className="text-sm text-slate-500 p-4">
            👋 Olá! Posso te ajudar com dúvidas sobre Home Equity, documentos necessários, taxas e processo de aprovação.
            <div className="mt-3 flex flex-wrap gap-2">
              {['Como funciona o Home Equity?', 'Quais documentos preciso enviar?', 'Qual a taxa de juros?'].map((q) => (
                <button
                  key={q}
                  type="button"
                  onClick={() => setInput(q)}
                  className="text-xs px-3 py-1 rounded-full bg-brand-50 text-brand-700 hover:bg-brand-100"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-2 text-sm whitespace-pre-wrap ${
                m.role === 'user'
                  ? 'bg-brand-600 text-white rounded-br-sm'
                  : 'bg-slate-100 text-slate-800 rounded-bl-sm'
              }`}
            >
              {m.content}
            </div>
          </div>
        ))}
        {busy && (
          <div className="flex justify-start">
            <div className="bg-slate-100 rounded-2xl px-4 py-2 text-sm text-slate-500">digitando…</div>
          </div>
        )}
        <div ref={endRef} />
      </div>

      <form onSubmit={send} className="flex gap-2">
        <input
          className="input flex-1"
          placeholder="Pergunte algo sobre crédito com garantia de imóvel…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={busy}
        />
        <button type="submit" className="btn-primary" disabled={busy || !input.trim()}>
          Enviar
        </button>
        <button type="button" onClick={clear} className="btn-secondary" title="Limpar conversa">
          🗑
        </button>
      </form>
      <div className="text-xs text-slate-400 mt-2">Sessão: {sessionId}</div>
    </div>
  );
}
