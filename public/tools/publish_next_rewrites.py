import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'articles'
REW = ART / '_rewrites'

def is_published(md: Path) -> bool:
    m = re.search(r'^publish_status:\s*(\w+)', md.read_text(encoding='utf-8', errors='ignore'), re.M)
    return bool(m and m.group(1).lower() == 'published')

def set_published(text: str) -> str:
    lines = text.splitlines()
    out = []
    in_fm = False
    seen = False
    for line in lines:
        if line.strip() == '---':
            in_fm = not in_fm
        if in_fm and line.lower().startswith('publish_status:'):
            out.append('publish_status: published')
            seen = True
        else:
            out.append(line)
    if not seen:
        try:
            i = out.index('---', 1)
            out.insert(i, 'publish_status: published')
        except ValueError:
            pass
    return '\n'.join(out)

def main(n=10):
    published = 0
    for rw in sorted(REW.glob('*.md')):
        slug = rw.stem
        dst = ART / f'{slug}.md'
        if dst.exists() and is_published(dst):
            continue
        txt = rw.read_text(encoding='utf-8', errors='ignore')
        txt = set_published(txt)
        dst.write_text(txt, encoding='utf-8')
        published += 1
        if published >= n:
            break
    print('Published next rewrites:', published)

if __name__ == '__main__':
    main()

