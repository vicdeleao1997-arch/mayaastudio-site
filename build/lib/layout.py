"""Layout comum (§2.7.1, §2.7.16, §5.1): head, moldura, cabeçalho, menu, rodapé e scripts."""
from __future__ import annotations

from . import components as c
from . import config, dados, seo
from .html import attrs, esc
from .page import Page

ASSET_VERSION = {"css": "0", "js": "0"}   # preenchido pelo build.py (hash de 8 caracteres)

NAV = [("servicos", "Serviços", "/servicos/"), ("portfolio", "Portfólio", "/portfolio/")]
# Menu: só os serviços levam número, e é o mesmo código em todo o site (002 · 003 · 004, os da home e de /servicos/).
MENU = [
    ("Início", "/", None), ("Serviços", "/servicos/", None),
    ("Tráfego pago", "/servicos/trafego-pago/", dados.SERVICES["trafego-pago"]["num"]),
    ("Audiovisual com IA", "/servicos/audiovisual-com-ia/", dados.SERVICES["audiovisual-com-ia"]["num"]),
    ("Marketing", "/servicos/marketing/", dados.SERVICES["marketing"]["num"]),
    ("Portfólio", "/portfolio/", None), ("Guia · Tráfego pago com IA", "/trafego-pago-com-ia/", None),
    ("Contato", "#contato", None),
]
MARK_VB = "0 0 1584 1473"


def _mark(cls: str) -> str:
    return (f'<svg class="{cls}" aria-hidden="true" focusable="false" viewBox="{MARK_VB}">'
            f'<use href="/assets/brand/sprite.svg#mk"/></svg>')


def _current(path: str, href: str) -> str:
    return ' aria-current="page"' if path == href else ""


def header(nav_active: str = "", path: str = "") -> str:
    links = []
    for key, txt, href in NAV:
        cur = ' aria-current="page"' if path == href else (' aria-current="true"' if nav_active == key else "")
        links.append(f'<a href="{href}"{cur}>{txt}</a>')
    links.append('<a href="#contato">Contato</a>')
    return (f'<header class="hd" data-header>'
            f'<a class="hd__brand" href="/" aria-label="MAYAA STUDIO, início">{_mark("hd__mark")}'
            f'<span class="hd__name">MAYAA STUDIO</span><span class="hd__kana" lang="ja">まやー工房</span></a>'
            f'<nav class="hd__nav" aria-label="Principal">{"".join(links)}</nav>'
            f'<a class="hd__cta label" href="#contato">Contato</a>'
            f'<button class="hd__menu label" type="button" aria-expanded="false" aria-controls="menu">Menu</button>'
            f'</header>')


def menu(path: str = "") -> str:
    lis = []
    for txt, href, num in MENU:
        n = f'<span class="label menu__num">{esc(num)}</span>' if num else '<span class="label menu__num"></span>'
        lis.append(f'<li><a href="{href}"{_current(path, href)}>{n}'
                   f'<span class="menu__t">{esc(txt)}</span></a></li>')
    foot = (f'<ul class="menu__foot-links">'
            f'<li>{c.link_arrow("Instagram", config.IG, external=True)}</li>'
            f'<li>{c.link_arrow("LinkedIn", config.LINKEDIN, external=True)}</li>'
            f'<li><a class="menu__mail" href="{esc(config.MAILTO_GERAL)}">{esc(config.EMAIL)}</a></li></ul>'
            f'<p class="label menu__sig"><span lang="ja">まやー工房</span> · São Paulo</p>')
    return (f'<div class="menu" id="menu" role="dialog" aria-modal="true" aria-label="Menu" hidden>'
            f'<div class="menu__top"><a class="hd__brand" href="/" aria-label="MAYAA STUDIO, início">{_mark("hd__mark")}'
            f'<span class="hd__name">MAYAA STUDIO</span></a>'
            f'<button class="menu__close label" type="button">Fechar</button></div>'
            f'<nav class="menu__nav" aria-label="Menu principal"><ol class="menu__list">{"".join(lis)}</ol></nav>'
            f'<div class="menu__foot">{foot}</div></div>')


