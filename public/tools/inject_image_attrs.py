#!/usr/bin/env python3
import os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

IMG_TAG = re.compile(r'<img\b([^>]*)>', re.I)

def should_lazy(attrs: str) -> bool:
    if 'loading=' in attrs.lower():
        return False
    # Avoid logos/mobile icon as they are in nav/header
    if 'proppy-logo' in attrs or 'proppy%20mobile%20icon' in attrs or 'proppy-mobile-icon' in attrs:
        return False
    return True

def add_attrs(h: str) -> str:
    def repl(m):
        attrs = m.group(1)
        new_attrs = attrs
        if should_lazy(attrs):
            new_attrs += ' loading="lazy"'
        if 'decoding=' not in attrs.lower():
            new_attrs += ' decoding="async"'
        return '<img' + new_attrs + '>'
    return IMG_TAG.sub(repl, h)

def add_preload_for_first_image(html: str) -> str:
    # Find first image src
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.I)
    if not m:
        return html
    src = m.group(1)
    # Skip if preload exists
    if src in html and re.search(r'<link[^>]+rel=["\']preload["\'][^>]+as=["\']image["\']', html, re.I):
        return html
    link = f'<link rel="preload" as="image" href="{src}">\n'
    return re.sub(r'</head>', link + '</head>', html, count=1, flags=re.I)

def main():
    changed = 0
    for name in os.listdir(ROOT):
        if not name.endswith('.html'):
            continue
        p = os.path.join(ROOT, name)
        with open(p,'r',encoding='utf-8',errors='ignore') as f:
            html = f.read()
        new_html = add_attrs(html)
        if name == 'index.html':
            new_html = add_preload_for_first_image(new_html)
        if new_html != html:
            with open(p,'w',encoding='utf-8') as w:
                w.write(new_html)
            changed += 1
    print(f'Updated images in {changed} pages')

if __name__ == '__main__':
    main()

