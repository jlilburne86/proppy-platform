import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def process(p: Path) -> bool:
    txt = p.read_text(encoding='utf-8', errors='ignore')
    new = re.sub(r'<script[^>]+src=\"https://cdn\.tailwindcss\.com[^\"]*\"[^>]*></script>\n?', '', txt, flags=re.I)
    if 'assets/site.css' not in new:
        # inject stylesheet before </head>
        new = re.sub(r'</head>', '\n<link rel="stylesheet" href="assets/site.css"/>\n</head>', new, flags=re.I)
    if new != txt:
        p.write_text(new, encoding='utf-8')
        return True
    return False

def main():
    changed = 0
    for p in ROOT.glob('*.html'):
        if process(p):
            changed += 1
    print('Updated', changed, 'root pages (removed Tailwind CDN; ensured site.css)')

if __name__ == '__main__':
    main()

