"""Serviços (C2 · §3.2 a §3.5): índice `/servicos/` e uma página por serviço. Texto final do SPEC, letra por letra.

Classes próprias com prefixo `.srv-` (estilos em `styles/50-servicos.css`).
"""
from lib import components as c, config, dados, media, seo
from lib.page import Page

OG_PADRAO = "/assets/og/og-mayaa.jpg"
REEL = "/assets/portfolio/reel-surreal.mp4"
REEL_POSTER = "/assets/portfolio/reel-surreal-poster.jpg"
REEL_ALT = "Reel da BVBA Supply: o ouro escorre das molduras de um museu enquanto visitantes atravessam a galeria"


# ── utilidades locais ────────────────────────────────────────────────────────
def og(path: str) -> str:
    """og:image do SPEC (§5.2). Enquanto `tools/og.py` (C3) não gerou o arquivo, usa o og padrão do site."""
    return path if media.exists(path) else OG_PADRAO


def crumbs(*extra):
    return [("Início", "/"), *extra]


def intro(label_text: str, lines, text=None, id: str | None = None) -> str:
    """Rótulo com fio + título + texto (o cabeçalho de seção padrão, com a classe da página)."""
    return c.head(label_text, lines=lines, text=text, cls="srv-head", id=id)


def what_we_do(lines, text: str, items, extra: str = "", id: str = "o-que-fazemos") -> str:
    """01 · O que fazemos: título e texto à esquerda, entregáveis numerados à direita (.split)."""
    left = (f'<div class="srv-what__main">{c.title(lines, size="h2")}'
            f'<div class="stack srv-what__text">{c.paras(text)}</div></div>')
    return c.section(
        c.label("01 · O que fazemos", cls="label--rule"),
        f'<div class="split srv-what">{left}<div class="srv-what__list">{c.deliv_list(items)}</div></div>{extra}',
        id=id, cls="srv-sec")


def ctas(*html) -> str:
    return "".join(html)


def page(path, title, desc, h1, body, og_path, og_alt, jsonld, priority=0.9) -> Page:
    return Page(path=path, title=title, description=desc, h1=c.plain(h1), body=body, og_image=og(og_path),
                og_alt=og_alt, jsonld=jsonld, nav="servicos", priority=priority, changefreq="monthly",
                body_class="srv")


# ── /servicos/ ───────────────────────────────────────────────────────────────
def indice() -> Page:
    path = "/servicos/"
    title = "Serviços · tráfego pago, audiovisual e marketing · MAYAA STUDIO"
    desc = ("Três serviços, um estúdio: gestão de tráfego pago em Meta Ads e Google Ads, audiovisual com IA e "
            "marketing que sustenta o anúncio. Em São Paulo.")
    h1 = ["Três serviços,", ("um estúdio.", "b")]
    trilha = crumbs(("Serviços", None))
    body = "".join([
        c.page_hero("Serviços · 03", h1,
                    "Tráfego pago, audiovisual com IA e marketing. Cada serviço resolve uma parte do caminho entre o "
                    "anúncio e a venda. Juntos, respondem à mesma pergunta: quanto virou venda.",
                    kanji=("間", "ma · espaço"), crumbs=trilha,
                    ctas=(c.btn("Manda CONTA no direct", config.IG_DM, external=True),
                          c.mail_cta(config.MAILTO_DIAG, pre="Ou por e-mail"))),
        c.section(c.label("01 · Serviços", cls="label--rule"),
                  f'<div class="srv-rows" data-reveal="stagger">{"".join(c.service_row(s) for s in dados.SERVICES)}</div>',
                  id="lista", cls="srv-sec srv-sec--rows"),
        c.section(
            f'<div class="split srv-pil">'
            f'{intro("02 · Pilares", ["Cinco pilares,", ("um time só.", "b")])}'
            f'<div class="srv-pil__text">{c.paras("Criativo, página e mídia não deveriam viver em agências separadas. Aqui, quem dirige o filme também monta o caminho até a venda e cuida da campanha.", cls="lead")}</div></div>'
            f'<div class="srv-pil__table">{c.pillars_table()}</div>',
            id="pilares", cls="srv-sec"),
        c.section(c.label("03 · Guia", cls="label--rule"),
                  f'<div class="split srv-guide">{c.title(["O guia do", ("tráfego pago com IA.", "b")], size="h2")}'
                  f'<div class="srv-guide__body stack">'
                  f'{c.paras("O que é, como medimos resultado em venda e não em curtida, e as respostas às perguntas mais comuns sobre Meta Ads e Google Ads.", cls="lead")}'
                  f'<p data-reveal="fade">{c.btn("Ler o guia", "/trafego-pago-com-ia/", kind="ghost", sr=" de tráfego pago com IA")}</p>'
                  f'</div></div>',
                  id="guia", cls="srv-sec srv-sec--guide"),
        c.cta("CONTA", "Contato"),
    ])
    jsonld = [
        seo.webpage(path, title, desc, og("/assets/og/og-servicos.jpg")),
        seo.item_list([seo.service(s) for s in dados.SERVICES], name="Serviços da MAYAA STUDIO"),
        seo.breadcrumb_jsonld(trilha),
    ]
    return page(path, title, desc, h1, body, "/assets/og/og-servicos.jpg",
                "MAYAA STUDIO · Três serviços, um estúdio: tráfego pago, audiovisual com IA e marketing.", jsonld)


