import re
from pathlib import Path
from tools.seo_config import site_url

ROOT = Path(__file__).resolve().parent.parent

def fix_file(p: Path, site: str) -> bool:
    txt = p.read_text(encoding='utf-8', errors='ignore')
    new = re.sub(r'<link\s+rel=\"canonical\"[^>]*href=\"([^\"]*)\"[^>]*>', '', txt, flags=re.I)
    # infer page path
    rel = '' if p.name == 'index.html' else p.name
    canon = f'{site}/' if p.name == 'index.html' else f'{site}/{p.name}'
    # insert canonical before </head>
    new = re.sub(r'</head>', f'\n<link rel="canonical" href="{canon}">\n</head>', new, flags=re.I)
    if new != txt:
        p.write_text(new, encoding='utf-8')
        return True
    return False

def main():
    site = site_url()
    changed = 0
    for p in ROOT.glob('*.html'):
        if p.name in ('articles.html',):
            continue
        if fix_file(p, site):
            changed += 1
    print('Updated canonicals on', changed, 'root HTML files')

if __name__ == '__main__':
    main()

