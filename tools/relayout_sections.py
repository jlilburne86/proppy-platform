import os
import re

ROOT = os.path.join(os.path.dirname(__file__), '..')

# Identify the product sections we inserted by their badge keywords
SECTION_MARKERS = {
    'how-it-works.html': ('In The App',),
    'technology.html': ('Interface Highlights',),
    'pricing.html': ('Included Tools',),
    'resources.html': ('Product Guides',),
    'results.html': ('Portfolio Snapshot',),
}

def move_section_into_main(path: str, badges: tuple[str, ...]) -> bool:
    txt = open(path, 'r', encoding='utf-8', errors='ignore').read()
    orig = txt
    # Find the main block
    main_m = re.search(r'<main[^>]*>', txt, flags=re.I)
    main_end = re.search(r'</main>', txt, flags=re.I)
    if not main_m or not main_end:
        return False
    # Find a section that contains any of the badge labels
    sec_m = None
    for label in badges:
        m = re.search(rf'<section[\s\S]*?<span[^>]*>\s*<span[^>]*>[^<]*</span>\s*{re.escape(label)}[\s\S]*?</section>', txt, flags=re.I)
        if m:
            sec_m = m
            break
    if not sec_m:
        return False
    start, end = sec_m.start(), sec_m.end()
    section_html = txt[start:end]
    # Remove from current location (even if it is already in main, so we can reinsert precisely)
    txt_wo = txt[:start] + txt[end:]
    # Recompute main positions in new string
    main_open = re.search(r'<main[^>]*>', txt_wo, flags=re.I)
    main_close = re.search(r'</main>', txt_wo, flags=re.I)
    if not main_open or not main_close:
        return False
    # Find first section inside main to insert after; fallback to right after <main>
    after_main_idx = main_open.end()
    inner = txt_wo[after_main_idx:main_close.start()]
    first_sec_m = re.search(r'<section[\s\S]*?</section>', inner, flags=re.I)
    if first_sec_m:
        insert_at = after_main_idx + first_sec_m.end()
    else:
        insert_at = after_main_idx
    new_txt = txt_wo[:insert_at] + '\n' + section_html + '\n' + txt_wo[insert_at:]
    open(path, 'w', encoding='utf-8').write(new_txt)
    return True

def main():
    changed = []
    for fname, badges in SECTION_MARKERS.items():
        path = os.path.join(ROOT, fname)
        if os.path.isfile(path):
            if move_section_into_main(path, badges):
                changed.append(fname)
    print('Relayout moved sections in:', ', '.join(changed) or 'none')

if __name__ == '__main__':
    main()
