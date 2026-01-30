#!/usr/bin/env python3
import json, os, html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'properties.json'
TPL = ROOT / 'tools' / 'generate-property-page-template.html'
RESULTS = ROOT / 'results.html'

def load_data():
    with open(DATA, 'r') as f:
        return json.load(f)

def load_template():
    return TPL.read_text()

def _detail_item(label, value):
    return f'''<div class="p-4 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
  <p class="text-xs font-bold text-slate-400 uppercase mb-1">{html.escape(label)}</p>
  <p class="text-sm font-semibold text-slate-800 dark:text-slate-200">{html.escape(value)}</p>
</div>'''

def _build_details_grid(p):
    fields = [
        ('Location', p.get('location','')),
        ('Profile', p.get('profile','')),
        ('Bedrooms', p.get('bedrooms','')),
        ('Bathrooms', p.get('bathrooms','')),
        ('Car Spaces', p.get('car_spaces','')),
        ('Land Size', p.get('land_size','')),
        ('Property Type', p.get('property_type','')),
        ('Purchase Date', p.get('purchase_date','')),
        ('Rent', p.get('rent','')),
        ('Rent Yield', p.get('rent_yield','')),
        ('Valuation (Post-Purchase)', p.get('valuation_post_purchase','')),
    ]
    items = [ _detail_item(lbl, val) for lbl, val in fields if val ]
    return '\n'.join(items) if items else ''

def _build_highlights_block(p):
    highlights = p.get('highlights') or []
    if not highlights:
        return ''
    lis = '\n'.join(f'<li class="flex gap-2"><span class="material-symbols-outlined text-emerald-500">check_circle</span><span>{html.escape(h)}</span></li>' for h in highlights)
    return f'''
<section class="mt-8">
  <h2 class="text-xl font-bold mb-3">Highlights</h2>
  <ul class="space-y-2 text-slate-600 dark:text-slate-300">{lis}</ul>
</section>'''

def _badge(text, color='indigo'):
    return f'<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold border border-{color}-200 dark:border-{color}-900 text-{color}-700 dark:text-{color}-300 bg-{color}-50 dark:bg-{color}-900/30 mr-2 mb-2">{html.escape(text)}</span>'

def _build_tags_block(p):
    tags = p.get('tags') or []
    if not tags:
        return ''
    chips = ''.join(_badge(t, 'indigo') for t in tags)
    return f'<div class="flex flex-wrap">{chips}</div>'

def _build_overview_block(p):
    overview = p.get('overview') or ''
    if not overview:
        return ''
    return f'''
<section class="mt-10 prose prose-slate max-w-none dark:prose-invert">
  <h2>Overview</h2>
  <p>{overview}</p>
</section>'''

def _build_list_block(title, items):
    if not items:
        return ''
    lis = ''.join(f'<li>{html.escape(i)}</li>' for i in items)
    return f'''
<section class="mt-10 prose prose-slate max-w-none dark:prose-invert">
  <h2>{html.escape(title)}</h2>
  <ul>{lis}</ul>
</section>'''

def _build_strategy_block(p):
    return _build_list_block('Why We Chose This Asset', p.get('strategy_points'))

def _build_execution_block(p):
    return _build_list_block('Execution & Outcome Notes', p.get('execution_points'))

def _build_outcome_block(p):
    outcome = []
    if p.get('instant_equity'): outcome.append(('Instant Equity', p['instant_equity']))
    if p.get('growth_12m'): outcome.append(('12-Mo Growth', p['growth_12m']))
    if p.get('growth_3y'): outcome.append(('Capital Growth (3y)', p['growth_3y']))
    if p.get('rental_growth_3y'): outcome.append(('Rental Growth (3y)', p['rental_growth_3y']))
    if p.get('rent_yield'): outcome.append(('Rent Yield', p['rent_yield']))
    if p.get('rent'): outcome.append(('Rent p/w', p['rent']))
    if not outcome:
        return ''
    cards = []
    for label, val in outcome:
        cards.append(f'''<div class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-700">
  <p class="text-xs font-bold text-indigo-500 uppercase mb-1">{html.escape(label)}</p>
  <p class="text-2xl font-extrabold">{html.escape(val)}</p>
</div>''')
    return f'''
<section class="mt-8">
  <h2 class="text-xl font-bold mb-3">Outcome</h2>
  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">{''.join(cards)}</div>
</section>'''

