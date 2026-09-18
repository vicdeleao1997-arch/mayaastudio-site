# Proposta comercial — Sistema de assinatura

**MAYAA STUDIO** para **Nação Verde**
Versão 0.1 · rascunho interno · **não enviar ao cliente neste estado**

> **Como ler este documento.** Tudo marcado `[A DEFINIR]` é informação que só
> existe com o Victor ou com o cliente. Nada disso foi estimado, arredondado ou
> preenchido por dedução: proposta comercial com número inventado vira
> problema no primeiro fechamento de mês. As seções técnicas já estão
> fechadas, porque essas eu sei responder — saem de
> [`../sistema/ARQUITETURA.md`](../sistema/ARQUITETURA.md).

---

## 1 · O que a Nação Verde quer resolver

`[A DEFINIR]` — a dor do cliente, nas palavras dele. Hoje como é? Cobrança
manual, planilha, Pix avulso todo mês? Quantos assinantes existem, ou é do
zero? O que acontece hoje quando alguém não paga?

*Esta seção decide o tom da proposta inteira. Uma proposta que abre pelo
problema do cliente vende; uma que abre pela nossa lista de entregáveis, não.*

---

## 2 · O que entregamos

Um sistema de assinatura recorrente completo, no ar, no nome do cliente:

- **Checkout** hospedado pelo gateway — o assinante escolhe o plano e paga sem
  sair da experiência da marca.
- **Cobrança automática**, todo ciclo, sem ninguém clicar em nada.
- **Recuperação de cobrança falhada** — tentativas automáticas, aviso ao
  assinante e corte de acesso só no fim da tolerância. É aqui que a receita
  recorrente se perde ou se sustenta.
- **Área do assinante** — ver plano, atualizar forma de pagamento, cancelar
  sozinho. Cancelamento fácil reduz chargeback e é exigência de lei.
- **Painel de acompanhamento** — quantos ativos, quantos inadimplentes, quanto
  entrou no mês.
- **Trilha de auditoria** de toda cobrança, para quando houver discussão.

O desenho técnico completo está em
[`../sistema/ARQUITETURA.md`](../sistema/ARQUITETURA.md).

---

## 3 · Planos da assinatura

`[A DEFINIR]` — preenchido com o cliente.

| Plano | Preço | Ciclo | O que o assinante recebe |
|---|---|---|---|
| `[A DEFINIR]` | `[A DEFINIR]` | `[A DEFINIR]` | `[A DEFINIR]` |

Definir junto: tem período de teste? Tem plano anual com desconto? Quantos dias
de tolerância antes de suspender? Cancelamento corta na hora ou no fim do
ciclo pago?

---

## 4 · Como o sistema fica montado

| Camada | Onde roda |
|---|---|
| Site e páginas públicas | Hospedagem estática (a atual, sem mudança) |
| Checkout e guarda do cartão | Gateway — `[A DEFINIR: qual]` |
| Backend, webhook e renovação | Serverless em nuvem |
| Banco de assinantes | Postgres gerenciado |

**Por que nuvem, e não um servidor do cliente:** a cobrança recorrente precisa
de um endereço público no ar 24 horas para receber o aviso do gateway e
renovar na data. É o que torna o sistema automático em vez de uma planilha com
lembrete.

**Dado de cartão nunca passa pelo nosso código nem pelo servidor do cliente.**
Quem guarda cartão é o gateway, que já é certificado para isso.

---

## 5 · Etapas e prazo

`[A DEFINIR]` — prazos reais, depois de fechado o escopo.

| # | Etapa | Entrega | Prazo |
|---|---|---|---|
| 1 | Descoberta e modelagem dos planos | Planos e regras aprovados por escrito | `[A DEFINIR]` |
| 2 | Núcleo de cobrança e integração | Assinatura funcionando em ambiente de teste | `[A DEFINIR]` |
| 3 | Área do assinante e painel | Telas no ar em teste | `[A DEFINIR]` |
| 4 | Homologação | Teste ponta a ponta com cobrança real de valor simbólico | `[A DEFINIR]` |
| 5 | Publicação e acompanhamento | Sistema no ar, primeiro ciclo acompanhado | `[A DEFINIR]` |

> A etapa 4 não é formalidade. Cobrança recorrente só se prova de verdade
> virando o ciclo — e é melhor descobrir o que quebra com R$1,00 do que com a
> base inteira.

---

## 6 · Investimento

`[A DEFINIR]` — modelo e valores.

| Item | Valor | Quando |
|---|---|---|
| Desenvolvimento e implantação | `[A DEFINIR]` | `[A DEFINIR]` |
| Manutenção e suporte mensal | `[A DEFINIR]` | Mensal, a partir da publicação |

### Custos recorrentes de terceiros

Não são receita da MAYAA. Entram na proposta porque o cliente precisa saber o
custo real de operar — proposta que esconde isso gera atrito no mês 2.

| Item | Quem cobra | Valor |
|---|---|---|
| Taxa por transação | Gateway | `[A DEFINIR — confirmar no contrato do gateway]` |
| Hospedagem do backend | Plataforma de nuvem | `[A DEFINIR]` |
| Banco de dados | Plataforma de nuvem | `[A DEFINIR]` |
| Domínio / e-mail transacional | `[A DEFINIR]` | `[A DEFINIR]` |

**Em nome de quem ficam as contas:** `[A DEFINIR]`. Se ficarem no CNPJ do
cliente, ele paga direto, recebe direto e responde pelo chargeback — é o mais
limpo. Se ficarem na MAYAA, isso precisa estar escrito, com repasse previsto.

---

## 7 · O que não está incluído

Dizer isto por escrito evita a conversa difícil depois.

- `[A DEFINIR]` — identidade visual e criação de peças, se não estiver no escopo
- Emissão fiscal, se o gateway escolhido não fizer
- Atendimento ao assinante final (o cliente atende, o sistema entrega a informação)
- Conteúdo e operação do que a assinatura entrega
- Redação da política de privacidade e dos termos de uso, se ficar com o jurídico do cliente

---

## 8 · Próximo passo

`[A DEFINIR]` — validade da proposta, forma de aceite e o que destrava a etapa 1.
