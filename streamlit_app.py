
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OWLSNATION Engine</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{
    --bg: #0a0d12;
    --panel: #12161f;
    --panel-2: #171c27;
    --line: #232a38;
    --text: #e7e6e1;
    --text-dim: #8b93a3;
    --gold: #d9a441;
    --gold-dim: #8a702f;
    --green: #6fae8c;
    --red: #c7665c;
    --radius: 2px;
  }
  *{ box-sizing: border-box; }
  html,body{ margin:0; padding:0; background:var(--bg); color:var(--text); font-family:'Inter',sans-serif; }
  body{ padding-bottom: 80px; }

  /* ---------- Header ---------- */
  header{
    border-bottom: 1px solid var(--line);
    padding: 28px 24px 22px;
    display:flex; align-items:baseline; justify-content:space-between;
    flex-wrap: wrap; gap:10px;
  }
  .brand{ display:flex; align-items:center; gap:14px; }
  .owl-mark{ width:34px; height:34px; flex-shrink:0; }
  .brand h1{
    font-family:'Space Grotesk', sans-serif; font-weight:700;
    font-size:1.5rem; letter-spacing:0.04em; margin:0; color:var(--text);
  }
  .brand h1 span{ color:var(--gold); }
  .brand small{ display:block; color:var(--text-dim); font-size:0.72rem; letter-spacing:0.12em; text-transform:uppercase; margin-top:2px; }
  .eyebrow{ color:var(--text-dim); font-size:0.78rem; font-family:'IBM Plex Mono',monospace; letter-spacing:0.04em; }

  main{ max-width: 1140px; margin: 0 auto; padding: 32px 24px 0; }

  /* ---------- Section labels ---------- */
  .phase-label{
    font-family:'IBM Plex Mono', monospace; font-size:0.72rem; color:var(--gold);
    letter-spacing:0.14em; text-transform:uppercase; margin: 0 0 10px;
    display:flex; align-items:center; gap:10px;
  }
  .phase-label::after{ content:''; flex:1; height:1px; background:var(--line); }

  /* ---------- Input grid ---------- */
  .teams-row{ display:grid; grid-template-columns: 1fr 1fr; gap:18px; }
  @media (max-width: 760px){ .teams-row{ grid-template-columns: 1fr; } }

  .team-card{
    background: var(--panel); border:1px solid var(--line); border-radius: var(--radius);
    padding: 20px;
  }
  .team-card h2{
    font-family:'Space Grotesk',sans-serif; font-size:1rem; margin:0 0 4px;
    display:flex; align-items:center; justify-content:space-between;
  }
  .team-card .tag{
    font-family:'IBM Plex Mono',monospace; font-size:0.65rem; color:var(--text-dim);
    border:1px solid var(--line); padding:2px 8px; border-radius:20px;
  }
  .team-card input[type=text]{
    width:100%; background:transparent; border:none; border-bottom:1px solid var(--line);
    color:var(--text); font-family:'Space Grotesk',sans-serif; font-size:0.95rem;
    padding: 4px 0 8px; margin-bottom: 14px; outline:none;
  }
  .field-grid{ display:grid; grid-template-columns: 1fr 1fr; gap: 12px 16px; }
  .field label{
    display:block; font-size:0.68rem; color:var(--text-dim); margin-bottom:5px;
    letter-spacing:0.03em;
  }
  .field input{
    width:100%; background:var(--panel-2); border:1px solid var(--line); color:var(--text);
    font-family:'IBM Plex Mono',monospace; font-size:0.9rem; padding:8px 9px;
    border-radius: var(--radius); outline:none; transition: border-color .15s;
  }
  .field input:focus{ border-color: var(--gold-dim); }

  .book-row{
    margin-top: 22px; background: var(--panel); border:1px solid var(--line); border-radius: var(--radius);
    padding: 18px 20px;
  }
  .book-row h3{ font-family:'Space Grotesk',sans-serif; font-size:0.92rem; margin:0 0 12px; color:var(--text); }
  .book-grid{ display:grid; grid-template-columns: repeat(3,1fr); gap:14px; }
  @media (max-width:600px){ .book-grid{ grid-template-columns:1fr; } }

  .run-bar{ display:flex; justify-content:center; margin: 28px 0 8px; }
  #calcBtn{
    background: var(--gold); color:#1a1305; border:none; font-family:'Space Grotesk',sans-serif;
    font-weight:600; font-size:0.95rem; letter-spacing:0.03em; padding: 13px 38px;
    border-radius: var(--radius); cursor:pointer; transition: transform .12s, box-shadow .12s;
  }
  #calcBtn:hover{ transform: translateY(-1px); box-shadow: 0 4px 16px rgba(217,164,65,0.25); }
  #calcBtn:active{ transform: translateY(0); }
  .err{ color:var(--red); text-align:center; font-family:'IBM Plex Mono',monospace; font-size:0.82rem; min-height: 20px; margin-top:8px; }

  /* ---------- Results ---------- */
  #results{ display:none; margin-top: 36px; }
  .grid3{ display:grid; grid-template-columns: repeat(3,1fr); gap:16px; }
  .grid2{ display:grid; grid-template-columns: 1fr 1fr; gap:16px; }
  @media (max-width: 760px){ .grid3, .grid2{ grid-template-columns: 1fr; } }

  .card{ background:var(--panel); border:1px solid var(--line); border-radius: var(--radius); padding:18px 20px; }
  .card h4{
    font-family:'IBM Plex Mono',monospace; font-size:0.7rem; color:var(--text-dim);
    letter-spacing:0.1em; text-transform:uppercase; margin:0 0 14px;
  }
  .num{ font-family:'IBM Plex Mono',monospace; }
  .big{ font-size:1.6rem; font-weight:600; color:var(--text); }
  .outcome-row{ display:flex; justify-content:space-between; align-items:baseline; padding:7px 0; border-bottom:1px solid var(--line); }
  .outcome-row:last-child{ border-bottom:none; }
  .outcome-row .lbl{ color:var(--text-dim); font-size:0.82rem; }
  .outcome-row .pct{ font-family:'IBM Plex Mono',monospace; font-size:0.85rem; color:var(--text); }
  .outcome-row .odd{ font-family:'IBM Plex Mono',monospace; font-size:0.95rem; color:var(--gold); font-weight:600; margin-left:14px; }

  /* Dominance gauge */
  .dom-card{ position:relative; overflow:hidden; }
  .dom-team{ display:flex; align-items:center; justify-content:space-between; margin-bottom:10px; }
  .dom-team .name{ font-family:'Space Grotesk',sans-serif; font-size:0.92rem; }
  .dom-team .score{ font-family:'IBM Plex Mono',monospace; font-size:1.1rem; font-weight:600; }
  .dom-bar-track{ height:6px; background:var(--panel-2); border-radius:3px; position:relative; margin-bottom:4px; }
  .dom-bar-mid{ position:absolute; left:50%; top:-3px; bottom:-3px; width:1px; background:var(--line); }
  .dom-bar-fill{ position:absolute; top:0; bottom:0; border-radius:3px; }
  .dom-label{ font-size:0.7rem; color:var(--text-dim); margin-top:4px; }
  .resilient{ color: var(--green); }
  .fragile{ color: var(--red); }

  .market-list{ list-style:none; margin:0; padding:0; }
  .market-list li{
    display:flex; justify-content:space-between; align-items:center;
    padding:12px 0; border-bottom:1px solid var(--line);
  }
  .market-list li:last-child{ border-bottom:none; }
  .market-list .rank{
    font-family:'IBM Plex Mono',monospace; color:var(--gold); font-weight:700; margin-right:10px;
  }
  .market-list .name{ font-family:'Space Grotesk',sans-serif; font-size:0.92rem; }
  .market-list .prob{ font-family:'IBM Plex Mono',monospace; color:var(--text-dim); font-size:0.85rem; }

  .score-pair{ display:flex; gap:14px; }

  /* Strength breakdown table */
  .strength-table{ width:100%; border-collapse: collapse; }
  .strength-table th, .strength-table td{
    text-align:left; padding: 10px 12px; border-bottom:1px solid var(--line);
    font-family:'IBM Plex Mono',monospace; font-size:0.85rem;
  }
  .strength-table th{
    color:var(--text-dim); font-size:0.68rem; letter-spacing:0.08em; text-transform:uppercase;
    font-family:'Inter',sans-serif; font-weight:600; border-bottom:1px solid var(--gold-dim);
  }
  .strength-table td:first-child{ color:var(--text-dim); font-family:'Inter',sans-serif; font-size:0.82rem; }
  .strength-table tr:last-child td{ border-bottom:none; }
  .strength-table .final-row td{ padding-top:14px; padding-bottom:14px; }
  .strength-table .final-row td:not(:first-child){
    font-size:1.15rem; font-weight:600; color:var(--gold); border-top:1px solid var(--line);
  }
  .strength-table td:nth-child(2), .strength-table td:nth-child(3){ color:var(--text); }

  .score-box{
    flex:1; text-align:center; background:var(--panel-2); border:1px solid var(--line);
    border-radius: var(--radius); padding: 18px 10px;
  }
  .score-box .sc{ font-family:'IBM Plex Mono',monospace; font-size:2rem; font-weight:600; color:var(--gold); }
  .score-box .pp{ font-family:'IBM Plex Mono',monospace; font-size:0.78rem; color:var(--text-dim); margin-top:6px; }

  .edge-note{ font-size:0.85rem; color:var(--text-dim); line-height:1.5; margin-top:6px; }
  .edge-note b{ color:var(--text); }

  /* Audit trail */
  details{ margin-top: 28px; background:var(--panel); border:1px solid var(--line); border-radius:var(--radius); }
  summary{
    cursor:pointer; padding:14px 20px; font-family:'IBM Plex Mono',monospace; font-size:0.78rem;
    color: var(--gold); letter-spacing:0.06em; text-transform:uppercase; list-style:none;
  }
  summary::-webkit-details-marker{ display:none; }
  summary::before{ content:'▸ '; }
  details[open] summary::before{ content:'▾ '; }
  .audit-body{ padding: 4px 20px 20px; font-family:'IBM Plex Mono',monospace; font-size:0.82rem; color:var(--text-dim); }
  .audit-section{ margin-bottom:16px; }
  .audit-section h5{ color:var(--text); font-size:0.78rem; margin:0 0 6px; text-transform:uppercase; letter-spacing:0.06em; }
  .audit-line{ display:flex; justify-content:space-between; padding:3px 0; border-bottom:1px dashed var(--line); }
  .audit-line span:last-child{ color:var(--text); }

  footer{ text-align:center; color:var(--text-dim); font-size:0.72rem; padding: 40px 20px 10px; font-family:'IBM Plex Mono',monospace; }
