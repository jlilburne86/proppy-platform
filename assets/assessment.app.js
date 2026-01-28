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
    answers.strategy = answers.strategy||{ auto_mapped: true };
    answers.brief = answers.brief||{};
    answers.locations = answers.locations||{ open_to_suggestions:true };
    if (!answers.client.country) answers.client.country = 'Australia';
    if (!Array.isArray(answers.locations.states) || answers.locations.states.length===0){
      answers.locations.states = ['Australia-wide'];
    }
    answers.risk = answers.risk||{};
    answers.engagement = answers.engagement||{};
    answers.comparables = answers.comparables||[];
  }

  function computeFlow(){
    // One screen per group; record activeGroups and stepOrder as groups
    const visible = window.ProppyEngine.visibleNodes(schema, answers);
    const groups = [];
    for (const step of schema.steps){
      const nodesInGroup = visible.filter(n=> n.step_group === step.group);
      if (nodesInGroup.length){ groups.push(step.group); }
      if (step.id==='comparables'){ groups.push('comparables'); }
    }
    activeGroups = groups;
    stepOrder = groups;
  }

  function render(){
    computeFlow();
    const curId = stepOrder[idx]||activeGroups[activeGroups.length-1];
    const root = $('#step-root');
    root.innerHTML = '';
    const head = document.createElement('div');
    const gInfo = groupProgress(curId);
    const hpObj = proppyHelp(curId);
    const helpLine = hpObj? `<p class=\"text-xs text-slate-500 dark:text-slate-400 mt-1\">How Proppy helps: ${esc(hpObj.text||hpObj)} ${hpObj.href? `<a href=\\\"${hpObj.href}\\\" class=\\\"underline insight-link\\\" data-step=\\\"${curId}\\\" target=\\\"_blank\\\" rel=\\\"noopener\\\">Learn more</a>`: ''}</p>` : '';
    head.innerHTML = `<div class=\"mb-4 animate-fadeIn\"><div class=\"text-xs text-slate-500\">Step ${gInfo.index+1} of ${gInfo.total}</div><h2 class=\"text-2xl font-extrabold\">${titleFor(curId)}</h2><p class=\"text-slate-600 dark:text-slate-300\">${helperFor(curId)}</p>${helpLine}</div>`;
    root.appendChild(head);
    if (curId==='comparables') root.appendChild(renderComparables());
    else root.appendChild(renderGroup(curId));
    setProgress();
    // Bind insight link tracking
    root.querySelectorAll('.insight-link').forEach(a=>{ if(!a._wired){ a._wired=true; a.addEventListener('click', ()=> track('insight_learn_more_click', { step: a.getAttribute('data-step')||curId, href: a.getAttribute('href')||'' })); }});
    if (hpObj){ track('insight_view', { step: curId, href: hpObj.href||'' }); }
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
    if (id==='preapproval') return 'This keeps your brief realistic and avoids unsuitable properties.';
    if (id==='open_to_suggestions' && (a.locations.open_to_suggestions!==false)) return 'We include areas you may not have considered when fundamentals align.';
    if (id==='property_types' && (a.brief.property_types||[]).includes('Unit/Apartment')) return 'Strata can materially change cashflow—this keeps recommendations aligned.';
    if (id==='target_states') return 'Choose states to consider, or keep it Australia‑wide for the broadest historical view.';
    if (id==='top_priorities') return 'Fast path: we’ll prioritise constraints to accelerate alignment.';
    return '';
  }

  function proppyHelp(groupId){
    const map = {
      start: { text: 'We’re buy‑side only, data‑led, and held to outcomes. Your brief shapes everything we show next.', href: 'guarantee.html' },
      location: { text: 'We consider nationwide signals and historical outcomes to surface candidate areas that fit your brief—no hype, no predictions.', href: 'technology.html' },
      goals: { text: 'We map goals to proven strategies (Set & Forget vs Value Add) and align constraints so you see the right stock sooner.', href: 'how-it-works.html' },
      timing: { text: 'Timing and experience guide how fast we move and how we negotiate; hot paths get streamlined sourcing.', href: 'how-it-works.html' },
      finance: { text: 'Budget and pre‑approval sharpen your target list and strengthen negotiation; we can introduce lending if needed.', href: 'advantage.html' },
      property: { text: 'We avoid oversupplied stock and poor strata; filters are tuned to scarcity, rentability, and long‑term resilience.', href: 'technology.html' },
      comparables: { text: 'Your examples calibrate condition and location expectations so the first shortlist is on‑target.', href: 'how-it-works.html' }
    };
    return map[groupId] || null;
  }

  function renderGroup(group){
    const wrap = document.createElement('div');
    wrap.className = 'space-y-4 animate-fadeIn';
    const nodes = window.ProppyEngine.visibleNodes(schema, answers).filter(n=> n.step_group===group);
    nodes.forEach(node=>{
      const row = document.createElement('div');
      row.className = 'space-y-2 animate-slideUp';
      const label = document.createElement('label');
      label.className = 'text-sm'; label.textContent = node.prompt;
      row.appendChild(label);
      const v = get(answers, node.maps_to_field);
      const input = buildControl(node, v);
      row.appendChild(input);
      wrap.appendChild(row);
    });
    // Start step: add privacy note
    if (group === 'start'){
      const priv = document.createElement('div');
      priv.className = 'text-xs text-slate-500 dark:text-slate-400';
      priv.innerHTML = 'We use this to prepare your brief and next steps. See our <a href="privacy.html" class="underline" target="_blank" rel="noopener">Privacy Policy</a>.';
      wrap.appendChild(priv);
    }
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
        if (node.id === 'strategy_goal'){
          const hint = document.createElement('div');
          hint.className = 'text-xs text-slate-500 dark:text-slate-400 mt-1';
          hint.textContent = 'Tip: We auto-map based on your goals (Yield → High Yield, Growth → High Growth, Balanced/Scale → Balanced). You can override.';
          box.appendChild(hint);
        } else if (node.id === 'country'){
          const hint = document.createElement('div');
          hint.className = 'text-xs text-slate-500 dark:text-slate-400 mt-1';
          hint.textContent = 'If you live outside Australia, we’ll include FIRB guidance in your next steps.';
          box.appendChild(hint);
        }
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
      <div class="flex items-center gap-3 mt-2">
        <button id="comp-add" class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 font-semibold">+ Add link</button>
        <button id="comp-skip" class="text-sm underline" type="button">Skip this step</button>
      </div>
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
    renderList();
    $('#comp-add', wrap).addEventListener('click', ()=>{
      if (answers.comparables.length>=3) return;
      answers.comparables.push({ url:'', tag:'' });
      saveDraft(); renderList(); track('comparable_added', { count: answers.comparables.length, domain: host(answers.comparables.at(-1).url||'') });
    });
    const skipBtn = $('#comp-skip', wrap);
    if (skipBtn) skipBtn.addEventListener('click', ()=>{ goNextIfValid(true); });
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
    if (answers.client.country) b.push(chip('Country', answers.client.country==='Other'? (answers.client.country_other||'Other') : answers.client.country));
    if (answers.client.country==='Australia' && answers.client.state) b.push(chip('State', answers.client.state));
    if (answers.strategy.investment_type) b.push(chip('Strategy', answers.strategy.investment_type));
    if (answers.engagement.timeline) b.push(chip('Timeline', answers.engagement.timeline));
    if (answers.finance.price_band) b.push(chip('Budget', answers.finance.price_band));
    if (answers.brief.property_types && answers.brief.property_types.length) b.push(chip('Types', answers.brief.property_types.join(', ')));
    if (answers.locations.states && answers.locations.states.length) b.push(chip('States', answers.locations.states.join(', ')));
    $('#brief').innerHTML = b.join('');
    renderEngine();
  }

  function renderEngine(){
    const ul = $('#engine'); if (!ul) return;
    const items = computeHighlights();
    const sig = computeSignals();
    const scope = computeScope();
    // Render meter
    const bar = $('#signals-bar'); const lab = $('#signals-label');
    if (bar) bar.style.width = Math.max(5, Math.min(100, sig.score)) + '%';
    if (lab) lab.textContent = sig.label;
    // Render breakdown
    const infoBtn = $('#signals-info'); const bd = $('#signals-breakdown');
    if (bd) bd.innerHTML = sig.breakdown.map(b=> `<li class="flex items-center justify-between"><span>${esc(b.label)}</span><span class="font-semibold ${b.points>=0?'text-emerald-600':'text-rose-600'}">${b.points>0?'+':''}${b.points}</span></li>`).join('');
    if (infoBtn && bd && !infoBtn._wired){ infoBtn._wired = true; infoBtn.addEventListener('click', ()=>{ bd.classList.toggle('hidden'); }); }
    const howBtn = document.getElementById('signals-how');
    if (howBtn && !howBtn._wired){ howBtn._wired = true; howBtn.addEventListener('click', ()=> showSignalsModal()); }
    // Render scope chip
    const chip = $('#scope-chip'); if (chip) chip.textContent = scope;
    ul.innerHTML = items.map(i=> `<li class="flex items-start gap-2"><span class="material-symbols-outlined text-accent">${esc(i.icon||'check_circle')}</span><div><div class="font-semibold">${esc(i.title)}</div><div class="text-slate-500 dark:text-slate-400 text-xs">${esc(i.desc)}</div></div></li>`).join('');
    renderHistorical();
  }

  let _proppyData = null;
  let _historicalFocus = '5y'; // '5y' or '10y'
  async function loadProppy(){ if (_proppyData) return _proppyData; try{ const r = await fetch(path('data/proppydata.json')); _proppyData = await r.json(); return _proppyData; }catch(e){ _proppyData=[]; return _proppyData; } }

  function isSuburbRow(row){
    const lvl = String(row.areaLevel||'');
    const slug = String(row.slug||'');
    return /suburb/i.test(lvl) || /^suburb-/.test(slug);
  }

  function matchesCohort(row){
    const type = (answers.brief.property_types||[])[0] || '';
    const mapType = t=> t.includes('Unit')? 'Units' : 'Houses';
    const rowType = (row.type||'').toLowerCase();
    const wantType = mapType(type).toLowerCase();
    if (type && rowType && rowType.indexOf(wantType)===-1) return false;
    const beds = Number(answers.brief.beds_min||0);
    const rb = String(row.bedrooms||'All');
    if (rb!=='All'){ const nb = parseInt(rb,10); if (!isNaN(nb) && nb < beds) return false; }
    // budget
    const band = answers.finance.price_band || '';
    const tp = Number(row.typicalPrice||0);
    if (band && tp){
      const m = band.match(/(\d+[\.,]?\d*)\s*[kKmM]?\s*[–-]\s*(\d+[\.,]?\d*)\s*([kKmM]?)/);
      if (m){
        const a = parseFloat(m[1].replace(',','')); const b = parseFloat(m[2].replace(',',''));
        const unit = m[3]||'';
        const toNum = (v)=> /m/i.test(unit)? v*1_000_000 : v*1_000;
        const lo = toNum(a), hi = toNum(b);
        if (tp < lo || tp > hi) return false;
      }
    }
    // state filter
    const states = answers.locations.states||[];
    if (states.length && !states.includes('Australia-wide')){
      const st = String(row.stateName||'').toUpperCase();
      if (!states.includes(st)) return false;
    }
    return true;
  }

  function bandFrom(str, jitter=0){
    if (!str) return '—';
    const n = parseFloat(String(str).replace('%',''));
    if (isNaN(n)) return String(str);
    const lo = Math.max(-100, n - (4 + jitter));
    const hi = Math.min(200, n + (4 + jitter));
    return `${lo.toFixed(0)}–${hi.toFixed(0)}%`;
  }

  async function renderHistorical(){
    const box = document.getElementById('historical'); if (!box) return;
    // Need minimum info
    if (!answers.finance.price_band || !(answers.brief.property_types||[]).length || !answers.brief.beds_min){ box.classList.add('hidden'); return; }
    const data = await loadProppy(); if (!data || !data.length){ box.classList.add('hidden'); return; }
    // filter and score
    const rows = data.filter(matchesCohort);
    if (!rows.length){ box.classList.add('hidden'); return; }
    // group by state, prefer suburb rows
    const byState = new Map();
    rows.forEach(r=>{
      const st = String(r.stateName||'OTHER').toUpperCase();
      if (!byState.has(st)) byState.set(st, []);
      byState.get(st).push(r);
    });
    // seeded sort helper
    const seed = 137;
    const h = s=>{ let x=seed; for(let i=0;i<s.length;i++){ x = (x*31 + s.charCodeAt(i)) & 0xffffffff; } return (x>>>0)/0xffffffff; };
    // pick up to 2 per state, prefer user-selected states first
    const picks = [];
    const sel = (answers.locations.states||[]).filter(s=> s && s!=='Australia-wide').map(s=> s.toUpperCase());
    const allStates = Array.from(byState.keys());
    const orderedStates = sel.length? [...sel.filter(s=> byState.has(s)), ...allStates.filter(s=> !sel.includes(s))] : allStates;
    for (const st of orderedStates){
      const arr = byState.get(st)||[];
      if (!arr.length) continue;
      const suburbFirst = arr.sort((a,b)=> (isSuburbRow(b)?1:0)-(isSuburbRow(a)?1:0) || (b.avgScore||0)-(a.avgScore||0));
      const shuffled = suburbFirst.sort((a,b)=> h(String(a.slug||a.area||'')) - h(String(b.slug||b.area||'')));
      shuffled.slice(0,2).forEach(x=> { if (picks.length<8) picks.push(x); });
      if (picks.length>=8) break; // safety cap before final limit
    }
    // limit total cards to 4
    const finalPicks = picks.slice(0,4);
    const cards = finalPicks.map((r,i)=>{
      const label = (String(r.area||'').replace(/<[^>]+>/g,'').replace(/,\s*AUSTRALIA/i,'')|| `${r.slug||''}`).replace(/\s+\(.*\)$/, '').trim();
      const price5 = bandFrom(r.price5yGrowth, i);
      const price10 = bandFrom(r.price10yGrowth, i);
      const cagr = bandFrom(r.gsp5, i);
      const rent5 = bandFrom(r.rent5yGrowth, i);
      const yieldNow = r.grossYield || '—';
      const vacTrend = (parseFloat(String(r.stVacancyRate||'0'))<0)? 'Vacancy ↓' : 'Vacancy ↔';
      const invTrend = (parseFloat(String(r.stInventory||'0'))<0)? 'Inventory ↓' : 'Inventory ↔';
      const fit = r.avgScore || 0;
      const why = [
        `Budget aligned with typical entry (~${Number(r.typicalPrice||0).toLocaleString()})`,
        `Vacancy trend: ${vacTrend.replace(/\s.*/, '')}`,
        `Inventory trend: ${invTrend.replace(/\s.*/, '')}`
      ];
      const priceLine = _historicalFocus==='10y'
        ? `<div>Price 10y: <span class=\"font-semibold\">${esc(price10)}</span></div><div>CAGR 5y: <span class=\"font-semibold\">${esc(cagr)}</span></div>`
        : `<div>Price 5y: <span class=\"font-semibold\">${esc(price5)}</span></div><div>Rent 5y: <span class=\"font-semibold\">${esc(rent5)}</span></div>`;
      return `<div class=\"rounded-xl border border-slate-200 dark:border-slate-800 p-3\">
        <div class=\"flex items-center justify-between mb-1\"><div class=\"font-semibold\">${esc(label)}</div><span class=\"text-xs bg-accent/10 text-accent px-2 py-0.5 rounded-full\">Fit ${fit}</span></div>
        <div class=\"grid grid-cols-2 gap-2 text-xs text-slate-600 dark:text-slate-300\">
          ${priceLine}
          <div>Yield now: <span class=\"font-semibold\">${esc(yieldNow)}</span></div>
          <div>Risk: <span class=\"font-semibold\">${esc(vacTrend)}, ${esc(invTrend)}</span></div>
        </div>
        <ul class=\"mt-2 text-[11px] text-slate-500 dark:text-slate-400 list-disc pl-5\">${why.map(w=>`<li>${esc(w)}</li>`).join('')}</ul>
      </div>`;
    }).join('');
    document.getElementById('historical-cards').innerHTML = cards;
    box.classList.remove('hidden');
    // analytics
    track('historical_fit_view', { count: finalPicks.length, focus: _historicalFocus, states: (answers.locations.states||[]).join(',') });
    // wire toggle buttons once
    const b5 = document.getElementById('hf-5y'); const b10 = document.getElementById('hf-10y');
    function setActive(){ if(!b5||!b10) return; b5.classList.toggle('bg-slate-200', _historicalFocus==='5y'); b10.classList.toggle('bg-slate-200', _historicalFocus==='10y'); }
    if (b5 && !b5._wired){ b5._wired=true; b5.addEventListener('click', ()=>{ _historicalFocus='5y'; track('historical_focus_toggle', { focus:'5y' }); renderHistorical(); setActive(); }); }
    if (b10 && !b10._wired){ b10._wired=true; b10.addEventListener('click', ()=>{ _historicalFocus='10y'; track('historical_focus_toggle', { focus:'10y' }); renderHistorical(); setActive(); }); }
    setActive();
  }

  function computeHighlights(){
    const out = [];
    // Fast path
    const soon = /^(Now|1–3 months)$/.test(answers.engagement.timeline||'');
    const finHelp = answers.finance.preapproval==='Need help';
    if (soon && !finHelp){ out.push({ icon:'bolt', title:'Fast Path enabled', desc:'We’ll prioritise constraints to accelerate your shortlist.' }); }
    // Finance readiness
    const pre = answers.finance.preapproval;
    if (pre==='Obtained' || pre==='Pending'){ out.push({ icon:'verified', title:'Finance readiness', desc:`Pre-approval ${pre.toLowerCase()}. We’ll keep scope realistic.` }); }
    else if (pre==='Need help'){ out.push({ icon:'account_balance', title:'Finance intro', desc:'We’ll queue a lending intro alongside your shortlist.' }); }
    // Strategy
    if (answers.strategy && answers.strategy.goal){ out.push({ icon:'track_changes', title:'Strategy focus', desc: `${answers.strategy.goal} focus shapes markets and stock.` }); }
    // Property focus
    if (answers.brief.property_types && answers.brief.property_types.length){ out.push({ icon:'home', title:'Property focus', desc: answers.brief.property_types.join(', ') }); }
    // Suggestions
    if (answers.locations.open_to_suggestions!==false){ out.push({ icon:'travel_explore', title:'Nationwide coverage', desc:'We include areas beyond the familiar when fundamentals align.' }); }
    else if (answers.locations.acceptability_drivers && answers.locations.acceptability_drivers.length){ out.push({ icon:'tune', title:'Location constraints', desc: answers.locations.acceptability_drivers.join(', ') }); }
    return out.slice(0,5);
  }

  function computeSignals(){
    let score = 0; const breakdown = [];
    // timing
    if (/^(Now|1–3 months)$/.test(answers.engagement.timeline||'')) { score += 30; breakdown.push({label:'Timeline soon', points:30}); }
    else if (answers.engagement.timeline) { score += 10; breakdown.push({label:'Timeline set', points:10}); }
    // finance
    const pre = answers.finance.preapproval;
    if (pre==='Obtained') { score += 25; breakdown.push({label:'Finance obtained', points:25}); }
    else if (pre==='Pending') { score += 15; breakdown.push({label:'Finance pending', points:15}); }
    else if (pre==='Expired') { score += 10; breakdown.push({label:'Finance expired', points:10}); }
    else if (pre==='Need help') { score += 5; breakdown.push({label:'Needs finance help', points:5}); }
    // experience
    if (answers.motivation.experience==='Experienced' || answers.motivation.experience==='Professional') { score += 10; breakdown.push({label:'Experienced', points:10}); }
    // suggestions openness
    if (answers.locations.open_to_suggestions!==false) { score += 10; breakdown.push({label:'Open to suggestions', points:10}); }
    // comparables
    const comps = (answers.comparables||[]).filter(c=> c && c.url).length; if (comps>0) { score += 5; breakdown.push({label:'Comparables added', points:5}); }
    score = Math.max(0, Math.min(100, score));
    const label = score>=70? 'Strong' : score>=35? 'Medium' : 'Early';
    return { score, label, breakdown };
  }

  function computeScope(){
    const parts = [];
    if (answers.finance.price_band) parts.push(`Budget ${answers.finance.price_band}`);
    if (answers.locations.states && answers.locations.states.length) parts.push(answers.locations.states.join(', '));
    if (answers.brief.property_types && answers.brief.property_types.length) parts.push(answers.brief.property_types.join(', '));
    if (answers.brief.beds_min) parts.push(`${answers.brief.beds_min}+ bed`);
    if (answers.brief.baths_min) parts.push(`${answers.brief.baths_min}+ bath`);
    return parts.join(' • ');
  }

  function bindNav(){
    $('#btn-back').addEventListener('click', ()=>{ if (idx>0){ idx--; render(); }});
    $('#btn-save').addEventListener('click', async ()=>{ await serverDraft('POST'); alert('Saved. You can resume later.'); });
    $('#btn-next').addEventListener('click', async ()=>{ await goNextIfValid(true); });
  }

  async function goNextIfValid(fromClick){
    const errs = window.ProppyEngine.validate(schema, answers);
    const curGroup = stepOrder[idx];
    const groupNodeIds = window.ProppyEngine.visibleNodes(schema, answers).filter(n=> n.step_group===curGroup).map(n=> n.id);
    const curErr = errs.find(e=> groupNodeIds.includes(e.id));
    if (curErr) { if (fromClick) alert('Please complete required fields.'); return false; }
    track('assessment_step_complete', { step_id: curGroup });
    if (idx < stepOrder.length-1){ await analyzeThen(()=>{ idx++; render(); }); return true; }
    else {
      const resp = await serverSubmit();
      let lead = null;
      if (resp && resp.recommended_next_step){ lead = { recommended_next_step: resp.recommended_next_step }; }
      if (!lead) lead = window.ProppyEngine.computeLead(answers);
      track('assessment_submit', { next: lead.recommended_next_step });
      await analyzeThen(()=> renderFinalNextSteps(lead), 'Finalising brief…');
      return true;
    }
  }

  async function analyzeThen(fn, label){
    try{
      const root = document.getElementById('step-root');
      if (!root) { fn(); return; }
      const overlay = document.createElement('div');
      overlay.className = 'analyze-overlay bg-white/90 dark:bg-slate-900/90 flex items-center justify-center z-40';
      overlay.innerHTML = `<div class="text-center animate-fadeIn"><div class="h-1.5 w-44 rounded-full scanner mb-3 mx-auto"></div><div class="text-sm text-slate-700 dark:text-slate-200">${esc(label||'Analyzing inputs…')}</div></div>`;
      // Position over step area
      const container = root.parentElement;
      container.style.position = 'relative';
      overlay.style.position = 'absolute'; overlay.style.inset = '0';
      container.appendChild(overlay);
      await new Promise(r=> setTimeout(r, 300));
      container.removeChild(overlay);
      fn();
    }catch(e){ fn(); }
  }

  function setVal(node, val){
    // Special handling
    if (node && node.id === 'target_states' && Array.isArray(val)){
      if (val.includes('Australia-wide')){ val = ['Australia-wide']; }
    }
    set(answers, node.maps_to_field, val);
    // Auto-map strategy based on goals unless user changed strategy manually
    if (node && node.id === 'goals'){
      if (answers.strategy && answers.strategy.auto_mapped !== false){
        const gs = (answers.motivation.goals||[]).map(String);
        const map = (arr)=>{
          if (arr.includes('Rental yield') || arr.includes('Cashflow now')) return 'High Yield';
          if (arr.includes('Capital growth')) return 'High Growth';
          if (arr.includes('Balanced') || arr.includes('Portfolio scale')) return 'Balanced';
          return answers.strategy.goal || 'Balanced';
        };
        answers.strategy.goal = map(gs);
        answers.strategy.auto_mapped = true;
      }
    } else if (node && node.id === 'strategy_goal'){
      // User set strategy manually; lock mapping
      answers.strategy.auto_mapped = false;
    }
    saveDraft(); renderBrief(); pulseData();
  }

  function setProgress(){
    const curId = stepOrder[idx]||'summary';
    const g = groupProgress(curId);
    const pct = Math.round(((g.index+1)/Math.max(1,g.total))*100);
    $('#progress-bar').style.width = Math.max(8, pct) + '%';
  }

  function groupFor(id){
    // curId is already a group id in the consolidated flow
    return id;
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
  function showSignalsModal(){
    const m = document.getElementById('signals-modal'); if (!m) return;
    m.classList.remove('hidden');
    const close = document.getElementById('signals-modal-close');
    const hide = ()=> m.classList.add('hidden');
    if (close && !close._wired){ close._wired=true; close.addEventListener('click', hide); }
    m.addEventListener('click', (e)=>{ if (e.target===m || e.target.classList.contains('bg-black/50')) hide(); });
  }
  function pulseData(){
    const bar = document.getElementById('data-pulse'); if (!bar) return;
    bar.classList.remove('hidden');
    clearTimeout(pulseData._t); pulseData._t = setTimeout(()=> bar.classList.add('hidden'), 1200);
  }
  function redirectToRecommended(lead){
    const qs = location.search || '';
    let href = 'technology.html';
    if (lead && lead.recommended_next_step==='BOOK_CALL') href = 'book.html';
    else if (lead && lead.recommended_next_step==='SIGNUP_MATCHES') href = 'pricing.html';
    else if (lead && lead.recommended_next_step==='FINANCE_INTRO') href = 'book.html#finance';
    location.assign(href + qs);
  }

  function renderFinalNextSteps(lead){
    const root = document.getElementById('step-root'); if (!root) return;
    const nextHref = (function(){
      if (!lead) return 'technology.html';
      if (lead.recommended_next_step==='BOOK_CALL') return 'book.html';
      if (lead.recommended_next_step==='SIGNUP_MATCHES') return 'pricing.html';
      if (lead.recommended_next_step==='FINANCE_INTRO') return 'book.html#finance';
      return 'technology.html';
    })();
    const tasks = [];
    if ((answers.client.country||'') !== 'Australia'){
      tasks.push({text:'Review FIRB requirements (if applicable)', href:'https://www.ato.gov.au/individuals-and-families/investments-and-assets/foreign-resident-investments/foreign-investment-in-australia'});
    }
    const pre = answers.finance.preapproval;
    if (pre==='Pending' || pre==='Unsure' || pre==='Need help'){
      tasks.push({text:'Prepare/confirm your pre‑approval letter', href: nextHref.indexOf('book.html')!==-1? 'book.html#finance':'pricing.html'});
    }
    const compsCount = (answers.comparables||[]).filter(c=> c && c.url).length;
    if (compsCount===0){ tasks.push({text:'Add 1–3 example properties (optional)', href:'#'}); }
    function quickSlots(){
      const now = new Date();
      const fmt = d=> d.toLocaleString(undefined,{ weekday:'short', hour:'numeric', minute:'2-digit'});
      const s1 = new Date(now.getTime()+ 6*60*60*1000);
      const s2 = new Date(now.getTime()+ 30*60*60*1000);
      const s3 = new Date(now.getTime()+ 54*60*60*1000);
      return [s1,s2,s3].map(d=>({ label: fmt(d), href: 'book.html?slot='+encodeURIComponent(d.toISOString()) }));
    }
    const slots = quickSlots();
    const leadLabel = (lead && lead.recommended_next_step==='BOOK_CALL')? 'Book a strategy call'
      : (lead && lead.recommended_next_step==='SIGNUP_MATCHES')? 'Create account to receive matches'
      : (lead && lead.recommended_next_step==='FINANCE_INTRO')? 'Finance intro + shortlist'
      : 'Save brief + get shortlist';
    root.innerHTML = `
      <div class="mb-4">
        <div class="text-xs text-slate-500">Final</div>
        <h2 class="text-2xl font-extrabold">Next steps</h2>
        <p class="text-slate-600 dark:text-slate-300">Here’s what we recommend based on your brief. Book a call, and we’ll take you through the next five years with context, not hype.</p>
      </div>
      <div class="rounded-2xl border border-slate-200 dark:border-slate-800 p-4 mb-6">
        <div class="font-semibold mb-2">Recommended action</div>
        <a href="${nextHref}" class="inline-flex items-center gap-2 px-5 py-3 rounded-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 font-semibold">${leadLabel}<span class="material-symbols-outlined text-sm">arrow_forward</span></a>
        ${lead && lead.recommended_next_step==='BOOK_CALL' ? `<div class="mt-3 text-xs text-slate-500">Quick times:</div><div class="mt-1 flex flex-wrap gap-2">${slots.map(s=>`<a href="${s.href}" class=\"px-3 py-1.5 text-xs rounded-full border border-slate-200 dark:border-slate-700\">${s.label}</a>`).join('')}</div>`:''}
      </div>
      ${tasks.length? `<div class="rounded-2xl border border-slate-200 dark:border-slate-800 p-4 mb-6"><div class="font-semibold mb-2">Prepare</div><ul class="list-disc pl-5 text-sm text-slate-600 dark:text-slate-300">${tasks.map(t=>`<li>${t.href && t.href!=='#'? `<a href=\"${t.href}\" class=\"underline\" target=\"_blank\" rel=\"noopener\">${t.text}</a>`: t.text}</li>`).join('')}</ul></div>`:''}
      <div class="flex items-center gap-3 mb-4">
        <button id="email-next" class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 text-sm font-semibold" ${!answers.client.email? 'disabled':''}>Email me my checklist<span class="material-symbols-outlined text-sm">mail</span></button>
        ${!answers.client.email? '<span class="text-xs text-slate-500">Add your email above to enable</span>':''}
      </div>
      <div class="text-xs text-slate-500">Backed by our <a href="guarantee.html" class="underline" target="_blank" rel="noopener">Money‑Back Guarantee</a>. Historical, educational view only. No predictions or advice.</div>
    `;
    const emailBtn = document.getElementById('email-next');
    if (emailBtn && answers.client.email){
      emailBtn.addEventListener('click', async ()=>{
        try{
          const tasksOut = tasks.map(t=> ({ text: t.text, href: t.href||'' }));
          const res = await fetch('/api/assessment/nextsteps', { method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({ email: answers.client.email, tasks: tasksOut, lead }) });
          if (res.ok){ alert('Checklist saved. We\'ll email you shortly.'); }
          else { alert('Saved locally. We\'ll send your checklist after the call.'); }
        }catch(e){ alert('Saved locally. We\'ll send your checklist after the call.'); }
      });
    }
  }
})();
