import os
import re

ROOT = os.path.join(os.path.dirname(__file__), '..')
STITCH = os.path.join(ROOT, 'stitch_corporate_landing_page_redesign_v1 2')
LIST_PATH = os.path.join(ROOT, 'stitch_pages.txt')

def find_candidates(stitch_dir):
    pages = {}
    for dirpath, dirnames, filenames in os.walk(stitch_dir):
        if 'code.html' in filenames:
            rel = os.path.relpath(dirpath, stitch_dir)
            pages[rel] = os.path.join(dirpath, 'code.html')
    return pages

def slug_for(key):
    low = key.lower()
    # common explicit maps
    if 'how_it_works' in low:
        return 'how-it-works.html'
    if 'pricing' in low:
        return 'pricing.html'
    if 'technology' in low:
        return 'technology.html'
    # default: sanitize folder name
    s = low
    s = re.sub(r'^proppy[_-]?', '', s)
    s = re.sub(r'[_\s]+', '-', s)
    s = re.sub(r'[^a-z0-9\-]', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    if not s.endswith('.html'):
        s += '.html'
    return s

def pick_home_variants(keys):
    homes = [k for k in keys if 'homepage' in k.lower()]
    # Return list of (variant_name, number)
    out = []
    for k in homes:
        m = re.search(r'_(\d+)$', k)
        n = int(m.group(1)) if m else 0
        out.append((k, n))
    out.sort(key=lambda x: x[1])
    return out

def main():
    if not os.path.isdir(STITCH):
        print('Stitch folder not found:', STITCH)
        raise SystemExit(1)
    pages = find_candidates(STITCH)
    if not pages:
        print('No code.html files found under', STITCH)
        raise SystemExit(1)

    # Build output map (filename -> source path). Keep content verbatim.
    route_map = {}
    # Handle home variants explicitly
    home_variants = pick_home_variants(list(pages.keys()))
    index_written = False
    for key, num in home_variants:
        src = pages[key]
        # Write a numbered variant as home-N.html
        out_num = f'home-{num}.html' if num else 'home.html'
        route_map[out_num] = src
        # Pick the highest-numbered variant for index.html
        index_written = True  # We'll set index later to the last in loop
        index_target = src
    if index_written:
        route_map['index.html'] = index_target

    # Non-home pages
    for key, src in pages.items():
        if 'homepage' in key.lower():
            continue
        out = slug_for(key)
        route_map[out] = src

    # Write files verbatim
    written = []
    for out, src in sorted(route_map.items()):
        with open(src, 'r', encoding='utf-8', errors='ignore') as f:
            txt = f.read()
        with open(os.path.join(ROOT, out), 'w', encoding='utf-8') as w:
            w.write(txt)
        written.append(out)
        print('Wrote', out)

    # Save list of stitch pages for downstream nav sync
    with open(LIST_PATH, 'w', encoding='utf-8') as lst:
        for name in written:
            lst.write(name + '\n')
    print('Saved list to', LIST_PATH)

if __name__ == '__main__':
    main()

