"""Página 404 (C1 · §3.14). Servida pelo GitHub Pages em qualquer URL inexistente: todos os caminhos são absolutos."""
from lib import components as c, config
from lib.page import Page

TITLE = "Página não encontrada · MAYAA STUDIO"
DESC = ("O endereço pode ter mudado. Volte ao início, aos serviços ou ao portfólio da MAYAA STUDIO, "
        "estúdio de tráfego pago com IA em São Paulo.")
H1 = ["Esta página", ("não existe.", "b")]


def pages():
    body = (
        '<section class="ph ph--404" data-hero><div class="wrap"><div class="grid ph__grid err__grid">'
        f'{c.label("404 · ma", cls="ph__label")}'
        f'{c.title(H1, tag="h1", size="h1", cls="ph__title", enter=True)}'
        f'{c.kanji("間", "ma · espaço", size="xl", cls="err__kanji")}'
        '<p class="lead ph__lead" data-reveal="fade" data-delay=".12">O endereço pode ter mudado. Aqui, o espaço vazio '
        'também é conteúdo, mas não era isto que você procurava.</p>'
        '</div>'
        f'<div class="err__links">{c.list_links([("Início", "/"), ("Serviços", "/servicos/"), ("Portfólio", "/portfolio/"), ("Guia · Tráfego pago com IA", "/trafego-pago-com-ia/"), ("Manda CONTA no direct", config.IG_DM)])}</div>'
        '</div></section>'
    )
    return [Page(path="/404.html", title=TITLE, description=DESC, h1=c.plain(H1), body=body,
                 og_image="/assets/og/og-mayaa.jpg", og_alt="MAYAA STUDIO · Esta página não existe.",
                 sitemap=False, noindex=True, body_class="err")]
