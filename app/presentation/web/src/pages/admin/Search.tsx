import { useState } from 'react';
import { api, SearchResult } from '../../lib/api';

export default function SearchPage() {
  const [q, setQ] = useState('');
  const [k, setK] = useState(4);
  const [busy, setBusy] = useState(false);
  const [results, setResults] = useState<SearchResult[]>([]);
  const [err, setErr] = useState<string | null>(null);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!q) return;
    setBusy(true);
    setErr(null);
    try {
      setResults(await api.search(q, k));
    } catch (e2) {
      setErr(String(e2));
      setResults([]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-6 max-w-5xl">
      <form onSubmit={submit} className="card flex gap-3 items-end">
        <div className="flex-1">
          <label className="label">Pergunta / termo de busca</label>
          <input
            className="input"
            placeholder='ex: "qual o LTV máximo em home equity?"'
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />
        </div>
        <div className="w-24">
          <label className="label">Top-K</label>
          <input
            type="number"
            min={1}
            max={20}
            className="input"
            value={k}
            onChange={(e) => setK(Number(e.target.value) || 4)}
          />
        </div>
        <button type="submit" className="btn-primary h-10" disabled={busy}>
          {busy ? '…' : 'Buscar'}
        </button>
      </form>

      {err && <div className="card bg-rose-50 border-rose-200 text-rose-700 text-sm">{err}</div>}

      {results.length > 0 && (
        <div className="space-y-3">
          {results.map((r, i) => (
            <div key={i} className="card">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs text-slate-500">{r.source}</span>
                <span className="badge bg-brand-50 text-brand-700 border border-brand-100">
                  score {r.score.toFixed(3)}
                </span>
              </div>
              <p className="text-sm text-slate-700 whitespace-pre-wrap">{r.content}</p>
            </div>
          ))}
        </div>
      )}

      {!busy && results.length === 0 && !err && (
        <p className="text-sm text-slate-500">
          Execute uma busca para ver chunks recuperados do ChromaDB (com score de similaridade).
        </p>
      )}
    </div>
  );
}
