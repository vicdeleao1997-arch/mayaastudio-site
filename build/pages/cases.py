"""Páginas de case (C3 · SPEC §3.8 a §3.12). Texto final do SPEC, letra por letra.

Estrutura comum (formato de case da NUMIS, na identidade da MAYAA):
case_hero + abertura · Visão geral · Abordagem + "O que foi feito" · séries por tema · Resumo · nota ·
cta_final · next_case. Numeração de legenda contínua dentro de cada case. Nenhuma métrica em nenhum case.
CSS próprio em styles/60-cases.css (prefixo .case-).
"""
from __future__ import annotations

from lib import components as c, config, dados, seo
from lib.html import attrs, esc
from lib.media import dims
from lib.page import Page

A_BVBA = "/assets/cases/bvba-surrealismo/"
A_ALU = "/assets/cases/alumee-vela-mel/"
A_ANA = "/assets/portfolio/"
A_IOSE = "/assets/cases/iose-trafego-pago/"

ALT_BANDA_GATO = ("Galeria clara de museu com uma moldura dourada que derrete até o piso e um gato sentado "
                  "num pedestal")
ALT_BANDA_MOLDURAS = "Parede de museu com três molduras douradas vazias; a do meio escorre até o chão"


# ── blocos de página ─────────────────────────────────────────────────────────
def _ar(src: str) -> str:
    w, h = dims(src)
    return f"{w / h:.4f}"


def fit(html: str, ar: str | float, cls: str = "") -> str:
    """Envolve mídia de proporção natural para caber na altura da janela (série "1 + texto", abertura)."""
    return f'<div class="case-fit{(" " + cls) if cls else ""}" style="--ar:{ar}">{html}</div>'


def fig(src: str, alt: str, caption: str, num: str, fx: bool = True, sizes: str = "(min-width:1024px) 50vw, 100vw",
        priority: bool = False) -> str:
    return c.figure(src, alt, caption, num, style="desc", fx=fx, sizes=sizes, priority=priority)


def texto(num: str, nome: str, paragrafos: list[str], feito: list[str] | None = None, id: str | None = None) -> str:
    """Visão geral / Abordagem: rótulo de seção (fio na largura toda) e texto logo abaixo (1.º parágrafo em Shippori).
    `num` fica na assinatura por compatibilidade; rótulo de seção não leva número."""
    p1, *resto = paragrafos
    corpo = f'<p class="case-txt__lead" data-reveal="fade">{esc(p1)}</p>'
    corpo += "".join(f'<p class="case-txt__p" data-reveal="fade">{esc(p)}</p>' for p in resto)
    if feito:
        corpo += (f'<div class="case-feito">{c.label("O que foi feito", cls="case-feito__label")}'
                  f'{c.deliv_list(feito, cls="case-feito__list")}</div>')
    return (f'<section{attrs(cls="sec case-txt", id=id)}>'
            f'<div class="wrap grid case-txt__grid">'
            f'{c.label(nome, cls="label--rule case-txt__label")}'
            f'<div class="case-txt__body">{corpo}</div></div></section>')


def ficha_faixa(rows) -> str:
    """Ficha técnica em faixa, logo abaixo da imagem de abertura (a abertura sobe para a 1.ª dobra)."""
    return f'<div class="wrap case-ficha">{c.ficha(rows, cls="ficha--row")}</div>'


def resumo(frase: str, nota: str, extra: str = "") -> str:
    """Resumo: frase em Shippori + (extra) + nota de IA / de "sem número"."""
    return (f'<section class="sec case-txt case-resumo" id="resumo"><div class="wrap grid case-txt__grid">'
            f'{c.label("Resumo", cls="label--rule case-txt__label")}'
            f'<div class="case-txt__body"><p class="case-resumo__t" data-reveal="fade">{esc(frase)}</p>'
            f'{extra}{c.note(nota, cls="case-resumo__note")}</div></div></section>')


