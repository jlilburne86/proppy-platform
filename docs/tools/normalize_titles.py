#!/usr/bin/env python3
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def main():
    changed = 0
    for name in os.listdir(ROOT):
        if not name.endswith('.html'):
            continue
        p = os.path.join(ROOT, name)
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
        # Swap "Proppy - Title" -> "Title - Proppy"
        new_html = re.sub(r'<title>\s*Proppy\s*-\s*(.*?)</title>', r'<title>\1 - Proppy</title>', html, flags=re.I)
        if new_html != html:
            with open(p, 'w', encoding='utf-8') as w:
                w.write(new_html)
            changed += 1
    print(f'Normalized titles in {changed} pages')


if __name__ == '__main__':
    main()

