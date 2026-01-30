import os
import re
from collections import defaultdict

ROOT = os.path.join(os.path.dirname(__file__), '..')
IN_LIST = os.path.join(ROOT, 'stitch_pages.txt')
OUT_LIST = os.path.join(ROOT, 'stitch_pages_slugs.txt')

def read(path):
    return open(path, 'r', encoding='utf-8', errors='ignore').read()

def extract_h1(txt: str) -> str | None:
    m = re.search(r'<h1[^>]*>([\s\S]*?)</h1>', txt, flags=re.I)
    if not m:
        return None
    raw = m.group(1)
    raw = re.sub(r'<[^>]+>', '', raw)
    return raw.strip()

def slugify(s: str) -> str:
    s = s.lower()
    # replace apostrophes and en dashes
    s = s.replace('’', "'").replace('–','-').replace('—','-')
    s = re.sub(r"[\'\"]", '', s)
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    if not s:
        s = 'page'
    return s

def main():
    if not os.path.isfile(IN_LIST):
        print('List not found:', IN_LIST)
        raise SystemExit(1)
    files = [l.strip() for l in open(IN_LIST,'r',encoding='utf-8').read().splitlines() if l.strip()]
    # Build slugs
    used = defaultdict(int)
    mapping = []  # (src, out)
    home3_src = None
    for fn in files:
        src_path = os.path.join(ROOT, fn)
        txt = read(src_path)
        h1 = extract_h1(txt) or fn.replace('.html','')
        base = slugify(h1)
        used[base] += 1
        slug = base if used[base] == 1 else f"{base}-{used[base]}"
        out_fn = slug + '.html'
        mapping.append((fn, out_fn))
        if fn == 'home-3.html':
            home3_src = src_path

    written = []
    for src, out in mapping:
        src_path = os.path.join(ROOT, src)
        out_path = os.path.join(ROOT, out)
        with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
            txt = f.read()
        with open(out_path, 'w', encoding='utf-8') as w:
            w.write(txt)
        written.append(out)
        print('Wrote', out)

    # Make home-3 the homepage
    if home3_src and os.path.isfile(home3_src):
        txt = read(home3_src)
        with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8') as w:
            w.write(txt)
        print('Set index.html from home-3.html')
    else:
        print('WARNING: home-3.html not found; index.html unchanged')

    # Save ordered list for nav (index first, then others excluding index)
    out_list = []
    out_list.append('index.html')
    for _, out in mapping:
        if out != 'index.html':
            out_list.append(out)
    with open(OUT_LIST, 'w', encoding='utf-8') as lst:
        for name in out_list:
            lst.write(name + '\n')
    print('Saved slugs list to', OUT_LIST)

if __name__ == '__main__':
    main()

