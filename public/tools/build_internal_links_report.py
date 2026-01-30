import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'articles'
OUT = ROOT / 'site-audit' / 'internal_links.md'

def parse_front(text: str):
    fm = {}
    body = text
    if text.strip().startswith('---'):
        parts = text.split('---',2)
        if len(parts) >= 3:
            for line in parts[1].splitlines():
                if ':' in line:
                    k,v = line.split(':',1)
                    fm[k.strip()] = v.strip().strip('"')
            body = parts[2]
    return fm, body

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    items = []
    for p in ART.glob('*.md'):
        fm,_ = parse_front(p.read_text(encoding='utf-8', errors='ignore'))
        status = (fm.get('publish_status','') or '').lower()
        if status != 'published':
            continue
        title = fm.get('title', p.stem)
        cat = (fm.get('category','') or '').strip('[]').split(',')[0].strip()
        items.append((p, p.stat().st_mtime, title, cat))
    # Build related by category
    lines = ["# Internal Linking Suggestions", ""]
    for p,_,title,cat in sorted(items, key=lambda x: x[2].lower()):
        related = []
        for q,mt,title2,cat2 in items:
            if q == p:
                continue
            if cat2 == cat:
                related.append((mt, title2, q.stem))
        related.sort(reverse=True)
        take = related[:3]
        link_str = ', '.join([f'[{t}](articles/{s}.html)' for _,t,s in take]) if take else '—'
        lines.append(f'- {title} ({cat}) → {link_str}')
    OUT.write_text('\n'.join(lines), encoding='utf-8')
    print('Wrote', OUT)

if __name__ == '__main__':
    main()

