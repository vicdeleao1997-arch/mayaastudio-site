"""Componentes do site (§2.7). C2 e C3 montam páginas só chamando estas funções.

Convenções:
- `lines` de título: lista de str (linha Regular) ou tupla (texto, "b") (linha Bold). "**texto**" também vale Bold.
- Todo texto recebido é escapado aqui dentro. Parâmetros que recebem HTML pronto estão marcados com "(HTML)".
- Revelação (`data-reveal`, lida pelo JS): lines · fade · mask · stagger · count.
"""
from __future__ import annotations

import re

from . import config, dados
from .html import attrs, cls as _cls, esc
from .media import SIZES, dims, picture

KANJI_OK = {"間", "知", "築", "創", "磨", "展"}
_ARROW_EXT = "↗"   # só marcador interno: no HTML sai ICO_OUT (R1-04)

# ↗ e ▶ não existem na Archivo nem na Shippori: o navegador desenhava com fonte do sistema (Segoe UI Symbol no
# Windows). Viram SVG em traço (currentColor, 1.5 px fixos). A seta → continua texto: a Archivo tem esse glifo.
ICO_OUT = ('<svg class="ico ico--out" viewBox="0 0 10 10" width="10" height="10" aria-hidden="true" focusable="false">'
           '<path d="M1.8 8.2 8.2 1.8M3 1.8h5.2V7"/></svg>')
ICO_PLAY = ('<svg class="ico ico--play" viewBox="0 0 10 10" width="10" height="10" aria-hidden="true" focusable="false">'
            '<path d="M2.2 1.2v7.6L8.8 5z"/></svg>')


# ── básicos ──────────────────────────────────────────────────────────────────
def sr(text: str) -> str:
    """Texto só para leitor de tela."""
    return f'<span class="sr">{esc(text)}</span>'


def anchor(id: str) -> str:
    """Âncora vazia (ids antigos da v1) com scroll-margin-top."""
    return f'<span id="{esc(id)}" class="anchor" aria-hidden="true"></span>'


def is_external(href: str) -> bool:
    return href.startswith(("http://", "https://")) and not href.startswith(config.SITE_URL)


def label(text: str, num: str | None = None, tag: str = "p", cls: str = "", id: str | None = None) -> str:
    """<p class="label"><span class="label__num">001</span> · Sobre</p>. cls="label--rule" põe fio em cima.
    Sem `num`, um texto que comece por "01 · " ou "006 · " tem o número separado sozinho."""
    if num is None and text:
        m = re.match(r"^(\d{2,3}) · (.+)$", text)
        if m:
            num, text = m.group(1), m.group(2)
    inner = (f'<span class="label__num">{esc(num)}</span> · {esc(text)}' if num else esc(text)) if text else \
        f'<span class="label__num">{esc(num)}</span>'
    return f"<{tag}{attrs(cls=_cls('label', cls), id=id)}>{inner}</{tag}>"


def _line_parts(line) -> tuple[str, bool]:
    if isinstance(line, (tuple, list)):
        return str(line[0]), (len(line) > 1 and line[1] == "b")
    s = str(line)
    if s.startswith("**") and s.endswith("**") and len(s) > 4:
        return s[2:-2], True
    return s, False


def plain(lines) -> str:
    """Texto corrido de um título por linhas (use em Page.h1)."""
    if isinstance(lines, str):
        return lines
    return " ".join(_line_parts(l)[0] for l in lines)


def title(lines, tag: str = "h2", size: str = "h2", cls: str = "", id: str | None = None, sep: str = " ",
          reveal: bool = True, delay: float | None = None, enter: bool = False) -> str:
    """Título por linhas com máscara de revelação. `sep` (HTML) vai entre as linhas; padrão um espaço.
    enter=True (H1 dos heróis): a entrada é só CSS (.t-enter, @keyframes), começa no 1.º paint e termina sozinha,
    sem esperar o JS/GSAP (que chega depois do paint e não animaria a 1.ª dobra). Sem data-reveal: o JS não mexe."""
    if isinstance(lines, str):
        lines = [lines]
    spans = []
    for i, l in enumerate(lines):
        txt, bold = _line_parts(l)
        t = f"<b>{esc(txt)}</b>" if bold else esc(txt)
        st = f' style="--i:{i}"' if enter else ""
        spans.append(f'<span class="line"><span class="line__in"{st}>{t}</span></span>')
    if enter:
        return f"<{tag}{attrs(cls=_cls('t-' + size, 't-enter', cls), id=id)}>{sep.join(spans)}</{tag}>"
    return (f"<{tag}{attrs(cls=_cls('t-' + size, cls), id=id, data_reveal='lines' if reveal else None, data_delay=delay)}>"
            f"{sep.join(spans)}</{tag}>")


def pillars_line(cls: str = "", tag: str = "p", reveal: str | None = None) -> str:
    """Linha dos 5 pilares (ordem canônica). Cada nome fica inteiro na quebra de linha; o « · » vai no fim."""
    nomes = [p["nome"] for p in dados.PILARES]
    spans = " ".join(f'<span class="nw">{esc(n)}{" ·" if i < len(nomes) - 1 else ""}</span>' for i, n in enumerate(nomes))
    return f"<{tag}{attrs(cls=_cls('label', cls), data_reveal=reveal)}>{spans}</{tag}>"


def paras(text, cls: str = "", reveal: str | None = "fade") -> str:
    """Um ou vários parágrafos (str ou lista). Texto puro."""
    items = [text] if isinstance(text, str) else list(text or [])
    return "".join(f"<p{attrs(cls=cls or None, data_reveal=reveal)}>{esc(t)}</p>" for t in items)


# ── links e botões ───────────────────────────────────────────────────────────
def _link_bits(href: str, arrow: str, external: bool):
    ext = external or is_external(href)
    if ext:
        arrow = _ARROW_EXT
    elif href.startswith("#") and arrow == "→":
        arrow = "↓"
    kind = {"↗": "out", "↓": "down"}.get(arrow, "in")
    if kind == "out":
        arrow = ICO_OUT
    a = attrs(href=href, target="_blank" if ext else None, rel="noopener" if ext else None)
    tail = sr(" (abre em nova aba)") if ext else ""
    return a, arrow, kind, tail


