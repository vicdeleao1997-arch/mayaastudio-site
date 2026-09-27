# Pedidos entre construtores (uma linha por pedido, com o nome de quem pede)

- PENDENTE VICTOR · CNPJ e razão social da MAYAA: conferir no cartão CNPJ; 41.242.625/0001-47 consta no vault como da BVBA Supply. Até lá o site sai sem CNPJ.
- legal-seo (privacidade + SEO) · A política saiu em pages/legal.py (não em privacidade.py): quem for criar privacidade.py, não crie, o caminho /privacidade/ já é deste módulo. As imagens og de §5.2 (1200×630) saem de tools/og_chrome.py (Chrome headless, fontes de build/fonts). Se o C3 também fizer tools/og.py, os dois escrevem os mesmos nomes de arquivo: o líder escolhe um e apaga o outro.
- servicos (C2) · pillars_table(): em 30-components.css o `.pillars__k .kanji` fica em linha e o kanji aparece duas vezes lado a lado ("磨磨 · otimizar"). Solução local em 50-servicos.css (`display:block;line-height:1`); o núcleo deveria absorver no componente.
- servicos (C2) · steps(layout="path") com texto, abaixo de 1024: o `max-width:28ch` do `.step__x` deixa passos curtos com o texto na mesma linha do título e os longos em duas. Solução local em 50-servicos.css (grade 2 colunas, texto sempre embaixo, alinhado ao título); o núcleo deveria absorver.
- servicos (C2) · video(): com controles nativos (modo suave e sem JS) o anel de foco do `<video>` fica cortado pelo `overflow:hidden` do `.vid__frame` e some. Solução local: `.vid__frame:has(.vid__el:focus-visible){outline:2px solid var(--tinta);outline-offset:3px}`; vale também para a home e os cases, então é do núcleo.
- servicos (C2) · case_card(): marca `data-fx="distort"` sempre, inclusive na capa do IOSE, que é anúncio com texto (§2.7.9 pede fx=False em peça com texto). Sugestão: `fx=False` quando o case for o IOSE (ou parâmetro `fx`).
- servicos (C2) · service_row() no celular: os marcadores quebram com « · » no começo da linha. Solução local em 50-servicos.css (um por linha abaixo de 640 px).
- C3 · `case_series`: aceitar `cls` na seção e HTML no `text` (hoje escapa tudo). No case Ana o link de @analauren.ai entra por troca de string em `pages/cases.py`; no IOSE e na Alumee as larguras das séries saem de seletores por id em `styles/60-cases.css` (`#formatos`, `#cha-branco`).
- C3 · mídia "1 + texto" (`cs--side`) e vídeo 9:16 no desktop ocupam 7 colunas sem teto de altura (vídeo chega a ~1.370 px). Solução local: `.case-fit` com `--ar` em `60-cases.css`; o núcleo pode absorver como padrão do `case_series`.
- C3 · `.split--rev` põe a mídia nas colunas 1 a 6, e o SPEC §3.10 pede a abertura da Alumee nas colunas 6 a 12. Usei `.case-open--rev` próprio; conferir qual dos dois vale.
- C3 · o relatório de órfãos lista `/assets/mayaa-mark-ink.png`, mas `tools/og.py` usa esse arquivo: não apagar.

## Integração · 27/09/2026 (o que foi absorvido pelo núcleo)
- servicos (C2) · kanji da tabela dos pilares, caminho do clique <1024, foco do vídeo com controles, marcadores no celular: ABSORVIDOS em `30-components.css`; regras locais tiradas de `50-servicos.css`.
- servicos (C2) · `case_card(fx=None)`: lê `cover_fx` de `CASES`; IOSE com `cover_fx=False` (sem distorção na capa com texto).
- C3 · `case_series(cls=, text_html=)`: ABSORVIDO; a troca de string do case Ana saiu de `pages/cases.py`. As larguras por id (`#formatos`, `#cha-branco`) continuam em `60-cases.css` (funcionam).
- C3 · `.case-fit`: ABSORVIDO em `30-components.css` como utilitário comum.
- C3 · `.split--rev`: sem mudança. Nenhuma página usa; a abertura da Alumee segue com `.case-open--rev` (colunas 6 a 12, como o SPEC §3.10).
- C3 / legal-seo · `mayaa-mark-ink.png`: fora do relatório de órfãos (`fontes_de_ferramenta` em `lib/checks.py`).
- legal-seo · WebSite no JSON-LD: o layout põe `WebSite` em toda página (tirado de `home.py` e `legal.py`).
- legal-seo · 404: legenda do kanji alinhada à direita no desktop (`40-home.css`).
- og duplicado: OFICIAL = `tools/og_chrome.py` (é o que está em `site/`). `tools/og.py` virou `tools/_og_pillow.py` e só roda com `--alternativo`.
- fontes: `build/fonts/*.ttf` no `build/.gitignore` (as ferramentas caem para `mayaa-leads/assets`).
