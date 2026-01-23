#!/usr/bin/env python3
"""
Convert Proppy markdown articles to HTML pages
Generates clean, SEO-optimized article pages with site navigation
"""

import os
import re
import yaml
import markdown
from pathlib import Path
from datetime import datetime

# Configuration
ARTICLES_DIR = Path(__file__).parent.parent / "articles"
OUTPUT_DIR = ARTICLES_DIR

# Category color mapping
CATEGORY_COLORS = {
    "Market Trends": "orange",
    "Suburb Profiles": "green",
    "Strategy": "purple",
    "Cycles": "blue",
    "Case Studies": "pink",
    "Risk": "red",
}

def extract_frontmatter(content: str):
    """Extract YAML frontmatter and markdown body."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return {}, content
    try:
        frontmatter = yaml.safe_load(match.group(1)) or {}
        body = match.group(2)
        return frontmatter, body
    except yaml.YAMLError:
        return {}, content

def markdown_to_html(md_content: str) -> str:
    """Convert markdown to HTML with extensions."""
    md = markdown.Markdown(extensions=[
        'extra',
        'codehilite',
        'toc',
        'tables',
        'fenced_code',
        'nl2br',
        'sane_lists'
    ])
    html = md.convert(md_content)

    # Remove first H1 from markdown (template already has display H1)
    html = re.sub(r'<h1[^>]*>.*?</h1>\s*', '', html, count=1, flags=re.DOTALL)

    return html

def generate_article_html(slug: str, frontmatter: dict, html_content: str) -> str:
    """Generate complete HTML page for article."""

    title = frontmatter.get('title', slug.replace('-', ' ').title())
    description = frontmatter.get('description', '')

    # Handle category as list or string
    category_raw = frontmatter.get('category', 'Strategy')
    category = category_raw[0] if isinstance(category_raw, list) else category_raw

    reading_time = frontmatter.get('reading_time', '7 min')

    # Handle audience as list or string
    audience_raw = frontmatter.get('audience', 'Both')
    audience = audience_raw[0] if isinstance(audience_raw, list) else audience_raw
    author = frontmatter.get('author', 'Proppy Editorial')

    # Get category color
    color = CATEGORY_COLORS.get(category, 'purple')

    # Format date
    pub_date = datetime.now().strftime('%d %b %Y')

    html = f'''<!DOCTYPE html>
<html class="scroll-smooth" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{title} - Proppy</title>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,typography"></script>
<script>
  tailwind.config = {{
    darkMode: 'class',
    theme: {{
      extend: {{
        fontFamily: {{
          sans: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif']
        }},
        colors: {{
          primary: '#8b5cf6',
          'background-light': '#ffffff',
          'background-dark': '#0f172a'
        }}
      }}
    }}
  }}
</script>
<link rel="canonical" href="/articles/{slug}.html">
<meta name="description" content="{description}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Proppy">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="/assets/screenshots/platform-screenshot.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="/assets/screenshots/platform-screenshot.png">
<script id="navx-script" src="../tools/navx-accessible.js"></script>
<link rel="stylesheet" href="../tools/ux.css"/>
<script src="../tools/analytics.js"></script>
<style>
  main h1 {{
    font-size: 2.25rem;
    font-weight: 800;
    margin-top: 2rem;
    margin-bottom: 1.5rem;
    color: #0f172a;
    line-height: 1.2;
  }}
  .dark main h1 {{
    color: #f1f5f9;
  }}
  main h2 {{
    font-size: 1.875rem;
    font-weight: 800;
    margin-top: 2.5rem;
    margin-bottom: 1.25rem;
    color: #0f172a;
    line-height: 1.2;
  }}
  .dark main h2 {{
    color: #f1f5f9;
  }}
  main h3 {{
    font-size: 1.5rem;
    font-weight: 700;
    margin-top: 2rem;
    margin-bottom: 1rem;
    color: #1e293b;
  }}
  .dark main h3 {{
    color: #e2e8f0;
  }}
  main p {{
    font-size: 1.125rem;
    line-height: 1.75;
    margin-bottom: 1.25rem;
    color: #475569;
  }}
  .dark main p {{
    color: #cbd5e1;
  }}
  main strong {{
    font-weight: 700;
    color: #1e293b;
  }}
  .dark main strong {{
    color: #f1f5f9;
  }}
  main ul, main ol {{
    margin-top: 1.25rem;
    margin-bottom: 1.25rem;
    padding-left: 1.75rem;
    font-size: 1.125rem;
    line-height: 1.75;
    color: #475569;
  }}
  .dark main ul, .dark main ol {{
    color: #cbd5e1;
  }}
  main li {{
    margin-bottom: 0.75rem;
  }}
  main blockquote {{
    border-left: 4px solid #8b5cf6;
    padding-left: 1.5rem;
    font-style: italic;
    color: #64748b;
    margin: 2rem 0;
    font-size: 1.125rem;
  }}
  .dark main blockquote {{
    color: #94a3b8;
  }}
  main a {{
    color: #8b5cf6;
    text-decoration: underline;
    transition: color 0.2s;
  }}
  main a:hover {{
    color: #7c3aed;
  }}
  .not-prose h1 {{
    color: #0f172a !important;
  }}
  .dark .not-prose h1 {{
    color: #f1f5f9 !important;
  }}
</style>
</head>
<body class="bg-background-light dark:bg-background-dark text-slate-900 dark:text-slate-100 font-sans">
<a href="#content" class="skip-link">Skip to content</a>
<nav class="fixed top-0 w-full z-50 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800">
  <div class="max-w-7xl mx-auto px-4 md:px-6 h-16 md:h-20 flex items-center justify-between">
    <div class="flex items-center gap-3">
      <a href="../index.html" class="inline-flex items-center gap-2" aria-label="Proppy home">
        <img src="../proppy%20mobile%20icon.png" alt="Proppy" class="h-7 w-7 md:hidden"/>
        <img src="../proppy-logo.png" alt="Proppy" class="hidden md:block h-8 md:h-9 w-auto"/>
        <span class="sr-only">Proppy</span>
      </a>
    </div>
    <div class="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600 dark:text-slate-400">
      <a class="hover:text-primary transition-colors" href="../index.html">Home</a>
<div class="navx-group relative">
  <a class="navx-toggle hover:text-primary transition-colors" href="../how-it-works.html" role="button" aria-expanded="false">How It Works</a>
  <div class="navx-sub absolute left-0 mt-2 hidden group-hover:block bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl shadow-lg min-w-[220px] p-2 z-50">
    <a href="../how-it-works.html" class="block px-4 py-2 rounded hover:bg-slate-100 dark:hover:bg-slate-800">How It Works</a>
<a href="../technology.html" class="block px-4 py-2 rounded hover:bg-slate-100 dark:hover:bg-slate-800">Technology</a>
  </div>
</div>
<div class="navx-group relative">
  <a class="navx-toggle hover:text-primary transition-colors" href="javascript:void(0)" role="button" aria-expanded="false">Solutions</a>
  <div class="navx-sub absolute left-0 mt-2 hidden group-hover:block bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl shadow-lg min-w-[220px] p-2 z-50">
    <a href="../advantage.html" class="block px-4 py-2 rounded hover:bg-slate-100 dark:hover:bg-slate-800">Advantage</a>
<a href="../sourcing.html" class="block px-4 py-2 rounded hover:bg-slate-100 dark:hover:bg-slate-800">Sourcing</a>
<a href="../about.html" class="block px-4 py-2 rounded hover:bg-slate-100 dark:hover:bg-slate-800">About</a>
<a href="../team.html" class="block px-4 py-2 rounded hover:bg-slate-100 dark:hover:bg-slate-800">Team</a>
  </div>
</div>
<div class="navx-group relative">
  <a class="navx-toggle hover:text-primary transition-colors" href="javascript:void(0)" role="button" aria-expanded="false">Success</a>
  <div class="navx-sub absolute left-0 mt-2 hidden group-hover:block bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl shadow-lg min-w-[220px] p-2 z-50">
    <a href="../results.html" class="block px-4 py-2 rounded hover:bg-slate-100 dark:hover:bg-slate-800">Results</a>
<a href="../guarantee.html" class="block px-4 py-2 rounded hover:bg-slate-100 dark:hover:bg-slate-800">Guarantee</a>
  </div>
</div>
<a class="hover:text-primary transition-colors" href="../resources.html">Resources</a>
<div class="navx-group relative">
  <a class="navx-toggle hover:text-primary transition-colors" href="javascript:void(0)" role="button" aria-expanded="false">Get Started</a>
  <div class="navx-sub absolute left-0 mt-2 hidden group-hover:block bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl shadow-lg min-w-[220px] p-2 z-50">
    <a href="../pricing.html" class="block px-4 py-2 rounded hover:bg-slate-100 dark:hover:bg-slate-800">Pricing</a>
<a href="../book.html" class="block px-4 py-2 rounded hover:bg-slate-100 dark:hover:bg-slate-800">Book</a>
<a href="../contact.html" class="block px-4 py-2 rounded hover:bg-slate-100 dark:hover:bg-slate-800">Contact</a>
  </div>
</div>
    </div>
    <div class="flex items-center gap-3">
      <a href="../book.html" class="hidden md:inline-flex px-5 py-2.5 text-sm font-semibold text-white bg-slate-900 dark:bg-white dark:text-slate-900 rounded-full hover:shadow-lg transition-all">Get Started</a>
      <button id="navx-burger" class="md:hidden inline-flex items-center justify-center w-10 h-10 rounded-lg border border-slate-300 dark:border-slate-700">
        <span class="material-symbols-outlined">menu</span>
      </button>
    </div>
  </div>
  <div class="fixed inset-0 navx-overlay bg-black/40 hidden"></div>
  <div class="fixed right-0 top-0 h-full w-80 max-w-[85vw] navx-drawer bg-white dark:bg-slate-900 border-l border-slate-200 dark:border-slate-800 p-4 hidden">
    <div class="flex items-center justify-between mb-2">
      <a href="../index.html" class="inline-flex items-center gap-2" aria-label="Proppy home">
        <img src="../proppy%20mobile%20icon.png" alt="Proppy" class="h-6 w-6"/>
      </a>
      <button id="navx-close" class="w-10 h-10 rounded-lg border border-slate-300 dark:border-slate-700 inline-flex items-center justify-center">
        <span class="material-symbols-outlined">close</span>
      </button>
    </div>
    <ul class="text-slate-700 dark:text-slate-300"><li class="border-b border-slate-200 dark:border-slate-800"><a class="block py-3 font-semibold" href="../index.html">Home</a></li>
<li class="border-b border-slate-200 dark:border-slate-800">
<button class="navx-acc w-full flex items-center justify-between py-3 text-left font-semibold">How It Works<span class="material-symbols-outlined text-base">expand_more</span></button>
<ul class="navx-acc-body hidden pl-3 pb-3">
<li><a class="block py-2" href="../how-it-works.html">How It Works</a></li>
<li><a class="block py-2" href="../technology.html">Technology</a></li>
</ul>
</li>
<li class="border-b border-slate-200 dark:border-slate-800">
<button class="navx-acc w-full flex items-center justify-between py-3 text-left font-semibold">Solutions<span class="material-symbols-outlined text-base">expand_more</span></button>
<ul class="navx-acc-body hidden pl-3 pb-3">
<li><a class="block py-2" href="../advantage.html">Advantage</a></li>
<li><a class="block py-2" href="../sourcing.html">Sourcing</a></li>
<li><a class="block py-2" href="../about.html">About</a></li>
<li><a class="block py-2" href="../team.html">Team</a></li>
</ul>
</li>
<li class="border-b border-slate-200 dark:border-slate-800">
<button class="navx-acc w-full flex items-center justify-between py-3 text-left font-semibold">Success<span class="material-symbols-outlined text-base">expand_more</span></button>
<ul class="navx-acc-body hidden pl-3 pb-3">
<li><a class="block py-2" href="../results.html">Results</a></li>
<li><a class="block py-2" href="../guarantee.html">Guarantee</a></li>
</ul>
</li>
<li class="border-b border-slate-200 dark:border-slate-800"><a class="block py-3 font-semibold" href="../resources.html">Resources</a></li>
<li class="border-b border-slate-200 dark:border-slate-800">
<button class="navx-acc w-full flex items-center justify-between py-3 text-left font-semibold">Get Started<span class="material-symbols-outlined text-base">expand_more</span></button>
<ul class="navx-acc-body hidden pl-3 pb-3">
<li><a class="block py-2" href="../pricing.html">Pricing</a></li>
<li><a class="block py-2" href="../book.html">Book</a></li>
<li><a class="block py-2" href="../contact.html">Contact</a></li>
</ul>
</li>
</ul>
<div class="mt-6"><a href="../book.html" class="block px-5 py-3 text-sm text-center font-semibold text-white bg-slate-900 dark:bg-white dark:text-slate-900 rounded-full">Get Started</a></div>
  </div>
</nav>

<main id="content" class="max-w-3xl mx-auto px-6 pt-28 pb-16">
<nav aria-label="Breadcrumb" class="text-sm text-slate-500 dark:text-slate-400 mb-4 not-prose">
  <ol class="flex items-center gap-2">
    <li><a class="hover:underline" href="../index.html">Home</a></li>
    <li>›</li>
    <li><a class="hover:underline" href="../resources.html">Resources</a></li>
    <li>›</li>
    <li>{category}</li>
  </ol>
</nav>

<div class="not-prose mb-8">
  <div class="flex items-center gap-3 mb-4">
    <span class="text-[10px] font-bold uppercase tracking-wider text-{color}-500 bg-{color}-50 dark:bg-{color}-900/30 px-3 py-1.5 rounded-md">{category}</span>
    <span class="text-sm text-slate-400">{reading_time}</span>
  </div>
  <h1 class="text-4xl md:text-5xl font-extrabold mb-4 leading-tight">{title}</h1>
  <div class="flex flex-wrap items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
    <span>By {author}</span>
    <span>•</span>
    <span>{pub_date}</span>
    <span>•</span>
    <span>{audience}</span>
  </div>
</div>

{html_content}

<div class="not-prose mt-12 pt-8 border-t border-slate-200 dark:border-slate-800">
  <div class="flex items-center justify-between flex-wrap gap-4">
    <a href="../resources.html" class="inline-flex items-center gap-2 text-primary font-semibold hover:gap-3 transition-all">
      <span class="material-symbols-outlined text-sm">arrow_back</span>
      Back to Resources
    </a>
    <a href="../book.html" class="inline-flex items-center gap-2 px-5 py-2.5 bg-primary text-white rounded-full font-semibold hover:shadow-lg transition-all">
      Book a Free Call
      <span class="material-symbols-outlined text-sm">arrow_forward</span>
    </a>
  </div>
</div>
</main>

<footer class="py-12 border-t border-slate-200 dark:border-slate-800 mt-12">
  <div class="max-w-7xl mx-auto px-6">
    <div class="flex flex-col md:flex-row justify-between items-center gap-8">
      <div class="flex items-center gap-3">
        <span class="text-xl font-extrabold uppercase tracking-tight">Proppy</span>
        <span class="text-slate-400 text-sm">© 2024 Proppy Inc. All rights reserved.</span>
      </div>
      <div class="flex gap-8 text-sm font-semibold text-slate-500 dark:text-slate-400">
        <a class="hover:text-primary transition-colors" href="../privacy.html">Privacy Policy</a>
        <a class="hover:text-primary transition-colors" href="../terms.html">Terms of Service</a>
        <a class="hover:text-primary transition-colors" href="../site-map.html">Site Map</a>
      </div>
    </div>
  </div>
</footer>

</body></html>'''

    return html

def convert_article(md_file: Path):
    """Convert a single markdown article to HTML."""
    slug = md_file.stem
    html_file = OUTPUT_DIR / f"{slug}.html"

    # Skip if HTML already exists and is newer than markdown
    if html_file.exists() and html_file.stat().st_mtime > md_file.stat().st_mtime:
        return False

    try:
        content = md_file.read_text(encoding='utf-8')
        frontmatter, md_body = extract_frontmatter(content)

        # Only convert published articles
        if frontmatter.get('publish_status') != 'published':
            return False

        # Convert markdown to HTML
        html_content = markdown_to_html(md_body)

        # Generate full HTML page
        full_html = generate_article_html(slug, frontmatter, html_content)

        # Write HTML file
        html_file.write_text(full_html, encoding='utf-8')
        return True
    except Exception as e:
        print(f"Error converting {md_file.name}: {e}")
        return False

def main():
    """Convert all markdown articles to HTML."""
    if not ARTICLES_DIR.exists():
        print(f"Error: Articles directory not found: {ARTICLES_DIR}")
        return

    print("🔄 Converting markdown articles to HTML...")
    converted = 0
    skipped = 0

    for md_file in sorted(ARTICLES_DIR.glob("*.md")):
        if convert_article(md_file):
            print(f"✅ {md_file.stem}")
            converted += 1
        else:
            skipped += 1

    print(f"\n✅ Converted {converted} articles")
    if skipped > 0:
        print(f"⏭  Skipped {skipped} articles (already up-to-date or not published)")

if __name__ == "__main__":
    main()