def btn(text: str, href: str, kind: str = "primary", arrow: str = "→", external: bool = False,
        sr: str | None = None, cls: str = "") -> str:
    """Botão. kind="primary" (cheio) | "ghost". Externo: nova aba + ↗; âncora "#x": ↓."""
    a, arrow, akind, tail = _link_bits(href, arrow, external)
    extra = f'<span class="sr">{esc(sr)}</span>' if sr else ""
    k = "btn--ghost" if kind == "ghost" else ""
    return (f'<a class="{_cls("btn", k, cls)}"{a}><span class="btn__txt">{esc(text)}</span>{extra}'
            f'<span class="btn__arrow btn__arrow--{akind}" aria-hidden="true">{arrow}</span>{tail}</a>')


def link_arrow(text: str, href: str, arrow: str = "→", external: bool = False, sr: str | None = None,
               cls: str = "") -> str:
    """Link de texto com seta e sublinhado desenhado."""
    a, arrow, akind, tail = _link_bits(href, arrow, external)
    extra = f'<span class="sr">{esc(sr)}</span>' if sr else ""
    return (f'<a class="{_cls("link-arrow", cls)}"{a}>{esc(text)}{extra}'
            f'<span class="link-arrow__a link-arrow__a--{akind}" aria-hidden="true">{arrow}</span>{tail}</a>')


def text_link(text: str, href: str) -> str:
    """Link sublinhado simples dentro de frase (externo ganha ↗ e nova aba)."""
    a, arrow, _k, tail = _link_bits(href, "", False)
    seta = f' <span aria-hidden="true">{ICO_OUT}</span>' if is_external(href) else ""
    return f"<a{a}>{esc(text)}{seta}{tail}</a>"


def mail_cta(mailto: str, kind: str = "ghost", pre: str | None = None, after: str = "") -> str:
    """E-mail visível + "Copiar e-mail" (o botão só aparece com JS e clipboard).
    after (HTML): outro botão na mesma linha, entre o e-mail e o "Copiar e-mail" (o copiar fica sempre por último)."""
    email = config.EMAIL
    k = "" if kind == "primary" else "btn--ghost"
    pre_html = f'<p class="small mail__pre">{esc(pre)}</p>' if pre else ""
    return (f'<div class="mail">{pre_html}<div class="mail__row">'
            f'<a class="{_cls("btn", k, "btn--mail")}" href="{esc(mailto)}"><span class="btn__txt">{esc(email)}</span>'
            f'<span class="btn__arrow btn__arrow--in" aria-hidden="true">→</span></a>{after}'
            f'<button class="mail__copy label" type="button" data-copy="{esc(email)}" hidden>Copiar e-mail</button>'
            f'<span class="sr" aria-live="polite" data-copy-status></span></div></div>')


# ── kanji e índice ───────────────────────────────────────────────────────────
def kanji(char: str, meaning: str, size: str = "md", cls: str = "", reveal: str | None = "fade",
          caption: bool = True) -> str:
    """Kanji com legenda só do significado ("escalar", "ma · espaço"), como na prancha: o caractere não se repete
    na legenda. Só os seis da prancha."""
    if char not in KANJI_OK:
        raise ValueError(f"kanji fora da prancha: {char}")
    cap = f'<figcaption class="label kanji-fig__cap">{esc(meaning)}</figcaption>' if caption else ""
    return (f'<figure{attrs(cls=_cls("kanji-fig", "kanji-fig--" + size, cls), data_reveal=reveal)}>'
            f'<span class="kanji" lang="ja" aria-hidden="true">{esc(char)}</span>{cap}</figure>')


_kanji = kanji  # alias: funções com parâmetro `kanji` usam este nome


def index_nav(items, title: str = "Índice · Serviços", cls: str = "", aria_label: str = "Índice dos serviços") -> str:
    """items = [("002", "Tráfego pago", "#trafego-pago", "↓"), (None, "Portfólio", "/portfolio/", "→")]"""
    lis = []
    for it in items:
        num, txt, href = it[0], it[1], it[2]
        arrow = it[3] if len(it) > 3 else "→"
        a, arrow, akind, tail = _link_bits(href, arrow, False)
        n = f'<span class="index__num label">{esc(num)}</span>' if num else '<span class="index__num label"></span>'
        lis.append(f'<li class="index__item"><a{a}>{n}<span class="index__txt">{esc(txt)}</span>'
                   f'<span class="index__arrow index__arrow--{akind}" aria-hidden="true">{arrow}</span>{tail}</a></li>')
    return (f'<nav class="{_cls("index", cls)}" aria-label="{esc(aria_label)}"><p class="label">{esc(title)}</p>'
            f'<ol class="index__list" data-reveal="stagger">{"".join(lis)}</ol></nav>')


# ── marquee ──────────────────────────────────────────────────────────────────
def _mq_toggle() -> str:
    return '<button class="mq__toggle label" type="button" aria-pressed="false">Pausar</button>'


def marquee_logos(label: str = "Marcas que já passaram pelo estúdio", id: str = "marcas") -> str:
    def track(hidden: bool) -> str:
        lis = []
        for arq, alt, esc_h in dados.CLIENT_LOGOS:
            src = f"/assets/clients/{arq}"
            w, h = dims(src)
            a = "" if hidden else alt
            lis.append(f'<li class="mq__item" style="--k:{esc_h}"><img src="{src}" alt="{esc(a)}" width="{w}" '
                       f'height="{h}" loading="lazy" decoding="async"></li>')
        extra = ' aria-hidden="true"' if hidden else ' role="list"'
        return f'<ul class="mq__track"{extra}>{"".join(lis)}</ul>'
    return (f'<section class="mq" id="{esc(id)}" aria-label="{esc(label)}" data-marquee>'
            f'<div class="wrap mq__head"><p class="label">{esc(label)}</p>{_mq_toggle()}</div>'
            f'<div class="mq__viewport">{track(False)}{track(True)}</div></section>')


