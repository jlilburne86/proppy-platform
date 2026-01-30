(function(){
  function track(name, data){
    if (typeof window.gtag === 'function') {
      try { window.gtag('event', name, data || {}); } catch(e){}
      return;
    }
    if (window.dataLayer && typeof window.dataLayer.push === 'function') {
      window.dataLayer.push({ event: name, ...data });
      return;
    }
    if (window.plausible) {
      try { window.plausible(name, { props: data }); } catch(e){}
      return;
    }
    // Dev fallback
    if (window.localStorage && localStorage.getItem('debug-analytics')==='1') {
      console.log('[analytics]', name, data);
    }
  }
  // Page view events for key funnels
  function onReady(fn){ if(document.readyState==='loading'){ document.addEventListener('DOMContentLoaded', fn); } else { fn(); } }
  onReady(function(){
    try{
      var path = (location.pathname||'').toLowerCase();
      if (path.endsWith('/book.html') || path.endsWith('book.html')) {
        track('booking_view', {});
      }
      if (path.endsWith('/contact.html') || path.endsWith('contact.html')) {
        track('contact_view', {});
      }
    }catch(e){}
  });
  document.addEventListener('click', function(e){
    var a = e.target.closest('a');
    if (!a) return;
    var href = (a.getAttribute('href')||'').trim();
    if (!href) return;
    if (
      href.includes('book.html') ||
      href.startsWith('https://calendly.com/') ||
      href.includes('leadconnectorhq') ||
      href.includes('engage.proppy.com.au/widget/booking')
    ) {
      track('cta_book_click', { href: href, text: (a.textContent||'').trim() });
    }
    if (href.startsWith('mailto:')) {
      track('cta_email_click', { href: href });
    }
    if (href.startsWith('tel:')) {
      track('cta_phone_click', { href: href });
    }
    if (href.startsWith('https://wa.me/') || href.startsWith('https://api.whatsapp.com/')) {
      track('cta_whatsapp_click', { href: href });
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
