import re, datetime
from pathlib import Path

ROOT = Path('/Users/boo2/Desktop/proppy')
ART = ROOT / 'articles'
RES = ROOT / 'resources.html'

TITLE_TO_SLUG = {
  'Quarterly Review: East Coast Capitals': 'quarterly-review-east-coast-capitals',
  'Yield vs. Capital Growth: Finding the Balance': 'yield-vs-capital-growth-finding-the-balance',
  'Suburb Spotlight: Logan Reserve': 'suburb-spotlight-logan-reserve',
  'Tax Depreciation 101': 'tax-depreciation-101',
  'Overcoming Analysis Paralysis': 'overcoming-analysis-paralysis',
  'Interest Rates: The 2024 Forecast': 'interest-rates-the-2024-forecast',
}

def parse_front(text: str) -> dict:
    fm = {}
    if not text.strip().startswith('---'):
        return fm
    fm_raw = text.split('---',2)[1]
    for line in fm_raw.splitlines():
        if ':' in line:
            k,v = line.split(':',1)
            fm[k.strip()] = v.strip().strip('"')
    return fm

def rel_or_date(iso: str) -> str:
    try:
        d = datetime.date.fromisoformat(iso)
    except Exception:
        return iso
    today = datetime.date.today()
    delta = (today - d).days
    if delta >= 0 and delta <= 7:
        return f"{delta} days ago" if delta != 0 else 'Today'
    return d.strftime('%b %d, %Y')

def run():
    html = RES.read_text(encoding='utf-8')
    for title, slug in TITLE_TO_SLUG.items():
        mdp = ART / f'{slug}.md'
        if not mdp.exists():
            continue
        fm = parse_front(mdp.read_text(encoding='utf-8', errors='ignore'))
        date = fm.get('date')
        if not date:
            continue
        display = rel_or_date(date)
        # Update the small date span following the label for this card
        # Find the card by its h3 title, then replace the next occurrence of the date span
        pattern = rf'(<h3[^>]*>\s*{re.escape(title)}\s*</h3>\s*\n\s*<p[\s\S]*?</p>\s*\n\s*<div class=\"mt-auto\">[\s\S]*?</div>|<div class=\"flex items-center gap-3 mb-3\">\s*\n\s*<span[^>]*>[A-Za-z\s]+</span>\s*\n\s*<span class=\"text-xs text-slate-400\">)([^<]+)(</span>)'
        html = re.sub(pattern, lambda m: m.group(1) + display + m.group(3), html, count=1)
    RES.write_text(html, encoding='utf-8')
    print('Synced resource card dates from article front matter')

if __name__=='__main__':
    run()

