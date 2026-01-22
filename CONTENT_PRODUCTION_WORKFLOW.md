# Proppy Content Production Workflow

## Overview

This document outlines the standardized workflow for producing high-quality, data-led property investment articles that align with the **PROPPY MASTER ARTICLE PROMPT** standards.

---

## 🎯 Quality Standards

Every article must:
- Be 1,000–1,500 words
- Include real Australian market data (CoreLogic, PropTrack, ABS, RBA)
- Contain the mandatory **🔍 Proppy Data Lens** section
- Maintain a calm, analytical, evidence-led tone
- Balance opportunity and risk
- Read like professional market analysis (comparable to CoreLogic research or AFR property coverage)

---

## 📋 Production Stages

### Stage 1: Topic Selection & Research (30-45 min)

**Inputs:**
- Editorial calendar
- Trending market topics
- Investor questions from client calls
- Data releases from CoreLogic, PropTrack, ABS

**Process:**
1. Select topic from approved content calendar
2. Identify category (Market Trends, Suburb Profiles, Strategy, Cycles, Case Studies, or Risk)
3. Define target audience (Beginner, Experienced, or Both)
4. Gather data sources:
   - CoreLogic monthly reports
   - PropTrack vacancy & rental data
   - ABS migration and dwelling approval figures
   - RBA statements and financial stability reviews
   - State planning infrastructure announcements

**Output:**
- Topic brief with 3-5 key data points
- Outline of H2 sections
- List of sources to cite

---

### Stage 2: Article Structure & Outline (15-20 min)

**Template Checklist:**
```markdown
---
title: ""
description: "" (150-160 characters)
category: [Market Trends | Suburb Profiles | Strategy | Cycles | Case Studies | Risk]
audience: [Beginner | Experienced | Both]
reading_time: ""
publish_status: draft
author: "Proppy Editorial"
owner: "editor@proppy.com.au"
next_review_date: ""
sources:
  - name: ""
    url: ""
version: 1
---

# [Title]

[Standfirst: 2-3 sentences - What, Why, Who]

## Market Context
- National/regional backdrop
- Economic/housing conditions
- Reference datasets with timeframes

## Key Drivers
- Multiple factors (supply/demand, migration, rates, etc.)
- Each with data point + timeframe

## What the Data Shows
- Structured evidence
- Comparative figures (capital vs regional, state vs state)
- Historical ranges (5-, 10-, 20-year context)

## 🔍 Proppy Data Lens
[MANDATORY - Explain multi-signal analysis, pattern recognition, signal divergence]

## Expert Insight
- Paraphrased/quoted commentary
- Clear attribution (CoreLogic, RBA, economists)
- Separation of data vs interpretation

## Investor Lens

### For Newer Investors
- Fundamentals focus
- Understanding cycles/trade-offs

### For Experienced Investors
- Diversification, volatility, liquidity, timing
- Long-term patterns

## Risks & Considerations
- Quantified risks (not vague)
- Volatility comparisons
- Historical/relative framing

## Practical Checklist
[Optional: actionable steps]

## Key Takeaways
- 3-5 concise, neutral insights
- Reference timeframes
- Highlight trade-offs
- Avoid recommendations

> Disclaimer: [Standard disclaimer text]
```

**Output:**
- Completed outline with section headers
- Bullet points for each section

---

### Stage 3: First Draft (60-90 min)

**Writing Rules:**
✅ Use cautious, analytical phrasing
✅ Attribute opinions clearly
✅ Quantify where possible
✅ Explain why, not just what

❌ No hype ("booms", "guaranteed returns")
❌ No personal advice
❌ No predictions framed as certainty
❌ No promotional language

**Data Integration Examples:**

**Poor:**
> "Brisbane is growing fast."

**Good:**
> "Between March 2020 and December 2023, CoreLogic reported Brisbane median house prices rose 42.7%, driven by interstate migration, sub-1% vacancy, and constrained supply."

**Poor:**
> "Interest rates matter."

**Good:**
> "Between May 2022 and November 2023, the RBA lifted the cash rate from 0.10% to 4.35%, reducing borrowing capacity by approximately 30% for median-income households."

**Output:**
- Complete first draft (1,000-1,500 words)
- All sections populated
- Data points cited with sources

---

### Stage 4: Data Verification & Citation (15-20 min)

**Checklist:**
- [ ] All figures cross-checked against original sources
- [ ] Timeframes specified (e.g., "2020-2023", "Q2 2023")
- [ ] Sources listed in YAML frontmatter
- [ ] No unsourced claims or estimates
- [ ] Attribution clear (CoreLogic vs PropTrack vs ABS)

