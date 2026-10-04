# mayaastudio-site

Repositório único da MAYAA STUDIO. Cada projeto ocupa sua própria pasta.

| Pasta | Projeto | O que é |
|---|---|---|
| [`site/`](site/) | **Site MAYAA STUDIO** | A página pública de mayaastudio.com.br — `index.html` e `assets/`. |
| [`bvba/`](bvba/) | **BVBA Supply®** | O antigo `bvba-qa`: agente de drop da Nuvemshop (Python), plano de marketing, QA de imagens, pesquisa e o material de imigração canadense. Ver [`bvba/README.md`](bvba/README.md). |
| [`nacao-verde/`](nacao-verde/) | **Nação Verde** | Sistema de assinatura recorrente e a proposta comercial que o descreve. Em desenvolvimento. Ver [`nacao-verde/README.md`](nacao-verde/README.md). |

## Como o site é publicado

O site não fica na raiz, então o GitHub Pages **não** o serve direto da
branch — quem publica é [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml),
que empacota `site/` e entrega ao Pages a cada push em `main`.

Isso exige `Settings > Pages > Source` em **GitHub Actions**. O domínio
personalizado vem de `site/CNAME`, que viaja junto no artefato.

## Sobre a fusão

O `bvba-qa` entrou por merge de subtree: os 23 commits dele continuam
alcançáveis pelo `git log` daqui, nada foi achatado ou reescrito, e o
repositório de origem segue intacto no GitHub.

Os workflows do BVBA ficaram em `bvba/.github/workflows/` e por isso estão
**dormentes** — o GitHub só executa workflows em `.github/workflows/` na
raiz. O cron que publica o drop na Nuvemshop continua rodando no repositório
`bvba-qa`, que é onde estão os secrets. Para reativá-los aqui seria preciso
mover os arquivos para a raiz e recadastrar os secrets neste repositório.
