import os, re
from pathlib import Path

ROOT = Path('/Users/boo2/Desktop/proppy')
ART_DIR = ROOT / 'articles'

CAT_TO_PILLAR = {
  'Market Trends': 'Market Trends & Analysis',
  'Suburb Profiles': 'Suburb & Regional Profiles',
  'Strategy': 'Investment Strategy (Educational)',
  'Cycles': 'Property Cycles & Timing',
  'Case Studies': 'Real Investor Case Studies',
  'Risk': 'Risk, Regulation & Market Reality',
}

PILLAR_ANCHOR = {
  'Market Trends & Analysis': 'pillar-market-trends',
  'Suburb & Regional Profiles': 'pillar-suburb-profiles',
  'Investment Strategy (Educational)': 'pillar-strategy',
  'Property Cycles & Timing': 'pillar-cycles',
  'Real Investor Case Studies': 'pillar-case-studies',
  'Risk, Regulation & Market Reality': 'pillar-risk'
}

def parse_front_matter(text: str):
    if not text.strip().startswith('---'):
        return {}
    parts = text.split('---', 2)
    if len(parts) < 3:
        return {}
    fm_raw = parts[1]
    fm = {}
    for line in fm_raw.splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm

def latest_articles(n=6):
    items = []
    for p in ART_DIR.glob('*.md'):
        fm = parse_front_matter(p.read_text(encoding='utf-8', errors='ignore'))
        title = fm.get('title', p.stem)
        mtime = p.stat().st_mtime
        slug = p.stem
        items.append((mtime, title, slug))
    items.sort(reverse=True)
    return items[:n]

def grouped_articles():
    groups = {pillar: [] for pillar in CAT_TO_PILLAR.values()}
    for p in ART_DIR.glob('*.md'):
        fm = parse_front_matter(p.read_text(encoding='utf-8', errors='ignore'))
        title = fm.get('title', p.stem)
        cat = fm.get('category', '').strip('[]')
        cat = cat.split(',')[0].strip()
        pillar = CAT_TO_PILLAR.get(cat)
        if pillar:
            groups[pillar].append((title, p.stem))
    return groups

def build_latest_block():
    items = latest_articles(6)
    cards = []
    for _, title, slug in items:
        cards.append(f'''<a href="/articles/{slug}.html" class="block rounded-2xl border border-slate-200 dark:border-slate-800 p-4 hover:shadow-md transition-shadow">
  <h4 class="font-bold mb-1">{title}</h4>
  <p class="text-sm text-slate-500">Draft outline</p>
</a>''')
    grid = '<div class="grid grid-cols-1 md:grid-cols-3 gap-4">' + '\n'.join(cards) + '</div>'
    block = '\n'.join([
      '<!-- latest-articles:start -->',
      '<section class="max-w-7xl mx-auto px-6 py-10">',
      '  <div class="rounded-[2rem] border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 md:p-8">',
      '    <h2 class="text-2xl font-extrabold mb-4">Latest Articles</h2>',
      grid,
      '  </div>',
      '</section>',
      '<!-- latest-articles:end -->'
    ])
    return block

def build_index_block():
    groups = grouped_articles()
    sections = []
    for pillar, items in groups.items():
        items.sort()
        lis = '\n'.join([f'<li><a class="text-primary hover:underline" href="/articles/{slug}.html">{title}</a></li>' for title, slug in items])
        pid = PILLAR_ANCHOR.get(pillar, 'pillar')
        sections.append(f'<div><h3 id="{pid}" class="text-lg font-bold mb-2">{pillar}</h3><ul class="list-disc pl-5 space-y-1">{lis}</ul></div>')
    grid = '<div class="grid grid-cols-1 md:grid-cols-2 gap-8">' + '\n'.join(sections) + '</div>'
    block = '\n'.join([
      '<!-- articles-index:start -->',
      '<section class="max-w-7xl mx-auto px-6 py-14">',
      '  <div class="rounded-[2rem] border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-8 md:p-12">',
      '    <div class="text-center mb-6">',
      '      <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-bold uppercase tracking-wider">',
      '        <span class="material-symbols-outlined text-sm">library_books</span>',
      '        Editorial Articles',
      '      </span>',
      '    </div>',
      '    <h2 class="text-2xl md:text-3xl font-extrabold text-center mb-6">Explore our articles</h2>',
      grid,
      '  </div>',
      '</section>',
      '<!-- articles-index:end -->'
    ])
    return block

def update_resources():
    p = ROOT / 'resources.html'
    html = p.read_text(encoding='utf-8')
    latest = build_latest_block()
    index = build_index_block()
    if '<!-- latest-articles:start -->' in html:
        html = re.sub(r'<!-- latest-articles:start -->[\s\S]*?<!-- latest-articles:end -->', latest, html)
    else:
        # Insert latest before the existing articles index or before footer
        if '<!-- articles-index:start -->' in html:
            html = html.replace('<!-- articles-index:start -->', latest + '\n<!-- articles-index:start -->')
        else:
            html = re.sub(r'(</footer>)', latest + '\n\1', html, count=1)

    if '<!-- articles-index:start -->' in html:
        html = re.sub(r'<!-- articles-index:start -->[\s\S]*?<!-- articles-index:end -->', index, html)
    else:
        html = re.sub(r'(</footer>)', index + '\n\1', html, count=1)
    p.write_text(html, encoding='utf-8')
    print('resources.html updated with latest + index')

if __name__ == '__main__':
    update_resources()
