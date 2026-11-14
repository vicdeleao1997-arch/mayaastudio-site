"""Aplicação local da direção aprovada em13/11. Não publica nem usa gerador antigo."""
from pathlib import Path
import re
import json

root = Path(__file__).resolve().parents[1]
source = root / 'build/victor-home.html'
html = source.read_text(encoding='utf-8')
if 'agency.css' in html:
    raise SystemExit('Direção já aplicada. Edite build/victor-home.html e as páginas canônicas; este patch de migração não deve ser repetido.')
hero = ''' <section class="hero wrap" aria-labelledby="hero-title">
  <div class="hero-copy">
   <p class="eyebrow" data-en="Paid media · Creative work · Applied AI">Tráfego pago · Criação · IA aplicada</p>
   <h1 id="hero-title">MAYAA.<br><span data-en="By Victor Mey.">Por Victor Mey.</span></h1>
   <p class="intro" data-en="I'm Victor. I lead MAYAA and connect strategy, creative work and technology to the day-to-day work of your business.">Sou o Victor. Eu lidero a MAYAA e conecto estratégia, criação e tecnologia ao dia a dia do seu negócio.</p>
   <div class="hero-actions"><a class="button" href="#recentes"><span data-en="Explore the work">Ver projetos</span><span class="arrow" aria-hidden="true">↓</span></a><a class="text-link" href="#contato"><span data-en="Talk to Victor">Falar com Victor</span><span aria-hidden="true">↗</span></a></div>
   <a class="hero-handle" href="https://www.instagram.com/victormey.ai/" target="_blank" rel="noopener noreferrer">@victormey.ai <span aria-hidden="true">↗</span></a>
  </div>
  <figure class="founder-portrait">
   <img src="/assets/victor/victor-retrato.webp" alt="Victor Mey, à frente da MAYAA" width="772" height="772" fetchpriority="high" decoding="async">
   <figcaption><span><strong>Victor Meyagusko</strong><span data-en="The person behind MAYAA">À frente da MAYAA</span></span><a href="#estudio" aria-label="Conheça o Victor"><span aria-hidden="true">↗</span></a></figcaption>
  </figure>
 </section>'''
html = re.sub(r' <section class="hero wrap".*?</section>', hero, html, count=1, flags=re.S)
services = re.search(r' <section id="servicos".*?</section>', html, re.S).group(0)
html = html.replace(services, '')
work = ''' <section id="recentes" class="wrap section work-section" aria-labelledby="work-title">
  <div class="section-heading"><div><p class="eyebrow" data-en="Selected projects">Projetos selecionados</p><h2 id="work-title" data-en="The work,<br>up close.">O trabalho,<br>de perto.</h2></div><div><p data-en="A product, a story, an idea. Each project starts with a different challenge.">Um produto, uma história, uma ideia. Cada projeto parte de um desafio diferente.</p><a class="text-link" href="/portfolio/"><span data-en="View the full portfolio">Ver portfólio completo</span><span aria-hidden="true">↗</span></a></div></div>
  <div class="work-grid">
   <a class="work-link" href="/cases/bvba-surrealismo/"><div class="work-image"><img src="/assets/cases/bvba-surrealismo/cover.jpg" alt="Editorial da BVBA Supply em um cenário surreal de museu criado com IA" width="800" height="1000" loading="lazy" decoding="async"><span class="image-action" aria-hidden="true">↗</span></div><div class="work-caption"><span class="mono" data-en="Fashion · Art direction &amp; AI">Moda · Direção de arte e IA</span><h3>BVBA Supply</h3><p data-en="Real clothes. An imaginary museum. Film and editorial with AI.">Roupa real. Museu imaginário. Filme e editorial com IA.</p><span class="project-index" aria-hidden="true">01</span></div></a>
   <a class="work-link" href="/cases/alumee-vela-mel/"><div class="work-image"><img src="/assets/cases/alumee-vela-mel/cover.jpg" alt="Vela Mel da Alumee com mel sobre a tampa de madeira" width="800" height="1000" loading="lazy" decoding="async"><span class="image-action" aria-hidden="true">↗</span></div><div class="work-caption"><span class="mono" data-en="Product · Launch campaign">Produto · Campanha de lançamento</span><h3>Alumee · Mel</h3><p data-en="The product's details guide the images for its launch.">Os detalhes do produto dão o caminho para as imagens do lançamento.</p><span class="project-index" aria-hidden="true">02</span></div></a>
  </div>
  <a class="work-feature" href="/cases/ana-lauren-modelo-ia/"><div class="feature-image"><img src="/assets/cases/ana-lauren-modelo-ia/cover.jpg" alt="Ana Lauren, personagem criada com inteligência artificial" width="800" height="1000" loading="lazy" decoding="async"></div><div class="feature-copy"><span class="mono" data-en="03 / Digital character">03 / Personagem digital</span><h3>Ana Lauren</h3><p data-en="A character created with AI. The same identity, across different stories and scenes.">Uma personagem criada com IA. A mesma identidade, em diferentes histórias e cenas.</p><span class="text-link"><span data-en="Explore the project">Conhecer o projeto</span><span aria-hidden="true">↗</span></span></div></a>
  <p class="work-disclaimer" data-en="These cases document creative work and production processes. Sales performance is evaluated separately.">Os cases documentam criação e processo de produção. Resultados de vendas são avaliados separadamente.</p>
 </section>'''
