// Route specific booking CTAs to book.html with a calendar override
(function(){
  function mergeParams(url, extra){
    try{
      var u = new URL(url, location.href);
      var cur = new URL(location.href);
      // carry UTM params
      cur.searchParams.forEach(function(v,k){ if(/^utm_/i.test(k) && !u.searchParams.has(k)) u.searchParams.set(k,v); });
      // merge any extras
      if (extra) Object.keys(extra).forEach(function(k){ u.searchParams.set(k, extra[k]); });
      return u.toString();
    }catch(e){ return url; }
  }
  document.addEventListener('click', function(e){
    var a = e.target.closest('a[data-booking-url]');
    if (!a) return;
    var cal = a.getAttribute('data-booking-url');
    if (!cal) return;
    e.preventDefault();
    var dest = mergeParams('book.html', { calendar: cal });
    location.assign(dest);
  }, true);
})();

