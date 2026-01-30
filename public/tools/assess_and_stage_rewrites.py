import re, json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / 'resources.html'
ART_DIR = ROOT / 'articles'
DATA = ROOT / 'data' / 'proppydata.json'
OUT_REPORT = ROOT / 'site-audit' / 'articles_assessment.md'
REWRITE_DIR = ART_DIR / '_rewrites'

REWRITE_TEMPLATE = """---
title: "{title}"
description: "{description}"
category: [{category}]
audience: [{audience}]
author: "Proppy Editorial"
publish_status: draft
sources:
  - name: ABS
    url: https://www.abs.gov.au/
  - name: RBA
    url: https://www.rba.gov.au/
  - name: PropTrack
    url: https://www.proptrack.com.au/insights/
  - name: CoreLogic
    url: https://www.corelogic.com.au/news-research
version: 1
---
# {title}

> Summary: {description}

## Key Takeaways
- [Fill 3–5 bullet takeaways referencing signals]

## Market Context
[Rewrite context in 2–3 short paragraphs.]

## Data Snapshot (Proppy)
- Vacancy: [FILL: %] • Rents (YoY): [FILL: %] • Listings (YoY): [FILL: %] • DOM: [FILL: days]
- Gross yield: [FILL: %] • Price 3y/5y/10y: [FILL]
Note: Verify against proppydata.json and latest sources.

## What the Data Shows
- [Bullet key observations pulled from signals.]

## Investor Actions
### Newer Investors
- [Actionable 3–4 bullets]

### Experienced Investors
- [Actionable 3–4 bullets]

## Risks & What to Watch
- [List regulatory/supply/interest‑rate risks with monitoring plan]

## Methodology
- Multi‑signal confirmation using vacancy, rents, listings, DOM, supply, lending.
- Validate at suburb/stock level prior to offers.

> Disclaimer: This article is general information only and not financial advice.
"""

def extract_slugs_from_resources(html_text: str):
    slugs = re.findall(r'href=\"articles/([a-z0-9\-]+)\.html\"', html_text)
    # keep order, de-duplicate
    seen = set()
    ordered = []
    for s in slugs:
        if s not in seen:
            seen.add(s)
            ordered.append(s)
    return ordered

def read_frontmatter_md(text: str):
    fm = {}
    body = text
    if text.strip().startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            fm_raw = parts[1]
            body = parts[2]
            for line in fm_raw.splitlines():
                if ':' in line:
                    k,v = line.split(':',1)
                    fm[k.strip()] = v.strip().strip('"')
    return fm, body

def count_metrics(text: str):
    words = len(re.findall(r'\b\w+\b', re.sub(r'<[^>]+>', ' ', text)))
    h2s = len(re.findall(r'^##\s', text, flags=re.M))
    imgs = text.count('![') + len(re.findall(r'<img ', text))
    data_mentions = len(re.findall(r'(vacancy|gross\s*yield|listings|dom|approvals|rent\s*(yo|q)q)', text, flags=re.I))
    return words, h2s, imgs, data_mentions

def main():
    REWRITE_DIR.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    res_html = RES.read_text(encoding='utf-8', errors='ignore')
    slugs = extract_slugs_from_resources(res_html)
    slugs = slugs[:46]
    rows = ["# Articles Assessment (Top 46 from resources.html)",""]
    for slug in slugs:
        md_path = ART_DIR / f"{slug}.md"
        html_path = ART_DIR / f"{slug}.html"
        title = slug.replace('-', ' ').title()
        description = ""
        category = "Strategy"
        audience = "Both"
        src_text = None
        if md_path.exists():
            txt = md_path.read_text(encoding='utf-8', errors='ignore')
            fm, body = read_frontmatter_md(txt)
            title = fm.get('title', title)
            description = fm.get('description', description)
            category = (fm.get('category','').strip('[]') or category).split(',')[0].strip() or category
            audience = (fm.get('audience','').strip('[]') or audience).split(',')[0].strip() or audience
            src_text = body
            words, h2s, imgs, data_mentions = count_metrics(body)
        elif html_path.exists():
            txt = html_path.read_text(encoding='utf-8', errors='ignore')
            # very rough extraction
            body = re.sub(r'[\s\S]*?<main[^>]*>', '', txt)
            body = re.sub(r'</main>[\s\S]*$', '', body)
            src_text = body
            words, h2s, imgs, data_mentions = count_metrics(body)
        else:
            rows.append(f"- {slug}: MISSING source file")
            continue
        rows.append(f"- {title} — words:{words} • h2:{h2s} • imgs:{imgs} • data refs:{data_mentions}")
        # Stage rewrite draft
        draft = REWRITE_TEMPLATE.format(title=title, description=description, category=category or 'Strategy', audience=audience or 'Both')
        (REWRITE_DIR / f"{slug}.md").write_text(draft, encoding='utf-8')
    OUT_REPORT.write_text('\n'.join(rows), encoding='utf-8')
    print(f"Assessed {len(slugs)} articles. Report: {OUT_REPORT}. Drafts in {REWRITE_DIR}")

if __name__ == '__main__':
    main()

