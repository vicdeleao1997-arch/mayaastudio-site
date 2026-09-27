"""Atalho do IndexNow com conferência local (grupo legal-seo). O envio de verdade é o de tools/indexnow.py.

  py build/indexnow.py --dry-run     confere chave, arquivo da chave e sitemap, e mostra o POST (não envia nada)
  py build/indexnow.py               mesma conferência e, se tudo bater, chama tools/indexnow.py (confere a chave
                                     no ar e faz o POST). SÓ DEPOIS DE PUBLICADO E COM O OK DO VICTOR.

POST https://api.indexnow.org/indexnow com {"host", "key", "keyLocation", "urlList"} (URLs do site/sitemap.xml).
Sucesso = HTTP 200 ou 202. A chave fica em lib/config.py (INDEXNOW_KEY) e é publicada pelo build em site/<chave>.txt.
O Google não usa IndexNow: o passo a passo do Search Console está no SPEC §7.3.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parent
sys.path.insert(0, str(BUILD))

from lib import config  # noqa: E402
from tools import indexnow as envio  # noqa: E402


def conferir() -> tuple[dict, list[str]]:
    """Monta o payload e devolve (payload, problemas). Nada sai da máquina aqui."""
    problemas = []
    key = config.INDEXNOW_KEY
    if not re.fullmatch(r"[0-9a-f]{32}", key or ""):
        problemas.append(f"chave fora do formato (32 caracteres hex): {key!r}")
    arq = config.SITE / f"{key}.txt"
    if not arq.exists():
        problemas.append(f"falta o arquivo da chave: site/{key}.txt (roda o build completo)")
    elif arq.read_text(encoding="utf-8").strip() != key:
        problemas.append(f"site/{key}.txt não contém a chave")
    sm = config.SITE / "sitemap.xml"
    if not sm.exists():
        problemas.append("falta site/sitemap.xml (roda o build completo)")
        urls = []
    else:
        urls = envio.urls_do_sitemap()
    base = f"https://{envio.HOST}/"
    fora = [u for u in urls if not u.startswith(base)]
    if fora:
        problemas.append(f"URLs fora de {base}: {fora[:5]}")
    if len(urls) != len(set(urls)):
        problemas.append("URL repetida no sitemap")
    if not urls:
        problemas.append("sitemap sem URL")
    if len(urls) > 10000:
        problemas.append("mais de 10.000 URLs num envio (limite do IndexNow)")
    payload = {"host": envio.HOST, "key": key, "keyLocation": f"{base}{key}.txt", "urlList": urls}
    return payload, problemas


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    seco = "--dry-run" in sys.argv or "--seco" in sys.argv
    payload, problemas = conferir()
    print(f"IndexNow · {envio.ENDPOINT} · {len(payload['urlList'])} URLs do sitemap")
    for p in problemas:
        print(f"  ! {p}")
    if seco:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        print("modo --dry-run: nada foi enviado.")
        return 1 if problemas else 0
    if problemas:
        print("não envio: corrija os itens acima.")
        return 1
    sys.argv = [sys.argv[0]]
    return envio.main()


if __name__ == "__main__":
    sys.exit(main())