</style>
</head>
<body>

<header>
  <div class="brand">
    <svg class="owl-mark" viewBox="0 0 48 48" fill="none">
      <circle cx="24" cy="24" r="23" stroke="#d9a441" stroke-width="1.5"/>
      <circle cx="16" cy="21" r="6.5" stroke="#d9a441" stroke-width="1.5"/>
      <circle cx="32" cy="21" r="6.5" stroke="#d9a441" stroke-width="1.5"/>
      <circle cx="16" cy="21" r="2" fill="#d9a441"/>
      <circle cx="32" cy="21" r="2" fill="#d9a441"/>
      <path d="M24 24 L21 31 L27 31 Z" fill="#d9a441"/>
    </svg>
    <div>
      <h1>OWLS<span>NATION</span> ENGINE</h1>
      <small>Fundamental Strength &middot; Poisson &middot; Variance Stress Model</small>
    </div>
  </div>
  <div class="eyebrow">PHASE 1&ndash;6 / DETERMINISTIC MODEL</div>
</header>

<main>

  <p class="phase-label">Match Inputs</p>
  <div class="teams-row">
    <div class="team-card">
      <h2>Home <span class="tag">TEAM A</span></h2>
      <input type="text" id="nameA" placeholder="Team name (optional)">
      <div class="field-grid">
        <div class="field"><label>Avg Goals Scored (G)</label><input type="number" step="any" id="GA" placeholder="2.0"></div>
        <div class="field"><label>Avg Goals Conceded (C)</label><input type="number" step="any" id="CA" placeholder="1.4"></div>
        <div class="field"><label>Shots on Target For (SOT)</label><input type="number" step="any" id="SOTA_" placeholder="5.2"></div>
        <div class="field"><label>Shots on Target Against</label><input type="number" step="any" id="SOTAGA" placeholder="3.1"></div>
        <div class="field"><label>Avg Big Chances</label><input type="number" step="any" id="BCA" placeholder="0.58"></div>
        <div class="field"><label>Avg Expected Goals (xG)</label><input type="number" step="any" id="xGA" placeholder="0.77"></div>
      </div>
    </div>

    <div class="team-card">
      <h2>Away <span class="tag">TEAM B</span></h2>
      <input type="text" id="nameB" placeholder="Team name (optional)">
      <div class="field-grid">
        <div class="field"><label>Avg Goals Scored (G)</label><input type="number" step="any" id="GB" placeholder="1.8"></div>
        <div class="field"><label>Avg Goals Conceded (C)</label><input type="number" step="any" id="CB" placeholder="1.6"></div>
        <div class="field"><label>Shots on Target For (SOT)</label><input type="number" step="any" id="SOTB_" placeholder="4.4"></div>
        <div class="field"><label>Shots on Target Against</label><input type="number" step="any" id="SOTBGA" placeholder="3.8"></div>
        <div class="field"><label>Avg Big Chances</label><input type="number" step="any" id="BCB" placeholder="0.50"></div>
        <div class="field"><label>Avg Expected Goals (xG)</label><input type="number" step="any" id="xGB" placeholder="0.89"></div>
      </div>
    </div>
  </div>

  <div class="book-row">
    <h3>Bookmaker Decimal Odds <span style="color:var(--text-dim); font-weight:400; font-size:0.78rem;">(for Value Margin comparison)</span></h3>
    <div class="book-grid">
      <div class="field"><label>Home Win Odd</label><input type="number" step="any" id="bkH" placeholder="3.60"></div>
      <div class="field"><label>Draw Odd</label><input type="number" step="any" id="bkD" placeholder="3.40"></div>
      <div class="field"><label>Away Win Odd</label><input type="number" step="any" id="bkA" placeholder="2.20"></div>
    </div>
  </div>

  <div class="run-bar"><button id="calcBtn" onclick="runEngine()">RUN ENGINE</button></div>
  <div class="err" id="errBox"></div>

  <div id="results">

    <p class="phase-label">Phase 2&ndash;3 &mdash; Strength Breakdown</p>
    <div class="card" style="margin-bottom:16px; overflow-x:auto;">
      <table class="strength-table">
        <thead>
          <tr><th>Metric</th><th id="thA">Home</th><th id="thB">Away</th></tr>
        </thead>
        <tbody>
          <tr><td>Net Score</td><td class="num" id="rowNetA">-</td><td class="num" id="rowNetB">-</td></tr>
          <tr><td>Goal Ratio</td><td class="num" id="rowRatioA">-</td><td class="num" id="rowRatioB">-</td></tr>
          <tr><td>Score Power</td><td class="num" id="rowPowerA">-</td><td class="num" id="rowPowerB">-</td></tr>
          <tr class="final-row"><td>Final Strength (&lambda;)</td><td class="num" id="rowStrA">-</td><td class="num" id="rowStrB">-</td></tr>
        </tbody>
      </table>
    </div>

    <p class="phase-label">Phase 4&ndash;6 &mdash; Baseline &amp; Master Odds</p>
    <div class="grid2" style="margin-bottom:16px;">
      <div class="card">
        <h4>Baseline Odds (Odd 0)</h4>
        <div class="outcome-row"><span class="lbl">Home</span><span class="pct" id="b0hp">-</span><span class="odd" id="b0ho">-</span></div>
        <div class="outcome-row"><span class="lbl">Draw</span><span class="pct" id="b0dp">-</span><span class="odd" id="b0do">-</span></div>
        <div class="outcome-row"><span class="lbl">Away</span><span class="pct" id="b0ap">-</span><span class="odd" id="b0ao">-</span></div>
      </div>
      <div class="card">
        <h4>Master Odds (Ensemble)</h4>
        <div class="outcome-row"><span class="lbl">Home</span><span class="pct" id="mhp">-</span><span class="odd" id="mho">-</span></div>
        <div class="outcome-row"><span class="lbl">Draw</span><span class="pct" id="mdp">-</span><span class="odd" id="mdo">-</span></div>
        <div class="outcome-row"><span class="lbl">Away</span><span class="pct" id="map">-</span><span class="odd" id="mao">-</span></div>
      </div>
    </div>

    <p class="phase-label">Separate Dominance Index</p>
    <div class="grid2" style="margin-bottom:16px;">
      <div class="card dom-card">
        <div class="dom-team"><span class="name" id="domNameA">Home</span><span class="score num" id="domScoreA">-</span></div>
        <div class="dom-bar-track"><div class="dom-bar-mid"></div><div class="dom-bar-fill" id="domBarA"></div></div>
        <div class="dom-label" id="domLabelA">-</div>
      </div>
      <div class="card dom-card">
        <div class="dom-team"><span class="name" id="domNameB">Away</span><span class="score num" id="domScoreB">-</span></div>
        <div class="dom-bar-track"><div class="dom-bar-mid"></div><div class="dom-bar-fill" id="domBarB"></div></div>
        <div class="dom-label" id="domLabelB">-</div>
      </div>
    </div>

    <p class="phase-label">Value Margin vs Bookmaker</p>
    <div class="card" style="margin-bottom:16px;">
      <div class="outcome-row"><span class="lbl">Home</span><span class="pct num" id="vmH">-</span></div>
      <div class="outcome-row"><span class="lbl">Draw</span><span class="pct num" id="vmD">-</span></div>
      <div class="outcome-row"><span class="lbl">Away</span><span class="pct num" id="vmA">-</span></div>
      <p class="edge-note" id="edgeNote">-</p>
    </div>

    <p class="phase-label">Most Likely Markets</p>
    <p class="edge-note" style="margin-top:-6px; margin-bottom:10px;">Derived only from Master Odds + Dominance Index — Strength and Baseline play no part in this step.</p>
    <div class="card" style="margin-bottom:16px;">
      <ul class="market-list" id="marketList"></ul>
    </div>

    <p class="phase-label">Most Likely Correct Scores</p>
    <p class="edge-note" style="margin-top:-6px; margin-bottom:10px;">Derived only from Master Odds + Dominance Index — Strength and Baseline play no part in this step.</p>
    <div class="card" style="margin-bottom: 8px;">
      <div class="score-pair" id="scorePair"></div>
    </div>

    <details>
      <summary>Full Calculation Audit Trail (Phase 1&ndash;6)</summary>
      <div class="audit-body" id="auditBody"></div>
    </details>

  </div>

