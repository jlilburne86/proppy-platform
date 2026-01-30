#!/usr/bin/env python3
"""
Rewrite the 46 RSS-listed articles into the approved Proppy template.

Actions per article:
- Parse existing frontmatter; keep title/category/audience when present.
- Replace frontmatter with version=2, publish_status=published, next_review_date ~6 months ahead,
  default sources (ABS, RBA, PropTrack, CoreLogic), and computed reading_time.
- Replace body with the standard structured template, tailored by title.
- Non-RSS markdown files are left untouched.

Note: Data points are left as [CHECK] with exact suggested queries per the editorial prompt.
"""

from __future__ import annotations
import re
import sys
import textwrap
from datetime import date, timedelta
from pathlib import Path
from typing import Tuple, Dict
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
ART_DIR = ROOT / 'articles'
RSS_PATH = ROOT / 'articles.xml'


def split_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
    """Very light-weight frontmatter splitter; returns (fm_text_map, body)."""
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n([\s\S]*)\Z', content, re.DOTALL)
    if not m:
        return ({}, content)
    fm_text = m.group(1)
    body = m.group(2)
    fm: Dict[str, str] = {}
    # shallow parse of simple key: value pairs we care about
    for line in fm_text.splitlines():
        if not line.strip() or line.strip().startswith('#'):
            continue
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm, body


def sanitize_description(txt: str) -> str:
    # Ensure approximately 155–165 chars by truncating gracefully.
    base = txt.strip().replace('\n', ' ')
    if len(base) <= 165:
        return base
    # cut at last space before 162 chars and add ellipsis if needed
    cut = base[:162]
    cut = cut[: cut.rfind(' ')] if ' ' in cut else cut
    if not cut.endswith('.'):
        cut += '…'
    return cut


def infer_category(title: str, existing: str | None) -> str:
    if existing:
        # existing may be like "[Strategy]"; normalise
        return existing.strip('[]') or 'Strategy'
    t = title.lower()
    if 'case study' in t or 'case' in t:
        return 'Case Studies'
    if 'cycle' in t or 'quarterly' in t or 'review' in t:
        return 'Cycles'
    if 'suburb' in t or 'tasmania' in t or 'perth' in t or 'logan' in t:
        return 'Suburb Profiles'
    if 'risk' in t or 'regulatory' in t or 'vacancy' in t:
        return 'Risk'
    if 'market' in t or 'prices' in t or 'growth' in t:
        return 'Market Trends'
    return 'Strategy'


def infer_audience(existing: str | None) -> str:
    if existing:
        return existing.strip('[]') or 'Both'
    return 'Both'


def make_description(title: str) -> str:
    return sanitize_description(
        f"A data‑led guide to {title.lower()} — using vacancy, rents, listings, DOM and supply signals to translate analysis into practical investor actions."
    )


def compute_read_time_words(text: str, wpm: int = 220) -> str:
    words = len(re.findall(r"\b\w+\b", text))
    mins = max(5, int(round(words / max(1, wpm))))
    return f"{mins} min"


