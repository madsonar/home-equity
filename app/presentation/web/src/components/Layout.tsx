import { NavLink, Outlet, useLocation } from 'react-router-dom';

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
  area: 'admin' | 'cliente';
}) {
  const { pathname } = useLocation();
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
        <div className="pt-4 border-t border-brand-700/40 mt-4 space-y-1 text-xs text-brand-100/70">
          <a href="/docs" target="_blank" rel="noreferrer" className="block hover:text-white">↗ API Docs (Swagger)</a>
          <a href={area === 'admin' ? '/ui/cliente' : '/ui/admin'} className="block hover:text-white">
            ↗ Área {area === 'admin' ? 'Cliente' : 'Admin'}
          </a>
        </div>
      </aside>

      <main className="flex-1 flex flex-col">
        <header className="bg-white border-b border-slate-200 px-6 py-3 flex items-center justify-between">
          <h1 className="text-base font-semibold text-slate-800">
            {items.find((i) => pathname === i.to || pathname.startsWith(i.to + '/'))?.label ?? title}
          </h1>
          <span className="badge bg-emerald-50 text-emerald-700 border border-emerald-200">API conectada</span>
        </header>
        <div className="flex-1 p-6 overflow-auto">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