**Output:**
- Verified draft with complete citations

---

### Stage 5: Quality Review (20-30 min)

**Self-Review Questions:**
1. Would this article still read well in 5+ years?
2. Does it sound like a research brief, not marketing?
3. Does it clearly reflect a data-driven platform?
4. Does it balance opportunity and risk?
5. Does it reinforce Proppy's authority?

**Specific Checks:**
- [ ] Contains **🔍 Proppy Data Lens** section
- [ ] Investor Lens split into Beginner/Experienced subsections
- [ ] Risks are quantified with comparisons
- [ ] No hype language
- [ ] No personal advice
- [ ] Standfirst explains what/why/who

**Output:**
- Polished draft ready for editorial review

---

### Stage 6: Editorial Review (15-20 min)

**Reviewer Checklist:**
- [ ] Tone matches Proppy standards (calm, analytical)
- [ ] Data is accurate and properly cited
- [ ] **🔍 Proppy Data Lens** is present and substantive
- [ ] Structure follows template
- [ ] Reading time matches content (estimate 200-250 words/min)
- [ ] No spelling/grammar errors

**Feedback Loop:**
- Minor edits: apply directly
- Major structural issues: return to writer with notes

**Output:**
- Approved final draft

---

### Stage 7: Publishing (5-10 min)

**Process:**
1. Update frontmatter:
   ```yaml
   publish_status: published
   next_review_date: [6 months from publish date]
   ```

2. Run article generator:
   ```bash
   cd /Users/boo2/Desktop/proppy
   source .venv/bin/activate
   python3 tools/generate-articles.py
   ```

3. Verify article appears on resources.html
4. Test link `/articles/[slug].html`

**Output:**
- Article live on site
- Category index updated
- RSS feed updated (if applicable)

---

## 📊 Production Metrics

**Target Output:**
- 2-4 flagship articles per month (1,000-1,500 words each)
- 8-12 articles per month at steady state

**Time Budget (per article):**
- Research: 30-45 min
- Outline: 15-20 min
- First draft: 60-90 min
- Verification: 15-20 min
- Review: 20-30 min
- Editorial: 15-20 min
- Publishing: 5-10 min

**Total: ~3.5-4 hours per article**

---

## 🔄 Quarterly Review Process

Every 3 months:
1. Audit published articles for data freshness
2. Update figures if significant market shifts have occurred
3. Increment version number in frontmatter
4. Update `next_review_date`

---

## 🛠️ Tools & Resources

**Data Sources (Bookmarked):**
- CoreLogic Monthly Charts: https://www.corelogic.com.au/news-research/reports
- PropTrack Insights: https://www.proptrack.com.au/insights/
- ABS Housing Data: https://www.abs.gov.au/statistics/economy/finance
- RBA Statements: https://www.rba.gov.au/publications/

**Templates:**
- Master article template: `/Users/boo2/Desktop/proppy/PROPPY_MASTER_ARTICLE_PROMPT.md`
- Article generator script: `/Users/boo2/Desktop/proppy/tools/generate-articles.py`

**Style Guide:**
- Prefer Australian spelling (e.g., "analyse" not "analyze")
- Use en-dashes for ranges (e.g., "2020–2023")
- Date format: Month Year (e.g., "March 2023")
- Percentage format: "42.7%" (one decimal place)

---

## 📝 Editorial Calendar Template

| Month | Topic | Category | Audience | Data Sources | Status |
|-------|-------|----------|----------|--------------|--------|
| Jan 2026 | Melbourne vs Brisbane: 5-Year Outlook | Market Trends | Both | CoreLogic, PropTrack | Planned |
| Jan 2026 | First-Time Investor Mistakes | Strategy | Beginner | Industry case studies | Research |
| Feb 2026 | Regional NSW: Infrastructure Impact | Suburb Profiles | Both | ABS, State planning | Outlined |

---

## ✅ Quality Checklist (Final)

Before marking `publish_status: published`, confirm:

- [ ] 1,000-1,500 words
- [ ] Contains **🔍 Proppy Data Lens** section
- [ ] Real Australian data with sources
- [ ] Expert Insight with attribution
- [ ] Investor Lens split (Beginner/Experienced)
- [ ] Risks quantified
- [ ] Standfirst present
- [ ] Key Takeaways 3-5 points
- [ ] Disclaimer included
- [ ] No hype language
- [ ] No personal advice
- [ ] Reads like CoreLogic research, not marketing

---

**Last Updated:** 2026-01-22
**Owner:** Proppy Editorial Team
