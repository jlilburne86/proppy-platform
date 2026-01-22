# Proppy.com.au – Australian Property Investment Content Blueprint

**Author Persona:** Australian Property Investment Adviser with 30+ years industry experience  
**Audience:** Beginner & seasoned property investors (Australia-wide)  
**Tone:** Data-led, authoritative, balanced, educational (aligned with realestate.com.au/news)  
**Constraints:** No tax or personal financial advice. Use factual reporting, expert commentary, and market data only.

---

## 1. Editorial Philosophy

All content published on Proppy.com.au should:

- Be grounded in **verifiable Australian data** (CoreLogic, PropTrack, ABS, RBA, REA Group, state planning bodies)
- Avoid hype, predictions framed as guarantees, or speculative language
- Present **both opportunity and risk**
- Educate readers to make informed decisions, not sell outcomes
- Be written in plain English, accessible to beginners but respected by experienced investors

Each article should answer:
> *“What is happening in the market, why it matters, and what investors should think about next?”*

---

## 2. Standard Article Structure (Technical Spec)

All long-form articles should follow this structure:

### Front Matter
```yaml
title: ""
description: ""
category: [Market Trends | Suburb Profiles | Strategy | Cycles | Case Studies | Risk]
audience: [Beginner | Experienced | Both]
reading_time: "X min"
publish_status: draft
```

### Article Body

1. **Headline (H1)**  
   Clear, data-led, time-relevant

2. **Standfirst / Summary (2–3 sentences)**  
   Snapshot of the insight and relevance

3. **Market Context (H2)**  
   - National or regional overview  
   - Referenced data sources

4. **Key Drivers (H2)**  
   - Supply & demand  
   - Population & infrastructure  
   - Lending or buyer behaviour

5. **What the Data Shows (H2)**  
   - Bullet points or short paragraphs  
   - Comparisons across states or years

6. **Expert Insight (H2)**  
   - Quotes or paraphrased commentary from economists, analysts, buyers’ agents

7. **Investor Lens (H2)**  
   - What beginners should understand  
   - What experienced investors may consider

8. **Risks & Considerations (H2)**  
   - Market volatility  
   - Regulation or supply risks

9. **Key Takeaways (H2)**  
   - 3–5 neutral, practical insights

---

## 3. Content Pillars & Article Catalogue

### Pillar A: Market Trends & Analysis

1. Australia’s 2026 Housing Market Outlook: What the Data Is Signalling  
2. Capital Cities vs Regional Markets: Where Growth Has Shifted  
3. Interest Rates and Property: Lessons from Past RBA Cycles  
4. Rental Market Pressures Explained: Supply, Demand and Rents  
5. Investor Lending Trends Across Australia’s States  
6. Housing Supply vs Population Growth: Why Shortages Persist  
7. Which Capital Cities Are Leading — and Which Are Lagging  
8. Units vs Houses: How Performance Has Changed Over the Decade

---

### Pillar B: Suburb & Regional Profiles

9. Emerging Suburbs to Watch Heading into 2026  
10. Affordable Investment Areas Still Under the National Median  
11. Coastal Markets That Have Transformed Over the Past 10 Years  
12. Brisbane Growth Corridors: Ipswich, Logan and Moreton Bay  
13. Perth’s Recovery Story: Suburbs Benefiting from WA’s Economy  
14. Adelaide’s Quiet Achievers: Where Demand Is Outpacing Supply  
15. Melbourne’s Shifting Growth Pattern: Inner vs Outer Suburbs  
16. Tasmania’s Property Market Explained: Hobart vs Regional Areas

---

### Pillar C: Investment Strategy (Educational)

17. Capital Growth vs Rental Yield: Understanding the Trade-Offs  
18. Diversification in Property: Cities, States and Asset Types  
19. Buy-and-Hold Explained: Why Long-Term Investors Focus on Cycles  
20. Value-Add Strategies: Renovation, Layout and Usability Improvements  
21. First-Time Investor Guide: Market Fundamentals to Understand  
22. Rentvesting Explained: How Investors Separate Home and Portfolio  
23. Co-Ownership in Property: What the Data and Case Studies Show

---

### Pillar D: Property Cycles & Timing

24. Understanding the Australian Property Cycle  
25. Boom, Plateau or Decline? How to Read Market Signals  
26. Post-Pandemic Property Shifts: What Has Endured and What Hasn’t  
27. When Growth Slows: Historical Examples from Australian Cities  
28. Long-Term Price Growth: What 20-Year Data Reveals

---

### Pillar E: Real Investor Case Studies

29. From First Property to Portfolio: A Long-Term Investor Journey  
30. Regional Investing Case Study: Growth Outside Capital Cities  
31. Rentvesting in Practice: A Decade of Outcomes  
32. Using Equity to Expand a Portfolio: An Educational Example  
33. Lessons from Investors Who Bought Early in Growth Corridors

---

### Pillar F: Risk, Regulation & Market Reality

