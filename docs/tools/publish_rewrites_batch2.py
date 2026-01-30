from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'articles'
REWRITES = ART / '_rewrites'

BATCH2 = [
    'central-coast-nsw-opportunity',
    'new-estates-vs-established-suburbs',
    'diy-investing-vs-buyers-agent-value',
    'days-on-market-as-leading-indicator',
    'demographic-trends-shaping-demand',
    'depreciation-and-tax-optimization-for-investors',
    'first-home-buyer-grants-market-impact',
    'foreign-investment-trends-australia',
    'geelong-and-bellarine-peninsula',
    'gold-coast-growth-corridors',
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
    for slug in BATCH2:
        src = REWRITES / f'{slug}.md'
        dst = ART / f'{slug}.md'
        if not src.exists():
            print('Missing rewrite draft for', slug)
            continue
        txt = src.read_text(encoding='utf-8', errors='ignore')
        txt = set_published(txt)
        dst.write_text(txt, encoding='utf-8')
        published.append(slug)
    print('Published rewrites (batch 2):', len(published))

if __name__ == '__main__':
    main()

