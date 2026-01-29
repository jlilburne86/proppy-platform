import os, re
ROOT = os.path.join(os.path.dirname(__file__), '..')
files = [f for f in os.listdir(ROOT) if re.match(r'home-\d+\.html$', f)]
meta = '<meta name="robots" content="noindex, nofollow">'

updated = []
for fn in files:
    p = os.path.join(ROOT, fn)
    txt = open(p,'r',encoding='utf-8',errors='ignore').read()
    if 'name="robots"' in txt:
        continue
    # inject after viewport meta if possible, else after <head>
    new = re.sub(r'(</title>\s*)', r'\1\n'+meta+'\n', txt, count=1, flags=re.I)
    if new == txt:
        new = re.sub(r'(<head[^>]*>\s*)', r'\1\n'+meta+'\n', txt, count=1, flags=re.I)
    if new != txt:
        open(p,'w',encoding='utf-8').write(new)
        updated.append(fn)
print('Added noindex to', len(updated), 'files')
for f in updated:
    print('-', f)
