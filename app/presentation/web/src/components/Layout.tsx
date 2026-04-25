import { NavLink, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../lib/auth';

interface NavItem {
  to: string;
  label: string;
  icon: string;
}

export default function Layout({
  title,
  items,
  area,
}: {
  title: string;
  items: NavItem[];
  area: 'admin' | 'cliente' | 'analista';
}) {
  const { pathname } = useLocation();
  const { user, logout } = useAuth();
  return (
    <div className="min-h-screen flex">
      <aside className="w-60 bg-brand-900 text-white flex-shrink-0 p-4 flex flex-col">
        <div className="mb-6">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-md bg-brand-500 flex items-center justify-center font-bold">C</div>
            <div>
              <div className="text-lg font-bold leading-tight">CashMe</div>
              <div className="text-xs text-brand-100/70">{title}</div>
            </div>
          </div>
        </div>
        <nav className="flex-1 space-y-1 text-sm">
          {items.map((it) => (
            <NavLink
              key={it.to}
              to={it.to}
              end
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2 rounded-md transition ${
                  isActive ? 'bg-brand-700 text-white' : 'text-brand-100/80 hover:bg-brand-700/40 hover:text-white'
                }`
              }
            >
              <span className="text-base">{it.icon}</span>
              {it.label}
            </NavLink>
          ))}
        </nav>
        <div className="pt-4 border-t border-brand-700/40 mt-4 space-y-2 text-xs text-brand-100/70">
          {user && (
            <div>
              <div className="text-white truncate">{user.full_name}</div>
              <div className="truncate">{user.email}</div>
              <div className="mt-1 opacity-70">papel: {user.role}</div>
            </div>
          )}
          <a href="/docs" target="_blank" rel="noreferrer" className="block hover:text-white">↗ API Docs (Swagger)</a>
          {user?.role === 'admin' && area !== 'admin' && <a href="/ui/admin" className="block hover:text-white">↗ Admin</a>}
          <button
            onClick={logout}
            className="block w-full text-left rounded-md bg-brand-700/40 hover:bg-brand-600 text-white px-3 py-2 mt-2"
            title="Sair e voltar para a tela de login"
          >
            🔄 Trocar de área / Login
          </button>
          <button onClick={logout} className="block w-full text-left hover:text-white">↪ Sair</button>
        </div>
      </aside>

      <main className="flex-1 flex flex-col">
        <header className="bg-white border-b border-slate-200 px-6 py-3 flex items-center justify-between">
          <h1 className="text-base font-semibold text-slate-800">
            {items.find((i) => pathname === i.to || pathname.startsWith(i.to + '/'))?.label ?? title}
          </h1>
          <div className="flex items-center gap-3">
            <button
              onClick={logout}
              className="text-xs text-slate-500 hover:text-brand-700 underline-offset-2 hover:underline"
              title="Voltar para a tela de login"
            >
              ← Trocar de área
            </button>
            <span className="badge bg-emerald-50 text-emerald-700 border border-emerald-200">API conectada</span>
          </div>
        </header>
        <div className="flex-1 p-6 overflow-auto">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
