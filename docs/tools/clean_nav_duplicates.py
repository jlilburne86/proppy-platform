import os
import re

ROOT = os.path.join(os.path.dirname(__file__), '..')

def extract_between(txt, start, end):
    m = re.search(start + r'([\s\S]*?)' + end, txt, flags=re.I)
    if not m:
        return None, None, None
    return txt[:m.start(1)], m.group(1), txt[m.end(1):]

def clean_nav(html: str) -> str:
    # Find the first <nav>...</nav>
    nav_m = re.search(r'<nav[\s\S]*?</nav>', html, flags=re.I)
    if not nav_m:
        return html
    nav = nav_m.group(0)
    # Extract the nav inner wrapper (max-w-7xl container)
    pre, inner, post = extract_between(nav, r'<div[^>]*class="[^"]*max-w-7xl[^"]*"[^>]*>', r'</div>')
    if inner is None:
        return html
    # Find brand block (first flex items-center)
    brand_m = re.search(r'<div[^>]*class="[^"]*flex[^"]*items-center[^"]*"[^>]*>[\s\S]*?</div>', inner, flags=re.I)
    brand = brand_m.group(0) if brand_m else ''
    # Find first link container with md:flex and gap-8
    links_m = re.search(r'<div[^>]*class="[^"]*md:flex[^"]*gap-8[^"]*"[^>]*>[\s\S]*?</div>', inner, flags=re.I)
    if not links_m:
        # nothing to clean
        return html
    links_container = links_m.group(0)
    # Keep CTA block: last flex items-center gap-4 (if any)
    cta_m_all = list(re.finditer(r'<div[^>]*class="[^"]*flex[^"]*items-center[^"]*gap-4[^"]*"[^>]*>[\s\S]*?</div>', inner, flags=re.I))
    cta = cta_m_all[-1].group(0) if cta_m_all else ''
    # Rebuild inner: brand + links_container + cta
    new_inner = brand + '\n' + links_container + (('\n' + cta) if cta else '')
    new_nav = pre + new_inner + post
    # Replace in full html
    return html[:nav_m.start()] + new_nav + html[nav_m.end():]

def main():
    updated = []
    for name in os.listdir(ROOT):
        if not name.endswith('.html'):
            continue
        path = os.path.join(ROOT, name)
        txt = open(path, 'r', encoding='utf-8', errors='ignore').read()
        new = clean_nav(txt)
        if new != txt:
            with open(path, 'w', encoding='utf-8') as w:
                w.write(new)
            updated.append(name)
    print('Cleaned nav duplicates in', len(updated), 'pages')
    for f in updated:
        print('-', f)

if __name__ == '__main__':
    main()

