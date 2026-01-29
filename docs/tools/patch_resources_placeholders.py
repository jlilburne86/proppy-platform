import re, html
from pathlib import Path

RES = Path('/Users/boo2/Desktop/proppy/resources.html')

def slugify(t: str) -> str:
    s = t.lower()
    s = re.sub(r"[’'“”]", '', s)
    s = re.sub(r"[^a-z0-9]+", '-', s).strip('-')
    return s

def unsplash(cat, title):
    base='https://source.unsplash.com/600x360/?'
    toks = re.findall(r'[a-zA-Z]+', (title or ''))[:2]
    kws=[]
    if cat: kws.append(cat.lower())
    kws += toks or ['australia','property']
    return base+','.join(kws)

def main():
    html_txt = RES.read_text(encoding='utf-8')
    # iterate over articles and replace top colored block with card-thumb img
    def repl_article(m):
        block = m.group(0)
        # title
        t_m = re.search(r'<h3[^>]*>([\s\S]*?)</h3>', block)
        if not t_m:
            return block
        title = re.sub(r'\s+', ' ', t_m.group(1)).strip()
        c_m = re.search(r'<span class=\"text-\[10px\][^>]*>([^<]+)</span>', block)
        cat = c_m.group(1).strip() if c_m else ''
        hero = unsplash(cat, title)
        # find first colored visual block by h-48 rounded
        new_block = re.sub(r'<div class=\"[^\"]*h-48[^\"]*\"[\s\S]*?</div>',
                           '<div class="card-thumb"><img src="'+html.escape(hero)+'" alt="'+html.escape(title)+'"/></div>',
                           block, count=1)
        return new_block

    new_html = re.sub(r'<article[\s\S]*?</article>', repl_article, html_txt)
    if new_html != html_txt:
        RES.write_text(new_html, encoding='utf-8')
        print('Patched placeholders with thumbnails in resources.html')
    else:
        print('No changes applied')

if __name__=='__main__':
    main()

