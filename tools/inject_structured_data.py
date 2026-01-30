import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def load_site():
    data = {
        "site_url": "https://jlilburne86.github.io/proppy-platform",
        "org_name": "Proppy",
        "logo_path": "/proppy-logo.png",
        "same_as": [],
        "telephone": "",
        "address": {},
    }
    p = ROOT / 'data' / 'site.json'
    try:
        data.update(json.loads(p.read_text(encoding='utf-8')))
    except Exception:
        pass
    # normalise
    data['site_url'] = data.get('site_url','').rstrip('/') or 'https://jlilburne86.github.io/proppy-platform'
    return data

def org_jsonld(cfg: dict) -> str:
    url = cfg['site_url']
    org = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": cfg.get("org_name") or "Proppy",
        "url": url,
        "logo": url + (cfg.get("logo_path") or "/proppy-logo.png"),
    }
    if cfg.get('same_as'):
        org['sameAs'] = cfg['same_as']
    if cfg.get('telephone'):
        org['telephone'] = cfg['telephone']
    if cfg.get('address'):
        org['address'] = {"@type":"PostalAddress", **cfg['address']}
    return '<script type="application/ld+json">' + json.dumps(org) + '</script>'

def website_jsonld(cfg: dict) -> str:
    url = cfg['site_url']
    site = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": cfg.get("org_name") or "Proppy",
        "url": url,
        "potentialAction": {
            "@type": "SearchAction",
            "target": url + "/?s={search_term_string}",
            "query-input": "required name=search_term_string"
        }
    }
    return '<script type="application/ld+json">' + json.dumps(site) + '</script>'

def inject_into_html(p: Path, org_ld: str, site_ld: str) -> bool:
    txt = p.read_text(encoding='utf-8', errors='ignore')
    payload = org_ld + "\n" + site_ld + "\n"
    new = re.sub(r'</head>', payload + '</head>', txt, flags=re.I)
    if new != txt:
        p.write_text(new, encoding='utf-8')
        return True
    return False

def main():
    cfg = load_site()
    org_ld = org_jsonld(cfg)
    site_ld = website_jsonld(cfg)
    changed = 0
    for p in ROOT.glob('*.html'):
        if inject_into_html(p, org_ld, site_ld):
            changed += 1
    print('Injected Organization/WebSite JSON-LD into', changed, 'root pages')

if __name__ == '__main__':
    main()

