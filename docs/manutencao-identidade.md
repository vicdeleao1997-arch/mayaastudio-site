# Aplicação no site institucional — 14/11/2026

O padrão vigente está em [brandbook.md](brandbook.md). Tokens JSON em `site/assets/brand/design-tokens.json`; CSS compartilhado com o funil em `site/assets/brand/mayaa-tokens.css`. O CSS foi copiado da mesma versão aplicada ao funil, sem reinterpretar os valores. Os aliases das páginas antigas ficam em `site/assets/victor/theme.css`.

## Fonte e conteúdo

- Home canônica: `build/victor-home.html`. Após editar, executar `python build/sync-home.py`; esse comando sincroniza `site/index.html` e atualiza as versões de CSS.
- Ordem: oferta e pessoa → faixa curta → serviços → seis clientes → método → biografia e marca própria → contato geral e alternativa de e-commerce → FAQ.
- A seleção da home não retira clientes da trajetória. Todos os 24 clientes e as três marcas do Grupo Yanguí continuam em `site/portfolio/index.html`, com o catálogo confirmado em `build/clientes-publicos.json`.
- Alumee, Studio Zeca Marques, Elwing e Baesh continuam fora da lista de clientes. Casos históricos mantêm suas URLs e seus conteúdos reais.
- `build/performance-ia.py` é uma migração histórica e está protegido contra recriação da home anterior. Não executar outros geradores antigos para atualizar este design.
- Contato institucional: Instagram de Victor e `contato@mayaastudio.com.br`. Diagnóstico de e-commerce: link separado com escopo explícito; não transforma os critérios do funil em requisito para todos os clientes.

## Validação e publicação

Executar `python build/check-brandbook.py` e `git diff --check`. A conferência visual deve incluir 1440 e 390 px, menu mobile, EN/PT, teclado, foco e a navegação para serviços/clientes/contato. O script estático não substitui essa conferência.

O institucional continua no **GitHub Pages**, não no Vercel. A ação `.github/workflows/deploy-pages.yml` publica `site/` quando mudanças nessa pasta chegam a `main`; `site/CNAME` conserva o domínio. Não alterar a hospedagem nem recriar o site no projeto Vercel do funil. Integração e publicação ficam a cargo da sessão principal após QA.

Prévia local: `python -m http.server 8843 --bind 127.0.0.1 --directory site`.
