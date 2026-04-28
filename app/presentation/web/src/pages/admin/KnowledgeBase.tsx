import { useState } from 'react';
import { api } from '../../lib/api';

export default function KnowledgeBase() {
  const [url, setUrl] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [busy, setBusy] = useState<'url' | 'doc' | null>(null);
  const [results, setResults] = useState<{ tag: string; msg: string; ok: boolean }[]>([]);

  function log(tag: string, msg: string, ok: boolean) {
    setResults((r) => [{ tag, msg, ok }, ...r].slice(0, 10));
  }

  async function submitUrl(e: React.FormEvent) {
    e.preventDefault();
    if (!url) return;
    setBusy('url');
    try {
      const r = await api.ingestUrl({ url });
      log('URL', `${r.chunks_added} chunks · ${r.source}`, true);
      setUrl('');
    } catch (err) {
      log('URL', String(err), false);
    } finally {
      setBusy(null);
    }
  }

  async function submitDoc(e: React.FormEvent) {
    e.preventDefault();
    if (!file) return;
    setBusy('doc');
    try {
      const r = await api.ingestDoc(file);
      log('DOC', `${r.chunks_added} chunks · ${r.source}`, true);
      setFile(null);
      (e.target as HTMLFormElement).reset();
    } catch (err) {
      log('DOC', String(err), false);
    } finally {
      setBusy(null);
    }
  }

  return (
    <div className="space-y-6 max-w-4xl">
      <div className="grid md:grid-cols-2 gap-6">
        <form onSubmit={submitUrl} className="card space-y-3">
          <h2 className="font-semibold">🔗 Ingerir URL</h2>
          <p className="text-sm text-slate-500">
            Busca a página com Crawl4AI, divide em chunks e indexa no ChromaDB.
          </p>
          <div>
            <label className="label">URL</label>
            <input
              type="url"
              className="input"
              placeholder="https://www.equity.com.br/home-equity"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn-primary" disabled={busy === 'url'}>
            {busy === 'url' ? 'Processando…' : 'Ingerir'}
          </button>
        </form>

        <form onSubmit={submitDoc} className="card space-y-3">
          <h2 className="font-semibold">📄 Upload de documento</h2>
          <p className="text-sm text-slate-500">
            PDF, DOCX, MD, HTML ou TXT — parseado com Docling antes da indexação.
          </p>
          <div>
            <label className="label">Arquivo</label>
            <input
              type="file"
              accept=".pdf,.docx,.md,.html,.txt"
              className="input"
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
              required
            />
          </div>
          <button type="submit" className="btn-primary" disabled={busy === 'doc' || !file}>
            {busy === 'doc' ? 'Enviando…' : 'Enviar e indexar'}
          </button>
        </form>
      </div>

      <div className="card">
        <h2 className="font-semibold mb-3">Últimas ingestões (sessão)</h2>
        {results.length === 0 ? (
          <p className="text-sm text-slate-500">Nenhuma ingestão ainda.</p>
        ) : (
          <ul className="divide-y divide-slate-200 text-sm">
            {results.map((r, i) => (
              <li key={i} className="py-2 flex items-start gap-2">
                <span
                  className={`badge ${
                    r.ok ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'
                  }`}
                >
                  {r.tag}
                </span>
                <span className={`flex-1 ${r.ok ? 'text-slate-700' : 'text-rose-700'}`}>{r.msg}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
