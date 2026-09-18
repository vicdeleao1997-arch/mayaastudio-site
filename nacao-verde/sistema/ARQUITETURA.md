# Arquitetura — sistema de assinatura Nação Verde

Documento de decisão técnica. O que está aqui é o que a proposta comercial
pode prometer; o que não está aqui não deve ser prometido.

---

## 1 · A decisão de fundo: isto é nuvem, não tem escolha

Uma assinatura recorrente não é um formulário de pagamento. É um processo que
continua rodando depois que o cliente fecha o navegador:

- o gateway precisa de **um endereço público** para avisar que a fatura foi
  paga, que o cartão falhou, que o assinante cancelou;
- alguém precisa estar de pé no **dia da renovação**, todo mês, sem ninguém
  clicar em nada;
- quando a cobrança falha, alguém precisa **tentar de novo**, avisar o
  assinante e, no fim do prazo, **cortar o acesso**.

Máquina local não faz isso. Ela dorme, troca de IP, fica atrás de NAT e não
recebe conexão de entrada. Local serve para desenvolver; produção é nuvem.

---

## 2 · Desenho

| Camada | Onde | Por quê |
|---|---|---|
| Site / landing | GitHub Pages, como o `site/` já é | Estático, rápido, sem custo, nada muda no que existe |
| Checkout | Página **hospedada pelo gateway** | O cartão nunca toca o nosso servidor — tira quase todo o peso de PCI-DSS |
| Backend (webhook + API) | Serverless: Vercel, Cloudflare Workers ou Supabase Edge | Endereço público com HTTPS, sem servidor para administrar |
| Banco | Postgres gerenciado (Supabase/Neon) | Fonte da verdade de quem está ativo |
| Área do assinante | Front no site, sessão contra o backend | Libera e bloqueia conforme o status |

> **Regra que não se negocia:** dado de cartão não passa pelo nosso código, não
> entra no nosso banco, não aparece em log. Quem guarda cartão é o gateway.
> Isso não é preciosismo — é o que mantém o escopo de PCI no mínimo e o risco
> fora do colo da MAYAA e do cliente.

---

## 3 · A máquina de estados da assinatura

É o coração do sistema, e é a parte que independe de qual gateway vencer.

```
                 pagamento aprovado
   [ pendente ] ────────────────────> [ ativa ]
        │                              │   ▲
        │ falhou / expirou             │   │ cobrança recuperada
        ▼                              ▼   │
   [ cancelada ] <──────────── [ inadimplente ]
        ▲                              │
        │  fim do prazo de tolerância  │
        └──────────── [ suspensa ] <───┘
                          │
                          └── acesso bloqueado, cadastro preservado
```

- **pendente** — checkout aberto, primeira cobrança ainda não confirmada.
- **ativa** — em dia. É o único estado que libera acesso.
- **inadimplente** — cobrança falhou; acesso segue liberado durante a
  tolerância enquanto o sistema tenta de novo (*dunning*).
- **suspensa** — acabou a tolerância. Acesso bloqueado, cadastro e histórico
  preservados para reativação sem recomeço.
- **cancelada** — por pedido do assinante ou por desistência da cobrança.
  Acesso vale até o fim do ciclo já pago.

**[A DEFINIR] com o cliente:** quantos dias de tolerância, quantas tentativas
de recobrança e se o cancelamento corta na hora ou no fim do ciclo pago. São
decisões de negócio, não técnicas — e cada uma vira uma linha da proposta.

---

## 4 · Escolha do gateway

Decisão pendente. O que pesa:

| Critério | Caminho brasileiro (Asaas, Pagar.me, Mercado Pago) | Stripe |
|---|---|---|
| Pix recorrente e boleto | Nativo, é o forte deles | Suporte limitado no Brasil |
| Emissão de NF-e / NFS-e | Alguns já fazem junto | Não faz — precisa de terceiro |
| Cartão internacional, cobrança em dólar | Fraco | É o forte dele |
| Qualidade de API e documentação | Varia bastante entre eles | Referência do mercado |
| Antifraude e disputa | Varia | Maduro |

**Recomendação:** se o assinante da Nação Verde é pessoa física no Brasil
pagando em real, com Pix e boleto na mesa, o caminho brasileiro tem menos
atrito — e a emissão de nota junto economiza um integrador inteiro. Stripe
entra se houver cobrança internacional.

> **Taxas:** deliberadamente não estão nesta tabela. Elas mudam por contrato e
> por volume, e este ambiente não alcança o site dos gateways (egresso 403)
> para conferir. Número de taxa entra na proposta **só** depois de confirmado
> na fonte ou no contrato — proposta comercial com taxa errada é problema que
> aparece no primeiro fechamento de mês.

O código isola a cobrança atrás de uma interface (`criar_assinatura`,
`cancelar`, `consultar`, `tratar_evento`), então trocar de gateway depois é
caro mas não é reescrever. Ainda assim vale decidir antes: o formato do
webhook e o modelo de ciclo de cada um são diferentes o bastante para mudar os
testes.

---

## 5 · Modelo de dados (esboço)

| Tabela | Guarda | Observação |
|---|---|---|
| `assinante` | pessoa, contato, identificação fiscal | LGPD: só o necessário, e com prazo de descarte definido |
| `plano` | nome, preço, ciclo, benefícios | Espelha o que existe no gateway, não substitui |
| `assinatura` | assinante + plano + estado + datas do ciclo | O estado da seção 3 mora aqui |
| `evento_cobranca` | todo webhook recebido, cru, com o resultado | Trilha de auditoria: sem ela, discussão de cobrança vira palavra contra palavra |

---

## 6 · Segurança e conformidade

- **Verificação de assinatura do webhook** (HMAC) em toda requisição recebida.
  Endpoint de webhook é endereço público: sem verificar, qualquer um libera
  assinatura mandando um POST.
- **Idempotência.** Gateway reenvia evento. Processar duas vezes não pode
  cobrar duas vezes nem duplicar acesso.
- **Segredos em variável de ambiente**, nunca no repositório. Chave de API de
  gateway commitada é incidente, não deslize.
- **LGPD.** Dado pessoal de assinante tem base legal (execução de contrato),
  finalidade declarada e prazo. O cliente precisa de política de privacidade no
  ar antes do primeiro pagamento real — **[A DEFINIR]** se a MAYAA redige ou o
  jurídico do cliente.

---

## 7 · O que só é testável com rede aberta

Verificado nesta sessão (18/09/2026): este ambiente remoto tem egresso negado.

| Consigo aqui | Não consigo aqui |
|---|---|
| Lógica de estados, regra de negócio | Chamar a API do gateway |
| Handler de webhook com payload simulado | Receber webhook de verdade |
| Testes automatizados, sem rede | `stripe listen` / túnel |
| Modelo de dados, migrations | Criar plano na conta real do cliente |

O teste ponta a ponta acontece contra um **staging publicado** — que é como
vai rodar em produção de qualquer forma.