def page(slug: str, title: str, description: str, og_alt: str, body: str, images: list[str], extra_ld=()):
    cz = dados.CASES[slug]
    path = f"/cases/{slug}/"
    h1 = c.plain(_h1_lines(slug))
    if slug == "bvba-surrealismo":
        h1 = "BVBA Supply · O surrealismo."
    crumbs = [("Início", "/"), ("Portfólio", "/portfolio/"), (cz["marca"], None)]
    og = f"/assets/cases/{slug}/og.jpg"
    cw_extra = {}
    if cz.get("ia_pessoa"):
        cw_extra["abstract"] = "Nenhuma pessoa real nestas fotos."
    cw = seo.creative_work(path, h1, description, cz["segmento"], cz["entregavel"], images, **cw_extra)
    ld = [cw, *extra_ld, seo.breadcrumb_jsonld(crumbs)]
    return Page(path=path, title=title, description=description, h1=h1, body=body, og_image=og, og_alt=og_alt,
                jsonld=ld, nav="portfolio", og_type="article", priority=0.7, body_class="case-page")


def _h1_lines(slug: str):
    cz = dados.CASES[slug]
    return {"bvba-surrealismo": ["BVBA Supply", ("O surrealismo.", "b")],
            "ana-lauren-modelo-ia": ["Ana Lauren", ("é 100% IA.", "b")]}.get(
        slug, [cz["marca"], (cz["titulo"] + ".", "b")])


# ── 01 · BVBA Supply ─────────────────────────────────────────────────────────
def bvba() -> Page:
    slug = "bvba-surrealismo"
    reel = c.video("/assets/portfolio/reel-surreal.mp4", "/assets/portfolio/reel-surreal-poster.jpg",
                   "Reel da BVBA Supply: visitantes atravessam um museu que derrete ao redor",
                   caption="Reel · 9:16 · 0:15", link=("Ver o reel no Instagram", config.REEL_BVBA), style="desc")

    def it(nome, num, cap, alt, **kw):
        return dict(src=A_BVBA + nome, num=num, caption=cap, alt=alt, **kw)

    ensaio = [
        it("ensaio-01.jpg", "01", "Sala clara, vão de céu ao fundo",
           "Modelo de moletom marrom da BVBA em pé numa galeria clara, com um vão de céu na parede do fundo"),
        it("ensaio-02.jpg", "02", "A moldura cede ao lado do gato",
           "Modelo de camiseta branca da BVBA ao lado de um gato num pedestal e de uma moldura dourada que derrete"),
        it("ensaio-03.jpg", "03", "A queda sobre a vitrine",
           "Modelo suspenso no ar, caindo sobre uma vitrine de vidro que derrete, com um gato sentado no piso"),
    ]
    sala = [
        it("sala-01.jpg", "04", "Moldura escorrendo, plano aberto",
           "Galeria clara com moldura dourada derretendo pela parede e gato sentado num pedestal", ratio="4/5"),
        it("sala-02.jpg", "05", "O pedestal cede", "Gato sentado sobre um pedestal branco que derrete e se espalha pelo chão",
           ratio="4/5"),
        it("sala-03.jpg", "06", "A parede de ouro",
           "Parede de ouro líquido escorrendo até formar uma poça no piso, com um gato ao lado", ratio="4/5"),
        it("sala-04.jpg", "07", "A gota, em detalhe", "Detalhe vertical de uma gota de ouro caindo numa poça dourada",
           ratio="4/5"),
    ]
    registros = [
        it("registro-01.jpg", "08", "Ausência: a tela caiu",
           "Galeria com uma moldura vazia na parede e a tela caída no chão, encostada"),
        it("registro-02.jpg", "09", "Escala: a porta pequena",
           "Galeria clara com uma porta de madeira pequena demais na parede do fundo"),
        it("registro-03.jpg", "10", "A sombra que não bate",
           "Galeria clara com um quadro cuja sombra pintada não combina com a luz da sala"),
        it("registro-04.jpg", "11", "O gato, exposto como acervo",
           "Gato sentado num pedestal branco no meio da galeria, como peça do acervo"),
    ]
    body = "".join([
        c.case_hero(slug,
                    "Filme e editorial de coleção num museu que não existe. A roupa é real, o corpo é real. A sala, a "
                    "luz de galeria e o ouro que escorre pelas paredes foram construídos depois, com IA e com direção."),
        f'<div class="case-open case-open--band">'
        + c.band("/assets/img/bandas/museu-moldura-gato.jpg", ALT_BANDA_GATO, "Abertura · A sala construída, na horizontal",
                 priority=True, pos="50% 55%", id="abertura")
        + ficha_faixa([("Cliente", "BVBA Supply"), ("Segmento", "Moda"),
                       ("Entregável", "Reel 9:16, editorial e cenário"), ("Ano", "2026")]) + "</div>",
        c.case_series("", "Ninguém acha estranho.",
                      "Visitantes atravessam a galeria como numa terça-feira qualquer. O museu derrete ao redor e "
                      "ninguém reage. Câmera travada, luz fixa: quem se move é o corpo e o ouro.",
                      [fit(reel, "0.5625", "case-fit--vid")], id="filme", label_text="Filme"),
        texto("01", "Visão geral", [
            "Uma coleção pedia um cenário que nenhum estúdio alugado entrega: um museu surreal, sóbrio, com a mesma "
            "sala em todas as fotos e em todos os planos do vídeo.",
            "A primeira tentativa, gerada só a partir de texto, mudava a cada imagem. A sala virava outra, o gato "
            "trocava de cara. Descrição sozinha não segura continuidade."], id="visao-geral"),
        texto("02", "Abordagem", [
            "Invertemos a ordem. Primeiro veio uma imagem-mestre da sala, com planta baixa, inventário de materiais e "
            "mapa de luz. Toda variação nasce dessa imagem, nunca do zero.",
            "No set, câmera travada e luz que não muda. Depois, o museu entra por trás do corpo e se mexe. A regra de "
            "arte: uma coisa errada por enquadramento, nunca duas."],
            feito=["Guia do cenário: planta, materiais e luz",
                   "Imagens da sala em alta resolução, vertical e horizontal",
                   "Direção de set: câmera, luz e marcações no chão",
                   "Composição da peça real com o cenário",
                   "Reel vertical para Instagram"], id="abordagem"),
        c.case_series("01", "O ensaio",
                      "A peça real, no corpo real, dentro da sala construída. A luz do set foi escolhida para bater com "
                      "a luz da galeria.", ensaio, id="ensaio"),
        c.case_series("02", "A sala que cede",
                      "O surreal está no prédio, não no quadro. Parede que escorre como cera assusta mais do que "
                      "pintura estranha.", sala, id="sala"),
        c.case_series("03", "Os outros registros",
                      "Um estranhamento por enquadramento: ausência, escala, sombra e o gato como acervo.",
                      registros, id="registros"),
        f'<div class="case-open case-open--band case-close">'
        + c.band("/assets/img/bandas/museu-tres-molduras.jpg", ALT_BANDA_MOLDURAS, "12 · Três molduras, uma cede",
                 pos="50% 40%", id="fecho") + "</div>",
        resumo("Uma sala construída segurou todas as imagens e o filme sem trocar de cara. A roupa e o corpo ficaram "
               "reais; o surreal ficou no prédio.",
               "Imagens geradas e compostas com IA a partir de ensaio fotográfico real, com direção da MAYAA. Esta "
               "página mostra criação; não há número de mídia aqui."),
        c.cta("COLECAO", "Próximo passo"),
        c.next_case(slug),
    ])
    imagens = (["/assets/img/bandas/museu-moldura-gato.jpg"] + [i["src"] for i in ensaio + sala + registros]
               + ["/assets/img/bandas/museu-tres-molduras.jpg"])
    return page(slug, "BVBA Supply · O surrealismo · fashion film com IA · MAYAA STUDIO",
                "Fashion film e editorial de coleção num museu que não existe. Roupa e corpo reais, sala construída "
                "com IA a partir de uma imagem-mestre. Case BVBA Supply.",
                "BVBA Supply · O surrealismo · case de fashion film com IA da MAYAA STUDIO",
                body, imagens, extra_ld=[seo.video_bvba()])