</main>

<footer>OWLSNATION ENGINE &mdash; deterministic model, no randomness. Verify any figure against the audit trail above.</footer>

<script>
function r3(x){ return Math.round(x*1000)/1000; }

// Precomputed factorial cache (0! .. 170!) — 171! overflows double precision, and our
// dynamic cap is bounded well below that, so this stays safe for any realistic lambda.
const FACT_CACHE = (function(){
  const arr = [1];
  for(let i=1;i<=170;i++) arr.push(arr[i-1]*i);
  return arr;
})();
function factorial(n){ return FACT_CACHE[n]; }
function pmf(k, lam){ return (Math.pow(lam,k)*Math.exp(-lam))/factorial(k); }

// The Poisson score cap must scale with lambda. A fixed cap of 6 is fine for a typical
// lambda of 1-3, but for a large lambda (e.g. 8.6) the mean itself sits above the cap,
// truncating the vast majority of the real probability mass. This sizes the cap to
// comfortably cover the mean plus six standard deviations (>99.9% of the distribution),
// floored at 6 (never smaller than the original spec) and capped at 150 for performance/safety.
function dynamicCap(lambda){
  const c = Math.ceil(lambda + 6*Math.sqrt(Math.max(lambda, 0.0001))) + 2;
  return Math.min(Math.max(c, 6), 150);
}