def footer(contato_aqui: bool) -> str:
    base_l = (f"© {config.ANO} MAYAA STUDIO · CNPJ {config.CNPJ} · São Paulo · Brasil" if config.CNPJ
              else f"© {config.ANO} MAYAA STUDIO · São Paulo · Brasil")
    navegar = [("Início", "/"), ("Serviços", "/servicos/"), ("Portfólio", "/portfolio/"),
               ("Guia · Tráfego pago com IA", "/trafego-pago-com-ia/"), ("Privacidade", "/privacidade/")]
    servicos = [("Tráfego pago", "/servicos/trafego-pago/"), ("Audiovisual com IA", "/servicos/audiovisual-com-ia/"),
                ("Marketing", "/servicos/marketing/")]

    def col(titulo: str, itens, cls: str, id_: str | None = None) -> str:
        lis = "".join(f"<li>{i}</li>" for i in itens)
        return (f'<div{attrs(cls="ft__col " + cls, id=id_)}><p class="label ft__h">{titulo}</p>'
                f'<ul class="ft__list">{lis}</ul></div>')

    nav_html = [f'<a href="{h}">{esc(t)}</a>' for t, h in navegar]
    srv_html = [f'<a href="{h}">{esc(t)}</a>' for t, h in servicos]
    ext = lambda t, h: (f'<a href="{esc(h)}" target="_blank" rel="noopener">{esc(t)}'
                        f'<span aria-hidden="true"> {c.ICO_OUT}</span>{c.sr(" (abre em nova aba)")}</a>')
    cont_html = [ext("Instagram", config.IG), ext("LinkedIn", config.LINKEDIN),
                 f'<a class="ft__mail" href="{esc(config.MAILTO_GERAL)}">{esc(config.EMAIL)}</a>']
    return (f'<footer class="ft on-tinta" id="rodape">'
            f'{c.marquee_text("まやー工房 · Do conceito à conversão · MAYAA STUDIO · ", cls="ft__mq")}'
            f'<div class="wrap grid ft__grid">'
            f'<div class="ft__brand"><svg class="ft__lk" role="img" aria-label="MAYAA STUDIO, まやー工房" viewBox="520 470 2130 2210">'
            f'<use href="/assets/brand/sprite.svg#lk" width="3171" height="3171"/></svg>'
            f'<p class="ft__claim">Estúdio de tráfego pago com IA em São Paulo. Do conceito à conversão.</p>'
            f'{c.pillars_line(cls="ft__pil")}</div>'
            f'{col("Navegar", nav_html, "ft__col--nav")}{col("Serviços", srv_html, "ft__col--srv")}'
            f'{col("Contato", cont_html, "ft__col--ct", None if not contato_aqui else "contato")}</div>'
            f'<div class="wrap"><div class="ft__base small"><p>{esc(base_l)}</p><p>IA é o ofício, não o produto.</p></div></div>'
            f'</footer>')


def _head(page: Page) -> str:
    canon = seo.url(page.path if page.path != "/404.html" else "/404.html")
    og_img = seo.url(page.og_image)
    robots = '<meta name="robots" content="noindex">' if page.noindex else ""
    v = ASSET_VERSION
    return (
        '<meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
        f"<title>{esc(page.title)}</title>"
        f'<meta name="description" content="{esc(page.description)}">{robots}'
        f'<link rel="canonical" href="{esc(canon)}">'
        '<meta name="color-scheme" content="light"><meta name="theme-color" content="#F6F4EF">'
        f'<meta property="og:type" content="{esc(page.og_type)}"><meta property="og:locale" content="pt_BR">'
        f'<meta property="og:site_name" content="MAYAA STUDIO"><meta property="og:url" content="{esc(canon)}">'
        f'<meta property="og:title" content="{esc(page.title)}"><meta property="og:description" content="{esc(page.description)}">'
        f'<meta property="og:image" content="{esc(og_img)}"><meta property="og:image:width" content="1200">'
        f'<meta property="og:image:height" content="630"><meta property="og:image:alt" content="{esc(page.og_alt)}">'
        '<meta name="twitter:card" content="summary_large_image">'
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
        '<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">'
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">'
        f'<link rel="stylesheet" href="/assets/css/main.css?v={v["css"]}">'
        + "".join(f'<link rel="preload" href="/assets/fonts/{f}.woff2" as="font" type="font/woff2" crossorigin>'
                  for f in config.FONTS_PRELOAD) +
        "<script>document.documentElement.classList.add('js')</script>"
    )


def _jsonld(page: Page) -> str:
    """Organization e WebSite em toda página (o #site é referenciado por isPartOf); depois os blocos da página."""
    blocks = [seo.organization(), seo.website()]
    canon = seo.url(page.path)
    for b in page.jsonld:
        b = dict(b)
        if b.get("@type") == "WebSite":
            continue
        if b.get("@type") == "BreadcrumbList" and "@id" not in b:
            b["@id"] = canon + "#trilha"
        blocks.append(b)
    return seo.graph(blocks)


def render(page: Page) -> str:
    contato_no_corpo = 'id="contato"' in page.body
    v = ASSET_VERSION
    scripts = (f'<script src="{config.CDN["gsap"]}" defer></script>'
               f'<script src="{config.CDN["scrolltrigger"]}" defer></script>'
               f'<script src="/assets/js/main.js?v={v["js"]}" defer></script>')
    body_cls = f' class="{esc(page.body_class)}"' if page.body_class else ""
    return (
        "<!doctype html>\n"
        f'<html lang="pt-BR"><head>{_head(page)}</head>\n'
        f"<body{body_cls}>"
        '<a class="skip" href="#conteudo">Pular para o conteúdo</a>'
        '<div class="frame" aria-hidden="true"></div>'
        f"{header(page.nav, page.path)}{menu(page.path)}\n"
        f'<main id="conteudo" tabindex="-1">\n{page.body}\n</main>\n'
        f"{footer(not contato_no_corpo)}\n"
        f'<script type="application/ld+json">{_jsonld(page)}</script>\n'
        f"{scripts}\n</body></html>\n"
    )
