import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth, defaultRoute } from '../lib/auth';

const DEMO = [
  { label: 'Admin',    email: 'admin@cashme.local',    pwd: 'admin123' },
  { label: 'Analista', email: 'analista1@cashme.local', pwd: 'analista123' },
  { label: 'Cliente',  email: 'cliente1@cashme.local',  pwd: 'cliente123' },
];

export default function Login() {
  const { login } = useAuth();
  const nav = useNavigate();
  const loc = useLocation() as { state?: { from?: { pathname?: string } } };
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [err, setErr] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    setBusy(true);
    try {
      const u = await login(email, password);
      const to = loc.state?.from?.pathname || defaultRoute(u.role);
      nav(to, { replace: true });
    } catch (e: unknown) {
      setErr((e as Error).message || 'Falha no login');
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-brand-900 via-brand-700 to-brand-500 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-md p-8">
        <div className="flex items-center gap-2 mb-6">
          <div className="w-10 h-10 rounded-md bg-brand-500 flex items-center justify-center text-white font-bold">C</div>
          <div>
            <div className="text-xl font-bold">CashMe</div>
            <div className="text-sm text-slate-500">Credit Intelligence Agent</div>
          </div>
        </div>
        <h1 className="text-2xl font-semibold mb-4">Entrar</h1>
        <form onSubmit={submit} className="space-y-4">
          <div>
            <label className="block text-sm text-slate-600 mb-1">E-mail</label>
            <input type="email" required className="input w-full" value={email}
              onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div>
            <label className="block text-sm text-slate-600 mb-1">Senha</label>
            <input type="password" required className="input w-full" value={password}
              onChange={(e) => setPassword(e.target.value)} />
          </div>
          {err && <div className="text-red-600 text-sm">{err}</div>}
          <button type="submit" disabled={busy} className="btn bg-brand-600 text-white w-full hover:bg-brand-700 disabled:opacity-50">
            {busy ? 'Entrando...' : 'Entrar'}
          </button>
        </form>
        <div className="mt-6 pt-4 border-t border-slate-200">
          <p className="text-xs text-slate-500 mb-2">Credenciais de demo (clique para preencher):</p>
          <div className="flex flex-wrap gap-2">
            {DEMO.map((d) => (
              <button key={d.email} type="button"
                onClick={() => { setEmail(d.email); setPassword(d.pwd); }}
                className="btn text-xs bg-slate-100 hover:bg-slate-200 text-slate-700">
                {d.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