# ── 02 · Alumee ──────────────────────────────────────────────────────────────
def alumee() -> Page:
    slug = "alumee-vela-mel"
    mel01, mel02 = A_ALU + "mel-01.jpg", A_ALU + "mel-02.jpg"
    cha = [
        dict(src=A_ALU + "cha-01.jpg", num="04", caption="Composição final, chama alta", ratio="3/4",
             alt="Vela Chá Branco da Alumee acesa sobre tecido claro, com galhos de flores brancas em primeiro plano"),
        dict(src=A_ALU + "cha-02.jpg", num="05", caption="Estética editorial, tecido e flor", ratio="3/4",
             alt="Vela Chá Branco da Alumee acesa sobre tecido cremoso, com uma haste de flor branca e um anel"),
    ]
    abertura = fig(mel01, "Vela Mel da Alumee fechada, com mel escorrendo de uma colher sobre a tampa de madeira até a "
                   "pedra", "Mel sobre a tampa fechada", "01", priority=True, sizes="(min-width:1024px) 45vw, 100vw")
    mel_det = A_ALU + "mel-detalhe.jpg"   # recorte da arte aprovada (vela Mel fechada), sem nenhuma edição
    serie_mel = [
        dict(src=mel02, num="02", caption="Pote aberto, tampa em pé", ratio="3/4",
             alt="Vela Mel da Alumee aberta, com a tampa de madeira em pé e o mel escorrendo por fora"),
        dict(src=mel_det, num="03", caption="Detalhe: rótulo, madeira e mel", ratio="3/4",
             alt="Detalhe da vela Mel da Alumee: rótulo de papel reciclado, tampa de madeira e o fio de mel que "
                 "escorre até a pedra"),
    ]
    reel = (f'<div class="case-reel">{c.label("O reel de lançamento", cls="case-reel__label")}'
            f'<p class="small case-reel__txt">O lançamento em vídeo está no Instagram da MAYAA.</p>'
            f'{c.ig_embed(config.REEL_ALUMEE, "reel", "o reel")}'
            f'</div>')
    body = "".join([
        c.case_hero(slug,
                    "Campanha de lançamento feita a partir do produto real. A vela, o rótulo e a tampa são os de "
                    "verdade. O mel escorrendo, a pedra e a luz de fim de tarde vieram da IA, conferidos peça por peça."),
        f'<section class="sec case-open case-open--rev" id="abertura"><div class="wrap grid case-open__grid">'
        f'<div class="case-open__ficha">'
        + c.ficha([("Cliente", "Alumee"), ("Segmento", "Velas artesanais"),
                   ("Entregável", "Campanha de lançamento, fotos e reel"), ("Ano", "2026")])
        + f'</div>{fit(abertura, _ar(mel01), "case-open__media")}</div></section>',
        texto("01", "Visão geral", [
            "Produto artesanal vive de detalhe: o papel reciclado do rótulo, a tipografia, a madeira da tampa, o nível "
            "da cera no pote.",
            "Imagem feita por IA costuma alisar tudo isso. Numa vela, rótulo errado é produto errado, e a cliente "
            "reconhece na hora."], id="visao-geral"),
        texto("02", "Abordagem", [
            "As fotos-mestre do produto entram como referência em toda geração, com as medidas do pote e da etiqueta. "
            "A cena nasce por referência, sem colar rótulo por cima.",
            "Cada correção mexe só na área pedida; o resto fica congelado. Antes de aprovar, conferência de proporção, "
            "tampa, rótulo, pavio, vidro, madeira e textura da pedra."],
            feito=["Direção de arte da cena de lançamento",
                   "Fotos verticais 3:4 para feed e anúncio",
                   "Regra de preservação do produto em cada edição",
                   "Segunda fragrância no mesmo método",
                   "Reel de lançamento no Instagram"], id="abordagem"),
        c.case_series("01", "Mel",
                      "Um único fio de mel, da colher até a pedra. Gravidade, brilho e poça no lugar certo; nunca "
                      "dentro do pote.", serie_mel, id="mel"),
        c.case_series("02", "Chá Branco",
                      "A mesma regra, outra fragrância: tecido, flor discreta e chama presa ao pavio.", cha, id="cha-branco"),
        resumo("Duas fragrâncias, o mesmo método: o produto real como referência em cada imagem e conferência peça por "
               "peça antes de aprovar.",
               "Cenas criadas com IA a partir das fotos reais do produto. Esta página mostra criação; não há número de "
               "mídia aqui.", extra=reel),
        c.cta("PROJETO", "Próximo passo"),
        c.next_case(slug),
    ])
    imagens = [mel01, mel02, mel_det] + [i["src"] for i in cha]
    return page(slug, "Alumee vela Mel · campanha de lançamento com IA · MAYAA STUDIO",
                "Campanha de lançamento da vela Mel e da Chá Branco, criada com IA a partir do produto real, com "
                "rótulo, vidro e madeira preservados. Case Alumee.",
                "Alumee vela Mel · case de campanha de lançamento com IA da MAYAA STUDIO", body, imagens)