def marquee_text(text: str, cls: str = "", label: str = "Faixa de texto em movimento") -> str:
    """Faixa de texto em movimento (rodapé). A frase fica legível uma vez; as cópias têm aria-hidden."""
    unit = f'<span class="mqt__unit">{esc(text)}</span>'
    unit_h = f'<span class="mqt__unit" aria-hidden="true">{esc(text)}</span>'
    return (f'<div class="{_cls("mq mqt", cls)}" data-marquee>'
            f'<div class="mq__viewport"><p class="mq__track mqt__track">{unit}{unit_h}</p>'
            f'<p class="mq__track mqt__track" aria-hidden="true">{unit}{unit}</p></div>'
            f'<div class="wrap mq__head mqt__head">{_mq_toggle()}</div></div>')


# ── imagem ───────────────────────────────────────────────────────────────────
def band(src: str, alt: str, cap_left: str, cap_right=None, priority: bool = False, id: str | None = None,
         pos: str | None = None) -> str:
    """Faixa de imagem em tela cheia. cap_right: (texto, href) ou HTML pronto. pos: object-position ("50% 55%")."""
    if isinstance(cap_right, (tuple, list)):
        cap_right = link_arrow(cap_right[0], cap_right[1])
    style = f"--pos:{pos}" if pos else None
    pic = picture(src, alt, "band", cls="band__img", priority=priority)
    return (f'<figure{attrs(cls="band", id=id)} data-band>'
            f'<div class="band__frame"><div{attrs(cls="band__media", style=style)} data-parallax>{pic}</div></div>'
            f'<figcaption class="band__cap"><div class="wrap band__cap-in"><span class="label">{esc(cap_left)}</span>'
            f'{cap_right or ""}</div></figcaption></figure>')


def _caption(caption: str | None, num: str | None, style: str) -> str:
    caption = (caption or "").strip()
    if not num:
        return caption
    parts = [p.strip() for p in caption.split(" · ")] if caption else []
    if num in parts:
        return caption
    if not caption:
        return num
    return f"{num} · {caption}" if style == "desc" else f"{caption} · {num}"


NBSP = " "


def cap_html(cap: str, arrow: bool = False) -> str:
    """Legenda "Criativo · Produto · 07 →" que nunca abre linha com « · » (espaço inseparável antes dele), não
    separa um número curto do seu « · » e não deixa a seta sozinha (ela fica colada à última palavra)."""
    parts = [esc(p) for p in cap.split(" · ")]
    out = parts[0]
    for i, p in enumerate(parts[1:], 1):
        glue = NBSP if (i == len(parts) - 1 and len(p) <= 3) else " "
        out += f"{NBSP}·{glue}{p}"
    if arrow:
        head, _sp, last = out.rpartition(" ")
        tail = f'<span class="nw">{last}{NBSP}<span class="fig__arrow" aria-hidden="true">→</span></span>'
        out = f"{head} {tail}" if head else tail
    return out


def figure(src: str, alt: str, caption: str | None = None, num: str | None = None, style: str = "tec",
           ratio: str | None = None, fx: bool = True, sizes: str = "grid4", priority: bool = False,
           link: str | None = None, cls: str = "") -> str:
    """Figura legendada. style="tec" → "EDITORIAL · 02" (.label); "desc" → "01 · Descrição" (.small).
    fx=False obrigatório em peça com texto (anúncios) e logos. link envolve tudo e leva ao case."""
    cap = _caption(caption, num, style)
    pic = picture(src, alt, sizes, priority=priority, ratio=ratio)
    cap_cls = "label" if style == "tec" else "small"
    capt = f'<figcaption class="fig__cap {cap_cls}">{cap_html(cap, bool(link))}</figcaption>' if cap else ""
    fig = (f'<figure{attrs(cls=_cls("fig", "fig--" + style, cls), data_reveal="mask", data_fx="distort" if fx else None)}>'
           f'<div class="fig__media">{pic}</div>{capt}</figure>')
    if link:
        return f'<a class="fig-link" href="{esc(link)}">{fig}<span class="sr">, ver o case</span></a>'
    return fig


def image_grid(items, cols: int = 4, ratio: str | None = "4/5", offset: bool = True, style: str = "tec",
               cls: str = "") -> str:
    """items = [dict(src, alt, caption, num, fx=True, link=None)]. ≥1024: `cols` colunas; abaixo: 2."""
    sizes = {4: "grid4", 3: "grid3", 2: "grid2"}.get(cols, "grid4")
    figs = []
    for it in items:
        figs.append(figure(it["src"], it["alt"], it.get("caption"), it.get("num"), style=it.get("style", style),
                           ratio=it.get("ratio", ratio), fx=it.get("fx", True), sizes=it.get("sizes", sizes),
                           priority=it.get("priority", False), link=it.get("link")))
    return (f'<div class="{_cls("igrid", "igrid--offset" if offset else "", cls)}" style="--cols:{cols}">'
            f'{"".join(figs)}</div>')


def video(src: str, poster: str, label: str, ratio: str = "9/16", caption: str | None = None,
          num: str | None = None, autoplay: bool = True, link=None, cls: str = "", play: str = "Ver filme") -> str:
    """Vídeo mudo com pôster. Sem JS: controles nativos. Modo completo: toca só quando ≥50% visível, com
    Pausar/Continuar e Ativar som. Modo suave: pôster + botão `play` ("Ver filme ▶"), controles só depois do clique.
    link: (texto, href) opcional, vai na linha da legenda."""
    cap = _caption(caption, num, "tec")
    if isinstance(link, (tuple, list)):
        link = link_arrow(link[0], link[1])
    capt = (f'<figcaption class="vid__cap"><span class="label">{esc(cap)}</span>{link or ""}</figcaption>'
            if (cap or link) else "")
    return (f'<figure class="{_cls("vid", cls)}" data-reveal="mask">'
            f'<div class="vid__frame" style="aspect-ratio:{esc(ratio)}">'
            f'<video{attrs(cls="vid__el", muted=True, playsinline=True, loop=True, preload="none", controls=True, poster=poster, aria_label=label, data_autoplay=True if autoplay else None, data_play=play if autoplay else None)}>'
            f'<source src="{esc(src)}" type="video/mp4"></video></div>{capt}</figure>')


