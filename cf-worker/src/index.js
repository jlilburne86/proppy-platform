export default {
  async fetch(request, env, ctx) {
    try {
      const url = new URL(request.url);
      const path = url.pathname.replace(/^\/api\//, '/');
      if (request.method === 'OPTIONS') return new Response('', cors());
      if (path === '/assessment/draft' && request.method === 'POST') {
        const data = await request.json();
        const id = cryptoRandomId();
        const token = cryptoRandomId();
        const now = Date.now();
        await env.ASSESS_KV.put(`draft:${id}`, JSON.stringify({ data, created: now, updated: now, token }), { expirationTtl: 60 * 60 * 24 * 14 });
        const base = env.PUBLIC_BASE_URL || `${url.protocol}//${url.host}`;
        return json({ draft_id: id, resume_token: token, resume_url: `${base}/assessment.html?resume=${token}`, expires_at: now + 14*864e5 });
      }
      if (path.startsWith('/assessment/draft/') && request.method === 'PATCH') {
        const id = path.split('/').pop();
        const current = await env.ASSESS_KV.get(`draft:${id}`, { type: 'json' });
        if (!current) return json({ error: 'not_found' }, 404);
        const patch = await request.json();
        current.data = { ...(current.data||{}), ...(patch||{}) };
        current.updated = Date.now();
        await env.ASSESS_KV.put(`draft:${id}`, JSON.stringify(current), { expirationTtl: 60 * 60 * 24 * 14 });
        return json({ ok: true });
      }
      if (path === '/assessment/submit' && request.method === 'POST') {
        const body = await request.json();
        const brief = body && body.brief || body || {};
        const route = computeRouting(brief);
        const engagement_id = `eng-${cryptoRandomId().slice(0,8)}`;
        await env.ASSESS_KV.put(`engagement:${engagement_id}`, JSON.stringify({ brief, route, created: Date.now() }), { expirationTtl: 60 * 60 * 24 * 365 });
        return json({ engagement_id, priority: route.priority, next_action: route.next });
      }
      if (path === '/listing/preview' && request.method === 'GET') {
        const target = url.searchParams.get('url');
        if (!target) return json({ ok:false, error:'missing_url' }, 400);
        const ok = isAllowedPreview(target, env.ALLOWED_PREVIEW_DOMAINS);
        if (!ok) return json({ ok:false, error:'domain_not_allowed' }, 400);
        try {
          const resp = await fetch(target, { redirect: 'follow', cf: { cacheEverything: true, cacheTtl: 300 }});
          const html = await resp.text();
          const og = extractOG(html);
          return json({ ok:true, ...og });
        } catch (e) {
          return json({ ok:false, error:'fetch_failed' }, 500);
        }
      }
      return json({ error: 'not_found' }, 404);
    } catch (e) {
      return json({ error: 'server_error' }, 500);
    }
  }
}

function cors() {
  return { headers: { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET,POST,PATCH,OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type' } }
}
function json(obj, status=200) { return new Response(JSON.stringify(obj), { status, headers: { 'content-type':'application/json', 'Access-Control-Allow-Origin': '*' } }); }
function cryptoRandomId() { return [...crypto.getRandomValues(new Uint8Array(16))].map(b=>b.toString(16).padStart(2,'0')).join(''); }

function computeRouting(b){
  const soon = /^(Now|1–3 months)$/.test(b.timeline||'');
  const fin = (b.preapproval==='In progress' || b.preapproval==='Obtained' || b.deposit_source==='Equity' || b.deposit_source==='Mix');
  const stratSet = (b.strategy && !/^Not sure/.test(b.strategy));
  if (soon && fin && stratSet) return { priority:'Hot', next:'book' };
  if (stratSet && (b.timeline==='3–6 months' || (b.timeline && !fin))) return { priority:'Warm', next:'trial' };
  return { priority:'Nurture', next:'report' };
}

function isAllowedPreview(target, list){
  try {
    const h = new URL(target).hostname.replace(/^www\./,'');
    const allowed = (list || 'realestate.com.au,domain.com.au').split(/[,\s]+/).filter(Boolean);
    return allowed.some(d => h.endsWith(d));
  } catch(e){ return false; }
}

function extractOG(html){
  const get = (p)=>{
    const m = html.match(new RegExp(`<meta[^>]+property=[\"\']${p}[\"\'][^>]+content=[\"\']([^\"\']+)[\"\']`, 'i'));
    return m && m[1];
  };
  const title = get('og:title') || get('twitter:title') || '';
  const image = get('og:image') || get('twitter:image') || '';
  let site = get('og:site_name') || '';
  if (!site) { const m = html.match(/<title>([^<]+)/i); site = (m && m[1]) || ''; }
  return { title, image, site };
}

