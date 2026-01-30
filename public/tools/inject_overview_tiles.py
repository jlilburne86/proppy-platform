import os
import re

ROOT = os.path.join(os.path.dirname(__file__), '..')

TILES = {
    'advantage.html': [
        ('Data‑led', '50+ signals per suburb to remove bias'),
        ('Proactive', 'Define what to buy, then we go get it'),
        ('Off‑market', 'Deep agent networks for early access'),
        ('Transparent', 'No commissions; clear pricing and guarantee'),
    ],
    'sourcing.html': [
        ('Nationwide', 'We buy where the value is, not just local'),
        ('Target Assets', 'Houses/townhouses/apartments with scarcity'),
        ('Off‑market', 'Pre‑market and private channels'),
        ('Due diligence', 'Disciplined checks before any offer'),
    ],
    'about.html': [
        ('Purpose', 'Make institutional‑grade investing accessible'),
        ('Philosophy', 'Evidence over opinion; tech + experts'),
        ('Approach', 'End‑to‑end support from strategy to settlement'),
        ('Guarantee', 'Start with confidence; risk‑free strategy phase'),
    ],
    'team.html': [
        ('Experience', '15+ years through multiple cycles'),
        ('Data + Experts', 'Engineers and property specialists together'),
        ('Negotiation', 'Experienced buyers on your side'),
        ('Care', 'Clear communication and guidance throughout'),
    ],
}

def build_overview(tiles):
    items = '\n'.join([f'<div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5"><h3 class="font-bold mb-1">{h}</h3><p class="text-sm text-slate-600 dark:text-slate-400">{p}</p></div>' for h,p in tiles])
    return f'''\n<section class="max-w-7xl mx-auto px-6 py-10">
  <div class="text-center mb-6">
    <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-[11px] font-bold uppercase tracking-wider">Quick Overview</span>
  </div>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">{items}</div>
</section>\n'''

def build_product():
    return '''\n<section class="max-w-7xl mx-auto px-6 py-10">
  <div class="rounded-2xl border border-slate-200 dark:border-slate-800 overflow-hidden bg-white dark:bg-slate-900">
    <img src="assets/screenshots/product-main.png" alt="Product preview" class="w-full h-auto"/>
  </div>
</section>\n'''

def inject(path: str, tiles) -> bool:
    html = open(path, 'r', encoding='utf-8', errors='ignore').read()
    orig = html
    main_open = re.search(r'<main[^>]*>', html, flags=re.I)
    main_close = re.search(r'</main>', html, flags=re.I)
    if not main_open or not main_close:
        return False
    inner = html[main_open.end():main_close.start()]
    first_section = re.search(r'<section[\s\S]*?</section>', inner, flags=re.I)
    insert_at = main_open.end() + (first_section.end() if first_section else 0)
    overview = build_overview(tiles)
    product = build_product()
    html = html[:insert_at] + overview + product + html[insert_at:]
    if html != orig:
        open(path, 'w', encoding='utf-8').write(html)
        return True
    return False

def main():
    updated = []
    for name, tiles in TILES.items():
        p = os.path.join(ROOT, name)
        if os.path.isfile(p):
            if inject(p, tiles):
                updated.append(name)
    print('Injected overview + product into:', ', '.join(updated) or 'none')

if __name__ == '__main__':
    main()