def ig_embed(url: str, kind: str = "reel", what: str = "o reel", link_text: str = "Abrir no Instagram",
             preview: str | None = None) -> str:
    """Embed do Instagram só depois do clique (nada carrega antes).
    preview: imagem estática (do próprio site) atrás do aviso de consentimento, para a caixa não parecer vazia."""
    embed = url.rstrip("/") + "/embed/"
    prev = (f'<div class="ig__prev" aria-hidden="true">'
            f'{picture(preview, "", "(min-width:1024px) 420px, 100vw", ratio="4/5", decorative=True)}</div>'
            if preview else "")
    return (f'<div class="{_cls("ig", "ig--prev" if preview else "")}" data-ig-src="{esc(embed)}" '
            f'data-ig-kind="{esc(kind)}" data-ig-what="{esc(what)}">{prev}<div class="ig__card">'
            f'<p class="small">Para ver {esc(what)} aqui, carregue o player oficial do Instagram. Ao carregar, o '
            f'Instagram pode gravar cookies no seu navegador. <a href="/privacidade/">Privacidade</a></p>'
            f'<div class="ig__row"><button class="btn btn--ghost" type="button" data-ig-load>'
            f'<span class="btn__txt">Carregar {esc(what)}</span></button>'
            f'{link_arrow(link_text, url, external=True)}</div></div></div>')


# ── listas e blocos de texto ─────────────────────────────────────────────────
def deliv_list(items, cls: str = "") -> str:
    """Lista numerada com fios (entregáveis). items: textos."""
    lis = "".join(f'<li><span class="label deliv__num">{i:02d}</span><span class="deliv__txt">{esc(t)}</span></li>'
                  for i, t in enumerate(items, 1))
    return f'<ol class="{_cls("deliv", cls)}" data-reveal="stagger">{lis}</ol>'


def note(text: str, link=None, cls: str = "") -> str:
    """Nota .small em fumaça com fio em cima. link: (texto, href) ou HTML pronto."""
    if isinstance(link, (tuple, list)):
        link = link_arrow(link[0], link[1])
    extra = f' <span class="note__link">{link}</span>' if link else ""
    return f'<div class="{_cls("note", cls)}" data-reveal="fade"><p class="small">{esc(text)}</p>{extra}</div>'


def _step_item(it, i: int):
    if isinstance(it, dict):
        num, t, x = it.get("num") or f"{i:02d}", it.get("title", ""), it.get("text")
    elif isinstance(it, (tuple, list)):
        num, t, x = f"{i:02d}", it[0], (it[1] if len(it) > 1 else None)
    else:
        num, t, x = f"{i:02d}", str(it), None
    m = re.match(r"^(\d{2}) · (.+)$", t)
    if m:
        num, t = m.group(1), m.group(2)
    return num, t, x


def steps(items, layout: str = "grid", cols: int | None = None, cls: str = "") -> str:
    """layout="grid": cartões numerados (4 itens → 2×2, 6 → 3×2). layout="path": "01 Anúncio → 02 Página → …".
    items: str (só título) · (título, texto) · dict(num, title, text)."""
    lis = []
    for i, it in enumerate(items, 1):
        num, t, x = _step_item(it, i)
        if layout == "path":
            body = f'<span class="step__t">{esc(t)}</span>' + (f'<span class="small step__x">{esc(x)}</span>' if x else "")
            lis.append(f'<li class="step"><span class="label step__num">{esc(num)}</span>{body}</li>')
        else:
            body = f'<h3 class="t-h3 step__t">{esc(t)}</h3>' + (f'<p class="small step__x">{esc(x)}</p>' if x else "")
            lis.append(f'<li class="step"><span class="label step__num">{esc(num)}</span>{body}</li>')
    if layout == "path":
        return f'<ol class="{_cls("steps steps--path", cls)}" data-reveal="stagger">{"".join(lis)}</ol>'
    n = cols or (3 if len(items) % 3 == 0 and len(items) > 4 else 2)
    return f'<ol class="{_cls("steps steps--grid", cls)}" style="--cols:{n}" data-reveal="stagger">{"".join(lis)}</ol>'


def list_links(items, cls: str = "") -> str:
    """Lista numerada "MARCA / SEGMENTO · ENTREGÁVEL →".
    items: (título, href) · (título, sub, href) · dict(title, sub, href, num, thumb).
    thumb: capa do case (decorativa, 4:5, lazy) entre o número e o texto; a lista ganha .llist--thumbs."""
    lis = []
    com_thumb = False
    for i, it in enumerate(items, 1):
        th = None
        if isinstance(it, dict):
            t, s, href, num = it["title"], it.get("sub"), it["href"], it.get("num") or f"{i:02d}"
            th = it.get("thumb")
        elif len(it) == 2:
            (t, href), s, num = it, None, f"{i:02d}"
        else:
            (t, s, href), num = it, f"{i:02d}"
        a, arrow, akind, tail = _link_bits(href, "→", False)
        cola = lambda x: esc(x).replace(" · ", NBSP + "· ")   # « · » preso à palavra de antes: fecha a linha, nunca abre
        sub = f'<span class="llist__s label">{cola(s)}</span>' if s else ""
        thumb = ""
        if th:
            com_thumb = True
            thumb = (f'<span class="llist__th" aria-hidden="true">'
                     f'{picture(th, "", "(min-width:1024px) 5rem, 4rem", ratio="4/5", decorative=True)}</span>')
        lis.append(f'<li><a{a}><span class="llist__n label">{esc(num)}</span>{thumb}<span class="llist__b">'
                   f'<span class="llist__t">{cola(t)}</span>{sub}</span>'
                   f'<span class="llist__a llist__a--{akind}" aria-hidden="true">{arrow}</span>{tail}</a></li>')
    return (f'<ol class="{_cls("llist", "llist--thumbs" if com_thumb else "", cls)}" data-reveal="stagger">'
            f'{"".join(lis)}</ol>')


def head(label_text: str | None = None, num: str | None = None, lines=None, text=None, tag: str = "h2",
         size: str = "h2", cls: str = "", id: str | None = None) -> str:
    """Cabeçalho de seção padrão: rótulo com fio + título por linhas + texto (str ou lista)."""
    parts = []
    if label_text or num:
        parts.append(label(label_text or "", num=num, cls="label--rule"))
    if lines:
        parts.append(title(lines, tag=tag, size=size, id=id))
    if text:
        parts.append(f'<div class="sec-head__text stack">{paras(text)}</div>')
    return f'<header class="{_cls("sec-head", cls)}">{"".join(parts)}</header>'


