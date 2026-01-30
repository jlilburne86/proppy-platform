import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'articles'

PILLAR_DEFAULT = {
    'Market Trends': '/assets/screenshots/technology.png',
    'Suburb Profiles': '/assets/screenshots/homepage-9.png',
    'Strategy': '/assets/screenshots/how-it-works.png',
    'Cycles': '/assets/screenshots/platform-screenshot.png',
    'Case Studies': '/assets/screenshots/platform-screenshot.png',
    'Risk': '/assets/screenshots/platform-screenshot.png',
}

def parse_front(text: str):
    fm = {}
    body = text
    if text.strip().startswith('---'):
        parts = text.split('---',2)
        if len(parts) >= 3:
            for line in parts[1].splitlines():
                if ':' in line:
                    k,v = line.split(':',1)
                    fm[k.strip()] = v.strip().strip('"')
            body = parts[2]
    return fm, body

def first_md_image(body: str) -> str:
    m = re.search(r'!\[[^\]]*\]\(([^)]+)\)', body)
    return m.group(1) if m else ''

def ensure_og(md: Path) -> bool:
    txt = md.read_text(encoding='utf-8', errors='ignore')
    fm, body = parse_front(txt)
    status = (fm.get('publish_status','') or '').lower()
    if status != 'published':
        return False
    if 'og_image:' in txt.split('---',2)[1]:
        return False
    cat = (fm.get('category','') or '').strip('[]').split(',')[0].strip()
    img = first_md_image(body) or PILLAR_DEFAULT.get(cat) or '/assets/screenshots/platform-screenshot.png'
    parts = txt.split('---',2)
    fm_txt = parts[1] + "\nog_image: \"" + img + "\
"
    md.write_text(parts[0] + '---' + fm_txt + '---' + parts[2], encoding='utf-8')
    return True

def main():
    changed = 0
    for md in ART.glob('*.md'):
        if ensure_og(md):
            changed += 1
    print('Added og_image to', changed, 'articles (bulk)')

if __name__ == '__main__':
    main()
