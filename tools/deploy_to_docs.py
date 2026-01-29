import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'

INCLUDE_DIRS = ['articles', 'assets', 'tools', 'property']
INCLUDE_FILES = [
    'index.html','resources.html','articles.xml','sitemap.xml','site-map.html',
    'about.html','advantage.html','assessment.html','book.html','built-for-signal-not-noise.html',
    'contact.html','guarantee.html','how-it-works.html','nationwide-sourcing.html','pricing.html',
    'privacy.html','results.html','smarter-property-investment-powered-by-data-guided-by-experts.html',
    'sourcing.html','speak-with-a-property-investment-specialist.html','speak-with-a-property-investment-specialist-2.html',
    'team.html','technology.html','terms.html','the-unfair-advantage-for-modern-investors.html',
    'transparent-pricing-clear-value-no-surprises.html','we-back-our-service-if-we-dont-deliver-youre-covered.html',
    'we-build-wealth-backed-by-15-years-of-experience.html','were-redefining-property-investment-by-making-it-simpler-more-transparent-and-less-stressful.html',
    'what-results-means.html', 'favicon.ico', '.nojekyll',
    # root images used in nav/logo
    'proppy-logo.png','proppy-logo.webp','proppy mobile icon.png','proppy-mobile-icon.png',
    'robots.txt'
]

def clean_docs():
    if DOCS.exists():
        for p in DOCS.iterdir():
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
    else:
        DOCS.mkdir(parents=True, exist_ok=True)

def copy_dirs():
    for d in INCLUDE_DIRS:
        src = ROOT / d
        dst = DOCS / d
        if dst.exists():
            shutil.rmtree(dst)
        if src.exists():
            shutil.copytree(src, dst)

def copy_files():
    for f in INCLUDE_FILES:
        src = ROOT / f
        if src.exists():
            shutil.copy2(src, DOCS / f)

def main():
    clean_docs()
    copy_dirs()
    copy_files()
    print('Deployed site to docs/')

if __name__ == '__main__':
    main()