def section(*parts, id: str | None = None, tone: str | None = None, cls: str = "", wrap: bool = True,
            aria_label: str | None = None, extra_ids=()) -> str:
    """Seção padrão. tone: None/"papel" · "cartao" · "tinta". parts: HTML pronto."""
    tone_cls = {"cartao": "sec--cartao", "tinta": "sec--tinta on-tinta"}.get(tone or "", "")
    anchors = "".join(anchor(x) for x in extra_ids)
    inner = "".join(parts)
    if wrap:
        inner = f'<div class="wrap">{inner}</div>'
    return f'<section{attrs(cls=_cls("sec", tone_cls, cls), id=id, aria_label=aria_label)}>{anchors}{inner}</section>'


# ── blocos da home e de serviço ──────────────────────────────────────────────
def service_block(id: str, num: str, value: str, title_lines, text, items=None, cta: str | None = None,
                  cta2: str | None = None, media: str = "", kanji=None, extra_ids=(), tone: str = "papel",
                  label_text: str = "Serviço") -> str:
    """Bloco de serviço. cta/cta2/media: HTML pronto. kanji: ("築", "construir")."""
    side = ""
    if items:
        side = deliv_list(items)
    if kanji:
        side = _kanji(kanji[0], kanji[1], size="lg", cls="svc__kanji") + side
    ctas = "".join(x for x in (cta, cta2) if x)
    ctas_html = f'<div class="svc__ctas" data-reveal="fade">{ctas}</div>' if ctas else ""
    media_html = f'<div class="svc__media">{media}</div>' if media else ""
    return section(
        label(label_text, num=num, cls="label--rule"),
        f'<div class="grid svc__grid"><div class="svc__main">'
        f'<p class="value" data-reveal="fade">{esc(value)}</p>{title(title_lines, size="h2", cls="svc__title")}'
        f'<div class="svc__text stack">{paras(text)}</div>{ctas_html}</div>'
        f'<div class="svc__side">{side}</div></div>{media_html}',
        id=id, tone="cartao" if tone == "cartao" else None, cls="svc", extra_ids=extra_ids)


def manifesto(lines, sub: str, images, id: str = "manifesto", label_text: str = "Manifesto") -> str:
    """Frase grande + sub + 3 imagens (col 1-4 3/4 · col 6-8 4/5 descendo · col 10-12 3/4).
    images = [dict(src, alt, num, link)]."""
    ratios = ["3/4", "4/5", "3/4"]
    figs = []
    for i, im in enumerate(images[:3]):
        figs.append(f'<div class="mf__img mf__img--{i + 1}">' + figure(
            im["src"], im["alt"], im.get("caption"), im.get("num"), ratio=im.get("ratio", ratios[i]),
            fx=im.get("fx", True), sizes="(min-width:1024px) 33vw, 50vw" if i < 2 else "(min-width:1024px) 25vw, 100vw",
            link=im.get("link")) + "</div>")
    return section(
        label(label_text, cls="label--rule"),
        f'<div class="grid mf__grid">{title(lines, size="display", cls="mf__title")}'
        f'<p class="lead mf__sub" data-reveal="fade">{esc(sub)}</p></div>'
        f'<div class="grid mf__imgs">{"".join(figs)}</div>',
        id=id, cls="mf")


def process(label_text: str, lines, steps_, id: str = "processo", extra_ids=(), num: str | None = None) -> str:
    """Processo com kanji. steps_ = [dict(num="01", kanji="知", meaning="saber", title="Diagnóstico", text="…")]."""
    lis = []
    for s in steps_:
        k = s["kanji"]
        if k not in KANJI_OK:
            raise ValueError(f"kanji fora da prancha: {k}")
        lis.append(f'<li class="proc__step"><span class="kanji proc__kanji" lang="ja" aria-hidden="true">{esc(k)}</span>'
                   f'<div class="proc__body"><p class="label proc__cap">{esc(s["meaning"])}</p>'
                   f'<p class="label proc__num">{esc(s["num"])}</p><h3 class="t-h3 proc__t">{esc(s["title"])}</h3>'
                   f'<p class="small proc__x">{esc(s["text"])}</p></div></li>')
    return section(
        label(label_text, num=num, cls="label--rule"), title(lines, size="h2", cls="proc__title"),
        f'<ol class="proc__steps" data-reveal="stagger">{"".join(lis)}</ol>',
        id=id, cls="proc", extra_ids=extra_ids)


def proof(tone: str = "tinta", num_label: str | None = None, link: bool | None = None) -> str:
    """Prova 12,55× · TEXTO FIXO (o check 8 depende disso). Na pilar: num_label="05 · Prova · …" (sem o link)."""
    lab = num_label or "Prova · conta de cliente, anonimizada"
    show_link = (num_label is None) if link is None else link
    tone_cls = "sec--tinta on-tinta" if tone == "tinta" else "sec--cartao"
    lk = f'<p class="proof__more">{link_arrow("Como lemos uma conta", "/trafego-pago-com-ia/")}</p>' if show_link else ""
    return (
        f'<section class="proof sec {tone_cls}" id="prova" aria-labelledby="prova-t"><div class="wrap grid">'
        f'<p class="label label--rule proof__label" id="prova-t">{esc(lab)}</p>'
        f'<div class="proof__fig"><p class="proof__num"><span data-reveal="count" data-to="12.55" data-dec="2">12,55</span>'
        f'<span class="proof__x" aria-hidden="true">×</span><span class="sr"> vezes</span></p>'
        f'<p class="label proof__unit">Retorno em vendas para cada real investido em anúncio · relatório da plataforma</p></div>'
        f'<div class="proof__body">'
        f'<p class="lead" data-reveal="fade">Para cada R$ 1 investido em anúncio, R$ 12,55 em vendas, segundo o relatório '
        f'da plataforma. É o topo entre 45 campanhas lidas uma por uma, de set/2025 a ago/2026.</p>'
        f'<ul class="proof__caveats" data-reveal="stagger"><li>Número do relatório da plataforma de anúncio, não do caixa.</li>'
        f'<li>Venda, não lucro.</li><li>Topo, não média.</li></ul>'
        f'<dl class="proof__stats">'
        f'<div><dt><span data-reveal="count" data-to="45">45</span></dt>'
        f'<dd>campanhas lidas uma por uma</dd></div>'
        f'<div><dt><span data-reveal="count" data-to="12">12</span></dt>'
        f'<dd>meses, de set/2025 a ago/2026</dd></div></dl>'
        f'<p class="small proof__disc">Resultado de uma conta não é promessa para outra. Cada negócio tem o seu ponto de partida.</p>'
        f'{lk}</div></div></section>')


