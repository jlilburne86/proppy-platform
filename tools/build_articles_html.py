import os, re, datetime, html
from pathlib import Path
import json

ROOT = Path('/Users/boo2/Desktop/proppy')
ART_MD_DIR = ROOT / 'articles'

def parse_front_matter(text: str):
    if not text.strip().startswith('---'):
        return {}, text
    parts = text.split('---', 2)
    if len(parts) < 3:
        return {}, text
    fm_raw = parts[1]
    body = parts[2]
    fm = {}
    for line in fm_raw.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm, body

def render_inline(text: str) -> str:
    import html as h
    # links [text](url)
    def link_repl(m):
        t = h.escape(m.group(1))
        raw = m.group(2)
        # rewrite absolute article links to sibling files; other absolute links to root become parent-relative
        if raw.startswith('/articles/'):
            u = raw.split('/')[-1]
        elif raw.startswith('/'):
            u = '../' + raw.lstrip('/')
        else:
            u = raw
        u = h.escape(u, quote=True)
        return f'<a href="{u}" class="text-primary hover:underline">{t}</a>'
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link_repl, text)
    # bold **text**
    text = re.sub(r'\*\*([^*]+)\*\*', lambda m: f'<strong>{h.escape(m.group(1))}</strong>', text)
    # italics *text*
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', lambda m: f'<em>{h.escape(m.group(1))}</em>', text)
    # escape remaining special chars (not tags we just added)
    # naive: escape then unescape tags is tricky; assume content safe beyond above formatting
    return text

def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out = []
    in_ul = False
    in_code = False
    # pass-through simple HTML blocks
    def is_html_line(s: str) -> bool:
        s = s.strip()
        return s.startswith('<') and not s.startswith('<!--')
    codebuf = []
    img_count = 0
    def slugify_heading(text: str) -> str:
        t = text.strip().lower()
        t = re.sub(r"[’'“”]", '', t)
        t = re.sub(r"[^a-z0-9]+", '-', t).strip('-')
        return t
    for ln in lines:
        if ln.strip().startswith('```'):
            if in_code:
                out.append('<pre class="rounded-xl bg-slate-50 dark:bg-slate-800 p-4 overflow-x-auto">' + html.escape('\n'.join(codebuf)) + '</pre>')
                codebuf = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            codebuf.append(ln)
            continue
        # image syntax ![alt](src)
        img_m = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', ln)
        if img_m:
            for alt, src in img_m:
                # make article-relative if absolute assets path
                if src.startswith('/assets/'):
                    src_eff = '../' + src.lstrip('/')
                else:
                    src_eff = src
                out.append(f'<figure class="my-4"><img src="{html.escape(src_eff, quote=True)}" alt="{html.escape(alt)}" class="w-full rounded-2xl border border-slate-200 dark:border-slate-800"/>')
                if alt:
                    out.append(f'<figcaption class="text-xs text-slate-500 dark:text-slate-400 mt-2">{html.escape(alt)}</figcaption>')
                out.append('</figure>')
                img_count += 1
            continue
        if is_html_line(ln):
            if in_ul:
                out.append('</ul>'); in_ul = False
            out.append(ln)
            continue
        if ln.startswith('# '):
            if in_ul:
                out.append('</ul>'); in_ul = False
            out.append(f'<h1 class="text-2xl md:text-4xl font-extrabold mb-4">{render_inline(ln[2:].strip())}</h1>')
            continue
        if ln.startswith('## '):
            if in_ul:
                out.append('</ul>'); in_ul = False
            htxt = ln[3:].strip()
            hid = slugify_heading(htxt)
            out.append(f'<h2 id="{hid}" class="text-xl md:text-2xl font-bold mt-8 mb-3">{render_inline(htxt)}</h2>')
            continue
        if ln.startswith('### '):
            if in_ul:
                out.append('</ul>'); in_ul = False
            htxt = ln[4:].strip()
            hid = slugify_heading(htxt)
            out.append(f'<h3 id="{hid}" class="text-lg md:text-xl font-bold mt-6 mb-2">{render_inline(htxt)}</h3>')
            continue
        if ln.startswith('- '):
            if not in_ul:
                out.append('<ul class="list-disc pl-6 space-y-1">'); in_ul = True
            out.append('<li>' + render_inline(ln[2:].strip()) + '</li>')
            continue
        if ln.startswith('> '):
            if in_ul:
                out.append('</ul>'); in_ul = False
            out.append('<blockquote class="border-l-4 border-slate-300 dark:border-slate-700 pl-4 italic text-slate-600 dark:text-slate-300">' + render_inline(ln[2:].strip()) + '</blockquote>')
            continue
        if ln.strip() == '---':
            if in_ul: out.append('</ul>'); in_ul = False
            out.append('<hr class="my-6 border-slate-200 dark:border-slate-700"/>')
            continue
        if not ln.strip():
            if in_ul:
                out.append('</ul>'); in_ul = False
            out.append('')
            continue
        # paragraph
        out.append('<p class="mb-4 text-slate-700 dark:text-slate-300">' + render_inline(ln) + '</p>')
    if in_ul:
        out.append('</ul>')
    body = '\n'.join(out)
    # Ensure at least 4 images by appending a small gallery if needed
    if img_count < 4:
        remaining = 4 - img_count
        gallery_imgs = [
            '../assets/screenshots/platform-screenshot.png',
            '../assets/screenshots/technology.png',
            '../assets/screenshots/how-it-works.png',
            '../assets/screenshots/homepage-9.png',
        ]
        fig = ['<section class="my-8 grid grid-cols-1 sm:grid-cols-2 gap-4">']
        for i in range(remaining):
            src = gallery_imgs[i % len(gallery_imgs)]
            fig.append(f'<figure><img src="{html.escape(src)}" alt="Article illustration" class="w-full rounded-2xl border border-slate-200 dark:border-slate-800"/><figcaption class="text-xs text-slate-500 dark:text-slate-400 mt-1">Illustrative screenshot</figcaption></figure>')
        fig.append('</section>')
        body += '\n' + '\n'.join(fig)
    return body

