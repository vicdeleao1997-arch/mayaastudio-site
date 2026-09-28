"""Validações do build (§7.1). Estrito: qualquer erro faz o build sair com código ≠ 0.
Em --only/--tolerante, links para páginas ainda não geradas viram aviso."""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

from . import config, dados

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
SKIP_TEXT = {"script", "style", "template"}
KANJI_OK = set("間知築創磨展")


# ── mini-DOM ─────────────────────────────────────────────────────────────────
class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.children, self.parent = tag, dict(attrs), [], parent

    def get(self, k, d=None):
        return self.attrs.get(k, d)

    def classes(self):
        return (self.attrs.get("class") or "").split()

    def iter(self):
        yield self
        for ch in self.children:
            if isinstance(ch, Node):
                yield from ch.iter()

    def text(self, skip_hidden=False):
        out = []
        for ch in self.children:
            if isinstance(ch, str):
                out.append(ch)
            elif ch.tag not in SKIP_TEXT and not (skip_hidden and ch.get("aria-hidden") == "true"):
                out.append(ch.text(skip_hidden))
        return "".join(out)


class _Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {}, None)
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def parse(html: str) -> Node:
    t = _Tree()
    t.feed(html)
    return t.root


def _flat(n: Node):
    """Texto e nós na ordem do documento (sem script/style/template)."""
    for ch in n.children:
        if isinstance(ch, str):
            yield ch
        elif ch.tag not in SKIP_TEXT:
            if ch.tag == "img":
                yield ch
            yield from _flat(ch)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def has_ancestor(n: Node, pred) -> bool:
    p = n.parent
    while p is not None:
        if pred(p):
            return True
        p = p.parent
    return False


# ── resolução de links ───────────────────────────────────────────────────────
def resolve(url: str) -> Path | None:
    path = url.split("#")[0].split("?")[0]
    if not path:
        return None
    p = config.SITE / path.lstrip("/")
    if path.endswith("/"):
        p = p / "index.html"
    elif p.is_dir():
        p = p / "index.html"
    return p


_ids_cache: dict[Path, set] = {}


def ids_of(p: Path) -> set:
    if p not in _ids_cache:
        try:
            _ids_cache[p] = set(re.findall(r'\sid="([^"]+)"', p.read_text(encoding="utf-8")))
        except OSError:
            _ids_cache[p] = set()
    return _ids_cache[p]


# ── checagens ────────────────────────────────────────────────────────────────
FORBIDDEN = [r"33,14", r"28,65", r"22,49", r"conferido no caixa", r"reuni[aã]o", r"desconto", r"closer", r"garant",
             r"escolas e cursos", r"potencializ", r"full-service", r"bricolage", r"tailwind", r"\bROAS\b",
             r"R\$\s?\d{3,}", r"R\$\s?\d{1,3}\.\d{3}"]
CNPJ_RE = re.compile(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}")
# Nomes e páginas que não podem ficar perto da prova: lista local, fora do repositório público
# (build/lib/privado.py, no .gitignore). Num clone sem a lista, essa parte do check 8 não roda.
try:
    from lib.privado import PROVA_LONGE_NOMES as _PROVA_LONGE_NOMES, PROVA_LONGE_URLS as _PROVA_LONGE_URLS
except ImportError:
    _PROVA_LONGE_NOMES, _PROVA_LONGE_URLS = (), ()
# Trava stealth (check 17): nomes que nunca podem aparecer no site. Mesma lista local, fora do repositório público.
try:
    from lib.privado import STEALTH_NOMES as _STEALTH_NOMES
except ImportError:
    _STEALTH_NOMES = ()
