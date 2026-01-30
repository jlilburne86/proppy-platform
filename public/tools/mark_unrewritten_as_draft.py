from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'articles'

KEEP = set([
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
])

def set_status(text: str, status: str) -> str:
    out = []
    in_fm = False
    seen = False
    for line in text.splitlines():
        if line.strip() == '---':
            in_fm = not in_fm
        if in_fm and line.lower().startswith('publish_status:'):
            out.append(f'publish_status: {status}')
            seen = True
        else:
            out.append(line)
    if not seen:
        try:
            i = out.index('---', 1)
            out.insert(i, f'publish_status: {status}')
        except ValueError:
            return text
    return '\n'.join(out)

def main():
    changed = 0
    for p in ART.glob('*.md'):
        slug = p.stem
        txt = p.read_text(encoding='utf-8', errors='ignore')
        if slug in KEEP:
            new = set_status(txt, 'published')
        else:
            new = set_status(txt, 'draft')
        if new != txt:
            p.write_text(new, encoding='utf-8')
            changed += 1
    print('Updated publish_status in', changed, 'files')

if __name__ == '__main__':
    main()

