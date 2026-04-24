"""
Gera um PDF com o conteúdo regulatório sobre crédito com garantia de imóvel
(Home Equity) — baseado em normas reais do BACEN (Resolução CMN 4.676/2018
e alterações).

Uso:
    python scripts/gen_regulation_pdf.py
        → gera data/sample_docs/regulacao_home_equity_bacen.pdf
"""
from pathlib import Path

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        PageBreak,
    )
    from reportlab.lib.enums import TA_JUSTIFY
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Faltou reportlab: pip install reportlab  (ou rode dentro do container cashme-agent)"
    ) from exc


OUT = Path("data/sample_docs/regulacao_home_equity_bacen.pdf")
OUT.parent.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()
body = ParagraphStyle(
    "body", parent=styles["BodyText"], alignment=TA_JUSTIFY, fontSize=10, leading=14
)
h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontSize=16, spaceAfter=12)
h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=13, spaceAfter=8)

doc = SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=2 * cm, rightMargin=2 * cm,
    topMargin=2 * cm, bottomMargin=2 * cm,
    title="Regulação — Crédito com Garantia de Imóvel",
    author="CashMe Credit Intelligence Agent",
)

story = []
P = lambda t, s=body: story.append(Paragraph(t, s))  # noqa: E731
SP = lambda h=0.4: story.append(Spacer(1, h * cm))   # noqa: E731

P("Regulação do Crédito com Garantia de Imóvel (Home Equity)", h1)
P(
    "<b>Documento técnico de referência para o agente de análise de crédito da "
    "CashMe.</b> Reúne as principais normas do Conselho Monetário Nacional "
    "(CMN) e do Banco Central do Brasil (BACEN) aplicáveis ao produto "
    "<i>Home Equity</i> (crédito com garantia de imóvel residencial ou comercial)."
)
SP()

# ─────────────────────────────────── Seção 1
P("1. Base normativa principal", h2)
P(
    "<b>Resolução CMN nº 4.676, de 31 de julho de 2018</b> — dispõe sobre as "
    "operações de crédito imobiliário, incluindo financiamento habitacional, "
    "empréstimo com garantia de imóvel residencial e crédito imobiliário a "
    "pessoa jurídica. É a norma central para o produto Home Equity praticado "
    "pela CashMe."
)
SP()
P(
    "<b>Resolução CMN nº 4.953, de 29 de setembro de 2021</b> — altera a "
    "4.676/2018 permitindo, entre outros pontos, o uso de imóveis comerciais "
    "como garantia de operações de empréstimo a pessoas físicas e jurídicas "
    "(art. 9º)."
)
SP()
P(
    "<b>Lei nº 9.514/1997</b> — institui a alienação fiduciária de bem imóvel, "
    "mecanismo de garantia utilizado nas operações de Home Equity. Em caso "
    "de inadimplência, permite a consolidação da propriedade em nome do credor "
    "após notificação e leilão público (arts. 26 e 27)."
)
SP()

# ─────────────────────────────────── Seção 2
P("2. Limites prudenciais aplicáveis", h2)
P(
    "<b>LTV (Loan to Value) — relação entre empréstimo e valor do imóvel:</b> "
    "a Resolução 4.676/2018, art. 9º, estabelece que o valor de avaliação do "
    "imóvel dado em garantia deve ser compatível com o saldo devedor, observado "
    "o limite de <b>até 60% do valor de avaliação</b> para empréstimos a "
    "pessoas físicas com garantia de imóvel residencial (Home Equity puro), "
    "podendo chegar a <b>80%</b> nos casos em que a operação se destina ao "
    "refinanciamento de dívidas imobiliárias ou aquisição de imóvel."
)
SP()
P(
    "<b>DTI (Debt-to-Income) — comprometimento de renda:</b> embora não haja "
    "um limite regulatório rígido, as boas práticas supervisórias do BACEN "
    "(Circular 3.978/2020 — prevenção à lavagem de dinheiro; e Resolução "
    "4.557/2017 — gerenciamento de risco) exigem política formal de crédito "
    "com limites internos. A CashMe adota, por política interna, "
    "comprometimento máximo de <b>30% da renda familiar líquida</b>."
)
SP()
P(
    "<b>Prazo máximo:</b> até 240 meses (20 anos) conforme prática de mercado "
    "e política da instituição; a Resolução 4.676/2018 não estabelece teto "
    "regulatório, mas exige avaliação da capacidade de pagamento ao longo de "
    "todo o período contratado."
)
SP()
P(
    "<b>Idade máxima ao final do contrato:</b> 80 anos (prática de mercado). "
    "Limite observado para compatibilização com a expectativa de sobrevida e "
    "contratação de seguro prestamista obrigatório."
)
SP()

