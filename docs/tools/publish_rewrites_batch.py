from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'articles'
REWRITES = ART / '_rewrites'

BATCH1 = [
    'adelaides-northern-suburbs',
    'auction-clearance-rates-what-they-signal',
    'boom-plateau-or-decline-how-to-read-market-signals',
    'brisbane-growth-corridors-ipswich-logan-and-moreton-bay',
    'building-your-first-investment-property-portfolio',
    'case-study-converting-to-dual-income',
    'case-study-first-time-buyer-regional-qld',
    'case-study-surviving-rate-rises',
    'case-study-multi-city-portfolio-building',
    'case-study-renovating-for-value-vs-cash',
]

def set_published(text: str) -> str:
    out = []
    in_fm = False
    seen = False
    for line in text.splitlines():
        if line.strip() == '---':
            if not in_fm:
                in_fm = True
            else:
                in_fm = False
        if in_fm and line.lower().startswith('publish_status:'):
            out.append('publish_status: published')
            seen = True
        else:
            out.append(line)
    if not seen:
        # insert before closing front-matter if possible
        lines = out
        try:
            i = lines.index('---', 1)
        except ValueError:
            return text
        lines.insert(i, 'publish_status: published')
        return '\n'.join(lines)
    return '\n'.join(out)

def main():
    published = []
    for slug in BATCH1:
        src = (REWRITES / f'{slug}.md')
        dst = (ART / f'{slug}.md')
        if not src.exists():
            print('Missing rewrite for', slug)
            continue
        txt = src.read_text(encoding='utf-8', errors='ignore')
        txt = set_published(txt)
        dst.write_text(txt, encoding='utf-8')
        published.append(slug)
    print('Published rewrites:', len(published))

if __name__ == '__main__':
    main()

