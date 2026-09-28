# Gerador do site mayaastudio.com.br

Site estático gerado por Python (stdlib + Pillow). A fonte fica em `build/`; a saída vai para `site/`, que é a pasta
publicada pelo GitHub Pages. O servidor não roda build nenhum: o que está em `site/` é o que vai ao ar.
Especificação completa: `SPEC.md` da reconstrução (texto final, componentes, checks).

## Gerar

```
py build/build.py                         # tudo, modo estrito (build final: checks precisam passar)
py build/build.py --only home,sistema     # só esses módulos de pages/ (não reescreve sitemap/robots)
py build/build.py --tolerante             # módulo com erro é pulado; erros de check viram aviso
py build/build.py --sem-checks
py build/tools/bandas_e_icones.py         # faixas da home + favicon/ícones/manifest (pula o que já existe; --forcar refaz)
py build/tools/indexnow.py --seco         # mostra o envio do IndexNow (o envio real só depois de publicado, com ok do Victor)
py build/tools/og_chrome.py               # imagens og 1200×630 (gerador OFICIAL; Chrome headless; --so mayaa,privacidade)
py build/tools/derive_images.py           # versões -800 e .webp das imagens dos cases (pula o que já existe)
py build/tools/fontes.py                  # fontes do site (woff2 recortado): rodar de novo se entrar kanji novo (check 16)
py build/tools/logos.py                   # logos de clientes em tinta, no tamanho exibido (fonte: assets/clients/*.png)
py build/tools/svg_leve.py                # sprite.svg e favicon.svg leves (fonte de alta fidelidade em build/brand/)
```

O build:
1. concatena `styles/*.css` em ordem alfabética → `site/assets/css/main.css` e `scripts/*.js` → `site/assets/js/main.js`
   (hash de 8 caracteres em `?v=`);
2. descobre sozinho todo `pages/*.py` e chama `pages()` de cada um;
3. recusa caminho duplicado, grava cada página com escrita atômica (`/x/` → `site/x/index.html`);
4. no build completo, grava `sitemap.xml`, `robots.txt` e a chave IndexNow;
5. roda `lib/checks.py` (travessão, alt, links, H1, termos proibidos, prova 12,55×, direct, pilares, JSON-LD, tamanho…).

Nunca apaga nada de `site/`. Não toca `site/CNAME`.

Imagens og: o gerador oficial é `tools/og_chrome.py`. `tools/_og_pillow.py` é a alternativa em Pillow (mesmos nomes
de saída; só roda com `--alternativo`). Fontes: `build/fonts/*.ttf` fica fora do git (17 MB); sem elas as ferramentas
usam `C:/Users/vicde/mayaa-leads/assets`. `site/assets/mayaa-mark-ink.png` é fonte do gato das og: não apagar.

## Página nova = um módulo em `pages/`

```python
# build/pages/minha_pagina.py
from lib import components as c, config, dados, seo
from lib.page import Page

def pages():
    h1 = ["Título", ("em negrito.", "b")]
    body = (
        c.page_hero("Rótulo · 01", h1, "Lead da página.", kanji=("創", "criar"),
                    crumbs=[("Início", "/"), ("Minha página", None)])
        + c.section(c.head("O que fazemos", num="01", lines=["Linha", ("negrito.", "b")], text="Parágrafo."),
                    c.deliv_list(["Item um", "Item dois"]))
        + c.cta("CONTA", "02 · Contato")
    )
    return [Page(path="/minha-pagina/", title="Minha página · MAYAA STUDIO",
                 description="Entre 110 e 165 caracteres, única no site…",
                 h1=c.plain(h1), body=body, og_image="/assets/og/og-mayaa.jpg", og_alt="…",
                 jsonld=[seo.webpage("/minha-pagina/", "Minha página · MAYAA STUDIO", "…", "/assets/og/og-mayaa.jpg"),
                         seo.breadcrumb_jsonld([("Início", "/"), ("Minha página", None)])],
                 nav="servicos", priority=0.8)]
```

- Não precisa registrar o módulo em lugar nenhum. Nome com `_` na frente é ignorado.
- Cabeçalho, menu, moldura, rodapé, `<head>`, Organization no JSON-LD e scripts entram sozinhos (`lib/layout.py`).
- Se a página não tem `cta`/`cta_final`, o `id="contato"` vai para a coluna Contato do rodapé.
- Imagens: sempre caminho absoluto (`/assets/...`). `picture()` lê width/height do arquivo e monta `srcset`/WebP com os
  irmãos que existirem (`-800`, `-2400`, `.webp`); falha se o arquivo não existe ou se o alt está vazio.
- CSS próprio da página: um arquivo seu em `styles/` (`50-servicos.css`, `60-cases.css`) com prefixo de classe do
  módulo (`.srv-…`, `.case-…`, `.pf-…`). JS só se precisar: `scripts/65-cases.js`, registrando com
  `window.MAYAA.register('nome', fn)`.

## Quem escreve o quê (paralelo sem conflito)

| Construtor | Arquivos |
|---|---|
| C1 · núcleo + home | `build.py`, `lib/*`, `styles/00..40-*.css`, `scripts/00..60,90-*.js`, `pages/home.py`, `pages/sistema.py`, `tools/bandas_e_icones.py`, `tools/indexnow.py` |
| C2 · serviços, pilar, privacidade | `pages/servicos.py`, `pages/pilar.py`, `pages/privacidade.py`, `styles/50-servicos.css` |
| C3 · portfólio, cases, imagens | `pages/portfolio.py`, `pages/cases.py`, `styles/60-cases.css`, `scripts/65-cases.js`, `tools/derive_images.py`, `fonts/*` (fora do git) |

