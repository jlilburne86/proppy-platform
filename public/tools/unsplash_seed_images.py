import json, re
from pathlib import Path

ROOT = Path('/Users/boo2/Desktop/proppy')
ART = ROOT / 'articles'
DATA = ROOT / 'data/article_scorecards.json'

CAT_KWS = {
  'Market Trends': ['australia','city','skyline','real estate'],
  'Strategy': ['finance','calculator','notebook','planning'],
  'Suburb Profiles': ['suburb','street','australia','houses'],
  'Risk': ['caution','risk','storm','umbrella'],
  'Cycles': ['cycle','waves','ocean','seasons'],
  'Case Studies': ['keys','house','door','home']
}

def parse_fm(txt: str) -> dict:
  if not txt.strip().startswith('---'): return {}
  fm = txt.split('---',2)[1]
  d = {}
  for line in fm.splitlines():
    if ':' in line:
      k,v=line.split(':',1)
      d[k.strip()] = v.strip().strip('"')
  return d

def kw_for_category(cat: str):
  return CAT_KWS.get(cat, ['australia','property','real estate'])

def make_src(kws: list[str]):
  # Use Unsplash source endpoint with keyword query
  q = ','.join(kws)
  return f'https://source.unsplash.com/960x600/?{q}'

def main():
  data = {}
  if DATA.exists():
    try:
      data = json.loads(DATA.read_text(encoding='utf-8'))
    except Exception:
      data = {}
  updated = 0
  for md in ART.glob('*.md'):
    slug = md.stem
    cur = data.get(slug, {})
    if cur.get('images'):
      continue
    fm = parse_fm(md.read_text(encoding='utf-8', errors='ignore'))
    cat = fm.get('category','').strip('[]')
    cat = cat.split(',')[0].strip() if cat else ''
    kws = kw_for_category(cat)
    imgs = []
    # Generate four images with slight variations by adding slug tokens
    tokens = re.findall(r'[a-z]+', slug)
    variants = [kws, kws[:3]+tokens[:1], kws[:2]+tokens[:2], kws[:1]+tokens[:3]]
    for i,kwset in enumerate(variants):
      imgs.append({"src": make_src(kwset), "alt": f"Unsplash: {' '.join(kwset)}", "og": i==0, "kw": ' '.join(kwset)})
    cur['images'] = imgs
    data[slug] = cur
    updated += 1
  DATA.write_text(json.dumps(data, indent=2), encoding='utf-8')
  print('Seeded Unsplash images for', updated, 'articles')

if __name__=='__main__':
  main()