function poissonGrid(lamH, lamA, cap){
  const grid = [];
  for(let h=0;h<=cap;h++){
    grid.push([]);
    for(let a=0;a<=cap;a++) grid[h].push(pmf(h,lamH)*pmf(a,lamA));
  }
  return grid;
}
function normalizeGrid(grid){
  let total=0;
  for(const row of grid) for(const v of row) total+=v;
  return grid.map(row=>row.map(v=>v/total));
}
function outcomeSums(grid){
  let home=0,draw=0,away=0;
  for(let h=0;h<grid.length;h++) for(let a=0;a<grid[h].length;a++){
    const p=grid[h][a];
    if(h>a) home+=p; else if(h===a) draw+=p; else away+=p;
  }
  return {home,draw,away};
}
function toPct(home,draw,away){ const t=home+draw+away; return {h:r3(home/t*100),d:r3(draw/t*100),a:r3(away/t*100)}; }
function odds(h,d,a){ return {oh:r3(100/h), od:r3(100/d), oa:r3(100/a)}; }
function renorm(h,d,a){ const t=h+d+a; return {h:r3(h/t*100),d:r3(d/t*100),a:r3(a/t*100)}; }

const SIGMA = r3(0.6*0.5*0.4*0.3);
const DRAG = r3(100*SIGMA);

function stressState(h,d,a,target){
  let H=h,D=d,A=a;
  if(target==='home') H=r3((h+50)-DRAG);
  else if(target==='away') A=r3((a+50)-DRAG);
  else if(target==='draw') D=r3((d+50)-DRAG);
  else if(target==='all'){ H=r3((h+50)-DRAG); D=r3((d+50)-DRAG); A=r3((a+50)-DRAG); }
  return renorm(H,D,A);
}

