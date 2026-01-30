(function(){
  var root = document.documentElement;
  var drawer, overlay, burger, closeBtn;

  function initRefs(){
    drawer = document.getElementById('navx-drawer') || document.querySelector('.navx-drawer');
    overlay = document.getElementById('navx-overlay') || document.querySelector('.navx-overlay');
    burger = document.getElementById('navx-burger');
    closeBtn = document.getElementById('navx-close');
    if (burger && drawer){
      burger.setAttribute('aria-controls','navx-drawer');
      burger.setAttribute('aria-expanded','false');
      burger.setAttribute('aria-label','Open menu');
    }
    if (closeBtn){ closeBtn.setAttribute('aria-label','Close menu'); }
  }

  function focusable(container){
    if (!container) return [];
    return Array.prototype.slice.call(container.querySelectorAll('a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])'));
  }

  function openMenu(){
    root.classList.add('navx-open');
    if (burger) burger.setAttribute('aria-expanded','true');
    var els = focusable(drawer);
    if (els.length) els[0].focus();
  }

  function closeMenu(){
    root.classList.remove('navx-open');
    if (burger){ burger.setAttribute('aria-expanded','false'); burger.focus(); }
  }

  function handleKeydown(e){
    if (!root.classList.contains('navx-open')) return;
    if (e.key === 'Escape'){ e.preventDefault(); closeMenu(); return; }
    if (e.key === 'Tab' && drawer){
      var els = focusable(drawer);
      if (!els.length) return;
      var first = els[0], last = els[els.length - 1];
      if (e.shiftKey && document.activeElement === first){ e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last){ e.preventDefault(); first.focus(); }
    }
  }

  function closeAll(){
    document.querySelectorAll('.navx-group.open').forEach(function(el){ el.classList.remove('open'); });
    document.querySelectorAll('.navx-toggle[aria-expanded="true"]').forEach(function(a){ a.setAttribute('aria-expanded','false'); });
  }

  function onClick(e){
    var t = e.target;
    // desktop submenu toggle
    var toggle = t.closest && t.closest('a.navx-toggle');
    if (toggle){ e.preventDefault(); e.stopPropagation(); var parent = toggle.closest('.navx-group'); var isOpen = parent.classList.contains('open'); closeAll(); if(!isOpen){ parent.classList.add('open'); toggle.setAttribute('aria-expanded','true'); } return; }
    if (!t.closest || !t.closest('.navx-sub')){ closeAll(); }
    // mobile drawer
    var openBtn = t.closest && t.closest('#navx-burger');
    var xBtn = t.closest && t.closest('#navx-close');
    if (openBtn){ e.preventDefault(); openMenu(); }
    if (xBtn || (t.classList && t.classList.contains('navx-overlay'))){ closeMenu(); }
    // accordion in drawer
    var acc = t.closest && t.closest('.navx-acc');
    if (acc){ e.preventDefault(); var body = acc.nextElementSibling; if(body){ body.classList.toggle('hidden'); }}
  }

  document.addEventListener('DOMContentLoaded', initRefs);
  document.addEventListener('click', onClick, true);
  document.addEventListener('keydown', handleKeydown);
})();
