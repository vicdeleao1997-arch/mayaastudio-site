"""Home `/` (C1 · §3.1). Texto final do SPEC, letra por letra.

Ordem (28/09, benchmark): herói · marcas · faixa 01 · Sobre · Tráfego · prova 12,55× (com o direct ao lado) ·
Audiovisual · Marketing · Trabalhos · Processo · Contato. A prova vem logo depois do tráfego e não sobe mais que isso:
o logo «O Setor Elétrico» das marcas precisa ficar a mais de 800 caracteres do 12,55 (check 8 lê alt e src).
Botão tinta só para o direct; "Ver o serviço" é link com seta. Número só onde há sequência real (Processo)."""
from lib import components as c, config, dados, seo
from lib.page import Page

TITLE = "MAYAA STUDIO · Tráfego pago com IA em São Paulo"
DESC = ("Estúdio de tráfego pago com IA em São Paulo. Meta Ads, Google Ads, audiovisual e marketing, "
        "com anúncio medido em resultado de caixa, não em curtida.")
H1 = ["Do conceito", ("à conversão.", "b")]
BVBA = "/cases/bvba-surrealismo/"


def hero() -> str:
    idx = c.index_nav([
        (None, "Tráfego pago", "#trafego-pago", "↓"),
        (None, "Audiovisual com IA", "#audiovisual", "↓"),
        (None, "Marketing", "#marketing", "↓"),
    ], cls="home-hero__index")   # Portfólio fica no cabeçalho
    dep = ' data-depth-group="hero" data-depth-start="top top"'
    kanji = c.kanji("間", "ma · o espaço entre o conceito e a conversão", size="xl", cls="home-hero__kanji", reveal=None,
                    extra=' data-depth="-12" data-depth-m="-6"' + dep)
    return (
        '<section class="home-hero" id="topo" data-hero><div class="wrap home-hero__in">'
        f'<div class="home-hero__top"><p class="label" data-depth="0" data-depth-o=".2"{dep}>Tráfego pago com IA · São Paulo</p></div>'
        '<div class="grid home-hero__grid">'
        f'{c.title(H1, tag="h1", size="mega", cls="home-hero__title", enter=True)}'
        f'<div class="home-hero__k" data-reveal="ink" data-delay=".1">{kanji}</div>'
        '</div>'
        '<div class="grid home-hero__foot">'
        '<div class="home-hero__body">'
        '<p class="lead" data-reveal="fade" data-delay=".12">Gestão de Meta Ads e Google Ads, com criativo e página feitos '
        'no mesmo estúdio. Anúncio medido em resultado de caixa, não em curtida.</p>'
        f'<div class="home-hero__cta">'
        f'<div class="home-hero__ctas">{c.btn("Já anuncia? Manda CONTA no direct", config.IG_DM, external=True)}'
        f'{c.link_arrow("Ou por e-mail", config.MAILTO_DIAG)}</div></div>'
        '</div>'
        f'<div class="home-hero__idx" data-reveal="fade" data-delay=".18">{idx}</div>'
        '<p class="home-hero__scroll"><a class="label" href="#marcas">Role <span class="mi" aria-hidden="true">'
        '<span data-reveal="fade" data-yp="-100" data-y="0" data-delay=".9">↓</span></span></a></p>'
        '</div></div></section>'
    )


def sobre() -> str:
    texto = c.paras([
        "A MAYAA é um estúdio de tráfego pago com IA em São Paulo. Criamos o criativo, construímos o caminho do "
        "clique e cuidamos da campanha. O mesmo time, do conceito à conversão.",
        "A estética vem do 間 (ma): o valor do espaço, do silêncio e da precisão. Menos ruído, mais intenção.",
        "Tsu dirige a criação e o audiovisual. Victor cuida do tráfego pago e da performance. Quem começa o seu "
        "projeto é quem segue nele.",
    ])
    return c.section(
        c.label("Sobre", cls="label--rule"),
        '<div class="grid home-sobre__grid">'
        f'{c.title(["Imagem, anúncio", "e venda sob o", ("mesmo teto.", "b")], size="display", cls="home-sobre__title")}'
        f'<div class="home-sobre__text stack">{texto}</div></div>',
        id="sobre", cls="home-sobre", extra_ids=("estudio",))


def trafego() -> str:
    return c.service_block(
        "trafego-pago", "Verba certa, régua certa.", ["Tráfego pago", ("e performance.", "b")],
        "Gestão de campanhas em Meta Ads e Google Ads para quem já anuncia. Verba lida campanha por campanha, não no "
        "total do mês. O relatório termina numa decisão: o que continua e o que sai.",
        items=dados.SERVICES["trafego-pago"]["entregas"],
        cta=c.link_arrow("Ver o serviço", "/servicos/trafego-pago/", sr=" de tráfego pago"),
        extra_ids=("servicos",), label_text="Serviço · Tráfego pago")