function fmtPct(v){ return v.toFixed(3)+'%'; }
function fmtOdd(v){ return v.toFixed(3); }
function val(id){ return parseFloat(document.getElementById(id).value); }

function runEngine(){
  const errBox = document.getElementById('errBox');
  errBox.textContent = '';

  const ids = ['GA','CA','SOTA_','SOTAGA','BCA','xGA','GB','CB','SOTB_','SOTBGA','BCB','xGB','bkH','bkD','bkA'];
  const v = {};
  for(const id of ids) v[id] = val(id);
  for(const id of ids){
    if(isNaN(v[id]) || v[id] <= 0){
      errBox.textContent = 'Please fill every stat field and bookmaker odd with a number greater than 0.';
      document.getElementById('results').style.display = 'none';
      return;
    }
  }

  const nameA = document.getElementById('nameA').value.trim() || 'Home';
  const nameB = document.getElementById('nameB').value.trim() || 'Away';

  // ---------- PHASE 1 ----------
  function phase1(G,C,SOT,SOTA){
    const PctScored = r3((G/SOT)*100);
    const CalcScored = r3((1/PctScored)*100);
    const PctConcede = r3((C/SOTA)*100);
    const CalcConcede = r3((1/PctConcede)*100);
    return {PctScored, CalcScored, PctConcede, CalcConcede};
  }
  const p1A = phase1(v.GA, v.CA, v.SOTA_, v.SOTAGA);
  const p1B = phase1(v.GB, v.CB, v.SOTB_, v.SOTBGA);

  // ---------- PHASE 2 & 3 ----------
  function phase23(Gself, Copp, SOTself, xGself, BCself, CalcScoredSelf, CalcConcedeOpp){
    const Net = r3(CalcScoredSelf / CalcConcedeOpp);
    const Ratio = r3(Gself / Copp);
    const Power = r3((Ratio/Net) * SOTself);
    const avgXgBc = r3((xGself + BCself)/2);
    const Strength = r3(avgXgBc * Power);
    return {Net, Ratio, Power, avgXgBc, Strength};
  }
  const p23A = phase23(v.GA, v.CB, v.SOTA_, v.xGA, v.BCA, p1A.CalcScored, p1B.CalcConcede);
  const p23B = phase23(v.GB, v.CA, v.SOTB_, v.xGB, v.BCB, p1B.CalcScored, p1A.CalcConcede);

  const StrengthA = p23A.Strength;
  const StrengthB = p23B.Strength;

  // ---------- PHASE 4 ----------
  const baseCap = Math.max(dynamicCap(StrengthA), dynamicCap(StrengthB));
  const grid = poissonGrid(StrengthA, StrengthB, baseCap);
  const sums = outcomeSums(grid);
  const basePct = toPct(sums.home, sums.draw, sums.away);
  const baseOdds = odds(basePct.h, basePct.d, basePct.a);

  // ---------- PHASE 5 ----------
  const states = [];
  states[0] = {h:basePct.h, d:basePct.d, a:basePct.a};
  states[1] = stressState(basePct.h, basePct.d, basePct.a, 'home');
  states[2] = stressState(basePct.h, basePct.d, basePct.a, 'away');
  states[3] = stressState(basePct.h, basePct.d, basePct.a, 'draw');
  states[4] = stressState(basePct.h, basePct.d, basePct.a, 'all');
  const stateOdds = states.map(s => odds(s.h, s.d, s.a));
  const implied = stateOdds.map(o => ({h:r3(1/o.oh), d:r3(1/o.od), a:r3(1/o.oa)}));
  let domHome = 0, domAway = 0;
  for(let i=1;i<=4;i++) domHome = r3(domHome + r3(implied[i].h - implied[0].h));
  for(let i=1;i<=4;i++) domAway = r3(domAway + r3(implied[i].a - implied[0].a));

  // ---------- PHASE 6: Master Odds ----------
  const masterPct = {
    h: r3(states.reduce((a,s)=>a+s.h,0)/5),
    d: r3(states.reduce((a,s)=>a+s.d,0)/5),
    a: r3(states.reduce((a,s)=>a+s.a,0)/5)
  };
  const masterOdds = odds(masterPct.h, masterPct.d, masterPct.a);

  // ---------- Bookmaker normalization & Value Margin ----------
  const bkImplied = {h:1/v.bkH, d:1/v.bkD, a:1/v.bkA};
  const bkTotal = bkImplied.h + bkImplied.d + bkImplied.a;
  const bkPct = {h:r3(bkImplied.h/bkTotal*100), d:r3(bkImplied.d/bkTotal*100), a:r3(bkImplied.a/bkTotal*100)};
  const valueMargin = {
    h: r3(masterPct.h - bkPct.h),
    d: r3(masterPct.d - bkPct.d),
    a: r3(masterPct.a - bkPct.a)
  };
  let edgeSide = 'h', edgeVal = valueMargin.h;
  if(valueMargin.d > edgeVal){ edgeSide='d'; edgeVal=valueMargin.d; }
  if(valueMargin.a > edgeVal){ edgeSide='a'; edgeVal=valueMargin.a; }
  const edgeSideName = {h:nameA, d:'Draw', a:nameB}[edgeSide];

  // ---------- MASTER + DOMINANCE FITTED GRID ----------
  // Correct scores and markets are generated from Master Odds + Dominance Index ONLY.
  // Step 1: reverse-fit a Poisson lambda pair so its outcome% matches Master% as closely as possible.
  // Uses Nelder-Mead simplex search (multiple seeds, to avoid local minima) rather than a
  // blind grid search, since the error surface can have a narrow minimum a coarse grid misses.
  function outcomePctOf(grid){
    let home=0,draw=0,away=0;
    for(let h=0;h<grid.length;h++) for(let a=0;a<grid[h].length;a++){
      const p=grid[h][a]; if(h>a) home+=p; else if(h===a) draw+=p; else away+=p;
    }
    const t=home+draw+away;
    return {h:home/t*100, d:draw/t*100, a:away/t*100};
  }
  function fitErr(pt){
    const lh = Math.max(pt[0], 0.001), la = Math.max(pt[1], 0.001);
    const c = Math.max(dynamicCap(lh), dynamicCap(la));
    const pct = outcomePctOf(poissonGrid(lh, la, c));
    return Math.pow(pct.h-masterPct.h,2) + Math.pow(pct.d-masterPct.d,2) + Math.pow(pct.a-masterPct.a,2);
  }
  function nelderMead(fn, x0, step, maxIter){
    const n = x0.length;
    let simplex = [x0.slice()];
    for(let i=0;i<n;i++){ const v = x0.slice(); v[i] += step; simplex.push(v); }
    let fvals = simplex.map(fn);
    for(let iter=0; iter<maxIter; iter++){
      const idx = fvals.map((v,i)=>i).sort((a,b)=>fvals[a]-fvals[b]);
      simplex = idx.map(i=>simplex[i]); fvals = idx.map(i=>fvals[i]);
      const worst = simplex[n];
      if(Math.abs(fvals[n]-fvals[0]) < 1e-10) break;
      const centroid = new Array(n).fill(0);
      for(let i=0;i<n;i++) for(let j=0;j<n;j++) centroid[j] += simplex[i][j];
      for(let j=0;j<n;j++) centroid[j] /= n;
      const reflect = centroid.map((c,j)=>c + 1.0*(c-worst[j]));
      const fr = fn(reflect);
      if(fr < fvals[0]){
        const expand = centroid.map((c,j)=>c + 2.0*(c-worst[j]));
        const fe = fn(expand);
        if(fe < fr){ simplex[n]=expand; fvals[n]=fe; } else { simplex[n]=reflect; fvals[n]=fr; }
      } else if(fr < fvals[n-1]){
        simplex[n] = reflect; fvals[n] = fr;
      } else {
        const contract = centroid.map((c,j)=>c + 0.5*(worst[j]-c));
        const fc = fn(contract);
        if(fc < fvals[n]){ simplex[n]=contract; fvals[n]=fc; }
        else { for(let i=1;i<=n;i++){ simplex[i]=simplex[0].map((b,j)=>b+0.5*(simplex[i][j]-b)); fvals[i]=fn(simplex[i]); } }
      }
    }
    const idx = fvals.map((v,i)=>i).sort((a,b)=>fvals[a]-fvals[b]);
    return {x: simplex[idx[0]], e: fvals[idx[0]]};
  }
  const fitSeeds = [
    [StrengthA, StrengthB],
    [StrengthB, StrengthA],
    [(StrengthA+StrengthB)/2, (StrengthA+StrengthB)/2],
    [Math.max(StrengthA,0.5), Math.max(StrengthB,0.5)*1.5]
  ];
  let bestFit = null;
  for(const seed of fitSeeds){
    const stepSize = Math.max(seed[0], seed[1]) * 0.2 + 0.3;
    const r = nelderMead(fitErr, seed, stepSize, 300);
    if(!bestFit || r.e < bestFit.e) bestFit = r;
  }
  const masterLambdaH = r3(Math.max(bestFit.x[0], 0.001));
  const masterLambdaA = r3(Math.max(bestFit.x[1], 0.001));

  // Step 2: adjust the fitted lambdas by each side's Dominance Index.
  // A plain (1 + Dominance) multiplier is unbounded: a Dominance score near -1 (extreme
  // fragility) would multiply lambda by near-zero, effectively erasing a team's attacking
  // threat entirely -- which is not what Dominance represents (it's a fragility signal,
  // not a literal "this team won't score" signal). Instead, cap the adjustment at +/-40%
  // using a saturating curve, so even an extreme Dominance score nudges scoring expectancy
  // meaningfully without ever being able to wipe it out.
  const DOM_MAX_ADJ = 0.4;
  const DOM_SCALE = 0.3;
  function domAdjFactor(dom){ return 1 + DOM_MAX_ADJ * Math.tanh(dom / DOM_SCALE); }
  const mdLambdaH = r3(masterLambdaH * domAdjFactor(domHome));
  const mdLambdaA = r3(masterLambdaA * domAdjFactor(domAway));

  // Step 3: build the final grid purely from Master+Dominance-adjusted lambdas, with a cap
  // that scales to whatever size these adjusted lambdas turn out to be.
  const mdLamH = Math.max(mdLambdaH, 0.01);
  const mdLamA = Math.max(mdLambdaA, 0.01);
  const mdCap = Math.max(dynamicCap(mdLamH), dynamicCap(mdLamA));
  const mdGridRaw = poissonGrid(mdLamH, mdLamA, mdCap);
  const mdGrid = normalizeGrid(mdGridRaw);
  const mdOutcome = outcomePctOf(mdGridRaw);
  const mdN = mdGrid.length;

  // ---------- Market candidates (from the Master+Dominance grid only) ----------
  let bttsYes = 0, totalLow = 0, totalHigh = 0;
  for(let h=0;h<mdN;h++) for(let a=0;a<mdN;a++){
    const p = mdGrid[h][a];
    if(h>=1 && a>=1) bttsYes += p;
    if(h+a <= 2) totalLow += p;
    if(h+a >= 3) totalHigh += p;
  }
  const dc12 = r3(mdOutcome.h + mdOutcome.a); // 100 - draw, from the Master+Dominance grid

  // Handicap candidate: favorite determined by Master Odds (not baseline), stability by Dominance
  const favoriteIsHome = masterOdds.oh <= masterOdds.oa;
  const favDominance = favoriteIsHome ? domHome : domAway;
  let marginWinProb = 0; // P(favorite wins by 2+ goals), from the Master+Dominance grid
  for(let h=0;h<mdN;h++) for(let a=0;a<mdN;a++){
    const p = mdGrid[h][a];
    if(favoriteIsHome && (h-a)>=2) marginWinProb += p;
    if(!favoriteIsHome && (a-h)>=2) marginWinProb += p;
  }
  marginWinProb = r3(marginWinProb);
  let handicapName, handicapProb;
  if(favDominance >= 0){
    handicapName = (favoriteIsHome?nameA:nameB) + ' -1.5 Asian Handicap';
    handicapProb = r3(marginWinProb * 100);
  } else {
    handicapName = (favoriteIsHome?nameB:nameA) + ' +1.5 Asian Handicap';
    handicapProb = r3((1 - marginWinProb) * 100);
  }

  const candidates = [
    {name:'BTTS — Yes', prob: r3(bttsYes*100)},
    {name:'Double Chance (12) — No Draw', prob: dc12},
    {name:'Over 2.5 / High-Scoring Match', prob: r3(totalHigh*100)},
    {name:'Under 2.5 / Low-Scoring Match', prob: r3(totalLow*100)},
    {name: handicapName, prob: handicapProb}
  ];
  candidates.sort((a,b)=>b.prob-a.prob);
  const topMarkets = candidates.slice(0,2);

  // ---------- Correct scores: top 2 from the Master+Dominance grid ONLY ----------
  const flat = [];
  for(let h=0;h<mdN;h++) for(let a=0;a<mdN;a++) flat.push({h,a,p:mdGrid[h][a]});
  flat.sort((x,y)=>y.p-x.p);
  const topScores = flat.slice(0,2);


  // ===================== RENDER =====================
  document.getElementById('results').style.display = 'block';

  document.getElementById('thA').textContent = nameA;
  document.getElementById('thB').textContent = nameB;
  document.getElementById('rowNetA').textContent = p23A.Net.toFixed(3);
  document.getElementById('rowNetB').textContent = p23B.Net.toFixed(3);
  document.getElementById('rowRatioA').textContent = p23A.Ratio.toFixed(3);
  document.getElementById('rowRatioB').textContent = p23B.Ratio.toFixed(3);
  document.getElementById('rowPowerA').textContent = p23A.Power.toFixed(3);
  document.getElementById('rowPowerB').textContent = p23B.Power.toFixed(3);
  document.getElementById('rowStrA').textContent = StrengthA.toFixed(3);
  document.getElementById('rowStrB').textContent = StrengthB.toFixed(3);

  document.getElementById('b0hp').textContent = fmtPct(basePct.h);
  document.getElementById('b0dp').textContent = fmtPct(basePct.d);
  document.getElementById('b0ap').textContent = fmtPct(basePct.a);
  document.getElementById('b0ho').textContent = fmtOdd(baseOdds.oh);
  document.getElementById('b0do').textContent = fmtOdd(baseOdds.od);
  document.getElementById('b0ao').textContent = fmtOdd(baseOdds.oa);

  document.getElementById('mhp').textContent = fmtPct(masterPct.h);
  document.getElementById('mdp').textContent = fmtPct(masterPct.d);
  document.getElementById('map').textContent = fmtPct(masterPct.a);
  document.getElementById('mho').textContent = fmtOdd(masterOdds.oh);
  document.getElementById('mdo').textContent = fmtOdd(masterOdds.od);
  document.getElementById('mao').textContent = fmtOdd(masterOdds.oa);

  function renderDominance(prefix, name, score){
    document.getElementById('domName'+prefix).textContent = name;
    document.getElementById('domScore'+prefix).textContent = (score>=0?'+':'')+score.toFixed(3);
    document.getElementById('domScore'+prefix).className = 'score num ' + (score>=0?'resilient':'fragile');
    const bar = document.getElementById('domBar'+prefix);
    const pctWidth = Math.min(Math.abs(score)/0.3, 1) * 50; // scale to half-track
    bar.style.background = score>=0 ? 'var(--green)' : 'var(--red)';
    if(score>=0){ bar.style.left='50%'; bar.style.width=pctWidth+'%'; }
    else { bar.style.left=(50-pctWidth)+'%'; bar.style.width=pctWidth+'%'; }
    let label;
    if(score >= 0) label = 'Resilient — holds or sharpens win probability under simulated stress';
    else if(score > -0.15) label = 'Mildly fragile — some erosion of win probability under stress';
    else label = 'Fragile — win probability collapses significantly under stress';
    document.getElementById('domLabel'+prefix).textContent = label;
    document.getElementById('domLabel'+prefix).className = 'dom-label ' + (score>=0?'resilient':'fragile');
  }
  renderDominance('A', nameA, domHome);
  renderDominance('B', nameB, domAway);

  document.getElementById('vmH').textContent = (valueMargin.h>=0?'+':'') + valueMargin.h.toFixed(3)+'%';
  document.getElementById('vmD').textContent = (valueMargin.d>=0?'+':'') + valueMargin.d.toFixed(3)+'%';
  document.getElementById('vmA').textContent = (valueMargin.a>=0?'+':'') + valueMargin.a.toFixed(3)+'%';
  document.getElementById('edgeNote').innerHTML = edgeVal > 0
    ? `Widest positive edge: <b>${edgeSideName}</b> at <b>+${edgeVal.toFixed(3)}%</b> versus the bookmaker's normalized price.`
    : `No positive value edge found anywhere on this match. Per the model's own rule, this match should be <b>discarded</b> rather than staked.`;

  const ml = document.getElementById('marketList');
  ml.innerHTML = '';
  topMarkets.forEach((m,i)=>{
    const li = document.createElement('li');
    li.innerHTML = `<span><span class="rank">${i+1}</span><span class="name">${m.name}</span></span><span class="prob">${m.prob.toFixed(3)}%</span>`;
    ml.appendChild(li);
  });

  const sp = document.getElementById('scorePair');
  sp.innerHTML = '';
  topScores.forEach(s=>{
    const div = document.createElement('div');
    div.className = 'score-box';
    div.innerHTML = `<div class="sc">${s.h} - ${s.a}</div><div class="pp">${(s.p*100).toFixed(3)}% probability</div>`;
    sp.appendChild(div);
  });

  // ---------- Audit trail ----------
  const audit = document.getElementById('auditBody');
  function line(l,v){ return `<div class="audit-line"><span>${l}</span><span>${v}</span></div>`; }
  audit.innerHTML = `
    <div class="audit-section"><h5>Phase 1 — Conversion Rates</h5>
      ${line(nameA+' Pct Scored', p1A.PctScored.toFixed(3))}
      ${line(nameA+' Calc Scored', p1A.CalcScored.toFixed(3))}
      ${line(nameA+' Pct Concede', p1A.PctConcede.toFixed(3))}
      ${line(nameA+' Calc Concede', p1A.CalcConcede.toFixed(3))}
      ${line(nameB+' Pct Scored', p1B.PctScored.toFixed(3))}
      ${line(nameB+' Calc Scored', p1B.CalcScored.toFixed(3))}
      ${line(nameB+' Pct Concede', p1B.PctConcede.toFixed(3))}
      ${line(nameB+' Calc Concede', p1B.CalcConcede.toFixed(3))}
    </div>
    <div class="audit-section"><h5>Phase 2 — Net Score / Score Power</h5>
      ${line(nameA+' Net', p23A.Net.toFixed(3))}
      ${line(nameA+' Ratio', p23A.Ratio.toFixed(3))}
      ${line(nameA+' Power', p23A.Power.toFixed(3))}
      ${line(nameB+' Net', p23B.Net.toFixed(3))}
      ${line(nameB+' Ratio', p23B.Ratio.toFixed(3))}
      ${line(nameB+' Power', p23B.Power.toFixed(3))}
    </div>
    <div class="audit-section"><h5>Phase 3 — Final Strength</h5>
      ${line(nameA+' Strength (lambda Home)', StrengthA.toFixed(3))}
      ${line(nameB+' Strength (lambda Away)', StrengthB.toFixed(3))}
    </div>
    <div class="audit-section"><h5>Phase 4 — Baseline (raw Poisson sums before normalization)</h5>
      ${line('Raw Home / Draw / Away sum', (sums.home+sums.draw+sums.away).toFixed(3)+' (cap-truncated, normalized to 100% above)')}
    </div>
    <div class="audit-section"><h5>Phase 5 — Stress States (H% / D% / A%)</h5>
      ${states.map((s,i)=>line('State '+i, `${s.h.toFixed(3)} / ${s.d.toFixed(3)} / ${s.a.toFixed(3)}`)).join('')}
      ${line('sigma', SIGMA)} ${line('drag (100*sigma)', DRAG.toFixed(3))}
    </div>
    <div class="audit-section"><h5>Phase 6 — Bookmaker Normalized %</h5>
      ${line('Bookmaker Home%', bkPct.h.toFixed(3))}
      ${line('Bookmaker Draw%', bkPct.d.toFixed(3))}
      ${line('Bookmaker Away%', bkPct.a.toFixed(3))}
      ${line('Bookmaker overround (raw sum)', ((bkImplied.h+bkImplied.d+bkImplied.a)*100).toFixed(3)+'%')}
    </div>
    <div class="audit-section"><h5>Master + Dominance Fitted Grid (drives ALL scores &amp; markets below)</h5>
      ${line('Lambda fitted to Master% (Home)', masterLambdaH.toFixed(3))}
      ${line('Lambda fitted to Master% (Away)', masterLambdaA.toFixed(3))}
      ${line('Fit check — implied Home/Draw/Away %', `${mdOutcome.h.toFixed(2)} / N/A / ${mdOutcome.a.toFixed(2)} (pre-dominance)`)}
      ${line('Dominance adjustment Home (bounded, tanh-scaled)', '×'+domAdjFactor(domHome).toFixed(3))}
      ${line('Dominance adjustment Away (bounded, tanh-scaled)', '×'+domAdjFactor(domAway).toFixed(3))}
      ${line('FINAL Lambda Home (Master×Dominance)', mdLambdaH.toFixed(3))}
      ${line('FINAL Lambda Away (Master×Dominance)', mdLambdaA.toFixed(3))}
    </div>
    <div class="audit-section"><h5>Market Candidate Probabilities (all 5, from Master+Dominance grid)</h5>
      ${candidates.map(c=>line(c.name, c.prob.toFixed(3)+'%')).join('')}
    </div>
  `;
}
</script>
</body>
</html>