Precisa de mudança num arquivo de outro? Não edite: escreva uma linha em `PEDIDOS.md` e siga com solução local.
Enquanto os outros constroem, rode `py build/build.py --only <seus módulos> --tolerante`.

## Componentes (`lib/components.py`, importe como `c`)

Títulos: `lines` = lista de str (Regular) ou `(texto, "b")` (Bold); `c.plain(lines)` dá o texto corrido para `Page.h1`.
Parâmetros marcados HTML recebem o retorno de outro componente (`c.btn(...)`, `c.mail_cta(...)`…).

| Função | Nota |
|---|---|
| `label(text, num=None, tag="p", cls="")` | `"01 · Serviços"` já separa o número sozinho. `cls="label--rule"` põe fio em cima |
| `title(lines, tag="h2", size="h2", cls="", id=None, sep=" ")` | `size` ∈ mega, h1, display, h2, h3 |
| `head(label_text, num, lines, text)` · `section(*html, id, tone, cls, extra_ids)` · `paras(text)` | atalhos de seção (`tone`: None, "cartao", "tinta") |
| `btn(text, href, kind="primary"\|"ghost", sr=None)` · `link_arrow(text, href, sr=None)` · `text_link(text, href)` | seta automática: → interno, ↗ externo (nova aba + aviso para leitor de tela), ↓ âncora `#x` |
| `mail_cta(config.MAILTO_*, kind="ghost", pre=None)` | e-mail visível + "Copiar e-mail" |
| `kanji(char, meaning, size="md"\|"lg"\|"xl")` | só 間 知 築 創 磨 展 |
| `index_nav(items)` · `marquee_logos()` · `band(src, alt, cap_left, cap_right=(txt, href), pos="50% 55%", height="alta")` | `marquee_logos`: parede estática a partir de 1024 px, marquee abaixo (sem animação com movimento reduzido). `band(height="cine")`: faixa min(62svh, 620px), 16:9 no celular (home) |
| `figure(src, alt, caption, num, style="tec"\|"desc", ratio, fx, link)` · `image_grid(items, cols, ratio, offset)` | `tec`: "Editorial · 02"; `desc`: "01 · Descrição". `fx=False` em peça com texto |
| `video(src, poster, label, caption, num, link=(txt, href))` · `ig_embed(url, kind, what, link_text)` | |
| `deliv_list(items)` · `steps(items, layout="grid"\|"path")` · `note(text, link=(txt, href))` · `list_links(items)` | `steps`: str, `(título, texto)` ou dict |
| `service_block(...)` · `manifesto(...)` · `process(...)` · `proof(tone, num_label, link, cta=False)` | `proof` tem texto fixo; com `num_label` (pilar) some o link "Como lemos uma conta"; `cta=True` põe o direct ao lado da prova (home). `service_block` sem `items` põe a mídia na coluna lateral |
| `cta_final(label, lines, text, primary, secondary, note)` · `cta("CONTA"\|"PROJETO"\|"COLECAO"\|"MODELO", label, secondary=None)` | `cta()` já traz o texto de §3.0.4 |
| `breadcrumb(items)` · `page_hero(label, lines, lead, kanji, ctas, crumbs, extra, side="")` | `side` (HTML): mídia ou lista na coluna direita da abertura (col 9 a 12) |
| `case_hero(slug, lead, ficha_rows, badge=None)` · `ficha(rows)` · `case_card(slug, size, heading, fx=None)` | rótulo e H1 saem de `CASES` (exceções da BVBA e da Ana já embutidas; `lines=`/`label_text=` forçam). `fx=None` lê `cover_fx` de `CASES` (IOSE = sem distorção, capa com texto) |
| `case_series(num, title, text, items, kanji, layout="auto", cls="", text_html=None)` · `next_case(slug)` | `text_html`: texto com link já em HTML. Mídia de proporção natural: envolver em `.case-fit` com `style="--ar:L/A"`. `next_case` recebe o case ATUAL e mostra o próximo da ordem, com capa 21:9 (`_NC_CAPA`); o IOSE fica tipográfico |
| `faq(items, label, lines, id="perguntas")` | parágrafo pode ser `(texto, href)` para virar link; `seo.faq_jsonld(items)` usa o mesmo `items` |
| `service_row(slug)` · `pillars_table()` · `pillars_line()` | |

SEO (`lib/seo.py`): `webpage(path, name, description, og_image, kind="WebPage")`, `service(slug)`, `item_list(urls)`,
`creative_work(...)`, `video_bvba()`, `faq_jsonld(items)`, `breadcrumb_jsonld(items)` (o `@id` é completado pelo layout).

## Movimento (`scripts/`)

`data-reveal` = `lines` · `fade` · `stagger` · `mask` · `count`, revelado por IntersectionObserver. Nada começa invisível
no CSS; sem JS ou sem GSAP, tudo aparece. `prefers-reduced-motion: reduce` = modo "suave" (reveals curtos, contadores,
marquee lento; sem Lenis, parallax, "respira", WebGL e autoplay). ScrollTrigger só no parallax das faixas, sem pin.

## Testar

```
py -m http.server <porta livre> --bind 127.0.0.1 -d site
```
Chrome headless 1440×900 e 390×844, com e sem `prefers-reduced-motion: reduce`: console sem erro, nada invisível no
fim da rolagem, sem rolagem lateral. Encerrar o servidor no fim.
