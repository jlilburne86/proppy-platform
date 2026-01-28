#!/usr/bin/env python3
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TARGET_PAGES = ['index.html', 'results.html']

def find_image_paths(html):
    # Return list of (src, absolute_path)
    paths = []
    for m in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.I):
        src = m.group(1)
        if src.startswith('http://') or src.startswith('https://'):
            continue
        # skip data URLs
        if src.startswith('data:'):
            continue
        # resolve to filesystem
        abspath = os.path.join(ROOT, src.lstrip('/')) if src.startswith('/') else os.path.join(ROOT, src)
        if os.path.exists(abspath):
            paths.append((src, abspath))
    return paths

def to_webp_path(path):
    base, _ = os.path.splitext(path)
    return base + '.webp'

def convert_to_webp(src_path, dst_path):
    try:
        from PIL import Image  # type: ignore
    except Exception:
        print('Pillow not available; skipping conversion for', src_path)
        return False
    try:
        with Image.open(src_path) as im:
            im.save(dst_path, 'WEBP', quality=82, method=6)
        return True
    except Exception as e:
        print('Failed to convert', src_path, '->', dst_path, e)
        return False

def replace_src_with_webp(html, src):
    # Replace only exact src occurrences in img tags
    return re.sub(r'(\<img[^>]+src=["\'])' + re.escape(src) + r'(["\'])', r'\1' + re.escape(to_webp_url(src)) + r'\2', html, flags=re.I)

def to_webp_url(url):
    base, _ = os.path.splitext(url)
    return base + '.webp'

def main():
    total_converted = 0
    total_linked = 0
    for page in TARGET_PAGES:
        p = os.path.join(ROOT, page)
        if not os.path.exists(p):
            continue
        with open(p,'r',encoding='utf-8',errors='ignore') as f:
            html = f.read()
        images = find_image_paths(html)
        changed = False
        for src, abspath in images:
            # Only target jpg/jpeg/png
            if not os.path.splitext(abspath)[1].lower() in ('.jpg', '.jpeg', '.png'):
                continue
            webp_path = to_webp_path(abspath)
            if not os.path.exists(webp_path):
                if convert_to_webp(abspath, webp_path):
                    total_converted += 1
            if os.path.exists(webp_path):
                new_html = replace_src_with_webp(html, src)
                if new_html != html:
                    html = new_html
                    changed = True
                    total_linked += 1
        if changed:
            with open(p,'w',encoding='utf-8') as w:
                w.write(html)
    print(f'WebP converted: {total_converted}, linked in HTML: {total_linked}')

if __name__ == '__main__':
    main()

