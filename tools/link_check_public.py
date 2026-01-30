import re
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / 'public'

def extract_urls(html: str):
    urls = []
    urls += re.findall(r'href="([^"]+)"', html)
    urls += re.findall(r'src="([^"]+)"', html)
    urls += re.findall(r'<meta[^>]+property="og:image"[^>]*content="([^"]+)"', html, flags=re.I)
    urls += re.findall(r'<meta[^>]+name="twitter:image"[^>]*content="([^"]+)"', html, flags=re.I)
    return urls

def is_external(u: str) -> bool:
    return u.startswith(('http://','https://','//','mailto:','tel:','javascript:','data:','#')) or (u.strip()=='')

def main():
    missing = []
    files = list(PUB.glob('*.html')) + list((PUB / 'articles').glob('*.html')) + list((PUB/'property').glob('*.html'))
    for f in files:
        html = f.read_text(encoding='utf-8', errors='ignore')
        for u in extract_urls(html):
            if is_external(u):
                continue
            p = urlparse(u)
            dest = (f.parent / unquote(p.path)).resolve()
            if not dest.exists():
                missing.append((str(f.relative_to(PUB)), u))
    if missing:
        print('Broken public links/files:')
        for where, u in missing[:200]:
            print('-', where, '=>', u)
        print('Total missing:', len(missing))
        raise SystemExit(1)
    print('Public link check passed ✅')

if __name__ == '__main__':
    main()

