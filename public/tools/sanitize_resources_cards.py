import re, html
from pathlib import Path

ROOT = Path('/Users/boo2/Desktop/proppy')
RES = ROOT / 'resources.html'

FM_KEYS = [
  'title:', 'description:', 'category:', 'audience:', 'reading_time:',
  'publish_status:', 'author:', 'owner:', 'next_review_date:', 'sources:'
]

def fallback_unsplash(slug: str, cat: str|None) -> str:
    base = 'https://source.unsplash.com/600x360/?'
    tokens = [w for w in re.findall(r'[a-zA-Z]+', slug)][:2]
    kws = []
    if cat: kws.append(cat.lower())
    kws += tokens or ['australia','property']
    return base + ','.join(kws)

def slugify(t: str) -> str:
    s = t.lower()
    s = re.sub(r"[’'“”]", '', s)
    s = re.sub(r"[^a-z0-9]+", '-', s).strip('-')
    return s

def sanitize_block(block: str) -> str:
    # remove any YAML-like front matter lines
    for key in FM_KEYS:
        block = re.sub(rf'\n\s*{re.escape(key)}\s*\"[^\"]*\"\s*\n?', '\n', block)
    # remove bare keys like "- name:" lists
    block = re.sub(r'\n\s*-\s*name:\s*\"[^\"]*\"\s*\n?', '\n', block)
    block = re.sub(r'\n\s*url:\s*\"[^\"]*\"\s*\n?', '\n', block)
    return block

def inject_thumb(block: str) -> str:
    if 'card-thumb' in block:
        return block
    # derive title + category
    t_m = re.search(r'<h3[^>]*>([\s\S]*?)</h3>', block)
    if not t_m:
        return block
    title = re.sub(r'\s+',' ', t_m.group(1)).strip()
    cat_m = re.search(r'<span class=\"text-\[10px\][^>]*>([^<]+)</span>', block)
    cat = cat_m.group(1).strip() if cat_m else ''
    hero = fallback_unsplash(slugify(title), cat)
    return re.sub(r'(<article[^>]*>)', r"\1\n<div class=\"card-thumb\"><img src=\""+html.escape(hero)+"\" alt=\""+html.escape(title)+"\"/></div>\n", block, count=1)

def main():
    html_txt = RES.read_text(encoding='utf-8')
    def repl(m):
        block = m.group(0)
        block = sanitize_block(block)
        block = inject_thumb(block)
        # ensure CTA hrefs point to html
        block = re.sub(r'href=\"(/articles/[^\"]+)\.md\"', r'href="\1.html"', block)
        return block
    new_html = re.sub(r'<article[\s\S]*?</article>', repl, html_txt)
    if new_html != html_txt:
        RES.write_text(new_html, encoding='utf-8')
        print('Sanitized resource cards (removed front matter, ensured thumbs, fixed hrefs)')
    else:
        print('No changes applied')

if __name__=='__main__':
    main()

