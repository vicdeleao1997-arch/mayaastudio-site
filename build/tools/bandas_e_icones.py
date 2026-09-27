"""Gera as faixas de tela cheia da home e os ícones do site (C1).

Uso:  py build/tools/bandas_e_icones.py            (pula o que já existe)
      py build/tools/bandas_e_icones.py --forcar   (refaz tudo)

Saídas:
  site/assets/img/bandas/museu-moldura-gato{,-800,-2400}.{jpg,webp}
  site/assets/img/bandas/museu-tres-molduras{,-800,-2400}.{jpg,webp}
  site/favicon.svg · site/favicon-32.png · site/apple-touch-icon.png
  site/assets/icons/icon-192.png · icon-512.png · site/assets/brand/logo-mayaa-512.png
  site/site.webmanifest
Os PNG dos ícones são rasterizados pelo Chrome headless a partir do sprite oficial.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
PLATES = Path("C:/Users/vicde/BVBA_AI_CEO/03_ads_campaigns/2026-07_editorial_museu_surreal/plates")
CHROME = Path("C:/Program Files/Google/Chrome/Application/chrome.exe")
TINTA, PAPEL = "#0B0B0B", "#F6F4EF"

BANDAS = {
    "museu-moldura-gato": PLATES / "G3_full_H32_4k.png",
    "museu-tres-molduras": PLATES / "G3_top_H32_4k.png",
}
LARGURAS = {"-800": 800, "": 1600, "-2400": 2400}


def _salvar_jpg_webp(im: Image.Image, destino_base: Path) -> None:
    im.save(destino_base.with_suffix(".jpg"), "JPEG", quality=82, progressive=True, optimize=True)
    im.save(destino_base.with_suffix(".webp"), "WEBP", quality=78, method=6)


def bandas(forcar: bool) -> None:
    pasta = SITE / "assets" / "img" / "bandas"
    pasta.mkdir(parents=True, exist_ok=True)
    for nome, fonte in BANDAS.items():
        if not fonte.exists():
            print(f"  ! fonte ausente: {fonte}")
            continue
        alvo = pasta / f"{nome}.jpg"
        if alvo.exists() and not forcar:
            print(f"  = {nome} (já existe)")
            continue
        with Image.open(fonte) as src:
            im = src.convert("RGB")  # sRGB, sem metadados (nada de info/exif copiado)
        for suf, largura in LARGURAS.items():
            w = min(largura, im.width)  # nunca amplia
            h = round(im.height * w / im.width)
            out = im.resize((w, h), Image.LANCZOS)
            _salvar_jpg_webp(out, pasta / f"{nome}{suf}")
            print(f"  + {nome}{suf} {w}x{h}")


def _simbolo(sprite: str, sid: str) -> tuple[str, str]:
    m = re.search(rf'<symbol id="{sid}" viewBox="([^"]+)">(.*?)</symbol>', sprite, re.S)
    if not m:
        raise SystemExit(f"símbolo #{sid} não encontrado no sprite")
    return m.group(1), m.group(2)


def _svg_quadrado(vb: str, corpo: str, cor: str, folga: float) -> str:
    x, y, w, h = (float(v) for v in vb.split())
    lado = max(w, h) * (1 + folga)
    ox = x - (lado - w) / 2
    oy = y - (lado - h) / 2
    corpo = corpo.replace('fill="currentColor"', f'fill="{cor}"')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{ox:.0f} {oy:.0f} {lado:.0f} {lado:.0f}">'
            f'{corpo}</svg>')


def _rasterizar(svg: str, lado: int, fundo: str | None, destino: Path, escala: float = 1.0) -> None:
    """Rasteriza um SVG num PNG quadrado de `lado` px pelo Chrome headless."""
    tam = round(lado * escala)
    bg = f"background:{fundo};" if fundo else "background:transparent;"
    html = (f"<!doctype html><html><head><style>html,body{{margin:0;width:{lado}px;height:{lado}px;{bg}"
            f"overflow:hidden;display:grid;place-items:center}}svg{{width:{tam}px;height:{tam}px;display:block}}"
            f"</style></head><body>{svg}</body></html>")
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "i.html"
        p.write_text(html, encoding="utf-8")
        shot = Path(tmp) / "i.png"
        args = [str(CHROME), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                f"--window-size={lado},{lado}", "--force-device-scale-factor=1",
                f"--screenshot={shot}", p.as_uri()]
        if not fundo:
            args.insert(2, "--default-background-color=00000000")
        subprocess.run(args, check=True, capture_output=True, timeout=60)
        with Image.open(shot) as im:
            im = im.convert("RGBA")
            if im.size != (lado, lado):
                im = im.crop((0, 0, lado, lado))
            if fundo:
                im = im.convert("RGB")
            destino.parent.mkdir(parents=True, exist_ok=True)
            im.save(destino, "PNG", optimize=True)
    print(f"  + {destino.relative_to(SITE)} {lado}px")


def icones(forcar: bool) -> None:
    # fonte de alta fidelidade (o sprite publicado é a versão leve de tools/svg_leve.py)
    fonte = SITE.parent / "build" / "brand" / "sprite-fonte.svg"
    sprite = (fonte if fonte.exists() else SITE / "assets" / "brand" / "sprite.svg").read_text(encoding="utf-8")
    vb_mk, corpo_mk = _simbolo(sprite, "mk")
    vb_lk, corpo_lk = _simbolo(sprite, "lk")

    fav = SITE / "favicon.svg"
    if forcar or not fav.exists():
        fav.write_text(_svg_quadrado(vb_mk, corpo_mk, TINTA, 0.06), encoding="utf-8")
        print("  + favicon.svg (pesado: rode tools/svg_leve.py depois)")

    gato = _svg_quadrado(vb_mk, corpo_mk, TINTA, 0.0)
    lockup = _svg_quadrado(vb_lk, corpo_lk, TINTA, 0.0)
    alvos = [
        (SITE / "favicon-32.png", 32, None, gato, 0.96),
        (SITE / "apple-touch-icon.png", 180, PAPEL, gato, 0.70),
        (SITE / "assets" / "icons" / "icon-192.png", 192, PAPEL, gato, 0.70),
        (SITE / "assets" / "icons" / "icon-512.png", 512, PAPEL, gato, 0.70),
        (SITE / "assets" / "brand" / "logo-mayaa-512.png", 512, PAPEL, lockup, 1.0),
    ]
    for destino, lado, fundo, svg, escala in alvos:
        if destino.exists() and not forcar:
            print(f"  = {destino.relative_to(SITE)} (já existe)")
            continue
        _rasterizar(svg, lado, fundo, destino, escala)

    man = SITE / "site.webmanifest"
    if forcar or not man.exists():
        man.write_text(json.dumps({
            "name": "MAYAA STUDIO", "short_name": "MAYAA", "lang": "pt-BR",
            "start_url": "/", "display": "browser",
            "theme_color": PAPEL, "background_color": PAPEL,
            "icons": [
                {"src": "/assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
                {"src": "/assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
            ],
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("  + site.webmanifest")


if __name__ == "__main__":
    forcar = "--forcar" in sys.argv
    print("Faixas:")
    bandas(forcar)
    print("Ícones:")
    icones(forcar)
