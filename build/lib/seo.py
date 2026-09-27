"""Blocos JSON-LD (§5.3). O layout junta tudo num único @graph por página."""
from __future__ import annotations

import json

from . import config, dados

ORG_ID = f"{config.SITE_URL}/#organizacao"
SITE_ID = f"{config.SITE_URL}/#site"


def url(path: str) -> str:
    return config.SITE_URL + path if path.startswith("/") else path


def organization() -> dict:
    o = {
        "@type": "Organization", "@id": ORG_ID,
        "name": "MAYAA STUDIO", "alternateName": "まやー工房",
        "url": f"{config.SITE_URL}/", "logo": url("/assets/brand/logo-mayaa-512.png"),
        "image": url("/assets/og/og-mayaa.jpg"), "email": config.EMAIL,
        "description": "Estúdio de tráfego pago com IA em São Paulo. " + dados.PILARES_LINHA + ".",
        "slogan": "Do conceito à conversão.",
        "address": {"@type": "PostalAddress", "addressLocality": "São Paulo", "addressRegion": "SP", "addressCountry": "BR"},
        "areaServed": {"@type": "Country", "name": "Brasil"},
        "knowsAbout": ["Tráfego pago", "Meta Ads", "Google Ads", "Audiovisual com IA", "Marketing", "Performance"],
        "sameAs": [config.IG, config.LINKEDIN],
        "contactPoint": {"@type": "ContactPoint", "contactType": "comercial", "email": config.EMAIL,
                         "availableLanguage": "pt-BR"},
    }
    if config.CNPJ:
        o["taxID"] = config.CNPJ
    if config.RAZAO_SOCIAL and config.CNPJ:
        o["legalName"] = config.RAZAO_SOCIAL
    return o


def website() -> dict:
    return {"@type": "WebSite", "@id": SITE_ID, "name": "MAYAA STUDIO", "url": f"{config.SITE_URL}/",
            "inLanguage": "pt-BR", "publisher": {"@id": ORG_ID}}


def webpage(path: str, name: str, description: str, og_image: str, kind: str = "WebPage",
            breadcrumb: bool = True, **extra) -> dict:
    """WebPage/CollectionPage da página. `name` = title da página."""
    u = url(path)
    d = {"@type": kind, "@id": f"{u}#pagina", "url": u, "name": name, "description": description,
         "inLanguage": "pt-BR", "isPartOf": {"@id": SITE_ID}, "about": {"@id": ORG_ID},
         "primaryImageOfPage": {"@type": "ImageObject", "url": url(og_image)},
         "dateModified": config.LASTMOD}
    if breadcrumb:
        d["breadcrumb"] = {"@id": f"{u}#trilha"}
    d.update(extra)
    return d


def service(slug: str, description: str | None = None) -> dict:
    s = dados.SERVICES[slug]
    return {"@type": "Service", "@id": url(s["url"]) + "#servico", "name": s["titulo"],
            "serviceType": s["service_type"], "description": description or s["linha"],
            "provider": {"@id": ORG_ID}, "areaServed": "BR", "url": url(s["url"])}


def item_list(urls_or_items, name: str | None = None) -> dict:
    """ItemList: lista de URLs (str) ou de blocos (dict)."""
    els = []
    for i, it in enumerate(urls_or_items, 1):
        e = {"@type": "ListItem", "position": i}
        if isinstance(it, str):
            e["url"] = url(it)
        else:
            e["item"] = it
        els.append(e)
    d = {"@type": "ItemList", "itemListElement": els}
    if name:
        d["name"] = name
    return d


def creative_work(path: str, name: str, description: str, genre: str, about: str, images: list[str],
                  **extra) -> dict:
    d = {"@type": "CreativeWork", "@id": url(path) + "#case", "name": name, "url": url(path),
         "description": description, "creator": {"@id": ORG_ID}, "dateCreated": "2026", "genre": genre,
         "image": [url(i) for i in images], "about": about, "inLanguage": "pt-BR"}
    d.update(extra)
    return d


def video(name: str, description: str, thumbnail: str, content: str, upload_date: str = "2026-08-02",
          duration: str = "PT15S") -> dict:
    return {"@type": "VideoObject", "name": name, "description": description, "thumbnailUrl": url(thumbnail),
            "contentUrl": url(content), "uploadDate": upload_date, "duration": duration}


def video_bvba() -> dict:
    """VideoObject do reel da BVBA (página do case e de audiovisual)."""
    return video("BVBA Supply · O surrealismo",
                 "Visitantes atravessam a galeria como numa terça-feira qualquer. O museu derrete ao redor e ninguém "
                 "reage. Câmera travada, luz fixa: quem se move é o corpo e o ouro.",
                 "/assets/portfolio/reel-surreal-poster.jpg", "/assets/portfolio/reel-surreal.mp4")


def faq_jsonld(items) -> dict:
    """items = [(pergunta, [parágrafos])] no mesmo formato do componente faq (links viram texto)."""
    from .components import faq_text
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faq_text(items)]}


def breadcrumb_jsonld(items, path: str | None = None) -> dict:
    """items = [("Início","/"), …, ("Nome", None)]. Sem `path`, o layout completa o @id com a URL da página."""
    els = []
    for i, (name, href) in enumerate(items, 1):
        e = {"@type": "ListItem", "position": i, "name": name}
        if href:
            e["item"] = url(href)
        els.append(e)
    d = {"@type": "BreadcrumbList", "itemListElement": els}
    if path:
        d["@id"] = url(path) + "#trilha"
    return d


def graph(blocks) -> str:
    data = {"@context": "https://schema.org", "@graph": blocks}
    s = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return s.replace("</", "<\\/")
