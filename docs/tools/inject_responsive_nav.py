import os
import re

ROOT = os.path.join(os.path.dirname(__file__), '..')

DESKTOP_MENU = [
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

def build_desktop_links():
    parts = []
    for href, label, kids in DESKTOP_MENU:
        if kids:
            submenu = '\n'.join([f'<a href="{h}" class="block px-4 py-2 rounded hover:bg-slate-100 dark:hover:bg-slate-800">{l}</a>' for h,l in kids])
            parent_href = 'javascript:void(0)' if href == '#' else href
            parts.append(
                f'''<div class="navx-group relative">
  <a class="navx-toggle hover:text-primary transition-colors" href="{parent_href}" role="button" aria-expanded="false">{label}</a>
  <div class="navx-sub absolute left-0 mt-2 hidden group-hover:block bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl shadow-lg min-w-[220px] p-2 z-50">
    {submenu}
  </div>
</div>'''
            )
        else:
            parts.append(f'<a class="hover:text-primary transition-colors" href="{href}">{label}</a>')
    return '\n'.join(parts)

def build_mobile_list():
    # mobile accordion list
    items = []
    for href, label, kids in DESKTOP_MENU:
        if kids:
            li = [f'<li class="border-b border-slate-200 dark:border-slate-800">']
            li.append(f'<button class="navx-acc w-full flex items-center justify-between py-3 text-left font-semibold">{label}<span class="material-symbols-outlined text-base">expand_more</span></button>')
            li.append('<ul class="navx-acc-body hidden pl-3 pb-3">')
            for h,l in kids:
                li.append(f'<li><a class="block py-2" href="{h}">{l}</a></li>')
            li.append('</ul>')
            li.append('</li>')
            items.append('\n'.join(li))
        else:
            items.append(f'<li class="border-b border-slate-200 dark:border-slate-800"><a class="block py-3 font-semibold" href="{href}">{label}</a></li>')
    return '\n'.join(items)

def nav_assets():
    return '''<script id="color-mode-guard">(function(){try{document.documentElement.classList.remove('dark');}catch(e){}})();</script>
<style id="navx-styles">
.navx-sub{display:none}
.navx-group:hover>.navx-sub,.navx-group:focus-within>.navx-sub,.navx-group.open>.navx-sub{display:block}
.navx-toggle{cursor:pointer}
.navx-overlay{display:none}
.navx-drawer{transform:translateX(100%); transition:transform .2s ease}
.navx-open .navx-overlay{display:block}
.navx-open .navx-drawer{transform:translateX(0)}
</style>
<script id="navx-script">
(function(){
  function closeAll(){ document.querySelectorAll('.navx-group.open').forEach(el=>el.classList.remove('open')); document.querySelectorAll('.navx-toggle[aria-expanded="true"]').forEach(a=>a.setAttribute('aria-expanded','false')); }
  document.addEventListener('click', function(e){
    var t = e.target;
    var toggle = t.closest('a.navx-toggle');
    if (toggle){ e.preventDefault(); e.stopPropagation(); var parent = toggle.closest('.navx-group'); var isOpen = parent.classList.contains('open'); closeAll(); if(!isOpen){ parent.classList.add('open'); toggle.setAttribute('aria-expanded','true'); } return; }
    if (!t.closest('.navx-sub')){ closeAll(); }
  }, true);
  // mobile drawer
  document.addEventListener('click', function(e){
    var btn = e.target.closest('#navx-burger');
    var closeBtn = e.target.closest('#navx-close');
    if (btn){ e.preventDefault(); document.documentElement.classList.add('navx-open'); }
    if (closeBtn || e.target.classList.contains('navx-overlay')){ document.documentElement.classList.remove('navx-open'); }
    // accordion
    var acc = e.target.closest('.navx-acc');
    if (acc){ e.preventDefault(); var body = acc.nextElementSibling; if(body){ body.classList.toggle('hidden'); }}
  });
})();
</script>'''

def build_nav_html():
    desktop = build_desktop_links()
    mobile = build_mobile_list()
    return f'''
<nav class="fixed top-0 w-full z-50 bg-white dark:bg-slate-900 md:bg-white/80 md:dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800">
  <div class="max-w-7xl mx-auto px-4 md:px-6 h-16 md:h-20 flex items-center justify-between">
    <div class="flex items-center gap-3">
      <a href="index.html" class="inline-flex items-center gap-2" aria-label="Proppy home">
        <img src="proppy%20mobile%20icon.png" alt="Proppy" class="h-7 w-7 md:hidden"/>
        <img src="proppy-logo.png" alt="Proppy" class="hidden md:block h-8 md:h-9 w-auto"/>
        <span class="sr-only">Proppy</span>
      </a>
    </div>
    <div class="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600 dark:text-slate-400">
      {desktop}
    </div>
    <div class="flex items-center gap-3">
      <a href="book.html" class="hidden md:inline-flex px-5 py-2.5 text-sm font-semibold text-white bg-slate-900 dark:bg-white dark:text-slate-900 rounded-full hover:shadow-lg transition-all">Get Started</a>
      <button id="navx-burger" class="md:hidden inline-flex items-center justify-center w-10 h-10 rounded-lg border border-slate-300 dark:border-slate-700">
        <span class="material-symbols-outlined">menu</span>
      </button>
    </div>
  </div>
  <div class="fixed inset-0 navx-overlay bg-black/40"></div>
  <div class="fixed right-0 top-0 h-full w-80 max-w-[85vw] navx-drawer bg-white dark:bg-slate-900 border-l border-slate-200 dark:border-slate-800 p-4">
    <div class="flex items-center justify-between mb-2">
      <a href="index.html" class="inline-flex items-center gap-2" aria-label="Proppy home">
        <img src="proppy%20mobile%20icon.png" alt="Proppy" class="h-6 w-6"/>
      </a>
      <button id="navx-close" class="w-10 h-10 rounded-lg border border-slate-300 dark:border-slate-700 inline-flex items-center justify-center">
        <span class="material-symbols-outlined">close</span>
      </button>
    </div>
    <ul class="text-slate-700 dark:text-slate-300">{mobile}</ul>
    <a href="book.html" class="mt-4 inline-flex w-full items-center justify-center px-5 py-3 rounded-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 font-semibold">Get Started</a>
  </div>
</nav>
'''

def inject_assets(html: str) -> str:
    if 'id="navx-styles"' not in html:
        html = re.sub(r'</head>', nav_assets() + '\n</head>', html, flags=re.I)
    return html

def replace_nav(html: str, nav_html: str) -> str:
    m = re.search(r'<nav[\s\S]*?</nav>', html, flags=re.I)
    if not m:
        return html
    return html[:m.start()] + nav_html + html[m.end():]

def main():
    nav_html = build_nav_html()
    updated = []
    for name in os.listdir(ROOT):
        if not name.endswith('.html'):
            continue
        path = os.path.join(ROOT, name)
        txt = open(path, 'r', encoding='utf-8', errors='ignore').read()
        new = replace_nav(inject_assets(txt), nav_html)
        if new != txt:
            with open(path, 'w', encoding='utf-8') as w:
                w.write(new)
            updated.append(name)
    print('Injected responsive nav into', len(updated), 'pages')
    for f in updated:
        print('-', f)

if __name__ == '__main__':
    main()
