import os
import re
import html as ihtml

ROOT = os.path.join(os.path.dirname(__file__), '..')

def read(path):
    return open(path,'r',encoding='utf-8',errors='ignore').read()

def extract_h1(txt: str) -> str | None:
    m = re.search(r'<h1[^>]*>([\s\S]*?)</h1>', txt, flags=re.I)
    if not m:
        return None
    raw = m.group(1)
    raw = re.sub(r'<[^>]+>', '', raw)
    return ihtml.unescape(raw).strip()

def label_for(fn: str, txt: str) -> str:
    if fn == 'index.html':
        return 'Home'
    h1 = extract_h1(txt)
    if h1:
        label = ' '.join(h1.split())
        return label if len(label) <= 70 else label[:67] + '…'
    m = re.search(r'<title>([\s\S]*?)</title>', txt, flags=re.I)
    if m:
        return ihtml.unescape(m.group(1)).strip()
    return fn.replace('.html','').replace('-', ' ').title()

def build_items():
    files = [f for f in os.listdir(ROOT) if f.endswith('.html')]
    # Keep index first and exclude site-map from nav (but still accessible)
    files = [f for f in files if f != 'site-map.html']
    files.sort()
    if 'index.html' in files:
        files.remove('index.html')
        files.insert(0, 'index.html')
    items = []
    for fn in files:
        txt = read(os.path.join(ROOT, fn))
        items.append((fn, label_for(fn, txt)))
    return items

def replace_nav_links(html: str, items) -> str:
    nav_m = re.search(r'<nav[\s\S]*?</nav>', html, flags=re.I)
    if not nav_m:
        return html
    nav = nav_m.group(0)
    container_m = re.search(r'<div[^>]*class="[^"]*md:flex[^"]*gap-8[^"]*"[^>]*>([\s\S]*?)</div>', nav, flags=re.I)
    if not container_m:
        return html
    old = container_m.group(0)
    links_html = '\n'.join([f'<a class="hover:text-primary dark:hover:text-white transition-colors" href="{ihtml.escape(href)}">{ihtml.escape(lbl)}</a>' for href,lbl in items])
    new = re.sub(r'>([\s\S]*?)</div>', '>' + links_html + '</div>', old)
    new_nav = nav.replace(old, new, 1)
    return html[:nav_m.start()] + new_nav + html[nav_m.end():]

def main():
    items = build_items()
    updated = []
    for name in os.listdir(ROOT):
        if not name.endswith('.html'):
            continue
        path = os.path.join(ROOT, name)
        html = read(path)
        new = replace_nav_links(html, items)
        if new != html:
            with open(path, 'w', encoding='utf-8') as w:
                w.write(new)
            updated.append(name)
    print('Updated top nav in', len(updated), 'pages')
    for f in updated:
        print('-', f)

if __name__ == '__main__':
    main()

