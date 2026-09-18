# Nação Verde — sistema de assinatura

Projeto da **MAYAA STUDIO** para a **Nação Verde**: assinatura recorrente para
o catálogo de suplementos, dentro da loja **Shopify** que o cliente já opera,
com **PagBank** como meio de pagamento.

**Etapa atual: orçamento.** O desenvolvimento só começa depois do valor
fechado — decisão do Victor em 18/09/2026.

| Pasta | O que é | Estado |
|---|---|---|
| [`proposta/`](proposta/) | O documento de fechamento que vai ao cliente | 🟡 rascunho — refazer no padrão MAYAA |
| [`sistema/`](sistema/) | [`ARQUITETURA.md`](sistema/ARQUITETURA.md) — decisão técnica. Código, só depois | ✅ arquitetura escrita |

---

## Valor proposto, à espera de confirmação

Calibrado pelo precedente real da MAYAA (fechamento França & Bisordi,
14/09/2026: R$ 2.000 + R$ 1.500/mês), não por tabela de mercado.

| Cenário | Implantação | Mensal | Mínimo |
|---|---|---|---|
| **A** — PagBank suporta recorrência no Shopify | **R$ 6.000** | R$ 1.200/mês | 3 meses |
| **B** — exige motor de recorrência próprio | R$ 18.000 | R$ 1.500/mês | 6 meses |

Se cair no cenário B, a recomendação é **somar um gateway que suporte
assinatura só no fluxo recorrente**, mantendo o PagBank no avulso — sai muito
mais barato que construir motor próprio.

---

## O que falta para gerar o PDF final

1. **Confirmar o valor e o prazo** a praticar.
2. **Responder a pergunta do PagBank** — ver
   [`sistema/ARQUITETURA.md`](sistema/ARQUITETURA.md#1--a-pergunta-que-decide-tudo).
   Decide entre os dois cenários e, portanto, o orçamento inteiro.
3. **Ver o layout da página de produto** — prints bastam. Não foi possível
   analisar nesta sessão (egresso bloqueado).
4. **Confirmar a fonte serifada** do padrão MAYAA. O PDF de referência usa uma
   serifa mincho; a reprodução vai de Shippori Mincho, que é a que o site
   declara na classe `.jp`.

---

## O padrão do PDF

Referência: `MAYAA-Fechamento-Franca-Bisordi.pdf` (enviado pelo Victor, não
versionado aqui por ser documento de outro cliente).

Fundo `paper` `#F6F4EF`, texto `ink` `#0B0B0B`, display em serifa mincho,
corpo em Archivo. Tarja de cabeçalho, marca do gato, bloco
`CLIENTE / ESTÚDIO / DATA`, resumo em negrito, itens numerados `01…`,
`CONDIÇÕES` em corpo miúdo e a caixa preta do `INVESTIMENTO` com o valor em
serifa grande. Rodapé centralizado. Fechamento na página 1, anexos depois,
assinados *Victor · MAYAA STUDIO*.

As fontes ficam em [`proposta/assets/fonts/`](proposta/assets/fonts/) — vêm do
npm (Fontsource, licença SIL OFL) porque este ambiente não alcança o Google
Fonts.

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
