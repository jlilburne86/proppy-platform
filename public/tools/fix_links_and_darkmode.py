import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GUARD = """<script id=\"color-mode-guard\">(function(){try{document.documentElement.classList.remove('dark');}catch(e){}})();</script>"""

def ensure_guard(html: str) -> str:
    if 'id="color-mode-guard"' in html:
        return html
    # insert just before </head>
    return re.sub(r'</head>', GUARD + '\n</head>', html, flags=re.I)

def fix_root_html(p: Path):
    txt = p.read_text(encoding='utf-8', errors='ignore')
    orig = txt
    # fix absolute root links to relative
    txt = re.sub(r'href="/(?!/)', 'href="', txt)
    txt = re.sub(r'src="/(?!/)', 'src="', txt)
    txt = txt.replace('content="/assets/', 'content="assets/')
    # specific escaped regressions
    txt = txt.replace('src=\\"tools/analytics.js\\"', 'src="tools/analytics.js"')
    txt = txt.replace('proppy\\-logo\\.webp', 'proppy-logo.webp')
    txt = ensure_guard(txt)
    if txt != orig:
        p.write_text(txt, encoding='utf-8')
        return True
    return False

def fix_article_html(p: Path):
    txt = p.read_text(encoding='utf-8', errors='ignore')
    orig = txt
    # make absolute paths relative to articles/ depth
    txt = re.sub(r'href="/(?!/)', 'href="../', txt)
    txt = re.sub(r'src="/(?!/)', 'src="../', txt)
    txt = txt.replace('content="/assets/', 'content="../assets/')
    txt = ensure_guard(txt)
    if txt != orig:
        p.write_text(txt, encoding='utf-8')
        return True
    return False

def main():
    changed = 0
    # root html files
    for p in ROOT.glob('*.html'):
        if fix_root_html(p):
            changed += 1
    # article html files
    art = ROOT / 'articles'
    for p in art.glob('*.html'):
        if fix_article_html(p):
            changed += 1
    print(f'Updated {changed} files')

if __name__ == '__main__':
    main()

