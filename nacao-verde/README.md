# Nação Verde — sistema de assinatura

Projeto da **MAYAA STUDIO** para o cliente **Nação Verde**: um sistema de
assinatura recorrente, desenvolvido junto com a proposta comercial que o
descreve. Os dois andam no mesmo passo de propósito — a proposta só promete o
que a arquitetura sustenta, e o preço só fecha quando o custo de operação está
na mesa.

| Pasta | O que é | Estado |
|---|---|---|
| [`proposta/`](proposta/) | A proposta comercial que vai ao cliente | 🟡 esqueleto — faltam os dados comerciais |
| [`sistema/`](sistema/) | Arquitetura e, depois, o código | 🟡 arquitetura decidida, código não começou |

---

## O que ainda falta para destravar

Nada aqui é dedução minha: são informações que só existem com você e com o
cliente. Enquanto não chegam, os dois documentos ficam com lacunas marcadas
`[A DEFINIR]` em vez de número inventado.

1. **Gateway de pagamento** — ver a comparação em [`sistema/ARQUITETURA.md`](sistema/ARQUITETURA.md#4--escolha-do-gateway).
2. **O que é a assinatura** — planos, preços, ciclo, período de teste, e o que
   o assinante recebe. Define metade do modelo de dados.
3. **Modelo comercial da MAYAA** — setup, mensalidade, prazo, o que entra no
   escopo e o que é fora dele.
4. **Em nome de quem ficam as contas** — gateway e hospedagem no CNPJ do
   cliente ou da MAYAA. Muda quem paga a taxa e quem responde pelo chargeback.

---

## Onde este projeto pode ser desenvolvido

| Etapa | Nuvem (sessão remota) | Local (Mac) |
|---|---|---|
| Escrever código, testes, documentação, proposta | ✅ | ✅ |
| Commit, push, PR | ✅ | ✅ |
| Chamar a API do gateway (criar plano, cobrança de teste) | ❌ egresso 403 | ✅ |
| Receber webhook do gateway | ❌ sem entrada | ✅ com túnel |
| Rodar a suíte de testes (payload simulado, sem rede) | ✅ | ✅ |

Verificado em **18/09/2026** nesta sessão: o proxy devolve `403 Forbidden` no
CONNECT para `api.stripe.com`, `api.asaas.com`, `api.pagar.me`,
`api.mercadopago.com` e `example.com`. GitHub e os registries passam.

**O que isso significa na prática:** quase todo o trabalho é nuvem. O que exige
rede aberta é a integração ponta a ponta — e essa etapa acontece melhor contra
um ambiente de *staging* publicado do que em qualquer máquina, porque é
exatamente assim que vai rodar em produção.

**O sistema em si não tem versão local.** Cobrança recorrente precisa de
servidor no ar para receber webhook, renovar, tentar de novo e bloquear acesso
quando a cobrança falha. Máquina local não faz esse papel.
