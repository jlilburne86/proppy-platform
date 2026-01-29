import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'

def fix_file(p: Path) -> bool:
    txt = p.read_text(encoding='utf-8', errors='ignore')
    new = re.sub(r'(https://cdn\.tailwindcss\.com\?plugins=[^"]+)([^>]*?)\sdefer(\s*/?>)', r'\1\2\3', txt)
    if new != txt:
        p.write_text(new, encoding='utf-8')
        return True
    return False

def main():
    changed = 0
    for p in list(DOCS.glob('*.html')) + list((DOCS/'articles').glob('*.html')):
        if fix_file(p):
            changed += 1
    print('Removed defer from Tailwind CDN in', changed, 'docs HTML files')

if __name__ == '__main__':
    main()

