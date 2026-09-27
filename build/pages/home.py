"""Home `/` (C1 · §3.1). Texto final do SPEC, letra por letra."""
from lib import components as c, config, dados, seo
from lib.page import Page

TITLE = "MAYAA STUDIO · Tráfego pago com IA em São Paulo"
DESC = ("Estúdio de tráfego pago com IA em São Paulo. Meta Ads, Google Ads, audiovisual e marketing, "
        "com anúncio medido em resultado de caixa, não em curtida.")
H1 = ["Do conceito", ("à conversão.", "b")]
BVBA = "/cases/bvba-surrealismo/"
ALUMEE = "/cases/alumee-vela-mel/"
ANA = "/cases/ana-lauren-modelo-ia/"


def hero() -> str:
    idx = c.index_nav([
        ("002", "Tráfego pago", "#trafego-pago", "↓"),
        ("003", "Audiovisual com IA", "#audiovisual", "↓"),
        ("004", "Marketing", "#marketing", "↓"),
    ], cls="home-hero__index")   # Portfólio fica no cabeçalho: no índice era a única linha sem número
    kanji = c.kanji("間", "ma · o espaço entre o conceito e a conversão", size="xl", cls="home-hero__kanji", reveal=None)
    return (
        '<section class="home-hero" id="topo" data-hero><div class="wrap home-hero__in">'
        '<div class="home-hero__top"><p class="label">Tráfego pago com IA · São Paulo</p>'
        '<p class="label home-hero__code">M·001</p></div>'
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
        f'{c.link_arrow("Ou por e-mail", config.MAILTO_DIAG)}</div>'
        '<p class="small home-hero__hint">Manda a palavra CONTA. Começamos pelo diagnóstico do que já roda.</p></div>'
        f'<div data-reveal="fade" data-delay=".65">{c.pillars_line(cls="home-hero__pil")}</div>'
        '</div>'
        f'<div class="home-hero__idx" data-reveal="fade" data-delay=".5">{idx}</div>'
        '<p class="home-hero__scroll"><a class="label" href="#marcas">Role <span aria-hidden="true">↓</span></a></p>'
        '</div></div></section>'
    )


def sobre() -> str:
    grid = c.image_grid([
        dict(src="/assets/cases/bvba-surrealismo/ensaio-01.jpg", caption="Editorial", num="02", link=BVBA,
             alt="Modelo de moletom marrom da BVBA em pé numa galeria clara, com um vão de céu na parede do fundo"),
        dict(src="/assets/cases/alumee-vela-mel/mel-02.jpg", caption="Produto", num="03", link=ALUMEE,
             alt="Vela Mel da Alumee aberta, com a tampa de madeira em pé e o mel escorrendo por fora"),
        dict(src="/assets/cases/bvba-surrealismo/registro-02.jpg", caption="Cenário", num="04", link=BVBA,
             alt="Galeria clara com uma porta de madeira pequena demais na parede do fundo"),
        dict(src="/assets/cases/bvba-surrealismo/sala-04.jpg", caption="Detalhe", num="05", link=BVBA,
             alt="Detalhe vertical de uma gota de ouro caindo numa poça dourada"),
    ], cols=4, ratio="4/5", offset=True)
    texto = c.paras([
        "A MAYAA é um estúdio de tráfego pago com IA em São Paulo. Criamos o criativo, construímos o caminho do "
        "clique e cuidamos da campanha. O mesmo time, do conceito à conversão.",
        "A estética vem do 間 (ma): o valor do espaço, do silêncio e da precisão. Menos ruído, mais intenção.",
        "Tsu dirige a criação e o audiovisual. Victor cuida do tráfego pago e da performance. Quem começa o seu "
        "projeto é quem segue nele.",
    ])
    return c.section(
        c.label("Sobre", num="001", cls="label--rule"),
        '<div class="grid home-sobre__grid">'
        f'{c.title(["Imagem, anúncio", "e venda sob o", ("mesmo teto.", "b")], size="display", cls="home-sobre__title")}'
        f'<div class="home-sobre__text stack">{texto}</div></div>'
        f'<div class="home-sobre__imgs">{grid}</div>',
        id="sobre", cls="home-sobre", extra_ids=("estudio",))


def trafego() -> str:
    media = c.image_grid([
        dict(src="/assets/cases/bvba-surrealismo/ensaio-03.jpg", caption="Criativo · Moda", num="06", link=BVBA,
             alt="Modelo suspenso no ar, caindo sobre uma vitrine de vidro que derrete, com um gato sentado no piso"),
        dict(src="/assets/cases/alumee-vela-mel/mel-01.jpg", caption="Criativo · Produto", num="07", link=ALUMEE,
             alt="Vela Mel da Alumee fechada, com mel escorrendo de uma colher sobre a tampa de madeira até a pedra"),
        dict(src="/assets/cases/bvba-surrealismo/ensaio-02.jpg", caption="Criativo · Moda", num="08", link=BVBA,
             alt="Modelo de camiseta branca da BVBA ao lado de um gato num pedestal e de uma moldura dourada que derrete"),
        dict(src="/assets/cases/alumee-vela-mel/cha-02.jpg", caption="Criativo · Produto", num="09", link=ALUMEE,
             alt="Vela Chá Branco da Alumee acesa sobre tecido cremoso, com uma haste de flor branca e um anel"),
    ], cols=4, ratio="4/5", offset=True)
    return c.service_block(
        "trafego-pago", "002", "Verba certa, régua certa.", ["Tráfego pago", ("e performance.", "b")],
        "Gestão de campanhas em Meta Ads e Google Ads para quem já anuncia. Verba lida campanha por campanha, não no "
        "total do mês. O relatório termina numa decisão: o que continua e o que sai.",
        items=["Diagnóstico da conta que já roda", "Estrutura de campanha com nomes padronizados",
               "Criativo feito para cada formato", "Rastreamento do clique até o contato",
               "Leitura campanha por campanha", "Relatório que termina em decisão"],
        cta=c.btn("Pedir diagnóstico", "/servicos/trafego-pago/#diagnostico"),
        cta2=c.link_arrow("Manda CONTA no direct", config.IG_DM, external=True),
        media=media, extra_ids=("servicos",))


