"""Imagens og:image 1200×630 na identidade MAYAA (grupo legal-seo · SPEC §5.2 e §6.5), desenhadas em HTML e
fotografadas pelo Chrome headless.

  py build/tools/og_chrome.py                    gera todas as de §5.2
  py build/tools/og_chrome.py --so mayaa,privacidade

Desenho (§6.5): papel; moldura de 1,5 px em --linha a 20 px da borda; gato + "MAYAA STUDIO" no alto; rótulo em
Archivo espaçado, fumaça; título em Shippori Mincho Bold, até 2 linhas (encolhe sozinho se não couber); embaixo
"mayaastudio.com.br" e "まやー工房" em fumaça. Páginas de texto: o kanji da página em --linha, atrás do título.
Cases e portfólio: imagem à direita em 45% da largura, dentro da moldura. Só papel e tinta (as fotos têm cor própria).
Fontes: build/fonts/*.ttf (cópias de mayaa-leads/assets). Saída JPG q86 progressivo, sem metadados.
"""
from __future__ import annotations

import argparse
import html
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
FONTS = ROOT / "build" / "fonts"
FONTS_ALT = Path("C:/Users/vicde/mayaa-leads/assets")
CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe"
W, H = 1200, 630

# nome · saída · rótulo · linhas do título · kanji · imagens (à direita) · legenda sobre a imagem
OGS = [
    dict(nome="mayaa", out="assets/og/og-mayaa.jpg", label="Tráfego pago com IA · São Paulo",
         lines=["Do conceito", "à conversão."], kanji="間"),
    dict(nome="servicos", out="assets/og/og-servicos.jpg", label="Serviços · 03",
         lines=["Três serviços,", "um estúdio."], kanji="間"),
    dict(nome="servicos-trafego-pago", out="assets/og/og-servicos-trafego-pago.jpg",
         label="Serviço 01 · Tráfego pago e performance",
         lines=["Tráfego pago, lido", "campanha por campanha."], kanji="展"),
    dict(nome="servicos-audiovisual-com-ia", out="assets/og/og-servicos-audiovisual-com-ia.jpg",
         label="Serviço 02 · Audiovisual com IA", lines=["Audiovisual com IA,", "com direção."], kanji="創"),
    dict(nome="servicos-marketing", out="assets/og/og-servicos-marketing.jpg", label="Serviço 03 · Marketing",
         lines=["O clique precisa chegar", "a algum lugar."], kanji="築"),
    dict(nome="trafego-pago-com-ia", out="assets/og/og-trafego-pago-com-ia.jpg",
         label="Guia · Tráfego pago com IA", lines=["Tráfego pago", "com IA."], kanji="知"),
    dict(nome="privacidade", out="assets/og/og-privacidade.jpg", label="LGPD · Lei 13.709/2018",
         lines=["Política de", "privacidade."], kanji=None),
    dict(nome="portfolio", out="assets/og/og-portfolio.jpg", label="Portfólio · 04 cases",
         lines=["Trabalhos", "do estúdio."],
         imgs=["assets/cases/bvba-surrealismo/cover.jpg", "assets/cases/alumee-vela-mel/cover.jpg"]),
    dict(nome="bvba", out="assets/cases/bvba-surrealismo/og.jpg", label="Case 01 · Moda",
         lines=["BVBA Supply ·", "O surrealismo."], imgs=["assets/cases/bvba-surrealismo/ensaio-03.jpg"]),
    dict(nome="alumee", out="assets/cases/alumee-vela-mel/og.jpg", label="Case 02 · Velas artesanais",
         lines=["Alumee", "vela Mel."], imgs=["assets/cases/alumee-vela-mel/mel-01.jpg"]),
    dict(nome="ana", out="assets/cases/ana-lauren-modelo-ia/og.jpg", label="Case 03 · Criativo para anúncio",
         lines=["Ana Lauren", "é 100% IA."], imgs=["assets/portfolio/ana-02.jpg"],
         cap="100% IA · Nenhuma pessoa real nestas fotos"),
    dict(nome="iose", out="assets/cases/iose-trafego-pago/og.jpg", label="Case 04 · Educação técnica",
         lines=["IOSE", "tráfego pago."], imgs=["assets/cases/iose-trafego-pago/feed-linhas.jpg"]),
]


def font_url(name: str) -> str:
    p = FONTS / name if (FONTS / name).exists() else FONTS_ALT / name
    if not p.exists():
        raise SystemExit(f"fonte não encontrada: {name} (build/fonts ou mayaa-leads/assets)")
    return p.resolve().as_uri()


def mark_url() -> str:
    """Gato em traço. site/assets/mayaa-mark-ink.png não é referenciado por página nenhuma (o build o lista como
    órfão); se sair do site, usa a cópia de mayaa-leads/assets."""
    for p in (SITE / "assets/mayaa-mark-ink.png", FONTS_ALT / "mayaa-mark-ink.png"):
        if p.exists():
            return p.resolve().as_uri()
    raise SystemExit("gato não encontrado: site/assets/mayaa-mark-ink.png ou mayaa-leads/assets/mayaa-mark-ink.png")


