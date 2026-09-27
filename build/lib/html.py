"""Utilitários de HTML (C1)."""
from __future__ import annotations

import html as _html


def esc(s) -> str:
    """Escapa texto para HTML (aspas incluídas)."""
    return _html.escape(str(s), quote=True)


def attrs(**kw) -> str:
    """attrs(cls="a b", data_reveal="lines", hidden=True, alt="") -> ' class="a b" data-reveal="lines" hidden alt=""'.
    None/False somem; True vira atributo booleano; `cls` vira `class`; `_` vira `-`."""
    out = []
    for k, v in kw.items():
        if v is None or v is False:
            continue
        name = "class" if k in ("cls", "class_") else k.rstrip("_").replace("_", "-")
        if v is True:
            out.append(f" {name}")
        else:
            out.append(f' {name}="{esc(v)}"')
    return "".join(out)


def cls(*names) -> str:
    return " ".join(n for n in names if n)


def join(items, sep: str = "") -> str:
    return sep.join(i for i in items if i)