# ── /servicos/trafego-pago/ ──────────────────────────────────────────────────
FAQ_TRAFEGO = [
    ("Vocês atendem quem ainda não anuncia?", [
        "Nosso diagnóstico parte de uma conta que já roda, porque é nela que estão os dados para ler.",
        "Se você ainda não anuncia, escreva mesmo assim e conte o que vende. Dizemos com franqueza se faz sentido "
        "começar agora."]),
    ("Em quanto tempo aparece resultado?", [
        "Não prometemos prazo nem número. O primeiro entregável é o diagnóstico, com o que continua e o que sai.",
        "A partir daí, cada campanha é lida pelo que traz de venda, e a verba acompanha a leitura."]),
    ("Vocês fazem o criativo também?", [
        "Sim. Criativo, página e mídia ficam no mesmo estúdio, com o mesmo time.",
        ("Veja o serviço de audiovisual com IA.", "/servicos/audiovisual-com-ia/")]),
]


def trafego() -> Page:
    slug = "trafego-pago"
    path = dados.SERVICES[slug]["url"]
    title = "Gestão de tráfego pago · Meta Ads e Google Ads · MAYAA STUDIO"
    desc = ("Gestão de tráfego pago em Meta Ads e Google Ads para quem já anuncia. IA no criativo e na leitura, "
            "campanha lida uma por uma e a venda como régua.")
    h1 = ["Tráfego pago,", "lido campanha", ("por campanha.", "b")]
    trilha = crumbs(("Serviços", "/servicos/"), ("Tráfego pago", None))

    formatos = (
        '<div class="srv-formats">'
        f'{c.label("Criativo por formato", cls="srv-formats__label")}'
        '<div class="srv-formats__grid">'
        + c.figure("/assets/cases/iose-trafego-pago/feed-linhas.jpg",
                   "Anúncio quadrado do IOSE para o curso Projeto de Linhas de Transmissão, com o professor em frente "
                   "a uma torre", "Feed · 1:1", fx=False, sizes="(min-width:1024px) 36vw, 62vw", cls="srv-formats__feed")
        + c.figure("/assets/cases/iose-trafego-pago/stories-linhas.jpg",
                   "O mesmo anúncio do curso de linhas de transmissão adaptado para stories, na vertical",
                   "Stories · 9:16", fx=False, sizes="(min-width:1024px) 20vw, 35vw", cls="srv-formats__story")
        + '</div></div>')

    diagnostico = c.section(
        c.label("02 · O diagnóstico", cls="label--rule"),
        f'<div class="split srv-diag__top">{c.title(["Seis perguntas", ("antes de qualquer verba.", "b")], size="h2")}'
        f'<div class="srv-diag__text">{c.paras("O diagnóstico olha a conta como ela está hoje, sem mexer em nada. Ao final, você recebe as respostas:", cls="lead")}</div></div>',
        c.steps([
            "Para onde vai a verba, campanha por campanha?",
            "Quais criativos rodam, e há quanto tempo?",
            "O que acontece depois do clique: página, formulário ou WhatsApp?",
            "O que a plataforma enxerga, e o que ela não enxerga?",
            "Quais campanhas trazem contato, e quais trazem venda?",
            "O que continua, o que sai e o que testar primeiro?",
        ], layout="grid", cols=3, cls="srv-diag__steps"),
        '<div class="srv-ask" data-reveal="fade">'
        f'{c.label("Para pedir", cls="label--rule srv-ask__label")}'
        '<div class="srv-ask__body">'
        '<p class="srv-ask__text">Manda a palavra CONTA no direct do Instagram. Se preferir e-mail, escreva para '
        'contato@mayaastudio.com.br com o assunto Diagnóstico e conte onde anuncia hoje, o que vende e o que quer '
        'resolver.</p>'
        f'<div class="srv-ask__ctas">{c.btn("Manda CONTA no direct", config.IG_DM, external=True)}'
        f'{c.mail_cta(config.MAILTO_DIAG)}</div></div></div>',
        id="diagnostico", tone="cartao", cls="srv-sec srv-diag")

    regras = c.section(
        intro("03 · Regras da casa", ["A conta é sua.", ("A leitura é nossa.", "b")]),
        c.steps([
            ("A conta fica no seu nome.",
             "Campanhas, públicos e histórico são da sua empresa, antes, durante e depois."),
            ("Acesso de parceiro, sem senha.",
             "Entramos no seu gerenciador de anúncios com acesso próprio. Você vê tudo e tira o acesso quando quiser."),
            ("Quem decide é uma pessoa.", "A IA lê e sugere. Verba e criativo passam sempre por uma pessoa."),
            ("Meta Ads e Google Ads.",
             "O canal sai do diagnóstico: onde o seu cliente procura e onde a sua venda fecha."),
        ], layout="grid", cols=2, cls="srv-steps"),
        id="regras", cls="srv-sec")

    iose = "/assets/cases/iose-trafego-pago/"
    pratica = c.section(
        c.label("04 · Na prática", cls="label--rule"),
        '<div class="srv-practice">'
        f'<div class="srv-practice__card">'
        + c.case_card("iose-trafego-pago", size="lg", heading="h2", ratio=None, cover=iose + "feed-nbr.jpg",
                      cover_alt="Anúncio do IOSE para o curso da nova NBR 5419 com o professor em primeiro plano")
        + '</div><div class="srv-practice__fig">'
        + c.figure(iose + "feed-bess.jpg",
                   "Anúncio do IOSE para o curso de sistemas de armazenamento de energia, com contêineres de baterias "
                   "num campo", "Armazenamento de energia · Feed 1:1", fx=False, sizes="(min-width:1024px) 40vw, 100vw")
        + '</div>'
        f'<p class="srv-practice__more" data-reveal="fade">'
        f'{c.link_arrow("Guia completo: tráfego pago com IA", "/trafego-pago-com-ia/")}</p></div>',
        id="na-pratica", cls="srv-sec")

    body = "".join([
        c.page_hero("Serviço 002 · Tráfego pago e performance", h1,
                    "Gestão de Meta Ads e Google Ads para quem já anuncia. A IA entra no criativo e na leitura. "
                    "A régua é a venda, não a curtida.",
                    kanji=("展", "escalar"), crumbs=trilha,
                    ctas=(c.btn("Manda CONTA no direct", config.IG_DM, external=True),
                          c.mail_cta(config.MAILTO_DIAG, pre="Ou por e-mail"))),
        what_we_do(["Da conta que já roda", ("a uma decisão clara.", "b")],
                   "Começamos lendo o que existe: campanhas, criativos, página e o caminho até a venda. Depois "
                   "organizamos a conta para que cada campanha possa ser lida sozinha. Só então mexemos na verba.",
                   ["Diagnóstico da conta que já roda",
                    "Estrutura de campanha por oferta, com nomes padronizados",
                    "Criativo em vídeo e imagem para cada formato",
                    "Rastreamento do anúncio até o contato",
                    "Leitura campanha por campanha, não pelo total do mês",
                    "Relatório que termina em decisão: o que continua e o que sai"],
                   extra=formatos),
        diagnostico,
        regras,
        pratica,
        c.faq(FAQ_TRAFEGO, "05 · Perguntas", ["Antes", ("de pedir.", "b")]),
        c.cta("CONTA", "06 · Contato"),
    ])
    jsonld = [seo.service(slug, desc), seo.breadcrumb_jsonld(trilha), seo.faq_jsonld(FAQ_TRAFEGO)]
    return page(path, title, desc, h1, body, "/assets/og/og-servicos-trafego-pago.jpg",
                "MAYAA STUDIO · Tráfego pago, lido campanha por campanha. Meta Ads e Google Ads.", jsonld)


