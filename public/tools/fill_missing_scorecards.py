import json
from pathlib import Path

ROOT = Path('/Users/boo2/Desktop/proppy')
ART = ROOT / 'articles'
DATA = ROOT / 'data/article_scorecards.json'

CAT_DEFAULTS = {
  'Market Trends': [
    ('Vacancy','Mixed','City/segment dependent'),
    ('Rent Pressure','Varies','Watch YoY'),
    ('Listings','Uneven','Absorption matters'),
    ('Pipeline','Below peaks','Delivery risk')
  ],
  'Strategy': [
    ('Vacancy','Target <1.5%','Screen threshold'),
    ('Rent Pressure','Rising','Prefer YoY up'),
    ('Listings','Flat','Avoid spikes'),
    ('Pipeline','Constrained','Prefer infill')
  ],
  'Suburb Profiles': [
    ('Vacancy','Tight','Tenant demand'),
    ('Rent Pressure','Rising','Comparable leases'),
    ('Listings','Stable','DOM steady'),
    ('Pipeline','Limited','Check estates')
  ],
  'Risk': [
    ('Vacancy','Rising','Stress scenario'),
    ('Rent Pressure','Sticky','Lag vs prices'),
    ('Listings','Up','Watch absorption'),
    ('Pipeline','Monitor','Delivery/capacity')
  ],
  'Cycles': [
    ('Vacancy','Phase signal','Leading'),
    ('Rent Pressure','Phase signal','Leading'),
    ('Listings','Phase signal','Lagging'),
    ('Pipeline','Lagging','Context')
  ],
  'Case Studies': [
    ('Vacancy','Local','Illustrative'),
    ('Rent Pressure','Local','Illustrative'),
    ('Listings','Local','Illustrative'),
    ('Pipeline','Local','Illustrative')
  ],
}

def parse_cat(md: Path) -> str:
    txt = md.read_text(encoding='utf-8', errors='ignore')
    if not txt.strip().startswith('---'):
        return ''
    fm = txt.split('---',2)[1]
    for line in fm.splitlines():
        if line.strip().startswith('category:'):
            val = line.split(':',1)[1].strip().strip('[]').split(',')[0].strip()
            return val
    return ''

def main():
    data = {}
    if DATA.exists():
        try:
            data = json.loads(DATA.read_text(encoding='utf-8'))
        except Exception:
            data = {}
    changed = 0
    for md in ART.glob('*.md'):
        slug = md.stem
        entry = data.get(slug, {})
        if 'metrics' in entry and entry['metrics']:
            continue
        cat = parse_cat(md)
        defaults = CAT_DEFAULTS.get(cat or 'Strategy', CAT_DEFAULTS['Strategy'])
        metrics = {}
        keys = ['vacancy','rent','listings','pipeline']
        for idx, key in enumerate(keys):
            label, value, note = defaults[idx]
            metrics[key] = {"label": label, "value": value, "note": note}
        entry['metrics'] = metrics
        data[slug] = entry
        changed += 1
    DATA.write_text(json.dumps(data, indent=2), encoding='utf-8')
    print('Filled metrics for', changed, 'articles')

if __name__=='__main__':
    main()
