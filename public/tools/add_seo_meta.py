import os
import re

ROOT = os.path.join(os.path.dirname(__file__), '..')

CANON = {
    'built-for-signal-not-noise.html': 'technology.html',
    'investor-resources-hub.html': 'resources.html',
    'what-results-means.html': 'results.html',
    'we-back-our-service-if-we-dont-deliver-youre-covered.html': 'guarantee.html',
    'transparent-pricing-clear-value-no-surprises.html': 'pricing.html',
    'the-unfair-advantage-for-modern-investors.html': 'advantage.html',
    'nationwide-sourcing.html': 'sourcing.html',
    'were-redefining-property-investment-by-making-it-simpler-more-transparent-and-less-stressful.html': 'about.html',
    'we-build-wealth-backed-by-15-years-of-experience.html': 'team.html',
    'speak-with-a-property-investment-specialist.html': 'book.html',
    'speak-with-a-property-investment-specialist-2.html': 'contact.html',
}

DESCRIPTIONS = {
    'index.html': 'Proppy helps you buy the right property in the right market at the right price with data-led insights and expert execution.',
    'how-it-works.html': 'See the Proppy process step-by-step and how our technology identifies high-performing markets.',
    'technology.html': 'Explore Proppy’s technology—built for signal, not noise—to find opportunities early and reduce risk.',
    'resources.html': 'Investor guides and market updates to help you invest with confidence.',
    'results.html': 'Results and case studies showing how data-led decisions deliver equity and growth.',
    'guarantee.html': 'Our money-back guarantee on the strategy phase so you can start with confidence.',
    'pricing.html': 'Transparent pricing with clear value—no commissions or surprises.',
    'advantage.html': 'Why Proppy’s approach gives modern investors a real edge.',
    'sourcing.html': 'Nationwide sourcing with off-market access for better deals, faster.',
    'about.html': 'Why we exist and how we’re simplifying property investing for Australians.',
    'team.html': 'Meet the team helping you invest with clarity and conviction.',
    'book.html': 'Book a free strategy call to discuss your goals and plan your next move.',
    'contact.html': 'Contact Proppy for questions about strategy, pricing, or getting started.',
}

def ensure_meta(html: str, filename: str) -> str:
    head_m = re.search(r'<head>([\s\S]*?)</head>', html, flags=re.I)
    if not head_m:
        return html
    head = head_m.group(1)
    canon_target = CANON.get(filename, filename)
    # Add canonical link
    if 'rel="canonical"' not in head:
        canon_tag = f'\n<link rel="canonical" href="{canon_target}">'
        head = head + canon_tag
    # Add meta description based on map
    desc = DESCRIPTIONS.get(canon_target, DESCRIPTIONS.get(filename))
    if desc and 'name="description"' not in head:
        head = head + f'\n<meta name="description" content="{desc}">'
    # Return updated html
    return html[:head_m.start(1)] + head + html[head_m.end(1):]

def main():
    updated = []
    for name in os.listdir(ROOT):
        if not name.endswith('.html'):
            continue
        path = os.path.join(ROOT, name)
        txt = open(path, 'r', encoding='utf-8', errors='ignore').read()
        new = ensure_meta(txt, name)
        if new != txt:
            with open(path, 'w', encoding='utf-8') as w:
                w.write(new)
            updated.append(name)
    print('Added SEO meta to', len(updated), 'pages')
    for f in updated:
        print('-', f)

if __name__ == '__main__':
    main()
