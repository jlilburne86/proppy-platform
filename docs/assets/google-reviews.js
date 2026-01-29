(() => {
  async function loadJSON(url){
    try { const r = await fetch(url, { cache: 'no-store' }); if(!r.ok) return null; return await r.json(); } catch(e){ return null; }
  }
  function stars(n){
    n = Math.max(0, Math.min(5, Number(n)||0));
    let s = '';
    for(let i=1;i<=5;i++) s += `<span class="material-symbols-outlined text-amber-500 align-middle">${i<=n?'grade':'star_rate'}</span>`;
    return s;
  }
  function card(r){
    const photo = r.profile_photo_url || 'https://maps.gstatic.com/mapfiles/place_api/icons_v1/png_71/geocode-71.png';
    const name = r.author_name || 'Google User';
    const text = (r.text||'').replace(/</g,'&lt;');
    const t = r.relative_time_description || '';
    const url = r.author_url || '#';
    return `<div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-sm">
      <div class="flex items-center gap-3 mb-2">
        <img src="${photo}" alt="${name}" class="w-10 h-10 rounded-full object-cover"/>
        <div>
          <div class="font-semibold text-sm"><a class="hover:underline" href="${url}" target="_blank" rel="noopener">${name}</a></div>
          <div class="text-xs text-slate-500">${t}</div>
        </div>
      </div>
      <div class="mb-2">${stars(r.rating)}</div>
      <p class="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">${text}</p>
    </div>`;
  }
  async function boot(){
    const el = document.getElementById('google-reviews');
    if(!el) return;
    const data = await loadJSON('data/google-reviews.json');
    if(!data || !Array.isArray(data.reviews)) return;
    const reviews = data.reviews.filter(r => (Number(r.rating)||0) >= 3);
    const head = `<div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-extrabold">What clients say</h2>
        <a class="text-sm font-semibold underline" target="_blank" rel="noopener" href="https://www.google.com/search?q=Proppy+Melbourne+reviews">See all on Google</a>
      </div>`;
    const grid = `<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">${reviews.map(card).join('')}</div>`;
    el.innerHTML = head + grid;
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();

