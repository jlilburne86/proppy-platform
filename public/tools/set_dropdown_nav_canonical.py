import os
import re

ROOT = os.path.join(os.path.dirname(__file__), '..')

# Canonical menu mapping
MENU = [
    ('index.html', 'Home', []),
    ('how-it-works.html', 'How It Works', [
        ('how-it-works.html', 'How It Works'),
        ('technology.html', 'Technology'),
    ]),
    ('#', 'Solutions', [
        ('advantage.html', 'Advantage'),
        ('sourcing.html', 'Sourcing'),
        ('about.html', 'About'),
        ('team.html', 'Team'),
    ]),
    ('#', 'Success', [
        ('results.html', 'Results'),
        ('guarantee.html', 'Guarantee'),
    ]),
    ('resources.html', 'Resources', []),
    ('#', 'Get Started', [
        ('pricing.html', 'Pricing'),
        ('book.html', 'Book'),
        ('contact.html', 'Contact'),
    ]),
]

def build_nav_html():
    # Build links with simple hover dropdowns
    items = []
    for href, label, children in MENU:
        if children:
            # Prevent jump with javascript:void(0) for non-destination parents
            parent_href = href if href != '#' else 'javascript:void(0)'
            submenu = '\n'.join([f'<a href="{ch_href}" class="block px-4 py-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded">{ch_label}</a>' for ch_href, ch_label in children])
            items.append(
                f'''<div class="group relative">
  <a class="nav-toggle hover:text-primary dark:hover:text-white transition-colors" href="{parent_href}" tabindex="0" aria-haspopup="true" role="button" aria-expanded="false">{label}</a>
  <div class="nav-submenu absolute left-0 mt-2 hidden group-hover:block group-focus-within:block bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl shadow-lg min-w-[220px] p-2 z-50">
    {submenu}
  </div>
</div>'''
            )
        else:
            items.append(f'<a class="hover:text-primary dark:hover:text-white transition-colors" href="{href}">{label}</a>')
    return '\n'.join(items)

def replace_nav(html: str, links_html: str) -> str:
    nav_m = re.search(r'<nav[\s\S]*?</nav>', html, flags=re.I)
    if not nav_m:
        return html
    nav = nav_m.group(0)
    container_m = re.search(r'<div[^>]*class="[^"]*md:flex[^"]*gap-8[^"]*"[^>]*>([\s\S]*?)</div>', nav, flags=re.I)
    if not container_m:
        return html
    old = container_m.group(0)
    new = re.sub(r'>([\s\S]*?)</div>', '>' + links_html + '</div>', old)
    new_nav = nav.replace(old, new, 1)
    return html[:nav_m.start()] + new_nav + html[nav_m.end():]

def main():
    links_html = build_nav_html()
    updated = []
    for name in os.listdir(ROOT):
        if not name.endswith('.html'):
            continue
        path = os.path.join(ROOT, name)
        txt = open(path, 'r', encoding='utf-8', errors='ignore').read()
        new = replace_nav(txt, links_html)
        if new != txt:
            with open(path, 'w', encoding='utf-8') as w:
                w.write(new)
            updated.append(name)
    print('Applied dropdown nav to', len(updated), 'pages')
    for f in updated:
        print('-', f)

if __name__ == '__main__':
    main()
