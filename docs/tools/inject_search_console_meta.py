#!/usr/bin/env python3
import os, re, json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TRACKING_CFG = os.path.join(ROOT, 'data', 'tracking.json')

def main():
    try:
        with open(TRACKING_CFG, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
            token = (cfg.get('search_console_verification') or '').strip()
    except Exception:
        token = ''
    if not token:
        print('No Search Console token set; skipping.')
        return
    meta = f'<meta name="google-site-verification" content="{token}">\n'
    changed = 0
    for name in os.listdir(ROOT):
        if not name.endswith('.html'):
            continue
        p = os.path.join(ROOT, name)
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
        if f'content="{token}"' in html:
            continue
        new_html, n = re.subn(r'</head>', meta + '</head>', html, count=1, flags=re.I)
        if n:
            with open(p, 'w', encoding='utf-8') as w:
                w.write(new_html)
            changed += 1
    print(f'Injected Search Console meta into {changed} pages')

if __name__ == '__main__':
    main()

