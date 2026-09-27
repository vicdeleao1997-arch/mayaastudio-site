"""Avisa Bing e outros buscadores (IndexNow) das URLs do sitemap (§7.3).

RODAR SÓ DEPOIS DE PUBLICADO E COM O OK DO VICTOR:
  py build/tools/indexnow.py            confere a chave no ar e envia
  py build/tools/indexnow.py --seco     só mostra o que enviaria (não envia nada)

Sucesso = HTTP 200 ou 202. O Google não usa IndexNow: o passo a passo do Search Console está no SPEC §7.3.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import config  # noqa: E402

HOST = "mayaastudio.com.br"
ENDPOINT = "https://api.indexnow.org/indexnow"


def urls_do_sitemap() -> list[str]:
    xml = (config.SITE / "sitemap.xml").read_text(encoding="utf-8")
    return re.findall(r"<loc>([^<]+)</loc>", xml)


def main() -> int:
    seco = "--seco" in sys.argv
    key = config.INDEXNOW_KEY
    key_url = f"https://{HOST}/{key}.txt"
    urls = urls_do_sitemap()
    payload = {"host": HOST, "key": key, "keyLocation": key_url, "urlList": urls}
    print(f"{len(urls)} URLs do sitemap")
    if seco:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    try:
        with urllib.request.urlopen(key_url, timeout=20) as r:
            no_ar = r.read().decode("utf-8").strip()
    except Exception as e:
        print(f"a chave não responde em {key_url}: {e}. Publique o site antes.")
        return 1
    if no_ar != key:
        print(f"a chave no ar ({no_ar!r}) não bate com config.INDEXNOW_KEY")
        return 1
    req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"IndexNow respondeu {r.status}")
            return 0 if r.status in (200, 202) else 1
    except urllib.error.HTTPError as e:
        print(f"IndexNow respondeu {e.code}: {e.read()[:300]!r}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
