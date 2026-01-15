import os
import re

ROOT = os.path.join(os.path.dirname(__file__), '..')

SECTION_START = '<!-- ALL_PAGES_SECTION_START -->'
SECTION_END = '<!-- ALL_PAGES_SECTION_END -->'

def build_links() -> str:
    files = [f for f in os.listdir(ROOT) if f.endswith('.html')]
    # Exclude index from list; include site-map
    files = [f for f in files if f != 'index.html']
    files.sort()
    items = []
    for f in files:
        items.append(f'<li><a class="text-primary hover:underline" href="{f}">{f}</a></li>')
    return '\n'.join(items)

def inject_section(index_html: str, list_html: str) -> str:
    section = f'''\n{SECTION_START}\n<section class="max-w-7xl mx-auto px-6 py-12">
  <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-8">
    <h2 class="text-2xl font-bold mb-4">All Pages</h2>
    <p class="text-slate-600 dark:text-slate-400 mb-4">Browse every page on this site.</p>
    <ul class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2 list-disc pl-5">{list_html}</ul>
  </div>
</section>
{SECTION_END}\n'''
    # If already present, replace between markers
    if SECTION_START in index_html and SECTION_END in index_html:
        return re.sub(f'{SECTION_START}[\s\S]*?{SECTION_END}', section, index_html)
    # Insert before footer if possible
    m = re.search(r'<footer[\s\S]*?</footer>', index_html, flags=re.I)
    if m:
        return index_html[:m.start()] + section + index_html[m.start():]
    # Else append to end
    return index_html + section

def main():
    idx_path = os.path.join(ROOT, 'index.html')
    html = open(idx_path, 'r', encoding='utf-8', errors='ignore').read()
    links = build_links()
    new_html = inject_section(html, links)
    if new_html != html:
        with open(idx_path, 'w', encoding='utf-8') as w:
            w.write(new_html)
        print('Injected All Pages section into index.html')
    else:
        print('All Pages section unchanged')

if __name__ == '__main__':
    main()

