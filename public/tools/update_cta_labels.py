#!/usr/bin/env python3
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def update_labels(html: str) -> str:
    new = html
    # 1) Replace exact anchor text 'Get Started' with 'Start Free Assessment'
    new = re.sub(r'(>\s*)Get Started(\s*<)', r'\1Start Free Assessment\2', new)
    # 2) Replace nav dropdown anchor text 'Book' (single word) with 'Book a Call'
    new = re.sub(r'(<a[^>]*>\s*)Book(\s*</a>)', r'\1Book a Call\2', new)
    # 3) Simplify 'Book a Free Strategy Call' to 'Book a Call'
    new = re.sub(r'(>\s*)Book a Free Strategy Call(\s*<)', r'\1Book a Call\2', new)
    return new

def main():
    changed = 0
    for root, _, files in os.walk(ROOT):
        for fn in files:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(root, fn)
            with open(path,'r',encoding='utf-8',errors='ignore') as f:
                html = f.read()
            new_html = update_labels(html)
            if new_html != html:
                with open(path,'w',encoding='utf-8') as w:
                    w.write(new_html)
                changed += 1
    print('Updated CTA labels in', changed, 'files')

if __name__ == '__main__':
    main()

