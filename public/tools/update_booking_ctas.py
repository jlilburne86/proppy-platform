#!/usr/bin/env python3
import os
import re
import json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CFG = os.path.join(ROOT, 'data', 'highlevel.json')


def load_calendar_url():
    with open(CFG, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    url = (cfg.get('calendar_url') or '').strip()
    if not url:
        raise SystemExit('calendar_url missing in data/highlevel.json')
    return url


def add_source_param(url: str, key='source', val='cta') -> str:
    if '?' in url:
        if f'{key}=' in url:
            return url
        return url + f'&{key}={val}'
    else:
        return url + f'?{key}={val}'


def rewrite_links(html: str, target_url: str) -> str:
    # Replace href to book.html (any quotes) with HL URL
    def repl_book(m):
        pre, _, post = m.groups()
        return f'{pre}{target_url}{post}'

    html = re.sub(r'(href\s*=\s*["\'])\s*book\.html(#[^"\']*)?(["\'])', repl_book, html, flags=re.I)

    # Replace Calendly links
    def repl_cal(m):
        pre, post = m.groups()
        return f'{pre}{target_url}{post}'

    html = re.sub(r'(href\s*=\s*["\'])https?://(?:www\.)?calendly\.com/[^"\']+(["\'])', repl_cal, html, flags=re.I)
    return html


def main():
    base = load_calendar_url()
    target = add_source_param(base)
    changed = []
    for root, _, files in os.walk(ROOT):
        for fn in files:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(root, fn)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                html = f.read()
            new_html = rewrite_links(html, target)
            if new_html != html:
                with open(path, 'w', encoding='utf-8') as w:
                    w.write(new_html)
                changed.append(os.path.relpath(path, ROOT))
    print('Updated booking CTAs in', len(changed), 'files')
    for p in changed[:20]:
        print('-', p)


if __name__ == '__main__':
    main()

