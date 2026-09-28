"""Gerador do site mayaastudio.com.br (§6.3).

  py build/build.py                         tudo, modo estrito (build final)
  py build/build.py --only home,sistema     só esses módulos de pages/ (não reescreve sitemap/robots)
  py build/build.py --tolerante             módulo com erro é pulado com aviso; checks viram avisos
  py build/build.py --sem-checks            não roda lib/checks.py
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import os
import pkgutil
import re
import sys
import tempfile
import time
import traceback
from pathlib import Path

BUILD = Path(__file__).resolve().parent
sys.path.insert(0, str(BUILD))

from lib import checks, config, layout  # noqa: E402
from lib.page import Page  # noqa: E402

SITE = config.SITE


def write_atomic(path: Path, data: str | bytes) -> None:
    """Escrita atômica: temporário + os.replace, 3 tentativas se o Windows segurar o arquivo."""
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = data.encode("utf-8") if isinstance(data, str) else data
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp-", suffix=path.suffix)
    with os.fdopen(fd, "wb") as f:
        f.write(raw)
    for i in range(3):
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            if i == 2:
                os.unlink(tmp)
                raise
            time.sleep(0.4 * (i + 1))


_CSS_STR = re.compile(r'"(?:[^"\\\n]|\\.)*"|\'(?:[^\'\\\n]|\\.)*\'')


def _css_min(s: str) -> str:
    # Só o que é seguro: espaço em volta de { } ; , e DEPOIS de ':'. NUNCA antes de ':' (".on-tinta :focus-visible"
    # é descendente; sem o espaço vira outra regra). Não toca em + e - (calc) nem em "/" (grid-column, font).
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s*([{};,])\s*", r"\1", s)
    return re.sub(r":\s+", ":", s)


def _css_enxuto(css: str) -> str:
    """CSS publicado enxuto: sem comentários, indentação e espaços desnecessários (a fonte fica legível em styles/).
    Strings ("…" e '…', ex. content:) passam intactas."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out, pos = [], 0
    for m in _CSS_STR.finditer(css):
        out += [_css_min(css[pos:m.start()]), m.group()]
        pos = m.end()
    out.append(_css_min(css[pos:]))
    return "".join(out).strip()


def _aspas_ok(s: str) -> bool:
    return s.count("'") % 2 == 0 and s.count('"') % 2 == 0 and "`" not in s


def _js_enxuto(js: str) -> str:
    """JS publicado enxuto, só por linha e só o que é seguro (sem reescrever código): tira indentação, linhas vazias,
    linhas que são só comentário (// ou /* … */ em bloco) e o /* … */ no fim de uma linha de código quando as aspas
    antes dele fecham. Quebras de linha ficam (ASI intacto). A fonte fica comentada em scripts/."""
    out, bloco = [], False
    for l in js.splitlines():
        s = l.strip()
        if bloco:
            bloco = "*/" not in s
            if not bloco and not s.endswith("*/"):
                raise ValueError(f"comentário de bloco com código depois: {s[:60]}")
            continue
        if not s or s.startswith("//"):
            continue
        if s.startswith("/*"):
            if "*/" not in s:
                bloco = True
                continue
            if s.endswith("*/") and s.index("*/") == len(s) - 2:
                continue
        m = re.match(r"^(.*?\S)\s+/\*((?:(?!\*/).)*)\*/$", s)
        if m and _aspas_ok(m.group(1)) and _aspas_ok(m.group(2)):
            s = m.group(1)
        out.append(s)
    return "\n".join(out)


def bundle(folder: str, out: Path, sep: str) -> str:
    parts = []
    for f in sorted((BUILD / folder).glob("*.css" if folder == "styles" else "*.js")):
        src = f.read_text(encoding="utf-8").strip()
        src = _css_enxuto(src) if folder == "styles" else _js_enxuto(src)
        parts.append(f"{sep[0]} {f.name} {sep[1]}\n" + src + "\n")
    data = "\n".join(parts)
    write_atomic(out, data)
    return hashlib.sha1(data.encode("utf-8")).hexdigest()[:8]


def out_path(page_path: str) -> Path:
    if page_path.endswith(".html"):
        return SITE / page_path.lstrip("/")
    return SITE / page_path.strip("/") / "index.html" if page_path != "/" else SITE / "index.html"