_STEALTH_RE = [re.compile(n if n.startswith(r"\b") else re.escape(n), re.I) for n in _STEALTH_NOMES]
# Check 8 também lê alt e src (não só o texto visível): o logo «O Setor Elétrico» da faixa de marcas conta como nome.
# Se reprovar a home por causa desse logo, é decisão do Victor (IOSE): não desligar sem ele.
PROVA_LE_ALT = True
PILAR_NOMES = [p["nome"] for p in dados.PILARES]
PILAR_RE = re.compile(r"(?<![\wÀ-ÿ])(?:%s)(?: · (?:%s)){2,}(?![\wÀ-ÿ])" % (
    "|".join(map(re.escape, PILAR_NOMES)), "|".join(map(re.escape, PILAR_NOMES))))
PROOF_PAGES = {"/", "/trafego-pago-com-ia/"}


def run(pages, written: list[Path], strict: bool = True, partial: bool = False) -> bool:
    errs: list[str] = []
    warns: list[str] = []
    E = errs.append
    _ids_cache.clear()

    # 1 · travessões em tudo o que foi gerado (menos CSS/JS)
    for f in written:
        if f.suffix in (".html", ".xml", ".txt", ".webmanifest") and f.exists():
            s = f.read_text(encoding="utf-8")
            for ch, nome in (("—", "travessão"), ("–", "meia-risca")):
                if ch in s:
                    i = s.index(ch)
                    E(f"[1] {nome} em {f.relative_to(config.SITE)}: …{s[max(0, i - 40):i + 20]!r}…")
    man = config.SITE / "site.webmanifest"
    if man.exists() and ("—" in man.read_text(encoding="utf-8") or "–" in man.read_text(encoding="utf-8")):
        E("[1] travessão em site.webmanifest")

    titles, descs = {}, {}
    for pg in pages:
        f = config.SITE / (pg.path.lstrip("/") + ("index.html" if pg.path.endswith("/") else ""))
        if not f.exists():
            continue
        html = f.read_text(encoding="utf-8")
        root = parse(html)
        where = pg.path
        body_nodes = list(root.iter())
        main = next((n for n in body_nodes if n.tag == "main"), root)
        visible = norm(main.text())
        if PROVA_LE_ALT:   # 8 · o texto lido inclui alt e src das imagens, na ordem do documento
            visible_8 = norm(" ".join(
                (n if isinstance(n, str) else f" {n.get('alt') or ''} {n.get('src') or ''} ")
                for n in _flat(main)))
        else:
            visible_8 = visible

        # 2 · imagens
        for n in body_nodes:
            if n.tag != "img":
                continue
            src = n.get("src", "")
            in_hidden = has_ancestor(n, lambda p: p.get("aria-hidden") == "true")
            if not (n.get("alt") or "").strip() and not in_hidden:
                E(f"[2] {where}: <img> sem alt: {src}")
            if not n.get("width") or not n.get("height"):
                E(f"[2] {where}: <img> sem width/height: {src}")
            if n.get("fetchpriority") != "high" and n.get("loading") != "lazy":
                E(f"[2] {where}: <img> sem loading=lazy (e sem priority): {src}")

        # 3 · links e mídia internos
        ids_here = set(re.findall(r'\sid="([^"]+)"', html))
        for n in body_nodes:
            refs = []
            for a in ("href", "src", "poster"):
                v = n.get(a)
                if v:
                    refs.append(v)
            if n.get("srcset"):
                refs += [x.strip().split(" ")[0] for x in n.get("srcset").split(",") if x.strip()]
            if n.tag == "use":
                continue  # sprite: conferido abaixo
            for v in refs:
                if v.startswith(("mailto:", "tel:", "data:")) or re.match(r"^https?://", v) or v.startswith("//"):
                    continue
                if v.startswith("#"):
                    if v != "#" and v[1:] not in ids_here:
                        E(f"[3] {where}: âncora {v} não existe na página")
                    continue
                if not v.startswith("/"):
                    E(f"[3] {where}: caminho relativo {v} (use absoluto a partir da raiz)")
                    continue
                target = resolve(v)
                if target is None:
                    continue
                if not target.exists():
                    msg = f"[3] {where}: {v} não existe em site/"
                    (warns if (partial or not strict) and n.tag == "a" else errs).append(msg)
                    continue
                if "#" in v and target.suffix == ".html":
                    frag = v.split("#", 1)[1]
                    if frag and frag not in ids_of(target):
                        msg = f"[3] {where}: {v} · id #{frag} não existe no destino"
                        (warns if (partial or not strict) else errs).append(msg)
        if not (config.SITE / "assets/brand/sprite.svg").exists():
            E("[3] sprite.svg ausente")

        # 4 · title e description
        t = next((norm(n.text()) for n in body_nodes if n.tag == "title"), "")
        d = next((n.get("content", "") for n in body_nodes if n.tag == "meta" and n.get("name") == "description"), "")
        if t in titles:
            E(f"[4] title repetido em {where} e {titles[t]}")
        titles[t] = where
        if d in descs:
            E(f"[4] description repetida em {where} e {descs[d]}")
        descs[d] = where
        if not 110 <= len(d) <= 165:
            E(f"[4] {where}: description com {len(d)} caracteres (110 a 165)")

        # 5 · H1
        h1s = [n for n in body_nodes if n.tag == "h1"]
        if len(h1s) != 1:
            E(f"[5] {where}: {len(h1s)} <h1>")
        elif norm(h1s[0].text()) != norm(pg.h1):
            E(f"[5] {where}: H1 {norm(h1s[0].text())!r} ≠ Page.h1 {pg.h1!r}")

        # 6 · lang, canonical, og:image
        html_tag = next((n for n in body_nodes if n.tag == "html"), None)
        if not html_tag or html_tag.get("lang") != "pt-BR":
            E(f"[6] {where}: <html lang> não é pt-BR")
        if not any(n.tag == "link" and n.get("rel") == "canonical" for n in body_nodes):
            E(f"[6] {where}: sem canonical")
        ogi = next((n.get("content", "") for n in body_nodes if n.tag == "meta" and n.get("property") == "og:image"), "")
        if not ogi.startswith(config.SITE_URL) or not (config.SITE / ogi[len(config.SITE_URL):].lstrip("/")).exists():
            E(f"[6] {where}: og:image inexistente: {ogi}")

        # 7 · termos proibidos e CNPJ (no arquivo inteiro)
        low = html
        for pat in FORBIDDEN:
            m = re.search(pat, low, re.I)
            if m:
                E(f"[7] {where}: termo proibido {m.group(0)!r} …{low[max(0, m.start() - 50):m.end() + 30]!r}…")
        for m in CNPJ_RE.finditer(html):
            if not config.CNPJ or m.group(0) != config.CNPJ:
                E(f"[7] {where}: CNPJ não autorizado {m.group(0)}")
        if not config.CNPJ and "41.242.625" in html:
            E(f"[7] {where}: 41.242.625 no site sem conferência")

        # 8 · prova 12,55×
        if "12,55" in html:
            if where not in PROOF_PAGES:
                E(f"[8] {where}: 12,55 fora de / e /trafego-pago-com-ia/")
            for must in ("Venda, não lucro.", "Topo, não média.", "não do caixa"):
                if must not in visible:
                    E(f"[8] {where}: falta {must!r} junto do 12,55")
            for m in re.finditer(r"12,55", visible_8):
                for nome in _PROVA_LONGE_NOMES:
                    if any(abs(m2.start() - m.start()) < 800 for m2 in re.finditer(re.escape(nome), visible_8)):
                        E(f"[8] {where}: 12,55 perto de um nome da lista local")
                        break
            for url in _PROVA_LONGE_URLS:
                if url in html:
                    E(f"[8] {where}: página com 12,55 tem link para uma página da lista local")
        if where in _PROVA_LONGE_URLS:
            if re.search(r"12,55|\bROAS\b|×\s?\d", html, re.I):
                E(f"[8] {where}: número de resultado numa página da lista local")

        # 17 · trava stealth: no HTML inteiro (texto, alt, src, href, JSON-LD, meta)
        for rx in _STEALTH_RE:
            m = rx.search(html)
            if m:
                E(f"[17] {where}: nome proibido (stealth) {m.group(0)!r} …{html[max(0, m.start() - 50):m.end() + 30]!r}…")

        # 8b · direct e perfil
        for n in body_nodes:
            if n.tag != "a":
                continue
            txt = norm(n.text())
            href = n.get("href", "")
            if "direct" in txt.lower() and href != config.IG_DM:
                E(f"[8b] {where}: link {txt!r} diz direct mas aponta para {href}")
            if href == config.IG and "Instagram" not in txt:
                E(f"[8b] {where}: link do perfil com texto {txt!r}")

        # 9 · Ana
        if re.search(r"/ana-0\d\.jpg|ana-lauren-modelo-ia/cover\.jpg", html) and "Nenhuma pessoa real nestas fotos" not in html:
            E(f"[9] {where}: foto da Ana sem «Nenhuma pessoa real nestas fotos»")

        # 10 · pilares
        texts = [norm(n.text()) for n in body_nodes if n.tag in ("p", "li", "span", "h1", "h2", "h3", "td", "a", "figcaption")]
        for s in texts:
            for m in PILAR_RE.finditer(s):
                if m.group(0) not in dados.PILARES_LINHA:
                    E(f"[10] {where}: pilares fora de ordem: {m.group(0)!r}")
        rows = [norm(n.text()) for n in body_nodes if "pillars__nome" in n.classes()]
        if rows and rows != PILAR_NOMES:
            E(f"[10] {where}: pillars_table fora de ordem: {rows}")

        # 11 · JSON-LD
        for n in body_nodes:
            if n.tag == "script" and n.get("type") == "application/ld+json":
                raw = n.text()
                try:
                    data = json.loads(raw)
                except ValueError as e:
                    E(f"[11] {where}: JSON-LD inválido ({e})")
                    continue
                graph = data.get("@graph", [data])
                for b in graph:
                    if b.get("@type") == "FAQPage":
                        qs = [norm(x["name"]) for x in b.get("mainEntity", [])]
                        ans = [norm(x["acceptedAnswer"]["text"]) for x in b.get("mainEntity", [])]
                        page_q = [norm(x.text()) for x in body_nodes if "faq__q" in x.classes()]
                        page_a = [norm(" ".join(norm(p.text()) for p in x.children if isinstance(p, Node)))
                                  for x in body_nodes if "faq__a" in x.classes()]
                        if qs != page_q:
                            E(f"[11] {where}: FAQPage ≠ perguntas da página")
                        elif ans != page_a:
                            E(f"[11] {where}: FAQPage ≠ respostas da página")
                    txt = json.dumps(b, ensure_ascii=False)
                    if "—" in txt or "–" in txt:
                        E(f"[11] {where}: travessão no JSON-LD")

        # 12 · externos
        for n in body_nodes:
            for a in ("href", "src"):
                v = n.get(a) or ""
                if v.startswith("http://"):
                    E(f"[12] {where}: http:// em {v}")
            if n.tag == "a" and re.match(r"^https?://", n.get("href", "")) and not n.get("href", "").startswith(config.SITE_URL):
                if "noopener" not in (n.get("rel") or ""):
                    E(f"[12] {where}: link externo sem noopener: {n.get('href')}")

        # 13 · tamanho
        kb = len(html.encode("utf-8")) / 1024
        if kb > 120:
            E(f"[13] {where}: HTML com {kb:.0f} KB (máx. 120)")

        # 14 · kanji
        for n in body_nodes:
            if "kanji" in n.classes():
                k = norm(n.text())
                if k not in KANJI_OK:
                    E(f"[14] {where}: kanji fora da prancha: {k!r}")

    # 16 · glifo japonês que a fonte do site não tem (a Shippori é recortada: rodar tools/fontes.py)
    fonte = config.SITE / "assets/fonts/shippori-400.woff2"
    if not fonte.exists():
        E("[16] site/assets/fonts/shippori-400.woff2 ausente (py build/tools/fontes.py)")
    else:
        try:
            from fontTools.ttLib import TTFont
            cmap = TTFont(fonte).getBestCmap()
        except Exception as e:  # sem fontTools/brotli: só avisa
            cmap = None
            warns.append(f"[16] não deu para ler a fonte ({e})")
        if cmap is not None:
            falta = set()
            for f in written:
                if f.suffix == ".html" and f.exists():
                    falta |= {ch for ch in f.read_text(encoding="utf-8")
                              if (0x3000 <= ord(ch) <= 0x30FF or 0x3400 <= ord(ch) <= 0x9FFF) and ord(ch) not in cmap}
            if falta:
                E(f"[16] glifo japonês fora da fonte do site: {' '.join(sorted(falta))} (py build/tools/fontes.py)")

    for asset, lim in (("assets/css/main.css", 60), ("assets/js/main.js", 60)):
        f = config.SITE / asset
        if f.exists() and f.stat().st_size / 1024 > lim:
            E(f"[13] {asset} com {f.stat().st_size / 1024:.0f} KB (máx. {lim})")

    # 17 · trava stealth também nos nomes de arquivo publicados (site/assets/**) e em qualquer .html/.xml/.txt gerado
    if _STEALTH_RE:
        for f in (config.SITE / "assets").rglob("*"):
            rel = f.relative_to(config.SITE).as_posix()
            for rx in _STEALTH_RE:
                if rx.search(rel.replace("-", " ").replace("_", " ")) or rx.search(rel):
                    E(f"[17] arquivo com nome proibido (stealth) em site/: {rel}")
                    break
        for f in written:
            if f.suffix in (".xml", ".txt", ".webmanifest") and f.exists():
                s = f.read_text(encoding="utf-8", errors="ignore")
                for rx in _STEALTH_RE:
                    if rx.search(s):
                        E(f"[17] nome proibido (stealth) em {f.relative_to(config.SITE)}")
                        break

    # 15 · órfãos (só relatório, build completo)
    if not partial:
        refs = ""
        for f in list(config.SITE.rglob("*.html")) + [config.SITE / "assets/css/main.css", config.SITE / "site.webmanifest"]:
            if f.exists():
                refs += f.read_text(encoding="utf-8", errors="ignore")
        # fontes das ferramentas (não são referenciadas por página, mas não são órfãs)
        fontes_de_ferramenta = {"/assets/mayaa-mark-ink.png"}   # gato das imagens og (tools/og_chrome.py)
        # logos originais (coloridos): fonte de tools/logos.py, que gera assets/clients/tinta/*.webp
        fontes_de_ferramenta |= {"/assets/clients/" + f.name for f in (config.SITE / "assets/clients").glob("*.png")}
        orf = []
        for f in (config.SITE / "assets").rglob("*"):
            if f.is_file():
                rel = "/" + f.relative_to(config.SITE).as_posix()
                if rel not in refs and rel not in fontes_de_ferramenta:
                    orf.append(rel)
        if orf:
            print(f"\n[15] {len(orf)} arquivo(s) em site/assets sem referência (relatório):")
            for o in sorted(orf)[:60]:
                print("   ", o)

    for w in dict.fromkeys(warns):
        print("  aviso", w)
    if errs:
        print(f"\nCHECKS: {len(errs)} erro(s)")
        for e in errs:
            print("  ✗", e)
        if not strict:
            print("  (modo tolerante: erros não bloqueiam)")
            return True
        return False
    print(f"\nCHECKS: ok ({len(pages)} página(s), {len(warns)} aviso(s))")
    return True
