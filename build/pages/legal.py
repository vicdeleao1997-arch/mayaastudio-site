"""Política de privacidade · /privacidade/ (grupo legal-seo · SPEC §3.13 e §5.2).

Texto final do SPEC, letra por letra. O controlador é a MAYAA STUDIO. CNPJ e razão social só aparecem quando
`config.CNPJ` e `config.RAZAO_SOCIAL` estiverem preenchidos (SPEC §3.0.1): o número pedido consta no vault como
CNPJ da BVBA Supply e a decisão é do Victor, com o cartão CNPJ na mão. Sem endereço comercial (não inventar).
Estilo próprio em styles/70-legal.css (prefixo .priv-); marcação da seção ativa do índice em scripts/70-legal.js.
"""
from __future__ import annotations

from urllib.parse import quote

from lib import components as c, config, seo
from lib.html import esc
from lib.page import Page

PATH = "/privacidade/"
TITLE = "Política de privacidade · MAYAA STUDIO"
DESC = ("Como o site mayaastudio.com.br trata dados pessoais, em linguagem simples: o que coleta, para quê, "
        "com quem compartilha e como exercer seus direitos.")
H1 = ["Política de", ("privacidade.", "b")]
OG = "/assets/og/og-privacidade.jpg"
OG_ALT = "MAYAA STUDIO · Política de privacidade"
CRUMBS = [("Início", "/"), ("Privacidade", None)]
ATUALIZADA = "Última atualização: 27 de setembro de 2026."

MAILTO_PRIV = f"mailto:{config.EMAIL}?subject=" + quote("Privacidade e dados pessoais", safe="")


def _mail() -> str:
    return f'<a href="{esc(MAILTO_PRIV)}">{esc(config.EMAIL)}</a>'


def _p(*parts: str) -> str:
    """Parágrafo. parts: texto puro (escapado aqui) ou HTML pronto marcado com o prefixo \x00."""
    out = "".join(x[1:] if x.startswith("\x00") else esc(x) for x in parts)
    return f"<p>{out}</p>"


def _li(bold: str | None, text: str) -> str:
    b = f"<b>{esc(bold)}</b> " if bold else ""
    return f"<li>{b}{esc(text)}</li>"


def _ul(items) -> str:
    return '<ul class="priv-list">' + "".join(_li(b, t) for b, t in items) + "</ul>"


def _controlador() -> str:
    if config.CNPJ and config.RAZAO_SOCIAL:
        return (f"O controlador dos dados é a MAYAA STUDIO (razão social {config.RAZAO_SOCIAL}, CNPJ {config.CNPJ}), "
                "estúdio de tráfego pago com IA em São Paulo.")
    if config.CNPJ:
        return (f"O controlador dos dados é a MAYAA STUDIO, CNPJ {config.CNPJ}, "
                "estúdio de tráfego pago com IA em São Paulo.")
    return "O controlador dos dados é a MAYAA STUDIO, estúdio de tráfego pago com IA em São Paulo."


