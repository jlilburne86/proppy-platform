#!/usr/bin/env python3
"""
Proppy Article Generator
Dynamically generates article listings for resources.html from markdown files.
Only includes articles with publish_status: published
"""

import os
import yaml
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Configuration
ARTICLES_DIR = Path(__file__).parent.parent / "articles"
RESOURCES_TEMPLATE = Path(__file__).parent.parent / "resources.html"
OUTPUT_FILE = Path(__file__).parent.parent / "resources.html"

# Category color mapping
CATEGORY_COLORS = {
    "Market Trends": {"text": "text-orange-500", "bg": "bg-orange-50 dark:bg-orange-900/30"},
    "Suburb Profiles": {"text": "text-green-600", "bg": "bg-green-50 dark:bg-green-900/30"},
    "Strategy": {"text": "text-purple-500", "bg": "bg-purple-50 dark:bg-purple-900/30"},
    "Cycles": {"text": "text-blue-500", "bg": "bg-blue-50 dark:bg-blue-900/30"},
    "Case Studies": {"text": "text-pink-500", "bg": "bg-pink-50 dark:bg-pink-900/30"},
    "Risk": {"text": "text-red-500", "bg": "bg-red-50 dark:bg-red-900/30"},
}

def extract_frontmatter(content: str) -> Dict[str, Any]:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}

def get_published_articles() -> List[Dict[str, Any]]:
    """Scan articles directory and return list of published articles."""
    articles = []

    if not ARTICLES_DIR.exists():
        print(f"Warning: Articles directory not found: {ARTICLES_DIR}")
        return articles

    for md_file in ARTICLES_DIR.glob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8')
            frontmatter = extract_frontmatter(content)

            # Only include published articles
            if frontmatter.get('publish_status') != 'published':
                continue

            # Extract slug from filename
            slug = md_file.stem

            articles.append({
                'slug': slug,
                'title': frontmatter.get('title', slug.replace('-', ' ').title()),
                'description': frontmatter.get('description', ''),
                'category': frontmatter.get('category', 'Strategy'),
                'reading_time': frontmatter.get('reading_time', '7 min'),
                'audience': frontmatter.get('audience', 'Both'),
            })
        except Exception as e:
            print(f"Error processing {md_file.name}: {e}")

    return sorted(articles, key=lambda x: x['title'])

def generate_article_card(article: Dict[str, Any]) -> str:
    """Generate HTML for a single article card."""
    category = article['category']
    colors = CATEGORY_COLORS.get(category, CATEGORY_COLORS['Strategy'])

    return f"""<article class="bg-card-light dark:bg-card-dark rounded-[2.5rem] p-2 border border-slate-100 dark:border-slate-800 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 group flex flex-col h-full">
  <div class="card-thumb">
    <img src="https://source.unsplash.com/600x360/?australia,property,investment" alt="{article['title']}" loading="lazy" decoding="async"/>
  </div>
  <div class="px-4 pb-6 flex flex-col flex-grow">
    <div class="flex items-center gap-3 mb-3 mt-4">
      <span class="text-[10px] font-bold uppercase tracking-wider {colors['text']} {colors['bg']} px-2 py-1 rounded-md">{category}</span>
      <span class="text-xs text-slate-400">{article['reading_time']}</span>
    </div>
    <h3 class="text-xl font-bold mb-3 group-hover:{colors['text']} transition-colors">{article['title']}</h3>
    <p class="text-slate-500 dark:text-slate-400 text-sm mb-4 line-clamp-3">
      {article['description']}
    </p>
    <div class="mt-auto">
      <a href="articles/{article['slug']}.html" class="inline-flex items-center gap-2 font-semibold {colors['text']} hover:gap-3 transition-all">
        Read Article
        <span class="material-symbols-outlined text-sm">arrow_forward</span>
      </a>
    </div>
  </div>
</article>"""

def generate_articles_grid(articles: List[Dict[str, Any]]) -> str:
    """Generate the complete articles grid HTML."""
    if not articles:
        return """<div class="text-center py-16">
      <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 text-sm font-semibold mb-4">
        <span class="material-symbols-outlined text-sm">edit_note</span>
        Coming Soon
      </div>
      <h2 class="text-2xl font-bold mb-3">Articles in production</h2>
      <p class="text-slate-600 dark:text-slate-400 max-w-md mx-auto">
        We're crafting data-led market analysis and investment guides. Subscribe below to be notified when they launch.
      </p>
    </div>"""

    cards_html = '\n'.join(generate_article_card(article) for article in articles)

    return f"""<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
{cards_html}
</div>

<div class="mt-12 text-center">
  <p class="text-slate-600 dark:text-slate-400">{len(articles)} article{'s' if len(articles) != 1 else ''} published</p>
</div>"""

