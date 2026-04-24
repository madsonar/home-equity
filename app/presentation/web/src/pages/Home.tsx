import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-brand-900 via-brand-700 to-brand-500 text-white flex flex-col">
      <header className="px-8 py-5 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-md bg-white text-brand-700 flex items-center justify-center font-bold">C</div>
          <span className="font-bold">CashMe</span>
        </div>
        <nav className="text-sm flex gap-4">
          <a href="/docs" target="_blank" rel="noreferrer" className="opacity-80 hover:opacity-100">API</a>
          <Link to="/admin" className="opacity-80 hover:opacity-100">Admin</Link>
        </nav>
      </header>

      <section className="flex-1 px-8 py-16 max-w-5xl mx-auto w-full">
        <p className="text-brand-100/80 mb-2 text-sm uppercase tracking-wider">Credit Intelligence Agent</p>
        <h1 className="text-4xl sm:text-5xl font-extrabold leading-tight mb-6">
          Libere crédito usando seu imóvel<br />como garantia
        </h1>
        <p className="text-lg text-brand-100/90 max-w-2xl mb-10">
          Simule em segundos, converse com nosso agente 24/7, envie seus documentos
          e acompanhe sua proposta — tudo online.
        </p>
        <div className="flex flex-wrap gap-4">
          <Link to="/cliente" className="btn bg-white text-brand-700 hover:bg-brand-50 text-base px-6 py-3">
            🚀 Começar simulação
          </Link>
          <Link to="/cliente/chat" className="btn bg-white/10 border border-white/30 text-white hover:bg-white/20 text-base px-6 py-3">
            💬 Tirar dúvidas com o agente
          </Link>
        </div>

        <div className="mt-16 grid sm:grid-cols-3 gap-4">
          {[
            ['Taxas baixas', 'A partir de 0,99% a.m. usando seu imóvel como garantia.'],
            ['Prazos longos', 'Até 240 meses para pagar, sem complicação.'],
            ['Análise 100% digital', 'Modelo de ML + agente conversacional em tempo real.'],
          ].map(([t, d]) => (
            <div key={t} className="bg-white/10 border border-white/20 rounded-xl p-4 backdrop-blur">
              <div className="font-semibold">{t}</div>
              <div className="text-sm text-brand-100/80 mt-1">{d}</div>
            </div>
          ))}
        </div>
      </section>

      <footer className="px-8 py-5 text-xs text-brand-100/60 border-t border-white/10">
        POC técnica · Grupo Cyrela · {new Date().getFullYear()}
      </footer>
    </div>
  );
}
