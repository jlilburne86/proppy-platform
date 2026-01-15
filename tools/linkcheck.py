#!/usr/bin/env python3
import os, sys, re
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = os.path.abspath(os.path.dirname(__file__) + '/..')

EXTERNAL_SCHEMES = ("http:", "https:", "mailto:", "tel:", "javascript:")

class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])
        if 'id' in attrs:
            self.ids.add(attrs['id'])


def read_html(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return ''


def collect_ids(path):
    parser = LinkCollector()
    parser.feed(read_html(path))
    return parser.ids


def check():
    # Map file -> ids
    html_files = [os.path.join(ROOT, f) for f in os.listdir(ROOT) if f.endswith('.html')]
    ids_map = {f: collect_ids(f) for f in html_files}

    broken = []
    skipped_external = 0

    for f in html_files:
        parser = LinkCollector()
        parser.feed(read_html(f))
        for href in parser.links:
            if not href or href.strip() == '' or href.strip() == '#':
                # empty or placeholder
                broken.append((f, href, 'empty-or-#'))
                continue
            u = urlparse(href)
            if u.scheme + (":" if u.scheme else "") in EXTERNAL_SCHEMES or href.startswith('//'):
                skipped_external += 1
                continue
            if href.startswith('#'):
                # intra-file fragment
                frag = href[1:]
                if frag and frag not in ids_map.get(f, set()):
                    broken.append((f, href, 'missing-id'))
                continue
            # Normalize path
            target_path = href.split('#',1)[0]
            # handle leading slash as root-relative
            if target_path.startswith('/'):
                target = os.path.join(ROOT, target_path.lstrip('/'))
            else:
                target = os.path.normpath(os.path.join(os.path.dirname(f), target_path))
            # If path points to dir, try index.html
            if os.path.isdir(target):
                idx = os.path.join(target, 'index.html')
                if not os.path.exists(idx):
                    broken.append((f, href, 'dir-no-index'))
                    continue
            else:
                if not os.path.exists(target):
                    # Try adding .html if missing extension
                    if not os.path.splitext(target)[1]:
                        alt = target + '.html'
                        if os.path.exists(alt):
                            continue
                    broken.append((f, href, 'missing-file'))
                    continue
            # If fragment present, check id in target doc
            if '#' in href:
                frag = href.split('#',1)[1]
                if frag:
                    tid = target if os.path.isfile(target) else os.path.join(target, 'index.html')
                    if frag not in ids_map.get(tid, collect_ids(tid)):
                        broken.append((f, href, 'missing-id-in-target'))
    return html_files, broken, skipped_external

if __name__ == '__main__':
    files, broken, skipped_ext = check()
    print(f"Checked {len(files)} HTML files (skipped {skipped_ext} external links)")
    if not broken:
        print("No broken links or anchors found.")
        sys.exit(0)
    print(f"Broken links found: {len(broken)}")
    # Group by file for readability
    by_file = {}
    for src, href, reason in broken:
        by_file.setdefault(src, []).append((href, reason))
    for f, items in sorted(by_file.items()):
        print(f"\n{os.path.basename(f)}:")
        for href, reason in items[:50]:
            print(f"  - {href} [{reason}]")
    # exit with non-zero to signal issues
    sys.exit(1)
