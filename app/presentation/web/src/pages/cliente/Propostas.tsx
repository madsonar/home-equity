import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ScoreRequest, ScoreResponse } from '../../lib/api';

interface Proposal {
  id: number;
  created_at: string;
  status: 'aprovada' | 'em_analise' | 'reprovada';
  request: ScoreRequest;
  result: ScoreResponse;
}

const KEY = 'cashme.proposals';
const brl = (v: number) => v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

function load(): Proposal[] {
  try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch { return []; }
}

export default function Propostas() {
  const [items, setItems] = useState<Proposal[]>(load);

  function remove(id: number) {
    const next = items.filter((p) => p.id !== id);
    setItems(next);
    localStorage.setItem(KEY, JSON.stringify(next));
  }

  if (items.length === 0) {
    return (
      <div className="card max-w-2xl text-center py-12">
        <p className="text-slate-500 mb-4">Você ainda não salvou nenhuma proposta.</p>
        <Link to="/cliente/simulador" className="btn-primary">Fazer uma simulação</Link>
      </div>
    );
  }

  return (
    <div className="space-y-4 max-w-5xl">
      {items.map((p) => (
        <div key={p.id} className="card">
          <div className="flex items-center justify-between gap-4 flex-wrap">
            <div>
              <div className="text-xs text-slate-500">
                #{p.id} · {new Date(p.created_at).toLocaleString('pt-BR')}
              </div>
              <div className="font-semibold text-lg mt-1">
                {brl(p.request.requested_amount)} &nbsp;
                <span className="text-slate-400 text-sm font-normal">
                  imóvel {brl(p.request.property_value)}
                </span>
              </div>
            </div>
            <span
              className={`badge text-sm px-3 py-1 ${
                p.status === 'aprovada'
                  ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                  : p.status === 'reprovada'
                    ? 'bg-rose-50 text-rose-700 border border-rose-200'
                    : 'bg-amber-50 text-amber-700 border border-amber-200'
              }`}
            >
              {p.status === 'aprovada' ? '✅ Aprovada' : p.status === 'reprovada' ? '❌ Reprovada' : '⏳ Em análise'}
            </span>
          </div>
          <div className="grid sm:grid-cols-3 gap-3 mt-3 text-sm">
            <div className="bg-slate-50 rounded-lg p-2">
              <div className="text-xs text-slate-500">Score</div>
              <div className="font-semibold">{(p.result.score * 1000).toFixed(0)}</div>
            </div>
            <div className="bg-slate-50 rounded-lg p-2">
              <div className="text-xs text-slate-500">LTV</div>
              <div className="font-semibold">{(p.result.ltv * 100).toFixed(1)}%</div>
            </div>
            <div className="bg-slate-50 rounded-lg p-2">
              <div className="text-xs text-slate-500">Parcela</div>
              <div className="font-semibold">{brl(p.result.monthly_installment)}</div>
            </div>
          </div>
          {p.result.risk_factors.length > 0 && (
            <details className="mt-3 text-sm">
              <summary className="cursor-pointer text-slate-600 hover:text-slate-800">Fatores de risco</summary>
              <ul className="list-disc list-inside text-slate-700 mt-1 space-y-1">
                {p.result.risk_factors.map((f, i) => <li key={i}>{f}</li>)}
              </ul>
            </details>
          )}
          <div className="mt-3 flex gap-2">
            <button onClick={() => remove(p.id)} className="text-xs text-rose-600 hover:text-rose-700">remover</button>
          </div>
        </div>
      ))}
    </div>
  );
}
