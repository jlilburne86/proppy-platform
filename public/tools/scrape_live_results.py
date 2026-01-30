#!/usr/bin/env python3
import re, json, sys
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'properties.json'

OUR_RESULTS_URL = 'https://proppy.com.au/our-results'
HDRS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15'}

def fetch(url):
    req = Request(url, headers=HDRS)
    with urlopen(req, timeout=30) as r:
        return r.read().decode('utf-8', errors='ignore')

def extract_cards(html):
    cards = []
    # Split by pr_container anchor blocks
    for m in re.finditer(r'<a class="pr_container" href="([^"]+)">(.+?)</a>', html, re.S):
        href, block = m.group(1), m.group(2)
        title = _text(re_search(r'<h2 class="pr_title">(.*?)</h2>', block))
        location = _text(re_search(r'<p class="pr_tags">(.*?)</p>', block))
        image_url = re_search(r'<div class="pr_featured-image">\s*<img[^>]+src="([^"]+)"', block) or re_search(r'<img[^>]+src="([^"]+)"', block)
        # features: match title span then following strong value
        feats = []
        for fi in re.finditer(r'<p class="pr_feature_title">.*?<span>(.*?)</span>.*?</p>\s*<strong class="pr_feature_value">\s*(.*?)\s*</strong>', block, re.S):
            label = _text(fi.group(1))
            value = _text(fi.group(2))
            if label and value:
                feats.append((label, value))
        cards.append({'href': href, 'title': title, 'location': location, 'image_url': image_url, 'features': feats})
    return cards

def _text(s):
    if s is None: return ''
    # remove tags and compress spaces
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def re_search(pat, s):
    m = re.search(pat, s, re.S)
    return m.group(1) if m else None

def map_feature_to_fields(features):
    data = {}
    for label, value in features:
        L = label.lower()
        if 'purchase price' in L:
            data['purchase_price'] = value
        elif 'capital growth over 3 years' in L:
            data['growth_3y'] = value
        elif 'rent per week' in L:
            data['rent'] = value
        elif 'rental growth over 3 years' in L:
            data['rental_growth_3y'] = value
    return data

def image_for(title, href):
    t = (title + ' ' + href).lower()
    # heuristics mapping keywords to existing assets
    if 'richmond' in t:
        return 'assets/properties/richmond-gem.jpg'
    if 'thornbury' in t:
        return 'assets/properties/thornbury-high-growth-strong-yield.jpg'
    if 'seaford' in t:
        return 'assets/properties/seaford-rare-block.jpg'
    if 'reservoir' in t and 'strong' in t:
        return 'assets/properties/reservoir-strong-rental-returns.jpg'
    if 'reservoir' in t:
        return 'assets/properties/reservoir-gem-cashflow.jpg'
    if 'albion' in t:
        return 'assets/properties/albion-capital-rental.jpg'
    if 'waterfront' in t:
        return 'assets/properties/hastings-waterfront-cottage.jpg'
    if 'morning' in t or 'coastal' in t or 'high-yield' in t:
        return 'assets/properties/hastings-high-yield.jpg'
    # fallback
    return 'assets/properties/hastings-high-growth-coastal-gem.jpg'

# ---- helpers ----
def _derive_tags(title):
    t = title.lower()
    tags = []
    if 'high-yield' in t or 'yield' in t:
        tags.append('High Yield')
    if 'high-growth' in t or 'growth' in t:
        tags.append('High Growth')
    if 'waterfront' in t or 'coast' in t:
        tags.append('Coastal')
    if 'inner' in t or 'richmond' in t or 'thornbury' in t:
        tags.append('Inner City')
    return tags

def _parse_money(s: str):
    if not s:
        return None
    m = re.sub(r'[^0-9.]', '', s)
    try:
        return float(m) if m else None
    except Exception:
        return None

