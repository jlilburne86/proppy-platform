from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

META = {
    'index.html': {
        'title': 'Smarter Property Investment - Proppy',
        'desc': 'Buy the right property at the right price with data-led insights and expert execution.'
    },
    'how-it-works.html': {
        'title': 'How It Works - Proppy',
        'desc': 'Our data-led process to find, assess and secure quality investment properties.'
    },
    'pricing.html': {
        'title': 'Transparent Pricing - Proppy',
        'desc': 'Simple, transparent pricing with clear value—no commissions or surprises.'
    },
    'results.html': {
        'title': 'Investor Results - Proppy',
        'desc': 'Real outcomes from our clients—growth, rental strength and better decisions.'
    },
    'resources.html': {
        'title': 'Proppy Resources Hub',
        'desc': 'Investor guides and market updates to help you invest with confidence.'
    }
}

def set_meta(p: Path, title: str, desc: str) -> bool:
    txt = p.read_text(encoding='utf-8', errors='ignore')
    new = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', txt, flags=re.I)
    if 'name="description"' in new:
        new = re.sub(r'<meta\s+name=\"description\"[^>]*>', f'<meta name="description" content="{desc}">', new, flags=re.I)
    else:
        new = re.sub(r'</head>', f'\n<meta name="description" content="{desc}">\n</head>', new, flags=re.I)
    if new != txt:
        p.write_text(new, encoding='utf-8')
        return True
    return False

def main():
    changed = 0
    for name, meta in META.items():
        p = ROOT / name
        if p.exists():
            if set_meta(p, meta['title'], meta['desc']):
                changed += 1
    print('Tweaked meta on', changed, 'pages')

if __name__ == '__main__':
    main()

