import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';

// Admin
import AdminDashboard from './pages/admin/Dashboard';
import KnowledgeBase from './pages/admin/KnowledgeBase';
import AdminSearch from './pages/admin/Search';
import AdminModel from './pages/admin/Model';

// Cliente
import ClienteHome from './pages/cliente/Home';
import Chat from './pages/cliente/Chat';
import Simulador from './pages/cliente/Simulador';
import Documentos from './pages/cliente/Documentos';
import Propostas from './pages/cliente/Propostas';

const adminNav = [
  { to: '/admin', label: 'Dashboard', icon: '📊' },
  { to: '/admin/kb', label: 'Knowledge base', icon: '📚' },
  { to: '/admin/search', label: 'Busca semântica', icon: '🔍' },
  { to: '/admin/model', label: 'Modelo ML', icon: '🎯' },
];
const clienteNav = [
  { to: '/cliente', label: 'Início', icon: '🏠' },
  { to: '/cliente/simulador', label: 'Simulador', icon: '💰' },
  { to: '/cliente/chat', label: 'Chat', icon: '💬' },
  { to: '/cliente/documentos', label: 'Documentos', icon: '📎' },
  { to: '/cliente/propostas', label: 'Minhas propostas', icon: '📋' },
];

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />

      <Route element={<Layout title="Backoffice" items={adminNav} area="admin" />}>
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/admin/kb" element={<KnowledgeBase />} />
        <Route path="/admin/search" element={<AdminSearch />} />
        <Route path="/admin/model" element={<AdminModel />} />
      </Route>

      <Route element={<Layout title="Área do cliente" items={clienteNav} area="cliente" />}>
        <Route path="/cliente" element={<ClienteHome />} />
        <Route path="/cliente/simulador" element={<Simulador />} />
        <Route path="/cliente/chat" element={<Chat />} />
        <Route path="/cliente/documentos" element={<Documentos />} />
        <Route path="/cliente/propostas" element={<Propostas />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
