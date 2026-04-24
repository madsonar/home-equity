import { Link } from 'react-router-dom';

export default function ClienteHome() {
  const links = [
    { to: '/cliente/simulador', icon: '💰', title: 'Simular crédito', desc: 'Veja quanto você pode liberar e a parcela mensal em segundos.' },
    { to: '/cliente/chat', icon: '💬', title: 'Tirar dúvidas', desc: 'Converse com nosso agente 24/7 sobre Home Equity.' },
    { to: '/cliente/documentos', icon: '📎', title: 'Enviar documentos', desc: 'RG, comprovante de renda, matrícula do imóvel.' },
    { to: '/cliente/propostas', icon: '📋', title: 'Minhas propostas', desc: 'Acompanhe o status das suas simulações aprovadas.' },
  ];
  return (
    <div className="space-y-6 max-w-4xl">
      <div className="card bg-gradient-to-br from-brand-500 to-brand-700 text-white border-transparent">
        <h2 className="text-xl font-bold">Olá! 👋</h2>
        <p className="text-brand-100/90 text-sm mt-1">
          Tudo o que você precisa para liberar crédito com garantia do seu imóvel, em um só lugar.
        </p>
      </div>

      <div className="grid sm:grid-cols-2 gap-4">
        {links.map((l) => (
          <Link
            key={l.to}
            to={l.to}
            className="card hover:border-brand-500 hover:shadow-md transition group"
          >
            <div className="text-2xl mb-2">{l.icon}</div>
            <div className="font-semibold group-hover:text-brand-600">{l.title}</div>
            <div className="text-sm text-slate-500 mt-1">{l.desc}</div>
          </Link>
        ))}
      </div>
    </div>
  );
}
