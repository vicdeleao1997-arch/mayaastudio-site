"""Imagens (§6.5): dimensões reais, srcset com os irmãos que existirem, <picture> com WebP."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from PIL import Image

from . import config
from .html import attrs, esc

SIZES = {
    "band": "100vw",
    "grid4": "(min-width:1024px) 23vw, 50vw",
    "grid3": "(min-width:1024px) 31vw, 50vw",
    "grid2": "(min-width:1024px) 46vw, 100vw",
    "card-lg": "(min-width:1024px) 45vw, 100vw",
    "card-md": "(min-width:1024px) 30vw, 100vw",
    "half": "(min-width:1024px) 50vw, 100vw",
    "third": "(min-width:1024px) 34vw, 100vw",
}


class MediaError(Exception):
    pass


def disk(src: str) -> Path:
    """Caminho em disco de um src absoluto do site ("/assets/x.jpg")."""
    if not src.startswith("/"):
        raise MediaError(f"caminho de mídia precisa ser absoluto a partir da raiz: {src!r}")
    return config.SITE / src.split("?")[0].lstrip("/")


@lru_cache(maxsize=None)
def dims(src: str) -> tuple[int, int]:
    p = disk(src)
    if not p.exists():
        raise MediaError(f"imagem não existe em site/: {src}")
    with Image.open(p) as im:
        return im.size


def exists(src: str) -> bool:
    return disk(src).exists()


def _variants(src: str, ext: str) -> list[tuple[str, int]]:
    """Lista (url, largura) de <nome>-320, <nome>-800, <nome>, <nome>-2400 com a extensão pedida, só os que existem."""
    base, _dot, _old = src.rpartition(".")
    out = []
    for suf in ("-320", "-800", "", "-2400"):
        url = f"{base}{suf}.{ext}"
        if exists(url):
            out.append((url, dims(url)[0]))
    out.sort(key=lambda t: t[1])
    # remove larguras repetidas (ex.: original com 800 px e -800 também)
    seen, uniq = set(), []
    for url, w in out:
        if w not in seen:
            seen.add(w)
            uniq.append((url, w))
    return uniq


def srcset(src: str, ext: str | None = None) -> str:
    ext = ext or src.rpartition(".")[2]
    v = _variants(src, ext)
    return ", ".join(f"{u} {w}w" for u, w in v) if len(v) > 1 or ext == "webp" else ""


def picture(src: str, alt: str, sizes: str = "100vw", cls: str = "", priority: bool = False,
            ratio: str | None = None, decorative: bool = False, img_attrs: dict | None = None) -> str:
    """<picture> com WebP (se houver) + <img> com width/height reais.
    `sizes` aceita uma chave de SIZES ("grid4", "band"…) ou o texto do atributo.
    `ratio` ("4/5") recorta com object-fit:cover. `decorative=True` permite alt vazio."""
    if not decorative and not (alt or "").strip():
        raise MediaError(f"alt vazio em {src}")
    w, h = dims(src)
    sizes = SIZES.get(sizes, sizes)
    jpg_set = srcset(src)
    webp_set = srcset(src, "webp") if exists(src.rpartition(".")[0] + ".webp") or _variants(src, "webp") else ""
    style = f"aspect-ratio:{ratio}" if ratio else None
    img_cls = " ".join(c for c in (cls, "is-cover" if ratio else "") if c) or None
    load = dict(loading="eager", fetchpriority="high") if priority else dict(loading="lazy", decoding="async")
    extra = img_attrs or {}
    img = (f"<img{attrs(cls=img_cls, src=src, srcset=jpg_set or None, sizes=sizes if jpg_set else None, alt=alt or '', width=w, height=h, style=style, **load, **extra)}>")
    source = f'<source type="image/webp"{attrs(srcset=webp_set, sizes=sizes)}>' if webp_set else ""
    return f"<picture>{source}{img}</picture>"


def img(src: str, alt: str, cls: str = "", lazy: bool = True, **extra) -> str:
    """<img> simples (logos, ícones) com width/height reais."""
    w, h = dims(src)
    load = dict(loading="lazy", decoding="async") if lazy else {}
    return f"<img{attrs(cls=cls or None, src=src, alt=alt, width=w, height=h, **load, **extra)}>"


def abs_url(src: str) -> str:
    return config.SITE_URL + src if src.startswith("/") else src


__all__ = ["picture", "img", "dims", "exists", "srcset", "abs_url", "SIZES", "MediaError", "esc"]
