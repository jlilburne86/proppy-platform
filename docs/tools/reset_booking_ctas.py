#!/usr/bin/env python3
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

BOOK = 'book.html'

def rewrite_links(html: str) -> str:
    new = html
    # Replace engage booking links to book.html
    new = re.sub(r'href\s*=\s*"https?://engage\.proppy\.com\.au/widget/booking/[^"]+"', f'href="{BOOK}"', new, flags=re.I)
    new = re.sub(r'href\s*=\s*"https?://(?:www\.)?calendly\.com/[^"]+"', f'href="{BOOK}"', new, flags=re.I)
    # Also fix any HL widget link without protocol varations
    new = re.sub(r'href\s*=\s*"https?://[^\"]*leadconnector[^\"]+"', f'href="{BOOK}"', new, flags=re.I)
    # Ensure nav dropdown item labelled Book points to book.html
    new = re.sub(r'(>Book<\s*</a>)', r'\1', new)  # no-op anchor for matching stability
    return new

def main():
    changed = 0
    for root, _, files in os.walk(ROOT):
        for fn in files:
            if not fn.endswith('.html'):
                continue
            p = os.path.join(root, fn)
            with open(p,'r',encoding='utf-8',errors='ignore') as f:
                html = f.read()
            new_html = rewrite_links(html)
            if new_html != html:
                with open(p,'w',encoding='utf-8') as w:
                    w.write(new_html)
                changed += 1
    print('Reset booking CTAs to book.html in', changed, 'files')

if __name__ == '__main__':
    main()

