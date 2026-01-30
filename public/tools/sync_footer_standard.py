import os
import re

ROOT = os.path.join(os.path.dirname(__file__), '..')

FOOTER = '''<footer class="py-12 border-t border-slate-200 dark:border-slate-800 mt-12">
  <div class="max-w-7xl mx-auto px-6">
    <div class="flex flex-col md:flex-row justify-between items-center gap-8">
      <div class="flex items-center gap-3">
        <span class="text-xl font-extrabold uppercase tracking-tight">Proppy</span>
        <span class="text-slate-400 text-sm">© 2024 Proppy Inc. All rights reserved.</span>
      </div>
      <div class="flex gap-8 text-sm font-semibold text-slate-500 dark:text-slate-400">
        <a class="hover:text-primary transition-colors" href="privacy.html">Privacy Policy</a>
        <a class="hover:text-primary transition-colors" href="terms.html">Terms of Service</a>
        <a class="hover:text-primary transition-colors" href="site-map.html">Site Map</a>
      </div>
    </div>
  </div>
</footer>'''

def replace_footer(html: str) -> str:
    m = re.search(r'<footer[\s\S]*?</footer>', html, flags=re.I)
    if not m:
        # if no footer, append before closing body
        return re.sub(r'</body>\s*</html>\s*$', FOOTER + '\n</body></html>', html, flags=re.I)
    start, end = m.start(), m.end()
    return html[:start] + FOOTER + html[end:]

def main():
    updated = []
    for name in os.listdir(ROOT):
        if not name.endswith('.html'):
            continue
        path = os.path.join(ROOT, name)
        txt = open(path, 'r', encoding='utf-8', errors='ignore').read()
        new = replace_footer(txt)
        if new != txt:
            with open(path, 'w', encoding='utf-8') as w:
                w.write(new)
            updated.append(name)
    print('Standardized footer in', len(updated), 'pages')
    for f in updated:
        print('-', f)

if __name__ == '__main__':
    main()

