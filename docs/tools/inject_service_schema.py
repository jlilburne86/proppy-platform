#!/usr/bin/env python3
import os, json, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Minimal mapping: page -> service details
SERVICES = {
  'technology.html': {
    'serviceType': 'Property Investment Technology',
    'areaServed': 'Australia',
    'description': 'Data-led property selection using market signals like vacancy, rents, listings, DOM and approvals to identify opportunities earlier and reduce risk.'
  },
  'advantage.html': {
    'serviceType': 'Property Investment Advisory',
    'areaServed': 'Australia',
    'description': 'End-to-end advisory combining data-led shortlists, negotiation and execution to help investors purchase high-quality assets with confidence.'
  },
  'sourcing.html': {
    'serviceType': 'Property Sourcing',
    'areaServed': 'Australia',
    'description': 'Nationwide property sourcing focused on undersupplied markets with strong rentability and value-add potential.'
  }
}

def inject_service_schema(path, service):
    with open(path,'r',encoding='utf-8',errors='ignore') as f:
        html = f.read()
    # Skip if already present for this serviceType
    if service['serviceType'] in html and 'Service' in html:
        return False
    import json as _json
    ld = {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": service['serviceType'],
        "areaServed": {"@type":"Country","name": service['areaServed']},
        "provider": {"@type":"Organization","name":"Proppy"},
        "description": service['description']
    }
    block = '<script type="application/ld+json" data-auto="1">' + _json.dumps(ld, ensure_ascii=False) + '</script>'
    new_html, n = re.subn(r'</body>', block + '\n</body>', html, count=1, flags=re.I)
    if n:
        with open(path,'w',encoding='utf-8') as w:
            w.write(new_html)
        return True
    return False

def main():
    changed = 0
    for name, svc in SERVICES.items():
        p = os.path.join(ROOT, name)
        if not os.path.exists(p):
            continue
        if inject_service_schema(p, svc):
            changed += 1
    print(f'Injected Service schema into {changed} pages')

if __name__ == '__main__':
    main()