def cta_final(label_text: str, lines, text: str, primary: str, secondary: str | None = None,
              note: str | None = None) -> str:
    """CTA de encerramento (id="contato"). primary/secondary/note: HTML pronto (btn, mail_cta…)."""
    note_html = f'<p class="small cta__note" data-reveal="fade">{note}</p>' if note else ""
    return (f'<section class="sec cta" id="contato" aria-labelledby="contato-t"><div class="wrap"><div class="cta__in">'
            f'{label(label_text)}{title(lines, size="display", cls="cta__title", id="contato-t")}'
            f'<p class="lead cta__text" data-reveal="fade">{esc(text)}</p>'
            f'<div class="cta__actions" data-reveal="fade">{primary}{secondary or ""}</div>{note_html}'
            f'</div></div></section>')


def cta(variante: str, label_text: str, secondary: str | None = None) -> str:
    """Atalho para as variantes de §3.0.4: "CONTA" · "PROJETO" · "COLECAO" · "MODELO".
    `secondary` (HTML) troca o secundário (ex.: IOSE)."""
    v = variante.upper().replace("Ç", "C").replace("Ã", "A")
    if v == "CONTA":
        nota = ('Quer uma modelo IA para a sua marca? '
                f'<a href="{esc(config.IG_DM)}" target="_blank" rel="noopener">Manda MODELO no direct.'
                f'<span aria-hidden="true"> {ICO_OUT}</span>{sr(" (abre em nova aba)")}</a>')
        return cta_final(label_text, ["Já anuncia?", ("Traz a conta pra mesa.", "b")],
                         "Manda a palavra CONTA no direct do Instagram. Começamos pelo diagnóstico do que já roda.",
                         btn("Manda CONTA no direct", config.IG_DM, external=True),
                         secondary if secondary is not None else mail_cta(config.MAILTO_DIAG, pre="Prefere e-mail?"),
                         nota)
    if v in ("PROJETO", "COLECAO"):
        l1 = "Tem um produto" if v == "PROJETO" else "Tem uma coleção"
        # o botão secundário fica na linha do e-mail, antes do "Copiar e-mail" (que vem sempre por último)
        sec = secondary if secondary is not None else btn("Falar no direct", config.IG_DM, kind="ghost", external=True)
        return cta_final(label_text, [l1, ("para lançar?", "b")],
                         "Conta o que quer lançar. Respondemos com o caminho e as peças que fazem sentido.",
                         mail_cta(config.MAILTO_PROJETO, kind="primary", pre="Iniciar projeto por e-mail", after=sec))
    if v == "MODELO":
        return cta_final(label_text, ["Quer uma modelo assim", ("para a sua marca?", "b")],
                         "Manda a palavra MODELO no direct do Instagram.",
                         btn("Manda MODELO no direct", config.IG_DM, external=True),
                         secondary if secondary is not None else btn("Ver o serviço de audiovisual", "/servicos/audiovisual-com-ia/", kind="ghost"))
    raise ValueError(f"variante de CTA desconhecida: {variante}")


# ── páginas internas ─────────────────────────────────────────────────────────
def breadcrumb(items) -> str:
    """items = [("Início","/"), ("Portfólio","/portfolio/"), ("BVBA Supply", None)]"""
    lis = []
    for name, href in items:
        if href:
            lis.append(f'<li><a href="{esc(href)}">{esc(name)}</a></li>')
        else:
            lis.append(f'<li aria-current="page">{esc(name)}</li>')
    return f'<nav class="crumbs label" aria-label="Trilha"><ol>{"".join(lis)}</ol></nav>'


def _hero_curto(crumbs, label_text: str, lines, lead: str | None, kanji, extra: str = "", sep: str = " ",
                h1_cls: str = "", cls: str = "") -> str:
    """Abertura curta (cases e portfólio): trilha e rótulo na mesma linha, H1 + kanji, texto logo abaixo, sem fio.
    O conteúdo principal (imagem de abertura, grade de cases) entra na 1.ª dobra."""
    k = _kanji(kanji[0], kanji[1], size="lg", cls="ph__kanji") if kanji else ""
    lead_html = f'<p class="lead ph__lead" data-reveal="fade" data-delay=".3">{esc(lead)}</p>' if lead else ""
    return (f'<section class="{_cls("ph ph--case", cls)}" data-hero><div class="wrap">'
            f'<div class="ph__top">{breadcrumb(crumbs)}{label(label_text, cls="ph__label")}</div>'
            f'<div class="grid ph__grid">'
            f'{title(lines, tag="h1", size="h1", cls=_cls("ph__title", h1_cls), sep=sep, enter=True)}{k}'
            f'{lead_html}{extra}</div></div></section>')


def page_hero(label_text: str, lines, lead: str | None, kanji=None, ctas=(), crumbs=(), extra: str = "",
              h1_cls: str = "", sep: str = " ", compact: bool = False) -> str:
    """Abertura de página interna: breadcrumb, rótulo, H1 (col 1-10), kanji (11-12), lead (1-7), CTAs, fio.
    compact=True: abertura curta (a dos cases), para o conteúdo entrar na 1.ª dobra (ex.: portfólio)."""
    if compact and crumbs:
        return _hero_curto(crumbs, label_text, lines, lead, kanji, extra="".join(ctas) + extra, sep=sep,
                           h1_cls=h1_cls, cls="ph--compact")
    k = _kanji(kanji[0], kanji[1], size="lg", cls="ph__kanji") if kanji else ""
    c = "".join(ctas)
    lead_html = f'<p class="lead ph__lead" data-reveal="fade" data-delay=".3">{esc(lead)}</p>' if lead else ""
    ctas_html = f'<div class="ph__ctas" data-reveal="fade" data-delay=".4">{c}</div>' if c else ""
    crumbs_html = breadcrumb(crumbs) if crumbs else ""
    return (f'<section class="ph" data-hero><div class="wrap">{crumbs_html}'
            f'<div class="grid ph__grid">{label(label_text, cls="ph__label")}'
            f'{title(lines, tag="h1", size="h1", cls=_cls("ph__title", h1_cls), sep=sep, enter=True)}{k}'
            f'{lead_html}{ctas_html}{extra}</div></div></section>')