html = re.sub(r' <section id="recentes".*?</section>', work + '\n' + services, html, count=1, flags=re.S)
html = html.replace('The person behind the work', 'The person behind MAYAA').replace('Quem está por trás</p>', 'Quem está por trás da MAYAA</p>')
html = html.replace("I'm Victor.<br>I work alongside your business.", "From the first conversation<br>to the work itself.").replace('Sou o Victor.<br>E trabalho junto do seu negócio.', 'Da primeira conversa<br>ao trabalho na prática.')
html = html.replace('I work with paid media, creative production and applied AI. These are parts of my own day-to-day work, not just topics in a presentation.', 'I lead MAYAA. I work with paid media, creative production and applied AI. You talk to me about your goals, the scope and the decisions along the way.').replace('Eu trabalho com tráfego pago, produção criativa e IA aplicada. São partes do meu dia a dia, não só assuntos de uma apresentação.', 'Eu lidero a MAYAA. Trabalho com tráfego pago, produção criativa e IA aplicada. Você conversa comigo sobre os objetivos, o escopo e as decisões ao longo do projeto.')
contact = '''  <div id="contato" class="diagnostic-contact"><span class="mono" data-en="LET'S TALK ABOUT YOUR PROJECT">VAMOS FALAR DO SEU PROJETO</span><a class="button" href="https://www.instagram.com/victormey.ai/" target="_blank" rel="noopener noreferrer"><span data-en="Talk to Victor">Falar com Victor</span><span class="arrow" aria-hidden="true">↗</span></a><p class="contact-hint" data-en="Tell me about your brand and what you want to build. I'll help you define the next step.">Me conte sobre sua marca e o que você quer construir. Eu te ajudo a definir o próximo passo.</p><a class="contact-secondary" href="mailto:contato@mayaastudio.com.br">contato@mayaastudio.com.br</a><div class="commerce-path"><strong data-en="Looking for paid media for your online store?">Procura tráfego pago para sua loja?</strong><a class="contact-secondary" href="https://diagnostico.mayaastudio.com.br/diagnostico/ecommerce" data-en="Answer the diagnostic and see available times ↗">Responder ao diagnóstico e ver horários ↗</a><p data-en="Availability is shown after qualification.">Os horários são apresentados após a qualificação.</p></div></div>'''
html = re.sub(r'  <div id="contato".*?</div>\s*</section>', contact + '\n </section>', html, count=1, flags=re.S)
html = html.replace('Victor Mey · Tráfego pago e IA aplicada', 'MAYAA por Victor Mey · Tráfego, criação e IA')
html = html.replace('content="Victor Mey"', 'content="MAYAA por Victor Mey"')
html = html.replace('href="#diagnostico"><span data-en="Let\'s talk">Vamos conversar', 'href="#contato"><span data-en="Talk to Victor">Falar com Victor')
html = html.replace('href="#diagnostico" data-en="The diagnostic">Conhecer o diagnóstico', 'href="#contato" data-en="Talk to Victor">Falar com Victor')
html = html.replace('aria-label="victormey.ai, início"', 'aria-label="MAYAA por Victor Mey, início"')
brand = '<span class="brand-name">MAYAA<span class="brand-period">.</span><small data-en="by Victor Mey">por Victor Mey</small></span>'
html = html.replace('<span class="brand-dot" aria-hidden="true"></span>victormey.ai', brand)
html = html.replace('© <span data-year>2026</span> Victor Mey', '© <span data-year>2026</span> MAYAA · Victor Mey')
html = html.replace('content="Victor Mey. Tráfego pago. IA aplicada. Mais clareza."', 'content="MAYAA por Victor Mey. Tráfego, criação e IA aplicada."')
for weight in (400,700):
    html = html.replace('<link rel="stylesheet"', f'<link rel="preload" href="/assets/victor/poppins-{weight}.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="stylesheet"',1)
source.write_text(html, encoding='utf-8')
(root/'site/index.html').write_text(html, encoding='utf-8')

# Manter os casos existentes e alinhar o cabeçalho/autoria em todas as páginas.
for page in (root/'site').glob('**/index.html'):
    if page == root/'site/index.html':
        continue
    text = page.read_text(encoding='utf-8')
    text = text.replace('aria-label="victormey.ai, início"', 'aria-label="MAYAA por Victor Mey, início"')
    text = text.replace('<span class="brand-dot" aria-hidden="true"></span><span>victormey.ai</span>', '<span class="brand-name">MAYAA<span class="brand-period">.</span><small>por Victor Mey</small></span>')
    text = text.replace('<span>Conversar</span>', '<span>Falar com Victor</span>')
    text = text.replace('© <span data-year>2026</span> Victor Mey', '© <span data-year>2026</span> MAYAA · Victor Mey')
    text = text.replace('content="Victor Mey"', 'content="MAYAA por Victor Mey"')
    text = text.replace(' | Victor Mey', ' | MAYAA por Victor Mey')
    text = text.replace('"@type": "WebSite",\n        "name": "Victor Mey"', '"@type": "WebSite",\n        "name": "MAYAA por Victor Mey"')
    for weight in (400,500,700,800):
        preload = f'<link rel="preload" href="/assets/victor/poppins-{weight}.woff2" as="font" type="font/woff2" crossorigin>'
        if preload not in text:
            text = text.replace('<link rel="stylesheet"',preload+'\n<link rel="stylesheet"',1)
    if '/cases/' in page.as_posix():
        text = text.replace('<dl class="hero-meta reveal">','<p class="case-author">Um projeto MAYAA · Direção de Victor Mey <a href="/#estudio">Conheça quem está por trás ↗</a></p>\n    <dl class="hero-meta reveal">',1)
    page.write_text(text,encoding='utf-8')

