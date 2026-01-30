import re, json, html
from pathlib import Path

ROOT = Path('/Users/boo2/Desktop/proppy')
RES = ROOT / 'resources.html'
DATA = ROOT / 'data/article_scorecards.json'

def slugify(t: str) -> str:
    s = t.lower()
    s = re.sub(r"[’'“”]", '', s)
    s = re.sub(r"[^a-z0-9]+", '-', s).strip('-')
    return s

def load_data():
    try:
        return json.loads(DATA.read_text(encoding='utf-8'))
    except Exception:
        return {}

def build_strip(metrics: dict) -> str:
    tiles=[]
    order=['vacancy','rent','listings','pipeline']
    for k in order:
        m = metrics.get(k)
        if not m: continue
        label = html.escape(m.get('label',''))
        value = html.escape(m.get('value',''))
        tiles.append(f'<div class="score-tile"><div class="score-label">{label}</div><div class="score-value">{value}</div></div>')
    if not tiles:
        return ''
    return '<div class="score-mini"><div class="score-grid">' + '\n'.join(tiles[:4]) + '</div></div>'

def main():
    data = load_data()
    html_txt = RES.read_text(encoding='utf-8')
    # replace within each <article>...</article>
    def repl_article(m):
        block = m.group(0)
        # title
        t_m = re.search(r'<h3[^>]*>([\s\S]*?)</h3>', block)
        if not t_m:
            return block
        title = re.sub(r'\s+',' ', t_m.group(1)).strip()
        slug = slugify(title)
        metrics = data.get(slug, {}).get('metrics')
        if not metrics:
            return block
        strip = build_strip(metrics)
        if not strip:
            return block
        # insert strip just before CTA container
        block = re.sub(r'(</p>[^<]*\n\s*)(<div class=\"mt-auto\">)', r"\1" + strip + r"\n\2", block, count=1)
        return block

    new_html = re.sub(r'<article[\s\S]*?</article>', repl_article, html_txt)
    if new_html != html_txt:
        RES.write_text(new_html, encoding='utf-8')
        print('Injected score strips into resources tiles')
    else:
        print('No changes applied')

if __name__=='__main__':
    main()