def build_body(title: str) -> str:
    topic = title
    intro = (
        f"Growth compounds equity; yield funds holding. This article examines {topic.lower()} with a repeatable, multi‑signal approach—vacancy, rents, listings, days on market, and supply—then turns it into investor actions."
    )
    body = f"""
# {title}

{intro}

![Illustration](/assets/screenshots/technology.png)
![Illustration](/assets/screenshots/how-it-works.png)
![Illustration](/assets/screenshots/platform-screenshot.png)
![Illustration](/assets/screenshots/homepage-9.png)

## Market Context
- Rental market tightness and uneven listing volumes have shaped yields and price momentum differently across cities and stock types.
- Policy, borrowing costs, and migration shifts matter—read them through high‑signal indicators that update monthly or quarterly.

Examples to verify and cite:
- Vacancy remained low in several markets through late 2025–early 2026, with sub‑1% periods in some corridors [CHECK: PropTrack/Domain vacancy, mm/yyyy, city/suburb].
- New dwelling approvals eased from 2021 peaks before stabilising in 2024–2025, varying by state [CHECK: ABS 8731.0, mm/yyyy, NSW/VIC/QLD lines].

## Key Drivers
- Vacancy: Lower vacancy supports rent growth and reduces leasing risk.
- Rent momentum: Sustained rent increases improve gross yield and buffers.
- Listings & DOM: Scarcer listings and falling DOM can confirm buyer depth.
- Supply pipeline: Completions vs approvals inform medium‑term rental pressure.
- Borrowing costs: Assessment rates shape buyer depth and turnover.
- Stock mix: Houses vs units, and micro‑location livability, drive dispersion.

## What the Data Shows
- Long‑run (10–20y): Compounding and holding quality assets through cycles dominate outcomes (CoreLogic indexes, [CHECK series & date]).
- 12–24m momentum: Some corridors show strong rent growth with modest price gains, others the reverse [CHECK: PropTrack/ABS rents, CoreLogic price indexes, mm/yyyy].
- Last 1–3 quarters: Listings, vacancy, and approvals provide near‑term signal; confirm across 2–3 updates to avoid noise.

## 🔍 Proppy Data Lens
| Signal              | Recent Read (mm/yyyy) | Direction | Why it matters |
|---------------------|------------------------|-----------|----------------|
| Vacancy             | [CHECK: %]            | ↘/↗/→     | Tight vacancy supports yields and leasing certainty. |
| Rents (YoY)         | [CHECK: %]            | ↘/↗/→     | Rent growth boosts gross yield and buffers. |
| Listings (YoY)      | [CHECK: %]            | ↘/↗/→     | Scarcity can support prices; rising stock can loosen conditions. |
| DOM                 | [CHECK: days]         | ↘/↗/→     | Faster sales often signal stronger buyer depth. |
| Building approvals  | [CHECK: level/YoY]    | ↘/↗/→     | Lower approvals today can mean tighter future rentals. |
| Investor lending    | [CHECK: YoY]          | ↘/↗/→     | Participation shifts influence competition and timing. |

Interpretation:
- Yield‑tilted: Vacancy low + rents rising + flat prices → prioritise resilient cashflow assets with rent review scope.
- Growth‑tilted: Falling DOM + tighter listings + stable borrowing costs → target quality assets in constrained micro‑locations.
- Mixed: Extend observation to the next print; seek 2–3 signals in agreement.

## Methodology & Criteria
- Dashboard (monthly/quarterly): Vacancy, rent YoY/QoQ, listings YoY, DOM, approvals, investor lending.
- Qualitative overlay: Micro‑location (arterials/noise/flood), stock quality (layout, light, maintenance), body corporate/land size.
- Guideline thresholds: “Vacancy < ~1.5% with rising rents” strengthens yield case; “DOM falling and listings tightening” strengthens growth case.

Worked examples
- Gross yield = annual rent / price. Example: $560/wk → $29,120/yr on $620,000 → 4.7% gross.
- Cashflow buffer (pre‑tax) = annual rent − interest − insurance − rates − maintenance − PM fees. Stress test at +100–150 bps.
- Equity sensitivity (illustrative): +6% on $620,000 → +$37,200 paper equity; compare to cashflow outcome.

## State Highlights (Qualitative)
- NSW/ACT: Inner‑ring scarcity dynamics; some middle‑ring units improve on yield where vacancy stays tight; outer‑ring depends on new‑build delivery and commute realities.
- VIC/TAS: Monitor approvals vs completions and rental pressure in growth corridors; inner/middle rings bifurcate by stock quality.
- QLD: SEQ demand has supported rents; watch corridor‑specific vacancy and listings when choosing between house yield plays vs inner‑unit recovery stories.
- SA/WA/NT: Tight vacancy in parts of SA/WA supported rent growth; confirm micro‑location and pipeline to avoid overpaying for transient yield.

## Risks & What to Watch Next
- Policy & Tenancy: State‑level rental rule changes and short‑stay regulation [CHECK source/date]; watch compliance costs.
- Supply Shocks: Catch‑up in approvals/completions can temper rents; track ABS approvals monthly.
- Migration & Employment: Shifts in interstate/overseas flows and labour markets alter rental pressure [CHECK: ABS/RBA].
- Cost & Rates: Funding costs and assessment rates change buyer depth; monitor RBA statements and lender pricing.

## Investor Actions
### For Newer Investors
- Define a 6‑metric dashboard; refresh monthly.
- Shortlist 3 suburbs that meet yield or growth criteria; run standard DD (zoning, overlays, stock quality).
- Timebox research (e.g., 2 weeks), then inspect and decide.

### For Experienced Investors
- Standardise cross‑state DD; set alerts for key signals.
- Run sensitivity (rent −5% / interest +1.5%) before offers.
- Sequence portfolio: Add a yield stabiliser if buffers are thin; lean into growth when signals align.

## Key Takeaways
- Let multi‑signal confirmation guide timing; avoid single‑metric bets.
- Balance current cashflow with future equity based on buffers and goals.
- Prefer quality assets in constrained micro‑locations; hold through cycles.

> Disclaimer: This article is general information only and does not constitute financial, taxation or legal advice.

References
- ABS — Building Approvals (8731.0) https://www.abs.gov.au/
- RBA — Statements on Monetary Policy https://www.rba.gov.au/
- PropTrack — Market Insights https://www.proptrack.com.au/insights/
- CoreLogic — Indices & Research https://www.corelogic.com.au/news-research
"""
    return textwrap.dedent(body).strip() + "\n"


