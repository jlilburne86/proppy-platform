#!/usr/bin/env python3
import os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

BTN_RE = re.compile(r'(\<a[^>]+class=\"[^\"]*hidden md:inline-flex[^\"]*\"[^>]*\>)([\s\S]*?)(\<\/a\>)', re.I)

def repl(match):
    start, inner, end = match.groups()
    # Force href to book.html
    start = re.sub(r'href=\"[^\"]*\"', 'href="book.html"', start, flags=re.I)
    # Replace button label with Book a Call (keep icon if exists)
    # Try to preserve trailing icon span if present
    # Extract any trailing icon span from inner
    m = re.search(r'(\<span[^>]*class=\"[^\"]*material-symbols-outlined[^\"]*\"[^>]*\>[\s\S]*?\<\/span\>)\s*$', inner)
    icon = m.group(1) if m else ''
    new_inner = 'Book a Call' + (icon and ('' + icon))
    return start + new_inner + end

def main():
    changed = 0
    for root, _, files in os.walk(ROOT):
        for fn in files:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(root, fn)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                html = f.read()
            new_html, n = BTN_RE.subn(repl, html, count=1)
            if n:
                with open(path, 'w', encoding='utf-8') as w:
                    w.write(new_html)
                changed += 1
    print('Updated top-nav CTA in', changed, 'files')

if __name__ == '__main__':
    main()

