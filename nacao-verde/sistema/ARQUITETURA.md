# Arquitetura — assinatura Nação Verde (Shopify + PagBank)

Documento interno. Sustenta o que o orçamento promete; o que não está aqui não
deve ser prometido.

> **Reescrito em 18/09/2026.** A versão anterior deste arquivo supunha site
> estático e backend próprio. Errado: a loja é **Shopify** e o gateway é
> **PagBank**. Isso muda a arquitetura inteira — e muda o orçamento.

---

## 1 · A pergunta que decide tudo

**O PagBank suporta contrato de assinatura dentro do Shopify?**

Não é detalhe de implementação. É a pergunta que separa um projeto de porte
médio de um projeto duas a três vezes maior, e precisa ser respondida **antes**
de fechar o valor.

Por quê: no Shopify, assinatura recorrente não é "cobrar de novo". O gateway
precisa **guardar o meio de pagamento** (tokenização/*vaulting*) e aceitar que
a loja dispare a cobrança sozinha, sem o cliente presente — o que o Shopify
chama de *subscription contract*. Nem todo gateway integrado ao Shopify faz
isso. No Brasil, poucos fazem.

| | Cenário A — o PagBank suporta | Cenário B — não suporta |
|---|---|---|
| Como funciona | App de assinatura do ecossistema Shopify, cobrando pelo PagBank | Plataforma de recorrência por fora, devolvendo o pedido ao Shopify a cada ciclo |
| O que construímos | Planos, vitrine, portal do assinante, régua de comunicação | Tudo do A **mais** o motor de recorrência, a sincronia de pedidos e a auditoria |
| Esforço | Médio | **2 a 3 vezes maior** |
| Risco | Baixo | Médio — duas fontes de verdade para manter em acordo |

**Como responder:** confirmar com o suporte do PagBank e com a documentação do
app dele no Shopify se há suporte a *subscriptions / pagamento recorrente com
cartão tokenizado*. Não dá para responder desta sessão — o ambiente remoto tem
egresso negado (403 no CONNECT, verificado em 18/09/2026).

Se a resposta for não, há três saídas, em ordem de preferência:
1. **Adicionar** um gateway que suporte assinatura só para o fluxo recorrente,
   mantendo o PagBank no avulso;
2. plataforma de recorrência externa (cenário B);
3. trocar de gateway — o mais caro em negociação, o mais barato em código.

---

## 2 · Desenho no cenário A

| Camada | Onde | Observação |
|---|---|---|
| Loja e checkout | Shopify | Nada é reconstruído. O checkout continua o do Shopify. |
| Planos de assinatura | *Selling plans* do Shopify | Ficam presos ao produto — o mesmo NAC vende avulso e assinatura |
| Vitrine da assinatura | Tema, na página de produto | É onde o layout já construído entra |
| Cobrança e guarda do cartão | PagBank | Cartão nunca toca nosso código |
| Portal do assinante | App + tema | Pausar, trocar, cancelar sem abrir chamado |
| Comunicação | E-mail transacional | Aviso antes de cobrar, recibo, falha, cancelamento |

> **Regra que não se negocia:** dado de cartão não passa pelo nosso código, não
> entra em banco nosso, não aparece em log. Quem guarda cartão é o gateway.

---

## 3 · A máquina de estados

Vale nos dois cenários. É a regra de negócio que o cliente precisa aprovar por
escrito antes de qualquer linha de código.

```
                 1ª cobrança aprovada
   [ pendente ] ────────────────────> [ ativa ] <──── [ pausada ]
        │                              │   ▲              ▲
        │ falhou                       │   │ recuperada   │ a pedido
        ▼                              ▼   │              │
   [ cancelada ] <──────────── [ inadimplente ] ──────────┘
        ▲                              │
        │   fim da tolerância          │
        └──────────── [ suspensa ] <───┘
```

Decisões pendentes com o cliente, cada uma vira linha do orçamento:
- quantos dias de tolerância antes de suspender;
- quantas tentativas de recobrança, e em que intervalo;
- cancelamento corta na hora ou no fim do ciclo já pago;
- pode pausar? por quantos ciclos?
- troca de produto dentro do mesmo plano é permitida?

---

## 4 · Particularidades de Shopify que afetam o custo

- **Taxa adicional por gateway externo.** O Shopify cobra um percentual extra
  quando a loja não usa o Shopify Payments. O valor muda conforme o plano da
  loja — **confirmar no painel do cliente**, não estimar.
- **Tema.** Se o tema for personalizado (e o layout indica que é), o widget de
  assinatura não "cai pronto": precisa ser integrado à mão para não quebrar o
  design. É a maior parte do trabalho de front.
- **App de assinatura** costuma ter mensalidade própria, às vezes com
  percentual sobre a receita recorrente. Entra como custo do cliente, não como
  receita da MAYAA.
- **Checkout Extensibility.** Personalização no checkout só é possível dentro
  do que o Shopify permite. Promessa de customização de checkout precisa ser
  verificada antes de virar escopo.

---

## 5 · O que este ambiente não alcança

Verificado em 18/09/2026: proxy devolve `403 Forbidden` no CONNECT para
`api.stripe.com`, `api.asaas.com`, `api.pagar.me`, `api.mercadopago.com`,
`example.com` e para **`nacaoverde.com.br`**. Só GitHub e registries passam.

Consequência: o layout de referência da página de produto **não pôde ser
analisado** nesta sessão. As estimativas de front assumem tema personalizado de
complexidade média. Ver o layout pode mexer nessa linha — para cima ou para
baixo.
