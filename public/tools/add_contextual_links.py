import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'articles'

# Map keywords/phrases to target slugs
KEYMAP = {
  r'\bvacancy rates?\b|\bvaca?ncy\b': 'vacancy-rates-explained-what-tight-and-loose-markets-mean',
  r'\bdays?-?on-?market\b|\bDOM\b': 'days-on-market-as-leading-indicator',
  r'\bbuilding approvals\b|\bapprovals\b|\bsupply constraints?\b|\bconstruction delays?\b': 'supply-constraints-construction-delays',
  r'\brentvesting\b': 'rentvesting-explained-how-investors-separate-home-and-portfolio',
  r'\bequity release\b|\busing equity\b': 'when-to-use-equity-when-to-save-cash',
  r'\binterstate migration\b|\bmigration patterns\b': 'interstate-migration-patterns-post-2020',
  r'\bgross yield\b|\byields?\b': 'rental-yield-compression-capital-cities',
  r'\bprice growth\b|\blong-?term growth\b': 'long-term-price-growth-what-20-year-data-reveals',
}

def parse_front(text: str):
    fm = {}
    body = text
    if text.strip().startswith('---'):
        parts = text.split('---',2)
        if len(parts) >= 3:
            for line in parts[1].splitlines():
                if ':' in line:
                    k,v = line.split(':',1)
                    fm[k.strip()] = v.strip().strip('"')
            body = parts[2]
    return fm, body

def is_published(slug: str) -> bool:
    p = ART / f'{slug}.md'
    if not p.exists():
        return False
    fm,_ = parse_front(p.read_text(encoding='utf-8', errors='ignore'))
    return (fm.get('publish_status','') or '').lower() == 'published'

def linkify(body: str, patterns, limit: int = 4) -> str:
    # Avoid replacing inside existing markdown links
    def safe_replace(text: str, pat: str, url: str) -> tuple[str, int]:
        count = 0
        def repl(m):
            nonlocal count
            before = text[max(0, m.start()-2):m.start()]
            after = text[m.end():m.end()+2]
            # crude guard if inside []() — skip if immediately preceded by [ or followed by )
            if '[' in before or ')' in after:
                return m.group(0)
            count += 1
            phrase = m.group(0)
            return f'[{phrase}]({url})'
        new = re.sub(pat, repl, text, count=1, flags=re.I)
        return new, count
    changed = 0
    txt = body
    for pat, href in patterns:
        if changed >= limit:
            break
        txt2, c = safe_replace(txt, pat, href)
        if c:
            txt = txt2
            changed += c
    return txt

def main():
    # Build target patterns using only published targets
    patterns = []
    for rx, slug in KEYMAP.items():
        if is_published(slug):
            # Within articles/, link to sibling HTML
            patterns.append((rx, f'{slug}.html'))
    updated = 0
    for md in ART.glob('*.md'):
        fm, body = parse_front(md.read_text(encoding='utf-8', errors='ignore'))
        status = (fm.get('publish_status','') or '').lower()
        if status != 'published':
            continue
        new_body = linkify(body, patterns, limit=2)
        # Cleanup old absolute-internal links from prior runs
        for _, slug in KEYMAP.items():
            new_body = new_body.replace(f'](articles/{slug}.html)', f']({slug}.html)')
        if new_body != body:
            txt = md.read_text(encoding='utf-8', errors='ignore')
            if txt.strip().startswith('---'):
                parts = txt.split('---',2)
                txt2 = parts[0] + '---' + parts[1] + '---' + new_body
            else:
                txt2 = new_body
            md.write_text(txt2, encoding='utf-8')
            updated += 1
    print('Contextual links added in', updated, 'articles')

if __name__ == '__main__':
    main()
