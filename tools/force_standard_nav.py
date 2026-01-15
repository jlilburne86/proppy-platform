import os
import re
from set_dropdown_nav_canonical import build_nav_html

ROOT = os.path.join(os.path.dirname(__file__), '..')

STANDARD_PREFIX = (
    '<nav class="fixed top-0 w-full z-50 bg-background-light/80 dark:bg-background-dark/80 '
    'backdrop-blur-md border-b border-slate-200 dark:border-slate-800">\n'
    '<div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">\n'
    '<div class="flex items-center gap-2">\n'
    '<span class="text-2xl font-extrabold tracking-tighter uppercase italic">Proppy</span>\n'
    '</div>\n'
    '<div class="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600 dark:text-slate-400">'
)

STANDARD_SUFFIX = (
    '</div>\n'
    '<div class="flex items-center gap-4">\n'
    '  <a href="book.html" class="px-5 py-2.5 text-sm font-semibold text-white bg-slate-900 dark:bg-white dark:text-slate-900 rounded-full hover:shadow-lg transition-all">Get Started</a>\n'
    '</div>\n'
    '</div>\n'
    '</nav>'
)

def force_nav(html: str) -> str:
    nav_m = re.search(r'<nav[\s\S]*?</nav>', html, flags=re.I)
    if not nav_m:
        return html
    links_html = build_nav_html()
    new_nav = STANDARD_PREFIX + links_html + STANDARD_SUFFIX
    return html[:nav_m.start()] + new_nav + html[nav_m.end():]

def main():
    updated = []
    for name in os.listdir(ROOT):
        if not name.endswith('.html'):
            continue
        path = os.path.join(ROOT, name)
        txt = open(path, 'r', encoding='utf-8', errors='ignore').read()
        new = force_nav(txt)
        if new != txt:
            with open(path, 'w', encoding='utf-8') as w:
                w.write(new)
            updated.append(name)
    print('Forced standard nav in', len(updated), 'pages')
    for f in updated:
        print('-', f)

if __name__ == '__main__':
    main()

