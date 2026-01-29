import re
from pathlib import Path

ROOT = Path('/Users/boo2/Desktop/proppy')
ART = ROOT / 'articles'
HOME = ROOT / 'index.html'

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

def latest(n=3):
    items=[]
    for p in ART.glob('*.md'):
        fm=parse_front(p.read_text(encoding='utf-8', errors='ignore'))
        title=fm.get('title', p.stem)
        desc=fm.get('description','')
        items.append((p.stat().st_mtime, title, desc, p.stem))
    items.sort(reverse=True)
    return items[:n]

def build_block():
    cards=[]
    for _,title,desc,slug in latest():
        cards.append(f'''<a href="articles/{slug}.html" class="block rounded-2xl border border-slate-200 dark:border-slate-800 p-4 hover:shadow-md transition-shadow bg-white dark:bg-slate-900">
  <h4 class="font-bold mb-1">{title}</h4>
  <p class="text-sm text-slate-500 line-clamp-2">{desc}</p>
</a>''')
    grid='<div class="grid grid-cols-1 md:grid-cols-3 gap-4">'+'\n'.join(cards)+'</div>'
    return '\n'.join([
      '<!-- latest-articles-home:start -->',
      '<section class="max-w-7xl mx-auto px-6 py-10">',
      '  <div class="rounded-[2rem] border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 md:p-8">',
      '    <div class="flex items-center justify-between mb-3">',
      '      <h2 class="text-2xl font-extrabold">Latest Articles</h2>',
      '      <a class="text-sm font-semibold text-primary" href="resources.html">View all</a>',
      '    </div>',
      grid,
      '  </div>',
      '</section>',
      '<!-- latest-articles-home:end -->'
    ])

def run():
    html=HOME.read_text(encoding='utf-8')
    block=build_block()
    if '<!-- latest-articles-home:start -->' in html:
        html=re.sub(r'<!-- latest-articles-home:start -->[\s\S]*?<!-- latest-articles-home:end -->', block, html)
    else:
        # Insert before the final big CTA section or before footer
        html=re.sub(r'(</section>\s*\n\s*<section[^>]*>\s*<div[^>]*>\s*<div class=\"inline-flex[\s\S]*?Ready\?[\s\S]*?</section>)', block+'\n\1', html, count=1)
        if html==HOME.read_text(encoding='utf-8'):
            html=re.sub(r'(</footer>)', block+'\n\1', html, count=1)
    HOME.write_text(html, encoding='utf-8')
    print('Updated home with Latest Articles')

if __name__=='__main__':
    run()
