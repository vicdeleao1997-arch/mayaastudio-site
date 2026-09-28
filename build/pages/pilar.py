"""Página-pilar `/trafego-pago-com-ia/` (C2 · §3.6). Texto final do SPEC, letra por letra.

Espinha da NUMIS: breadcrumb · H1 · parágrafo · link de projetos · seções · CTA (rótulos sem número).
A pilar é uma das duas páginas com a prova (check 8).
"""
from lib import components as c, config, media, seo
from lib.page import Page

PATH = "/trafego-pago-com-ia/"
TITLE = "Tráfego pago com IA: guia e perguntas · MAYAA STUDIO"
DESC = ("O que é tráfego pago com IA, como medir resultado em venda e não em curtida, e respostas às dúvidas mais "
        "comuns sobre Meta Ads e Google Ads.")
H1 = ["Tráfego pago", ("com IA.", "b")]
OG = "/assets/og/og-trafego-pago-com-ia.jpg"
TRILHA = [("Início", "/"), ("Tráfego pago com IA", None)]

FAQ = [
    ("Quanto preciso investir para começar?", [
        "Depende do valor do que você vende, da sua margem e de onde você anuncia hoje. Não existe um número bom para "
        "todo mundo.",
        "O nosso foco é quem já anuncia. O primeiro passo é um diagnóstico da conta que já roda: o que gasta, o que traz "
        "contato e o que vende. Só depois disso faz sentido falar em verba."]),
    ("A conta de anúncio fica no nome de quem?", [
        "No seu. A conta de anúncio, as campanhas e o histórico são da sua empresa.",
        "Entramos como parceiros no seu gerenciador de anúncios, com acesso próprio, sem pedir a sua senha. Você vê "
        "tudo o que é feito e pode tirar o acesso quando quiser."]),
    ("Como vocês medem resultado?", [
        "Com o relatório da plataforma lado a lado com o caixa. A plataforma mostra o que consegue enxergar; a venda "
        "que fecha no WhatsApp ou no balcão muitas vezes fica de fora.",
        "Por isso a leitura olha as duas linhas, campanha por campanha, e termina numa decisão: o que continua e o "
        "que sai."]),
    ("Vocês usam IA em quê?", [
        "No roteiro, nas variações de criativo, na produção de imagem e vídeo e na leitura das campanhas.",
        "A IA não decide sozinha: toda decisão de verba e de criativo passa por uma pessoa. Quando uma peça usa uma "
        "pessoa criada por IA, isso é dito."]),
    ("Vocês fazem Meta Ads e Google Ads?", [
        "Sim. Meta Ads (Instagram e Facebook) e Google Ads. A escolha do canal sai do diagnóstico: onde o seu cliente "
        "procura e onde a sua venda fecha."]),
    ("O que acontece se a gente parar?", [
        "O histórico fica com você. Como a conta de anúncio está no seu nome, campanhas, públicos e relatórios "
        "continuam lá.",
        "Para encerrar, basta remover o acesso da MAYAA no seu gerenciador."]),
]


def _o_que_e() -> str:
    texto = c.paras([
        "Tráfego pago é o dinheiro que você coloca na Meta (Instagram e Facebook) e no Google para levar a pessoa "
        "certa até a sua oferta. O anúncio é a parte que aparece. Por trás dele há estrutura de campanha, criativo, "
        "página, formulário e leitura de resultado.",
        "Com IA, a diferença não é um botão mágico. É produzir mais variações de criativo, testar com mais método e "
        "ler cada campanha com mais atenção. A IA é o ofício; a direção continua humana.",
        "A régua é a venda. Curtida, alcance e clique ajudam a entender o caminho, mas não pagam a conta. Por isso a "
        "leitura é campanha por campanha, com o relatório da plataforma ao lado do que entrou no caixa.",
    ])
    return c.section(
        c.label("O que é", cls="label--rule"),
        f'<div class="split srv-what">'
        f'<div class="srv-what__main">{c.title(["Verba certa,", ("régua certa.", "b")], size="h2")}</div>'
        f'<div class="stack srv-prose">{texto}</div></div>',
        id="o-que-e", cls="srv-sec")


def _como() -> str:
    return c.section(
        c.label("Como fazemos", cls="label--rule"),
        f'<div class="split srv-pil">'
        f'{c.head(None, lines=["Cinco pilares,", ("um time só.", "b")], cls="srv-head")}'
        f'<div class="srv-pil__text">{c.paras("Criativo, página e mídia não deveriam viver em agências separadas. Aqui, quem dirige o filme também monta o caminho até a venda e cuida da campanha.", cls="lead")}</div></div>'
        f'<div class="srv-pil__table">{c.pillars_table()}</div>',
        id="como-fazemos", cls="srv-sec")


def _para_quem() -> str:
    return c.section(
        c.head("Para quem é", lines=["Para quem", ("já anuncia.", "b")], cls="srv-head"),
        c.steps([
            "Já investe em Meta Ads ou Google Ads.",
            "Quer saber quais campanhas trazem venda, não só clique.",
            "Tem quem responda o contato que chega.",
            "Prefere uma decisão clara a um relatório bonito.",
        ], layout="grid", cols=2, cls="srv-steps srv-steps--only-t"),
        id="para-quem", tone="cartao", cls="srv-sec")


def pages():
    og = OG if media.exists(OG) else "/assets/og/og-mayaa.jpg"
    body = "".join([
        c.page_hero("Guia", H1,
                    "Anúncio medido em resultado de caixa, não em curtida. A IA entra no roteiro, no criativo e na "
                    "leitura da campanha. Quem decide é sempre uma pessoa.",
                    crumbs=TRILHA,
                    ctas=(c.btn("Manda CONTA no direct", config.IG_DM, external=True),
                          c.link_arrow("Conheça os projetos", "/portfolio/"))),
        _o_que_e(),
        _como(),
        _para_quem(),
        c.proof(tone="tinta", link=False),
        c.faq(FAQ, "Perguntas frequentes", ["Antes", ("de começar.", "b")], id="perguntas"),
        c.cta("CONTA", "Contato"),
    ])
    jsonld = [seo.webpage(PATH, TITLE, DESC, og), seo.breadcrumb_jsonld(TRILHA), seo.faq_jsonld(FAQ)]
    return [Page(path=PATH, title=TITLE, description=DESC, h1=c.plain(H1), body=body, og_image=og,
                 og_alt="MAYAA STUDIO · Tráfego pago com IA: o que é, como medimos e as perguntas mais comuns.",
                 jsonld=jsonld, nav="servicos", priority=0.9, changefreq="monthly", body_class="srv srv--pilar")]
