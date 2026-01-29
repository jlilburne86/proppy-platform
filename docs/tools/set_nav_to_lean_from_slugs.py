import os
import re

ROOT = os.path.join(os.path.dirname(__file__), '..')
SLUG_LIST = os.path.join(ROOT, 'stitch_pages_slugs.txt')

# Choose a lean nav from available slugs
PREFERRED = [
    ('index.html', 'Home'),
    ('how-it-works.html', 'How It Works'),
    ('transparent-pricing-clear-value-no-surprises.html', 'Pricing'),
    ('built-for-signal-not-noise.html', 'Technology'),
    ('investor-resources-hub.html', 'Resources'),
    ('what-results-means.html', 'Results'),
    ('book.html', 'Get Started'),
]

def replace_nav_links(html: str, items) -> str:
    nav_m = re.search(r'<nav[\s\S]*?</nav>', html, flags=re.I)
    if not nav_m:
        return html
    nav = nav_m.group(0)
    container_m = re.search(r'<div[^>]*class="[^"]*md:flex[^"]*gap-8[^"]*"[^>]*>([\s\S]*?)</div>', nav, flags=re.I)
    if not container_m:
        return html
    old = container_m.group(0)
    links_html = '\n'.join([f'<a class="hover:text-primary dark:hover:text-white transition-colors" href="{href}">{label}</a>' for href,label in items])
    new = re.sub(r'>([\s\S]*?)</div>', '>' + links_html + '</div>', old)
    new_nav = nav.replace(old, new, 1)
    return html[:nav_m.start()] + new_nav + html[nav_m.end():]

def main():
    if not os.path.isfile(SLUG_LIST):
        print('Slug list missing:', SLUG_LIST)
        raise SystemExit(1)
    # Filter preferred by availability
    available = set([l.strip() for l in open(SLUG_LIST,'r',encoding='utf-8').read().splitlines() if l.strip()])
    items = [item for item in PREFERRED if item[0] in available or item[0] == 'book.html']
    updated = []
    for name in available:
        path = os.path.join(ROOT, name)
        txt = open(path, 'r', encoding='utf-8', errors='ignore').read()
        new = replace_nav_links(txt, items)
        if new != txt:
            with open(path, 'w', encoding='utf-8') as w:
                w.write(new)
            updated.append(name)
    # Also apply to book.html if present
    bpath = os.path.join(ROOT, 'book.html')
    if os.path.isfile(bpath):
        txt = open(bpath, 'r', encoding='utf-8', errors='ignore').read()
        new = replace_nav_links(txt, items)
        if new != txt:
            with open(bpath, 'w', encoding='utf-8') as w:
                w.write(new)
            updated.append('book.html')
    print('Set lean nav in', len(updated), 'pages')
    for f in updated:
        print('-', f)

if __name__ == '__main__':
    main()

