export default {
  async fetch(request, env, ctx) {
    try {
      const url = new URL(request.url);
      const path = url.pathname.replace(/^\/api\//, '/');
      if (request.method === 'OPTIONS') return new Response('', cors());
      if (path.startsWith('/assessment/resume/') && request.method === 'GET') {
        const token = path.split('/').pop();
        // Token lookup: scan drafts and match token (KV key list requires Durable Objects; store secondary index)
        // Simplified: store token->id pointer
        const id = await env.ASSESS_KV.get(`token:${token}`);
        if (!id) return json({ error:'invalid_token' }, 404);
        const current = await env.ASSESS_KV.get(`draft:${id}`, { type:'json' });
        if (!current) return json({ error:'not_found' }, 404);
        return json({ draft_id: id, data: current.data });
      }
      if (path === '/assessment/draft' && request.method === 'POST') {
        const data = await request.json();
        const id = cryptoRandomId();
        const token = cryptoRandomId();
        const now = Date.now();
        await env.ASSESS_KV.put(`draft:${id}`, JSON.stringify({ data, created: now, updated: now, token }), { expirationTtl: 60 * 60 * 24 * 14 });
        await env.ASSESS_KV.put(`token:${token}`, id, { expirationTtl: 60 * 60 * 24 * 14 });
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
        const answers = body && body.answers || {};
        const analytics = body && body.analytics || {};
        const rule_version = body && body.rule_version || 'v1.0.0';
        const lead = computeLead(answers);
        const engagement = buildEngagement(answers, analytics, rule_version, lead);
        const engagement_id = `eng-${cryptoRandomId().slice(0,8)}`;
        const payload = { engagement, created: Date.now(), status:'submitted' };
        await env.ASSESS_KV.put(`engagement:${engagement_id}`, JSON.stringify(payload), { expirationTtl: 60 * 60 * 24 * 365 });
        return json({ engagement_id, priority: lead.priority, recommended_next_step: lead.recommended_next_step, reason_codes: lead.reason_codes, rule_version });
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

function computeLead(a){
  let score = 0; const reasons = [];
  const tl = get(a,'engagement.timeline');
  const pre = get(a,'finance.preapproval');
  const dep = get(a,'finance.deposit_source');
  const exp = get(a,'motivation.experience');
  const sugg = get(a,'locations.open_to_suggestions');
  const comps = (get(a,'comparables')||[]).filter(Boolean).length;
  if (/^(Now|1–3 months)$/.test(tl||'')) { score+=25; reasons.push('TL_SOON'); }
  if (pre==='Obtained' || pre==='Pending' || pre==='Expired' || dep==='Equity' || dep==='Cash + Equity') { score+=20; reasons.push('FIN_READY'); }
  if (exp==='Experienced' || exp==='Professional') { score+=10; reasons.push('EXP'); }
  if (sugg===true || sugg===undefined) { score+=5; reasons.push('OPEN_SUGG'); }
  if (comps>0) { score+=5; reasons.push('COMPS'); }
  if (tl==='6–12 months') { score-=10; reasons.push('TL_LATER'); }
  let priority='NURTURE'; if (score>=50) priority='HOT'; else if (score>=25) priority='WARM';
  let next='REPORT_SHORTLIST';
  if (pre==='Need help') next='FINANCE_INTRO';
  else if (priority==='HOT') next='BOOK_CALL';
  else if (priority==='WARM') next='SIGNUP_MATCHES';
  return { score, priority, recommended_next_step: next, reason_codes: reasons };
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

function get(obj, path){ if(!path) return undefined; return path.split('.').reduce((o,k)=> (o&&o[k]!==undefined)? o[k]:undefined, obj); }

function set(obj, path, val){ const parts = path.split('.'); let o=obj; while(parts.length>1){ const k=parts.shift(); o=o[k]=o[k]||{}; } o[parts[0]]=val; }

function pickPaths(obj, paths){ const out={}; for(const p of paths){ const v=get(obj,p); if(v!==undefined) set(out,p,v); } return out; }

function safeHost(u){ try{ return new URL(u).hostname; }catch(e){ return ''; } }

function buildEngagement(answers, analytics, rule_version, lead){
  const engagement = {
    client: pickPaths(answers, ['client.first_name','client.last_name','client.email','client.mobile','client.location']),
    motivation: pickPaths(answers, ['motivation.goals','motivation.horizon','motivation.experience','motivation.risk']),
    finance: pickPaths(answers, ['finance.price_band','finance.deposit_band','finance.deposit_source','finance.borrowing_band','finance.preapproval','finance.preapproval_amount','finance.preapproval_expiry']),
    strategy: pickPaths(answers, ['strategy.investment_type','strategy.goal','strategy.target_yield','strategy.target_growth','strategy.reno_budget','strategy.reno_scope','strategy.dev_experience','strategy.dev_planning_risk','strategy.dev_holding']),
    brief: pickPaths(answers, ['brief.property_types','brief.beds_min','brief.beds_max','brief.baths_min','brief.baths_max','brief.construction','brief.land_min','brief.land_max','brief.strata_tolerance','brief.building_style','brief.dual_config','brief.features','brief.additional_requirements','brief.top_priorities','brief.must_avoids']),
    locations: pickPaths(answers, ['locations.states','locations.regions','locations.suburbs','locations.proximity','locations.open_to_suggestions','locations.acceptability_drivers']),
    comparableProperties: (answers.comparables||[]).slice(0,3).map(c=>({ url:c.url, tag:c.tag, source_domain: safeHost(c.url) })),
    engagement: { timeline: get(answers,'engagement.timeline'), status:'submitted' },
    rule_version,
    analytics,
    lead_score: lead.score,
    priority: lead.priority,
    recommended_next_step: lead.recommended_next_step,
    reason_codes: lead.reason_codes
  };
  return engagement;
}
