# Nação Verde — sistema de assinatura

Projeto da **MAYAA STUDIO** para a **Nação Verde**: assinatura recorrente para
o catálogo de suplementos, dentro da loja **Shopify** que o cliente já opera,
com **PagBank** como meio de pagamento.

**Etapa atual: proposta entregue, aguardando aceite do cliente.** O
desenvolvimento só começa depois do aceite e da verificação do meio de
pagamento.

| Arquivo | O que é |
|---|---|
| [`proposta/MAYAA-Fechamento-Nacao-Verde.pdf`](proposta/MAYAA-Fechamento-Nacao-Verde.pdf) | O documento de fechamento, 3 páginas. **Pronto para enviar.** |
| [`proposta/MAYAA-Apresentacao-Nacao-Verde.pdf`](proposta/MAYAA-Apresentacao-Nacao-Verde.pdf) | A apresentação, 11 slides em 16:9. **Pronta para apresentar.** |
| [`proposta/fechamento.html`](proposta/fechamento.html) · [`apresentacao.html`](proposta/apresentacao.html) | As fontes dos dois PDFs. Editar aqui e re-renderizar |
| [`sistema/ARQUITETURA.md`](sistema/ARQUITETURA.md) | Decisão técnica interna. Código, só depois do aceite |

---

## Valor fechado

**R$ 6.000, valor único.** Sem mensalidade, revisões ilimitadas dentro do
escopo, prazo de 15 dias úteis do último insumo. Decidido pelo Victor em
18/09/2026.

Calibrado pelo precedente real do estúdio — fechamento França & Bisordi,
14/09/2026, R$ 2.000 + R$ 1.500/mês — e não por tabela de agência.

O valor cobre o **cenário A** (o meio de pagamento suporta recorrência dentro
da Shopify). No cenário B o escopo não cabe neste valor, e o documento diz
isso: escopo e valor são revistos antes de começar. A recomendação, nesse
caso, é somar um segundo meio de pagamento só para o fluxo de assinatura.

---

## O que ainda depende de terceiros

1. **A pergunta do PagBank** — ver
   [`sistema/ARQUITETURA.md`](sistema/ARQUITETURA.md#1--a-pergunta-que-decide-tudo).
   Precede o início e decide entre os dois cenários.
2. **O layout da página de produto** — prints bastam. Não foi possível
   analisar nesta sessão (egresso bloqueado).
3. **Planos, descontos e regras** de pausa, troca e cancelamento — a etapa 1
   do próprio projeto.

---

## O padrão do PDF

Referência: `MAYAA-Fechamento-Franca-Bisordi.pdf` (enviado pelo Victor, não
versionado aqui por ser documento de outro cliente). Reproduzido em
`fechamento.html`.

Fundo `paper` `#F6F4EF`, texto `ink` `#0B0B0B`, display em serifa mincho,
corpo em Archivo. Tarja de cabeçalho, marca do gato, bloco
`CLIENTE / ESTÚDIO / DATA`, resumo em negrito, itens numerados `01…`,
`CONDIÇÕES` em corpo miúdo e a caixa preta do `INVESTIMENTO` com o valor em
serifa grande. Rodapé centralizado. Fechamento na página 1, anexos depois,
assinados *Victor · MAYAA STUDIO*.

As fontes ficam em [`proposta/assets/fonts/`](proposta/assets/fonts/) — Shippori
Mincho no display e Archivo no texto, vindas do npm (Fontsource, licença SIL
OFL) porque este ambiente não alcança o Google Fonts. O subconjunto japonês
tem só os cinco glifos de まやー工房, 1,6 KB em vez de 1,4 MB.

### Como regerar os PDFs

```bash
cd nacao-verde/proposta
CHROME=/caminho/para/chrome   # no Mac: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless --no-pdf-header-footer \
  --print-to-pdf="MAYAA-Fechamento-Nacao-Verde.pdf" fechamento.html
"$CHROME" --headless --no-pdf-header-footer \
  --print-to-pdf="MAYAA-Apresentacao-Nacao-Verde.pdf" apresentacao.html
```

O documento sai em A4 e a apresentação em 16:9 — o tamanho vem do `@page` de
cada arquivo, não da linha de comando.

---

## Onde este projeto pode ser desenvolvido

| Etapa | Nuvem (sessão remota) | Local (Mac) |
|---|---|---|
| Redigir proposta, gerar o PDF, documentar | ✅ | ✅ |
| Commit, push, PR | ✅ | ✅ |
| Ver o layout de `nacaoverde.com.br` | ❌ egresso 403 | ✅ |
| Falar com a API do PagBank ou do Shopify | ❌ egresso 403 | ✅ |
| Receber webhook de cobrança | ❌ sem entrada | ✅ com túnel |

Verificado em **18/09/2026**: o proxy devolve `403 Forbidden` no CONNECT para
`nacaoverde.com.br`, `api.stripe.com`, `api.asaas.com`, `api.pagar.me`,
`api.mercadopago.com` e `example.com`. GitHub e os registries do npm passam —
foi por eles que as fontes chegaram.

**O sistema em si não tem versão local.** Cobrança recorrente precisa de algo
no ar para cobrar na data, tentar de novo quando falha e cortar o acesso no
fim da tolerância. Máquina local não faz esse papel — no cenário A, quem faz é
o Shopify com o app de assinatura.
