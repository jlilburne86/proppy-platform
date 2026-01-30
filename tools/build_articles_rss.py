import datetime, re, html
from pathlib import Path

ROOT = Path('/Users/boo2/Desktop/proppy')
ART = ROOT / 'articles'
OUT = ROOT / 'articles.xml'
try:
    from tools.seo_config import site_url
    SITE = site_url()
except Exception:
    SITE = 'https://jlilburne86.github.io/proppy-platform'

def parse_front(text: str) -> dict:
    fm = {}
    if not text.strip().startswith('---'):
        return fm
    raw = text.split('---',2)[1]
    for line in raw.splitlines():
        if ':' in line:
            k,v = line.split(':',1)
            fm[k.strip()] = v.strip().strip('"')
    return fm

def pub_date(iso: str) -> str:
    try:
        d = datetime.datetime.fromisoformat(iso)
    except Exception:
        d = datetime.datetime.utcnow()
    # RFC 2822
    return d.strftime('%a, %d %b %Y %H:%M:%S +0000')

def main():
    items=[]
    for p in ART.glob('*.md'):
        fm = parse_front(p.read_text(encoding='utf-8', errors='ignore'))
        title = fm.get('title', p.stem)
        desc = fm.get('description', '')
        date = fm.get('date') or datetime.datetime.utcnow().date().isoformat()
        link = f"{SITE}/articles/{p.stem}.html"
        items.append((date, title, desc, link))
    items.sort(reverse=True)
    parts=[
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0">',
        '  <channel>',
        '    <title>Proppy Articles</title>',
        f'    <link>{SITE}/resources.html</link>',
        '    <description>Latest articles from Proppy</description>'
    ]
    for d,t,desc,link in items:
        parts += [
            '    <item>',
            f'      <title>{html.escape(t)}</title>',
            f'      <link>{html.escape(link)}</link>',
            f'      <pubDate>{pub_date(d)}</pubDate>',
            f'      <description>{html.escape(desc)}</description>',
            '    </item>'
        ]
    parts += ['  </channel>', '</rss>']
    OUT.write_text('\n'.join(parts), encoding='utf-8')
    print('Wrote', OUT)

if __name__=='__main__':
    main()
