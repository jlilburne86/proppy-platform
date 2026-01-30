#!/usr/bin/env python3
import os
import re
import time
import html
import json
from urllib.parse import urljoin

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SITE_CFG = os.path.join(ROOT, 'data', 'site.json')
OUTPUT = os.path.join(ROOT, 'sitemap.xml')


def load_site_url():
    site_url = 'https://proppy.com.au/'
    try:
        with open(SITE_CFG, 'r', encoding='utf-8') as f:
            data = json.load(f)
            site_url = (data.get('site_url') or site_url).rstrip('/') + '/'
    except Exception:
        pass
    return site_url


def find_images(html_text: str):
    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html_text, flags=re.I)
    # Keep only typical image extensions; skip tracking pixels
    exts = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg')
    out = []
    for u in imgs:
        low = u.lower()
        if 'facebook.com/tr' in low:
            continue
        if any(low.endswith(ext) for ext in exts):
            out.append(u)
    return out


def main():
    site_url = load_site_url()
    urlset = []
    for name in os.listdir(ROOT):
        if not name.endswith('.html'):
            continue
        if name.startswith('admin'):
            continue
        # skip demo/variant pages from sitemap
        if name.startswith('home-'):
            continue
        path = os.path.join(ROOT, name)
        try:
            st = os.stat(path)
            lastmod = time.strftime('%Y-%m-%d', time.gmtime(st.st_mtime))
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                txt = f.read()
        except Exception:
            continue
        loc = site_url if name == 'index.html' else urljoin(site_url, name)
        images = []
        for src in find_images(txt):
            if src.startswith('http://') or src.startswith('https://'):
                images.append(src)
            elif src.startswith('/'):
                images.append(urljoin(site_url, src.lstrip('/')))
            else:
                images.append(urljoin(loc, src))
        urlset.append((loc, lastmod, images))

    # Build XML
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">'
    ]
    for loc, lastmod, images in urlset:
        lines.append('  <url>')
        lines.append(f'    <loc>{html.escape(loc)}</loc>')
        lines.append(f'    <lastmod>{lastmod}</lastmod>')
        for img in images[:20]:
            lines.append('    <image:image>')
            lines.append(f'      <image:loc>{html.escape(img)}</image:loc>')
            lines.append('    </image:image>')
        lines.append('  </url>')
    lines.append('</urlset>')

    with open(OUTPUT, 'w', encoding='utf-8') as w:
        w.write('\n'.join(lines) + '\n')
    print(f'Wrote {OUTPUT} with {len(urlset)} URLs')


if __name__ == '__main__':
    main()
