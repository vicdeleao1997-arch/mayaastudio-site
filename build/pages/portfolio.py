"""Portfólio `/portfolio/` (C3 · SPEC §3.7). Texto final do SPEC, letra por letra.
CSS próprio em styles/60-cases.css (prefixo .pf-)."""
from __future__ import annotations

from pathlib import Path

from lib import components as c, dados, seo
from lib.html import esc
from lib.media import img
from lib.page import Page

PATH = "/portfolio/"
TITLE = "Portfólio · audiovisual com IA e tráfego pago · MAYAA STUDIO"
DESC = ("Cases da MAYAA STUDIO: fashion film com IA para a BVBA Supply, lançamento da vela Mel da Alumee, a modelo "
        "sintética Ana Lauren e o tráfego pago do IOSE.")
H1 = ["Trabalhos", ("do estúdio.", "b")]
OG = "/assets/og/og-portfolio.jpg"
CRUMBS = [("Início", "/"), ("Portfólio", None)]


def cases_grid() -> str:
    # 1.ª capa: maior conteúdo da 1.ª dobra no celular (LCP) → eager + fetchpriority=high
    # máscara em cascata na ordem de leitura (linha*2 + coluna = i; i * .08, teto .5); coluna par numa 2.ª camada (±4%, só
    # >= 1024, no card: o .pf-grid__item já tem o degrau de 18% no CSS)
    dep = ' data-depth="-4" data-depth-from="4" data-depth-m="0" data-depth-group="pf"'
    cards = "".join(f'<div class="pf-grid__item">{c.case_card(s, size="lg", heading="h2", priority=(i == 0), delay=round(min(i * .08, .5), 2), extra=dep if i % 2 else "")}</div>'
                    for i, s in enumerate(dados.ORDEM_CASES))
    return (f'<section class="sec pf-cases" id="cases" aria-label="Cases"><div class="wrap">'
            f'<div class="pf-grid">{cards}</div></div></section>')


# Na parede estática os logos ficam parados e maiores: emblemas com muito detalhe pedem escala própria.
ESCALA_PAREDE = {"daterrinha": 2.2, "paluama": 1.6, "osetor": 0.7}   # por nome do arquivo, sem extensão


def clientes() -> str:
    logos = "".join(
        f'<li class="pf-logo" style="--k:{ESCALA_PAREDE.get(Path(arq).stem, k)}">'
        f'{img(f"/assets/clients/{arq}", alt, cls="pf-logo__img")}</li>'
        for arq, alt, k in dados.CLIENT_LOGOS)
    return c.section(
        c.head("Clientes", lines=["Marcas que já passaram", ("pelo estúdio.", "b")],
               text="Marcas diferentes, o mesmo rigor.", cls="pf-clientes__head"),
        f'<ul class="cols-3 pf-logos" role="list" aria-label="Logos das marcas" data-reveal="stagger" data-y="16" '
        f'data-st=".04">{logos}</ul>',
        id="clientes", tone="cartao", cls="pf-clientes")


def pages():
    body = "".join([
        c.page_hero("Portfólio · 04 cases", H1,
                    "Cada case com o desafio, a abordagem e as peças. Aqui mostramos o trabalho; número de conta de "
                    "cliente só aparece sem nome.",
                    crumbs=[("Início", "/"), ("Portfólio", None)], compact=True,
                    h1_cls="ph__title--uma"),
        cases_grid(),
        clientes(),
        c.cta("CONTA", "Contato"),
    ])
    urls = [f"/cases/{s}/" for s in dados.ORDEM_CASES]
    lista = seo.item_list(urls, name="Cases da MAYAA STUDIO")
    jsonld = [seo.webpage(PATH, TITLE, DESC, OG, kind="CollectionPage", mainEntity=lista),
              seo.breadcrumb_jsonld(CRUMBS)]
    return [Page(path=PATH, title=TITLE, description=DESC, h1=c.plain(H1), body=body, og_image=OG,
                 og_alt="Portfólio da MAYAA STUDIO · Trabalhos do estúdio", jsonld=jsonld, nav="portfolio",
                 priority=0.8, body_class="pf-page")]