def discover(only: set[str] | None, tolerant: bool) -> tuple[list[Page], list[str], dict[str, list[str]]]:
    import pages as pkg
    found, erros, por_modulo = [], [], {}
    for m in pkgutil.iter_modules(pkg.__path__):
        if m.name.startswith("_") or (only and m.name not in only):
            continue
        try:
            mod = importlib.import_module(f"pages.{m.name}")
            if not hasattr(mod, "pages"):
                continue
            ps = list(mod.pages())
            por_modulo[m.name] = [p.path for p in ps]
            found.extend(ps)
        except Exception:
            msg = f"módulo pages/{m.name}.py falhou:\n{traceback.format_exc()}"
            if not tolerant:
                raise SystemExit(msg)
            erros.append(msg)
            print(f"  ! {msg.splitlines()[0]} (pulado, --tolerante)")
    if only:
        faltando = only - set(por_modulo) - {e.split("pages/")[1].split(".py")[0] for e in erros}
        for f in sorted(faltando):
            print(f"  ! módulo pages/{f}.py não encontrado")
    return found, erros, por_modulo


def sitemap(pages: list[Page]) -> str:
    rows = []
    for p in sorted((p for p in pages if p.sitemap and not p.noindex), key=lambda p: (-p.priority, p.path)):
        rows.append(f"  <url><loc>{config.SITE_URL}{p.path}</loc><lastmod>{p.lastmod or config.LASTMOD}</lastmod>"
                    f"<changefreq>{p.changefreq}</changefreq><priority>{p.priority:.1f}</priority></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n")


ROBOTS = "User-agent: *\nAllow: /\n\nSitemap: https://mayaastudio.com.br/sitemap.xml\n"


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="Gera o site em site/")
    ap.add_argument("--only", default="", help="módulos de pages/ separados por vírgula")
    ap.add_argument("--tolerante", action="store_true")
    ap.add_argument("--sem-checks", action="store_true")
    a = ap.parse_args()
    only = {x.strip() for x in a.only.split(",") if x.strip()} or None

    t0 = time.time()
    layout.ASSET_VERSION["css"] = bundle("styles", SITE / "assets/css/main.css", ("/*", "*/"))
    layout.ASSET_VERSION["js"] = bundle("scripts", SITE / "assets/js/main.js", ("/*", "*/"))
    print(f"CSS e JS: main.css?v={layout.ASSET_VERSION['css']} · main.js?v={layout.ASSET_VERSION['js']}")

    pages, erros, por_modulo = discover(only, a.tolerante)
    seen: dict[str, str] = {}
    for mod, paths in por_modulo.items():
        for p in paths:
            if p in seen:
                raise SystemExit(f"caminho duplicado: {p} ({seen[p]} e {mod})")
            seen[p] = mod

    written: list[Path] = []
    for p in pages:
        try:
            html = layout.render(p)
        except Exception:
            msg = f"página {p.path} falhou:\n{traceback.format_exc()}"
            if not a.tolerante:
                raise SystemExit(msg)
            erros.append(msg)
            print(f"  ! {msg.splitlines()[0]} (pulada)")
            continue
        dest = out_path(p.path)
        write_atomic(dest, html)
        written.append(dest)
        print(f"  {p.path:<36} {len(html.encode()) / 1024:6.1f} KB")

    if not only:
        write_atomic(SITE / "sitemap.xml", sitemap(pages))
        write_atomic(SITE / "robots.txt", ROBOTS)
        write_atomic(SITE / f"{config.INDEXNOW_KEY}.txt", config.INDEXNOW_KEY)
        written += [SITE / "sitemap.xml", SITE / "robots.txt", SITE / f"{config.INDEXNOW_KEY}.txt"]
        print("  sitemap.xml · robots.txt · chave IndexNow")

    ok = True
    if not a.sem_checks:
        ok = checks.run(pages, written, strict=not a.tolerante, partial=bool(only))
    for e in erros:
        print("\n" + e)
    print(f"\n{len(written)} arquivos em {time.time() - t0:.1f}s")
    if erros and not a.tolerante:
        return 1
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
