// Generate a slim historical dataset: Houses-only, top 10 per state by avgScore
// Input: data/proppydata.json
// Output: data/historical/top10.json

const fs = require('fs');
const path = require('path');

function num(v){
  if (v === undefined || v === null) return NaN;
  if (typeof v === 'number') return v;
  const m = String(v).match(/-?\d+(?:\.\d+)?/);
  return m ? parseFloat(m[0]) : NaN;
}

function main(){
  const root = process.cwd();
  const inPath = path.join(root, 'data', 'proppydata.json');
  const outDir = path.join(root, 'data', 'historical');
  const outPath = path.join(outDir, 'top10.json');
  if (!fs.existsSync(inPath)){
    console.error('Input not found:', inPath);
    process.exit(1);
  }
  const raw = JSON.parse(fs.readFileSync(inPath, 'utf-8'));
  const rows = Array.isArray(raw)? raw : [];
  const byState = new Map();
  rows.forEach(r=>{
    const t = String(r.type||'').toLowerCase();
    if (!t.includes('house')) return;
    const st = String(r.stateName||'OTHER').toUpperCase();
    if (!byState.has(st)) byState.set(st, []);
    byState.get(st).push(r);
  });
  const out = [];
  for (const [st, arr] of byState){
    const ranked = arr.slice().sort((a,b)=> (num(b.avgScore||0) - num(a.avgScore||0)) );
    out.push(...ranked.slice(0,10));
  }
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(outPath, JSON.stringify(out, null, 2));
  console.log('Wrote', outPath, 'with', out.length, 'rows');
}

main();

