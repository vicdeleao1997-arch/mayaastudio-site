# Performance & IA para empresas — entrega

Revisão solicitada por Victor após conferir o site publicado: Humanizer em todas as páginas, clientes no lugar dos projetos e a chamada principal Performance & IA para empresas. Mantidos o retrato real, a assinatura MAYAA por Victor Mey e a identidade clara do feed. Instagram será entregue como texto para colar, conforme escolha do Victor.

## O que mudou
- Oferta no H1; contato como ação principal e clientes como ação secundária. Serviços divididos em Performance e IA na empresa, com propostas separadas.
- Home e /portfolio/ exibem 21 entradas de clientes/marcas verificadas. Três marcas do Grupo Yanguí ficam agrupadas; BVBA é marca própria em bloco separado. Exclusões anteriores preservadas. Não se atribui contratação direta da MAYAA, IA ou mídia paga a toda a lista.
- Humanizer aplicado às sete páginas, metadados, inglês da home e imagem de compartilhamento. Voz real de Victor: para, está, retorno; retiradas metáforas e slogans vazios.
- Cases antigos continuam disponíveis, com texto revisado. O ROAS histórico saiu da página comercial; fonte preservada no material de trabalho. Política de privacidade descreve o contato atual por Instagram/e-mail, sem alegar agenda automática ativa.
- Logos comprimidos em WebP sem perda: pixels RGBA idênticos, 340606 → 218920 bytes. CSS da home reunido em landing.css para reduzir requisições; fontes e retrato continuam locais.

## Xquads e qualidade
Perspectivas de Donald Miller/Emily Heyward no posicionamento, David Ogilvy na copy e UX Designer no inventário de clientes. Nota visual manual independente 8,8/10. Humanizer e as amostras de voz do Victor prevalecem sobre estilos dos agentes.

Playwright: sete páginas em 1440 e 390 px; sem imagem quebrada, overflow, âncora local inválida ou erro de JavaScript. Verificados menu/Escape/foco, PT/EN, contato, seção de clientes, exclusões, identificação da BVBA, FAQ, modo sem JavaScript e movimento reduzido. Home também conferida em 320 px.

Lighthouse local mobile, rede/CPU simuladas (não são métricas reais de visitantes):

| Página | Desempenho / Acessibilidade / Boas práticas / SEO | LCP numérico | CLS |
|---|---|---|---|
| Home | 98/100/100/100 | 2.487 s | 0.000 |
| Clientes | 100/100/100/100 | 1.055 s | 0.001 |

Impeccable final: zero achados primários; três avisos consultivos sobre borda+sombra dos botões, mantidos por pertencerem ao visual aprovado. Ajustados nomes pequenos dos clientes para 12 px. Capturas integrais de home/clientes são a evidência atual; capturas isoladas antigas clientes-390.png podem conter o header sticky na costura.

## Portão de design
| Item | Resultado |
|---|---|
| Brandbook | Poppins, cinza/branco/laranja, retrato real e assinatura preservados. |
| Anti-genérico | Oferta concreta, autor reconhecível e marcas reais; sem símbolos inventados nem cartões de benefícios iguais. |
| Referências | Direção já aprovada de Dennis/Worth/Norm; Apple como apoio à hierarquia; conteúdo atualizado por pedido expresso. |
| Motion | Hover/reveal existentes com transform/opacity; reduced motion verificado; sem novo efeito, vídeo ou WebGL. 60 fps não medido instrumentalmente. |
| Mobile | 390 e 320 px sem corte; ações principais >=44 px. |
| Acessibilidade | Lighthouse 100; foco, teclado, alt e nomes verificados. |
| Desempenho | LCP numérico <2,5 s nas duas entradas; CLS zero/0,001. |
| Provas | checks.json, lighthouse-home.json, lighthouse-clientes.json e screenshots nesta pasta. |
| Impeccable / Xquads | Zero achados primários; revisão visual manual 8,8/10. |
| Fotos / vídeo / 3D | Sem geração; fotografia real e logos existentes. Sem novos vídeos/3D. |

## Instagram para copiar
Nome: Victor Mey | Performance & IA

Bio (128 caracteres):

```text
Performance & IA para empresas
Cuido dos seus anúncios e aplico IA à rotina do seu time.
À frente da MAYAA.
Veja como trabalho ↓
```

Link: https://mayaastudio.com.br/

O pacote de posicionamento inclui sugestões de três fixados (apresentação, performance e IA) e quatro destaques (Comece aqui, Clientes, Performance, IA na prática). Nenhum perfil, post, DM ou automação do Instagram foi alterado. A agenda automática continua pendente; contatos públicos levam ao Instagram/e-mail.
