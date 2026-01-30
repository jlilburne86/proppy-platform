#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

python3 tools/wire_highlevel.py
python3 tools/inject_highlevel_snippet.py
python3 tools/inject_breadcrumbs_and_article_schema.py
python3 tools/normalize_titles.py
python3 tools/generate_sitemap_xml.py

echo "SEO pipeline complete."

