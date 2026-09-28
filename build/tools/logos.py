"""Logos de clientes em tinta, no tamanho em que aparecem (faixa da home e parede do portfólio).

Antes: PNGs coloridos de 160 px de altura (284 KB no total) exibidos a 26 a 72 px, com filtro de cinza no CSS:
as partes claras dos logos viravam cinza claro e quase sumiam, e os pretos pesavam.

Agora, para cada site/assets/clients/<nome>.png (fonte, não é alterada):
  1. tinta = opacidade × escuridão do pixel (fundo branco e caixas brancas somem);
  2. o que fica abaixo de 12% de tinta vira transparente (sobras de recorte);
  3. normaliza: o percentil 95 da tinta vira tinta cheia (todo logo com o mesmo preto);
  4. recorte (RECORTE) e aparo das margens vazias;
  5. altura final = 2× a maior altura exibida (faixa 34 px × k, parede 40 px × k), WebP sem perdas.
Saída: site/assets/clients/tinta/<nome>.webp · cor #0B0B0B com transparência.

    py build/tools/logos.py
"""
from __future__ import annotations

import io
import math
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "build"))
from lib import dados  # noqa: E402
from pages.portfolio import ESCALA_PAREDE  # noqa: E402

SRC = ROOT / "site" / "assets" / "clients"
OUT = SRC / "tinta"
TINTA = (11, 11, 11)
# O Setor Elétrico: sai o "REVISTA" vertical, a serpentina e os fios (amarelo e vermelho) que viravam traço solto
RECORTE = {"osetor.png": (22, 4, 1187, 137)}
LIMIAR = 0.12


def tinta(im: Image.Image) -> Image.Image:
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    ink = [[0.0] * w for _ in range(h)]
    vals = []
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            v = (a / 255) * (1 - lum)
            v = 0.0 if v < LIMIAR else v
            ink[y][x] = v
            if v:
                vals.append(v)
    vals.sort()
    p95 = vals[int(len(vals) * 0.95)] if vals else 1.0
    out = Image.new("RGBA", (w, h), TINTA + (0,))
    op = out.load()
    for y in range(h):
        for x in range(w):
            v = ink[y][x]
            if v:
                op[x, y] = TINTA + (min(255, round(255 * min(1.0, v / p95))),)
    bbox = out.getchannel("A").getbbox()
    return out.crop(bbox) if bbox else out


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    for arq, _alt, k in dados.CLIENT_LOGOS:
        nome = Path(arq).stem + ".png"
        im = Image.open(SRC / nome)
        if nome in RECORTE:
            im = im.crop(RECORTE[nome])
        im = tinta(im)
        exibida = max(34 * k, 40 * ESCALA_PAREDE.get(Path(arq).stem, k))
        alvo = math.ceil(2 * exibida)
        if im.height > alvo:
            im = im.resize((round(im.width * alvo / im.height), alvo), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "WEBP", lossless=True, quality=100, method=6)
        dest = OUT / (Path(arq).stem + ".webp")
        dest.write_bytes(buf.getvalue())
        total += len(buf.getvalue())
        print(f"  {dest.name:<18} {im.width:>4}×{im.height:<4} {len(buf.getvalue()) / 1024:5.1f} KB")
    print(f"  total {total / 1024:.1f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