def audiovisual() -> str:
    # o reel vai na coluna lateral (sem coluna morta); a Ana segue no card de Trabalhos, com a nota de IA
    vid = c.video("/assets/portfolio/reel-surreal.mp4", "/assets/portfolio/reel-surreal-poster.jpg",
                  "Reel da BVBA Supply: o ouro escorre das molduras de um museu enquanto visitantes atravessam a galeria",
                  caption="Filme · BVBA Supply", link=("Ver case", BVBA))
    return c.service_block(
        "audiovisual", "Feito para ser assistido até o fim.", ["Audiovisual", ("com IA.", "b")],
        "Filme, campanha de produto e modelo sintética. A peça real entra como referência; o que a IA constrói passa "
        "por conferência, quadro a quadro. Direção humana do roteiro ao corte.",
        cta=c.link_arrow("Ver o serviço", "/servicos/audiovisual-com-ia/", sr=" de audiovisual com IA"),
        media=f'<div class="home-av">{vid}</div>', label_text="Serviço · Audiovisual com IA")


def marketing() -> str:
    return c.service_block(
        "marketing", "O que sustenta o anúncio.", [("Marketing.", "b")],
        "Página, formulário, oferta e mensagem que sustentam o anúncio. Construímos o caminho entre o clique e a "
        "venda e medimos cada passo. Quando esse caminho falha, nenhuma campanha resolve.",
        items=dados.SERVICES["marketing"]["marcadores"],
        cta=c.link_arrow("Ver o serviço", "/servicos/marketing/", sr=" de marketing"),
        tone="cartao", label_text="Serviço · Marketing")


def trabalhos() -> str:
    """Grade quebrada: BVBA grande à esquerda (col 1 a 7), Alumee e Ana empilhadas à direita (col 8 a 12, 3:2).
    A BVBA usa o quadro da queda (ensaio-03, publicado no case), diferente da faixa 01 e do pôster do reel."""
    lead = c.case_card("bvba-surrealismo", size="lg", heading="h3", ratio="4/5",
                       sizes="(min-width:1024px) 56vw, 100vw",   # col 1 a 7: ~770 px no 1440
                       cover="/assets/cases/bvba-surrealismo/ensaio-03.jpg",
                       cover_alt="Modelo suspenso no ar, caindo sobre uma vitrine de vidro que derrete, com um gato "
                                 "sentado no piso")
    side = "".join(c.case_card(s, size="md", heading="h3", ratio="3/2", delay=.08 * (i + 1))
                   for i, s in enumerate(("alumee-vela-mel", "ana-lauren-modelo-ia")))
    return c.section(
        f'<div class="home-work__head label--rule">{c.label("Trabalhos")}'
        f'{c.link_arrow("Ver portfólio", "/portfolio/")}</div>'
        f'{c.title(["Trabalhos", ("do estúdio.", "b")], size="h2", cls="home-work__title")}'
        f'<div class="home-work"><div class="home-work__lead">{lead}</div>'
        f'<div class="home-work__side" data-depth="-4" data-depth-from="4" data-depth-m="0" data-depth-id="depth-work">'
        f'{side}</div></div>',
        id="trabalhos", cls="home-work-sec")


def processo() -> str:
    return c.process("Processo", ["Cinco movimentos.", ("Uma régua: a venda.", "b")], [
        dict(num="01", kanji="知", meaning="saber", title="Diagnóstico",
             text="Lemos a conta que já roda: o que gasta, o que traz contato e o que vende."),
        dict(num="02", kanji="築", meaning="construir", title="Estrutura",
             text="Campanha, página e formulário montados para que cada passo possa ser lido."),
        dict(num="03", kanji="創", meaning="criar", title="Criação",
             text="Criativo em vídeo e imagem, um para cada formato, com direção humana e IA no ofício."),
        dict(num="04", kanji="磨", meaning="otimizar", title="Otimização",
             text="Campanha por campanha: o que traz venda continua, o que não traz sai."),
        dict(num="05", kanji="展", meaning="escalar", title="Escala",
             text="A verba cresce onde a leitura mostrou resultado, nunca no escuro."),
    ], extra_ids=("metodo",))


def pages():
    body = "".join([
        hero(),
        c.marquee_logos("Marcas que já passaram pelo estúdio"),
        c.band("/assets/img/bandas/museu-moldura-gato.jpg",
               "Galeria clara de museu com uma moldura dourada que derrete até o piso e um gato sentado num pedestal",
               "Campanha · BVBA Supply", ("Ver case", BVBA), pos="50% 32%", id="faixa-01", height="cine"),
        sobre(),
        trafego(),
        c.proof(tone="tinta", cta=True),
        audiovisual(),
        marketing(),
        trabalhos(),
        processo(),
        c.cta("CONTA", "Contato"),
    ])
    jsonld = [seo.webpage("/", TITLE, DESC, "/assets/og/og-mayaa.jpg", breadcrumb=False)]
    return [Page(path="/", title=TITLE, description=DESC, h1=c.plain(H1), body=body,
                 og_image="/assets/og/og-mayaa.jpg",
                 og_alt="MAYAA STUDIO · Tráfego pago com IA em São Paulo · Do conceito à conversão.",
                 jsonld=jsonld, changefreq="weekly", priority=1.0, body_class="home")]
