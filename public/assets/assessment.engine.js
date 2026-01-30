// Proppy Assessment Rules Engine (Deterministic)
// - Evaluates show/required
// - Computes insights (basic v1)
// - Lead scoring + CTA routing with reason codes
// - Engagement mapping

(function(global){
  const Engine = {};

  Engine.RULE_VERSION = 'v1.0.0';

  Engine.getNodeMap = function(schema){
    const map = new Map();
    (schema.nodes||[]).forEach(n=> map.set(n.id, n));
    return map;
  };

  Engine.evalExpr = function(answers, expr){
    if (!expr) return true;
    if (expr.const !== undefined) return !!expr.const;
    if (expr.eq) { const [path, val] = expr.eq; return get(answers, path) === val; }
    if (expr.in) { const [path, arr] = expr.in; const v = get(answers, path); return Array.isArray(arr)? arr.includes(v) : false; }
    if (expr.includes) {
      const [path, val] = expr.includes; const v = get(answers, path);
      if (Array.isArray(v)) {
        if (val.includes('|')) { const any = val.split('|'); return any.some(x=> v.includes(x)); }
        return v.includes(val);
      }
      if (typeof v === 'string' && typeof val === 'string' && val.includes('|')) {
        return val.split('|').some(x=> v.includes(x));
      }
      return false;
    }
    if (expr.and) return expr.and.every(e=> Engine.evalExpr(answers, e));
    if (expr.or) return expr.or.some(e=> Engine.evalExpr(answers, e));
    if (expr.not) return !Engine.evalExpr(answers, expr.not);
    return true;
  };

  Engine.visibleNodes = function(schema, answers){
    return (schema.nodes||[]).filter(n=> Engine.evalExpr(answers, n.show_when));
  };

  Engine.requiredNodes = function(schema, answers){
    return (schema.nodes||[]).filter(n=> Engine.evalExpr(answers, n.required_when));
  };

  Engine.validate = function(schema, answers){
    const errors = [];
    const reqs = Engine.requiredNodes(schema, answers);
    for (const n of reqs){
      const v = get(answers, n.maps_to_field);
      if (v === undefined || v === null || v === '' || (Array.isArray(v) && v.length===0)) {
        errors.push({ id:n.id, reason:'required' });
      }
    }
    for (const n of schema.nodes||[]){
      if (!Engine.evalExpr(answers, n.show_when)) continue;
      const v = get(answers, n.maps_to_field);
      const val = n.validation||{};
      if (val.pattern && v){ try{ const re = new RegExp(val.pattern); if (!re.test(v)) errors.push({id:n.id,reason:'pattern'}); }catch(e){} }
      if (val.max && Array.isArray(v) && v.length > val.max) errors.push({id:n.id,reason:'max'});
    }
    // Comparables (dedupe + URL format)
    const comps = get(answers, 'comparables')||[];
    if (Array.isArray(comps)){
      const seen = new Set();
      for (const c of comps){
        if (!c || !c.url) continue;
        if (!/^https?:\/\//i.test(c.url)) errors.push({ id:'comparables', reason:'url_format' });
        const key = String(c.url).toLowerCase();
        if (seen.has(key)) errors.push({ id:'comparables', reason:'duplicate' }); else seen.add(key);
      }
      if (comps.length > 3) errors.push({ id:'comparables', reason:'max_3' });
    }
    return errors;
  };

  Engine.computeLead = function(answers){
    let score = 0; const reasons = [];
    const timeline = get(answers, 'engagement.timeline');
    const pre = get(answers, 'finance.preapproval');
    const depositSrc = get(answers, 'finance.deposit_source');
    const exp = get(answers, 'motivation.experience');
    const sugg = get(answers, 'locations.open_to_suggestions');
    const comps = (get(answers,'comparables')||[]).filter(Boolean).length;

    if (/^(Now|1–3 months)$/.test(timeline||'')) { score += 25; reasons.push('TL_SOON'); }
    if (pre==='Obtained' || pre==='Pending' || pre==='Expired' || depositSrc==='Equity' || depositSrc==='Cash + Equity') { score += 20; reasons.push('FIN_READY'); }
    if (exp==='Experienced' || exp==='Professional') { score += 10; reasons.push('EXP'); }
    if (sugg===true || sugg===undefined) { score += 5; reasons.push('OPEN_SUGG'); }
    if (comps>0) { score += 5; reasons.push('COMPS'); }
    if (timeline==='6–12 months') { score -= 10; reasons.push('TL_LATER'); }
    if (pre==='Need help') { reasons.push('NEEDS_FINANCE'); }

    let priority = 'NURTURE';
    if (score >= 50) priority = 'HOT';
    else if (score >= 25) priority = 'WARM';

    let next = 'REPORT_SHORTLIST';
    if (reasons.includes('NEEDS_FINANCE')) next = 'FINANCE_INTRO';
    else if (priority==='HOT') next = 'BOOK_CALL';
    else if (priority==='WARM') next = 'SIGNUP_MATCHES';

    return { score, priority, recommended_next_step: next, reason_codes: reasons };
  };

  Engine.buildEngagement = function(schema, answers, meta){
    const rule_version = schema.rule_version || Engine.RULE_VERSION;
    const engagement = {
      client: pickPaths(answers, ['client.first_name','client.last_name','client.email','client.mobile','client.location']),
      motivation: pickPaths(answers, ['motivation.goals','motivation.horizon','motivation.experience','motivation.risk']),
      finance: pickPaths(answers, ['finance.price_band','finance.deposit_band','finance.deposit_source','finance.borrowing_band','finance.preapproval','finance.preapproval_amount','finance.preapproval_expiry']),
      strategy: pickPaths(answers, ['strategy.investment_type','strategy.goal','strategy.target_yield','strategy.target_growth','strategy.reno_budget','strategy.reno_scope','strategy.dev_experience','strategy.dev_planning_risk','strategy.dev_holding']),
      brief: pickPaths(answers, ['brief.property_types','brief.beds_min','brief.beds_max','brief.baths_min','brief.baths_max','brief.construction','brief.land_min','brief.land_max','brief.strata_tolerance','brief.building_style','brief.dual_config','brief.features','brief.additional_requirements']),
      locations: pickPaths(answers, ['locations.states','locations.regions','locations.suburbs','locations.proximity','locations.open_to_suggestions','locations.acceptability_drivers']),
      comparableProperties: (answers.comparables||[]).slice(0,3).map(c=>({ url:c.url, tag:c.tag, source_domain: safeHost(c.url) })),
      engagement: { timeline: get(answers,'engagement.timeline'), status:'draft' },
      analytics: meta&&meta.analytics || {},
      rule_version
    };
    const lead = Engine.computeLead(answers);
    engagement.lead_score = lead.score;
    engagement.priority = lead.priority;
    engagement.recommended_next_step = lead.recommended_next_step;
    engagement.reason_codes = lead.reason_codes;
    return engagement;
  };

  function safeHost(u){ try{ return new URL(u).hostname; }catch(e){ return ''; } }
  function pickPaths(obj, paths){ const out={}; for(const p of paths){ const v=get(obj,p); if(v!==undefined) set(out,p,v); } return out; }
  function get(obj, path){ if(!path) return undefined; return path.split('.').reduce((o,k)=> (o&&o[k]!==undefined)? o[k]:undefined, obj); }
  function set(obj, path, val){ const parts = path.split('.'); let o=obj; while(parts.length>1){ const k=parts.shift(); o=o[k]=o[k]||{}; } o[parts[0]]=val; }

  // export
  global.ProppyEngine = Engine;
})(window);

