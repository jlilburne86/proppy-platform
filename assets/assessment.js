/* Proppy Free Investment Assessment - first pass
 * - Steps 1–5B (Examples)
 * - Local draft persistence
 * - Live Brief updates
 * - GA4 events (if gtag present)
 */
(function(){
  const $ = sel => document.querySelector(sel);
  const $$ = sel => Array.from(document.querySelectorAll(sel));
  const state = loadDraft() || defaultState();
  const steps = buildSteps();
  let idx = 0;

  function defaultState(){
    return {
      meta: { started: false },
      brief: {
        name: '', email:'', mobile:'', location:'', consent:false,
        strategy:'', timeline:'', budget_band:'', deposit_source:'', preapproval:'',
        types:[], beds_min:'', beds_max:'', baths_min:'', baths_max:'', construction:'',
        examples:[], // { kind:'url'|'address', value:'', notes:'' }
        states:[], suburbs:'', open_suggestions:true, risk:'', success:''
      }
    };
  }

  function saveDraft(){ try{ localStorage.setItem('assessmentDraft', JSON.stringify(state)); }catch(e){} }
  function loadDraft(){ try{ return JSON.parse(localStorage.getItem('assessmentDraft')||''); }catch(e){ return null; } }

  function track(ev, params){ try{ if (typeof window.gtag==='function') gtag('event', ev, params||{}); }catch(e){} }

  function setProgress(){
    const pct = Math.round(((idx+1)/steps.length)*100);
    $('#progress-bar').style.width = Math.max(8, pct)+ '%';
  }

  function render(){
    const root = $('#step-root');
    root.innerHTML = '';
    root.appendChild(steps[idx].el);
    setProgress();
    renderBrief();
    $('#btn-back').disabled = idx===0;
    $('#btn-next').textContent = idx===steps.length-1? 'Review' : 'Continue';
    track('assessment_step_view', { step_id: steps[idx].id });
  }

  function renderBrief(){
    const b = state.brief;
    const wrap = $('#brief');
    const chip = (label,val)=> val? `<div><span class="text-slate-500">${label}:</span> <span class="font-semibold">${escapeHtml(val)}</span></div>`:'';
    const chips = [];
    if (b.name) chips.push(chip('Name', b.name));
    if (b.email) chips.push(chip('Email', b.email));
    if (b.location) chips.push(chip('Location', b.location));
    if (b.strategy) chips.push(chip('Strategy', b.strategy));
    if (b.timeline) chips.push(chip('Timeline', b.timeline));
    if (b.budget_band) chips.push(chip('Budget', b.budget_band));
    if (b.types && b.types.length) chips.push(chip('Types', b.types.join(', ')));
    if (b.states && b.states.length) chips.push(chip('States', b.states.join(', ')));
    if (b.risk) chips.push(chip('Risk', b.risk));
    wrap.innerHTML = chips.join('');
  }

  function escapeHtml(s){ return (s||'').replace(/[&<>\"]/g, c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c])); }

  function buildSteps(){
    const list = [];

    // Step 1: Define brief
    list.push(step('define', el=>{
      el.innerHTML = `
        <h2 class="text-2xl font-extrabold mb-1">Let’s define your brief.</h2>
        <p class="text-slate-600 dark:text-slate-300 mb-4">This keeps the search focused — and saves time later.</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div><label class="text-sm">First name</label><input id="fn" class="mt-1 w-full rounded-xl border-slate-300 dark:border-slate-700" type="text" value=""></div>
          <div><label class="text-sm">Last name</label><input id="ln" class="mt-1 w-full rounded-xl border-slate-300 dark:border-slate-700" type="text" value=""></div>
          <div><label class="text-sm">Email</label><input id="em" class="mt-1 w-full rounded-xl border-slate-300 dark:border-slate-700" type="email" value=""></div>
          <div><label class="text-sm">Mobile</label><input id="mb" class="mt-1 w-full rounded-xl border-slate-300 dark:border-slate-700" type="tel" value=""></div>
          <div class="md:col-span-2"><label class="text-sm">Current location</label><input id="loc" class="mt-1 w-full rounded-xl border-slate-300 dark:border-slate-700" type="text" value=""></div>
          <div class="md:col-span-2 flex items-center gap-2"><input id="cc" type="checkbox"><label for="cc" class="text-sm">I agree to privacy & communications</label></div>
        </div>`;
      const b = state.brief;
      el.querySelector('#fn').value = (b.name||'').split(' ')[0]||'';
      el.querySelector('#ln').value = (b.name||'').split(' ').slice(1).join(' ');
      el.querySelector('#em').value = b.email||'';
      el.querySelector('#mb').value = b.mobile||'';
      el.querySelector('#loc').value = b.location||'';
      el.querySelector('#cc').checked = !!b.consent;
      el.oninput = function(){
        const first = el.querySelector('#fn').value.trim();
        const last = el.querySelector('#ln').value.trim();
        state.brief.name = [first,last].filter(Boolean).join(' ');
        state.brief.email = el.querySelector('#em').value.trim();
        state.brief.mobile = el.querySelector('#mb').value.trim();
        state.brief.location = el.querySelector('#loc').value.trim();
        state.brief.consent = el.querySelector('#cc').checked;
        if (!state.meta.started && (first||last||state.brief.email)) { state.meta.started = true; track('assessment_start',{}); }
        saveDraft(); renderBrief();
      };
    }, ()=> valid(['email','consent'])));

    // Step 2: Strategy
    list.push(step('strategy', el=>{
      el.innerHTML = `
        <h2 class="text-2xl font-extrabold mb-1">What should this investment deliver?</h2>
        <p class="text-slate-600 dark:text-slate-300 mb-4">Pick one — we can refine later.</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          ${['Capital growth','Rental yield','Balanced growth + yield','Value-add potential','Development','Not sure — help me choose'].map(opt=>`
            <label class="flex items-center gap-3 p-3 rounded-xl border border-slate-200 dark:border-slate-700 cursor-pointer">
              <input type="radio" name="strat" value="${opt}"> <span>${opt}</span>
            </label>`).join('')}
        </div>
        <p class="mt-4 text-sm text-slate-500" id="tip"></p>`;
      // set
      $$('input[name=strat]').forEach(r=>{ r.checked = (state.brief.strategy===r.value); r.addEventListener('change',()=>{
        state.brief.strategy = r.value; saveDraft(); renderBrief(); updateTip(); }); });
      function updateTip(){
        const s = state.brief.strategy||'';
        let t = '';
        if (/Capital/.test(s)) t = 'We’ll prioritise scarcity and fundamentals, then verify with signals.';
        else if (/Rental/.test(s)) t = 'We’ll prioritise demand, vacancy and rentability — not just headline rent.';
        else if (/Not sure/.test(s)) t = 'Common — we clarify the strategy first, then choose markets.';
        $('#tip').textContent = t;
      }
      updateTip();
    }, ()=> !!state.brief.strategy));

    // Step 3: Readiness
    list.push(step('readiness', el=>{
      el.innerHTML = `
        <h2 class="text-2xl font-extrabold mb-1">When do you want to act?</h2>
        <p class="text-slate-600 dark:text-slate-300 mb-4">Timing guides shortlist urgency and negotiation strategy.</p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          ${['Now','1–3 months','3–6 months','6–12 months'].map(opt=>`
            <label class="flex items-center gap-3 p-3 rounded-xl border border-slate-200 dark:border-slate-700 cursor-pointer">
              <input type="radio" name="tl" value="${opt}"> <span>${opt}</span>
            </label>`).join('')}
        </div>`;
      $$('input[name=tl]').forEach(r=>{ r.checked = (state.brief.timeline===r.value); r.addEventListener('change',()=>{ state.brief.timeline=r.value; saveDraft(); renderBrief(); }); });
    }, ()=> !!state.brief.timeline));

    // Step 4: Finance
    list.push(step('finance', el=>{
      el.innerHTML = `
        <h2 class="text-2xl font-extrabold mb-1">Let’s set the search range.</h2>
        <p class="text-slate-600 dark:text-slate-300 mb-4">No issue if not ready — we can introduce finance partners.</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div><label class="text-sm">Budget (band)</label>
            <select id="bb" class="mt-1 w-full rounded-xl border-slate-300 dark:border-slate-700">
              <option value="">Select…</option>
              ${['500–700k','700–900k','900k–1.2M','1.2–1.5M','1.5M+'].map(b=>`<option>${b}</option>`).join('')}
            </select>
          </div>
          <div><label class="text-sm">Deposit source</label>
            <select id="ds" class="mt-1 w-full rounded-xl border-slate-300 dark:border-slate-700">
              ${['','Cash','Equity','Mix','Not sure'].map(x=>`<option value="${x}">${x||'Select…'}</option>`).join('')}
            </select>
          </div>
          <div><label class="text-sm">Pre‑approval</label>
            <select id="pa" class="mt-1 w-full rounded-xl border-slate-300 dark:border-slate-700">
              ${['','Not yet','In progress','Obtained','Expired'].map(x=>`<option value="${x}">${x||'Select…'}</option>`).join('')}
            </select>
          </div>
        </div>`;
      el.querySelector('#bb').value = state.brief.budget_band||'';
      el.querySelector('#ds').value = state.brief.deposit_source||'';
      el.querySelector('#pa').value = state.brief.preapproval||'';
      el.oninput = ()=>{
        state.brief.budget_band = el.querySelector('#bb').value;
        state.brief.deposit_source = el.querySelector('#ds').value;
        state.brief.preapproval = el.querySelector('#pa').value;
        saveDraft(); renderBrief();
      };
    }, ()=> !!state.brief.budget_band && !!state.brief.preapproval));

    // Step 5: Property requirements
    list.push(step('property', el=>{
      const opts = ['House','Townhouse','Unit','Dual income','Villa','Land & development'];
      el.innerHTML = `
        <h2 class="text-2xl font-extrabold mb-1">What are we targeting?</h2>
        <p class="text-slate-600 dark:text-slate-300 mb-4">We avoid oversupplied stock and risky projects to de‑risk outcomes.</p>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-3 mb-4">
          ${opts.map(o=>`<label class="flex items-center gap-2 p-2 rounded-xl border border-slate-200 dark:border-slate-700 cursor-pointer"><input type="checkbox" value="${o}"> <span>${o}</span></label>`).join('')}
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div><label class="text-sm">Beds (min–max)</label><div class="flex gap-2"><input id="bemin" type="number" min="0" class="w-full rounded-xl border-slate-300 dark:border-slate-700"><input id="bemax" type="number" min="0" class="w-full rounded-xl border-slate-300 dark:border-slate-700"></div></div>
          <div><label class="text-sm">Baths (min–max)</label><div class="flex gap-2"><input id="bammin" type="number" min="0" class="w-full rounded-xl border-slate-300 dark:border-slate-700"><input id="bammax" type="number" min="0" class="w-full rounded-xl border-slate-300 dark:border-slate-700"></div></div>
          <div><label class="text-sm">Construction preference</label><select id="cp" class="mt-1 w-full rounded-xl border-slate-300 dark:border-slate-700"><option value="">Select…</option><option>Low maintenance</option><option>Renovation OK</option></select></div>
        </div>`;
      // set
      $$('#step-root input[type=checkbox]').forEach(c=>{ c.checked = (state.brief.types||[]).includes(c.value); c.addEventListener('change',()=>{
        const set = new Set(state.brief.types||[]); if (c.checked) set.add(c.value); else set.delete(c.value); state.brief.types = Array.from(set); saveDraft(); renderBrief(); }); });
      el.querySelector('#bemin').value = state.brief.beds_min||'';
      el.querySelector('#bemax').value = state.brief.beds_max||'';
      el.querySelector('#bammin').value = state.brief.baths_min||'';
      el.querySelector('#bammax').value = state.brief.baths_max||'';
      el.querySelector('#cp').value = state.brief.construction||'';
      el.oninput = ()=>{
        state.brief.beds_min = el.querySelector('#bemin').value;
        state.brief.beds_max = el.querySelector('#bemax').value;
        state.brief.baths_min = el.querySelector('#bammin').value;
        state.brief.baths_max = el.querySelector('#bammax').value;
        state.brief.construction = el.querySelector('#cp').value;
        saveDraft();
      };
    }, ()=> (state.brief.types||[]).length>0 ));

    // Step 5B: Examples (URLs or addresses)
    list.push(step('examples', el=>{
      el.innerHTML = `
        <h2 class="text-2xl font-extrabold mb-1">Show us 1–3 examples.</h2>
        <p class="text-slate-600 dark:text-slate-300 mb-4">Paste a listing link or an address. This helps us read your preferences.</p>
        <div id="ex-list" class="space-y-3"></div>
        <button type="button" id="ex-add" class="mt-2 inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 font-semibold">+ Add another</button>
        <p class="mt-4 text-sm text-slate-500">Why we ask: it helps us de‑risk the shortlist and save time.</p>`;
      const list = state.brief.examples || (state.brief.examples=[]);
      function row(item, i){
        const wrap = document.createElement('div');
        wrap.className = 'p-3 rounded-xl border border-slate-200 dark:border-slate-700';
        wrap.innerHTML = `
          <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div class="md:col-span-2">
              <label class="text-sm">URL or address</label>
              <input type="text" class="mt-1 w-full rounded-xl border-slate-300 dark:border-slate-700 ex-val" value="${escapeHtml(item.value||'')}">
            </div>
            <div>
              <label class="text-sm">Notes (optional)</label>
              <input type="text" class="mt-1 w-full rounded-xl border-slate-300 dark:border-slate-700 ex-notes" value="${escapeHtml(item.notes||'')}">
            </div>
          </div>
          <div class="mt-2 flex items-center justify-between text-xs text-slate-500">
            <span>${previewHint(item.value)}</span>
            <button type="button" class="text-red-600 ex-del">Remove</button>
          </div>`;
        wrap.querySelector('.ex-val').addEventListener('input', e=>{ item.value = e.target.value.trim(); saveDraft(); });
        wrap.querySelector('.ex-notes').addEventListener('input', e=>{ item.notes = e.target.value.trim(); saveDraft(); });
        wrap.querySelector('.ex-del').addEventListener('click', ()=>{ state.brief.examples.splice(i,1); saveDraft(); render(); });
        return wrap;
      }
      function previewHint(v){
        if (!v) return '';
        if (/^https?:\/\//i.test(v)){
          try{ return new URL(v).hostname; }catch(e){ return 'Link'; }
        }
        return 'Address';
      }
      function renderList(){
        const root = el.querySelector('#ex-list');
        root.innerHTML = '';
        list.forEach((item,i)=> root.appendChild(row(item,i)) );
        el.querySelector('#ex-add').disabled = list.length>=3;
      }
      if (list.length===0) list.push({kind:'', value:'', notes:''});
      renderList();
      el.querySelector('#ex-add').addEventListener('click', ()=>{
        if (list.length>=3) return; list.push({kind:'', value:'', notes:''}); saveDraft(); renderList(); track('assessment_example_add',{count:list.length});
      });
    }, ()=> true));

    return list;
  }

  function valid(required){
    const b = state.brief;
    for (const f of required){
      if (f==='email' && !/.+@.+\..+/.test(b.email||'')) return false;
      if (f==='consent' && !b.consent) return false;
    }
    return true;
  }

  function step(id, renderFn, validateFn){
    const el = document.createElement('div');
    renderFn(el);
    return { id, el, validate: validateFn||(()=>true) };
  }

  $('#btn-back').addEventListener('click', ()=>{ if (idx>0){ idx--; render(); } });
  $('#btn-save').addEventListener('click', ()=>{ saveDraft(); alert('Saved on this device. You can resume later.'); });
  $('#btn-next').addEventListener('click', ()=>{
    const s = steps[idx];
    if (!s.validate()) return alert('Please complete the required fields.');
    track('assessment_step_complete', { step_id: s.id });
    if (idx<steps.length-1){ idx++; render(); }
    else { /* would show summary/review in next milestone */ alert('Assessment captured. Next: summary & routing.'); }
  });

  // init
  render();
})();

