
const jobs = [
  {company:"Northwind Robotics", role:"Field Deployment Engineer", meta:"Remote · Match 94%"},
  {company:"Halcyon Data", role:"Forward Deployed Engineer", meta:"Austin, TX · Match 91%"},
  {company:"Ferro Systems", role:"Solutions Architect", meta:"Remote · Match 88%"},
  {company:"Basecamp Labs", role:"Technical Chief of Staff", meta:"Remote · Match 97%"},
  {company:"Lumen Fraud Co.", role:"Sr. Sales Engineer", meta:"Austin, TX · Match 85%"}
];
let jobIdx = 0, likedCount = 0;
function renderSwipe(){
  if(jobIdx >= jobs.length){
    document.getElementById('swipe-company').textContent = "queue refilled";
    document.getElementById('swipe-role').textContent = "dailyJobRefresh cron just ran";
    document.getElementById('swipe-meta').textContent = "5 new matches loaded";
    document.getElementById('swipe-status').textContent = `Liked: ${likedCount} · Queue: 5 remaining`;
    jobIdx = 0;
    return;
  }
  const j = jobs[jobIdx];
  document.getElementById('swipe-company').textContent = j.company;
  document.getElementById('swipe-role').textContent = j.role;
  document.getElementById('swipe-meta').textContent = j.meta;
  document.getElementById('swipe-status').textContent = `Liked: ${likedCount} · Queue: ${jobs.length - jobIdx - 1} remaining`;
}
function swipeCard(dir){
  const card = document.getElementById('swipe-card');
  card.classList.add(dir === 'like' ? 'like-out' : 'pass-out');
  if(dir === 'like') likedCount++;
  setTimeout(()=>{
    card.classList.remove('like-out','pass-out');
    jobIdx++;
    renderSwipe();
  }, 280);
}
renderSwipe();
const pipeSteps = ["Ingest","Clean & Normalize","Classify","Summarize","Deliver"];
const pipeRow = document.getElementById('pipe-row');
pipeSteps.forEach((s,i)=>{
  const el = document.createElement('div');
  el.className = 'pipe-step';
  el.id = 'pstep-'+i;
  el.textContent = s;
  pipeRow.appendChild(el);
});
function runPipeline(){
  pipeSteps.forEach((_,i)=>document.getElementById('pstep-'+i).className='pipe-step');
  const log = document.getElementById('pipe-log');
  log.textContent = '';
  const lines = [
    "-> pulling raw feedback batch (n=214)...",
    "-> cleaning + normalizing fields...",
    "-> classifying by feature area...",
    "-> summarizing via LangChain -> GPT-4...",
    "check: digest delivered to exec inbox"
  ];
  pipeSteps.forEach((_,i)=>{
    setTimeout(()=>{
      if(i>0) document.getElementById('pstep-'+(i-1)).className='pipe-step done';
      document.getElementById('pstep-'+i).className='pipe-step active';
      log.textContent += lines[i] + "\n";
      if(i === pipeSteps.length-1){
        setTimeout(()=>document.getElementById('pstep-'+i).className='pipe-step done', 500);
      }
    }, i*650);
  });
}
function haversine(lat1,lon1,lat2,lon2){
  const R = 6371;
  const dLat = (lat2-lat1)*Math.PI/180;
  const dLon = (lon2-lon1)*Math.PI/180;
  const a = Math.sin(dLat/2)**2 + Math.cos(lat1*Math.PI/180)*Math.cos(lat2*Math.PI/180)*Math.sin(dLon/2)**2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}
