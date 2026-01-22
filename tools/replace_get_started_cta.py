import os, re

ROOT = os.path.join(os.path.dirname(__file__), '..')

def read(path):
    return open(path,'r',encoding='utf-8',errors='ignore').read()

def write(path, txt):
    with open(path,'w',encoding='utf-8') as w:
        w.write(txt)

def replace_cta(html: str) -> str:
    # Replace only anchors to book.html that have inner text exactly 'Get Started'
    pattern = re.compile(r'(\<a[^>]*href=["\']book\.html["\'][^>]*\>)\s*Get Started\s*(\</a\>)', re.I)
    return pattern.sub(r'\1Book a Free Strategy Call\2', html)

def main():
    updated = []
    for root, _, files in os.walk(ROOT):
        for fn in files:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(root, fn)
            txt = read(path)
            new = replace_cta(txt)
            if new != txt:
                write(path, new)
                updated.append(os.path.relpath(path, ROOT))
    print('Updated CTA text in', len(updated), 'files')
    for f in updated:
        print('-', f)

if __name__ == '__main__':
    main()