def rewrite_article(md_path: Path, rss_title: str | None = None) -> bool:
    raw = md_path.read_text(encoding='utf-8', errors='ignore')
    fm, _ = split_frontmatter(raw)

    title = (fm.get('title') or rss_title or md_path.stem.replace('-', ' ').title()).strip('"')
    existing_cat = fm.get('category')
    existing_aud = fm.get('audience')

    category = infer_category(title, existing_cat)
    audience = infer_audience(existing_aud)
    description = make_description(title)

    # next review ~6 months ahead
    next_review = (date.today() + timedelta(days=180)).isoformat()

    # Build body first to compute reading time
    body = build_body(title)
    reading_time = compute_read_time_words(body)

    fm_lines = [
        '---',
        f'title: "{title}"',
        f'description: "{description}"',
        f'category: [{category}]',
        f'audience: [{audience}]',
        f'reading_time: "{reading_time}"',
        'publish_status: published',
        'author: "Proppy Editorial"',
        'owner: "editor@proppy.com.au"',
        f'next_review_date: "{next_review}"',
        'sources:',
        '  - name: "ABS"',
        '    url: "https://www.abs.gov.au/"',
        '  - name: "RBA"',
        '    url: "https://www.rba.gov.au/"',
        '  - name: "PropTrack"',
        '    url: "https://www.proptrack.com.au/insights/"',
        '  - name: "CoreLogic"',
        '    url: "https://www.corelogic.com.au/news-research"',
        'version: 2',
        '',
        body,
    ]
    out = "\n".join(fm_lines)
    md_path.write_text(out, encoding='utf-8')
    return True


def parse_rss_slugs() -> Dict[str, str]:
    items: Dict[str, str] = {}
    tree = ET.parse(RSS_PATH)
    root = tree.getroot()
    # find all item/title + item/link
    for item in root.findall('.//item'):
        title_el = item.find('title')
        link_el = item.find('link')
        if title_el is None or link_el is None:
            continue
        title = title_el.text.strip()
        link = link_el.text.strip()
        # link expected like http://.../articles/<slug>.html
        m = re.search(r'/articles/([^/]+)\.html', link)
        if not m:
            continue
        slug = m.group(1)
        items[slug] = title
    return items


def main() -> int:
    if not ART_DIR.exists():
        print(f"Articles directory not found: {ART_DIR}")
        return 1
    if not RSS_PATH.exists():
        print(f"RSS file not found: {RSS_PATH}")
        return 1

    slugs = parse_rss_slugs()
    if not slugs:
        print("No items parsed from RSS.")
        return 1

    rewritten = []
    missing = []
    for slug, rss_title in slugs.items():
        path = ART_DIR / f"{slug}.md"
        if not path.exists():
            missing.append(slug)
            continue
        try:
            rewrite_article(path, rss_title)
            rewritten.append(slug)
        except Exception as e:
            print(f"Error rewriting {slug}: {e}")

    print(f"Rewritten {len(rewritten)} articles (from RSS list of {len(slugs)}).")
    if missing:
        print("Missing markdown for slugs:")
        for s in missing:
            print('-', s)
    return 0


if __name__ == '__main__':
    sys.exit(main())