def generate_category_index(articles: List[Dict[str, Any]]) -> str:
    """Generate the category index section."""
    categories = {}
    for article in articles:
        cat = article['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(article)

    category_map = {
        "Market Trends": "Market Trends & Analysis",
        "Suburb Profiles": "Suburb & Regional Profiles",
        "Strategy": "Investment Strategy (Educational)",
        "Cycles": "Property Cycles & Timing",
        "Case Studies": "Real Investor Case Studies",
        "Risk": "Risk, Regulation & Market Reality",
    }

    sections = []
    for cat_key, cat_display in category_map.items():
        cat_articles = categories.get(cat_key, [])
        if cat_articles:
            items_html = '\n'.join(
                f'<li><a href="/articles/{a["slug"]}.html" class="text-slate-600 dark:text-slate-400 hover:text-primary transition-colors">{a["title"]}</a></li>'
                for a in cat_articles
            )
            sections.append(f"""<div>
  <h3 id="pillar-{cat_key.lower().replace(' ', '-')}" class="text-lg font-bold mb-2">{cat_display}</h3>
  <ul class="list-disc pl-5 space-y-1">
{items_html}
  </ul>
</div>""")
        else:
            sections.append(f"""<div>
  <h3 id="pillar-{cat_key.lower().replace(' ', '-')}" class="text-lg font-bold mb-2">{cat_display}</h3>
  <ul class="list-disc pl-5 space-y-1">
    <li class="text-slate-400">Coming soon</li>
  </ul>
</div>""")

    return '\n'.join(sections)

def update_resources_page(articles: List[Dict[str, Any]]):
    """Update resources.html with generated article content."""
    if not RESOURCES_TEMPLATE.exists():
        print(f"Error: Template not found: {RESOURCES_TEMPLATE}")
        return

    template_content = RESOURCES_TEMPLATE.read_text(encoding='utf-8')

    # Generate content
    articles_grid = generate_articles_grid(articles)
    category_index = generate_category_index(articles)

    # Find insertion point (after hero section, before CTA section)
    # Look for the "Articles Grid" comment
    grid_marker = "<!-- Articles Grid - Will be populated dynamically -->"
    index_marker = "<!-- articles-index:start -->"

    if grid_marker in template_content:
        # Replace placeholder with actual grid
        parts = template_content.split(grid_marker)
        if len(parts) == 2:
            # Find the end of the section (next </div>)
            end_idx = parts[1].find('<!-- CTA Section -->')
            if end_idx != -1:
                new_content = (
                    parts[0] +
                    f"<!-- Articles Grid -->\n  <div class=\"max-w-7xl mx-auto px-6 mb-16\">\n{articles_grid}\n  </div>\n\n  " +
                    parts[1][end_idx:]
                )
                template_content = new_content

    # Update category index if marker exists
    if index_marker in template_content and '<!-- articles-index:end -->' in template_content:
        start_idx = template_content.find(index_marker)
        end_idx = template_content.find('<!-- articles-index:end -->') + len('<!-- articles-index:end -->')

        new_index_section = f"""{index_marker}
<section class="max-w-7xl mx-auto px-6 py-14">
  <div class="rounded-[2rem] border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-8 md:p-12">
    <div class="text-center mb-6">
      <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-bold uppercase tracking-wider">
        <span class="material-symbols-outlined text-sm">library_books</span>
        Editorial Articles
      </span>
    </div>
    <h2 class="text-2xl md:text-3xl font-extrabold text-center mb-6">Explore our articles</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
{category_index}
    </div>
  </div>
</section>
<!-- articles-index:end -->"""

        template_content = template_content[:start_idx] + new_index_section + template_content[end_idx:]

    # Write updated content
    OUTPUT_FILE.write_text(template_content, encoding='utf-8')
    print(f"✅ Generated {len(articles)} published articles in resources.html")

def main():
    """Main execution function."""
    print("🔍 Scanning for published articles...")
    articles = get_published_articles()

    if not articles:
        print("⚠️  No published articles found. Articles must have 'publish_status: published' in frontmatter.")
    else:
        print(f"✅ Found {len(articles)} published article(s)")

    print("📝 Updating resources.html...")
    update_resources_page(articles)
    print("✅ Done!")

if __name__ == "__main__":
    main()
