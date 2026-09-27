"""Versões leves do gato (sprite do cabeçalho/rodapé e favicon).

O traço vetorizado original tem ~100 caminhos com curvas em 6 casas decimais: sprite.svg com 115 KB e favicon.svg
com 39 KB, baixados em toda página por causa de um gato de 32 px no cabeçalho. Aqui cada curva vira uma poligonal
simplificada (Ramer-Douglas-Peucker) com tolerância abaixo de 1/4 de pixel no tamanho em que o símbolo aparece,
coordenadas inteiras e relativas. Detalhes menores que meio pixel (poeira do vetor) saem do gato pequeno: é o que
virava ruído dentro do círculo a 26 px.

Fonte (alta fidelidade, não publicada): build/brand/sprite-fonte.svg e build/brand/favicon-fonte.svg
(copiadas de site/ na 1.ª execução). tools/bandas_e_icones.py rasteriza os PNG grandes a partir da fonte.

    py build/tools/svg_leve.py
"""
from __future__ import annotations

import math
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
FONTE = ROOT / "build" / "brand"

# símbolo → (tolerância em unidades do viewBox, menor detalhe mantido em unidades)
#   mk: gato do cabeçalho/menu, 32 px para 1584 unidades (≈ 50 un/px) → 8 un ≈ 0,16 px; some o que tem < 25 un (0,5 px)
#   lk: marca do rodapé, 140 px para 2130 unidades (≈ 15 un/px) → 3 un ≈ 0,2 px
#   favicon: 16 a 64 px para 1679 unidades (≥ 26 un/px) → 5 un ≈ 0,2 px a 64 px
AJUSTE = {"mk": (8.0, 25.0), "lk": (3.0, 0.0), "favicon": (5.0, 12.0)}

NUM = re.compile(r"-?\d*\.?\d+(?:[eE][-+]?\d+)?")


def _subpaths(d: str, tx: float, ty: float):
    """Converte um d com M/C/Z absolutos (o que o vetorizador gera) em listas de pontos, já com o translate."""
    toks = re.findall(r"[MCLZmclz]|-?\d*\.?\d+(?:[eE][-+]?\d+)?", d)
    i, cmd, cur, start = 0, None, (0.0, 0.0), (0.0, 0.0)
    subs, pts = [], []
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t
            i += 1
            if cmd in "Zz":
                if pts:
                    subs.append(pts)
                pts, cur = [], start
            continue
        if cmd == "M":
            cur = (float(toks[i]) + tx, float(toks[i + 1]) + ty)
            start = cur
            if pts:
                subs.append(pts)
            pts = [cur]
            i += 2
            cmd = "L"
        elif cmd == "L":
            cur = (float(toks[i]) + tx, float(toks[i + 1]) + ty)
            pts.append(cur)
            i += 2
        elif cmd == "C":
            c1 = (float(toks[i]) + tx, float(toks[i + 1]) + ty)
            c2 = (float(toks[i + 2]) + tx, float(toks[i + 3]) + ty)
            p3 = (float(toks[i + 4]) + tx, float(toks[i + 5]) + ty)
            est = math.dist(cur, c1) + math.dist(c1, c2) + math.dist(c2, p3)
            n = max(2, min(64, math.ceil(est / 2.0)))
            for k in range(1, n + 1):
                u = k / n
                a, b, c_, e = (1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u ** 3
                pts.append((a * cur[0] + b * c1[0] + c_ * c2[0] + e * p3[0],
                            a * cur[1] + b * c1[1] + c_ * c2[1] + e * p3[1]))
            cur = p3
            i += 6
        else:
            raise ValueError(f"comando não suportado: {cmd}")
    if pts:
        subs.append(pts)
    return subs


def _rdp(pts, tol):
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        (x1, y1), (x2, y2) = pts[a], pts[b]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1e-9
        best, idx = -1.0, -1
        for k in range(a + 1, b):
            x0, y0 = pts[k]
            dist = abs(dy * x0 - dx * y0 + x2 * y1 - y2 * x1) / L if L > 1e-9 else math.dist(pts[k], pts[a])
            if dist > best:
                best, idx = dist, k
        if best > tol and idx > 0:
            keep[idx] = True
            stack += [(a, idx), (idx, b)]
    return [p for p, k in zip(pts, keep) if k]


def _fmt(nums) -> str:
    return " ".join(str(n) for n in nums).replace(" -", "-")


def _d(subs, tol, minimo) -> str:
    out = []
    for pts in subs:
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        if minimo and math.hypot(max(xs) - min(xs), max(ys) - min(ys)) < minimo:
            continue
        s = _rdp(pts + [pts[0]], tol)[:-1]
        q = [(round(x), round(y)) for x, y in s]
        q = [p for i, p in enumerate(q) if i == 0 or p != q[i - 1]]
        if len(q) < 3:
            continue
        rel = []
        for (x0, y0), (x1, y1) in zip(q, q[1:]):
            rel += [x1 - x0, y1 - y0]
        out.append(f"M{_fmt(q[0])}l{_fmt(rel)}z")
    return "".join(out)


def _caminhos(corpo: str, tol: float, minimo: float, fill: str) -> str:
    paths = []
    for m in re.finditer(r'<path d="([^"]+)"[^>]*?transform="translate\(([-\d.]+),([-\d.]+)\)"[^>]*/>', corpo):
        d = _d(_subpaths(m.group(1), float(m.group(2)), float(m.group(3))), tol, minimo)
        if d:
            paths.append(f'<path d="{d}"/>')
    return f'<g fill="{fill}">{"".join(paths)}</g>'


def main() -> int:
    FONTE.mkdir(parents=True, exist_ok=True)
    for nome, publicado in (("sprite-fonte.svg", SITE / "assets/brand/sprite.svg"), ("favicon-fonte.svg", SITE / "favicon.svg")):
        if not (FONTE / nome).exists():
            shutil.copy2(publicado, FONTE / nome)
            print(f"  fonte guardada: build/brand/{nome}")

    sprite = (FONTE / "sprite-fonte.svg").read_text(encoding="utf-8")
    simbolos = []
    for m in re.finditer(r'<symbol id="(\w+)" viewBox="([^"]+)">(.*?)</symbol>', sprite, re.S):
        sid, vb, corpo = m.groups()
        tol, minimo = AJUSTE.get(sid, (3.0, 0.0))
        simbolos.append(f'<symbol id="{sid}" viewBox="{vb}">{_caminhos(corpo, tol, minimo, "currentColor")}</symbol>')
    out = '<svg xmlns="http://www.w3.org/2000/svg">' + "".join(simbolos) + "</svg>\n"
    dest = SITE / "assets/brand/sprite.svg"
    dest.write_text(out, encoding="utf-8")
    print(f"  sprite.svg  {len(sprite.encode()) / 1024:6.1f} KB → {len(out.encode()) / 1024:5.1f} KB")

    fav = (FONTE / "favicon-fonte.svg").read_text(encoding="utf-8")
    vb = re.search(r'viewBox="([^"]+)"', fav).group(1)
    fill = re.search(r'fill="(#[0-9A-Fa-f]{6})"', fav).group(1)
    tol, minimo = AJUSTE["favicon"]
    out = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{_caminhos(fav, tol, minimo, fill)}</svg>\n'
    (SITE / "favicon.svg").write_text(out, encoding="utf-8")
    print(f"  favicon.svg {len(fav.encode()) / 1024:6.1f} KB → {len(out.encode()) / 1024:5.1f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
