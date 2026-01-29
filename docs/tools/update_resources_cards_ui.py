import re, json, html
from pathlib import Path

ROOT = Path('/Users/boo2/Desktop/proppy')
RES = ROOT / 'resources.html'
DATA = ROOT / 'data/article_scorecards.json'

def load_data():
    try:
        return json.loads(DATA.read_text(encoding='utf-8'))
    except Exception:
        return {}

def slugify(t: str) -> str:
    s = t.lower()
    s = re.sub(r"[’'“”]", '', s)
    s = re.sub(r"[^a-z0-9]+", '-', s).strip('-')
    return s

STOP = set(['the','and','of','in','to','for','a','an','vs','vs.','with','on','by','how','why','what'])

def derive_tags(title: str, cat: str, img_kw: str|None) -> list[str]:
    tags=[cat] if cat else []
    if img_kw:
        tags.extend([w.strip() for w in img_kw.split()[:2]])
    # add two tokens from title
    tokens=[w for w in re.findall(r'[a-zA-Z]+', title.lower()) if w not in STOP]
    for w in tokens:
        if w not in tags:
            tags.append(w.capitalize())
        if len(tags)>=3: break
    return tags[:3]

def fallback_unsplash(slug: str, cat: str|None) -> str:
    base = 'https://source.unsplash.com/600x360/?'
    tokens = [w for w in re.findall(r'[a-zA-Z]+', slug)][:2]
    kws = []
    if cat:
        kws.append(cat.lower())
    kws += tokens or ['australia','property']
    return base + ','.join(kws)

def replace_top_visual(block: str, hero: str, title: str) -> str:
    # Remove known placeholder visual blocks (bg-... h-48 ...)
    block = re.sub(r'<div class=\\"[^\\"]*h-48[^\\"]*\\"[\s\S]*?</div>\n', '', block, count=1)
    # Ensure our card-thumb at top
    if 'card-thumb' not in block:
        block = re.sub(r'(<article[^>]*>)', r"\1\n<div class=\"card-thumb\"><img src=\""+html.escape(hero)+"\" alt=\""+html.escape(title)+"\"/></div>\n", block, count=1)
    else:
        # Update existing
        block = re.sub(r'(<div class=\\"card-thumb\\">)\s*<img[^>]*>\s*(</div>)', r"\1<img src=\""+html.escape(hero)+"\" alt=\""+html.escape(title)+"\"/>\2", block, count=1)
    return block

def main():
    data = load_data()
    html_txt = RES.read_text(encoding='utf-8')
    # process each article tile
    def repl(m):
        block = m.group(0)
        # locate title and label
        t_m = re.search(r'<h3[^>]*>([\s\S]*?)</h3>', block)
        if not t_m: return block
        title = re.sub(r'\s+',' ', t_m.group(1)).strip()
        slug = slugify(title)
        entry = data.get(slug, {})
        imgs = entry.get('images') or []
        hero = imgs[0]['src'] if imgs else None
        if not hero:
            # fallback unsplash based on slug/category
            cat_m = re.search(r'<span class=\"text-\[10px\][^>]*>([^<]+)</span>', block)
            cat = cat_m.group(1).strip() if cat_m else ''
            hero = fallback_unsplash(slug, cat)
        # normalize: remove any stale thumb and placeholder, then inject
        block = re.sub(r'<div class=\"card-thumb\">[\s\S]*?</div>\n?', '', block)
        block = replace_top_visual(block, hero, title)
        # derive tags
        cat_m = re.search(r'<span class=\"text-\[10px\][^>]*>([^<]+)</span>', block)
        cat = cat_m.group(1).strip() if cat_m else ''
        kw = None
        if imgs and 'kw' in imgs[0]:
            kw = imgs[0]['kw']
        tags = derive_tags(title, cat, kw)
        tag_html = '<div class="tag-list">' + ''.join([f'<span class="tag">{html.escape(t)}</span>' for t in tags]) + '</div>'
        # remove stale tag-list
        block = re.sub(r'<div class=\"tag-list\">[\s\S]*?</div>', '', block)
        # place tags after summary if present; else before CTA container
        new_block = re.sub(r'(</p>\s*\n\s*)(<div class=\"mt-auto\">)', r"\1"+tag_html+r"\n\2", block, count=1)
        if new_block == block:
            new_block = re.sub(r'(<div class=\"mt-auto\">)', tag_html + r"\n\1", block, count=1)
        block = new_block
        return block
    new_html = re.sub(r'<article[\s\S]*?</article>', repl, html_txt)
    if new_html != html_txt:
        RES.write_text(new_html, encoding='utf-8')
        print('Updated resource cards UI (thumb + tags)')
    else:
        print('No changes applied to resource cards')

if __name__=='__main__':
    main()