# ── 03 · Ana Lauren ──────────────────────────────────────────────────────────
def ana() -> Page:
    slug = "ana-lauren-modelo-ia"
    fotos = [
        dict(src=A_ANA + "ana-01.jpg", num="01", caption="100% IA · Plano aberto", priority=True,
             alt="Ana Lauren, modelo gerada por IA, de vestido preto numa festa à noite, plano aberto"),
        dict(src=A_ANA + "ana-02.jpg", num="02", caption="100% IA · Close",
             alt="Ana Lauren, modelo gerada por IA, sorrindo em close"),
        dict(src=A_ANA + "ana-03.jpg", num="03", caption="100% IA · Plano médio",
             alt="Ana Lauren, modelo gerada por IA, em plano médio segurando a bolsa"),
    ]
    insta = c.case_series("02", "No Instagram", None,
                          [f'<div class="case-ig">{c.ig_embed(config.IG_ANA_POST, "post", "o post", preview="/assets/cases/ana-lauren-modelo-ia/cover.jpg")}</div>'],
                          id="instagram",
                          text_html=f'Post em parceria com {c.text_link("@analauren.ai", config.IG_ANA)}.')
    body = "".join([
        c.case_hero(slug,
                    "Modelo criada do zero pela MAYAA com IA. Licenciável para criativo de anúncio e UGC (conteúdo no "
                    "estilo de cliente) da sua marca, com o mesmo rosto em cada cena.",
                    badge="Nenhuma pessoa real nestas fotos"),
        c.case_series("01", "Uma noite, três planos",
                      "O mesmo rosto do plano aberto ao close. É isso que torna a Ana usável em campanha.",
                      fotos, id="abertura",
                      after=ficha_faixa([("Projeto", "Próprio da MAYAA"), ("Segmento", "Criativo para anúncio e UGC"),
                                         ("Entregável", "Modelo licenciável, fotos e posts"), ("Ano", "2026")])),
        texto("01", "Visão geral", [
            "Marca que anuncia precisa de rosto novo com frequência: para testar criativo, para UGC, para falar com "
            "públicos diferentes.",
            "E imagem de IA comum troca o rosto de uma cena para a outra, o que quebra a confiança de quem vê."],
            id="visao-geral"),
        texto("02", "Abordagem", [
            "Criamos uma pessoa que não existe, com rosto, estilo e jeito de posar definidos, e mantemos a mesma "
            "identidade em todas as cenas.",
            "A Ana tem perfil próprio no Instagram e pode aparecer com o seu produto, no seu cenário. Transparência "
            "vem junto: a Ana é apresentada como IA."],
            feito=["Criação da identidade: rosto, estilo e poses",
                   "Ensaio em cenas diferentes com o mesmo rosto",
                   "Perfil próprio no Instagram, @analauren.ai",
                   "Licença para anúncio e UGC de marca"], id="abordagem"),
        insta,
        resumo("Uma identidade estável, apresentada como IA desde o primeiro post. É isso que torna uma modelo "
               "sintética usável em campanha.",
               "Todas as imagens desta página foram geradas por IA. Nenhuma pessoa real aparece nelas."),
        c.cta("MODELO", "Próximo passo"),
        c.next_case(slug),
    ])
    return page(slug, "Ana Lauren · modelo 100% IA para anúncio · MAYAA STUDIO",
                "Modelo criada do zero com IA pela MAYAA, com o mesmo rosto em cada cena e licenciável para anúncio e "
                "UGC. Nenhuma pessoa real nestas fotos.",
                "Ana Lauren é 100% IA · modelo sintética da MAYAA STUDIO · Nenhuma pessoa real nestas fotos",
                body, [f["src"] for f in fotos])


