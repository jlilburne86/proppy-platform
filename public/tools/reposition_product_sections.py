import os
import re

ROOT = os.path.join(os.path.dirname(__file__), '..')

LABELS = (
    'The Platform',
    'In The App',
    'Interface Highlights',
    'Included Tools',
    'Portfolio Snapshot',
    'Product Guides',
)

def find_main_bounds(html: str):
    mo = re.search(r'<main[^>]*>', html, flags=re.I)
    mc = re.search(r'</main>', html, flags=re.I)
    if not mo or not mc:
        return None
    return mo.start(), mo.end(), mc.start(), mc.end()

def find_labeled_sections(html: str):
    # Return list of (start, end) for sections containing any of the labels
    spans = []
    for m in re.finditer(r'<section[\s\S]*?</section>', html, flags=re.I):
        sec = m.group(0)
        if any(lbl in sec for lbl in LABELS):
            spans.append((m.start(), m.end()))
    return spans

def reposition(html: str) -> str:
    bounds = find_main_bounds(html)
    labeled = find_labeled_sections(html)
    if not labeled:
        return html
    # Determine insertion anchor
    if bounds:
        m_start, m_open_end, m_inner_end, m_close_end = bounds
        inner = html[m_open_end:m_inner_end]
        fs = re.search(r'<section[\s\S]*?</section>', inner, flags=re.I)
        anchor = m_open_end + (fs.end() if fs else 0)
        def is_inside(s):
            return m_open_end <= s < m_inner_end
    else:
        # Fallback: use after first section following </nav>, or before <footer>
        nav_end = re.search(r'</nav>', html, flags=re.I)
        foot_start = re.search(r'<footer', html, flags=re.I)
        start = nav_end.end() if nav_end else 0
        end = foot_start.start() if foot_start else len(html)
        inner = html[start:end]
        fs = re.search(r'<section[\s\S]*?</section>', inner, flags=re.I)
        anchor = (start + fs.end()) if fs else start
        def is_inside(s):
            return start <= s < end
    # Collect labeled sections not inside the anchor region
    removed = []
    for s,e in labeled:
        if not is_inside(s):
            removed.append((s,e))
    if not removed:
        return html
    # Remove from html, adjusting indices
    removed.sort()
    new_html = html
    shift = 0
    extracted = []
    for s,e in removed:
        s2, e2 = s+shift, e+shift
        extracted.append(new_html[s2:e2])
        new_html = new_html[:s2] + new_html[e2:]
        shift -= (e - s)
    # Compute new anchor index in updated string
    if bounds:
        b2 = find_main_bounds(new_html)
        if not b2:
            return html
        m_start2, m_open_end2, m_inner_end2, m_close_end2 = b2
        inner2 = new_html[m_open_end2:m_inner_end2]
        fs2 = re.search(r'<section[\s\S]*?</section>', inner2, flags=re.I)
        anchor2 = m_open_end2 + (fs2.end() if fs2 else 0)
    else:
        nav_end2 = re.search(r'</nav>', new_html, flags=re.I)
        foot_start2 = re.search(r'<footer', new_html, flags=re.I)
        start2 = nav_end2.end() if nav_end2 else 0
        end2 = foot_start2.start() if foot_start2 else len(new_html)
        inner2 = new_html[start2:end2]
        fs2 = re.search(r'<section[\s\S]*?</section>', inner2, flags=re.I)
        anchor2 = (start2 + fs2.end()) if fs2 else start2
    insertion = '\n'.join(extracted) + '\n'
    new_html = new_html[:anchor2] + insertion + new_html[anchor2:]
    return new_html

def process_file(path: str) -> bool:
    html = open(path, 'r', encoding='utf-8', errors='ignore').read()
    new = reposition(html)
    if new != html:
        with open(path, 'w', encoding='utf-8') as w:
            w.write(new)
        return True
    return False

def main():
    updated = []
    for name in os.listdir(ROOT):
        if not name.endswith('.html'):
            continue
        if process_file(os.path.join(ROOT, name)):
            updated.append(name)
    print('Repositioned product sections in', len(updated), 'files')
    for n in updated:
        print('-', n)

if __name__ == '__main__':
    main()