# ── /servicos/audiovisual-com-ia/ ────────────────────────────────────────────
FAQ_AUDIOVISUAL = [
    ("A IA substitui a produção com câmera?", [
        "Não. Muitas vezes a peça começa num ensaio real, como no case da BVBA: a roupa e o corpo são reais, o "
        "cenário foi construído depois.",
        "A IA amplia o que a câmera alcança. A direção continua humana."]),
    ("O produto fica igual ao real?", [
        "É a primeira regra. As fotos reais do produto entram como referência em cada imagem.",
        "Antes de sair, cada peça é conferida: proporção, rótulo, vidro, madeira, textura."]),
    ("Posso usar a modelo IA na minha marca?", [
        "Sim. A Ana Lauren é uma modelo criada do zero pela MAYAA, licenciável para anúncio e para UGC (conteúdo no "
        "estilo de cliente) da sua marca, sempre apresentada como IA.",
        "Manda a palavra MODELO no direct do Instagram."]),
]


def audiovisual() -> Page:
    slug = "audiovisual-com-ia"
    path = dados.SERVICES[slug]["url"]
    title = "Audiovisual com IA · filme, campanha e modelo · MAYAA STUDIO"
    desc = ("Filme, campanha de produto e modelo sintética com IA e direção humana. A peça real entra como "
            "referência e cada quadro é conferido antes de sair.")
    h1 = ["Audiovisual com IA,", ("com direção.", "b")]
    trilha = crumbs(("Serviços", "/servicos/"), ("Audiovisual com IA", None))

    reel = c.video(REEL, REEL_POSTER, REEL_ALT, caption="Filme · BVBA Supply · 9:16")
    trabalhos = c.section(
        intro("02 · Três trabalhos", ["O mesmo rigor,", ("três problemas diferentes.", "b")]),
        '<div class="split srv-reel">'
        f'<div class="srv-reel__vid">{reel}</div>'
        '<div class="srv-reel__text stack">'
        f'{c.paras("Ninguém acha estranho. Visitantes atravessam a galeria como numa terça-feira qualquer, e o museu derrete ao redor. Câmera travada, luz fixa: quem se move é o corpo e o ouro.", cls="lead")}'
        f'<p data-reveal="fade">{c.link_arrow("Ver o reel no Instagram", config.REEL_BVBA)}</p></div></div>'
        '<div class="cols-3 srv-cards">'
        + "".join(c.case_card(s, size="md", heading="h3")
                  for s in ("bvba-surrealismo", "alumee-vela-mel", "ana-lauren-modelo-ia"))
        + '</div>',
        id="trabalhos", cls="srv-sec")

    como = c.section(
        intro("03 · Como fazemos", ["Referência primeiro.", ("Conferência sempre.", "b")]),
        c.steps([
            ("01 · Imagem-mestre",
             "Antes de variar, fixamos uma imagem de referência: a sala, o produto, o rosto. Toda variação nasce "
             "dela, nunca do zero."),
            ("02 · O real como âncora",
             "As fotos do produto e da peça entram em cada geração, com medidas e detalhes. Rótulo errado é produto "
             "errado."),
            ("03 · Correção localizada", "Cada ajuste mexe só na área pedida. O resto fica congelado."),
            ("04 · Conferência peça por peça",
             "Proporção, rótulo, textura e luz conferidos antes de aprovar. Nada sai sem passar por uma pessoa."),
        ], layout="grid", cols=2, cls="srv-steps"),
        c.note("Quando uma peça usa uma pessoa criada por IA, isso é dito. Sempre.", cls="srv-note"),
        id="como-fazemos", tone="cartao", cls="srv-sec")

    body = "".join([
        c.page_hero("Serviço 003 · Audiovisual com IA", h1,
                    "Filme, campanha de produto e modelo sintética para anúncio e para marca. A peça real entra como "
                    "referência. O que a IA constrói passa por conferência, quadro a quadro.",
                    kanji=("創", "criar"), crumbs=trilha,
                    ctas=(c.mail_cta(config.MAILTO_PROJETO, kind="primary", pre="Iniciar projeto por e-mail",
                                     after=c.btn("Manda MODELO no direct", config.IG_DM, kind="ghost", external=True)),)),
        what_we_do(["Imagem feita para anúncio", ("e para marca.", "b")],
                   "Trabalhamos a partir do que é real: o produto, a roupa, o corpo, a marca. A IA constrói o cenário, "
                   "a luz e o movimento que a câmera sozinha não alcança. A direção decide o que fica.",
                   ["Fashion film e filme de marca",
                    "Campanha de produto a partir das fotos reais",
                    "Cenário construído com IA, com continuidade entre planos",
                    "Modelo sintética licenciável, sempre apresentada como IA",
                    "Fotos para feed, stories e anúncio",
                    "Reels e cortes para cada formato"]),
        trabalhos,
        como,
        c.faq(FAQ_AUDIOVISUAL, "04 · Perguntas", ["Antes", ("de lançar.", "b")]),
        c.cta("PROJETO", "05 · Contato"),
    ])
    jsonld = [seo.service(slug, desc), seo.breadcrumb_jsonld(trilha), seo.faq_jsonld(FAQ_AUDIOVISUAL),
              seo.video_bvba()]
    return page(path, title, desc, h1, body, "/assets/og/og-servicos-audiovisual-com-ia.jpg",
                "MAYAA STUDIO · Audiovisual com IA, com direção. Filme, campanha de produto e modelo sintética.",
                jsonld)