def page_html(o: dict) -> str:
    e = html.escape
    imgs = o.get("imgs") or []
    for i in imgs:
        if not (SITE / i).exists():
            raise SystemExit(f"imagem não encontrada: site/{i}")
    title = "".join(f'<span class="ln">{e(l)}</span>' for l in o["lines"])
    kanji = f'<div class="kanji" aria-hidden="true">{e(o["kanji"])}</div>' if o.get("kanji") else ""
    media = ""
    if imgs:
        cells = "".join(f'<div class="cell" style="background-image:url(\'{(SITE / i).resolve().as_uri()}\')"></div>'
                        for i in imgs)
        cap = f'<p class="cap">{e(o["cap"])}</p>' if o.get("cap") else ""
        media = f'<div class="media n{len(imgs)}">{cells}{cap}</div>'
    textw = 560 if imgs else 1000
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>
@font-face{{font-family:"Shippori Mincho";font-weight:400;src:url("{font_url('Shippori-Regular.ttf')}")}}
@font-face{{font-family:"Shippori Mincho";font-weight:700;src:url("{font_url('Shippori-Bold.ttf')}")}}
@font-face{{font-family:"Archivo";font-weight:100 900;src:url("{font_url('Archivo.ttf')}")}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#F6F4EF;color:#0B0B0B}}
body{{position:relative;font-family:"Archivo",sans-serif;-webkit-font-smoothing:antialiased}}
.frame{{position:absolute;inset:20px;border:1.5px solid #DAD5CB;z-index:5;pointer-events:none}}
.kanji{{position:absolute;right:92px;top:50%;transform:translateY(-52%);font:400 420px/1 "Shippori Mincho",serif;
  color:#DAD5CB;z-index:1}}
.brand{{position:absolute;left:60px;top:52px;display:flex;align-items:center;gap:16px;z-index:3}}
.brand img{{width:56px;height:56px}}
.brand span{{font:500 17px/1 "Archivo",sans-serif;letter-spacing:.2em;text-transform:uppercase}}
.body{{position:absolute;left:60px;bottom:128px;width:{textw}px;z-index:3}}
.label{{font:500 19px/1.35 "Archivo",sans-serif;letter-spacing:.2em;text-transform:uppercase;color:#6B6864;
  margin-bottom:26px}}
h1{{font:700 76px/1.06 "Shippori Mincho",serif;letter-spacing:-.01em;color:#0B0B0B}}
h1 .ln{{display:block;white-space:nowrap}}
.foot{{position:absolute;left:60px;right:60px;bottom:50px;display:flex;justify-content:space-between;
  align-items:baseline;color:#6B6864;z-index:3}}
.foot .url{{font:400 18px/1 "Archivo",sans-serif;letter-spacing:.04em}}
.foot .kana{{font:400 20px/1 "Shippori Mincho",serif;letter-spacing:.18em}}
.has-media .foot{{right:auto;width:{textw}px}}
.media{{position:absolute;top:20px;right:20px;bottom:20px;width:{round(W * .45)}px;display:flex;gap:10px;
  z-index:2;background:#F6F4EF}}
.cell{{flex:1;background-size:cover;background-position:50% 40%}}
.cap{{position:absolute;left:0;bottom:0;background:#F6F4EF;color:#0B0B0B;padding:14px 18px 12px;
  font:500 14px/1.3 "Archivo",sans-serif;letter-spacing:.16em;text-transform:uppercase}}
</style></head><body class="{'has-media' if imgs else ''}">
<div class="frame"></div>{kanji}{media}
<div class="brand"><img src="{mark_url()}" alt=""><span>MAYAA STUDIO</span></div>
<div class="body"><p class="label">{e(o['label'])}</p><h1 id="t">{title}</h1></div>
<div class="foot"><span class="url">mayaastudio.com.br</span><span class="kana">まやー工房</span></div>
<script>
document.fonts.ready.then(function(){{
  var t=document.getElementById('t'), max={textw}, fs=76;
  function wide(){{return Array.prototype.some.call(t.children,function(l){{return l.scrollWidth>max;}});}}
  while(wide() && fs>50){{fs-=2; t.style.fontSize=fs+'px';}}
  document.body.setAttribute('data-ok','1');
}});
</script></body></html>"""


def shoot(o: dict, tmp: Path) -> Path:
    src = tmp / f"og-{o['nome']}.html"
    png = tmp / f"og-{o['nome']}.png"
    src.write_text(page_html(o), encoding="utf-8")
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--mute-audio",
           "--allow-file-access-from-files", "--force-device-scale-factor=1", "--run-all-compositor-stages-before-draw",
           "--virtual-time-budget=6000", f"--window-size={W},{H}", f"--screenshot={png}", src.resolve().as_uri()]
    subprocess.run(cmd, check=True, capture_output=True, timeout=120)
    if not png.exists():
        raise SystemExit(f"o Chrome não gerou {png}")
    return png


def main() -> int:
    ap = argparse.ArgumentParser(description="Gera as og:image 1200×630 (§5.2) com o Chrome headless")
    ap.add_argument("--so", default="", help="nomes separados por vírgula (ex.: mayaa,privacidade)")
    a = ap.parse_args()
    so = {x.strip() for x in a.so.split(",") if x.strip()}
    alvo = [o for o in OGS if not so or o["nome"] in so]
    if so - {o["nome"] for o in OGS}:
        raise SystemExit(f"nome desconhecido: {sorted(so - {o['nome'] for o in OGS})}")
    with tempfile.TemporaryDirectory(prefix="og-") as t:
        tmp = Path(t)
        for o in alvo:
            png = shoot(o, tmp)
            im = Image.open(png).convert("RGB")
            if im.size != (W, H):
                im = im.crop((0, 0, W, H))
            dest = SITE / o["out"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            part = dest.with_suffix(".tmp.jpg")
            im.save(part, "JPEG", quality=86, progressive=True, optimize=True)
            part.replace(dest)
            print(f"  {o['out']:<48} {dest.stat().st_size / 1024:6.1f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