# ── 04 · IOSE (sem número nenhum na página) ──────────────────────────────────
def iose() -> Page:
    slug = "iose-trafego-pago"
    abertura = [
        (A_IOSE + "feed-bess.jpg", "01", "Armazenamento de energia (BESS)",
         "Anúncio do IOSE para o curso de sistemas de armazenamento de energia, com contêineres de baterias num campo"),
        (A_IOSE + "feed-iec.jpg", "02", "IEC 61850 (norma de automação de subestações), turma extra",
         "Anúncio em carrossel do IOSE para a turma extra do curso IEC 61850, em azul"),
        (A_IOSE + "feed-nbr.jpg", "03", "Nova NBR 5419 (proteção contra descargas atmosféricas)",
         "Anúncio do IOSE para o curso da nova NBR 5419 com o professor em primeiro plano"),
    ]
    figs = "".join(f'<div class="case-pecas__item">'
                   f'{fig(s, a, cap, n, fx=False, sizes="grid3", priority=(i == 0))}</div>'
                   for i, (s, n, cap, a) in enumerate(abertura))
    open_html = (f'<section class="sec case-open case-pecas" id="abertura"><div class="wrap">'
                 f'<div class="case-pecas__grid">{figs}</div>'
                 f'<header class="case-pecas__head">{c.label("Uma peça por curso", cls="label--rule label--5")}'
                 f'<p class="small case-pecas__txt" data-reveal="fade">Cada curso com a sua promessa, a sua data e o '
                 f'seu público. A estrutura da conta segue a mesma lógica.</p></header></div>'
                 + ficha_faixa([("Cliente", "IOSE, Instituto O Setor Elétrico"), ("Segmento", "Educação técnica"),
                                ("Entregável", "Gestão de tráfego pago e criativos"),
                                ("Formatos", "Feed, stories e reels")])
                 + '</section>')
    formatos = [
        dict(src=A_IOSE + "feed-linhas.jpg", num="04", caption="Feed 1:1", fx=False,
             alt="Anúncio quadrado do IOSE para o curso Projeto de Linhas de Transmissão, com o professor em frente a "
                 "uma torre"),
        dict(src=A_IOSE + "stories-linhas.jpg", num="05", caption="Stories 9:16", fx=False,
             alt="O mesmo anúncio do curso de linhas de transmissão adaptado para stories, na vertical"),
    ]
    reel = c.video(A_IOSE + "reel-iec.mp4", poster=A_IOSE + "reel-iec-poster.jpg",
                   label="Reel do IOSE: o professor apresenta o curso IEC 61850", caption="06 · Reels 9:16",
                   play="Ver vídeo", style="desc")
    body = "".join([
        c.case_hero(slug,
                    "O Instituto O Setor Elétrico forma engenheiros e técnicos em cursos online e ao vivo. Cuidamos "
                    "da mídia paga: criativo, estrutura de campanha por curso e leitura do que vira inscrição."),
        open_html,
        texto("01", "Visão geral", [
            "Cada curso tem turma, data de início e público próprios. Quem procura um curso de linhas de transmissão "
            "não é a mesma pessoa que procura a norma nova de proteção contra descargas.",
            "Uma campanha só para tudo dilui a verba e esconde o que funciona."], id="visao-geral"),
        texto("02", "Abordagem", [
            "Uma estrutura por curso, com nome padronizado para cada campanha e cada criativo, para que a leitura seja "
            "possível. Peças feitas para cada formato, com o professor na frente da câmera.",
            "E leitura campanha por campanha, não pelo total do mês: o que traz inscrição continua, o que não traz "
            "sai."],
            feito=["Estrutura de campanha por curso e por turma",
                   "Nomenclatura padrão de campanhas e criativos",
                   "Criativos para feed 1:1, stories e reels 9:16",
                   "Reels com o professor do curso",
                   "Revisão diária e semanal da conta"], id="abordagem"),
        c.case_series("01", "Um curso, cada formato",
                      "A mesma mensagem refeita para cada lugar onde o anúncio aparece. Nada de esticar a peça do feed "
                      "para caber no stories.", formatos, id="formatos"),
        c.case_series("02", "O professor na frente",
                      "Curso técnico se vende por quem ensina. O reel abre com o professor, mostra o conteúdo do curso "
                      "e fecha com a turma.", [fit(reel, "0.5625", "case-fit--vid")], id="professor"),
        resumo("Uma conta organizada por curso, peças feitas para cada formato e leitura campanha por campanha. O que "
               "traz inscrição continua; o que não traz sai.",
               "Sem números nesta página: aqui mostramos o trabalho. Os resultados da conta são do cliente."),
        c.cta("CONTA", "Próximo passo",
              secondary=c.btn("Ver o serviço de tráfego pago", "/servicos/trafego-pago/", kind="ghost")),
        c.next_case(slug),
    ])
    imagens = [s for s, *_ in abertura] + [f["src"] for f in formatos]
    return page(slug, "IOSE · gestão de tráfego pago e criativos · MAYAA STUDIO",
                "Gestão de tráfego pago do Instituto O Setor Elétrico: estrutura de campanha por curso, criativo para "
                "cada formato e leitura campanha por campanha.",
                "IOSE tráfego pago · case de gestão de tráfego pago e criativos da MAYAA STUDIO", body, imagens)


def pages():
    return [bvba(), alumee(), ana(), iose()]
