import re, html, json
from pathlib import Path

ROOT = Path('/Users/boo2/Desktop/proppy')
RES = ROOT / 'resources.html'
ART_DIR = ROOT / 'articles'
SCORE = ROOT / 'data/article_scorecards.json'

def load_scores():
    try:
        return json.loads(SCORE.read_text(encoding='utf-8'))
    except Exception:
        return {}

def slugify(t: str) -> str:
    s = t.lower()
    s = re.sub(r"[’'“”]", '', s)
    s = re.sub(r"[^a-z0-9]+", '-', s).strip('-')
    return s

def parse_fm(slug: str):
    p = ART_DIR / f'{slug}.md'
    if not p.exists():
        return None
    txt = p.read_text(encoding='utf-8', errors='ignore')
    if not txt.strip().startswith('---'):
        return None
    fm = txt.split('---',2)[1]
    def get(k):
        m = re.search(rf'\n{k}:\s*\"([^\"]+)\"', fm)
        return m.group(1) if m else ''
    return {
        'reading_time': get('reading_time'),
        'date': re.search(r'\ndate:\s*\"([^\"]+)\"', fm).group(1) if re.search(r'\ndate:\s*\"', fm) else ''
    }

def compute_outlook(metrics: dict):
    if not metrics: return ('Neutral','outlook-neutral')
    vac = (metrics.get('vacancy') or {}).get('value','').lower()
    rent = (metrics.get('rent') or {}).get('value','').lower()
    listg = (metrics.get('listings') or {}).get('value','').lower()
    pipe = (metrics.get('pipeline') or {}).get('value','').lower()
    if ('tight' in vac or 'target' in vac) and 'rising' in rent and ('flat' in listg or 'stable' in listg) and ('constrained' in pipe or 'limited' in pipe):
        return ('Constructive','outlook-constructive')
    if ('rising' in vac and 'up' in listg) or ('oversupply' in pipe):
        return ('Cautious','outlook-cautious')
    return ('Neutral','outlook-neutral')

def main():
    data = load_scores()
    html_txt = RES.read_text(encoding='utf-8')
    def repl(m):
        block = m.group(0)
        # title
        t_m = re.search(r'<h3[^>]*>([\s\S]*?)</h3>', block)
        if not t_m: return block
        title = re.sub(r'\s+',' ', t_m.group(1)).strip()
        slug = slugify(title)
        fm = parse_fm(slug) or {}
        metrics = data.get(slug, {}).get('metrics', {})
        outlook_txt, outlook_cls = compute_outlook(metrics)
        # insert outlook pill under title if not present
        if 'outlook-badge' not in block:
            block = re.sub(r'(<h3[^>]*>[\s\S]*?</h3>)', r"\1\n<span class=\"outlook-badge "+outlook_cls+"\">Outlook: "+outlook_txt+"</span>", block, count=1)
        # also overlay pill inside thumbnail for stronger visual
        if 'card-thumb' in block and 'thumb-overlay' not in block:
            block = re.sub(r'(</div>\s*\n)(\s*<h3)', r"<div class=\"thumb-overlay\"><span class=\"outlook-badge "+outlook_cls+"\">Outlook: "+outlook_txt+"</span></div>\n\1\2", block, count=1)
        # insert meta row (read time • date) above CTA
        meta_parts = []
        # compute read time from markdown body length if available
        try:
            md = (ART_DIR / f'{slug}.md').read_text(encoding='utf-8', errors='ignore')
            if md.startswith('---'):
                body = md.split('---',2)[2]
            else:
                body = md
            import re as _re
            words = len(_re.findall(r'\b\w+\b', body))
            mins = max(1, round(words/220))
            meta_parts.append(f"{mins} min read")
        except Exception:
            if fm.get('reading_time'): meta_parts.append(fm['reading_time'])
        # find date already on card
        d_m = re.search(r'<span class=\"text-xs text-slate-400\">([^<]+)</span>', block)
        if d_m:
            meta_parts.append(d_m.group(1).strip())
        meta_html = ''
        if meta_parts:
            meta_html = '<div class="text-xs text-slate-500 mt-1">' + ' • '.join(html.escape(x) for x in meta_parts) + '</div>'
            block = re.sub(r'(</p>\s*\n\s*)(<div class=\"tag-list\">)?', r"\1"+meta_html+"\n"+(r"\2" if r"\2" else ''), block, count=1)
        return block
    new_html = re.sub(r'<article[\s\S]*?</article>', repl, html_txt)
    if new_html != html_txt:
        RES.write_text(new_html, encoding='utf-8')
        print('Enhanced resource tiles with Outlook and meta row')
    else:
        print('No changes applied')

if __name__=='__main__':
    main()
