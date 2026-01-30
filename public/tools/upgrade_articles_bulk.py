import os, re, textwrap
from pathlib import Path

ROOT = Path('/Users/boo2/Desktop/proppy')
ART = ROOT / 'articles'

GALLERY = [
    '/assets/screenshots/platform-screenshot.png',
    '/assets/screenshots/technology.png',
    '/assets/screenshots/how-it-works.png',
    '/assets/screenshots/homepage-9.png',
]

def make_desc(title: str) -> str:
    title_l = title.lower()
    if 'adelaide' in title_l:
        return 'Where demand is outpacing supply across Adelaide — vacancy, rents, and fundamentals.'
    if 'tasmania' in title_l or 'hobart' in title_l:
        return 'How Hobart and regional Tasmania differ — vacancy, rents, and supply dynamics.'
    if 'coastal' in title_l:
        return 'A balanced look at coastal market shifts over the past decade.'
    if 'which capital cities' in title_l:
        return 'A comparative snapshot of which capitals lead and lag on key indicators.'
    if 'affordable' in title_l:
        return 'Areas still under national median prices — checked against demand and supply.'
    if 'emerging suburbs' in title_l:
        return 'Signals pointing to emerging suburbs heading into 2026.'
    if 'rentvesting' in title_l and 'practice' in title_l:
        return 'A decade-long look at rentvesting outcomes — what worked and what didn’t.'
    if 'rentvesting' in title_l:
        return 'How rentvesting separates home choice from portfolio strategy.'
    if 'co-ownership' in title_l:
        return 'What the data and case studies say about co-ownership structures.'
    if 'using equity' in title_l:
        return 'A pragmatic example of using equity to expand a portfolio — with risks.'
    if 'lessons from investors' in title_l:
        return 'What early corridor investors learned — a balanced set of takeaways.'
    if 'market downturns' in title_l:
        return 'How Australian property historically responded in downturns — risks and resilience.'
    if 'overconcentration' in title_l:
        return 'Why concentrating in one market is risky — how to diversify sensibly.'
    if 'short-term rentals' in title_l:
        return 'Changing rules for short-term rentals across states — what matters for investors.'
    if 'regulatory changes' in title_l and 'landlords' in title_l:
        return 'The regulatory changes affecting landlords now — and how to stay compliant.'
    if 'vacancy rates' in title_l:
        return 'What tight and loose rental markets mean — and how to read vacancy.'
    if 'lessons from past rba' in title_l or 'interest rates and property' in title_l:
        return 'What prior RBA cycles suggest — planning without relying on forecasts.'
    return f'A measured look at {title} — data-led and balanced.'

def ensure_images(body: str) -> str:
    # count markdown images
    count = len(re.findall(r'!\[[^\]]*\]\(([^)]+)\)', body))
    needed = max(0, 4 - count)
    if needed == 0:
        return body
    figs = []
    for i in range(needed):
        src = GALLERY[i % len(GALLERY)]
        figs.append(f"![Illustration]({src})")
    # insert after H1 and standfirst if present
    parts = body.split('\n')
    try:
        h1_idx = next(i for i,l in enumerate(parts) if l.startswith('# '))
    except StopIteration:
        h1_idx = 0
    insert_at = h1_idx + 1
    # skip blank + standfirst line if present
    if insert_at < len(parts) and parts[insert_at].strip() == '':
        insert_at += 1
    if insert_at < len(parts) and parts[insert_at].strip().startswith('<Standfirst'):
        insert_at += 1
    parts[insert_at:insert_at] = figs + ['']
    return '\n'.join(parts)

def upgrade(md_path: Path) -> bool:
    txt = md_path.read_text(encoding='utf-8', errors='ignore')
    if '---' not in txt:
        return False
    fm, body = txt.split('---',2)[1:]  # fm, rest
    # rest still contains trailing '---' already split; body begins after fm
    # normalise
    body = body.strip('\n')
    changed = False
    # description line
    m = re.search(r'\ndescription:\s*"([^"]*)"', fm)
    if m:
        cur = m.group(1)
        if cur.startswith('Outline and data sources for:') or cur.startswith('Draft article:'):
            title_m = re.search(r'\ntitle:\s*"([^"]+)"', fm)
            title = title_m.group(1) if title_m else md_path.stem.replace('-', ' ').title()
            new_desc = make_desc(title)
            fm = fm.replace(f'description: "{cur}"', f'description: "{new_desc}"')
            changed = True
    # ensure author field exists and set to Proppy Editorial
    if 'author:' not in fm:
        fm = fm.replace('publish_status: draft', 'publish_status: draft\nauthor: "Proppy Editorial"')
        changed = True
    else:
        fm = re.sub(r'author:\s*"[^"]*"', 'author: "Proppy Editorial"', fm)
    # standfirst
    if '<Standfirst:' in body:
        title_m = re.search(r'\ntitle:\s*"([^"]+)"', fm)
        title = title_m.group(1) if title_m else md_path.stem.replace('-', ' ').title()
        standfirst = f"A balanced, data‑led overview of {title.lower()}."
        body = body.replace('<Standfirst: 2–3 sentences summarising the insight>', standfirst)
        changed = True
    # ensure images
    new_body = ensure_images(body)
    if new_body != body:
        body = new_body
        changed = True
    if not changed:
        return False
    md_path.write_text('\n'.join(['---', fm, body]), encoding='utf-8')
    return True

def main():
    updated = []
    for p in ART.glob('*.md'):
        if upgrade(p):
            updated.append(p.name)
    print('Upgraded', len(updated), 'articles')
    for u in updated:
        print('-', u)

if __name__ == '__main__':
    main()