def read_nav():
    idx = (ROOT / 'index.html').read_text(encoding='utf-8', errors='ignore')
    m = re.search(r'<nav[\s\S]*?</nav>', idx, flags=re.I)
    return m.group(0) if m else ''

def make_nav_article_relative(nav_html: str) -> str:
    def href_repl(m):
        v = m.group(1)
        if v.startswith(('http://','https://','//','#','mailto:','tel:','javascript:','data:','../')):
            return m.group(0)
        return f'href="../{v}"'
    def src_repl(m):
        v = m.group(1)
        if v.startswith(('http://','https://','//','#','data:','../')):
            return m.group(0)
        return f'src="../{v}"'
    nav_html = re.sub(r'href="([^"]+)"', href_repl, nav_html)
    nav_html = re.sub(r'src="([^"]+)"', src_repl, nav_html)
    return nav_html

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

def compute_read_time(md_body: str, wpm: int = 220) -> str:
    # strip code fences and markdown symbols for a rough count
    text = re.sub(r'```[\s\S]*?```', '', md_body)
    text = re.sub(r'[>#*_`\-]', ' ', text)
    words = len([w for w in re.split(r'\s+', text) if w])
    mins = max(1, round(words / wpm))
    return f"{mins} min"

def load_authors() -> dict:
    p = Path('/Users/boo2/Desktop/proppy/data/authors.json')
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except Exception:
        return {}

AUTHORS = load_authors()

def load_scorecards():
    p = Path('/Users/boo2/Desktop/proppy/data/article_scorecards.json')
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except Exception:
        return {}

SCORECARDS = load_scorecards()

def author_block(name: str) -> str:
    a = AUTHORS.get(name) or AUTHORS.get('Proppy Editorial') or {
        'name': name,
        'title': 'Editorial',
        'avatar': '../proppy-mobile-icon.png',
        'bio': ''
    }
    av = a.get('avatar','')
    if av.startswith('/'):
        av = '../' + av.lstrip('/')
    return f'''<section class="max-w-3xl mx-auto px-6 py-8">
  <div class="flex items-start gap-4 border border-slate-200 dark:border-slate-800 rounded-2xl p-4 bg-white dark:bg-slate-900">
    <img src="{av}" alt="{a.get('name','Author')}" class="w-12 h-12 rounded-full object-cover"/>
    <div>
      <p class="font-bold">{a.get('name','Author')}</p>
      <p class="text-xs text-slate-500">{a.get('title','')}</p>
      <p class="text-sm text-slate-600 dark:text-slate-400 mt-1">{a.get('bio','')}</p>
    </div>
  </div>
</section>'''