# ── /servicos/marketing/ ─────────────────────────────────────────────────────
FAQ_MARKETING = [
    ("Vocês fazem o site inteiro?", [
        "Fazemos página de destino e site quando eles fazem parte do caminho do anúncio.",
        "O foco é o que ajuda a vender, não o site pelo site."]),
    ("Preciso trocar a minha página atual?", [
        "Nem sempre. O diagnóstico mostra se o problema está na página, no formulário, na oferta ou na campanha.",
        "Mexemos onde a leitura aponta."]),
    ("Como sei qual passo está falhando?", [
        "Medindo cada um. Com o rastreamento no lugar, dá para ver onde as pessoas param: no clique, na página, no "
        "formulário ou no atendimento."]),
]


def marketing() -> Page:
    slug = "marketing"
    path = dados.SERVICES[slug]["url"]
    title = "Página, formulário e oferta para anúncio · MAYAA STUDIO"
    desc = ("Página, formulário, oferta e mensagem que sustentam o anúncio. Construímos o caminho entre o clique e a "
            "venda e medimos cada passo. Em São Paulo.")
    h1 = ["O clique", "precisa chegar", ("a algum lugar.", "b")]
    trilha = crumbs(("Serviços", "/servicos/"), ("Marketing", None))

    # R1-06: o passo 01 com uma peça real (anúncio do IOSE, já publicado no case). Não há print de página ou funil
    # feito pela MAYAA: a imagem mostra só o anúncio, e o texto não diz que fizemos a página do IOSE.
    iose = "/assets/cases/iose-trafego-pago/"
    ponto = ('<div class="srv-ad">'
             '<div class="srv-ad__fig">'
             + c.figure(iose + "feed-linhas.jpg",
                        "Anúncio quadrado do IOSE para o curso Projeto de Linhas de Transmissão, com o professor em "
                        "frente a uma torre", "Passo 01 · Anúncio · IOSE", fx=False,
                        sizes="(min-width:1024px) 28vw, (min-width:480px) 28rem, 100vw", link="/cases/iose-trafego-pago/")
             + '</div><div class="srv-ad__txt">'
             f'{c.label("01 · O anúncio, numa peça real", cls="label--rule")}'
             '<p class="lead" data-reveal="fade">Um curso, uma data, um público. O que vem depois do clique precisa '
             'repetir essa promessa: a página, o formulário e quem atende.</p>'
             f'<p data-reveal="fade">{c.link_arrow("Ver as peças do IOSE", "/cases/iose-trafego-pago/")}</p>'
             '</div></div>')

    caminho = c.section(
        intro("02 · O caminho do clique", ["Cinco passos", ("entre o anúncio e a venda.", "b")]),
        c.steps([
            ("Anúncio", "Promete uma coisa só, com clareza."),
            ("Página", "Cumpre a promessa do anúncio, sem desvio."),
            ("Contato", "Formulário ou WhatsApp, com as perguntas que filtram."),
            ("Atendimento", "Quem responde sabe de onde a pessoa veio."),
            ("Venda", "O que fecha volta para a leitura da campanha."),
        ], layout="path", cls="srv-path"),
        ponto,
        f'<p class="srv-path__more" data-reveal="fade">'
        f'{c.link_arrow("O diagnóstico mostra em qual passo o caminho falha", "/servicos/trafego-pago/#diagnostico")}</p>',
        id="caminho", tone="cartao", cls="srv-sec")

    principios = c.section(
        intro("03 · Princípios", ["Uma promessa,", ("do anúncio ao botão.", "b")]),
        c.steps([
            ("Continuidade", "A página repete a promessa do anúncio. Quem clicou reconhece na hora."),
            ("Menos campos, perguntas melhores", "O formulário pergunta só o que ajuda a atender bem."),
            ("Medição de ponta a ponta", "Do anúncio ao contato, cada passo fica registrado para ser lido."),
            ("Nada além do que se entrega", "A oferta diz o que o seu negócio entrega. Nem mais, nem menos."),
        ], layout="grid", cols=2, cls="srv-steps"),
        id="principios", cls="srv-sec")

    relacionados = c.section(
        '<nav class="srv-rel" aria-labelledby="srv-rel-t">'
        f'{c.label("Serviços relacionados", cls="label--rule", id="srv-rel-t")}'
        '<ul class="srv-rel__list" data-reveal="stagger">'
        f'<li>{c.link_arrow("Tráfego pago e performance", "/servicos/trafego-pago/")}</li>'
        f'<li>{c.link_arrow("Audiovisual com IA", "/servicos/audiovisual-com-ia/")}</li>'
        f'<li>{c.link_arrow("Ver o portfólio", "/portfolio/")}</li></ul></nav>',
        id="relacionados", cls="srv-sec srv-sec--rel")

    body = "".join([
        c.page_hero("Serviço 004 · Marketing", h1,
                    "Página, formulário, oferta e mensagem que sustentam o anúncio. Quando o caminho depois do clique "
                    "falha, nenhuma campanha resolve.",
                    kanji=("築", "construir"), crumbs=trilha,
                    ctas=(c.btn("Manda CONTA no direct", config.IG_DM, external=True),
                          c.mail_cta(config.MAILTO_DIAG, pre="Ou por e-mail"))),
        what_we_do(["Tudo o que acontece", ("depois do anúncio.", "b")],
                   "Um bom anúncio leva a pessoa até você. O resto do caminho decide se ela compra. Construímos esse "
                   "caminho junto com a campanha, para que cada passo possa ser medido.",
                   ["Página de destino e site",
                    "Formulário com as perguntas certas",
                    "Oferta e mensagem, da promessa ao botão",
                    "Caminho para o WhatsApp e para o atendimento",
                    "Rastreamento de cada passo, do anúncio ao contato",
                    "Ajuste contínuo a partir do que a campanha mostra"]),
        caminho,
        principios,
        c.faq(FAQ_MARKETING, "04 · Perguntas", ["Antes", ("de mexer na página.", "b")]),
        relacionados,
        c.cta("CONTA", "05 · Contato"),
    ])
    jsonld = [seo.service(slug, desc), seo.breadcrumb_jsonld(trilha), seo.faq_jsonld(FAQ_MARKETING)]
    return page(path, title, desc, h1, body, "/assets/og/og-servicos-marketing.jpg",
                "MAYAA STUDIO · O clique precisa chegar a algum lugar. Página, formulário, oferta e mensagem.", jsonld)


def pages():
    return [indice(), trafego(), audiovisual(), marketing()]
