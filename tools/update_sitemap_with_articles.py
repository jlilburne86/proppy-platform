import re
from pathlib import Path

ROOT = Path('/Users/boo2/Desktop/proppy')
ART = ROOT / 'articles'
MAP = ROOT / 'site-map.html'

def parse_front(text: str) -> dict:
    fm={}
    if not text.strip().startswith('---'):
        return fm
    raw=text.split('---',2)[1]
    for line in raw.splitlines():
        if ':' in line:
            k,v=line.split(':',1)
            fm[k.strip()]=v.strip().strip('"')
    return fm

def build_block():
    lis=[]
    for p in sorted(ART.glob('*.md')):
        fm=parse_front(p.read_text(encoding='utf-8',errors='ignore'))
        title=fm.get('title', p.stem)
        lis.append(f'<li><a class="text-primary hover:underline" href="/articles/{p.stem}.html">{title}</a></li>')
    ul='<ul class="list-disc pl-6 space-y-1">'+'\n'.join(lis)+'</ul>'
    return '\n'.join([
      '<!-- sitemap-articles:start -->',
      '<section class="max-w-7xl mx-auto px-6 py-10">',
      '  <h2 class="text-xl font-extrabold mb-3">Articles</h2>',
      ul,
      '</section>',
      '<!-- sitemap-articles:end -->'
    ])

def run():
    html=MAP.read_text(encoding='utf-8')
    block=build_block()
    if '<!-- sitemap-articles:start -->' in html:
        html=re.sub(r'<!-- sitemap-articles:start -->[\s\S]*?<!-- sitemap-articles:end -->', block, html)
    else:
        html=re.sub(r'(</footer>)', block+'\n\1', html, count=1)
    MAP.write_text(html, encoding='utf-8')
    print('Updated site-map with articles list')

if __name__=='__main__':
    run()

