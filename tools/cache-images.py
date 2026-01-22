#!/usr/bin/env python3
import json, os
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'properties.json'
OUTDIR = ROOT / 'assets' / 'properties' / 'live'
HDRS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15'}

def dl(url: str, slug: str) -> str:
    parsed = urlparse(url)
    base = os.path.basename(parsed.path)
    ext = '.jpg'
    if '.' in base:
        ext = '.' + base.split('.')[-1]
    OUTDIR.mkdir(parents=True, exist_ok=True)
    out = OUTDIR / f"{slug}{ext}"
    with urlopen(Request(url, headers=HDRS), timeout=30) as r:
        data = r.read()
    out.write_bytes(data)
    return str(out.relative_to(ROOT))

def main():
    items = json.loads(DATA.read_text())
    changed = False
    for it in items:
        img = it.get('image','')
        if isinstance(img, str) and img.startswith('http'):
            try:
                local = dl(img, it['slug'])
                it['image'] = local
                changed = True
            except Exception:
                pass
    if changed:
        DATA.write_text(json.dumps(items, indent=2))
        print('Cached images and updated data file')
    else:
        print('No remote images to cache')

if __name__ == '__main__':
    main()
