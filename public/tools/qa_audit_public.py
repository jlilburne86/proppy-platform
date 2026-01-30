import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / 'public'
OUT = ROOT / 'site-audit' / 'qa_public.md'

CTA_PATTERNS = [
    re.compile(r'>\s*Book( a Call)?\s*<', re.I),
    re.compile(r'>\s*Contact\s*<', re.I),
    re.compile(r'>\s*Start Free Assessment\s*<', re.I),
    re.compile(r'>\s*Pricing\s*<', re.I),
    re.compile(r'>\s*Get Started\s*<', re.I),
]

def extract_anchors(html: str):
    anchors = re.findall(r'<a\s+[^>]*>', html, flags=re.I)
    data = []
    for a in anchors:
        href_m = re.search(r'href=\"([^\"]*)\"', a, flags=re.I)
        href = href_m.group(1).strip() if href_m else ''
        data.append((a, href))
    return data

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    files = list(PUB.glob('*.html')) + list((PUB/'articles').glob('*.html')) + list((PUB/'property').glob('*.html'))
    broken = []
    empty = []
    hash_only = []
    js_void = []
    ctas = []
    nav_ok = []
    nav_missing = []
    for f in files:
        html = f.read_text(encoding='utf-8', errors='ignore')
        # nav presence
        if all(x in html for x in ['id="navx-burger"', 'class="navx-drawer', 'class="navx-overlay']):
            nav_ok.append(str(f.relative_to(PUB)))
        else:
            nav_missing.append(str(f.relative_to(PUB)))
        # anchors
        for a, href in extract_anchors(html):
            if not href:
                empty.append((str(f.relative_to(PUB)), a))
            elif href == '#':
                hash_only.append((str(f.relative_to(PUB)), a))
            elif href.startswith('javascript:'):
                js_void.append((str(f.relative_to(PUB)), a))
            # CTA capture
            for pat in CTA_PATTERNS:
                if pat.search(a + html[html.find(a)+len(a): html.find(a)+len(a)+120]):
                    ctas.append((str(f.relative_to(PUB)), href, pat.pattern))

    # Build report
    lines = [
        '# QA Audit (Public build)',
        '',
        f'- Pages scanned: {len(files)}',
        f'- Nav present on: {len(nav_ok)} pages; missing on: {len(nav_missing)} pages',
        f'- Empty href anchors: {len(empty)}',
        f'- Hash-only anchors: {len(hash_only)}',
        f'- javascript:void anchors: {len(js_void)}',
        f'- CTAs found: {len(ctas)}',
        '',
        '## Missing Nav (should be 0)',
    ]
    for p in nav_missing[:50]:
        lines.append(f'- {p}')
    lines += ['', '## Empty href anchors (should be 0)']
    for p,a in empty[:50]:
        lines.append(f'- {p}: {a}')
    lines += ['', '## Hash-only anchors (review)']
    for p,a in hash_only[:50]:
        lines.append(f'- {p}: {a}')
    lines += ['', '## javascript:void anchors (review)']
    for p,a in js_void[:50]:
        lines.append(f'- {p}: {a}')
    lines += ['', '## CTAs']
    for p,href,kind in ctas:
        lines.append(f'- {p} → {href} ({kind})')

    OUT.write_text('\n'.join(lines), encoding='utf-8')
    print('Wrote', OUT)

if __name__ == '__main__':
    main()

