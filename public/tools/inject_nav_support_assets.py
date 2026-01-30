import os
import re

ROOT = os.path.join(os.path.dirname(__file__), '..')

STYLE = '''<style id="nav-support-styles">
.nav-submenu{display:none}
.group:hover>.nav-submenu,.group:focus-within>.nav-submenu,.group.open>.nav-submenu{display:block}
.nav-toggle{cursor:pointer}
</style>'''

SCRIPT = '''<script id="nav-support-script">
(function(){
  function closeAll(){
    document.querySelectorAll('.group.open').forEach(el=>el.classList.remove('open'));
    document.querySelectorAll('.nav-toggle[aria-expanded="true"]').forEach(a=>a.setAttribute('aria-expanded','false'));
  }
  document.addEventListener('click', function(e){
    var toggle = e.target.closest('a.nav-toggle');
    if (toggle){
      e.preventDefault();
      e.stopPropagation();
      var parent = toggle.closest('.group');
      var isOpen = parent.classList.contains('open');
      closeAll();
      if (!isOpen){ parent.classList.add('open'); toggle.setAttribute('aria-expanded','true'); }
      return;
    }
    if (!e.target.closest('.nav-submenu')){ closeAll(); }
  }, true);
  document.addEventListener('keydown', function(e){ if(e.key==='Escape') closeAll(); });
})();
</script>'''

def inject(path):
  html = open(path,'r',encoding='utf-8',errors='ignore').read()
  # ensure style in head
  if 'id="nav-support-styles"' not in html:
    html = re.sub(r'</head>', STYLE + '\n</head>', html, flags=re.I)
  # ensure script before body end
  if 'id="nav-support-script"' not in html:
    html = re.sub(r'</body>\s*</html>\s*$', SCRIPT + '\n</body></html>', html, flags=re.I)
  return html

def main():
  updated = []
  for name in os.listdir(ROOT):
    if not name.endswith('.html'):
      continue
    p = os.path.join(ROOT, name)
    new = inject(p)
    open(p,'w',encoding='utf-8').write(new)
    updated.append(name)
  print('Injected nav support into', len(updated), 'pages')

if __name__ == '__main__':
  main()
