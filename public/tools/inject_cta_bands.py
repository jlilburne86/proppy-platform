import os
import re

ROOT = os.path.join(os.path.dirname(__file__), '..')

CTA_TOP = '''\n<section class="max-w-7xl mx-auto px-6 py-10">
  <div class="rounded-[2rem] border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 md:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
    <div>
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-[11px] font-bold uppercase tracking-wider mb-2">Get Started</div>
      <h3 class="text-2xl md:text-3xl font-extrabold">Book a free strategy call</h3>
      <p class="text-slate-600 dark:text-slate-400 mt-1">See how Proppy helps you buy the right property, in the right market, at the right price.</p>
    </div>
    <div class="flex items-center gap-3">
      <a href="book.html" class="px-5 py-3 rounded-full bg-primary text-white font-semibold hover:shadow-lg hover:shadow-primary/30">Book now</a>
      <a href="pricing.html" class="px-5 py-3 rounded-full border border-slate-200 dark:border-slate-700 font-semibold">View pricing</a>
    </div>
  </div>
</section>\n'''

CTA_BOTTOM = '''\n<section class="max-w-7xl mx-auto px-6 py-14">
  <div class="rounded-[2rem] border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-8 md:p-10 text-center">
    <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-[11px] font-bold uppercase tracking-wider mb-3">Ready?</div>
    <h3 class="text-2xl md:text-3xl font-extrabold mb-2">Let’s map your next purchase</h3>
    <p class="text-slate-600 dark:text-slate-400 mb-6">A 20‑minute call to clarify goals, markets, and the plan to act.</p>
    <div class="flex items-center gap-3 justify-center">
      <a href="book.html" class="px-5 py-3 rounded-full bg-primary text-white font-semibold hover:shadow-lg hover:shadow-primary/30">Book a call</a>
      <a href="how-it-works.html" class="px-5 py-3 rounded-full border border-slate-200 dark:border-slate-700 font-semibold">How it works</a>
    </div>
  </div>
</section>\n'''

EXCLUDE = {'book.html', 'contact.html', 'site-map.html'}

def inject(file_path: str) -> bool:
    html = open(file_path, 'r', encoding='utf-8', errors='ignore').read()
    orig = html
    # Skip if already contains our CTA markers (by heading text)
    if 'Book a free strategy call' in html and 'Let’s map your next purchase' in html:
        return False
    # Insert top CTA after first <section> inside <main>
    main_open = re.search(r'<main[^>]*>', html, flags=re.I)
    main_close = re.search(r'</main>', html, flags=re.I)
    if not main_open or not main_close:
        return False
    inner = html[main_open.end():main_close.start()]
    first_section = re.search(r'<section[\s\S]*?</section>', inner, flags=re.I)
    if first_section:
        insert_top = main_open.end() + first_section.end()
        html = html[:insert_top] + CTA_TOP + html[insert_top:]
        # Recompute positions after insertion
        main_close = re.search(r'</main>', html, flags=re.I)
    # Insert bottom CTA before </main>
    html = html[:main_close.start()] + CTA_BOTTOM + html[main_close.start():]
    if html != orig:
        with open(file_path, 'w', encoding='utf-8') as w:
            w.write(html)
        return True
    return False

def main():
    updated = []
    for name in os.listdir(ROOT):
        if not name.endswith('.html') or name in EXCLUDE:
            continue
        path = os.path.join(ROOT, name)
        if inject(path):
            updated.append(name)
    print('Injected CTA bands into', len(updated), 'pages')
    for n in updated:
        print('-', n)

if __name__ == '__main__':
    main()

