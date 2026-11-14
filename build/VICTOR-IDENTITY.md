# Identidade Victor · 13/11/2026

**Direção atual aprovada: MAYAA por Victor Mey.** Depois da pesquisa pela skill `referencias-de-site`, Victor confirmou «Pode seguir»: Dennis Snellenberg para presença pessoal, Worth Agency para galeria e Norm Architects para contexto das imagens. Esta decisão mantém a paleta/Poppins do feed e torna Victor o rosto e líder da agência no site. Substitui o trecho histórico abaixo que retirava MAYAA da assinatura.

Implementação vigente: home em `build/victor-home.html` → `site/index.html`; CSS `site/assets/victor/agency.css` + `theme.css`; portfólio em `site/portfolio/index.html` + `portfolio.css`; cabeçalho/autoria dos casos em `site/assets/pages/pages.css`. `home.css` é a revisão anterior preservada. `build/portfolio-direction.py` é patch de migração já aplicado, com trava contra repetição. Não executar os geradores anteriores para recriar a home.

Produto/direção: `PRODUCT.md` e `DESIGN.md`. QA vigente: `qa/portfolio-20261113/`. Foto real do Victor em AVIF com fallback WebP, sem geração/retoque; OG em `og-mayaa-victor.png`. Contato geral direciona ao próprio Victor; diagnóstico de e-commerce permanece alternativa específica. Publicação e conexão real do funil ainda dependem das etapas já registradas.

**Histórico da etapa anterior: identidade dos posts finais.** Após a primeira prévia, Victor pediu o visual dos últimos posts do feed. Valem `carrossel_claro.html` e `claro_final_*.jpg` de 12/13 de novembro: Poppins, cinza suave, avatar/nome/@, cartões brancos e pílulas com laranja. A referência v3/Bricolage descrita historicamente abaixo foi substituída. QA dessa etapa anterior: `qa/victor-feed-20261113/ENTREGA.md`.

A revisão anterior substituía a marca pública MAYAA por@victormey.ai; a direção atual acima passa a assinar MAYAA por Victor Mey. O site continua estático em `site/`, servido pelo GitHub Pages. Nenhum deploy foi feito nesta revisão.

- Fonte da home: `build/victor-home.html`; copiar para `site/index.html` após editar.
- Fontes, estilos e interação da home: `site/assets/victor/`; `build/victor-assets.py` baixa fontes do Google Fonts e copia o avatar aprovado.
- Páginas internas: os seis HTML de `site/portfolio`, `trafego-pago-com-ia`, `privacidade`, `cases/*` são canônicos. Seus estilos e navegação estão em `site/assets/pages/`.
- Não executar o gerador antigo para reconstruir a marca: ele mantém templates, validações e bundles MAYAA. A guarda em `build.py` interrompe antes de qualquer escrita.
- Domínio e e-mail mantidos, pois são endereços reais. Link de Instagram atualizado para @victormey.ai. O formulário/agenda de captação fica em outro repositório e não foi modificado por este redesign.
- Cabeçalhos, conteúdo, SEO, schema, fontes e OG precisam continuar com a mesma identidade nas sete páginas.
- `main` publica automaticamente. Aprovação do Victor antes de push que dispare deploy.

Brandbook: `10 - Projetos/VICTOR — FDE/Identidade visual @victormey.ai.md` no vault. Amostra aprovada: `C:/Users/vicde/posts/victormey-identidade/v3/desk.png`. Referências auxiliares: Linear (hierarquia e demonstração do trabalho), Framer (projeto apresentado com contexto); não copiar paletas, logos nem conteúdo dessas marcas.

QA e screenshots desta revisão: `qa/victor-20261113/`. Nenhuma rotina, anúncio ou backend foi reativado.

## Publicação autorizada em 13/11
Victor solicitou «Publique o site para eu conferir». O deploy usa GitHub Pages existente; não migrar a hospedagem nesta etapa. Por enquanto, os CTAs de e-commerce usam o Instagram do Victor: a rota automática respondeu 404 na checagem pré-publicação. Restaurar o link do diagnóstico apenas após seu backend e agenda funcionarem em produção.
