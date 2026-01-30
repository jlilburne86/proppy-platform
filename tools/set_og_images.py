from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'articles'

OG_MAP = {
  'days-on-market-as-leading-indicator': '/assets/screenshots/technology.png',
  'vacancy-rates-explained-what-tight-and-loose-markets-mean': '/assets/screenshots/technology.png',
  'supply-constraints-construction-delays': '/assets/screenshots/how-it-works.png',
  'when-to-use-equity-when-to-save-cash': '/assets/screenshots/platform-screenshot.png',
  'rentvesting-explained-how-investors-separate-home-and-portfolio': '/assets/screenshots/homepage-9.png',
  'interest-rate-risk-management': '/assets/screenshots/technology.png',
  'the-2024-interstate-investment-playbook': '/assets/screenshots/homepage-9.png',
  'building-your-first-investment-property-portfolio': '/assets/screenshots/how-it-works.png',
  'brisbane-growth-corridors-ipswich-logan-and-moreton-bay': '/assets/screenshots/homepage-9.png',
  'gold-coast-growth-corridors': '/assets/screenshots/homepage-9.png',
}

def ensure_og(md: Path, og_path: str) -> bool:
    txt = md.read_text(encoding='utf-8', errors='ignore')
    if not txt.strip().startswith('---'):
        return False
    parts = txt.split('---',2)
    fm = parts[1]
    body = parts[2]
    if 'og_image:' in fm:
        return False
    fm = fm + f"\nog_image: \"{og_path}\"\n"
    md.write_text(parts[0] + '---' + fm + '---' + body, encoding='utf-8')
    return True

def main():
    changed = 0
    for slug, og in OG_MAP.items():
        p = ART / f'{slug}.md'
        if p.exists():
            if ensure_og(p, og):
                changed += 1
    print('Added og_image to', changed, 'articles')

if __name__ == '__main__':
    main()

