"""Sincroniza a fonte atual da home, sem regenerar conteúdo histórico."""
from pathlib import Path
from hashlib import sha256
import re

root = Path(__file__).resolve().parents[1]
source = root / 'build/victor-home.html'
s = source.read_text(encoding='utf-8')
def version(match):
    asset = match[1]
    digest = sha256((root / 'site' / asset.lstrip('/')).read_bytes()).hexdigest()[:12]
    return f'{asset}?v={digest}'
s = re.sub(r'(/assets/[^"\s]+\.css)(?:\?[^"\s]*)?', version, s)
source.write_text(s, encoding='utf-8')
(root / 'site/index.html').write_text(s, encoding='utf-8')
print('Home sincronizada; conteúdo e clientes não regenerados.')
