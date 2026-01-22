import os, re, textwrap, datetime
from pathlib import Path

ROOT = Path('/Users/boo2/Desktop/proppy')
ART_DIR = ROOT / 'articles'

PILLARS = {
  'Market Trends & Analysis': [
    "Australia’s 2026 Housing Market Outlook: What the Data Is Signalling",
    "Capital Cities vs Regional Markets: Where Growth Has Shifted",
    "Interest Rates and Property: Lessons from Past RBA Cycles",
    "Rental Market Pressures Explained: Supply, Demand and Rents",
    "Investor Lending Trends Across Australia’s States",
    "Housing Supply vs Population Growth: Why Shortages Persist",
    "Which Capital Cities Are Leading — and Which Are Lagging",
    "Units vs Houses: How Performance Has Changed Over the Decade",
  ],
  'Suburb & Regional Profiles': [
    "Emerging Suburbs to Watch Heading into 2026",
    "Affordable Investment Areas Still Under the National Median",
    "Coastal Markets That Have Transformed Over the Past 10 Years",
    "Brisbane Growth Corridors: Ipswich, Logan and Moreton Bay",
    "Perth’s Recovery Story: Suburbs Benefiting from WA’s Economy",
    "Adelaide’s Quiet Achievers: Where Demand Is Outpacing Supply",
    "Melbourne’s Shifting Growth Pattern: Inner vs Outer Suburbs",
    "Tasmania’s Property Market Explained: Hobart vs Regional Areas",
  ],
  'Investment Strategy (Educational)': [
    "Capital Growth vs Rental Yield: Understanding the Trade-Offs",
    "Diversification in Property: Cities, States and Asset Types",
    "Buy-and-Hold Explained: Why Long-Term Investors Focus on Cycles",
    "Value-Add Strategies: Renovation, Layout and Usability Improvements",
    "First-Time Investor Guide: Market Fundamentals to Understand",
    "Rentvesting Explained: How Investors Separate Home and Portfolio",
    "Co-Ownership in Property: What the Data and Case Studies Show",
  ],
  'Property Cycles & Timing': [
    "Understanding the Australian Property Cycle",
    "Boom, Plateau or Decline? How to Read Market Signals",
    "Post-Pandemic Property Shifts: What Has Endured and What Hasn’t",
    "When Growth Slows: Historical Examples from Australian Cities",
    "Long-Term Price Growth: What 20-Year Data Reveals",
  ],
  'Real Investor Case Studies': [
    "From First Property to Portfolio: A Long-Term Investor Journey",
    "Regional Investing Case Study: Growth Outside Capital Cities",
    "Rentvesting in Practice: A Decade of Outcomes",
    "Using Equity to Expand a Portfolio: An Educational Example",
    "Lessons from Investors Who Bought Early in Growth Corridors",
  ],
  'Risk, Regulation & Market Reality': [
    "Regulatory Changes Affecting Australian Landlords",
    "Short-Term Rentals and Changing State Rules",
    "Climate Risk and Property: What Investors Should Know",
    "Vacancy Rates Explained: What Tight and Loose Markets Mean",
    "Market Downturns: How Australian Property Has Historically Responded",
    "Overconcentration Risk: Why One Market Is Rarely Enough",
  ],
}

CATEGORY_MAP = {
  'Market Trends & Analysis': 'Market Trends',
  'Suburb & Regional Profiles': 'Suburb Profiles',
  'Investment Strategy (Educational)': 'Strategy',
  'Property Cycles & Timing': 'Cycles',
  'Real Investor Case Studies': 'Case Studies',
  'Risk, Regulation & Market Reality': 'Risk',
}

def slugify(title: str) -> str:
    t = title.lower()
    t = re.sub(r"[’'“”]", '', t)
    t = re.sub(r"[^a-z0-9]+", '-', t).strip('-')
    return t

def front_matter(title: str, category: str) -> str:
    desc = f"Outline and data sources for: {title}"
    today = datetime.date.today().isoformat()
    return textwrap.dedent(f"""
    ---
    title: "{title}"
    description: "{desc}"
    category: [{category}]
    audience: [Both]
    reading_time: "7 min"
    publish_status: draft
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
    """)

BODY = textwrap.dedent("""
# H1

<Standfirst: 2–3 sentences summarising the insight>

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
""")

def ensure_articles():
    ART_DIR.mkdir(exist_ok=True)
    created = []
    for pillar, titles in PILLARS.items():
        cat = CATEGORY_MAP[pillar]
        for title in titles:
            slug = slugify(title)
            path = ART_DIR / f"{slug}.md"
            if not path.exists():
                content = front_matter(title, cat) + '\n' + BODY.replace('# H1', f'# {title}')
                path.write_text(content, encoding='utf-8')
                created.append(path.name)
    return created

def update_resources():
    p = ROOT / 'resources.html'
    html = p.read_text(encoding='utf-8')
    # Build index block
    sections = []
    for pillar, titles in PILLARS.items():
        items = []
        for title in titles:
            slug = slugify(title)
            items.append(f'<li><a class="text-primary hover:underline" href="/articles/{slug}.md">{title}</a></li>')
        ul = '<ul class="list-disc pl-5 space-y-1">' + '\n'.join(items) + '</ul>'
        sections.append(f'<div><h3 class="text-lg font-bold mb-2">{pillar}</h3>{ul}</div>')
    grid = '<div class="grid grid-cols-1 md:grid-cols-2 gap-8">' + '\n'.join(sections) + '</div>'
    block = '\n'.join([
      '<!-- articles-index:start -->',
      '<section class="max-w-7xl mx-auto px-6 py-14">',
      '  <div class="rounded-[2rem] border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-8 md:p-12">',
      '    <div class="text-center mb-6">',
      '      <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-bold uppercase tracking-wider">',
      '        <span class="material-symbols-outlined text-sm">library_books</span>',
      '        Editorial Articles',
      '      </span>',
      '    </div>',
      '    <h2 class="text-2xl md:text-3xl font-extrabold text-center mb-6">Explore our articles</h2>',
      grid,
      '  </div>',
      '</section>',
      '<!-- articles-index:end -->'
    ])
    # Replace if exists, else append before final CTA or before footer
    if '<!-- articles-index:start -->' in html:
        html = re.sub(r'<!-- articles-index:start -->[\s\S]*?<!-- articles-index:end -->', block, html)
    else:
        html = re.sub(r'(</section>\s*</section>|</footer>)', block + '\n\1', html, count=1)
    p.write_text(html, encoding='utf-8')

def main():
    created = ensure_articles()
    print('Created', len(created), 'articles')
    for c in created: print('-', c)
    update_resources()
    print('resources.html updated with articles index')

if __name__ == '__main__':
    main()

