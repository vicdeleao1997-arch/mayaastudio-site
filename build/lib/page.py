"""Contrato de página (§6.2). Cada módulo de pages/ expõe `def pages() -> list[Page]`."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Page:
    path: str                    # "/servicos/trafego-pago/" · "/404.html"
    title: str                   # <title> completo (§5.2)
    description: str
    h1: str                      # texto corrido do H1 (conferido pelo check 5)
    body: str                    # HTML do <main id="conteudo">
    og_image: str                # caminho absoluto a partir da raiz
    og_alt: str
    jsonld: list = field(default_factory=list)      # blocos além de Organization
    nav: str = ""                # "servicos" | "portfolio" | ""
    og_type: str = "website"
    lastmod: str | None = None   # None = config.LASTMOD
    changefreq: str = "monthly"
    priority: float = 0.7
    sitemap: bool = True
    noindex: bool = False
    body_class: str = ""
    progress: bool = False       # fio de leitura no cabeçalho (cases, guia, privacidade)
    cta: str = "CONTA"           # variante do CTA final ("CONTA" · "MODELO" · "PROJETO" · "COLECAO"): rótulo do topo
