#!/usr/bin/env python3
import os, re, json, time
import xml.etree.ElementTree as ET
from urllib.parse import urljoin

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SITE_CFG = os.path.join(ROOT, 'data', 'site.json')
ARTICLES_XML = os.path.join(ROOT, 'articles.xml')


def load_site_url():
    site_url = 'https://proppy.com.au/'
    try:
        with open(SITE_CFG, 'r', encoding='utf-8') as f:
            data = json.load(f)
            site_url = (data.get('site_url') or site_url).rstrip('/') + '/'
    except Exception:
        pass
    return site_url


def load_article_filenames(site_url: str):
    files = set()
    if not os.path.exists(ARTICLES_XML):
        return files
    try:
        tree = ET.parse(ARTICLES_XML)
        root = tree.getroot()
        for link in root.findall('.//link'):
            url = (link.text or '').strip()
            if not url:
                continue
            if url.startswith(site_url):
                path = url[len(site_url):]
            else:
                # If relative or different base, just take tail after last '/'
                path = url.split('/')[-1]
            if path:
                files.add(path)
    except Exception:
        pass
    return files


def text_between_tags(html, tag):
    m = re.search(rf'<{tag}[^>]*>([\s\S]*?)</{tag}>', html, re.I)
    return (m.group(1).strip() if m else '')


def extract_first_img(html):
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.I)
    return m.group(1) if m else ''


def inject_schema(html, block):
    marker = '<script type="application/ld+json" data-auto="1">'
    if marker in html:
        return re.sub(r'<script type="application/ld\+json" data-auto="1">[\s\S]*?</script>', block, html, count=1, flags=re.I)
    return re.sub(r'</body>', block + '\n</body>', html, count=1, flags=re.I)


def main():
    site_url = load_site_url()
    article_files = load_article_filenames(site_url)
    changed = 0
    for name in os.listdir(ROOT):
        if not name.endswith('.html'):
            continue
        path = os.path.join(ROOT, name)
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()

        # Determine page URL and name
        loc = site_url if name == 'index.html' else urljoin(site_url, name)
        h1 = text_between_tags(html, 'h1')
        title = text_between_tags(html, 'title')
        page_name = h1 or title or name.replace('.html','')

        # Breadcrumbs JSON-LD (Home -> Current)
        breadcrumb = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type":"ListItem","position":1,"item":{"@id": site_url.rstrip('/'), "name":"Home"}},
                {"@type":"ListItem","position":2,"item":{"@id": loc, "name": page_name}}
            ]
        }

        blocks = [breadcrumb]

        # Article schema for known article files
        if name in article_files:
            img = extract_first_img(html)
            if img:
                if img.startswith('/'):
                    img = urljoin(site_url, img.lstrip('/'))
                elif not (img.startswith('http://') or img.startswith('https://')):
                    img = urljoin(loc, img)
            # Dates from file mtime
            try:
                st = os.stat(path)
                dt = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(st.st_mtime))
            except Exception:
                dt = None
            article = {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": page_name[:110],
                "mainEntityOfPage": loc,
                "author": {"@type": "Organization", "name": "Proppy"},
                "publisher": {"@type": "Organization", "name": "Proppy"},
            }
            if dt:
                article["datePublished"] = dt
                article["dateModified"] = dt
            if img:
                article["image"] = [img]
            blocks.append(article)

        block = '<script type="application/ld+json" data-auto="1">' + json.dumps(blocks, ensure_ascii=False) + '</script>'
        new_html = inject_schema(html, block)
        if new_html != html:
            with open(path, 'w', encoding='utf-8') as w:
                w.write(new_html)
            changed += 1
    print(f'Injected JSON-LD into {changed} pages')


if __name__ == '__main__':
    main()
