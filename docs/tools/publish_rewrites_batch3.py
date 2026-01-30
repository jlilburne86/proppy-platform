from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'articles'
REWRITES = ART / '_rewrites'

BATCH3 = [
    'hobarts-expanding-outer-ring',
    'house-vs-unit-what-the-data-shows',
    'interest-rate-risk-management',
    'interstate-migration-patterns-post-2020',
    'legislative-changes-and-tenancy-reforms',
    'long-term-price-growth-what-20-year-data-reveals',
    'natural-disasters-insurance-and-resilience',
    'newcastle-and-lake-macquarie',
    'overleveraging-and-cashflow-stress',
    'perth-metro-north-joondalup-wanneroo',
]

def set_published(text: str) -> str:
    lines = text.splitlines()
    out = []
    in_fm = False
    seen = False
    for line in lines:
        if line.strip() == '---':
            in_fm = not in_fm
        if in_fm and line.lower().startswith('publish_status:'):
            out.append('publish_status: published')
            seen = True
        else:
            out.append(line)
    if not seen:
        try:
            i = out.index('---', 1)
            out.insert(i, 'publish_status: published')
        except ValueError:
            pass
    return '\n'.join(out)

def main():
    published = []
    for slug in BATCH3:
        src = REWRITES / f'{slug}.md'
        dst = ART / f'{slug}.md'
        if not src.exists():
            print('Missing rewrite draft for', slug)
            continue
        txt = src.read_text(encoding='utf-8', errors='ignore')
        txt = set_published(txt)
        dst.write_text(txt, encoding='utf-8')
        published.append(slug)
    print('Published rewrites (batch 3):', len(published))

if __name__ == '__main__':
    main()