function runHaversine(){
  const [c1,c2] = document.getElementById('hv-center').value.split(',').map(s=>parseFloat(s));
  const [p1,p2] = document.getElementById('hv-point').value.split(',').map(s=>parseFloat(s));
  const radius = parseFloat(document.getElementById('hv-radius').value);
  const dist = haversine(c1,c2,p1,p2);
  const box = document.getElementById('hv-result');
  if(dist <= radius){
    box.className = 'result-box pass';
    box.textContent = `PASS - computed distance ${dist.toFixed(2)} km <= radius ${radius} km`;
  } else {
    box.className = 'result-box fail';
    box.textContent = `FAIL - computed distance ${dist.toFixed(2)} km exceeds radius ${radius} km`;
  }
}
function runMigration(){
  const raw = document.getElementById('mig-input').value.split('\n').filter(r=>r.trim());
  let rows = [];
  raw.forEach(line=>{
    const parts = line.split(',').map(s=>s.trim());
    const [name, email, date] = parts;
    const cleanName = name.split(' ').filter(Boolean).map(w=>w[0].toUpperCase()+w.slice(1).toLowerCase()).join(' ');
    const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    let dateOk = true, normDate = date;
    const m = date.match(/^(\d{1,4})[\/\-](\d{1,2})[\/\-](\d{1,4})$/);
    if(m){ normDate = date; } else { dateOk = false; }
    rows.push({name:cleanName, email, date:normDate, flag: !emailOk || !dateOk});
  });
  let html = '<table class="mig-table"><tr><th>Name</th><th>Email</th><th>Signup Date</th><th>Status</th></tr>';
  let flagged = 0;
  rows.forEach(r=>{
    if(r.flag) flagged++;
    html += `<tr class="${r.flag?'flag':''}"><td>${r.name}</td><td>${r.email}</td><td>${r.date}</td><td>${r.flag?'needs review':'clean'}</td></tr>`;
  });
  html += '</table>';
  if(flagged) html += `<div class="mig-flag-label">${flagged} row(s) flagged for human review - malformed email or date</div>`;
  document.getElementById('mig-output').innerHTML = html;
}
function runSync(){
  const dot = document.getElementById('sync-dot');
  const pbSub = document.getElementById('pb-sub');
  const sfSub = document.getElementById('sf-sub');
  const map = document.getElementById('sync-map');
  dot.style.left = '130px'; dot.style.background = '#E8A33D';
  pbSub.textContent = 'syncing...';
  setTimeout(()=>{
    dot.style.left = 'calc(100% - 140px)';
  }, 100);
  setTimeout(()=>{
    dot.style.background = '#5FD9A4';
    pbSub.textContent = 'Note created: "Bulk export API"';
    map.innerHTML = `<div class="row"><span>Opportunity: "Bulk export API"</span><span>-> Feature note created</span></div><div class="row"><span>Stage: Discovery</span><span>-> Priority: Medium</span></div>`;
  }, 1100);
  setTimeout(()=>{
    dot.style.left = '130px';
    sfSub.textContent = 'field updated';
  }, 1900);
  setTimeout(()=>{
    map.innerHTML += `<div class="row"><span>Roadmap: In Progress</span><span>-> Opportunity field synced</span></div>`;
  }, 2600);
}
const agentResponses = {
  "summarize my week": "This week: 3 new enterprise feature requests logged from Salesforce sync, the Nova integration moved to In Progress, and 2 client calls need follow-up (Acme, Halcyon). No blockers flagged.",
  "draft a follow-up email": "Subject: Following up from today\n\nHi [Name] - great talking today. Recapping: we'll get the API sandbox credentials over by EOD Friday, and I'll loop in engineering on the webhook question you raised. Let me know if anything's missing.",
  "what changed on project nova?": "Project Nova: priority moved from Medium to High after 4 new enterprise requests synced in from Salesforce this week. Engineering estimate now targets late Q3."
};
function askAgent(q){
  event && event.stopPropagation && event.stopPropagation();
  if(!q || !q.trim()) return;
  const key = q.trim().toLowerCase();
  const out = document.getElementById('agent-text');
  out.textContent = '...';
  const resp = agentResponses[key] || "Got it - let me pull the latest context on that and draft a response. (In the live version this queries Productboard + CRM directly.)";
  let i = 0;
  const typer = setInterval(()=>{
    out.textContent = resp.slice(0, i);
    i += 3;
    if(i > resp.length) clearInterval(typer);
  }, 12);
}
function runTerminal(){
  const box = document.getElementById('term-box');
  box.textContent = '';
  const lines = [
    "$ python bot.py --check",
    "-> polling Ankara consulate...  no slots",
    "-> polling Istanbul consulate...  no slots",
    "-> polling Izmir consulate...  slot found: Jul 14, 09:40",
    "-> sending Telegram alert...",
    "check: alert sent - 5711747330"
  ];
  let i = 0;
  const iv = setInterval(()=>{
    if(i < lines.length){
      box.textContent += (i>0?'\n':'') + lines[i];
      i++;
    } else clearInterval(iv);
  }, 450);
}
function renderDoc(){
  document.getElementById('dg-name-out').textContent = document.getElementById('dg-name').value;
  document.getElementById('dg-tag-out').textContent = document.getElementById('dg-tag').value;
  const color = document.getElementById('dg-color').value;
  document.getElementById('dg-name-out').style.color = color;
  document.getElementById('dg-bar-out').style.background = color;
}
renderDoc();
function renderBoard(){
  const arr = parseFloat(document.getElementById('bd-arr').value) || 0;
  const churn = parseFloat(document.getElementById('bd-churn').value) || 0;
  const hc = parseInt(document.getElementById('bd-hc').value) || 0;
  document.getElementById('bd-arr-out').textContent = '$' + arr + 'k';
  document.getElementById('bd-churn-out').textContent = churn + '%';
  document.getElementById('bd-hc-out').textContent = hc;
  let note = `ARR at $${arr}k this period. `;
  note += churn > 2.5 ? `Net churn at ${churn}% is above trend - worth a line of color for the board. ` : `Net churn holding steady at ${churn}%. `;
  note += `Headcount at ${hc}, ` + (hc > 40 ? 'above plan - flag hiring pace.' : 'in line with plan.');
  document.getElementById('bd-narrative').textContent = note;
}
renderBoard();
function extractActions(){
  const text = document.getElementById('mtg-input').value;
  const sentences = text.split(/(?<=[.!?])\s+/).filter(s=>s.trim());
  const actionWords = /\b(will|should|need to|needs to|follow up|loop in|send|finalize|schedule)\b/i;
  let html = '';
  let found = 0;
  sentences.forEach(s=>{
    if(actionWords.test(s)){
      found++;
      const ownerMatch = s.match(/^([A-Z][a-z]+)\b/);
      const owner = ownerMatch ? ownerMatch[1] : 'Unassigned';
      html += `<div class="action-item"><span class="owner">${owner}</span><span>${s.trim()}</span></div>`;
    }
  });
  if(!found) html = '<div class="proto-status">No clear action items detected in this text.</div>';
  document.getElementById('mtg-output').innerHTML = html;
}
const today = new Date('2026-07-02');
const contracts = [
  {name:"AWS Enterprise Support", date:"2026-07-18"},
  {name:"Salesforce Sales Cloud", date:"2026-08-30"},
  {name:"Office lease - Austin HQ", date:"2026-09-15"},
  {name:"LoopCV API contract", date:"2027-01-10"},
  {name:"Payroll/HRIS platform", date:"2026-07-09"}
];
function renderRenewals(){
  let html = '<tr><th>Contract</th><th>Renewal date</th><th>Days out</th><th>Status</th></tr>';
  contracts.forEach(c=>{
    const d = new Date(c.date);
    const days = Math.round((d - today) / 86400000);
    let pill = 'green', label = 'On track';
    if(days <= 14){ pill='red'; label='Act now'; }
    else if(days <= 45){ pill='amber'; label='Notice window'; }
    html += `<tr><td>${c.name}</td><td>${c.date}</td><td>${days}d</td><td><span class="ren-pill ${pill}">${label}</span></td></tr>`;
  });
  document.getElementById('ren-table').innerHTML = html;
}
renderRenewals();
/* Clients - delivered digest output */
function runDigest(){
  const out = document.getElementById('digest-out');
  out.innerHTML = '';
  const lines = [
    "<span class='k'>WEEKLY FEEDBACK DIGEST</span> · 1,240 items processed",
    "",
    "<span class='k'>Integrations (312 items, +18% w/w)</span>",
    "<span class='v'>  Top theme: bulk export API - 47 requests</span>",
    "<span class='v'>  Sentiment: frustrated, blocking enterprise deals</span>",
    "",
    "<span class='k'>Reporting (204 items)</span>",
    "<span class='v'>  Top theme: custom dashboard fields - 31 requests</span>",
    "",
    "<span class='k'>Mobile (156 items, NEW spike)</span>",
    "<span class='v'>  Top theme: offline mode - 22 requests</span>",
    "",
    "<span class='k'>-> Routed to 3 product teams automatically</span>"
  ];
  let i = 0;
  const iv = setInterval(()=>{
    if(i < lines.length){ out.innerHTML += (i>0?'\n':'') + lines[i]; i++; }
    else clearInterval(iv);
  }, 130);
}
/* Generic live-Claude caller - reused across every AI-generation demo.
   One live call per task per browser session; falls back gracefully on error. */
