# LEIA-ME

Como gerar o site e como acrescentar uma página: ver `README.md` nesta pasta.

Resumo: `py build/build.py` gera tudo em `site/` (modo estrito). Página nova = um módulo em `build/pages/` com
`def pages() -> list[Page]`; o build descobre sozinho.
