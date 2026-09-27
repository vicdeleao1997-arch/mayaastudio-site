"""Deriva versões leves das imagens do site (C3 · SPEC §6.5).

Para cada JPG em site/assets/cases/**, site/assets/portfolio/** e site/assets/img/** com largura > 1000 px (≥ 850 px
para o -800; ≥ 600 px só o .webp, como as capas 800×1000)
(exceto og.jpg, *-poster.jpg, *-800.jpg, *-2400.jpg e os órfãos da v1 de §6.7), gera:
  <nome>-800.jpg  (800 px de largura, q80, progressivo, sRGB, sem metadados)
  <nome>.webp     (mesma largura do original, q78)
  <nome>-800.webp (q78)
  cover-320.jpg / cover-320.webp (só as capas dos cases: miniatura da lista numerada da pilar)
`lib/media.picture()` encontra esses irmãos sozinho e monta srcset + <source type="image/webp">.

Idempotente: pula o que já existe e é mais novo que a fonte. Nunca amplia, nunca apaga, nunca mexe no original.

    py build/tools/derive_images.py            # gera o que falta
    py build/tools/derive_images.py --forcar   # refaz tudo
    py build/tools/derive_images.py --seco     # só lista
"""
from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

from PIL import Image, ImageCms

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
PASTAS = ["assets/cases", "assets/portfolio", "assets/img"]
# faixas da home: já saem prontas (-800/-2400/.webp) de tools/bandas_e_icones.py (C1); não mexer
PULA_PASTAS = ("assets/img/bandas/",)
MIN_W = 1000          # -800 (jpg e webp) só acima disto…
MIN_W_WEBP = 600      # …mas o .webp na largura original sai para toda imagem a partir de 600 px (capas 800×1000)
MIN_W_800 = 850       # e o -800 também para as de 850 a 1000 px (stories 900×1600)
W_800 = 800
W_320 = 320           # capas dos cases (cover.jpg) ganham também -320: miniatura da lista da pilar (R1-06)
# órfãos da v1 (SPEC §6.7): não vale a pena gerar derivados de arquivo que nenhuma página usa
ORFAOS = {"assets/portfolio/mel-01.jpg", "assets/portfolio/mel-02.jpg", "assets/portfolio/mel-03.jpg"}


def _pula(p: Path) -> bool:
    n = p.name.lower()
    rel = p.relative_to(SITE).as_posix()
    return (n == "og.jpg" or n.endswith(("-poster.jpg", "-320.jpg", "-800.jpg", "-2400.jpg")) or rel in ORFAOS
            or rel.startswith(PULA_PASTAS))


def _srgb(im: Image.Image) -> Image.Image:
    """Converte para sRGB se a imagem tiver perfil ICC diferente; sempre devolve RGB."""
    icc = im.info.get("icc_profile")
    if icc:
        try:
            src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
            dst = ImageCms.createProfile("sRGB")
            im = ImageCms.profileToProfile(im, src, dst, outputMode="RGB")
        except Exception:
            pass
    return im.convert("RGB")


def _atual(dest: Path, fonte: Path) -> bool:
    return dest.exists() and dest.stat().st_mtime >= fonte.stat().st_mtime


def _grava(im: Image.Image, dest: Path, fmt: str, q: int) -> None:
    tmp = dest.with_name(dest.name + ".tmp")
    if fmt == "JPEG":
        im.save(tmp, "JPEG", quality=q, optimize=True, progressive=True)
    else:
        im.save(tmp, "WEBP", quality=q, method=6)
    tmp.replace(dest)


def candidatos() -> list[Path]:
    out = []
    for pasta in PASTAS:
        base = SITE / pasta
        if not base.exists():
            continue
        for p in sorted(base.rglob("*.jpg")):
            if _pula(p):
                continue
            with Image.open(p) as im:
                if im.size[0] >= MIN_W_WEBP:
                    out.append((p, im.size[0]))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--forcar", action="store_true")
    ap.add_argument("--seco", action="store_true")
    a = ap.parse_args()
    feitos = pulados = 0
    for p, largura in candidatos():
        alvos = {p.with_suffix(".webp"): ("WEBP", 78, False)}
        if largura > MIN_W or largura >= MIN_W_800:
            alvos[p.with_name(p.stem + "-800.jpg")] = ("JPEG", 80, True)
            alvos[p.with_name(p.stem + "-800.webp")] = ("WEBP", 78, True)
        if p.name.lower() == "cover.jpg":
            alvos[p.with_name(p.stem + "-320.jpg")] = ("JPEG", 80, W_320)
            alvos[p.with_name(p.stem + "-320.webp")] = ("WEBP", 78, W_320)
        falta = {d: v for d, v in alvos.items() if a.forcar or not _atual(d, p)}
        rel = p.relative_to(SITE).as_posix()
        if not falta:
            pulados += 1
            continue
        if a.seco:
            print(f"[seco] {rel} → {', '.join(d.name for d in falta)}")
            continue
        with Image.open(p) as im0:
            im = _srgb(im0)
        w, h = im.size
        small = im.resize((W_800, round(h * W_800 / w)), Image.LANCZOS)
        for dest, (fmt, q, reduz) in falta.items():
            if reduz is True:
                alvo = small
            elif reduz:
                alvo = im.resize((reduz, round(h * reduz / w)), Image.LANCZOS)
            else:
                alvo = im
            _grava(alvo, dest, fmt, q)
            feitos += 1
        print(f"ok {rel} ({w}×{h}) → {', '.join(d.name for d in falta)}")
    print(f"derivados gravados: {feitos} · imagens já em dia: {pulados}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