def _clean_text(html_str: str) -> str:
    s = re.sub(r'<br\s*/?>', '\n', html_str, flags=re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def _page_text(page_html: str) -> str:
    # Replace common break tags, then remove tags for a full-text scan
    s = re.sub(r'<br\s*/?>', '\n', page_html, flags=re.I)
    s = re.sub(r'<style[\s\S]*?</style>|<script[\s\S]*?</script>', ' ', s, flags=re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'[\u2009\u202f\u00a0]', ' ', s)  # thin spaces etc
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def _extract_overview(page_html: str) -> str:
    paras = re.findall(r'<div class=\"et_pb_text_inner\">(.*?)</div>', page_html, re.S)
    texts = [_clean_text(p) for p in paras if p]
    texts = [t for t in texts if 120 <= len(t) <= 1200]
    if texts:
        return sorted(texts, key=len, reverse=True)[0]
    md = re.search(r'<meta name=\"description\" content=\"([^\"]+)\"', page_html)
    return md.group(1) if md else ''

def _extract_beds_baths_land(s: str):
    beds = baths = land = ''
    # beds
    m = re.search(r'(\d+)\s*(?:bed(?:room)?s?\b|\-?bed\b)', s, re.I)
    if m: beds = m.group(1)
    # baths
    m = re.search(r'(\d+)\s*(?:bath(?:room)?s?\b|\-?bath\b)', s, re.I)
    if m: baths = m.group(1)
    # land size
    m = re.search(r'([0-9]{2,4}(?:,[0-9]{3})?)\s*(?:m\s?(?:²|2)|sqm|square\s*m(?:etres|eters)?)', s, re.I)
    if m:
        land = m.group(1).replace(',', '') + ' m²'
    return beds, baths, land

def _extract_specs(page_html: str):
    t = _page_text(page_html)
    beds, baths, land = _extract_beds_baths_land(t)
    # car spaces / garage / parking
    car = ''
    m = re.search(r'(\d+)\s*(?:car\s*spaces?|carspaces?|garage(?:s)?|parking)\b', t, re.I)
    if m:
        car = m.group(1)
    return beds, baths, car, land

def _extract_highlights(page_html: str):
    items = []
    for ul in re.findall(r'<ul>(.*?)</ul>', page_html, re.S):
        for li in re.findall(r'<li[^>]*>(.*?)</li>', ul, re.S):
            text = _clean_text(li)
            if text and len(text) >= 8:
                items.append(text)
    seen = set(); out = []
    for i in items:
        if i not in seen:
            seen.add(i); out.append(i)
    return out[:10]

def _extract_og_image(page_html: str) -> str:
    m = re.search(r'<meta property=\"og:image\" content=\"([^\"]+)\"', page_html)
    return m.group(1) if m else ''

def main():
    html = fetch(OUR_RESULTS_URL)
    cards = extract_cards(html)
    items = []
    # load previous data to preserve values if scrape misses any
    prev = {}
    try:
        prev_list = json.loads(DATA.read_text())
        prev = {it.get('slug'): it for it in prev_list if isinstance(it, dict) and it.get('slug')}
    except Exception:
        prev = {}
    for c in cards:
        slug = Path(urlparse(c['href']).path).name
        fields = map_feature_to_fields(c['features'])
        # derive fields from available values
        pp = _parse_money(fields.get('purchase_price',''))
        rw = _parse_money(fields.get('rent',''))
        rent_yield = ''
        if pp and rw:
            y = (rw * 52.0) / pp * 100.0
            rent_yield = f"{y:.1f}%"
        tags = _derive_tags(c['title'])
        if 'High Yield' in tags and 'High Growth' in tags:
            strategy = 'Balanced Growth & Yield'
        elif 'High Yield' in tags:
            strategy = 'High Yield Strategy'
        elif 'High Growth' in tags:
            strategy = 'High Growth Strategy'
        else:
            strategy = ''
        # basic property type heuristic
        t = c['title'].lower()
        property_type = ''
        if 'cottage' in t or 'house' in t:
            property_type = 'House'
        elif 'apartment' in t or 'unit' in t:
            property_type = 'Apartment'
        # prepare local image path (prefer OG image, fallback to card image)
        img_local = ''

        # fetch property page for rich details
        page_html = ''
        try:
            page_html = fetch(c['href'])
        except Exception:
            page_html = ''
        og_img = _extract_og_image(page_html) if page_html else ''
        overview = _extract_overview(page_html) if page_html else ''
        beds, baths, car_spaces, land = _extract_specs(page_html) if page_html else ('','','','')
        highlights = _extract_highlights(page_html) if page_html else []

        # attempt to download OG image; if not available, download card image
        try:
            if og_img:
                img_local = download_image(og_img, slug)
        except Exception:
            pass
        if not img_local:
            try:
                if c.get('image_url'):
                    img_local = download_image(c['image_url'], slug)
            except Exception:
                pass

        item = {
            'live_url': c['href'],
            'slug': slug,
            'title': c['title'],
            'location': c['location'],
            'image': img_local or image_for(c['title'], c['href']),
            'strategy': strategy,
            'tags': tags,
            'purchase_price': fields.get('purchase_price',''),
            'instant_equity': '',
            'growth_12m': '',
            'growth_3y': fields.get('growth_3y',''),
            'rent': fields.get('rent',''),
            'rental_growth_3y': fields.get('rental_growth_3y',''),
            'rent_yield': rent_yield,
            'profile': '',
            'overview': overview,
            'strategy_points': [],
            'execution_points': [],
            'bedrooms': beds,
            'bathrooms': baths,
            'car_spaces': car_spaces,
            'land_size': land,
            'property_type': property_type,
            'purchase_date': '',
            'valuation_post_purchase': '',
            'highlights': highlights
        }
        # merge fallback from prev if empty
        if slug in prev:
            for k in ('purchase_price','growth_3y','rent','rental_growth_3y','rent_yield','image'):
                if not item.get(k):
                    item[k] = prev[slug].get(k,'')
        items.append(item)
    # write JSON
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(items, indent=2))
    print(f"Wrote {len(items)} properties to {DATA}")

if __name__ == '__main__':
    main()

def download_image(url: str, slug: str) -> str:
    from urllib.request import urlopen
    from urllib.parse import urlparse
    import os
    if not url:
        return ''
    parsed = urlparse(url)
    base = os.path.basename(parsed.path)
    ext = '.jpg'
    if '.' in base:
        ext = '.' + base.split('.')[-1]
    out_dir = ROOT / 'assets' / 'properties' / 'live'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}{ext}"
    try:
        with urlopen(Request(url, headers=HDRS), timeout=30) as r:
            data = r.read()
        with open(out_path, 'wb') as f:
            f.write(data)
        return str(out_path.relative_to(ROOT))
    except Exception:
        return ''