def scorecard_block(slug: str) -> str:
    m = SCORECARDS.get(slug, {}).get('metrics', {})
    tiles = []
    defaults = [
        ('Vacancy','Tight','Signal: improving tenant demand'),
        ('Rent Pressure','Rising','Signal: yields stabilising/upgrading'),
        ('Listings','Flat','Signal: absorption steady'),
        ('Pipeline','Constrained','Signal: limited new supply')
    ]
    items = []
    if m:
        for key in ['vacancy','rent','listings','pipeline']:
            mv = m.get(key)
            if mv:
                items.append((mv.get('label',''), mv.get('value',''), mv.get('note','')))
    if not items:
        items = defaults
    for label, val, note in items:
        tiles.append(f'''<div class="score-tile">
  <div class="score-label">{html.escape(label)}</div>
  <div class="score-value">{html.escape(val)}</div>
  <div class="score-note">{html.escape(note)}</div>
</div>''')
    return '<section class="max-w-3xl mx-auto px-6 py-4"><div class="score-grid">' + '\n'.join(tiles) + '</div></section>'

def images_block(slug: str) -> str:
    imgs = SCORECARDS.get(slug, {}).get('images', [])
    if not imgs:
        return ''
    figures=[]
    for img in imgs[:4]:
        raw = img.get('src','')
        if raw.startswith('/'):
            raw = '../' + raw.lstrip('/')
        src = html.escape(raw)
        alt = html.escape(img.get('alt',''))
        figures.append(f'''<figure class="my-4">
  <picture>
    <source srcset="{src.replace('.png','.webp').replace('.jpg','.webp')}" type="image/webp"/>
    <img src="{src}" alt="{alt}" class="w-full rounded-2xl border border-slate-200 dark:border-slate-800" loading="lazy" decoding="async"/>
  </picture>
  <figcaption class="text-xs text-slate-500 dark:text-slate-400 mt-2">{alt}</figcaption>
</figure>''')
    return '<section class="max-w-3xl mx-auto px-6">' + '\n'.join(figures) + '</section>'

def hero_image(slug: str, title: str) -> str:
    imgs = SCORECARDS.get(slug, {}).get('images', [])
    if not imgs:
        return ''
    hero = imgs[0]['src']
    if hero.startswith('/'):
        hero = '../' + hero.lstrip('/')
    alt = imgs[0].get('alt', title)
    return f'''<section class="max-w-3xl mx-auto px-6">
  <div class="hero-img"><img src="{html.escape(hero)}" alt="{html.escape(alt)}" loading="eager" decoding="async"/></div>
</section>'''

def scorecard_legend() -> str:
    return '''<section class="max-w-3xl mx-auto px-6 py-2">
  <details class="border border-slate-200 dark:border-slate-800 rounded-xl p-3">
    <summary class="text-sm font-semibold cursor-pointer">How to read these tiles</summary>
    <div class="text-sm text-slate-600 dark:text-slate-400 mt-2">
      <p>Vacancy and rent pressure are leading indicators of tenant demand; listings and pipeline indicate supply. We prefer <em>tight</em> vacancy (&lt;~1.5%), <em>rising</em> rents, <em>flat</em> listings and a <em>constrained</em> pipeline. Always validate at suburb and stock level.</p>
    </div>
  </details>
</section>'''

