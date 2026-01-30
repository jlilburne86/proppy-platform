import os
import shutil
import re

ROOT = os.path.join(os.path.dirname(__file__), '..')
STITCH = os.path.join(ROOT, 'stitch_corporate_landing_page_redesign_v1 2')
ASSETS = os.path.join(ROOT, 'assets', 'screenshots')

MAP = {
    # page -> list of (alt_substring, asset filename)
    'index.html': [
        ('Workflow overview', 'how-it-works.png'),
        ('Market intelligence', 'technology.png'),
        ('Portfolio dashboard', 'homepage-9.png'),
    ],
    'how-it-works.html': [
        ('Process screen', 'how-it-works.png'),
        ('Signals screen', 'technology.png'),
    ],
    'technology.html': [
        ('Signals view', 'technology.png'),
        ('Compare view', 'pricing-faq.png'),
        ('Process view', 'how-it-works.png'),
    ],
    'pricing.html': [
        ('Workflow', 'how-it-works.png'),
        ('Signals', 'technology.png'),
        ('Portfolio', 'homepage-9.png'),
    ],
    'results.html': [
        ('Portfolio dashboard', 'homepage-9.png'),
    ],
    'resources.html': [
        ('Workflow', 'how-it-works.png'),
        ('Signals', 'technology.png'),
        ('Portfolio', 'homepage-9.png'),
    ],
    'advantage.html': [
        ('Product preview', 'technology.png'),
    ],
    'sourcing.html': [
        ('Product preview', 'homepage-6.png'),
    ],
    'about.html': [
        ('Product preview', 'homepage-5.png'),
    ],
    'team.html': [
        ('Product preview', 'homepage-4.png'),
    ],
    'platform.html': [
        ('Search markets', 'technology.png'),
        ('Shortlist deals', 'pricing-faq.png'),
        ('Track portfolio', 'homepage-9.png'),
    ],
}

SRC_IMAGES = {
    'how-it-works.png': os.path.join(STITCH, 'proppy_how_it_works_-_fintech_style', 'screen.png'),
    'technology.png': os.path.join(STITCH, 'proppy_technology_-_fintech_style', 'screen.png'),
    'pricing-faq.png': os.path.join(STITCH, 'proppy_pricing_&_faq_-_fintech_style', 'screen.png'),
    'homepage-9.png': os.path.join(STITCH, 'proppy_homepage_-_fintech_style_9', 'screen.png'),
    'homepage-6.png': os.path.join(STITCH, 'proppy_homepage_-_fintech_style_6', 'screen.png'),
    'homepage-5.png': os.path.join(STITCH, 'proppy_homepage_-_fintech_style_5', 'screen.png'),
    'homepage-4.png': os.path.join(STITCH, 'proppy_homepage_-_fintech_style_4', 'screen.png'),
}

def ensure_assets():
    os.makedirs(ASSETS, exist_ok=True)
    for name, src in SRC_IMAGES.items():
        if os.path.isfile(src):
            dst = os.path.join(ASSETS, name)
            shutil.copyfile(src, dst)

def replace_img_src(html: str, alt_sub: str, asset_name: str) -> str:
    # Replace src for img tags whose alt contains alt_sub (regardless of attribute order)
    def _sub(m):
        tag = m.group(0)
        tag = re.sub(r'(src=\")[^\"]+(\")', r'\1assets/screenshots/%s\2' % asset_name, tag, flags=re.I)
        return tag
    pattern = re.compile(r'<img[^>]*alt=\"[^\"]*%s[^\"]*\"[^>]*>' % re.escape(alt_sub), flags=re.I)
    return pattern.sub(_sub, html)

def apply_mapping():
    updated = []
    for page, entries in MAP.items():
        path = os.path.join(ROOT, page)
        if not os.path.isfile(path):
            continue
        html = open(path, 'r', encoding='utf-8', errors='ignore').read()
        orig = html
        for alt_sub, asset in entries:
            html = replace_img_src(html, alt_sub, asset)
        if html != orig:
            with open(path, 'w', encoding='utf-8') as w:
                w.write(html)
            updated.append(page)
    print('Updated screenshots in:', ', '.join(updated) or 'none')

def main():
    ensure_assets()
    apply_mapping()

if __name__ == '__main__':
    main()
