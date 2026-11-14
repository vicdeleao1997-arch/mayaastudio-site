"""Aplica a mensagem aprovada por Victor; preserva o retrato e a navegação."""
from pathlib import Path
import json
import re
from html import escape

ROOT = Path(__file__).resolve().parents[1]
clients = json.loads((ROOT / 'build/clientes-publicos.json').read_text(encoding='utf-8'))

def logo_image(logo):
    return f'<img src="{escape(logo)}" alt="" loading="lazy" decoding="async">'


def grid():
    items = []
    for client in clients:
        if client['relation'] != 'cliente':
            continue
        name = escape(client['name'])
        logo = client.get('logo')
        children = [brand for brand in clients if brand.get('group') == client['name']]
        classes = ['client-tile']
        if logo:
            mark_class = ' client-mark--dark' if client.get('logo_background') == 'dark' else ''
            media = f'<div class="client-mark{mark_class}">{logo_image(logo)}</div>'
        else:
            classes.append('client-tile--text')
            media = ''
        brands = ''
        if children:
            classes.append('client-tile--group')
            brand_items = []
            for brand in children:
                brand_name = escape(brand['name'])
                brand_logo = logo_image(brand['logo']) if brand.get('logo') else ''
                brand_items.append(f'<li>{brand_logo}<span>{brand_name}</span></li>')
            brands = f'<ul class="client-brands" aria-label="{name}">{"".join(brand_items)}</ul>'
        items.append(f'<li class="{" ".join(classes)}">{media}<span class="client-name">{name}</span>{brands}</li>')
    return '<ul class="client-grid">' + '\n'.join(items) + '</ul>'

source = (ROOT / 'build/victor-home.html').read_text(encoding='utf-8')
head = source.split('<body id="top">')[0]
head = re.sub(r'<title>.*?</title>', '<title>Performance &amp; IA para empresas | MAYAA por Victor Mey</title>', head)
description = 'Sou Victor Mey. Trabalho com gestão de anúncios, criativos e implantação de IA na rotina das empresas. Conheça os clientes que já atendi.'
head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m[1]+description, head)
head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m[1]+'Performance &amp; IA para empresas | MAYAA por Victor Mey', head)
head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m[1]+description, head)
head = re.sub(r'(<meta property="og:image:alt" content=")[^"]*', lambda m: m[1]+'MAYAA por Victor Mey. Performance &amp; IA para empresas.', head)
head = head.replace('Especialista em tráfego pago e IA aplicada', 'Performance e IA para empresas')
if 'clients.css' not in head:
    head = head.replace('<link rel="stylesheet" href="/assets/victor/agency.css">', '<link rel="stylesheet" href="/assets/victor/agency.css">\n<link rel="stylesheet" href="/assets/victor/clients.css">')
if '/assets/victor/poppins-600.woff2' not in head:
    head = head.replace('<link rel="stylesheet" href="/assets/victor/theme.css">', '<link rel="preload" href="/assets/victor/poppins-600.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="preload" href="/assets/victor/victor-retrato.avif" as="image" type="image/avif" fetchpriority="high">\n<link rel="stylesheet" href="/assets/victor/theme.css">')
