"""ALTERNATIVO · o gerador oficial é tools/og_chrome.py (integração 27/09/2026). Só roda com --alternativo.

Imagens de compartilhamento 1200×630 (C3 · SPEC §6.5 e §5.2).

Desenho único, papel e tinta: fundo papel; moldura de 1,5 px em --linha a 20 px da borda (passe-partout);
no alto à esquerda o gato + "MAYAA STUDIO" (Archivo espaçado); rótulo em Archivo 20 px espaçado, fumaça;
título em Shippori Bold até 76 px, no máximo 2 linhas (reduz até caber); embaixo "mayaastudio.com.br" e "まやー工房".
- Home, serviços, pilar e privacidade: o kanji da página em Shippori 420 px, cor --linha, à direita.
- Cases e portfólio: imagem à direita em 45% da largura, altura total, sob a moldura.

    py build/tools/og.py            # gera todas
    py build/tools/og.py --only alumee-vela-mel,og-portfolio
    py build/tools/og.py --prova <arquivo.png>   # também grava uma folha de conferência com todas (fora de site/)

Sobrescreve os og da v1 com os mesmos nomes. Nenhum travessão em texto; nada de número de conta.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
FONTS = ROOT / "build" / "fonts"
FONTS_ALT = Path("C:/Users/vicde/mayaa-leads/assets")   # mesma origem das cópias de build/fonts

W, H = 1200, 630
PAPEL, CARTAO, LINHA, FUMACA, TINTA = "#F6F4EF", "#EEEBE4", "#DAD5CB", "#6B6864", "#0B0B0B"
FRAME_IN = 20          # a moldura fica a 20 px da borda
PAD = 64               # margem do texto
IMG_W = round(W * .45)  # 540 px de imagem à direita

# chave → (arquivo de saída, rótulo, linhas do título, kanji | imagens)
OG = {
    "og-mayaa": dict(out="assets/og/og-mayaa.jpg", label="Tráfego pago com IA · São Paulo",
                     lines=["Do conceito", "à conversão."], kanji="間"),
    "og-servicos": dict(out="assets/og/og-servicos.jpg", label="Serviços · 03",
                        lines=["Três serviços,", "um estúdio."], kanji="間"),
    "og-servicos-trafego-pago": dict(out="assets/og/og-servicos-trafego-pago.jpg",
                                     label="Serviço 01 · Tráfego pago e performance",
                                     lines=["Tráfego pago, lido", "campanha por campanha."], kanji="展"),
    "og-servicos-audiovisual-com-ia": dict(out="assets/og/og-servicos-audiovisual-com-ia.jpg",
                                           label="Serviço 02 · Audiovisual com IA",
                                           lines=["Audiovisual com IA,", "com direção."], kanji="創"),
    "og-servicos-marketing": dict(out="assets/og/og-servicos-marketing.jpg", label="Serviço 03 · Marketing",
                                  lines=["O clique precisa", "chegar a algum lugar."], kanji="築"),
    "og-trafego-pago-com-ia": dict(out="assets/og/og-trafego-pago-com-ia.jpg", label="Guia · Tráfego pago com IA",
                                   lines=["Tráfego pago", "com IA."], kanji="知"),
    "og-privacidade": dict(out="assets/og/og-privacidade.jpg", label="LGPD · Lei 13.709/2018",
                           lines=["Política de", "privacidade."], kanji="間"),
    "og-portfolio": dict(out="assets/og/og-portfolio.jpg", label="Portfólio · 04 cases",
                         lines=["Trabalhos", "do estúdio."],
                         imgs=[("assets/cases/bvba-surrealismo/cover.jpg", (.5, .5)),
                               ("assets/cases/alumee-vela-mel/cover.jpg", (.5, .5))]),
    "bvba-surrealismo": dict(out="assets/cases/bvba-surrealismo/og.jpg", label="Case 01 · Moda · Audiovisual com IA",
                             lines=["BVBA Supply ·", "O surrealismo."],
                             imgs=[("assets/cases/bvba-surrealismo/ensaio-03.jpg", (.5, .45))]),
    "alumee-vela-mel": dict(out="assets/cases/alumee-vela-mel/og.jpg",
                            label="Case 02 · Velas artesanais · Audiovisual com IA",
                            lines=["Alumee", "vela Mel."],
                            imgs=[("assets/cases/alumee-vela-mel/mel-01.jpg", (.5, .5))]),
    "ana-lauren-modelo-ia": dict(out="assets/cases/ana-lauren-modelo-ia/og.jpg", label="Case 03 · IA · Modelo sintética",
                                 lines=["Ana Lauren", "é 100% IA."],
                                 imgs=[("assets/portfolio/ana-02.jpg", (.5, .35))],
                                 tag="100% IA · Nenhuma pessoa real nestas fotos"),
    "iose-trafego-pago": dict(out="assets/cases/iose-trafego-pago/og.jpg",
                              label="Case 04 · Educação técnica · Tráfego pago",
                              lines=["IOSE", "tráfego pago."],
                              # peça com texto: inteira (sem recorte), sobre cartão
                              imgs=[("assets/cases/iose-trafego-pago/feed-linhas.jpg", "contain")]),
}


# ── fontes ───────────────────────────────────────────────────────────────────
def _fonte(nome: str) -> Path:
    for base in (FONTS, FONTS_ALT):
        p = base / nome
        if p.exists():
            return p
    raise SystemExit(f"fonte ausente: {nome} (copie de {FONTS_ALT} para {FONTS})")


def shippori(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(_fonte("Shippori-Bold.ttf" if bold else "Shippori-Regular.ttf")), size)


def archivo(size: int, weight: int = 500) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(str(_fonte("Archivo.ttf")), size)
    try:
        f.set_variation_by_axes([weight, 100])
    except Exception:
        pass
    return f


# ── desenho ──────────────────────────────────────────────────────────────────
def tracked_width(font, text: str, track: float) -> float:
    return sum(font.getlength(ch) for ch in text) + track * font.size * max(len(text) - 1, 0)


def draw_tracked(d: ImageDraw.ImageDraw, xy, text: str, font, fill, track: float) -> None:
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += font.getlength(ch) + track * font.size


def wrap_label(font, text: str, maxw: float, track: float) -> list[str]:
    words, lines, cur = text.upper().split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tracked_width(font, t, track) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def fit_title(lines: list[str], maxw: float, start: int = 76, minimo: int = 48):
    size = start
    while size > minimo:
        f = shippori(size, bold=True)
        if all(f.getlength(l) <= maxw for l in lines):
            return f
        size -= 2
    return shippori(minimo, bold=True)


def cover(im: Image.Image, w: int, h: int, focus=(.5, .5)) -> Image.Image:
    return ImageOps.fit(im.convert("RGB"), (w, h), Image.LANCZOS, centering=focus)


def render(key: str) -> Image.Image:
    cfg = OG[key]
    im = Image.new("RGB", (W, H), PAPEL)
    d = ImageDraw.Draw(im)
    imgs = cfg.get("imgs")
    text_right = W - PAD

    # imagem à direita (cases e portfólio), altura total, sob a moldura
    if imgs:
        x0 = W - IMG_W
        text_right = x0 - 48
        if len(imgs) == 1 and imgs[0][1] == "contain":
            d.rectangle([x0, 0, W, H], fill=CARTAO)
            src = Image.open(SITE / imgs[0][0]).convert("RGB")
            lado = min(IMG_W - 2 * 56, H - 2 * 64)
            pc = src.resize((lado, round(src.height * lado / src.width)), Image.LANCZOS)
            im.paste(pc, (x0 + (IMG_W - pc.width) // 2, (H - pc.height) // 2))
        else:
            n = len(imgs)
            gap = 4
            each = (IMG_W - gap * (n - 1)) // n
            x = x0
            for i, (path, focus) in enumerate(imgs):
                wi = each if i < n - 1 else W - x
                im.paste(cover(Image.open(SITE / path), wi, H, focus), (x, 0))
                x += wi + gap
        if cfg.get("tag"):
            tr = .14
            t = cfg["tag"].upper()
            caixa = IMG_W - 32 - FRAME_IN - 24 - 36          # largura útil do selo dentro da imagem
            tam = 15
            while tam > 10 and tracked_width(archivo(tam, 600), t, tr) > caixa:
                tam -= 1
            f = archivo(tam, 600)
            tw = tracked_width(f, t, tr)
            bx0, by1 = x0 + 32, H - FRAME_IN - 28
            bx1, by0 = bx0 + tw + 36, by1 - 44
            d.rectangle([bx0, by0, bx1, by1], fill=PAPEL, outline=TINTA, width=1)
            draw_tracked(d, (bx0 + 18, by0 + (44 - tam) // 2 - 2), t, f, TINTA, tr)

    # kanji grande em --linha, à direita (serviços, pilar, home, privacidade)
    if cfg.get("kanji"):
        fk = shippori(420)
        bb = d.textbbox((0, 0), cfg["kanji"], font=fk)
        kw, kh = bb[2] - bb[0], bb[3] - bb[1]
        kx = W - PAD - kw - bb[0] + 8
        ky = (H - kh) // 2 - bb[1] + 10
        d.text((kx, ky), cfg["kanji"], font=fk, fill=LINHA)

    # passe-partout: margem de papel + fio de 1,5 px em --linha (por cima da imagem, como no site)
    d.rectangle([0, 0, W, FRAME_IN - 1], fill=PAPEL)
    d.rectangle([0, H - FRAME_IN, W, H], fill=PAPEL)
    d.rectangle([0, 0, FRAME_IN - 1, H], fill=PAPEL)
    d.rectangle([W - FRAME_IN, 0, W, H], fill=PAPEL)
    big = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
    ImageDraw.Draw(big).rectangle([FRAME_IN * 2, FRAME_IN * 2, (W - FRAME_IN) * 2 - 1, (H - FRAME_IN) * 2 - 1],
                                  outline=LINHA, width=3)
    im.paste(big.resize((W, H), Image.LANCZOS), (0, 0), big.resize((W, H), Image.LANCZOS))
    d = ImageDraw.Draw(im)

    # marca: gato + MAYAA STUDIO
    mark = Image.open(SITE / "assets/mayaa-mark-ink.png").convert("RGBA")
    mark = mark.resize((56, round(mark.height * 56 / mark.width)), Image.LANCZOS)
    im.paste(mark, (PAD, 52), mark)
    fb = archivo(19, 600)
    draw_tracked(d, (PAD + 56 + 16, 52 + (mark.height - 19) // 2 - 2), "MAYAA STUDIO", fb, TINTA, .18)

    # rótulo + título, alinhados pela base
    maxw = text_right - PAD
    if cfg.get("kanji"):
        maxw = 900   # o título pode passar por cima do kanji (fundo em --linha), sem cobri-lo inteiro
    fl = archivo(20, 500)
    lab = wrap_label(fl, cfg["label"], maxw, .2)
    ft = fit_title(cfg["lines"], maxw)
    lh = round(ft.size * 1.08)
    base_title = 470 if len(lab) == 1 else 480
    y_title0 = base_title - lh * len(cfg["lines"])
    y_lab = y_title0 - 30 - 30 * len(lab)
    for i, l in enumerate(lab):
        draw_tracked(d, (PAD, y_lab + i * 30), l, fl, FUMACA, .2)
    for i, l in enumerate(cfg["lines"]):
        d.text((PAD, y_title0 + i * lh), l, font=ft, fill=TINTA)

    # rodapé: endereço à esquerda, まやー工房 à direita (da coluna de texto)
    fu = archivo(18, 500)
    yb = H - FRAME_IN - 52
    draw_tracked(d, (PAD, yb), "mayaastudio.com.br", fu, FUMACA, .04)
    fk2 = shippori(22)
    kana = "まやー工房"
    d.text((text_right - fk2.getlength(kana), yb - 3), kana, font=fk2, fill=FUMACA)
    # fio fino acima do rodapé
    d.line([(PAD, yb - 22), (text_right, yb - 22)], fill=LINHA, width=1)
    return im


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--prova", default="")
    a = ap.parse_args()
    keys = [k for k in OG if not a.only or k in a.only.split(",")]
    feitos = []
    for k in keys:
        out = SITE / OG[k]["out"]
        out.parent.mkdir(parents=True, exist_ok=True)
        im = render(k)
        tmp = out.with_name(out.name + ".tmp")
        im.save(tmp, "JPEG", quality=86, optimize=True, progressive=True)
        tmp.replace(out)
        feitos.append((k, im))
        print(f"ok {OG[k]['out']} ({out.stat().st_size // 1024} KB)")
    if a.prova and feitos:
        cols = 3
        tw, th = 600, 315
        rows = (len(feitos) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * (tw + 10) + 10, rows * (th + 10) + 10), "#888")
        for i, (_k, im) in enumerate(feitos):
            sheet.paste(im.resize((tw, th), Image.LANCZOS), (10 + (i % cols) * (tw + 10), 10 + (i // cols) * (th + 10)))
        p = Path(a.prova)
        sheet.save(p)
        print(p)
    return 0


if __name__ == "__main__":
    # alternativo desde a integração de 27/09/2026: o oficial é tools/og_chrome.py (mesmos nomes de saída)
    if "--alternativo" not in sys.argv:
        raise SystemExit("Gerador og ALTERNATIVO (Pillow). O oficial é build/tools/og_chrome.py; os dois gravam "
                         "os mesmos arquivos. Para rodar este mesmo assim: --alternativo")
    sys.argv.remove("--alternativo")
    sys.exit(main())
