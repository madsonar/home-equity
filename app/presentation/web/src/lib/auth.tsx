import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import {
  AuthUser, api, clearAuth, getStoredUser,
  setStoredUser, setToken,
} from './api';

interface AuthCtx {
  user: AuthUser | null;
  login: (email: string, password: string) => Promise<AuthUser>;
  logout: () => void;
  loading: boolean;
}

const Ctx = createContext<AuthCtx>({} as AuthCtx);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(getStoredUser());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      if (getStoredUser()) {
        try {
          const me = await api.me();
          setUser(me);
          setStoredUser(me);
        } catch {
          clearAuth();
          setUser(null);
        }
      }
      setLoading(false);
    })();
  }, []);

  const login = async (email: string, password: string) => {
    const r = await api.login(email, password);
    setToken(r.access_token);
    const u: AuthUser = {
      user_id: r.user_id, email: r.email, full_name: r.full_name, role: r.role,
    };
    setStoredUser(u);
    setUser(u);
    return u;
  };

  const logout = () => {
    clearAuth();
    setUser(null);
    location.href = '/ui/login';
  };

  return <Ctx.Provider value={{ user, login, logout, loading }}>{children}</Ctx.Provider>;
}

export function useAuth() { return useContext(Ctx); }

export function RequireRole({ roles, children }: { roles: Array<'cliente' | 'analista' | 'admin'>; children: ReactNode }) {
  const { user, loading } = useAuth();
  const loc = useLocation();
  if (loading) return <div className="p-8 text-slate-500">Carregando...</div>;
  if (!user) return <Navigate to="/login" state={{ from: loc }} replace />;
  const allowed = roles.includes(user.role) || user.role === 'admin';
  if (!allowed) return <Navigate to={defaultRoute(user.role)} replace />;
  return <>{children}</>;
}

export function defaultRoute(role: string): string {
  if (role === 'analista') return '/analista';
  if (role === 'admin') return '/admin';
  return '/cliente';
}