def _secoes() -> list[tuple[str, str]]:
    """(título, HTML do corpo) das 11 seções, na ordem do SPEC."""
    M = "\x00" + _mail()
    return [
        ("Quem cuida dos seus dados",
         _p(_controlador() + " Para qualquer assunto de privacidade, inclusive para exercer os seus direitos, "
            "escreva para ", M, ".")),
        ("O que este site coleta",
         _ul([
             (None, "Hoje o site não tem cadastro, não tem área de login e não tem formulário que envie dados para "
                    "um servidor da MAYAA."),
             ("Links de e-mail:", "alguns botões abrem o seu programa de e-mail com o assunto e um roteiro de "
                                  "perguntas já preenchidos. Nada é enviado até você mesmo mandar o e-mail. Se mandar, "
                                  "recebemos o que você escreveu."),
             ("E-mail, Instagram e LinkedIn:", "se você nos escrever por esses canais, recebemos o que você enviar, "
                                               "junto com os dados que esses serviços mostram, como o nome e o perfil."),
             ("Sem ferramentas de análise ou de anúncio no site:", "não usamos Google Analytics, pixel de anúncio ou "
                                                                   "ferramenta parecida neste site. Se isso mudar, esta "
                                                                   "política será atualizada antes."),
         ])),
        ("Para que usamos e com qual base legal",
         _ul([
             (None, "Responder ao seu contato e preparar um diagnóstico ou proposta que você pediu: procedimentos "
                    "preliminares a um contrato, a seu pedido (art. 7º, V, da LGPD)."),
             (None, "Guardar a conversa para dar continuidade ao atendimento e nos proteger em caso de disputa: "
                    "legítimo interesse (art. 7º, IX) e exercício regular de direitos (art. 7º, VI)."),
             (None, "Cumprir obrigações legais e fiscais, se virarmos parceiros: obrigação legal (art. 7º, II)."),
             (None, "Não vendemos dados pessoais e não usamos os seus dados para decisões automatizadas."),
         ])),
        ("Serviços de terceiros que o site usa",
         _p("Para funcionar, o site carrega alguns recursos de outras empresas. Ao abrir uma página, o seu navegador "
            "se conecta a elas e informa dados técnicos, como o endereço IP e o tipo de navegador.")
         + _ul([
             ("Hospedagem:", "o site é publicado pelo GitHub Pages (GitHub, Inc.), que pode registrar o acesso para "
                             "segurança e funcionamento do serviço."),
             ("Fontes:", "as fontes do texto vêm do Google Fonts (Google)."),
             ("Bibliotecas de código:", "as animações vêm de redes de distribuição públicas, como cdnjs (Cloudflare) "
                                        "e jsDelivr."),
             ("Instagram:", "vídeos e posts do Instagram só são carregados dentro do site se você clicar para "
                            "carregar. A partir desse clique, o Instagram (Meta) pode gravar cookies e receber dados "
                            "do seu acesso, conforme a política dele."),
             ("Links externos:", "os links para o Instagram e o LinkedIn abrem esses serviços, que seguem as "
                                 "próprias políticas."),
         ])
         + _p("Essas empresas podem tratar dados fora do Brasil. Nesses casos, a transferência segue o art. 33 da "
              "LGPD, com as salvaguardas que cada uma oferece.")),
        ("Cookies",
         _p("O site da MAYAA não grava cookies próprios. Cookies de terceiros só aparecem se você carregar um conteúdo "
            "do Instagram, como explicado acima. Você pode apagar ou bloquear cookies nas configurações do seu "
            "navegador.")),
        ("Por quanto tempo guardamos",
         _p("Mensagens de contato ficam guardadas enquanto houver conversa ou relação comercial e, depois disso, pelo "
            "prazo que a lei exigir ou que for necessário para nos defender numa disputa. Quando não houver mais "
            "motivo, os dados são apagados ou anonimizados.")),
        ("Com quem compartilhamos",
         _p("Só com quem precisa para o atendimento acontecer, como o provedor de e-mail, e com autoridades quando a "
            "lei obrigar. Nunca com outras empresas para fazerem marketing.")),
        ("Os seus direitos",
         _p("Pela LGPD (art. 18), você pode pedir, a qualquer momento e sem custo:")
         + _ul([(None, t) for t in (
             "confirmação de que tratamos dados seus e acesso a eles;",
             "correção de dados incompletos, errados ou desatualizados;",
             "anonimização, bloqueio ou eliminação de dados desnecessários ou tratados em desacordo com a lei;",
             "portabilidade dos dados para outro fornecedor;",
             "informação sobre com quem compartilhamos;",
             "eliminação dos dados tratados com o seu consentimento e revogação desse consentimento.",
         )])
         + _p("Para pedir, escreva para ", M, ". Respondemos em até 15 dias. Se não ficar satisfeito, você também pode "
              "procurar a Autoridade Nacional de Proteção de Dados (ANPD).")),
        ("Segurança",
         _p("O site é servido com conexão segura (HTTPS). O acesso às mensagens recebidas fica restrito a quem trabalha "
            "no seu atendimento.")),
        ("Crianças e adolescentes",
         _p("O site é voltado a empresas e não se destina a menores de 18 anos.")),
        ("Mudanças nesta política",
         _p("Se o site passar a coletar dados de outro jeito, por exemplo com um formulário de diagnóstico que envie "
            "dados direto para a MAYAA, esta página será atualizada antes, dizendo quais dados, para quê e por quanto "
            "tempo. A data no topo mostra a última versão.")),
    ]


def _toc(secoes) -> str:
    lis = "".join(
        f'<li><a href="#p{i:02d}"><span class="label__num priv-toc__n">{i:02d}</span>'
        f'<span class="priv-toc__t">{esc(t)}</span></a></li>'
        for i, (t, _b) in enumerate(secoes, 1))
    return (f'<nav class="priv-toc" aria-labelledby="priv-toc-t" data-priv-toc>'
            f'<p class="label priv-toc__label" id="priv-toc-t">Nesta página · 11 tópicos</p>'
            f'<ol class="priv-toc__list">{lis}</ol></nav>')


def _artigos(secoes) -> str:
    """O id fica na <section> e a revelação num filho: assim o salto pelo índice mira a caixa sem transform."""
    out = []
    for i, (t, body) in enumerate(secoes, 1):
        out.append(
            f'<section class="priv-sec" id="p{i:02d}" aria-labelledby="p{i:02d}-t">'
            f'<div class="priv-sec__in" data-reveal="fade">'
            f'<h2 class="t-h3 priv-sec__t" id="p{i:02d}-t"><span class="label priv-sec__n">{i:02d}</span>'
            f'<span class="priv-sec__tt">{esc(t)}</span></h2>'
            f'<div class="priv-sec__body">{body}</div></div></section>')
    return "".join(out)


def pages():
    secoes = _secoes()
    abertura = ('<p class="priv-intro lead" data-reveal="fade">Esta política explica, em linguagem simples, como o '
                'site mayaastudio.com.br trata dados pessoais. Ela vale para este site. Se você contratar a MAYAA, o '
                'contrato traz as regras do projeto.</p>')
    corpo = (f'<section class="sec priv" aria-label="Texto da política"><div class="wrap"><div class="priv__grid">'
             f'<aside class="priv__aside">{_toc(secoes)}</aside>'
             f'<div class="priv__text">{abertura}{_artigos(secoes)}</div>'
             f'</div></div></section>')
    body = c.page_hero("LGPD · Lei 13.709/2018", H1, ATUALIZADA, crumbs=CRUMBS, h1_cls="priv-h1") + corpo
    return [Page(
        path=PATH, title=TITLE, description=DESC, h1=c.plain(H1), body=body,
        og_image=OG, og_alt=OG_ALT,
        jsonld=[seo.webpage(PATH, TITLE, DESC, OG),
                seo.breadcrumb_jsonld(CRUMBS)],
        changefreq="yearly", priority=0.3, body_class="priv-page",
    )]
