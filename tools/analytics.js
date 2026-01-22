(function(){
  function track(name, data){
    if (window.dataLayer && typeof window.dataLayer.push === 'function') {
      window.dataLayer.push({ event: name, ...data });
    } else if (window.plausible) {
      try { window.plausible(name, { props: data }); } catch(e){}
    } else {
      // Dev fallback
      if (window.localStorage && localStorage.getItem('debug-analytics')==='1') {
        console.log('[analytics]', name, data);
      }
    }
  }
  document.addEventListener('click', function(e){
    var a = e.target.closest('a');
    if (!a) return;
    var href = (a.getAttribute('href')||'').trim();
    if (!href) return;
    if (href.includes('book.html') || href.startsWith('https://calendly.com/')) {
      track('cta_book_click', { href: href, text: (a.textContent||'').trim() });
    }
    if (href.startsWith('mailto:')) {
      track('cta_email_click', { href: href });
    }
    if (href.startsWith('tel:')) {
      track('cta_phone_click', { href: href });
    }
  }, true);

  // Track newsletter submits
  document.addEventListener('submit', function(e){
    var f = e.target;
    if (!f || !f.tagName) return;
    var name = f.getAttribute('name') || '';
    if (name.toLowerCase() === 'newsletter') {
      track('newsletter_submit', {});
    }
    if (name.toLowerCase() === 'contact') {
      track('contact_submit', {});
    }
  }, true);
})();
