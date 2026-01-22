import re, textwrap, datetime
from pathlib import Path

ROOT = Path('/Users/boo2/Desktop/proppy')
RES = ROOT / 'resources.html'
ART_DIR = ROOT / 'articles'

LABEL_TO_CATEGORY = {
    'Market Update': 'Market Trends',
    'Guide': 'Strategy',
    'Hotspot Update': 'Suburb Profiles',
    'Basics': 'Strategy',
    'Strategy': 'Strategy',
}

BLUEPRINT_BODY = textwrap.dedent('''
# {title}

<Standfirst: 2–3 sentences summarising the insight>

![Illustration](/assets/screenshots/platform-screenshot.png)
![Signals](/assets/screenshots/technology.png)
![Workflow](/assets/screenshots/how-it-works.png)
![Portfolio](/assets/screenshots/homepage-9.png)

## Market Context
- National or regional overview with cited data.

## Key Drivers
- Supply & demand
- Population & infrastructure
- Lending or buyer behaviour

## What the Data Shows
- Bullet points or short paragraphs; compare across states/years.

## Expert Insight
- Quotes or paraphrased commentary with attribution.

## Investor Lens
- For beginners
- For experienced investors

## Risks & Considerations
- Market volatility, regulation, supply risks.

## Key Takeaways
- 3–5 neutral, practical insights.

> Disclaimer: This article is general information only and does not constitute financial, taxation or legal advice.
''')

def slugify(t: str) -> str:
    t = t.strip().lower()
    t = re.sub(r"[’'“”]", '', t)
    t = re.sub(r"[^a-z0-9]+", '-', t).strip('-')
    return t

def ensure_article(title: str, category: str):
    slug = slugify(title)
    md = ART_DIR / f'{slug}.md'
    if md.exists():
        return slug
    today = datetime.date.today().isoformat()
    fm = textwrap.dedent(f'''---
title: "{title}"
description: "Draft article: {title}"
category: [{category}]
audience: [Both]
reading_time: "7 min"
publish_status: draft
author: "Proppy Editorial"
owner: "editor@proppy.com.au"
next_review_date: "{today}"
sources:
  - name: "ABS"
    url: "https://www.abs.gov.au/"
  - name: "RBA"
    url: "https://www.rba.gov.au/"
  - name: "PropTrack"
    url: "https://www.proptrack.com.au/insights/"
version: 1
---
''')
    body = BLUEPRINT_BODY.format(title=title)
    ART_DIR.mkdir(exist_ok=True)
    md.write_text(fm + '\n' + body, encoding='utf-8')
    return slug

def update_resources_cards():
    html = RES.read_text(encoding='utf-8')
    # Identify the cards grid section and iterate article blocks
    card_pattern = re.compile(r'<article[\s\S]*?</article>')
    def repl(block: str) -> str:
        # extract title within h3
        m = re.search(r'<h3[^>]*>([\s\S]*?)</h3>', block)
        if not m:
            return block
        title = re.sub(r'\s+', ' ', m.group(1)).strip()
        # extract label text (Market Update/Guide/etc.)
        label_m = re.search(r'<span[^>]*class=\"[^\"]*uppercase[^\"]*\"[^>]*>([^<]+)</span>', block)
        label = label_m.group(1).strip() if label_m else 'Guide'
        category = LABEL_TO_CATEGORY.get(label, 'Strategy')
        slug = ensure_article(title, category)
        # derive CTA text
        cta_text = 'Read Article'
        if 'Read Report' in block:
            cta_text = 'Read Report'
        elif 'Read Guide' in block:
            cta_text = 'Read Guide'
        elif 'View Analysis' in block:
            cta_text = 'View Analysis'
        # replace the CTA container with a proper anchor
        block = re.sub(r'<div class=\"mt-auto\">[\s\S]*?</div>',
                       f'<div class="mt-auto">\n<a href="/articles/{slug}.html">{cta_text} <span class="material-symbols-outlined text-sm">arrow_forward</span></a>\n</div>',
                       block, count=1)
        return block

    new_html = card_pattern.sub(lambda m: repl(m.group(0)), html)
    if new_html != html:
        RES.write_text(new_html, encoding='utf-8')
        print('Updated resource cards to link articles')
    else:
        print('No changes applied to resource cards')

if __name__ == '__main__':
    update_resources_cards()

