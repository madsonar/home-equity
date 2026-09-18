import { useEffect, useState } from 'react';
import { api } from '../../lib/api';

interface U { id: number; email: string; full_name: string; role: string; created_at: string; }

export default function Usuarios() {
  const [rows, setRows] = useState<U[]>([]);
  const [form, setForm] = useState({ email: '', password: '', full_name: '', role: 'cliente' });
  const [busy, setBusy] = useState(false);

  const load = () => api.listUsers().then(setRows);
  useEffect(() => { load(); }, []);

  const create = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    try {
      await api.createUser(form);
      setForm({ email: '', password: '', full_name: '', role: 'cliente' });
      load();
    } finally { setBusy(false); }
  };

  const del = async (id: number) => {
    if (!confirm('Remover usuário?')) return;
    await api.deleteUser(id);
    load();
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold">Usuários</h2>
        <p className="text-sm text-slate-500">Gerenciar clientes, analistas e administradores.</p>
      </div>

      <form onSubmit={create} className="card p-4 grid grid-cols-5 gap-3 text-sm">
        <input className="input" placeholder="Nome" required
          value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} />
        <input className="input" placeholder="E-mail" type="email" required
          value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
        <input className="input" placeholder="Senha" type="password" required
          value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
        <select className="input" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}>
          <option value="cliente">cliente</option>
          <option value="analista">analista</option>
          <option value="admin">admin</option>
        </select>
        <button className="btn bg-brand-600 text-white hover:bg-brand-700" disabled={busy}>+ Criar</button>
      </form>

      <div className="card overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 text-slate-600">
            <tr><th className="p-3 text-left">#</th><th className="p-3 text-left">Nome</th><th className="p-3 text-left">E-mail</th><th className="p-3 text-left">Papel</th><th className="p-3"></th></tr>
          </thead>
          <tbody className="divide-y">
            {rows.map((u) => (
              <tr key={u.id} className="hover:bg-slate-50">
                <td className="p-3">{u.id}</td>
                <td className="p-3">{u.full_name}</td>
                <td className="p-3">{u.email}</td>
                <td className="p-3"><span className="badge bg-slate-100">{u.role}</span></td>
                <td className="p-3 text-right">
                  <button onClick={() => del(u.id)} className="btn bg-red-50 text-red-700 hover:bg-red-100 text-xs">Remover</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
