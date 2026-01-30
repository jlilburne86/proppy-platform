import os
import re

ROOT = os.path.join(os.path.dirname(__file__), '..')

TARGETS = [
    (r'how\s+it\s+works', 'how-it-works.html'),
    (r'pricing|plans|see\s+pricing|view\s+pricing', 'transparent-pricing-clear-value-no-surprises.html'),
    (r'technology|platform|built\s+for\s+signal', 'built-for-signal-not-noise.html'),
    (r'resources|guides|market\s+updates', 'investor-resources-hub.html'),
    (r'results|case\s*stud', 'what-results-means.html'),
    (r'nationwide|sourcing', 'nationwide-sourcing.html'),
    (r'advantage|why\s+choose', 'the-unfair-advantage-for-modern-investors.html'),
    (r'guarantee|money[-\s]*back', 'we-back-our-service-if-we-dont-deliver-youre-covered.html'),
    (r'book|get\s+started|speak\s+with', 'book.html'),
]

def link_ctas_in_html(txt: str) -> str:
    # Replace anchors with href="#" or empty that have recognizable labels
    def repl(m):
        before, inner, after = m.group(1), m.group(2), m.group(3)
        label = re.sub(r'<[^>]+>', ' ', inner)
        label = re.sub(r'\s+', ' ', label).strip().lower()
        for pattern, href in TARGETS:
            if re.search(pattern, label):
                return f'<a{before} href="{href}">{inner}</a>'
        return m.group(0)

    # case 1: <a ... href="#"> ... </a>
    txt = re.sub(r'<a([^>]*?)\s+href=(["\"])#\2([^>]*)>([\s\S]*?)</a>', lambda m: repl((lambda: None) or type('x', (), {'group': lambda self,i: ['', m.group(1)+f' href={m.group(2)}#'+m.group(2)+m.group(3), m.group(4), '']})()), txt)
    # simpler robust approach: search manually and replace common patterns
    txt = re.sub(r'<a([^>]*?)\s+href=(["\"])#\2(.*?)>([\s\S]*?)</a>', lambda m: repl(type('M', (), {'group': lambda self,i: (('', m.group(1), m.group(4), '')[i])})()), txt)
    # generic: any <a ...>label</a> with no href
    txt = re.sub(r'<a(?![^>]*href=)([^>]*)>([\s\S]*?)</a>', lambda m: repl(type('M', (), {'group': lambda self,i: (('', m.group(1), m.group(2), '')[i])})()), txt)
    # Also update button-like links
    for pattern, href in TARGETS:
        txt = re.sub(rf'<a([^>]*?)>([^<]*?{pattern}[^<]*?)</a>', rf'<a\1 href="{href}">\2</a>', txt, flags=re.I)
    return txt

def main():
    updated = []
    for name in os.listdir(ROOT):
        if not name.endswith('.html'):
            continue
        path = os.path.join(ROOT, name)
        original = open(path, 'r', encoding='utf-8', errors='ignore').read()
        new = link_ctas_in_html(original)
        if new != original:
            with open(path, 'w', encoding='utf-8') as w:
                w.write(new)
            updated.append(name)
    print('Linked CTAs in', len(updated), 'files')
    for f in updated:
        print('-', f)

if __name__ == '__main__':
    main()

