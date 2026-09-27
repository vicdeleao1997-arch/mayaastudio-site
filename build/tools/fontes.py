"""Fontes do site hospedadas no próprio domínio (sai o Google Fonts: CSS de 60 KB que bloqueava o 1.º paint e
5 a 11 fatias japonesas da Shippori só para uns 11 glifos).

Gera em site/assets/fonts/:
  archivo.woff2       Archivo variável, eixo wght 400 a 600 (largura fixa em 100), latin + latin-ext
  shippori-400.woff2  Shippori Mincho Regular, latin + latin-ext + os glifos japoneses usados no site
  shippori-700.woff2  Shippori Mincho Bold, idem

Os glifos japoneses saem de uma varredura de site/**/*.html (mais a prancha: 間 創 築 展 磨 知 e まやー工房).
Kanji novo numa página → rodar de novo. O check [16] do build acusa glifo japonês que não está na fonte.

    py build/tools/fontes.py          # gera (sobrescreve)
    py build/tools/fontes.py --seco   # só mostra os glifos japoneses encontrados

Fontes de origem: build/fonts/*.ttf (fora do git) ou C:/Users/vicde/mayaa-leads/assets.
"""
from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
OUT = SITE / "assets" / "fonts"
SRC = [ROOT / "build" / "fonts", Path("C:/Users/vicde/mayaa-leads/assets")]

PRANCHA = "間創築展磨知まやー工房"
# faixas "latin" e "latin-ext" do Google Fonts (as mesmas que o site usava) + setas e sinais do site
LATIN = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,"
         "U+20AC,U+2122,U+2190-2193,U+2212,U+2215,U+FEFF,U+FFFD")
LATIN_EXT = ("U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,"
             "U+20A0-20AB,U+20AD-20C0,U+2113,U+A720-A7FF")


def eh_japones(ch: str) -> bool:
    o = ord(ch)
    return 0x3000 <= o <= 0x30FF or 0x3400 <= o <= 0x9FFF or 0xFF00 <= o <= 0xFFEF


def glifos_japoneses() -> str:
    achados = set(PRANCHA)
    for f in SITE.rglob("*.html"):
        achados |= {c for c in f.read_text(encoding="utf-8", errors="ignore") if eh_japones(c)}
    return "".join(sorted(achados))


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
    # alternativas que o site não usa (+25% na Shippori)
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
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--seco", action="store_true")
    a = ap.parse_args()
    jp = glifos_japoneses()
    print("glifos japoneses:", " ".join(jp))
    if a.seco:
        return 0
    base = faixa(LATIN) + faixa(LATIN_EXT)
    com_jp = base + [ord(c) for c in jp]

    arch = TTFont(origem("Archivo.ttf"))
    arch = instancer.instantiateVariableFont(arch, {"wght": (400, 600), "wdth": 100})
    tmp = io.BytesIO()
    arch.save(tmp)                        # recompila antes do subset (o instanciador deixa tabelas preguiçosas)
    tmp.seek(0)
    arch = TTFont(tmp)
    n = gera(arch, base, OUT / "archivo.woff2")
    print(f"  archivo.woff2       {n / 1024:6.1f} KB (wght 400 a 600)")
    for peso, arq in ((400, "Shippori-Regular.ttf"), (700, "Shippori-Bold.ttf")):
        n = gera(TTFont(origem(arq)), com_jp, OUT / f"shippori-{peso}.woff2")
        print(f"  shippori-{peso}.woff2  {n / 1024:6.1f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