def toc_block(body_html: str) -> str:
    # Extract H2s and build a simple TOC
    items = re.findall(r'<h2 id=\"([^\"]+)\"[^>]*>(.*?)</h2>', body_html, flags=re.I)
    if len(items) < 2:
        return ''
    links = []
    for hid, title in items:
        links.append(f'<li><a class="text-primary hover:underline" href="#${hid}">{html.escape(re.sub(r"<[^>]+>", "", title))}</a></li>'.replace('#$', '#'))
    ul = '<ul class="list-disc pl-6 space-y-1">' + '\n'.join(links) + '</ul>'
    return '<section class="max-w-3xl mx-auto px-6 py-2"><details class="border border-slate-200 dark:border-slate-800 rounded-xl p-3"><summary class="text-sm font-semibold cursor-pointer">In this article</summary>' + ul + '</details></section>'

def pick_related(this_slug: str, category: str) -> str:
    items = []
    for p in ART_MD_DIR.glob('*.md'):
        if p.stem == this_slug: continue
        try:
            fm_txt = p.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        if not fm_txt.startswith('---'):
            continue
        fm = fm_txt.split('---',2)[1]
        cat_m = re.search(r'\ncategory:\s*\[([^\]]+)\]', fm)
        cat = cat_m.group(1).strip() if cat_m else ''
        if category and category not in cat:
            continue
        title_m = re.search(r'\ntitle:\s*"([^"]+)"', fm)
        title = title_m.group(1) if title_m else p.stem
        items.append((p.stat().st_mtime, title, p.stem))
    items.sort(reverse=True)
    items = items[:3]
    if not items:
        return ''
    cards = []
    for _, title, slug in items:
        cards.append(f'<a href="{slug}.html" class="related-card"><h4 class="font-bold mb-1">{title}</h4><p class="text-sm text-slate-500">Related read</p></a>')
    grid = '<div class="related-grid">' + '\n'.join(cards) + '</div>'
    return '<section class="max-w-3xl mx-auto px-6 py-8"><h3 class="text-lg font-extrabold mb-2">Related Articles</h3>' + grid + '</section>'

def compute_outlook(slug: str) -> tuple[str,str]:
    m = SCORECARDS.get(slug, {}).get('metrics', {})
    txt = 'Neutral'
    cls = 'outlook-neutral'
    vac = (m.get('vacancy') or {}).get('value','').lower()
    rent = (m.get('rent') or {}).get('value','').lower()
    listg = (m.get('listings') or {}).get('value','').lower()
    pipe = (m.get('pipeline') or {}).get('value','').lower()
    if ('tight' in vac or 'target' in vac) and 'rising' in rent and ('flat' in listg or 'stable' in listg) and ('constrained' in pipe or 'limited' in pipe):
        txt = 'Constructive'
        cls = 'outlook-constructive'
    elif ('rising' in vac and 'up' in listg) or ('oversupply' in pipe):
        txt = 'Cautious'
        cls = 'outlook-cautious'
    return txt, cls

