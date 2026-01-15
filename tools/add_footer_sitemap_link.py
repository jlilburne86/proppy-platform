import os
import re

ROOT = os.path.join(os.path.dirname(__file__), '..')

def add_link(html: str) -> str:
    # Append a Site Map link next to Privacy/Terms if footer is present
    # Try a few common footers
    if 'site-map.html' not in html:
        html = re.sub(r'(Privacy Policy</a>\s*</div>)', r'\1', html)
        # Add into common footer group of links
        html = re.sub(r'(Terms of Service</a>\s*</div>)', r'Terms of Service</a> <a class="hover:text-primary transition-colors" href="site-map.html">Site Map</a></div>', html)
        # Another variant with list items
        html = re.sub(r'(</ul>\s*</div>\s*</div>\s*</footer>)', r'<li><a class="hover:text-primary" href="site-map.html">Site Map</a></li>\1', html)
    return html

def main():
    updated = []
    for name in os.listdir(ROOT):
        if not name.endswith('.html'):
            continue
        path = os.path.join(ROOT, name)
        txt = open(path, 'r', encoding='utf-8', errors='ignore').read()
        new = add_link(txt)
        if new != txt:
            with open(path, 'w', encoding='utf-8') as w:
                w.write(new)
            updated.append(name)
    print('Added Site Map link in', len(updated), 'pages')
    for f in updated:
        print('-', f)

if __name__ == '__main__':
    main()

