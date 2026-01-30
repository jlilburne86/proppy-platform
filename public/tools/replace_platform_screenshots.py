import os, re
from pathlib import Path

ROOT = Path('/Users/boo2/Desktop/proppy')
IMG_PATTERN = re.compile(r'src=["\']assets/screenshots/[^"\']+["\']', re.I)

# Heuristic annotations by context
RULES = [
    (re.compile(r'portfolio|dashboard|track', re.I), 'Show portfolio dashboard with equity, rent p/w, recent growth.'),
    (re.compile(r'shortlist|compare|due diligence|comps', re.I), 'Show shortlist table with scores, comps, rental appraisals.'),
    (re.compile(r'market|signal|search|vacancy|yield|supply', re.I), 'Show suburb search + filters, vacancy/yield/supply signals.'),
    (re.compile(r'workflow|onboarding|goals|timeline', re.I), 'Show onboarding flow — goals, budget, timeline → outputs.'),
]
DEFAULT_ANN = 'Show relevant platform view supporting this section.'

FIGURE_BLOCK = re.compile(r'<figure[\s\S]*?</figure>', re.I)
FIGCAP = re.compile(r'</figcaption>', re.I)


def pick_annotation(block: str) -> str:
    for rx, text in RULES:
        if rx.search(block):
            return text
    # Try alt text as signal
    m = re.search(r'alt="([^"]+)"', block, flags=re.I)
    if m:
        alt = m.group(1)
        for rx, text in RULES:
            if rx.search(alt):
                return text
    return DEFAULT_ANN


def process_html(txt: str) -> str:
    original = txt
    # First replace all screenshot sources with the provided asset
    txt = IMG_PATTERN.sub('src="assets/screenshots/platform-screenshot.png"', txt)

    # Then add annotations within figures that contain screenshots and lack our annotation
    def repl_figure(m):
        block = m.group(0)
        if 'assets/screenshots/platform-screenshot.png' not in block:
            return block
        if 'Annotation:' in block:
            return block
        ann = pick_annotation(block)
        ann_html = f'\n          <p class="px-4 pb-4 text-xs text-slate-500 dark:text-slate-400 italic">Annotation: {ann}</p>'
        if FIGCAP.search(block):
            return FIGCAP.sub('</figcaption>' + ann_html, block, count=1)
        # No figcaption: place after first image
        block = re.sub(r'(</img>|/>)', r"\1" + ann_html, block, count=1)
        if 'Annotation:' not in block:
            # Fallback: append before </figure>
            block = re.sub(r'</figure>', ann_html + '\n</figure>', block, count=1)
        return block

    txt = FIGURE_BLOCK.sub(repl_figure, txt)

    # For standalone images not wrapped in <figure>, add annotation once, directly after
    def add_ann_after_img(match):
        tag = match.group(0)
        if 'platform-screenshot.png' not in tag:
            return tag
        return tag + '\n<p class="text-xs text-slate-500 dark:text-slate-400 italic">Annotation: {}' \
            .format(DEFAULT_ANN) + '</p>'

    # Only for cases where not inside a figure: cheap guard
    if '<figure' not in txt:
        txt = re.sub(r'<img[^>]+src="assets/screenshots/platform-screenshot.png"[^>]*>', add_ann_after_img, txt, count=1)

    return txt


def main():
    updated = []
    for path in ROOT.rglob('*.html'):
        try:
            txt = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        new = process_html(txt)
        if new != txt:
            path.write_text(new, encoding='utf-8')
            updated.append(str(path.relative_to(ROOT)))
    print('Patched screenshots + annotations in', len(updated), 'files')
    for u in updated:
        print('-', u)

if __name__ == '__main__':
    main()
