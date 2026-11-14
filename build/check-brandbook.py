"""Valida invariantes de conteúdo e referências locais da aplicação do brandbook."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import json
import re

root = Path(__file__).resolve().parents[1]
site = root / 'site'
class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.references = [], []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        for key in ('href', 'src'):
            if key in a: self.references.append(a[key])

files = list(site.rglob('*.html'))
documents = {p: Document(p.read_text(encoding='utf-8')) for p in files}
errors = []
for path, doc in documents.items():
    for id_, count in Counter(doc.ids).items():
        if count > 1: errors.append(f'{path.relative_to(site)}: id duplicado {id_}')
    for ref in doc.references:
        url = urlsplit(ref)
        if url.scheme or url.netloc: continue
        target = (site / unquote(url.path).lstrip('/')) if url.path.startswith('/') else (path.parent / unquote(url.path) if url.path else path)
        if target.is_dir(): target /= 'index.html'
        target = target.resolve()
        if not target.exists(): errors.append(f'{path.relative_to(site)}: referência ausente {ref}')
        elif url.fragment and target in documents and url.fragment not in documents[target].ids:
            errors.append(f'{path.relative_to(site)}: âncora ausente {ref}')

home = (site / 'index.html').read_text(encoding='utf-8')
portfolio = (site / 'portfolio/index.html').read_text(encoding='utf-8')
assert home == (root / 'build/victor-home.html').read_text(encoding='utf-8'), 'Home e fonte divergentes'
assert home.index('id="servicos"') < home.index('id="clientes"') < home.index('id="metodo"')
assert len(re.findall(r'<li class="client-tile(?: [^"]*)?">', home)) == 6
clients = json.loads((root / 'build/clientes-publicos.json').read_text(encoding='utf-8'))
expected = [c for c in clients if c['relation'] == 'cliente']
assert len(expected) == 24
assert len(re.findall(r'<li class="client-tile(?: [^"]*)?">', portfolio)) == len(expected)
from html import escape
for client in expected: assert escape(client['name']) in portfolio, client['name']
for name in ('Alumee', 'Studio Zeca Marques', 'Elwing', 'Baesh'):
    assert name.casefold() not in (home + portfolio).casefold(), name
for path in files:
    text = path.read_text(encoding='utf-8')
    if '/assets/victor/theme.css' in text:
        assert '/assets/brand/mayaa-tokens.css' in text, path
assert not errors, '\n'.join(errors)
print(f'OK: {len(files)} páginas; referências locais e âncoras; 6 clientes na home e 24 no portfólio; exclusões e fonte preservadas.')
