import re
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parent.parent

def iter_html_files():
    for p in ROOT.glob('*.html'):
        yield p
    for p in (ROOT / 'articles').glob('*.html'):
        yield p

def extract_urls(html: str):
    urls = []
    # href and src
    urls += re.findall(r'href="([^"]+)"', html)
    urls += re.findall(r'src="([^"]+)"', html)
    # meta content: only capture OG/Twitter images
    urls += re.findall(r'<meta[^>]+property="og:image"[^>]*content="([^"]+)"', html, flags=re.I)
    urls += re.findall(r'<meta[^>]+name="twitter:image"[^>]*content="([^"]+)"', html, flags=re.I)
    return urls

def is_external(u: str) -> bool:
    u = u.strip()
    if not u or u.startswith('#'):
        return True
    if any(u.startswith(s) for s in ('http://','https://','//','mailto:','tel:','javascript:','data:')):
        return True
    return False

def normalize(current: Path, url: str) -> Path:
    # strip fragment and query
    parsed = urlparse(url)
    path = unquote(parsed.path)
    if path.startswith('/'):
        target = ROOT / path.lstrip('/')
    else:
        target = current.parent / path
    return target.resolve()

def main():
    missing = []
    for f in iter_html_files():
        html = f.read_text(encoding='utf-8', errors='ignore')
        for u in extract_urls(html):
            if is_external(u):
                continue
            tgt = normalize(f, u)
            # Ignore anchors within same file after stripping
            if not tgt.exists():
                missing.append((f.relative_to(ROOT), u))
    if missing:
        print('Broken links/files:')
        for where, u in missing[:200]:
            print(f'- {where}: {u}')
        print(f'Total missing: {len(missing)}')
        raise SystemExit(1)
    print('All local links/assets resolve ✅')

if __name__ == '__main__':
    main()
