#!/usr/bin/env python3
import os, json, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FAQS = os.path.join(ROOT, 'data', 'faqs.json')

def faq_html(items):
    parts = [
        '<section class="mt-10 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 md:p-8">',
        '  <h2 class="text-2xl font-extrabold mb-4">Frequently Asked Questions</h2>',
        '  <div class="divide-y divide-slate-200 dark:divide-slate-800">'
    ]
    for qa in items:
        q = qa['q']; a = qa['a']
        parts.append('    <div class="py-4">')
        parts.append(f'      <h3 class="font-semibold mb-2">{q}</h3>')
        parts.append(f'      <p class="text-slate-600 dark:text-slate-300">{a}</p>')
        parts.append('    </div>')
    parts.append('  </div>')
    parts.append('</section>')
    return '\n'.join(parts)

def faq_ldjson(url, items):
    ent = [{
        "@type": "Question",
        "name": qa['q'],
        "acceptedAnswer": {"@type": "Answer", "text": qa['a']}
    } for qa in items]
    ld = {
        "@context":"https://schema.org",
        "@type":"FAQPage",
        "mainEntity": ent
    }
    import json as _json
    return '<script type="application/ld+json" data-auto="1">' + _json.dumps(ld, ensure_ascii=False) + '</script>'

def inject_for(page, items):
    p = os.path.join(ROOT, page)
    if not os.path.exists(p):
        return False
    with open(p,'r',encoding='utf-8',errors='ignore') as f:
        html = f.read()
    # Only inject once per page
    if 'Frequently Asked Questions' in html:
        return False
    block = faq_html(items)
    # Insert before closing main if present, else before </footer> or </body>
    for pat in [r'</main>', r'</footer>', r'</body>']:
        new_html, n = re.subn(pat, block + '\n' + pat, html, count=1, flags=re.I)
        if n:
            html = new_html
            break
    # Add JSON-LD
    url = '/' + page
    html = re.sub(r'</body>', faq_ldjson(url, items) + '\n</body>', html, count=1, flags=re.I)
    with open(p,'w',encoding='utf-8') as w:
        w.write(html)
    return True

def main():
    with open(FAQS,'r',encoding='utf-8') as f:
        data = json.load(f)
    changed = 0
    for page in ('how-it-works.html', 'pricing.html'):
        items = data.get(page)
        if items and inject_for(page, items):
            changed += 1
    print(f'Injected FAQs into {changed} pages')

if __name__ == '__main__':
    main()