def write_detail_pages(props, tpl):
    for p in props:
        html_out = tpl
        html_out = html_out.replace('{{TITLE}}', p['title'])
        html_out = html_out.replace('{{STRATEGY}}', p.get('strategy',''))
        img = p['image']
        if isinstance(img, str) and not (img.startswith('http') or img.startswith('/')):
            img = '/' + img
        html_out = html_out.replace('{{IMAGE}}', img)
        html_out = html_out.replace('{{PURCHASE_PRICE}}', p.get('purchase_price','') or '—')
        html_out = html_out.replace('{{INSTANT_EQUITY}}', p.get('instant_equity','') or '—')
        html_out = html_out.replace('{{GROWTH_12M}}', p.get('growth_12m','') or '—')
        html_out = html_out.replace('{{TAGS_BLOCK}}', _build_tags_block(p))
        html_out = html_out.replace('{{DETAILS_GRID}}', _build_details_grid(p))
        html_out = html_out.replace('{{HIGHLIGHTS_BLOCK}}', _build_highlights_block(p))
        html_out = html_out.replace('{{OUTCOME_BLOCK}}', _build_outcome_block(p))
        html_out = html_out.replace('{{OVERVIEW_BLOCK}}', _build_overview_block(p))
        html_out = html_out.replace('{{STRATEGY_BLOCK}}', _build_strategy_block(p))
        html_out = html_out.replace('{{EXECUTION_BLOCK}}', _build_execution_block(p))
        out_path = ROOT / 'property' / f"{p['slug']}.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html_out)

def build_cards(props):
    cards = []
    for p in props:
        badge = p.get('strategy','')
        color = 'indigo' if ('Growth' in badge and 'Yield' not in badge) else ('emerald' if 'Yield' in badge else 'blue')
        pp = p.get('purchase_price') or '—'
        g3 = p.get('growth_3y') or '—'
        rpw = p.get('rent') or '—'
        rg3 = p.get('rental_growth_3y') or '—'
        card = f'''
<article class="group bg-white dark:bg-slate-900 rounded-[2rem] border border-slate-200 dark:border-slate-800 overflow-hidden hover:shadow-2xl hover:shadow-indigo-500/10 transition-all duration-300 hover:-translate-y-1">
  <a href="property/{p['slug']}.html" class="block focus:outline-none focus:ring-2 focus:ring-indigo-500">
    <div class="h-64 overflow-hidden relative">
      <div class="absolute inset-0 bg-slate-200 dark:bg-slate-800 animate-pulse"></div>
      <img src="{p['image']}" alt="{html.escape(p['title'])}" class="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-700 img-rounded img-shadow" />
      <div class="absolute top-4 left-4">
        <span class="bg-white/90 dark:bg-slate-900/90 backdrop-blur text-{color}-600 dark:text-{color}-400 text-xs font-bold px-3 py-1.5 rounded-full uppercase tracking-wide border border-{color}-100 dark:border-{color}-900">{html.escape(badge)}</span>
      </div>
    </div>
    <div class="p-8">
      <h3 class="text-lg font-bold text-slate-900 dark:text-white">{html.escape(p['title'])}</h3>
      <p class="text-xs text-slate-400 mt-1">{html.escape(p.get('location',''))}</p>
      <div class="mt-5 grid grid-cols-2 gap-3">
        <div class="rounded-xl border border-slate-100 dark:border-slate-800 p-3 bg-slate-50 dark:bg-slate-800/40">
          <p class="text-[10px] font-bold uppercase text-slate-400">Purchase Price</p>
          <p class="text-sm font-extrabold text-slate-900 dark:text-white">{html.escape(pp)}</p>
        </div>
        <div class="rounded-xl border border-slate-100 dark:border-slate-800 p-3 bg-slate-50 dark:bg-slate-800/40">
          <p class="text-[10px] font-bold uppercase text-slate-400">Capital Growth (3y)</p>
          <p class="text-sm font-extrabold text-indigo-600 dark:text-indigo-400">{html.escape(g3)}</p>
        </div>
        <div class="rounded-xl border border-slate-100 dark:border-slate-800 p-3 bg-slate-50 dark:bg-slate-800/40">
          <p class="text-[10px] font-bold uppercase text-slate-400">Rent p/w</p>
          <p class="text-sm font-extrabold text-emerald-600 dark:text-emerald-400">{html.escape(rpw)}</p>
        </div>
        <div class="rounded-xl border border-slate-100 dark:border-slate-800 p-3 bg-slate-50 dark:bg-slate-800/40">
          <p class="text-[10px] font-bold uppercase text-slate-400">Rental Growth (3y)</p>
          <p class="text-sm font-extrabold text-amber-600 dark:text-amber-400">{html.escape(rg3)}</p>
        </div>
      </div>
    </div>
  </a>
</article>'''
        cards.append(card)
    return cards