portfolio = root/'site/portfolio/index.html'
p = portfolio.read_text(encoding='utf-8')
start = p.index('<section class="sec sec--light phero"')
stop = p.index('<section class="sec sec--light" style="border-top:',start)
replacement = '''<section class="sec portfolio-intro">
 <div class="wrap">
  <nav class="crumbs" aria-label="Caminho"><a href="/">Início</a><span aria-hidden="true">/</span><span aria-current="page">Portfólio</span></nav>
  <div class="portfolio-heading"><div><p class="kicker">Portfólio MAYAA</p><h1>Ideias que<br>ganham forma.</h1></div><div class="portfolio-author"><img src="/assets/victor/avatar.png" alt="Victor Mey" width="64" height="64"><p><strong>Por Victor Mey.</strong>Direção, criação e tecnologia.<br><a href="/#estudio">Conheça meu trabalho ↗</a></p></div></div>
  <p class="portfolio-intro-copy">Três projetos, três desafios. Explore as peças e veja como cada ideia foi construída.</p>
 </div>
</section>
<section class="sec portfolio-projects" aria-label="Projetos selecionados"><div class="wrap">
 <div class="portfolio-grid">
  <a class="portfolio-project" href="/cases/bvba-surrealismo/"><div class="project-media"><img src="/assets/cases/bvba-surrealismo/cover.jpg" width="800" height="1000" alt="Editorial BVBA em um museu surreal criado com IA" fetchpriority="high" decoding="async"><span aria-hidden="true">↗</span></div><div class="project-caption"><span class="kicker">01 / Moda · Filme e editorial</span><h2>BVBA Supply</h2><p>Filme e editorial com roupa real em um museu construído com IA.</p><p class="project-role">Direção de arte · Cenário e composição</p></div></a>
  <a class="portfolio-project" href="/cases/alumee-vela-mel/"><div class="project-media"><img src="/assets/cases/alumee-vela-mel/cover.jpg" width="800" height="1000" alt="Vela Mel da Alumee com mel sobre madeira e vidro" fetchpriority="high" decoding="async"><span aria-hidden="true">↗</span></div><div class="project-caption"><span class="kicker">02 / Produto · Lançamento</span><h2>Alumee · Mel</h2><p>Imagens de lançamento criadas a partir do produto real, preservando seus detalhes.</p><p class="project-role">Direção de arte · Imagens com IA e reel</p></div></a>
  <a class="portfolio-project project-wide" href="/cases/ana-lauren-modelo-ia/"><div class="project-media"><img src="/assets/cases/ana-lauren-modelo-ia/cover.jpg" width="800" height="1000" alt="Ana Lauren, personagem digital criada com IA" loading="lazy" decoding="async"><span aria-hidden="true">↗</span></div><div class="project-caption"><span class="kicker">03 / Personagem digital</span><h2>Ana Lauren</h2><p>Personagem criada com IA, mantendo a mesma identidade em diferentes cenas.</p><p class="project-role">Identidade visual · Ensaios e conteúdo</p><span class="project-more">Explorar o projeto <span aria-hidden="true">↗</span></span></div></a>
 </div>
 <p class="portfolio-note">Aqui você encontra criação e processo. Cada página detalha o escopo do trabalho apresentado.</p>
</div></section>
'''
p = p[:start]+replacement+p[stop:]
p = p.replace('>Clientes</div>', '>Trajetória</div>')
p = p.replace('Marcas diferentes, o mesmo rigor.', 'Experiências em diferentes projetos e contextos profissionais. Não significa contratação direta de todas as marcas pela MAYAA.')
p = p.replace('>Iniciar projeto</span>', '>Falar com Victor</span>')
p = p.replace('href="/trafego-pago-com-ia/" class="nav-link reveal" style="font-size:15px">Como eu trabalho', 'href="/#metodo" class="nav-link reveal" style="font-size:15px">Como eu trabalho')
p = p.replace('<link rel="stylesheet" href="/assets/pages/pages.css" />', '<link rel="stylesheet" href="/assets/pages/pages.css" />\n<link rel="stylesheet" href="/assets/victor/portfolio.css" />')
portfolio.write_text(p,encoding='utf-8')
print('Home, portfólio e assinatura das páginas alinhados. Sem deploy.')
