"""Home `/` (C1 · §3.1). Texto final do SPEC, letra por letra.

Ordem (28/09): herói · marcas · faixa 01 · Sobre · os três serviços seguidos (tráfego, audiovisual, marketing) ·
prova 12,55× · Trabalhos · Processo · Contato. Número só onde há sequência real (os passos do Processo)."""
from lib import components as c, config, dados, seo
from lib.page import Page

TITLE = "MAYAA STUDIO · Tráfego pago com IA em São Paulo"
DESC = ("Estúdio de tráfego pago com IA em São Paulo. Meta Ads, Google Ads, audiovisual e marketing, "
        "com anúncio medido em resultado de caixa, não em curtida.")
H1 = ["Do conceito", ("à conversão.", "b")]
BVBA = "/cases/bvba-surrealismo/"
ANA = "/cases/ana-lauren-modelo-ia/"


def hero() -> str:
    idx = c.index_nav([
        (None, "Tráfego pago", "#trafego-pago", "↓"),
        (None, "Audiovisual com IA", "#audiovisual", "↓"),
        (None, "Marketing", "#marketing", "↓"),
    ], cls="home-hero__index")   # Portfólio fica no cabeçalho
    kanji = c.kanji("間", "ma · o espaço entre o conceito e a conversão", size="xl", cls="home-hero__kanji", reveal=None)
    return (
        '<section class="home-hero" id="topo" data-hero><div class="wrap home-hero__in">'
        '<div class="home-hero__top"><p class="label">Tráfego pago com IA · São Paulo</p></div>'
        '<div class="grid home-hero__grid">'
        f'{c.title(H1, tag="h1", size="mega", cls="home-hero__title", enter=True)}'
        f'<div class="home-hero__k" data-reveal="fade" data-y="16" data-dur="1.2" data-delay=".2">{kanji}</div>'
        '</div>'
        '<div class="grid home-hero__foot">'
        '<div class="home-hero__body">'
        '<p class="lead" data-reveal="fade" data-delay=".45">Gestão de Meta Ads e Google Ads, com criativo e página feitos '
        'no mesmo estúdio. Anúncio medido em resultado de caixa, não em curtida.</p>'
        f'<div class="home-hero__cta" data-reveal="fade" data-delay=".55">'
        f'<div class="home-hero__ctas">{c.btn("Já anuncia? Manda CONTA no direct", config.IG_DM, external=True)}'
        f'{c.link_arrow("Ou por e-mail", config.MAILTO_DIAG)}</div></div>'
        '</div>'
        f'<div class="home-hero__idx" data-reveal="fade" data-delay=".5">{idx}</div>'
        '<p class="home-hero__scroll"><a class="label" href="#marcas">Role <span aria-hidden="true">↓</span></a></p>'
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
        cta=c.btn("Ver o serviço", "/servicos/trafego-pago/", sr=" de tráfego pago"),
        extra_ids=("servicos",), label_text="Serviço · Tráfego pago")


def audiovisual() -> str:
    vid = c.video("/assets/portfolio/reel-surreal.mp4", "/assets/portfolio/reel-surreal-poster.jpg",
                  "Reel da BVBA Supply: o ouro escorre das molduras de um museu enquanto visitantes atravessam a galeria",
                  caption="Filme · BVBA Supply", link=("Ver case", BVBA))
    ana = "".join(
        f'<div class="home-av__ph">{c.figure(src, alt, "Modelo 100% IA", ratio="4/5", sizes="(min-width:1024px) 23vw, 50vw")}</div>'
        for src, alt in [
            ("/assets/portfolio/ana-01.jpg",
             "Ana Lauren, modelo gerada por IA, de vestido preto numa festa à noite, plano aberto"),
            ("/assets/portfolio/ana-03.jpg",
             "Ana Lauren, modelo gerada por IA, em plano médio segurando a bolsa"),
        ])
    media = (
        '<div class="grid home-av">'
        f'<div class="home-av__vid">{vid}</div>'
        f'<div class="home-av__ana">{ana}'
        '<div class="home-av__note">'
        f'{c.note("Nenhuma pessoa real nestas fotos. Ana Lauren é uma modelo criada pela MAYAA com IA.", link=("Ver case", ANA))}'
        '</div></div></div>')
    return c.service_block(
        "audiovisual", "Feito para ser assistido até o fim.", ["Audiovisual", ("com IA.", "b")],
        "Filme, campanha de produto e modelo sintética. A peça real entra como referência; o que a IA constrói passa "
        "por conferência, quadro a quadro. Direção humana do roteiro ao corte.",
        cta=c.btn("Ver o serviço", "/servicos/audiovisual-com-ia/", sr=" de audiovisual com IA"),
        media=media, label_text="Serviço · Audiovisual com IA")


def marketing() -> str:
    return c.service_block(
        "marketing", "O que sustenta o anúncio.", [("Marketing.", "b")],
        "Página, formulário, oferta e mensagem que sustentam o anúncio. Construímos o caminho entre o clique e a "
        "venda e medimos cada passo. Quando esse caminho falha, nenhuma campanha resolve.",
        cta=c.btn("Ver o serviço", "/servicos/marketing/", sr=" de marketing"),
        tone="cartao", label_text="Serviço · Marketing")


def trabalhos() -> str:
    cards = "".join(c.case_card(s, size="md", heading="h3", ratio="1/1")
                    for s in ("bvba-surrealismo", "alumee-vela-mel", "ana-lauren-modelo-ia"))
    return c.section(
        c.label("Trabalhos", cls="label--rule"),
        f'<div class="cols-3 home-work">{cards}</div>'
        f'<p class="home-work__more" data-reveal="fade">{c.link_arrow("Ver portfólio", "/portfolio/")}</p>',
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
               "Campanha · BVBA Supply", ("Ver case", BVBA), pos="50% 55%", id="faixa-01"),
        sobre(),
        trafego(),
        audiovisual(),
        marketing(),
        c.proof(tone="tinta"),
        trabalhos(),
        processo(),
        c.cta("CONTA", "Contato"),
    ])
    jsonld = [seo.webpage("/", TITLE, DESC, "/assets/og/og-mayaa.jpg", breadcrumb=False)]
    return [Page(path="/", title=TITLE, description=DESC, h1=c.plain(H1), body=body,
                 og_image="/assets/og/og-mayaa.jpg",
                 og_alt="MAYAA STUDIO · Tráfego pago com IA em São Paulo · Do conceito à conversão.",
                 jsonld=jsonld, changefreq="weekly", priority=1.0, body_class="home")]