def update_results(cards):
    content = RESULTS.read_text()
    # remove any stale markers first
    content = re.sub(r'<!-- CASE_STUDIES_(START|END) -->\n?', '', content)
    # replace the first grid wrapper with our generated cards and reinsert markers
    grid_pat = re.compile(r'(\<div class=\"grid grid-cols-1[^\"]*gap-8\"\>)(.*?)(\</div\>)', re.S)
    def repl(m):
        open_tag, _, close_tag = m.group(1), m.group(2), m.group(3)
        inner = '\n'.join(cards)
        return '<!-- CASE_STUDIES_START -->\n' + open_tag + '\n' + inner + '\n' + close_tag + '\n<!-- CASE_STUDIES_END -->'
    content, n = grid_pat.subn(repl, content, count=1)
    # Prune any leftover content within the same section after the grid
    end_marker = '<!-- CASE_STUDIES_END -->'
    end_idx = content.find(end_marker)
    if end_idx != -1:
        sec_close = content.find('</section>', end_idx)
        if sec_close != -1:
            content = content[:end_idx+len(end_marker)] + content[sec_close:]
    RESULTS.write_text(content)

def cleanup_placeholder_articles():
    html = RESULTS.read_text()
    start_marker = '<!-- CASE_STUDIES_START -->'
    end_marker = '<!-- CASE_STUDIES_END -->'
    if start_marker in html and end_marker in html:
        pre, rest = html.split(start_marker, 1)
        inside, post = rest.split(end_marker, 1)
        # strip any article blocks outside the marker-protected grid
        article_pat = re.compile(r'<article\b[\s\S]*?</article>', re.I)
        pre = article_pat.sub('', pre)
        post = article_pat.sub('', post)
        RESULTS.write_text(pre + start_marker + inside + end_marker + post)

def _fmt_currency(avg):
    # round to nearest $5 for nicer display
    import math
    val = int(round(avg / 5.0) * 5)
    s = f"${val:,}"
    return s

def _fmt_percent(avg):
    return f"{avg:.1f}%"

def _parse_money(s):
    import re
    if not s:
        return None
    m = re.sub(r'[^0-9.]', '', s)
    try:
        return float(m) if m else None
    except Exception:
        return None

def _parse_percent(s):
    import re
    if not s:
        return None
    m = re.sub(r'[^0-9.+-]', '', s)
    try:
        return float(m) if m else None
    except Exception:
        return None

def update_top_stats(props):
    # compute averages from available data
    rents = [ _parse_money(p.get('rent')) for p in props ]
    rents = [r for r in rents if r ]
    growth3y = [ _parse_percent(p.get('growth_3y')) for p in props ]
    growth3y = [g for g in growth3y if g is not None ]
    avg_rent = sum(rents)/len(rents) if rents else None
    avg_growth3y = sum(growth3y)/len(growth3y) if growth3y else None

    if avg_rent is None and avg_growth3y is None:
        return

    html = RESULTS.read_text()
    import re
    # Replace the first stat card labeled "Avg. Instant Equity" -> Avg. Rent p/w
    if avg_rent is not None:
        html = re.sub(
            r'(>)[^<]*(</span>\s*\n\s*<span[^>]*>\s*Avg\. Instant Equity\s*</span>)',
            rf'>{_fmt_currency(avg_rent)}\2',
            html,
            count=1
        )
        html = html.replace('Avg. Instant Equity', 'Avg. Rent p/w', 1)
    # Replace the second stat card labeled "Avg. 1st Year Growth" -> Avg. 3-Year Growth
    if avg_growth3y is not None:
        # find the next occurrence of a number preceding the label
        html = re.sub(
            r'(>)[^<]*(</span>\s*\n\s*<span[^>]*>\s*Avg\. 1st Year Growth\s*</span>)',
            rf'>{_fmt_percent(avg_growth3y)}\2',
            html,
            count=1
        )
        html = html.replace('Avg. 1st Year Growth', 'Avg. 3-Year Growth', 1)
    RESULTS.write_text(html)

def main():
    props = load_data()
    tpl = load_template()
    write_detail_pages(props, tpl)
    cards = build_cards(props)
    update_results(cards)
    update_top_stats(props)
    cleanup_placeholder_articles()
    print(f"Built {len(props)} property pages and updated results.html")

if __name__ == '__main__':
    main()
