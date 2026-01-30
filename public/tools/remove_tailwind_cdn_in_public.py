import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / 'public'

def strip_cdn(p: Path) -> bool:
    txt = p.read_text(encoding='utf-8', errors='ignore')
    new = re.sub(r'<script[^>]+src=\"https://cdn\.tailwindcss\.com[^\"]*\"[^>]*></script>\n?', '', txt, flags=re.I)
    if new != txt:
        p.write_text(new, encoding='utf-8')
        return True
    return False

def main():
    changed = 0
    files = list(PUB.glob('*.html')) + list((PUB/'articles').glob('*.html'))
    for f in files:
        if strip_cdn(f):
            changed += 1
    print('Removed Tailwind CDN script in', changed, 'public files')

if __name__ == '__main__':
    main()

