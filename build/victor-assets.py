"""Prepara fontes oficiais e avatar existente; não publica nem gera imagens com IA."""
from pathlib import Path
from urllib.request import Request, urlopen
import re
import shutil

root = Path(__file__).resolve().parent.parent
assets = root / 'site/assets/victor'
assets.mkdir(parents=True, exist_ok=True)
shutil.copy2(Path('C:/Users/vicde/posts/victormey-identidade/avatar_perfil.png'), assets / 'avatar.png')
families = {
    'poppins-400.woff2': 'Poppins:wght@400',
    'poppins-500.woff2': 'Poppins:wght@500',
    'poppins-600.woff2': 'Poppins:wght@600',
    'poppins-700.woff2': 'Poppins:wght@700',
    'poppins-800.woff2': 'Poppins:wght@800',
}
for name, family in families.items():
    css_url = 'https://fonts.googleapis.com/css2?family=' + family + '&display=swap'
    request = Request(css_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'})
    css = urlopen(request, timeout=30).read().decode()
    urls = re.findall(r'url\((https://fonts.gstatic.com/[^)]+)\)', css)
    if not urls:
        raise RuntimeError('Fonte não encontrada: ' + name)
    data = urlopen(urls[-1], timeout=30).read()
    (assets / name).write_bytes(data)
    print(name, len(data))
(assets / 'FONTES.md').write_text('Identidade dos posts finais: Poppins 400, 500, 600, 700 e 800; subconjunto latino, fontes locais de Google Fonts / fonts.gstatic.com.\nAvatar: cópia da fotografia de perfil já aprovada, sem alteração.\nFontes antigas preservadas apenas como histórico; não usadas pela identidade atual.\n', encoding='utf-8')
