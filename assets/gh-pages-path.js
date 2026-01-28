(() => {
  try {
    if (!/\.github\.io$/i.test(location.hostname)) return;
    var parts = location.pathname.split('/').filter(Boolean);
    if (!parts.length) return;
    var repo = '/' + parts[0];
    function fix(u){ return (u && u.startsWith('/')) ? (repo + u) : u; }
    document.querySelectorAll('a[href^="/"]').forEach(a => { a.href = fix(a.getAttribute('href')); });
    document.querySelectorAll('img[src^="/"]').forEach(img => { img.src = fix(img.getAttribute('src')); });
    document.querySelectorAll('link[href^="/"]').forEach(l => { l.href = fix(l.getAttribute('href')); });
    document.querySelectorAll('script[src^="/"]').forEach(s => { s.src = fix(s.getAttribute('src')); });
    document.querySelectorAll('meta[property="og:image"], meta[name="twitter:image"]').forEach(m => {
      var c = m.getAttribute('content');
      if (c && c.startsWith('/')) m.setAttribute('content', repo + c);
    });
  } catch (e) {}
})();

