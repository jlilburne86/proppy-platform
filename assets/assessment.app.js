// Proppy Assessment App (config-driven, v1)
(function(){
  const $ = (s,p)=> (p||document).querySelector(s);
  const $$ = (s,p)=> Array.from((p||document).querySelectorAll(s));
  let schema = null; let answers = {}; let stepOrder = []; let idx = 0; let draft = {};
  let activeGroups = [];

  init();

  async function init(){
    const v = '20260128';
    schema = await fetchJson(path('assets/assessment.schema.json?v='+v));
    const resume = new URLSearchParams(location.search||'').get('resume');
    if (resume){
      try{
        const r = await fetch(`/api/assessment/resume/${encodeURIComponent(resume)}`);
        if (r.ok){ const j = await r.json(); answers = (j && j.data && j.data.answers) || {}; }
      }catch(e){}
    }
    if (!answers || Object.keys(answers).length===0) answers = loadDraft() || {};
    ensureDefaults();
    computeFlow();
    bindNav();
    render();
    track('assessment_start');
  }

  function ensureDefaults(){
    answers.client = answers.client||{};
    answers.motivation = answers.motivation||{};
    answers.finance = answers.finance||{};
    answers.strategy = answers.strategy||{};
    answers.brief = answers.brief||{};
    answers.locations = answers.locations||{ open_to_suggestions:true };
    answers.risk = answers.risk||{};
    answers.engagement = answers.engagement||{};
    answers.comparables = answers.comparables||[];
  }

  function computeFlow(){
    // Derive one-question-per-screen order by step groups; also compute activeGroups for progress
    const visible = window.ProppyEngine.visibleNodes(schema, answers);
    const order = [];
    const groups = [];
    for (const step of schema.steps){
      const nodesInGroup = visible.filter(n=> n.step_group === step.group);
      if (nodesInGroup.length){ groups.push(step.group); nodesInGroup.forEach(n=> order.push(n.id)); }
      if (step.id==='comparables'){ groups.push('comparables'); order.push('comparables'); }
      if (step.id==='summary'){ groups.push('summary'); order.push('summary'); }
    }
    stepOrder = order;
    activeGroups = groups;
  }

  function render(){
    computeFlow();
    const curId = stepOrder[idx]||'summary';
    const root = $('#step-root');
    root.innerHTML = '';
    const head = document.createElement('div');
    const gInfo = groupProgress(curId);
    head.innerHTML = `<div class=\"mb-4\"><div class=\"text-xs text-slate-500\">Step ${gInfo.index+1} of ${gInfo.total}</div><h2 class=\"text-2xl font-extrabold\">${titleFor(curId)}</h2><p class=\"text-slate-600 dark:text-slate-300\">${helperFor(curId)}</p></div>`;
    root.appendChild(head);
    if (curId==='comparables') root.appendChild(renderComparables());
    else if (curId==='summary') root.appendChild(renderSummary());
    else root.appendChild(renderQuestion(curId));
    setProgress();
    // Advance on Enter for non-textarea inputs
    root.onkeydown = (ev)=>{
      if (ev.key === 'Enter' && !ev.shiftKey && !ev.metaKey && !ev.altKey && !ev.ctrlKey){
        const target = ev.target;
        const isTextArea = target && target.tagName === 'TEXTAREA';
        if (!isTextArea){ ev.preventDefault(); goNextIfValid(); }
      }
    };
    renderBrief();
    $('#btn-back').disabled = idx===0;
    $('#btn-next').textContent = idx>=stepOrder.length-1? 'Finish' : 'Continue';
    track('assessment_step_view', { step_id: curId });
  }

  function titleFor(id){
    const step = schema.steps.find(s=> s.id===id) || schema.nodes.find(n=> n.id===id);
    return (step && (step.title||step.prompt)) || 'Assessment';
  }
  function helperFor(id){
    const a = answers;
    // Insight selection based on node + state
    if (id==='preapproval') return 'This keeps your shortlist realistic and avoids unsuitable properties.';
    if (id==='open_to_suggestions' && (a.locations.open_to_suggestions!==false)) return 'We scan beyond familiar areas to find where fundamentals strengthen before headlines.';
    if (id==='property_types' && (a.brief.property_types||[]).includes('Unit/Apartment')) return 'Strata can materially change cashflow—this keeps recommendations aligned.';
    if (id==='investment_type' && a.strategy.investment_type==='Value Add') return 'Your renovation appetite changes both suburbs and property condition we target.';
    if (id==='target_states') return 'Nationwide scan ensures we don’t miss markets where signals are strongest.';
    if (id==='top_priorities') return 'Fast path: we’ll prioritise constraints to accelerate your shortlist.';
    return '';
  }

  function renderQuestion(id){
    const node = schema.nodes.find(n=> n.id===id);
    const wrap = document.createElement('div');
    wrap.className = 'space-y-3';
    const label = document.createElement('label');
    label.className = 'text-sm'; label.textContent = node.prompt;
    wrap.appendChild(label);
    const path = node.maps_to_field;
    const v = get(answers, path);
    const input = buildControl(node, v);
    wrap.appendChild(input);
    return wrap;
  }

  function buildControl(node, value){
    const common = 'mt-1 w-full rounded-xl border-slate-300 dark:border-slate-700';
    const box = document.createElement('div');
    switch(node.type){
      case 'text':
        box.innerHTML = `<input type="text" class="${common}" value="${esc(value||'')}">`;
        box.firstChild.addEventListener('input', e=>{ setVal(node, e.target.value.trim()); });
        break;
      case 'number':
        box.innerHTML = `<input type="number" class="${common}" value="${value||''}">`;
        box.firstChild.addEventListener('input', e=>{ const n=e.target.value; setVal(node, n!==''? Number(n):''); });
        break;
      case 'date':
        box.innerHTML = `<input type=\"date\" class=\"${common}\" value=\"${value||''}\">`;
        box.firstChild.addEventListener('input', e=> { setVal(node, e.target.value); autoAdvance(node); });
        break;
      case 'toggle':
        box.innerHTML = `<label class=\"inline-flex items-center gap-2\"><input type=\"checkbox\" ${value? 'checked':''}> <span>${node.prompt}</span></label>`;
        box.firstChild.querySelector('input').addEventListener('change', e=> { setVal(node, !!e.target.checked); autoAdvance(node); });
        break;
      case 'single_select':
        box.innerHTML = `<select class=\"${common}\"><option value=\"\">Select…</option>${(node.options||[]).map(o=>`<option ${o===value?'selected':''}>${o}</option>`).join('')}</select>`;
        box.firstChild.addEventListener('change', e=> { setVal(node, e.target.value||''); autoAdvance(node); });
        break;
      case 'multi_select':
        box.innerHTML = `<div class="grid grid-cols-1 md:grid-cols-2 gap-2">${(node.options||[]).map(o=>`<label class="flex items-center gap-2 p-2 rounded-xl border border-slate-200 dark:border-slate-700 cursor-pointer"><input type="checkbox" value="${o}" ${(value||[]).includes(o)?'checked':''}> <span>${o}</span></label>`).join('')}</div>`;
        box.querySelectorAll('input[type=checkbox]').forEach(c=> c.addEventListener('change', ()=>{
          const arr = []; box.querySelectorAll('input[type=checkbox]').forEach(x=>{ if (x.checked) arr.push(x.value); });
          setVal(node, arr);
        }));
        break;
      default:
        box.textContent = 'Unsupported field';
    }
    return box;
  }

  function renderComparables(){
    const wrap = document.createElement('div');
    wrap.innerHTML = `
      <p class="text-slate-600 dark:text-slate-300 mb-3">This helps calibrate condition, size and location expectations so our conversation is productive.</p>
      <div id="comp-list" class="space-y-3"></div>
      <button id="comp-add" class="mt-2 inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 font-semibold">+ Add link</button>
    `;
    const root = wrap.querySelector('#comp-list');
    function row(item, i){
      const r = document.createElement('div');
      r.className = 'p-3 rounded-xl border border-slate-200 dark:border-slate-700';
      r.innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div class="md:col-span-2">
            <label class="text-sm">Listing URL</label>
            <input type="url" class="mt-1 w-full rounded-xl border-slate-300 dark:border-slate-700 comp-url" placeholder="https://..." value="${esc(item.url||'')}">
          </div>
          <div>
            <label class="text-sm">Reason tag</label>
            <select class="mt-1 w-full rounded-xl border-slate-300 dark:border-slate-700 comp-tag">
              ${['','LIKED','MISSED','BENCHMARK','UNSURE'].map(t=>`<option ${t===(item.tag||'')?'selected':''} value="${t}">${t||'Select…'}</option>`).join('')}
            </select>
          </div>
        </div>
        <div class="mt-2 flex items-center justify-between text-xs text-slate-500">
          <span>${item.url? host(item.url):''}</span>
          <button type="button" class="text-red-600 comp-del">Remove</button>
        </div>`;
      r.querySelector('.comp-url').addEventListener('input', e=>{ item.url = e.target.value.trim(); saveDraft(); });
      r.querySelector('.comp-tag').addEventListener('change', e=>{ item.tag = e.target.value; saveDraft(); });
      r.querySelector('.comp-del').addEventListener('click', ()=>{ answers.comparables.splice(i,1); saveDraft(); render(); });
      return r;
    }
    function renderList(){
      root.innerHTML = '';
      answers.comparables.forEach((c,i)=> root.appendChild(row(c,i)));
      $('#comp-add', wrap).disabled = answers.comparables.length>=3;
    }
    if (answers.comparables.length===0) answers.comparables.push({ url:'', tag:'' });
    renderList();
    $('#comp-add', wrap).addEventListener('click', ()=>{
      if (answers.comparables.length>=3) return;
      answers.comparables.push({ url:'', tag:'' });
      saveDraft(); renderList(); track('comparable_added', { count: answers.comparables.length, domain: host(answers.comparables.at(-1).url||'') });
    });
    return wrap;
  }

  function renderSummary(){
    const wrap = document.createElement('div');
    const lead = window.ProppyEngine.computeLead(answers);
    wrap.innerHTML = `
      <h3 class="text-xl font-bold mb-2">Summary</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        ${sum('Strategy', answers.strategy.investment_type)}
        ${sum('Timeline', answers.engagement.timeline)}
        ${sum('Budget', answers.finance.price_band)}
        ${sum('Types', (answers.brief.property_types||[]).join(', '))}
        ${sum('States', (answers.locations.states||[]).join(', '))}
        ${sum('Risk', answers.motivation.risk)}
      </div>
      <div class="rounded-2xl border border-slate-200 dark:border-slate-800 p-4 mb-6">
        <h4 class="font-bold mb-2">What happens next</h4>
        <ol class="list-decimal pl-5 space-y-1 text-slate-600 dark:text-slate-300">
          <li>Define the brief</li>
          <li>Scan markets nationwide</li>
          <li>Source and secure the right property</li>
        </ol>
      </div>
      <div class="flex flex-col md:flex-row items-start md:items-center gap-3">
        ${primaryCta(lead)}
        <div class="flex gap-4">${secondaryCtas(lead)}</div>
      </div>
      <p class="mt-3 text-sm text-slate-500">No pressure. Clear, data‑led insights. Speak with an expert, not a salesperson.</p>`;
    wrap.querySelectorAll('[data-ev]').forEach(a=> a.addEventListener('click', ()=> track(a.getAttribute('data-ev'))));
    return wrap;
  }

  function primaryCta(lead){
    if (lead.recommended_next_step==='BOOK_CALL') return `<a data-ev="cta_book_click" href="book.html" class="inline-flex items-center gap-2 px-5 py-3 rounded-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 font-semibold">Book a strategy call<span class="material-symbols-outlined text-sm">arrow_forward</span></a>`;
    if (lead.recommended_next_step==='SIGNUP_MATCHES') return `<a data-ev="cta_signup_click" href="pricing.html" class="inline-flex items-center gap-2 px-5 py-3 rounded-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 font-semibold">Create account to receive matches<span class="material-symbols-outlined text-sm">arrow_forward</span></a>`;
    if (lead.recommended_next_step==='FINANCE_INTRO') return `<a data-ev="cta_finance_click" href="book.html#finance" class="inline-flex items-center gap-2 px-5 py-3 rounded-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 font-semibold">Finance intro + shortlist<span class="material-symbols-outlined text-sm">arrow_forward</span></a>`;
    return `<a data-ev="cta_report_click" href="technology.html" class="inline-flex items-center gap-2 px-5 py-3 rounded-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 font-semibold">Save brief + get shortlist<span class="material-symbols-outlined text-sm">arrow_forward</span></a>`;
  }
  function secondaryCtas(lead){
    const out=[]; if (lead.recommended_next_step!=='BOOK_CALL') out.push(`<a data-ev="cta_book_click" href="book.html" class="text-sm underline">Book a strategy call</a>`);
    if (lead.recommended_next_step!=='SIGNUP_MATCHES') out.push(`<a data-ev="cta_signup_click" href="pricing.html" class="text-sm underline">Create account</a>`);
    if (lead.recommended_next_step!=='REPORT_SHORTLIST') out.push(`<a data-ev="cta_report_click" href="technology.html" class="text-sm underline">Get shortlist/report</a>`);
    return out.join('');
  }

  function renderBrief(){
    const wrap = $('#brief');
    const chip = (k,v)=> v? `<div><span class="text-slate-500">${k}:</span> <span class="font-semibold">${esc(v)}</span></div>`:'';
    const b = [];
    if (answers.client.first_name || answers.client.last_name) b.push(chip('Name', [answers.client.first_name,answers.client.last_name].filter(Boolean).join(' ')));
    if (answers.client.email) b.push(chip('Email', answers.client.email));
    if (answers.client.location) b.push(chip('Location', answers.client.location));
    if (answers.strategy.investment_type) b.push(chip('Strategy', answers.strategy.investment_type));
    if (answers.engagement.timeline) b.push(chip('Timeline', answers.engagement.timeline));
    if (answers.finance.price_band) b.push(chip('Budget', answers.finance.price_band));
    if (answers.brief.property_types && answers.brief.property_types.length) b.push(chip('Types', answers.brief.property_types.join(', ')));
    if (answers.locations.states && answers.locations.states.length) b.push(chip('States', answers.locations.states.join(', ')));
    $('#brief').innerHTML = b.join('');
  }

  function bindNav(){
    $('#btn-back').addEventListener('click', ()=>{ if (idx>0){ idx--; render(); }});
    $('#btn-save').addEventListener('click', async ()=>{ await serverDraft('POST'); alert('Saved. You can resume later.'); });
    $('#btn-next').addEventListener('click', async ()=>{ await goNextIfValid(true); });
  }

  async function goNextIfValid(fromClick){
    const errs = window.ProppyEngine.validate(schema, answers);
    const curId = stepOrder[idx];
    const curErr = errs.find(e=> e.id===curId);
    if (curErr) { if (fromClick) alert('Please complete required fields.'); return false; }
    track('assessment_step_complete', { step_id: curId });
    if (idx < stepOrder.length-1){ idx++; render(); return true; }
    else {
      const resp = await serverSubmit();
      let lead = null;
      if (resp && resp.recommended_next_step){ lead = { recommended_next_step: resp.recommended_next_step }; }
      if (!lead) lead = window.ProppyEngine.computeLead(answers);
      track('assessment_submit', { next: lead.recommended_next_step });
      redirectToRecommended(lead);
      return true;
    }
  }

  function setVal(node, val){ set(answers, node.maps_to_field, val); saveDraft(); renderBrief(); }

  function setProgress(){
    const curId = stepOrder[idx]||'summary';
    const g = groupProgress(curId);
    const pct = Math.round(((g.index+1)/Math.max(1,g.total))*100);
    $('#progress-bar').style.width = Math.max(8, pct) + '%';
  }

  function groupFor(id){
    if (id==='comparables' || id==='summary') return id;
    const n = schema.nodes.find(x=> x.id===id);
    return n && n.step_group || 'start';
  }
  function groupProgress(id){
    const grp = groupFor(id);
    const idxG = Math.max(0, activeGroups.indexOf(grp));
    return { index: idxG, total: Math.max(1, activeGroups.length) };
  }

  function autoAdvance(node){
    if (node.type === 'single_select' || node.type === 'toggle' || node.type === 'date'){
      setTimeout(()=> { goNextIfValid(false); }, 40);
    }
  }

  function saveDraft(){ try{ localStorage.setItem('assessmentDraftV2', JSON.stringify(answers)); }catch(e){} }
  function loadDraft(){ try{ return JSON.parse(localStorage.getItem('assessmentDraftV2')||''); }catch(e){ return null; } }

  async function serverDraft(method){
    try{
      const res = await fetch('/api/assessment/draft', { method: method||'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({ answers, rule_version: schema.rule_version, analytics: gatherAttribution() }) });
      if (!res.ok) return null; return await res.json();
    }catch(e){ return null; }
  }
  async function serverSubmit(){
    try{
      const res = await fetch('/api/assessment/submit', { method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({ answers, rule_version: schema.rule_version, analytics: gatherAttribution() }) });
      if (!res.ok) return null; return await res.json();
    }catch(e){ return null; }
  }

  function gatherAttribution(){
    let ref=''; try{ ref=document.referrer||''; }catch(e){}
    const qs = new URLSearchParams(location.search||'');
    const obj = {};
    ['utm_source','utm_medium','utm_campaign','utm_term','utm_content'].forEach(k=>{ if (qs.get(k)) obj[k]=qs.get(k); });
    obj.referrer = ref; obj.landing_page = location.pathname + location.search; obj.first_touch_ts = Number(localStorage.getItem('ass_ft')||Date.now()); obj.last_touch_ts = Date.now(); localStorage.setItem('ass_ft', String(obj.first_touch_ts));
    return obj;
  }

  function fetchJson(url){ return fetch(url).then(r=>r.json()); }
  function path(p){ return (window.ghBasePath? window.ghBasePath(''+p): p); }
  function esc(s){ return String(s||'').replace(/[&<>"']/g, c=> ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'&#39;'}[c])); }
  function sum(k,v){ if(!v) return ''; return `<div><div class="text-slate-500 text-sm">${k}</div><div class="font-semibold">${esc(v)}</div></div>`; }
  function host(u){ try{ return new URL(u).hostname; }catch(e){ return ''; } }
  function get(o,p){ return p.split('.').reduce((x,k)=> (x&&x[k]!==undefined)? x[k]:undefined, o); }
  function set(o,p,v){ const parts=p.split('.'); let x=o; while(parts.length>1){ const k=parts.shift(); x=x[k]=x[k]||{}; } x[parts[0]]=v; }
  function track(ev, params){ try{ if (typeof window.gtag==='function') gtag('event', ev, params||{}); }catch(e){} }
  function redirectToRecommended(lead){
    const qs = location.search || '';
    let href = 'technology.html';
    if (lead && lead.recommended_next_step==='BOOK_CALL') href = 'book.html';
    else if (lead && lead.recommended_next_step==='SIGNUP_MATCHES') href = 'pricing.html';
    else if (lead && lead.recommended_next_step==='FINANCE_INTRO') href = 'book.html#finance';
    location.assign(href + qs);
  }
})();
