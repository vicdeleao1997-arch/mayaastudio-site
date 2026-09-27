"""Configuração do site (C1). Trocar um valor aqui e rodar o build atualiza todas as páginas."""
from __future__ import annotations

import os
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
BUILD = ROOT / "build"

SITE_URL = "https://mayaastudio.com.br"
LASTMOD = os.environ.get("MAYAA_LASTMOD") or date.today().isoformat()
ANO = 2026

# Contatos (§3.0.1)
IG = "https://www.instagram.com/mayaastudio.br/"      # perfil: só "Instagram ↗" e sameAs
IG_DM = "https://ig.me/m/mayaastudio.br"              # todo CTA que diga "direct"
LINKEDIN = "https://www.linkedin.com/company/mayaastudio/"
EMAIL = "contato@mayaastudio.com.br"


def _mailto(assunto: str, corpo: str | None = None) -> str:
    q = "subject=" + quote(assunto, safe="")
    if corpo:
        q += "&body=" + quote(corpo.replace("\n", "\r\n"), safe="")
    return f"mailto:{EMAIL}?{q}"


MAILTO_DIAG = _mailto(
    "Diagnóstico da conta",
    "Empresa:\nSite ou Instagram:\nOnde anuncia hoje (Meta Ads, Google Ads):\nO que vende:\nO que quer resolver:\n",
)
MAILTO_PROJETO = _mailto("Projeto audiovisual", "Empresa:\nSite ou Instagram:\nO que quer lançar:\nPara quando:\n")
MAILTO_GERAL = _mailto("Contato pelo site")

IG_ANA = "https://www.instagram.com/analauren.ai/"
IG_ANA_POST = "https://www.instagram.com/p/DdreKmjFWqC/"
REEL_ALUMEE = "https://www.instagram.com/reel/DbZFaIlBBCR/"
REEL_BVBA = "https://www.instagram.com/reel/DbjBnflO0AR/"

# CNPJ: pedido do Victor em 27/09/2026 ("MAYAA STUDIO, 41242625000147, sem endereço comercial ainda").
# O número é o da LTDA dele (razão social VICTOR MEYAGUSKO DE LEAO BASTOS PEREIRA LTDA, nome fantasia registrado
# BVBA Supply). O site mostra "MAYAA STUDIO · CNPJ ..." sem rotular "razão social", para não afirmar o que o cartão
# não diz. RAZAO_SOCIAL fica vazio: se o Victor quiser o nome da LTDA publicado, preencher aqui.
CNPJ: str | None = "41.242.625/0001-47"
RAZAO_SOCIAL: str | None = None

INDEXNOW_KEY = "f52add39abf76a763c2ac9e3440c87bb"

CDN = {
    "gsap": "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js",
    "scrolltrigger": "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js",
    "lenis": "https://cdn.jsdelivr.net/npm/@studio-freight/lenis@1.0.42/dist/lenis.min.js",
    "ogl": "https://cdn.jsdelivr.net/npm/ogl@1.0.11/+esm",
}
# Fontes no próprio site (site/assets/fonts, geradas por tools/fontes.py; @font-face em styles/00-tokens.css).
# As três aparecem na 1.ª dobra de toda página (texto em Archivo, título em Shippori Regular e Bold).
FONTS_PRELOAD = ("archivo", "shippori-400", "shippori-700")