def manifesto() -> str:
    return c.manifesto(
        ["IA é o ofício,", ("não o produto.", "b")],
        "Entra no roteiro, no criativo e na leitura da campanha. Quem decide é sempre uma pessoa.",
        [dict(src="/assets/cases/bvba-surrealismo/sala-03.jpg", caption="Cenário · BVBA Supply", num="10", link=BVBA,
              alt="Parede de ouro líquido escorrendo até formar uma poça no piso, com um gato ao lado"),
         dict(src="/assets/cases/bvba-surrealismo/registro-04.jpg", caption="Detalhe · BVBA Supply", num="11", link=BVBA,
              alt="Gato sentado num pedestal branco no meio da galeria, como peça do acervo"),
         dict(src="/assets/cases/alumee-vela-mel/cha-01.jpg", caption="Produto · Alumee", num="12", link=ALUMEE,
              alt="Vela Chá Branco da Alumee acesa sobre tecido claro, com galhos de flores brancas em primeiro plano")])


def audiovisual() -> str:
    vid = c.video("/assets/portfolio/reel-surreal.mp4", "/assets/portfolio/reel-surreal-poster.jpg",
                  "Reel da BVBA Supply: o ouro escorre das molduras de um museu enquanto visitantes atravessam a galeria",
                  caption="Filme · BVBA Supply · 13", link=("Ver case", BVBA))
    ana = "".join(
        f'<div class="home-av__ph">{c.figure(src, alt, "Modelo 100% IA", num, ratio="4/5", sizes="(min-width:1024px) 23vw, 50vw")}</div>'
        for src, num, alt in [
            ("/assets/portfolio/ana-01.jpg", "14",
             "Ana Lauren, modelo gerada por IA, de vestido preto numa festa à noite, plano aberto"),
            ("/assets/portfolio/ana-03.jpg", "15",
             "Ana Lauren, modelo gerada por IA, em plano médio segurando a bolsa"),
        ])
    media = (
        '<div class="grid home-av">'
        f'<div class="home-av__vid">{vid}</div>'
        f'<div class="home-av__ana">{ana}'
        '<div class="home-av__note">'
        f'{c.note("Nenhuma pessoa real nestas fotos. Ana Lauren é uma modelo criada pela MAYAA com IA.", link=("Ver case", ANA))}'
        f'<p class="home-av__modelo">{c.link_arrow("Manda MODELO no direct", config.IG_DM, external=True)}</p>'
        '</div></div></div>')
    return c.service_block(
        "audiovisual", "003", "Feito para ser assistido até o fim.", ["Audiovisual", ("com IA.", "b")],
        "Filme, campanha de produto e modelo sintética. A peça real entra como referência; o que a IA constrói passa "
        "por conferência, quadro a quadro. Direção humana do roteiro ao corte.",
        cta=c.btn("Ver o serviço", "/servicos/audiovisual-com-ia/", sr=" de audiovisual com IA"),
        media=media)


def marketing() -> str:
    return c.service_block(
        "marketing", "004", "O que sustenta o anúncio.", [("Marketing.", "b")],
        "Página, formulário, oferta e mensagem que sustentam o anúncio. Construímos o caminho entre o clique e a "
        "venda e medimos cada passo. Quando esse caminho falha, nenhuma campanha resolve.",
        cta=c.btn("Ver o serviço", "/servicos/marketing/", sr=" de marketing"),
        media=c.steps(["Anúncio", "Página", "Contato", "Atendimento", "Venda"], layout="path"),
        kanji=("築", "construir"), tone="cartao")


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
    ], num="005", extra_ids=("metodo",))


def pages():
    body = "".join([
        hero(),
        c.marquee_logos("Marcas que já passaram pelo estúdio"),
        c.band("/assets/img/bandas/museu-moldura-gato.jpg",
               "Galeria clara de museu com uma moldura dourada que derrete até o piso e um gato sentado num pedestal",
               "Campanha · BVBA Supply · 01", ("Ver case", BVBA), pos="50% 55%", id="faixa-01"),
        sobre(),
        trafego(),
        c.proof(tone="tinta"),
        manifesto(),
        audiovisual(),
        marketing(),
        processo(),
        c.band("/assets/img/bandas/museu-tres-molduras.jpg",
               "Parede de museu com três molduras douradas vazias; a do meio escorre até o chão",
               "Cenário · BVBA Supply · 16", ("Ver portfólio", "/portfolio/"), pos="50% 40%", id="faixa-16"),
        c.cta("CONTA", "006 · Contato"),
    ])
    jsonld = [seo.webpage("/", TITLE, DESC, "/assets/og/og-mayaa.jpg", breadcrumb=False)]
    return [Page(path="/", title=TITLE, description=DESC, h1=c.plain(H1), body=body,
                 og_image="/assets/og/og-mayaa.jpg",
                 og_alt="MAYAA STUDIO · Tráfego pago com IA em São Paulo · Do conceito à conversão.",
                 jsonld=jsonld, changefreq="weekly", priority=1.0, body_class="home")]