async function callLive(task, input, outId, btnId, noteId, fallbackFn){
  const key = 'liveUsed_' + task;
  const out = document.getElementById(outId);
  const btn = document.getElementById(btnId);
  const note = noteId ? document.getElementById(noteId) : null;
  out.style.display = 'block';
  if(sessionStorage.getItem(key)){
    if(note) note.textContent = 'Live call already used this session for this demo - showing the instant version.';
    if(fallbackFn) fallbackFn();
    return;
  }
  if(!input || !input.trim()) return;
  const origLabel = btn.textContent;
  btn.disabled = true;
  btn.textContent = 'Calling Claude...';
  out.textContent = 'Calling Claude live - one moment...';
  try {
    const res = await fetch('/api/translate', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({task, ask: input})
    });
    if(!res.ok) throw new Error('API error: ' + res.status);
    const data = await res.json();
    if(!data.spec) throw new Error('Empty response');
    out.textContent = '● LIVE CLAUDE RESPONSE\n\n' + data.spec;
    sessionStorage.setItem(key, '1');
    btn.textContent = '✓ Live call used this session';
    if(note) note.textContent = 'That was a real Claude API call, not scripted.';
  } catch(err){
    if(fallbackFn) fallbackFn();
    btn.disabled = false;
    btn.textContent = origLabel;
    if(note) note.textContent = 'Live endpoint hit an error - showing the instant version instead.';
  }
}
function runLiveReq(){
  callLive('spec', document.getElementById('req-in').value.trim(), 'req-out', 'live-btn', 'live-note', runReq);
}
function runGapAgentLive(){
  const input = document.getElementById('agent-config-in').value.trim();
  callLive('gap-agent', input, 'gap-live-out', 'gap-live-btn', 'gap-live-note', null);
}
function askAgentLive(){
  const input = document.getElementById('agent-in').value.trim() || 'Summarize my week';
  callLive('colleague-agent', input, 'agent-live-out', 'agent-live-btn', 'agent-live-note', null);
}
function runBoardLive(){
  const arr = document.getElementById('bd-arr').value;
  const churn = document.getElementById('bd-churn').value;
  const hc = document.getElementById('bd-hc').value;
  const input = `ARR: $${arr}k. Net churn: ${churn}%. Headcount: ${hc}.`;
  callLive('board-narrative', input, 'board-live-out', 'board-live-btn', 'board-live-note', null);
}
function runMeetingLive(){
  const input = document.getElementById('mtg-input').value.trim();
  callLive('meeting-actions', input, 'mtg-live-out', 'mtg-live-btn', 'mtg-live-note', extractActions);
}
function runHealthLive(){
  const usage = document.getElementById('h-usage').value;
  const integ = document.getElementById('h-integ').value;
  const admin = document.getElementById('h-admin').value;
  const score = document.getElementById('h-score').textContent;
  const input = `Account: Acme Manufacturing, Enterprise tier, renews in 45 days. Active usage: ${usage}/100. Integration depth: ${integ}/100. Admin engagement: ${admin}/100. Computed health score: ${score}/100.`;
  callLive('health-summary', input, 'health-out', 'health-live-btn', 'health-note', null);
}
/* SA2 - requirements translator */
function runReq(){
  const ask = document.getElementById('req-in').value.toLowerCase();
  let spec;
  if(ask.includes('gl') || ask.includes('coding')){
    spec =
`<span class="k">Systems:</span> <span class="v">HRIS -> ERP (GL module)</span>
<span class="k">Trigger:</span> <span class="v">employee.created event</span>
<span class="k">Data flow:</span> <span class="v">one-way, HRIS -> ERP</span>
<span class="k">Field map:</span>
  department -> gl_segment (lookup table)
  employee_id -> vendor_ref
  start_date -> effective_date
<span class="k">Edge cases:</span>
  - department with no GL mapping -> flag for review
  - mid-period start -> proration rule
  - contractor vs FTE -> different GL account`;
  } else if(ask.includes('deprovision') || ask.includes('access') || ask.includes('team')){
    spec =
`<span class="k">Systems:</span> <span class="v">HRIS -> Identity (Okta) -> Apps</span>
<span class="k">Trigger:</span> <span class="v">employee.department_changed</span>
<span class="k">Data flow:</span> <span class="v">event-driven, real-time</span>
<span class="k">Logic:</span>
  diff old vs new group memberships
  revoke apps not in new role bundle
  grant apps in new role bundle
<span class="k">Edge cases:</span>
  - shared apps across roles -> keep, don't revoke
  - in-flight approvals -> hold until resolved
  - break-glass admin access -> never auto-revoke`;
  } else if(ask.includes('warehouse') || ask.includes('sync') || ask.includes('nightly')){
    spec =
`<span class="k">Systems:</span> <span class="v">HRIS -> Data warehouse (Snowflake)</span>
<span class="k">Trigger:</span> <span class="v">scheduled, nightly batch</span>
<span class="k">Data flow:</span> <span class="v">ETL, incremental load</span>
<span class="k">Pipeline:</span>
  extract changed records since last run
  transform to dimensional schema
  load into employee_dim + headcount_fact
<span class="k">Edge cases:</span>
  - late-arriving records -> reconciliation pass
  - PII columns -> masked in non-prod
  - schema drift -> alert, don't fail silently`;
  } else {
    spec =
`<span class="k">Systems:</span> <span class="v">resolved from source + destination</span>
<span class="k">Trigger:</span> <span class="v">event or schedule (TBD in review)</span>
<span class="k">Data flow:</span> <span class="v">direction inferred from intent</span>
<span class="k">Next step:</span> confirm field-level mapping in workshop
<span class="k">Edge cases:</span> flagged once systems are named`;
  }
  document.getElementById('req-out').innerHTML = spec;
}
runReq();
/* SA3 - gap scorecard */
const gaps = [
  {name:"SSO enforced across all users", sev:"high", on:true},
  {name:"Automated offboarding / deprovisioning", sev:"high", on:false},
  {name:"Cost-center mapping to finance system", sev:"med", on:false},
  {name:"MFA required for admin roles", sev:"high", on:true},
  {name:"Integration error alerting configured", sev:"med", on:false},
  {name:"Role-based access bundles defined", sev:"med", on:true}
];
function renderGaps(){
  const list = document.getElementById('gap-list');
  list.innerHTML = '';
  gaps.forEach((g,i)=>{
    const row = document.createElement('div');
    row.className = 'gap-row';
    row.innerHTML = `<div class="gap-check ${g.on?'on':''}" onclick="toggleGap(${i})"></div><span>${g.name}</span><span class="gap-sev ${g.sev}">${g.sev==='high'?'high risk':'medium'}</span>`;
    list.appendChild(row);
  });
  const total = gaps.length;
  const inPlace = gaps.filter(g=>g.on).length;
  const openHigh = gaps.filter(g=>!g.on && g.sev==='high').length;
  const score = Math.round((inPlace/total)*100);
  const scoreColor = score>=80?'var(--mint)':score>=50?'var(--amber)':'var(--red)';
  document.getElementById('gap-score').innerHTML =
    `Agent readiness score: <span style="color:${scoreColor}">${score}%</span> · ${inPlace}/${total} best practices in place` +
    (openHigh?` · <span style="color:var(--red)">agent flagged ${openHigh} high-risk gap${openHigh>1?'s':''} to prioritize</span>`:` · <span style="color:var(--mint)">no high-risk gaps found</span>`);
}
function toggleGap(i){ gaps[i].on = !gaps[i].on; renderGaps(); }
renderGaps();
/* SA6 - decision tree */
const tree = {
  q:"Sync is failing. What's the symptom?",
  opts:[
    {label:"Intermittent failures", next:{
      q:"Do failures correlate with volume spikes?",
      opts:[
        {label:"Yes", answer:"Root cause: rate limiting on the destination API. Fix: implement exponential backoff + request queuing. Batch writes under the rate ceiling."},
        {label:"No", answer:"Root cause: likely token expiry mid-sync. Fix: add proactive token refresh before batch runs; check OAuth refresh-token rotation."}
      ]
    }},
    {label:"Total failure, nothing syncs", next:{
      q:"Did it ever work, or is this a new setup?",
      opts:[
        {label:"Worked before", answer:"Root cause: a credential or endpoint changed. Fix: verify API key validity and check for a deprecated endpoint version in the destination's changelog."},
        {label:"New setup", answer:"Root cause: auth scope or field-mapping misconfiguration. Fix: confirm the integration user has write scope and required fields are mapped and non-null."}
      ]
    }},
    {label:"Data syncs but is wrong", next:{
      q:"Wrong values, or wrong records?",
      opts:[
        {label:"Wrong values", answer:"Root cause: a transformation/format mismatch (date, enum, units). Fix: audit the field mapping for type coercion; add validation on the transform step."},
        {label:"Wrong records", answer:"Root cause: filter or dedup logic is off. Fix: review the query filter and unique-key matching; check for duplicate source records."}
      ]
    }}
  ]
};
function renderTree(node, path){
  const box = document.getElementById('tree-box');
  let html = '';
  if(path.length) html += `<div class="tree-path">${path.join('  ->  ')}</div>`;
  if(node.answer){
    html += `<div class="tree-answer"><div class="ta-label">Root cause + fix</div>${node.answer}</div>`;
    html += `<button class="proto-btn" style="margin-top:12px;" onclick="startTree()">↺ Start over</button>`;
    box.innerHTML = html;
    return;
  }
  html += `<div class="tree-q">${node.q}</div><div class="tree-opts">`;
  node.opts.forEach((o,i)=>{
    html += `<button class="proto-btn" onclick="treeStep(${i})">${o.label}</button>`;
  });
  html += `</div>`;
  box.innerHTML = html;
  window._treeNode = node;
  window._treePath = path;
}
function treeStep(i){
  const chosen = window._treeNode.opts[i];
  const newPath = [...window._treePath, chosen.label];
  renderTree(chosen.next || {answer:chosen.answer}, newPath);
}
function startTree(){ renderTree(tree, []); }
startTree();
/* SA7 - health dashboard */
function runHealth(){
  const u = +document.getElementById('h-usage').value;
  const i = +document.getElementById('h-integ').value;
  const a = +document.getElementById('h-admin').value;
  const score = Math.round(u*0.45 + i*0.35 + a*0.20);
  const el = document.getElementById('h-score');
  el.textContent = score;
  let color, rec;
  if(score>=70){ color='var(--mint)'; rec='Healthy - candidate for expansion conversation.'; }
  else if(score>=45){ color='var(--amber)'; rec='Watch - schedule an architecture review to deepen adoption.'; }
  else { color='var(--red)'; rec='At risk - proactive intervention needed before renewal.'; }
  el.style.color = color;
  document.getElementById('h-rec').textContent = rec;
}
runHealth();
/* SA8 - consolidation calculator */
const tools = [
  {name:"Standalone HRIS", price:1200, on:true},
  {name:"Separate payroll provider", price:900, on:true},
  {name:"IT / identity tool", price:800, on:true},
  {name:"Expense management", price:600, on:false},
  {name:"Benefits admin platform", price:700, on:true},
  {name:"Contractor payments tool", price:400, on:false}
];
function renderConsol(){
  const list = document.getElementById('consol-list');
  list.innerHTML = '';
  tools.forEach((t,i)=>{
    const row = document.createElement('label');
    row.className = 'consol-item';
    row.innerHTML = `<input type="checkbox" ${t.on?'checked':''} onchange="toggleTool(${i})" onclick="event.stopPropagation()"> <span>${t.name}</span> <span class="price">$${t.price}/mo</span>`;
    list.appendChild(row);
  });
  const current = tools.filter(t=>t.on).reduce((s,t)=>s+t.price,0);
  const consolidated = Math.round(current*0.62);
  const saved = current - consolidated;
  const integrations = tools.filter(t=>t.on).length;
  const savedPct = current? Math.round(saved/current*100):0;
  document.getElementById('consol-out').innerHTML =
    `Current stack: $${current}/mo across ${integrations} tools<br>Consolidated: $${consolidated}/mo · <span class="save">$${saved}/mo saved</span> (${savedPct}%)<br><span style="color:var(--text-dim);font-size:11px">${Math.max(0,integrations-1)} integration points eliminated</span>`;
}
function toggleTool(i){ tools[i].on = !tools[i].on; renderConsol(); }
renderConsol();
/* SA9 - warehouse query */
function runQuery(type){
  let out;
  if(type==='cost'){
    out =
`<span class="k">SELECT</span> tier, <span class="k">COUNT</span>(*) AS accounts, <span class="k">SUM</span>(monthly_usage) AS usage
<span class="k">FROM</span> usage_fact f
<span class="k">JOIN</span> account_dim d <span class="k">ON</span> f.acct_key = d.acct_key
<span class="k">GROUP BY</span> tier;
<span class="v">Enterprise    42     1,840,000
Growth       118       960,000
Starter      340       410,000</span>`;
  } else if(type==='growth'){
    out =
`<span class="k">SELECT</span> quarter, active_accounts,
  active_accounts - <span class="k">LAG</span>(active_accounts) <span class="k">OVER</span>(<span class="k">ORDER BY</span> quarter) AS delta
<span class="k">FROM</span> account_snapshot;
<span class="v">Q1 2026    468     -
Q2 2026    501    +33
Q3 2026    542    +41</span>`;
  } else {
    out =
`<span class="k">SELECT</span> tier, <span class="k">ROUND</span>(<span class="k">AVG</span>(integration_count),1) AS avg_integrations
<span class="k">FROM</span> usage_fact f
<span class="k">JOIN</span> account_dim d <span class="k">ON</span> f.acct_key = d.acct_key
<span class="k">GROUP BY</span> tier;
<span class="v">Enterprise    6.4
Growth        3.1
Starter       1.2</span>`;
  }
  document.getElementById('wh-out').innerHTML = out;
}
document.querySelectorAll('.navbar a').forEach(a=>{
  a.addEventListener('click', e=>{
    e.preventDefault();
    document.querySelector(a.getAttribute('href')).scrollIntoView({behavior:'smooth', block:'start'});
  });
});
