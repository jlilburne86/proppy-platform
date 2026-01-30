import os
import re
import html as ihtml

ROOT = os.path.join(os.path.dirname(__file__), '..')
LIST_PATH = os.path.join(ROOT, 'stitch_pages_slugs.txt')

def read(path):
    return open(path, 'r', encoding='utf-8', errors='ignore').read()

def extract_h1(txt: str) -> str | None:
    m = re.search(r'<h1[^>]*>([\s\S]*?)</h1>', txt, flags=re.I)
    if not m:
        return None
    raw = m.group(1)
    raw = re.sub(r'<[^>]+>', '', raw)
    return ihtml.unescape(raw).strip()

def label_for(filename: str, txt: str) -> str:
    if filename == 'index.html':
        return 'Home'
    h1 = extract_h1(txt) or ''
    if h1:
        return ' '.join(h1.split())[:80]
    title_m = re.search(r'<title>([\s\S]*?)</title>', txt, flags=re.I)
    if title_m:
        return ihtml.unescape(title_m.group(1)).strip()
    return filename.replace('.html','').replace('-', ' ').title()

def replace_nav_links(html: str, items: list[tuple[str,str]]) -> str:
    nav_m = re.search(r'<nav[\s\S]*?</nav>', html, flags=re.I)
    if not nav_m:
        return html
    nav = nav_m.group(0)
    container_m = re.search(r'<div[^>]*class="[^"]*md:flex[^"]*gap-8[^"]*"[^>]*>([\s\S]*?)</div>', nav, flags=re.I)
    if not container_m:
        return html
    old = container_m.group(0)
    links_html = '\n'.join([f'<a class="hover:text-primary dark:hover:text-white transition-colors" href="{ihtml.escape(fn)}">{ihtml.escape(lbl)}</a>' for fn,lbl in items])
    new = re.sub(r'>([\s\S]*?)</div>', '>' + links_html + '</div>', old)
    new_nav = nav.replace(old, new, 1)
    return html[:nav_m.start()] + new_nav + html[nav_m.end():]

def main():
    if not os.path.isfile(LIST_PATH):
        print('List not found:', LIST_PATH)
        raise SystemExit(1)
    files = [l.strip() for l in open(LIST_PATH,'r',encoding='utf-8').read().splitlines() if l.strip()]
    items = []
    for fn in files:
        path = os.path.join(ROOT, fn)
        if not os.path.isfile(path):
            continue
        txt = read(path)
        items.append((fn, label_for(fn, txt)))
    updated = []
    for fn in files:
        path = os.path.join(ROOT, fn)
        txt = read(path)
        new = replace_nav_links(txt, items)
        if new != txt:
            with open(path, 'w', encoding='utf-8') as w:
                w.write(new)
            updated.append(fn)
    print('Updated nav in', len(updated), 'pages (slugs set):')
    for n in updated:
        print('-', n)

if __name__ == '__main__':
    main()