def ficha(rows, cls: str = "") -> str:
    """Ficha técnica: rows = [("Cliente", "BVBA Supply"), …]. cls="ficha--row": em faixa (4 colunas)."""
    items = "".join(f'<div class="ficha__row"><dt class="label">{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a, b in rows)
    return f'<dl class="{_cls("ficha", cls)}" data-reveal="stagger">{items}</dl>'


_CASE_HERO = {
    "bvba-surrealismo": dict(lines=["BVBA Supply", ("O surrealismo.", "b")], sep=' <span class="sr">· </span>'),
    "ana-lauren-modelo-ia": dict(lines=["Ana Lauren", ("é 100% IA.", "b")], label="Case 03 · IA · Modelo sintética"),
}


def case_hero(slug: str, lead: str, ficha_rows=None, badge: str | None = None, lines=None,
              label_text: str | None = None, sep: str | None = None) -> str:
    """Abertura de case, curta como a da NUMIS: trilha e rótulo na mesma linha, H1, kanji e texto de abertura.
    A imagem de abertura vem logo depois (na 1.ª dobra) e a ficha técnica vai junto dela (`ficha(rows,
    cls="ficha--row")` na página). ficha_rows aqui é opcional (fica à direita do texto, como antes)."""
    cz = dados.CASES[slug]
    d = _CASE_HERO.get(slug, {})
    lines = lines or d.get("lines") or [cz["marca"], (cz["titulo"] + ".", "b")]
    lab = label_text or d.get("label") or f'Case {cz["num"]} · {cz["segmento"]} · {cz["area"]}'
    sep = sep if sep is not None else d.get("sep", " ")
    fic = ficha(ficha_rows) if ficha_rows and not isinstance(ficha_rows, str) else (ficha_rows or "")
    fic_html = f'<div class="ph__ficha">{fic}</div>' if fic else ""
    bdg = f'<p class="badge label" data-reveal="fade">{esc(badge)}</p>' if badge else ""
    return _hero_curto([("Início", "/"), ("Portfólio", "/portfolio/"), (cz["marca"], None)], lab, lines, lead,
                       cz["kanji"], extra=bdg + fic_html, sep=sep)


def case_card(slug: str, size: str = "lg", heading: str = "h2", show_line: bool = True,
              fx: bool | None = None, cover: str | None = None, cover_alt: str | None = None,
              ratio: str | None = "4/5", priority: bool = False) -> str:
    """Card de case. fx=None usa `cover_fx` de CASES (False na capa com texto, como a do IOSE, §2.7.9).
    cover/cover_alt trocam a imagem (ex.: outra peça do mesmo case); ratio=None mantém a proporção do arquivo
    (peça com texto não se recorta). priority=True: 1.ª imagem da dobra (eager + fetchpriority=high)."""
    cz = dados.CASES[slug]
    if fx is None:
        fx = cz.get("cover_fx", True)
    sizes = "card-lg" if size == "lg" else "card-md"
    pic = picture(cover or cz["cover"], cover_alt or cz["cover_alt"], sizes, ratio=ratio, priority=priority)
    line = f'<p class="small case-card__line">{esc(cz["linha"])}</p>' if show_line else ""
    ia = '<p class="small case-card__ia">100% IA · Nenhuma pessoa real nestas fotos</p>' if cz.get("ia_pessoa") else ""
    return (f'<article class="case-card case-card--{esc(size)}"><a href="/cases/{esc(slug)}/" class="case-card__link">'
            f'<figure{attrs(cls="case-card__media", data_reveal="mask", data_fx="distort" if fx else None)}>{pic}</figure>'
            f'<p class="label case-card__meta"><span class="label__num">{esc(cz["num"])}</span> · {esc(cz["segmento"])} · {esc(cz["entregavel"])}</p>'
            f'<{heading} class="t-h3 case-card__title">{esc(cz["nome"])}</{heading}>{line}'
            f'<span class="link-arrow case-card__go" aria-hidden="true">Ver case<span class="link-arrow__a link-arrow__a--in">→</span></span>'
            f'</a>{ia}</article>')


def case_series(num: str, title_text: str, text: str | None, items, kanji=None, layout: str = "auto",
                id: str | None = None, label_text: str | None = None, cls: str = "",
                text_html: str | None = None, media_first: bool = False, after: str = "") -> str:
    """Série de imagens de case. items: dict(src, alt, caption, num, fx=True) ou HTML pronto (video/ig_embed).
    layout auto: 1 → mídia 7 col + texto ao lado; 2/3/4 → colunas.
    cls: classe extra na <section>. text_html: texto já em HTML (com link), no lugar de `text`.
    media_first: a mídia vem antes do cabeçalho (abertura na 1.ª dobra). after (HTML): depois da série (ex.: ficha)."""
    n = len(items)
    lay = layout if layout != "auto" else ("side" if n == 1 else f"c{min(n, 4)}")
    sizes = {"side": "(min-width:1024px) 58vw, 100vw", "c2": "grid2", "c3": "grid3", "c4": "grid4"}.get(lay, "grid2")
    media = []
    for it in items:
        if isinstance(it, str):
            media.append(f'<div class="cs__item">{it}</div>')
        else:
            media.append('<div class="cs__item">' + figure(
                it["src"], it["alt"], it.get("caption"), it.get("num"), style=it.get("style", "desc"),
                ratio=it.get("ratio"), fx=it.get("fx", True), sizes=it.get("sizes", sizes),
                priority=it.get("priority", False), link=it.get("link")) + "</div>")
    k = _kanji(kanji[0], kanji[1], size="md", cls="cs__kanji") if kanji else ""
    corpo = text_html if text_html is not None else (esc(text) if text else "")
    txt = f'<p class="small cs__text" data-reveal="fade">{corpo}</p>' if corpo else ""
    lab = label_text or f"Série {num}"
    head_html = (f'<header class="cs__head">{label(lab, cls="label--rule")}{k}'
                 f'{title([title_text], size="h3", cls="cs__title")}{txt}</header>')
    media_html = f'<div class="cs__media">{"".join(media)}</div>'
    corpo_html = media_html + head_html if media_first else head_html + media_html
    return (f'<section{attrs(cls=_cls("sec cs", f"cs--{lay}", "cs--mfirst" if media_first else "", cls), id=id)}>'
            f'<div class="wrap"><div class="cs__grid">{corpo_html}</div>{after}</div></section>')


def next_case(slug: str, alvo: str | None = None) -> str:
    """Próximo case. `slug` = case ATUAL; o próximo sai de ORDEM_CASES (circular). `alvo` força outro."""
    ordem = dados.ORDEM_CASES
    nxt = alvo or ordem[(ordem.index(slug) + 1) % len(ordem)]
    cz = dados.CASES[nxt]
    return (f'<section class="sec nc" aria-label="Próximo case"><div class="wrap">'
            f'<a class="nc__link" href="/cases/{esc(nxt)}/"><span class="label">Próximo case · {esc(cz["segmento"])} · '
            f'{esc(cz["entregavel"])}</span><span class="t-h2 nc__t">{esc(cz["marca"])} '
            f'<span class="nc__a" aria-hidden="true">→</span></span></a>'
            f'<p class="nc__all">{link_arrow("Ver todos os cases", "/portfolio/")}</p></div></section>')


def _faq_para(p) -> tuple[str, str]:
    if isinstance(p, (tuple, list)):
        return f'<a href="{esc(p[1])}">{esc(p[0])}</a>', str(p[0])
    return esc(p), str(p)


def faq(items, label_text: str, lines, id: str = "perguntas", num: str | None = None) -> str:
    """FAQ com <details>. items = [(pergunta, [parágrafo, …])]; parágrafo pode ser (texto, href) para virar link."""
    det = []
    for i, (q, ans) in enumerate(items, 1):
        ans = [ans] if isinstance(ans, (str, tuple)) else ans
        ps = "".join(f"<p>{_faq_para(p)[0]}</p>" for p in ans)
        det.append(f'<details class="faq__item"><summary><span class="label faq__num">{i:02d}</span>'
                   f'<span class="faq__q">{esc(q)}</span><span class="faq__icon" aria-hidden="true"></span></summary>'
                   f'<div class="faq__a">{ps}</div></details>')
    return section(
        f'<div class="grid faq-sec__grid"><div class="faq-sec__head">{label(label_text, num=num, cls="label--rule")}'
        f'{title(lines, size="h2")}</div><div class="faq" data-reveal="stagger">{"".join(det)}</div></div>',
        id=id, cls="faq-sec")


def faq_text(items) -> list[tuple[str, str]]:
    """(pergunta, resposta em texto puro) para o JSON-LD."""
    out = []
    for q, ans in items:
        ans = [ans] if isinstance(ans, (str, tuple)) else ans
        out.append((q, " ".join(_faq_para(p)[1] for p in ans)))
    return out


def _srow_thumb(s) -> str:
    """Miniatura da linha de serviço (decorativa: o link já diz tudo em texto). Sem imagem: o caminho do clique."""
    th = s.get("thumb")
    if th:
        inner = picture(th, "", "(min-width:1024px) 11rem, 6rem", ratio="1/1", decorative=True)
    else:
        passos = s.get("thumb_passos") or []
        inner = "".join(f'<span class="srow__step">{esc(p)}</span>' for p in passos)
        inner = f'<span class="srow__path">{inner}</span>'
    return f'<span class="srow__thumb" aria-hidden="true">{inner}</span>'


def service_row(slug: str) -> str:
    s = dados.SERVICES[slug]
    k, m = s["kanji"]
    marks = "".join(f"<li>{esc(x)}</li>" for x in s["marcadores"])
    return (f'<article class="srow"><a class="srow__link" href="{esc(s["url"])}">'
            f'<span class="label srow__num">{esc(s["num"])}</span>'
            f'<span class="srow__kanji"><span class="kanji" lang="ja" aria-hidden="true">{esc(k)}</span>'
            f'<span class="label">{esc(m)}</span></span>'
            f'<span class="srow__body"><h2 class="t-h2 srow__t">{esc(s["titulo"])}</h2>'
            f'<span class="srow__line">{esc(s["linha"])}</span><ul class="srow__marks">{marks}</ul></span>'
            f'{_srow_thumb(s)}'
            f'<span class="link-arrow srow__go" aria-hidden="true">Ver serviço<span class="link-arrow__a link-arrow__a--in">→</span></span>'
            f'</a></article>')


def pillars_table(cls: str = "") -> str:
    """Os 5 pilares na ordem canônica, com links."""
    rows = []
    for p in dados.PILARES:
        k, m = p["kanji"]
        rows.append(f'<tr class="pillars__row"><th scope="row" class="pillars__nome">{esc(p["nome"])}</th>'
                    f'<td class="pillars__k"><span class="kanji" lang="ja" aria-hidden="true">{esc(k)}</span>'
                    f'<span class="label">{esc(m)}</span></td>'
                    f'<td class="pillars__v">{esc(p["verbo"])}</td><td class="pillars__f">{esc(p["frase"])}</td>'
                    f'<td class="pillars__o">{link_arrow(p["onde"][0], p["onde"][1])}</td></tr>')
    return (f'<table class="{_cls("pillars", cls)}"><caption class="sr">Os cinco pilares da MAYAA</caption>'
            f'<thead><tr><th scope="col">Pilar</th><th scope="col">Kanji</th><th scope="col">Verbo</th>'
            f'<th scope="col">Frase</th><th scope="col">Onde entra</th></tr></thead><tbody>{"".join(rows)}</tbody></table>')


__all__ = [n for n in dir() if not n.startswith("_")]
