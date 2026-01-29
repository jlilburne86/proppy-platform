import re, os
root = '/Users/boo2/Desktop/proppy'
plan = {
  'index.html': [
    'Onboarding: define goals, budget, timeline → suggested markets & criteria.',
    'Suburb heatmap with KPIs: vacancy, yield, supply, growth momentum.',
    'Portfolio dashboard: equity, rent p/w, 12‑mo growth, pipeline.'
  ],
  'platform.html': [
    'Market search with filters; rank suburbs by KPIs and risk.',
    'Shortlist comparison: price vs value, comps, rental appraisal, checklists.',
    'Portfolio & pipeline: holdings, equity trend, rent roll, tasks.'
  ],
  'technology.html': [
    'Signals view: growth momentum, yield dynamics, supply/vacancy.',
    'Compare view: side-by-side suburbs with deciles and backtests.',
    'Process view: step-by-step sourcing with confidence score.'
  ],
  'advantage.html': [
    'Competitive edge: signals + expert execution combined.'
  ],
  'results.html': [
    'Portfolio snapshot: purchase price, rent p/w, 3‑year growth, strategy tag.'
  ],
  'sourcing.html': [
    'Pipeline view: off‑market → appraisal → negotiation → contract; DD checklist.'
  ],
  'about.html': [
    'Platform overview: investor workflow at a glance.'
  ],
  'team.html': [
    'Advisory workflow: how we guide your purchase.'
  ],
  'pricing.html': [
    'Plans feature map: what’s included per plan.'
  ],
}

updated=[]
for fn, notes in plan.items():
    p = os.path.join(root, fn)
    if not os.path.exists(p):
        continue
    txt = open(p,'r',encoding='utf-8',errors='ignore').read()
    # find all Annotation occurrences
    matches = list(re.finditer(r'Annotation:\s*[^<]+', txt))
    if not matches:
        continue
    new = txt
    # replace in order up to number of notes
    for i, note in enumerate(notes):
        try:
            m = matches[i]
        except IndexError:
            break
        start, end = m.span()
        new = new[:start] + 'Annotation: ' + note + new[end:]
        # shift subsequent match positions due to possible length change
        # recompute matches after each replacement to stay safe
        matches = list(re.finditer(r'Annotation:\s*[^<]+', new))
    if new != txt:
        open(p,'w',encoding='utf-8').write(new)
        updated.append(fn)

print('Updated annotations in', len(updated), 'files:')
for u in updated:
    print('-', u)