header = source.split('<body id="top">')[1].split('<main id="conteudo">')[0]
header = header.replace('data-en="Work">Trabalhos', 'data-en="Clients">Clientes')
portrait = re.search(r'<figure class="founder-portrait">.*?</figure>', source, re.S)[0]
footer = source[source.index('<footer class="footer wrap">'):]
footer = footer.replace('data-en="Work">Trabalhos','data-en="Clients">Clientes').replace('data-en="Paid media, creative work and applied AI.">Tráfego pago, criação e IA aplicada.', 'data-en="Performance &amp; AI for businesses.">Performance &amp; IA para empresas.')
main = '''
<main id="conteudo">
 <section class="hero wrap" aria-labelledby="hero-title">
  <div class="hero-copy">
   <p class="eyebrow" data-en="MAYAA by Victor Mey">MAYAA por Victor Mey</p>
   <h1 id="hero-title" class="performance-title" data-en="Performance<br>&amp; AI<span>for businesses.</span>">Performance<br>&amp; IA<span>para empresas.</span></h1>
   <p class="intro" data-en="I'm Victor. I manage your ads and put AI to work on the tasks that take up your team's time.">Sou o Victor. Cuido dos seus anúncios e aplico IA às tarefas que tomam tempo do seu time.</p>
   <div class="hero-actions"><a class="button" href="#contato"><span data-en="Talk to Victor">Falar com Victor</span><span class="arrow" aria-hidden="true">↗</span></a><a class="text-link" href="#clientes"><span data-en="Meet the clients">Conhecer clientes</span><span aria-hidden="true">↓</span></a></div>
   <a class="hero-handle" href="https://www.instagram.com/victormey.ai/" target="_blank" rel="noopener noreferrer">@victormey.ai <span aria-hidden="true">↗</span></a>
  </div>
  PORTRAIT
 </section>
 <div class="wrap expertise-strip"><span class="mono" data-en="HOW I CAN HELP">COMO POSSO AJUDAR</span><div class="expertise-list"><span data-en="Paid media">Tráfego pago</span><span aria-hidden="true">/</span><span data-en="Ad creative">Criativos</span><span aria-hidden="true">/</span><span data-en="AI at work">IA na empresa</span></div></div>
 <section id="clientes" class="wrap section clients-section" aria-labelledby="clients-title">
  <span id="recentes" class="anchor-alias" aria-hidden="true"></span>
  <div class="section-heading"><div><p class="eyebrow" data-en="My experience">Minha trajetória</p><h2 id="clients-title" data-en="Clients I've<br>worked with.">Clientes que<br>já atendi.</h2></div><div><p data-en="I've worked with these companies directly and through agencies, at different points in my career.">Atendi essas empresas diretamente e em projetos com outras agências, em diferentes momentos da minha carreira.</p><a class="text-link" href="/portfolio/"><span data-en="More about my experience">Conhecer minha trajetória</span><span aria-hidden="true">↗</span></a></div></div>
  CLIENTGRID
  <div class="own-brand"><img src="/assets/clients/bvba.png" alt="BVBA Supply" width="481" height="160" loading="lazy"><p data-en="I'm also the founder of <strong>BVBA Supply</strong>, my clothing brand. There, I work on the store, marketing and day-to-day operations.">Também sou fundador da <strong>BVBA Supply</strong>, minha marca de roupas. Lá, acompanho a loja, o marketing e a operação no dia a dia.</p></div>
 </section>
 <section id="servicos" class="wrap section" aria-labelledby="services-title">
  <div id="manifesto" class="section-heading reveal"><div><p class="eyebrow" data-en="Services">Como posso ajudar</p><h2 id="services-title" data-en="Your ads.<br>Your team's work.">Seus anúncios.<br>A rotina do seu time.</h2></div><p data-en="You can hire me for either area. We agree on the work and the investment based on what your business needs.">Você pode me contratar para uma dessas frentes. O trabalho e o investimento são definidos de acordo com o que a sua empresa precisa.</p></div>
  <div class="services">
   <article class="service-row reveal"><span class="service-num mono">01</span><h3>Performance</h3><div><p data-en="I plan and manage Meta and Google Ads campaigns, develop ad creative and review the data to understand which ads bring in enquiries and sales.">Planejo e acompanho campanhas no Meta e no Google Ads, desenvolvo os criativos e analiso os dados para entender quais anúncios trazem contatos e vendas.</p><a class="service-detail" href="/trafego-pago-com-ia/" data-en="See how I manage campaigns ↗">Conheça o trabalho de tráfego pago ↗</a></div></article>
   <article class="service-row reveal"><span class="service-num mono">02</span><h3 data-en="AI for your business">IA na empresa</h3><div><p data-en="I identify repetitive tasks and build AI workflows using your existing tools. The work includes implementation and adjustments with the people who will use it.">Identifico tarefas repetitivas e monto rotinas com IA nas ferramentas que você já usa. O trabalho inclui a implantação e os ajustes com quem vai usar no dia a dia.</p><span class="service-tags" data-en="AI implementation is scoped separately from campaign management.">A implantação de IA tem uma proposta própria, separada da gestão de campanhas.</span></div></article>
  </div>
 </section>
 <section id="metodo" class="wrap section method" aria-labelledby="method-title">
  <div class="reveal"><p class="eyebrow" data-en="How I work">Como eu trabalho</p><h2 id="method-title" data-en="First, I need to understand your business.">Primeiro, preciso conhecer sua empresa.</h2><p class="section-intro" data-en="What do you sell? How do customers reach you? Which tasks take up your team's time? That's where we start.">O que você vende? Como os clientes chegam? Quais tarefas ocupam o seu time? É por aí que começamos.</p></div>
  <ol class="method-list">
   <li class="reveal"><span class="step">01</span><div><h3 data-en="A conversation with you">Uma conversa com você</h3><p data-en="You tell me what you want to improve. I look at what you already do, the tools you use and the data you have.">Você me conta o que quer melhorar. Eu olho para o que já é feito, as ferramentas que vocês usam e os dados disponíveis.</p></div></li>
   <li class="reveal"><span class="step">02</span><div><h3 data-en="A proposal with deliverables and a timeline">Uma proposta com entregas e prazo</h3><p data-en="We agree on what I will do, what your team needs to provide, the cost and how we'll assess the work.">Combinamos o que vou fazer, o que preciso do seu time, quanto custa e como vamos avaliar o trabalho.</p></div></li>
   <li class="reveal"><span class="step">03</span><div><h3 data-en="Follow-up throughout the work">Acompanhamento do trabalho</h3><p data-en="During the project, I show you what's been done, review the results with you and explain any changes needed.">Durante o projeto, mostro o que foi feito, reviso os resultados com você e explico os ajustes necessários.</p></div></li>
  </ol>
 </section>
 <section id="estudio" class="wrap section about" aria-labelledby="about-title">
  <div class="reveal"><p class="eyebrow" data-en="The person behind MAYAA">Quem está à frente da MAYAA</p><h2 id="about-title" data-en="I'm Victor.">Sou o Victor.</h2></div>
  <div class="about-copy reveal"><p data-en="I lead MAYAA. I've worked with companies in retail, services and industry, both directly and as part of agency teams.">Eu lidero a MAYAA. Já trabalhei com empresas de comércio, serviços e indústria, tanto em atendimentos diretos quanto em equipes de agências.</p><p data-en="You talk directly to me about the work, from the first meeting through to delivery. On Instagram, I share what I'm testing and how I use AI in my own work.">Você conversa diretamente comigo sobre o trabalho, da primeira reunião até a entrega. No Instagram, compartilho o que estou testando e como uso IA na minha própria rotina.</p><div class="profile"><img src="/assets/victor/avatar.webp" alt="Foto de perfil de Victor Mey" width="82" height="82" loading="lazy"><div><strong>Victor Mey</strong><a href="https://www.instagram.com/victormey.ai/" target="_blank" rel="noopener noreferrer">@victormey.ai ↗</a></div></div></div>
 </section>
 <section id="diagnostico" class="wrap diagnostic-section" aria-labelledby="diagnostic-title">
  <div><p class="eyebrow" data-en="Contact">Vamos conversar</p><h2 id="diagnostic-title" data-en="What do you want to improve in your business?">O que você quer melhorar na sua empresa?</h2><p data-en="Send me a message about your business and what you need help with. It could be your ads, your ad creative or a task you'd like to automate.">Me mande uma mensagem contando sobre sua empresa e o que precisa de atenção. Pode ser uma campanha, os criativos ou uma tarefa que você gostaria de automatizar.</p></div>
  <div id="contato" class="diagnostic-contact"><span class="mono" data-en="TALK DIRECTLY TO ME">FALE DIRETAMENTE COMIGO</span><a class="button" href="https://www.instagram.com/victormey.ai/" target="_blank" rel="noopener noreferrer"><span data-en="Talk to Victor">Falar com Victor</span><span class="arrow" aria-hidden="true">↗</span></a><p class="contact-hint" data-en="The button opens my Instagram profile. Send me a direct message there.">O botão abre meu perfil no Instagram. Você pode me chamar por mensagem por lá.</p><a class="contact-secondary" href="mailto:contato@mayaastudio.com.br">contato@mayaastudio.com.br</a></div>
 </section>
 <section class="wrap faq-section" aria-labelledby="faq-title"><h2 id="faq-title" data-en="Questions about the work">Dúvidas sobre o trabalho</h2><div class="faq">
  <details><summary data-en="Do I need to know about AI?">Preciso entender de IA?</summary><p data-en="No. Tell me what your team does today and where the difficulties are. I'll explain what can be done, the costs and what it requires from you.">Não. Me conte o que o seu time faz hoje e onde estão as dificuldades. Eu explico o que pode ser feito, os custos e o que preciso de vocês.</p></details>
  <details><summary data-en="Do you only work with online stores?">Você atende só lojas online?</summary><p data-en="I also work with service and B2B businesses. In our first conversation, we check whether I can help with what you need.">Também trabalho com empresas de serviços e negócios B2B. Na primeira conversa, avaliamos se consigo ajudar no que você precisa.</p></details>
  <details><summary data-en="Can I hire just one service?">Posso contratar só um dos serviços?</summary><p data-en="Yes. You can hire campaign management, ad creative or an AI implementation project. Each proposal sets out the deliverables, timing and cost.">Sim. Você pode contratar gestão de campanhas, produção de criativos ou um projeto de implantação de IA. Cada proposta define as entregas, o prazo e o valor.</p></details>
  <details><summary data-en="Do you guarantee sales?">Você garante vendas?</summary><p data-en="I can't guarantee sales. They also depend on your offer, pricing and service. I track the results of the work and explain where I see room for improvement.">Não consigo garantir vendas. Elas também dependem da sua oferta, do preço e do atendimento. Eu acompanho os resultados do trabalho e explico onde vejo espaço para melhorar.</p></details>
 </div></section>
</main>
'''.replace('PORTRAIT', portrait).replace('CLIENTGRID', grid())
# Um único CSS na home evita encadear folhas durante a primeira renderização.
css = '\n'.join((ROOT / 'site/assets/victor' / name).read_text(encoding='utf-8') for name in ['theme.css', 'agency.css', 'clients.css'])
(ROOT / 'site/assets/victor/landing.css').write_text(css, encoding='utf-8')
head = re.sub(r'<link rel="stylesheet" href="/assets/victor/(?:theme|agency|clients|landing)\.css">', '', head)
head = head.replace('</head>', '<link rel="stylesheet" href="/assets/victor/landing.css">\n</head>')
home = head + '<body id="top">' + header + main + footer
(ROOT/'build/victor-home.html').write_text(home, encoding='utf-8')
(ROOT/'site/index.html').write_text(home, encoding='utf-8')