# ─────────────────────────────────── Seção 3
PageBreak()
story.append(PageBreak())
P("3. Requisitos de análise de crédito", h2)
P(
    "A Resolução CMN 4.557/2017 (gerenciamento integrado de riscos) determina "
    "que toda instituição financeira deve manter estrutura de gestão do risco "
    "de crédito que contemple:"
)
P("• avaliação da capacidade de pagamento do tomador (renda comprovada);", body)
P("• análise da qualidade e liquidez da garantia (laudo de avaliação imobiliária);", body)
P("• verificação de restritivos (SPC/Serasa, ações judiciais, protestos);", body)
P("• análise de concentração de exposição por cliente e por região;", body)
P("• monitoramento contínuo da carteira e revisão periódica dos ratings.", body)
SP()
P(
    "<b>Documentação mínima exigida</b> (prática consolidada de mercado, "
    "alinhada à Circular 3.978/2020 — KYC/PLD):"
)
P("• RG, CPF e comprovante de residência atualizado;", body)
P("• comprovação de renda dos últimos 3 meses (holerite, extratos, IRPF);", body)
P("• matrícula atualizada do imóvel (com averbações dos últimos 20 anos);", body)
P("• IPTU e certidão negativa de débitos municipais;", body)
P("• laudo de avaliação por engenheiro/arquiteto credenciado;", body)
P("• certidão de ações cíveis e criminais do proprietário.", body)
SP()

# ─────────────────────────────────── Seção 4
P("4. Transparência e direitos do consumidor", h2)
P(
    "<b>Resolução BCB nº 4.881/2020</b> — determina que o Custo Efetivo Total "
    "(CET) seja informado de forma clara e previamente à contratação, "
    "incluindo todas as tarifas, seguros, tributos e demais despesas."
)
SP()
P(
    "<b>Resolução CMN nº 3.694/2009</b> — trata da prevenção de riscos na "
    "contratação de operações e da prestação de serviços, exigindo "
    "atendimento adequado ao cliente."
)
SP()
P(
    "<b>CDC — Lei 8.078/1990, art. 52:</b> no fornecimento de crédito, o "
    "consumidor deve ser previamente informado sobre preço em moeda corrente, "
    "taxa efetiva anual de juros, acréscimos legalmente previstos, número e "
    "periodicidade das prestações e soma total a pagar."
)
SP()
P(
    "<b>Direito à antecipação de pagamento (Resolução 4.320/2014, art. 10):</b> "
    "o cliente pode liquidar ou amortizar antecipadamente, total ou "
    "parcialmente, obtendo redução proporcional dos encargos financeiros."
)
SP()

# ─────────────────────────────────── Seção 5
P("5. Seguros obrigatórios", h2)
P(
    "Nas operações com garantia de imóvel é obrigatória, pela Lei 4.380/1964 "
    "e normas do SFH, a contratação de:"
)
P(
    "• <b>MIP</b> — Morte e Invalidez Permanente: cobre o saldo devedor em "
    "caso de morte ou invalidez permanente do tomador.", body
)
P(
    "• <b>DFI</b> — Danos Físicos ao Imóvel: cobre destruição parcial ou total "
    "do bem dado em garantia por sinistros previstos em apólice.", body
)
SP()

# ─────────────────────────────────── Seção 6
P("6. Modalidades permitidas pela CashMe", h2)
P(
    "<b>Home Equity Clássico:</b> empréstimo com livre uso dos recursos e "
    "garantia de imóvel residencial/comercial já quitado ou em fase final de "
    "quitação. Prazo 36 a 240 meses. Taxa a partir de 1,09% a.m. + IPCA."
)
SP()
P(
    "<b>Crédito com Garantia de Imóvel para PJ:</b> linha destinada a capital "
    "de giro ou expansão de empresas, com garantia de imóvel do sócio ou da "
    "empresa. Prazo até 180 meses. Taxa a partir de 1,19% a.m. + IPCA."
)
SP()
P(
    "<b>Portabilidade:</b> transferência de financiamento/Home Equity de outra "
    "instituição com redução de taxa, nos termos da Resolução CMN 4.292/2013 "
    "e Circular 3.977/2020."
)
SP()

# ─────────────────────────────────── Seção 7
P("7. Proibições e alertas", h2)
P(
    "• É <b>vedada</b> a cobrança de tarifa pela emissão de boleto de "
    "pagamento da parcela (Resolução CMN 3.919/2010, art. 1º).", body
)
P(
    "• É <b>vedado</b> o uso dos recursos para finalidades ilícitas; a "
    "instituição deve aplicar diligência reforçada em operações acima de "
    "R$ 30.000,00 à vista (Circular 3.978/2020).", body
)
P(
    "• A propriedade do imóvel é transferida fiduciariamente ao credor "
    "durante o contrato; em caso de inadimplência de 3 parcelas consecutivas, "
    "o credor pode iniciar a execução extrajudicial (Lei 9.514/1997).", body
)
SP()
P(
    "<i>Documento gerado automaticamente a partir do compilado normativo "
    "interno da CashMe Credit Intelligence Agent — v1.0, abril/2026.</i>", body
)

doc.build(story)
print(f"✓ PDF gerado: {OUT.resolve()}  ({OUT.stat().st_size / 1024:.1f} KB)")
