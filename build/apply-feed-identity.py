"""Migração local da v3 para os posts finais de 12/13 de novembro. Não publica."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
assets = root / 'site/assets/victor'
fonts = '\n'.join('@font-face{font-family:Poppins;src:url("/assets/victor/poppins-%s.woff2") format("woff2");font-weight:%s;font-style:normal;font-display:swap}' % (w,w) for w in [400,500,600,700,800])
(assets/'theme.css').write_text(fonts+'\n:root{--paper:#E9E9ED;--ink:#26262B;--heading:#141417;--accent:#FF6A1A;--muted:#5F5F68;--white:#fff;--line:#D6D6DC;--display:Poppins,sans-serif;--body:Poppins,sans-serif;--mono:Poppins,sans-serif;--ease:cubic-bezier(.22,1,.36,1)}\n',encoding='utf-8')
home = root/'build/victor-home.html'
s = home.read_text(encoding='utf-8')
s=s.replace('bricolage.woff2','poppins-800.woff2').replace('schibsted.woff2','poppins-500.woff2').replace('#F1F3F0','#E9E9ED')
s=s.replace('<p class="eyebrow" data-en="For people running a business">Para quem toca uma empresa</p>','<div class="feed-author"><img src="/assets/victor/avatar.png" alt="" width="68" height="68"><div><strong>Victor Meyagusko</strong><a href="https://www.instagram.com/victormey.ai/">@victormey.ai</a></div></div>')
s=s.replace('<div class="card-header mono"><span data-en="THE STARTING POINT">O PONTO DE PARTIDA</span><span class="status-dot" aria-hidden="true"></span></div>','<div class="card-header mono"><span class="window-dots" aria-hidden="true"><i></i><i></i><i></i></span><span data-en="The starting point">O ponto de partida</span></div>')
home.write_text(s,encoding='utf-8')
shutil.copy2(home,root/'site/index.html')
for page in (root/'site').rglob('*.html'):
    s=page.read_text(encoding='utf-8').replace('#F1F3F0','#E9E9ED').replace('bricolage.woff2','poppins-800.woff2').replace('schibsted.woff2','poppins-500.woff2')
    page.write_text(s,encoding='utf-8')
css=(assets/'home.css').read_text(encoding='utf-8')
css=css.replace('font-variation-settings:"opsz" 96;','').replace('font-stretch:78%;','')
# Replace the old palette and composition at source, with a small responsive layer below.
css=css.replace('background:var(--paper);color:var(--ink);font-family:var(--body)', 'background:radial-gradient(1200px 900px at 20% 0%,#f6f6f8 0%,#e9e9ed 55%,#dcdde2 100%);color:var(--ink);font-family:var(--body)')
css=css.replace('background:var(--ink);color:var(--white);border:1px solid var(--ink)', 'background:var(--white);color:var(--ink);border:0;box-shadow:0 12px 26px -12px #28283c38')
css=css.replace('background:#E3E7E2','background:transparent').replace('background:#e3e7e2','background:#dcdde2')
css=css.replace('background:#f8f9f7','background:#f4f4f6').replace('#e8ebe7','#ececf0')
(assets/'home.css').write_text(css,encoding='utf-8')
out=root/'qa/victor-feed-20261113'
out.mkdir(exist_ok=True)
check=(root/'qa/victor-20261113/check.mjs').read_text(encoding='utf-8').replace('qa/victor-20261113','qa/victor-feed-20261113')
(out/'check.mjs').write_text(check,encoding='utf-8')
(out/'og.html').write_text('''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><link rel="stylesheet" href="http://127.0.0.1:8843/assets/victor/theme.css"><style>*{box-sizing:border-box}body{width:1200px;height:630px;margin:0;padding:60px 75px;background:radial-gradient(1200px 900px at 20% 0%,#f6f6f8,#e9e9ed 55%,#dcdde2);color:#26262b;font-family:Poppins,sans-serif}header{display:flex;gap:20px;align-items:center}header img{width:82px;height:82px;border-radius:50%}strong{font-size:27px;font-weight:700}header p{margin:2px 0;font-size:20px;color:#5f5f68}h1{font-size:72px;font-weight:500;line-height:1.15;letter-spacing:-.03em;margin:42px 0 28px}h1 b{font-weight:800;color:#141417}.pill{display:inline-flex;gap:24px;align-items:center;padding:14px 16px 14px 26px;border-radius:60px;background:white;box-shadow:0 12px 30px #28283c22;font-size:18px}.pill i{display:grid;place-items:center;width:40px;height:40px;border-radius:50%;background:#ff6a1a;font-style:normal}</style></head><body><header><img src="http://127.0.0.1:8843/assets/victor/avatar.png" alt=""><div><strong>Victor Meyagusko</strong><p>@victormey.ai</p></div></header><h1>Tráfego pago. IA aplicada.<br><b>Mais clareza.</b></h1><div class="pill">Seu negócio. Uma conversa direta comigo.<i>↗</i></div></body></html>''',encoding='utf-8')
print('Identidade dos posts aplicada. QA em',out)
