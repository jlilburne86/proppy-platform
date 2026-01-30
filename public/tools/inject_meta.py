#!/usr/bin/env python3
import os, re
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
meta = '''<meta property="og:type" content="website">
<meta property="og:site_name" content="Proppy">
<meta property="og:title" content="Proppy">
<meta property="og:description" content="Smarter property investment with data-led insights and expert execution.">
<meta property="og:image" content="assets/placeholders/tablet.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Proppy">
<meta name="twitter:description" content="Smarter property investment with data-led insights and expert execution.">
<meta name="twitter:image" content="assets/placeholders/tablet.svg">'''

for name in os.listdir(root):
    if not name.endswith('.html'): continue
    p = os.path.join(root, name)
    with open(p,'r',encoding='utf-8',errors='ignore') as f:
        html = f.read()
    if re.search(r'og:(title|type|image)', html):
        continue
    html = re.sub(r'</head>', meta + '\n</head>', html, count=1, flags=re.IGNORECASE)
    with open(p,'w',encoding='utf-8') as f:
        f.write(html)
print('Injected meta where missing')
