import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def fix_paths(html: str) -> str:
    # Convert root-absolute to parent-relative (../) for property pages
    html = re.sub(r'href="/(?!/)','href="../', html)
    html = re.sub(r'src="/(?!/)','src="../', html)
    # Fix bare links like book.html to go up a level
    html = re.sub(r'href=\"(?!\.{2}/)([a-z0-9\-]+\.html)\"', r'href="../\1"', html)
    return html

def process_dir(d: Path) -> int:
    changed = 0
    for p in d.glob('*.html'):
        txt = p.read_text(encoding='utf-8', errors='ignore')
        new = fix_paths(txt)
        if new != txt:
            p.write_text(new, encoding='utf-8')
            changed += 1
    return changed

def main():
    total = 0
    total += process_dir(ROOT / 'property')
    docs_prop = ROOT / 'docs' / 'property'
    if docs_prop.exists():
        total += process_dir(docs_prop)
    print('Fixed links in', total, 'property HTML files')

if __name__ == '__main__':
    main()

