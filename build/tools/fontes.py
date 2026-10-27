"""Fontes do site hospedadas no próprio domínio (sem Google Fonts: CSS que bloqueava o 1.º paint).

A marca usa Lato em tudo (título, corpo, número, rótulo). Gera em site/assets/fonts/:
  lato-400.woff2   Lato Regular (corpo)
  lato-700.woff2   Lato Bold (títulos, rótulos)
  lato-900.woff2   Lato Black (destaque em título grande, número)
Todas recortadas em latin + latin-ext (+ setas e sinais do site). Licença OFL.

    py build/tools/fontes.py

Fontes de origem: build/fonts/Lato-*.ttf (fora do git) ou C:/Users/vicde/mayaa-leads/assets.
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
OUT = SITE / "assets" / "fonts"
SRC = [ROOT / "build" / "fonts", Path("C:/Users/vicde/mayaa-leads/assets")]

# faixas "latin" e "latin-ext" do Google Fonts + setas e sinais do site
LATIN = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,"
         "U+20AC,U+2122,U+2190-2193,U+2212,U+2215,U+FEFF,U+FFFD")
LATIN_EXT = ("U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,"
             "U+20A0-20AB,U+20AD-20C0,U+2113,U+A720-A7FF")


def faixa(txt: str) -> list[int]:
    out = []
    for part in txt.split(","):
        part = part.strip().replace("U+", "")
        if "-" in part:
            a, b = part.split("-")
            out += range(int(a, 16), int(b, 16) + 1)
        else:
            out.append(int(part, 16))
    return out


def origem(nome: str) -> Path:
    for d in SRC:
        if (d / nome).exists():
            return d / nome
    raise SystemExit(f"fonte não encontrada: {nome} (build/fonts ou mayaa-leads/assets)")


def gera(font: TTFont, unicodes: list[int], dest: Path) -> int:
    opt = subset.Options()
    opt.flavor = "woff2"
    # recursos padrão (kern, liga, locl…) + números tabulares dos rótulos e caixa alta; "*" trazia formas
    # alternativas que o site não usa
    opt.layout_features = opt.layout_features + ["tnum", "lnum", "pnum", "case"]
    opt.name_IDs = [0, 1, 2, 3, 4, 5, 6]
    opt.notdef_outline = True
    opt.hinting = False                   # woff2 menor; o site não depende de hinting
    opt.desubroutinize = True
    sub = subset.Subsetter(opt)
    sub.populate(unicodes=unicodes)
    sub.subset(font)
    dest.parent.mkdir(parents=True, exist_ok=True)
    buf = io.BytesIO()
    subset.save_font(font, buf, opt)
    dest.write_bytes(buf.getvalue())
    return len(buf.getvalue())


def main() -> int:
    base = faixa(LATIN) + faixa(LATIN_EXT)
    for peso, arq in ((400, "Lato-Regular.ttf"), (700, "Lato-Bold.ttf"), (900, "Lato-Black.ttf")):
        n = gera(TTFont(origem(arq)), base, OUT / f"lato-{peso}.woff2")
        print(f"  lato-{peso}.woff2  {n / 1024:6.1f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
