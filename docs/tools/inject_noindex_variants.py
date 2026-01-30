import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def inject_noindex(p: Path) -> bool:
    txt = p.read_text(encoding='utf-8', errors='ignore')
    if 'name="robots"' in txt.lower():
        return False
    new = re.sub(r'</head>', '\n<meta name="robots" content="noindex">\n</head>', txt, flags=re.I)
    if new != txt:
        p.write_text(new, encoding='utf-8')
        return True
    return False

def main():
    changed = 0
    for p in ROOT.glob('home-*.html'):
        if inject_noindex(p):
            changed += 1
    print('Added noindex to', changed, 'variant pages')

if __name__ == '__main__':
    main()

