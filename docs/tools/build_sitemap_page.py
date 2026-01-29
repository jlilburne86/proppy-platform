import os

ROOT = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(ROOT, 'site-map.html')

def main():
    files = [f for f in os.listdir(ROOT) if f.endswith('.html') and f not in { 'site-map.html' }]
    files.sort()
    items = '\n'.join([f'<li><a class="text-primary hover:underline" href="{f}">{f}</a></li>' for f in files])
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Site Map</title>
  <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
</head>
<body class="bg-white text-slate-900">
  <div class="max-w-3xl mx-auto p-8 prose">
    <h1>Site Map</h1>
    <p>All pages in this site are listed below.</p>
    <ul>
      {items}
    </ul>
  </div>
</body>
</html>'''
    with open(OUT, 'w', encoding='utf-8') as w:
        w.write(html)
    print('Wrote', OUT)

if __name__ == '__main__':
    main()