34. Regulatory Changes Affecting Australian Landlords  
35. Short-Term Rentals and Changing State Rules  
36. Climate Risk and Property: What Investors Should Know  
37. Vacancy Rates Explained: What Tight and Loose Markets Mean  
38. Market Downturns: How Australian Property Has Historically Responded  
39. Overconcentration Risk: Why One Market Is Rarely Enough

---

## 4. Referencing Standards

- Use **named sources** where possible (e.g. PropTrack, CoreLogic)
- Avoid specific forecasts presented as certainty
- Attribute opinions clearly: *“According to REA Group analysis…”*
- No personal recommendations, no numerical return promises

---

## 5. SEO & CMS Notes (for Codex Build)

- One H1 per article  
- Logical H2/H3 nesting  
- Schema-ready metadata fields  
- Evergreen URLs (no dates in slugs)  
- Internal linking across pillars

---

## 6. Brand Voice Summary

> Calm. Experienced. Evidence-led. Never alarmist. Never promotional.

The Proppy.com.au voice should feel like:
- A seasoned buyer’s advocate explaining markets over coffee
- An analyst translating complex data into practical insight
- A long-term investor who has seen multiple cycles

---

**End of Document**

---

## 7. Conversion & CTA Guidelines

- Primary CTA: “Book a Free Strategy Call” → link to `book.html`.  
  Placement: under Standfirst (top), mid-article (after “Investor Lens”), and end.
- Secondary CTAs: “See Results” (`results.html`), “How It Works” (`how-it-works.html`), “Guarantee” (`guarantee.html`).
- Lead magnets: In-depth suburb briefs; capture via newsletter form (Netlify Forms) with UTM retention.
- UTM conventions: `utm_source=content&utm_medium=article&utm_campaign=<slug>` appended on CTA links.

---

## 8. Editorial Workflow & Governance

- Roles: Author → Editor → Fact-check → Publish (CMS) → Distribution (newsletter/social).
- Pre-publish checklist:
  - Conflicts of interest declared (if any)
  - Data citations added with dates and links (ABS, RBA, PropTrack, CoreLogic, state bodies)
  - Risk section present and balanced
  - CTA placement verified (top/mid/end) and links tested
  - Accessibility: headings order, alt text, color contrast for charts
- Post-publish:
  - Add to Resources hub index with tags  
  - Annotate analytics (event names: `cta_book_click`, `newsletter_submit`)
  - Schedule refresh review (see Section 10)

---

## 9. Legal & Disclaimers

Include a short disclaimer footer on educational content:

> This article is general information only and does not constitute financial, taxation or legal advice. Consider your circumstances and seek professional advice before acting.

Avoid: individual recommendations, projected returns, or statements implying certainty.

---

## 10. Cadence, Refresh, and Ownership

- Cadence: 2 Market Trends, 1 Strategy, 1 Suburb Profile per fortnight.  
- Refresh policy: Review Market Trends every 90 days; Suburb Profiles every 6 months; Case Studies annually.  
- Ownership fields in CMS: `owner`, `next_review_date`, `sources` (array), `version`.

Example front matter extension:

```yaml
owner: "editor@proppy.com.au"
next_review_date: "2026-04-15"
sources:
  - name: "ABS"
    url: "https://www.abs.gov.au/"
  - name: "PropTrack"
    url: "https://www.proptrack.com.au/insights/"
version: 1
```

---

## 11. Data & Charting Standards

- Data snapshots must include the collection month/quarter and source.  
- Prefer YoY and 3/5/10-year comparisons; avoid cherry-picking single month moves.  
- Charts: label axes, show units (%, $), and add note for methodology if non-obvious.  
- Use AU English, AUD currency (`$700k`, `$1.2m`), dates `21 Jan 2026`.

---

## 12. Category & Tagging Framework

- Categories: Market Trends, Suburb Profiles, Strategy, Cycles, Case Studies, Risk.  
- Required tags (3–6): city/state (e.g., `VIC`, `QLD`), theme (`yield`, `growth`, `vacancy`), audience (`beginner`, `experienced`).  
- Add cross-links to pillar pages within the first 40% of the article.

---

## 13. Distribution Playbook

- Newsletter summary (80–120 words) with one chart and 1 deep link.  
- LinkedIn post: 2–3 bullets, insight-first, link at end; add `#ausproperty #investing`.  
- Syndication (optional): Medium or Substack; use canonical back to Proppy.  
- Internal: Add to Resources hub tiles with appropriate icon and tag color.

---

## 14. Short-Form “Market Note” Template (Under 600 words)

```yaml
title: "Market Note: <topic>"
description: "<one-sentence insight>"
category: [Market Trends]
audience: [Both]
reading_time: "3 min"
publish_status: draft
```

Structure:
- H1 + 2-sentence standfirst  
- 2–3 bullets: “What’s changed” (with data)  
- 1 paragraph: “Why it matters”  
- 2 bullets: “Investor lens” (beginner, experienced)  
- Risk note (1–2 lines)  
- CTA: “Book a Free Strategy Call” + “See Results”
