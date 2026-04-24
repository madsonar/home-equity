import { useState } from 'react';

interface DocMeta {
  id: number;
  name: string;
  type: string;
  size: number;
  uploaded_at: string;
  tag: 'RG' | 'Renda' | 'Matrícula' | 'Outro';
}

const KEY = 'cashme.documents';

function load(): DocMeta[] {
  try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch { return []; }
}
function save(ds: DocMeta[]) {
  localStorage.setItem(KEY, JSON.stringify(ds));
}

export default function Documentos() {
  const [docs, setDocs] = useState<DocMeta[]>(load);
  const [tag, setTag] = useState<DocMeta['tag']>('RG');

  function onFile(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0];
    if (!f) return;
    // NOTA: POC — metadados ficam em localStorage; arquivo não é enviado.
    // Numa integração real, chamar POST /api/v1/documents/upload (a criar).
    const meta: DocMeta = {
      id: Date.now(),
      name: f.name,
      type: f.type || 'application/octet-stream',
      size: f.size,
      uploaded_at: new Date().toISOString(),
      tag,
    };
    const next = [meta, ...docs];
    setDocs(next);
    save(next);
    e.target.value = '';
  }

  function remove(id: number) {
    const next = docs.filter((d) => d.id !== id);
    setDocs(next);
    save(next);
  }

  const required: DocMeta['tag'][] = ['RG', 'Renda', 'Matrícula'];
  const have = new Set(docs.map((d) => d.tag));

  return (
    <div className="space-y-6 max-w-4xl">
      <div className="card">
        <h2 className="font-semibold">📎 Documentação necessária</h2>
        <p className="text-sm text-slate-500 mt-1">
          Envie RG, comprovante de renda recente e matrícula do imóvel. Formatos aceitos: PDF, JPG, PNG.
        </p>
        <div className="mt-4 flex flex-wrap gap-2">
          {required.map((t) => (
            <span
              key={t}
              className={`badge ${
                have.has(t) ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-600'
              }`}
            >
              {have.has(t) ? '✓' : '○'} {t}
            </span>
          ))}
        </div>
      </div>

      <div className="card">
        <div className="flex flex-wrap items-end gap-3">
          <div>
            <label className="label">Tipo do documento</label>
            <select className="input" value={tag} onChange={(e) => setTag(e.target.value as DocMeta['tag'])}>
              <option>RG</option>
              <option>Renda</option>
              <option>Matrícula</option>
              <option>Outro</option>
            </select>
          </div>
          <div className="flex-1 min-w-64">
            <label className="label">Arquivo</label>
            <input type="file" accept=".pdf,.png,.jpg,.jpeg" className="input" onChange={onFile} />
          </div>
        </div>
      </div>

      <div className="card">
        <h3 className="font-semibold mb-3">Enviados</h3>
        {docs.length === 0 ? (
          <p className="text-sm text-slate-500">Nenhum documento ainda.</p>
        ) : (
          <ul className="divide-y divide-slate-200 text-sm">
            {docs.map((d) => (
              <li key={d.id} className="py-2 flex items-center gap-3">
                <span className="badge bg-brand-50 text-brand-700 border border-brand-100 min-w-20 text-center">{d.tag}</span>
                <div className="flex-1 min-w-0">
                  <div className="font-medium truncate">{d.name}</div>
                  <div className="text-xs text-slate-500">
                    {(d.size / 1024).toFixed(1)} KB · {new Date(d.uploaded_at).toLocaleString('pt-BR')}
                  </div>
                </div>
                <button onClick={() => remove(d.id)} className="text-rose-600 hover:text-rose-700 text-xs">
                  remover
                </button>
              </li>
            ))}
          </ul>
        )}
        <p className="text-xs text-slate-400 mt-4">
          ℹ️ POC: os metadados ficam apenas no navegador. Num ambiente real o upload seria persistido em S3 + DB.
        </p>
      </div>
    </div>
  );
}