def build_page_html(fm: dict, body_html: str, nav_html: str, slug: str, raw_md: str) -> str:
    title = fm.get('title', 'Article')
    desc = fm.get('description', 'Article on Proppy')
    category = fm.get('category', '').strip('[]') or 'Resources'
    audience = fm.get('audience', '').strip('[]') or 'Both'
    reading_time = compute_read_time(raw_md)
    author = fm.get('author', 'Proppy Editorial')
    today = datetime.date.today().strftime('%d %b %Y')
    canonical = f'{slug}.html'
    pillar = CAT_TO_PILLAR.get(category, category)
    anchor = PILLAR_ANCHOR.get(pillar, '')
    breadcrumbs = f'''<nav aria-label="Breadcrumb" class="text-sm text-slate-500 dark:text-slate-400 mb-4">
  <ol class="flex items-center gap-2">
    <li><a class="hover:underline" href="../index.html">Home</a></li>
    <li>›</li>
    <li><a class="hover:underline" href="../resources.html">Resources</a></li>
    <li>›</li>
    <li><a class="hover:underline" href="../resources.html#{anchor}">{html.escape(pillar)}</a></li>
  </ol>
</nav>'''
    meta_row = f'''<div class="flex flex-wrap items-center gap-2 text-xs text-slate-500 dark:text-slate-400 mb-6">
  <span class="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-slate-100 dark:bg-slate-800">{html.escape(category)}</span>
  <span>•</span>
  <span>{html.escape(reading_time)}</span>
  <span>•</span>
  <span>{html.escape(audience)}</span>
  <span>•</span>
  <span>By {author}</span>
  <span>•</span>
  <span>{today}</span>
</div>'''
    back_cta = f'''<section class="max-w-3xl mx-auto px-6 py-8 flex items-center gap-3">
  <a href="../resources.html" class="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-sm font-semibold">
    <span class="material-symbols-outlined text-sm">arrow_back</span>
    Back to Resources
  </a>
  <a href="../resources.html#{anchor}" class="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-sm font-semibold">
    <span class="material-symbols-outlined text-sm">category</span>
    Back to {html.escape(pillar)}
  </a>
</section>'''
    author_html = author_block(author)
    # OG image override from scorecards
    og_image = '../assets/screenshots/platform-screenshot.png'
    for img in SCORECARDS.get(slug, {}).get('images', []):
        if img.get('og'):
            og_image = img.get('src', og_image)
    if og_image.startswith('/'):
        og_image = '../' + og_image.lstrip('/')

    outlook_txt, outlook_cls = compute_outlook(slug)
    page = f'''<!DOCTYPE html>
<html class="scroll-smooth" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{html.escape(title)} - Proppy</title>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,typography"></script>
<link rel="stylesheet" href="../assets/site.css"/>
<link rel="canonical" href="{canonical}">
<meta name="description" content="{html.escape(desc)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Proppy">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{html.escape(og_image)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{html.escape(og_image)}">
<script id="color-mode-guard">(function(){{try{{document.documentElement.classList.remove('dark');}}catch(e){{}}}})();</script>
<script id="navx-script" src="../tools/navx-accessible.js"></script>
<link rel="stylesheet" href="../tools/ux.css"/>
<script src="../tools/analytics.js"></script>
</head>
<body class="bg-background-light dark:bg-background-dark text-slate-900 dark:text-slate-100 font-sans">
<a href="#content" class="skip-link">Skip to content</a>
{nav_html}
<main id="content" class="max-w-3xl mx-auto px-6 pt-28 pb-16 prose prose-slate dark:prose-invert">
{breadcrumbs}
{hero_image(slug, title)}
<div class="flex items-center justify-between gap-3 flex-wrap">
  <h1 class="!mb-2">{html.escape(title)}</h1>
  <span class="outlook-badge {outlook_cls}">Outlook: {outlook_txt}</span>
</div>
{meta_row}
{scorecard_block(slug)}
{scorecard_legend()}
{toc_block(body_html)}
{images_block(slug)}
{body_html}
</main>
{author_html}
{pick_related(slug, category)}
{back_cta}
<footer class="py-12 border-t border-slate-200 dark:border-slate-800 mt-12">
  <div class="max-w-7xl mx-auto px-6">
    <div class="flex flex-col md:flex-row justify-between items-center gap-8">
      <div class="flex items-center gap-3">
        <span class="text-xl font-extrabold uppercase tracking-tight">Proppy</span>
        <span class="text-slate-400 text-sm">© {datetime.date.today().year} Proppy Inc. All rights reserved.</span>
      </div>
      <div class="flex gap-8 text-sm font-semibold text-slate-500 dark:text-slate-400">
        <a class="hover:text-primary transition-colors" href="../privacy.html">Privacy Policy</a>
        <a class="hover:text-primary transition-colors" href="../terms.html">Terms of Service</a>
        <a class="hover:text-primary transition-colors" href="../site-map.html">Site Map</a>
      </div>
    </div>
  </div>
</footer>
</body></html>'''
    return page

def main():
    nav_html = make_nav_article_relative(read_nav())
    out_files = []
    for md_path in ART_MD_DIR.glob('*.md'):
        slug = md_path.stem
        txt = md_path.read_text(encoding='utf-8', errors='ignore')
        fm, body = parse_front_matter(txt)
        body_html = md_to_html(body)
        html_page = build_page_html(fm, body_html, nav_html, slug, body)
        out_path = ART_MD_DIR / f'{slug}.html'
        out_path.write_text(html_page, encoding='utf-8')
        out_files.append(out_path)
    print('Built', len(out_files), 'HTML articles')

if __name__ == '__main__':
    main()
