import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Login from './pages/Login';
import { AuthProvider, RequireRole, useAuth, defaultRoute } from './lib/auth';

// Admin
import AdminDashboard from './pages/admin/Dashboard';
import KnowledgeBase from './pages/admin/KnowledgeBase';
import AdminSearch from './pages/admin/Search';
import AdminModel from './pages/admin/Model';
import AdminUsuarios from './pages/admin/Usuarios';

// Cliente
import ClienteHome from './pages/cliente/Home';
import Chat from './pages/cliente/Chat';
import NovaSimulacao from './pages/cliente/NovaSimulacao';
import MinhasSimulacoes from './pages/cliente/MinhasSimulacoes';
import Notificacoes from './pages/cliente/Notificacoes';
import Documentos from './pages/cliente/Documentos';

// Analista
import Fila from './pages/analista/Fila';
import Analise from './pages/analista/Analise';

const adminNav = [
  { to: '/admin', label: 'Dashboard', icon: '📊' },
  { to: '/admin/kb', label: 'Knowledge base', icon: '📚' },
  { to: '/admin/search', label: 'Busca semântica', icon: '🔍' },
  { to: '/admin/model', label: 'Modelo ML', icon: '🎯' },
  { to: '/admin/usuarios', label: 'Usuários', icon: '👥' },
];
const clienteNav = [
  { to: '/cliente', label: 'Início', icon: '🏠' },
  { to: '/cliente/nova', label: 'Nova simulação', icon: '💰' },
  { to: '/cliente/simulacoes', label: 'Minhas simulações', icon: '📋' },
  { to: '/cliente/notificacoes', label: 'Notificações', icon: '🔔' },
  { to: '/cliente/chat', label: 'Chat IA', icon: '💬' },
  { to: '/cliente/documentos', label: 'Documentos', icon: '📎' },
];
const analistaNav = [
  { to: '/analista', label: 'Fila', icon: '📥' },
];

function IndexRedirect() {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (!user) return <Home />;
  return <Navigate to={defaultRoute(user.role)} replace />;
}

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<IndexRedirect />} />
        <Route path="/login" element={<Login />} />

        <Route element={<RequireRole roles={['admin']}><Layout title="Backoffice" items={adminNav} area="admin" /></RequireRole>}>
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/admin/kb" element={<KnowledgeBase />} />
          <Route path="/admin/search" element={<AdminSearch />} />
          <Route path="/admin/model" element={<AdminModel />} />
          <Route path="/admin/usuarios" element={<AdminUsuarios />} />
        </Route>

        <Route element={<RequireRole roles={['cliente']}><Layout title="Área do cliente" items={clienteNav} area="cliente" /></RequireRole>}>
          <Route path="/cliente" element={<ClienteHome />} />
          <Route path="/cliente/nova" element={<NovaSimulacao />} />
          <Route path="/cliente/simulacoes" element={<MinhasSimulacoes />} />
          <Route path="/cliente/notificacoes" element={<Notificacoes />} />
          <Route path="/cliente/chat" element={<Chat />} />
          <Route path="/cliente/documentos" element={<Documentos />} />
        </Route>

        <Route element={<RequireRole roles={['analista']}><Layout title="Área do analista" items={analistaNav} area="analista" /></RequireRole>}>
          <Route path="/analista" element={<Fila />} />
          <Route path="/analista/analise/:id" element={<Analise />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AuthProvider>
  );
}
