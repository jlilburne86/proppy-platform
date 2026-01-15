import os
import re
import html as ihtml

ROOT = os.path.join(os.path.dirname(__file__), '..')
LIST_PATH = os.path.join(ROOT, 'stitch_pages.txt')

def read(path):
    return open(path, 'r', encoding='utf-8', errors='ignore').read()

def extract_h1(txt: str) -> str | None:
    m = re.search(r'<h1[^>]*>([\s\S]*?)</h1>', txt, flags=re.I)
    if not m:
        return None
    raw = m.group(1)
    raw = re.sub(r'<[^>]+>', '', raw)
    return ihtml.unescape(raw).strip()

def extract_title(txt: str) -> str | None:
    m = re.search(r'<title>([\s\S]*?)</title>', txt, flags=re.I)
    if not m:
        return None
    return ihtml.unescape(m.group(1)).strip()

def short_label(h1: str, title: str, filename: str) -> str:
    if filename == 'index.html':
        return 'Home'
    s = (h1 or '').strip()
    t = (title or '').strip()
    low = s.lower()
    if 'how it works' in low:
        return 'How It Works'
    if 'pricing' in low:
        return 'Pricing'
    if 'technology' in low:
        return 'Technology'
    if 'resources' in low:
        return 'Resources'
    if 'case stud' in low:
        return 'Case Studies'
    if 'results' in low:
        return 'Results'
    if 'solutions' in low:
        return 'Solutions'
    if 'contact' in low:
        return 'Contact'
    if ' - ' in t:
        tpart = t.split(' - ',1)[1].strip()
        if tpart:
            return tpart
    words = re.findall(r"\w[\w'’\-]*", s)
    if words:
        return ' '.join(words[:4]).title()
    return filename.replace('-', ' ').replace('.html','').title()

def build_items(file_list: list[str]) -> list[tuple[str,str]]:
    items = []
    for fn in file_list:
        path = os.path.join(ROOT, fn)
        if not os.path.isfile(path):
            continue
        txt = read(path)
        h1 = extract_h1(txt) or ''
        title = extract_title(txt) or ''
        label = short_label(h1, title, fn)
        items.append((fn, label))
    # de-duplicate while preserving order by filename
    seen = set()
    dedup = []
    for fn, label in items:
        if fn in seen:
            continue
        seen.add(fn)
        dedup.append((fn, label))
    return dedup

def replace_nav_links(html: str, items: list[tuple[str,str]]) -> str:
    nav_m = re.search(r'<nav[\s\S]*?</nav>', html, flags=re.I)
    if not nav_m:
        return html
    nav = nav_m.group(0)
    # A lot of Stitch navs use this container signature
    container_m = re.search(r'<div[^>]*class="[^"]*md:flex[^"]*gap-8[^"]*"[^>]*>([\s\S]*?)</div>', nav, flags=re.I)
    if not container_m:
        return html
    old = container_m.group(0)
    links_html = '\n'.join([f'<a class="hover:text-primary dark:hover:text-white transition-colors" href="{ihtml.escape(fn)}">{ihtml.escape(label)}</a>' for fn,label in items])
    new = re.sub(r'>([\s\S]*?)</div>', '>' + links_html + '</div>', old)
    new_nav = nav.replace(old, new, 1)
    return html[:nav_m.start()] + new_nav + html[nav_m.end():]

def main():
    if not os.path.isfile(LIST_PATH):
        print('List file not found:', LIST_PATH)
        raise SystemExit(1)
    files = [l.strip() for l in open(LIST_PATH, 'r', encoding='utf-8').read().splitlines() if l.strip()]
    items = build_items(files)
    updated = []
    for fn in files:
        path = os.path.join(ROOT, fn)
        txt = read(path)
        new = replace_nav_links(txt, items)
        if new != txt:
            with open(path, 'w', encoding='utf-8') as w:
                w.write(new)
            updated.append(fn)
    print('Updated nav in', len(updated), 'pages (stitch set only):')
    for n in updated:
        print('-', n)

if __name__ == '__main__':
    main()