p = ROOT/'site/portfolio/index.html'
s = p.read_text(encoding='utf-8')
s = s.replace('Trabalhos</a>', 'Clientes</a>').replace('Portfólio | MAYAA por Victor Mey', 'Clientes | MAYAA por Victor Mey')
desc = 'Clientes que Victor Mey já atendeu diretamente e em projetos com agências. Conheça sua trajetória em marketing e a MAYAA.'
s = s.replace('Portfólio de Victor Mey: fashion film com IA, campanha de lançamento, modelo sintética licenciável e gestão de tráfego pago. Um case por página.', desc)
s = s.replace('<link rel="stylesheet" href="/assets/victor/portfolio.css" />', '<link rel="stylesheet" href="/assets/victor/clients.css" />')
schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)[1])
for item in schema['@graph']:
    if item['@type'] == 'CollectionPage':
        item['name'] = 'Clientes | MAYAA por Victor Mey'
        item['description'] = desc
        item['mainEntity'] = {'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':c['name']} for i,c in enumerate(clients) if c['relation']=='cliente']}
    if item['@type'] == 'BreadcrumbList': item['itemListElement'][1]['name'] = 'Clientes'
s = re.sub(r'(<script type="application/ld\+json">).*?(</script>)', lambda m: m[1]+json.dumps(schema,ensure_ascii=False)+m[2], s, flags=re.S)
body = '''<main id="conteudo">
<section class="sec clients-intro"><div class="wrap"><nav class="crumbs" aria-label="Caminho"><a href="/">Início</a><span aria-hidden="true">/</span><span aria-current="page">Clientes</span></nav><p class="kicker">A trajetória de Victor Mey</p><h1>Clientes que<br>já atendi.</h1><p class="lead muted">Trabalhei com essas empresas em momentos diferentes da minha carreira, em atendimentos diretos e em equipes de agências.</p></div></section>
<section class="sec clients-directory" aria-label="Clientes atendidos"><div class="wrap">CLIENTGRID
<div class="own-brand"><img src="/assets/clients/bvba.png" alt="BVBA Supply" width="481" height="160" loading="lazy"><div><h2>Minha marca: BVBA Supply.</h2><p>Sou fundador da BVBA. Além do trabalho com clientes, acompanho a loja, as campanhas e a operação da minha marca de roupas.</p></div></div></div></section>
<section class="sec cta-band"><div class="wrap"><p class="kicker">Performance &amp; IA para empresas</p><h2 class="display h-lg">Vamos falar<br>da sua empresa?</h2><p class="lead muted">Me conte como você trabalha hoje e o que quer melhorar.</p><div class="cta-row"><a class="btn" href="https://www.instagram.com/victormey.ai/" target="_blank" rel="noopener noreferrer">Falar com Victor <span aria-hidden="true">↗</span></a><a href="/#servicos" class="nav-link">Conhecer os serviços</a></div></div></section>
</main>'''.replace('CLIENTGRID',grid())
s = re.sub(r'<main id="conteudo">.*?</main>', lambda _:body,s,flags=re.S)
s = s.replace('Tráfego pago, IA e trabalho de verdade.','Performance &amp; IA para empresas.').replace('href="/#diagnostico">Diagnóstico', 'href="/#servicos">Serviços').replace('href="/#diagnostico" class="nav-link">Conhecer o diagnóstico ↗', 'href="/#contato" class="nav-link">Falar com Victor ↗')
p.write_text(s,encoding='utf-8')
print('Home e página de clientes atualizadas.')
