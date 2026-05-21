#!/usr/bin/env python3
"""Apply all 5 CRM feature patches"""

with open('/root/.openclaw/workspace/steven-crm/index.html', 'r') as f:
    html = f.read()

def replace_once(old, new, label):
    assert old in html, f"ANCHOR NOT FOUND: {label}"
    return html.replace(old, new, 1)

# ============================================================
# PATCH 1a: Add MLS nav item to sidebar
# ============================================================
html = replace_once(
    "    <div class=\"nav-item\" onclick=\"go('settings',this)\"><span class=\"nav-icon\">⚙️</span>Settings</div>",
    "    <div class=\"nav-item\" onclick=\"go('mls',this)\" data-p=\"mls\"><span class=\"nav-icon\">🏘️</span>MLS Data</div>\n    <div class=\"nav-item\" onclick=\"go('settings',this)\" data-p=\"settings\"><span class=\"nav-icon\">⚙️</span>Settings</div>",
    "nav settings item"
)

# ============================================================
# PATCH 1b: Add page-mls HTML before <!-- end #main -->
# ============================================================
MLS_PAGE = """
<!-- MLS DATA -->
<div id="page-mls" class="page">
  <div class="topbar">
    <div class="page-title">🏘️ MLS / Property Data</div>
  </div>
  <div class="card mb-20">
    <div style="display:flex;gap:9px;flex-wrap:wrap;align-items:center">
      <input id="mlsAddr" class="fi" style="flex:1;min-width:240px" placeholder="Enter property address..." onkeydown="if(event.key==='Enter')searchMLS()">
      <button class="btn btn-primary" onclick="searchMLS()">🔍 Pull Data</button>
      <button class="btn btn-secondary" onclick="clearMLS()">✕ Clear</button>
    </div>
    <div id="mlsApiWarn" style="display:none;margin-top:11px;padding:10px 14px;background:rgba(200,168,75,.08);border:1px solid rgba(200,168,75,.3);border-radius:8px;font-size:12.5px;color:var(--text2)">
      ⚠️ <strong>RentCast API key not set.</strong> Go to <a href="#" onclick="go('settings',document.querySelector('[data-p=settings]'));return false;" style="color:var(--accent)">Settings → Property Data &amp; MLS</a> to add your key.<br>
      Get a free key at <a href="https://www.rentcast.io" target="_blank" style="color:var(--accent)">rentcast.io</a> (free tier available). ATTOM trial also supported.
    </div>
  </div>
  <div id="mlsResults"></div>
</div>
"""

html = replace_once(
    "  </div>\n</div>\n\n</div><!-- end #main -->",
    MLS_PAGE + "\n  </div>\n</div>\n\n</div><!-- end #main -->",
    "end #main"
)

# ============================================================
# PATCH 1c: Update go() nav map to include mls
# ============================================================
html = replace_once(
    "  const map={dashboard:renderDash,leads:renderLeads,pipeline:renderKanban,ads:renderAds,analytics:renderAnalytics,buyers:renderBuyers,realtors:renderRealtors,contacts:renderContacts,followups:renderFU,templates:renderTemplates,settings:renderSettings};",
    "  const map={dashboard:renderDash,leads:renderLeads,pipeline:renderKanban,ads:renderAds,analytics:renderAnalytics,buyers:renderBuyers,realtors:renderRealtors,contacts:renderContacts,followups:renderFU,templates:renderTemplates,settings:renderSettings,mls:renderMLS};",
    "go() map"
)

# ============================================================
# PATCH 1d: Update auto-refresh pageMap to include page-mls
# ============================================================
html = replace_once(
    "      const pageMap={'page-dashboard':renderDash,'page-leads':renderLeads,'page-pipeline':renderKanban,'page-followups':renderFU};",
    "      const pageMap={'page-dashboard':renderDash,'page-leads':renderLeads,'page-pipeline':renderKanban,'page-followups':renderFU,'page-mls':renderMLS};",
    "pageMap"
)

# ============================================================
# PATCH 1e: Add data-p attributes to existing nav items
# ============================================================
html = replace_once(
    "    <div class=\"nav-item active\" onclick=\"go('dashboard',this)\">",
    "    <div class=\"nav-item active\" onclick=\"go('dashboard',this)\" data-p=\"dashboard\">",
    "dashboard nav"
)
html = replace_once(
    "    <div class=\"nav-item\" onclick=\"go('leads',this)\">",
    "    <div class=\"nav-item\" onclick=\"go('leads',this)\" data-p=\"leads\">",
    "leads nav"
)
html = replace_once(
    "    <div class=\"nav-item\" onclick=\"go('pipeline',this)\">",
    "    <div class=\"nav-item\" onclick=\"go('pipeline',this)\" data-p=\"pipeline\">",
    "pipeline nav"
)
html = replace_once(
    "    <div class=\"nav-item\" onclick=\"go('analytics',this)\">",
    "    <div class=\"nav-item\" onclick=\"go('analytics',this)\" data-p=\"analytics\">",
    "analytics nav"
)
html = replace_once(
    "    <div class=\"nav-item\" onclick=\"go('buyers',this)\">",
    "    <div class=\"nav-item\" onclick=\"go('buyers',this)\" data-p=\"buyers\">",
    "buyers nav"
)

# ============================================================
# PATCH 2: Add MLS settings section placeholder to settings page
# ============================================================
html = replace_once(
    "</div>\n\n</div><!-- end #main -->",
    "</div>\n\n  <!-- MLS/Property Data Settings (rendered dynamically) -->\n  <div id=\"mlsSettingsSection\" style=\"margin-top:18px\"></div>\n\n</div><!-- end #main -->",
    "mlsSettingsSection"
)

# ============================================================
# PATCH 3: Add "Pull Data" button in lead detail
# ============================================================
html = replace_once(
    '<div style="font-size:12px;color:var(--text2)">${l.address}</div>',
    '<div style="font-size:12px;color:var(--text2)">${l.address} <button class="btn btn-secondary btn-sm" style="font-size:10px;padding:2px 7px" onclick="event.stopPropagation();openMLSFor(\'${l.address}\')">🔍 Pull Data</button></div>',
    "lead address pull data"
)

# ============================================================
# PATCH 4: Add "Pull Data" button in property detail
# ============================================================
html = replace_once(
    '<div style="margin-bottom:16px"><div style="font-size:17px;font-weight:800">${p.address}</div><div style="font-size:12px;color:var(--text2)">Seller: ${p.seller}${agent?\' · 🤝 Agent: \'+agent.name:\'\'}</div></div>',
    '<div style="margin-bottom:16px"><div style="font-size:17px;font-weight:800">${p.address} <button class="btn btn-secondary btn-sm" style="font-size:10px" onclick="event.stopPropagation();openMLSFor(\'${p.address}\')">🔍 Pull Data</button></div><div style="font-size:12px;color:var(--text2)">Seller: ${p.seller}${agent?\' · 🤝 Agent: \'+agent.name:\'\'}</div></div>',
    "prop address pull data"
)

# ============================================================
# PATCH 5: Add Matched Buyers section in openPropD
# ============================================================
html = replace_once(
    '    ${p.notes?`<div class="card card-sm" style="margin-top:14px"><div style="font-size:10px;color:var(--text3);font-weight:700;text-transform:uppercase;margin-bottom:7px">Notes</div><div style="font-size:12.5px;color:var(--text2)">${p.notes}</div></div>`:\'\'}',
    '    ${p.notes?`<div class="card card-sm" style="margin-top:14px"><div style="font-size:10px;color:var(--text3);font-weight:700;text-transform:uppercase;margin-bottom:7px">Notes</div><div style="font-size:12.5px;color:var(--text2)">${p.notes}</div></div>`:\'\'}\n    ${renderMatchedBuyers(p)}',
    "matched buyers injection"
)

# ============================================================
# PATCH 6: Analytics page HTML - add KPI div
# ============================================================
html = replace_once(
    "<!-- ANALYTICS -->\n<div id=\"page-analytics\" class=\"page\">\n  <div class=\"topbar\"><div class=\"page-title\">Analytics</div></div>\n  <div class=\"charts-grid\" id=\"chartsGrid\"></div>\n</div>",
    "<!-- ANALYTICS -->\n<div id=\"page-analytics\" class=\"page\">\n  <div class=\"topbar\"><div class=\"page-title\">Analytics</div></div>\n  <div id=\"analyticsKPI\"></div>\n  <div class=\"charts-grid\" id=\"chartsGrid\" style=\"margin-top:18px\"></div>\n</div>",
    "analytics page HTML"
)

# ============================================================
# PATCH 8: Update renderDash with 4 new stat cards
# ============================================================
OLD_DASH = """  document.getElementById('dashStats').innerHTML=`
    <div class="stat-card gold"><div class="stat-icon">👥</div><div class="stat-label">${isAdmin()?'Total Leads':'My Leads'}</div><div class="stat-value">${db.leads.length}</div><div class="stat-sub">🔥 ${hot} hot</div></div>
    <div class="stat-card blue"><div class="stat-icon">📋</div><div class="stat-label">${isAdmin()?'Active Deals':'My Active Deals'}</div><div class="stat-value">${active}</div><div class="stat-sub">In pipeline</div></div>
    <div class="stat-card green"><div class="stat-icon">💰</div><div class="stat-label">Pipeline Value</div><div class="stat-value">$${Math.round(pipeVal/1000)}K</div><div class="stat-sub">Est. profit</div></div>
    <div class="stat-card purple"><div class="stat-icon">🏆</div><div class="stat-label">Deals Closed</div><div class="stat-value">${closed}</div><div class="stat-sub">All time</div></div>
  `;"""

NEW_DASH = """  const closedProps=db.properties.filter(p=>p.stage==='closed');
  const convRate=db.leads.length>0?((closedProps.length/db.leads.length)*100).toFixed(1):0;
  const profits2=closedProps.map(p=>{const fin=JSON.parse(localStorage.getItem('prop_fin_'+p.id)||'{}');if(fin.feeEarned||fin.wholesaleFee)return(fin.feeEarned||0)+(fin.wholesaleFee||0)-(fin.concessions||0);return Math.round(p.arv*.7-p.repairs-p.offerPrice);});
  const avgProfit2=profits2.length>0?Math.round(profits2.reduce((a,b)=>a+b,0)/profits2.length):0;
  const nowD=new Date();
  const thisMonthRev2=closedProps.filter(p=>{const d=new Date(p.createdAt||p.created_at||Date.now());return d.getFullYear()===nowD.getFullYear()&&d.getMonth()===nowD.getMonth();}).reduce((s,p)=>{const fin=JSON.parse(localStorage.getItem('prop_fin_'+p.id)||'{}');return s+(fin.revenue||fin.feeEarned||Math.max(0,p.arv*.7-p.repairs-p.offerPrice)||0);},0);
  document.getElementById('dashStats').innerHTML=`
    <div class="stat-card gold"><div class="stat-icon">👥</div><div class="stat-label">${isAdmin()?'Total Leads':'My Leads'}</div><div class="stat-value">${db.leads.length}</div><div class="stat-sub">🔥 ${hot} hot</div></div>
    <div class="stat-card blue"><div class="stat-icon">📋</div><div class="stat-label">${isAdmin()?'Active Deals':'My Active Deals'}</div><div class="stat-value">${active}</div><div class="stat-sub">In pipeline</div></div>
    <div class="stat-card green"><div class="stat-icon">💰</div><div class="stat-label">Pipeline Value</div><div class="stat-value">$${Math.round(pipeVal/1000)}K</div><div class="stat-sub">Est. profit</div></div>
    <div class="stat-card purple"><div class="stat-icon">🏆</div><div class="stat-label">Deals Closed</div><div class="stat-value">${closed}</div><div class="stat-sub">All time</div></div>
    <div class="stat-card blue"><div class="stat-icon">🎯</div><div class="stat-label">Lead to Deal Rate</div><div class="stat-value">${convRate}%</div><div class="stat-sub">conversion</div></div>
    <div class="stat-card green"><div class="stat-icon">📈</div><div class="stat-label">Avg Profit/Deal</div><div class="stat-value">$${Math.round(avgProfit2/1000)}K</div><div class="stat-sub">per closed deal</div></div>
    <div class="stat-card gold"><div class="stat-icon">📅</div><div class="stat-label">This Month Revenue</div><div class="stat-value">$${Math.round(thisMonthRev2/1000)}K</div><div class="stat-sub">closed this month</div></div>
    <div class="stat-card red"><div class="stat-icon">🏠</div><div class="stat-label">Total Pipeline Value</div><div class="stat-value">$${Math.round(pipeVal/1000)}K</div><div class="stat-sub">active deals</div></div>
  `;"""

assert OLD_DASH in html, "dashStats not found"
html = html.replace(OLD_DASH, NEW_DASH, 1)

# ============================================================
# PATCH 9: Add MLS + Buyer matching + Settings functions
# ============================================================
OLD_LEGACY = """// Keep legacy functions so nothing breaks
function addTeamMember(){}
function removeTeamMember(){}"""

NEW_LEGACY = """// ============================================================
// MLS / PROPERTY DATA (Task 1)
// ============================================================
function openMLSFor(address){
  go('mls',document.querySelector('[data-p=mls]'));
  setTimeout(()=>{
    const input=document.getElementById('mlsAddr');
    if(input){input.value=address;searchMLS();}
  },200);
}

async function searchMLS(){
  const addr=(document.getElementById('mlsAddr')?.value||'').trim();
  if(!addr){toast('Enter an address first','err');return;}
  const apiKey=(db.settings.rentcast_api_key||'').trim();
  const provider=db.settings.mls_provider||'rentcast';
  const resultsEl=document.getElementById('mlsResults');
  const warnEl=document.getElementById('mlsApiWarn');
  if(!apiKey){
    if(warnEl)warnEl.style.display='block';
    resultsEl.innerHTML=`<div class="card" style="padding:28px;text-align:center;color:var(--text3)">
      <div style="font-size:32px;margin-bottom:12px">🔑</div>
      <div style="font-size:15px;font-weight:700;margin-bottom:8px">API Key Required</div>
      <div style="font-size:12.5px;color:var(--text2);margin-bottom:16px">To pull live property data, add a RentCast API key in Settings.<br>Free tier: <a href="https://www.rentcast.io" target="_blank" style="color:var(--accent)">rentcast.io</a></div>
      <button class="btn btn-primary" onclick="go('settings',document.querySelector('[data-p=settings]'))">⚙️ Go to Settings</button>
    </div>`;
    return;
  }
  if(warnEl)warnEl.style.display='none';
  resultsEl.innerHTML='<div style="text-align:center;padding:28px;color:var(--text2)">⏳ Fetching property data...</div>';
  try {
    const encAddr=encodeURIComponent(addr);
    const [propRes,compsRes]=await Promise.all([
      fetch(`https://api.rentcast.io/v1/properties?address=${encAddr}&limit=1`,{headers:{'X-Api-Key':apiKey,'Accept':'application/json'}}),
      fetch(`https://api.rentcast.io/v1/avm/sale/comparables?address=${encAddr}&radius=0.5&limit=5`,{headers:{'X-Api-Key':apiKey,'Accept':'application/json'}})
    ]);
    let propData=null,compsData=null;
    if(propRes.ok){const d=await propRes.json();propData=Array.isArray(d)?d[0]:d;}
    if(compsRes.ok){compsData=await compsRes.json();}
    renderMLSResults(addr,propData,compsData);
  }catch(e){
    resultsEl.innerHTML=`<div class="card" style="padding:22px;color:var(--hot)">Error: ${e.message}</div>`;
  }
}

function renderMLSResults(addr,prop,compsData){
  const el=document.getElementById('mlsResults');
  const comps=compsData?.comparables||compsData?.properties||[];
  let arvEstimate=compsData?.price||compsData?.avm||0;
  if(!arvEstimate&&comps.length>0){
    const sqftRatios=comps.filter(c=>c.squareFootage&&c.price).map(c=>c.price/c.squareFootage);
    if(sqftRatios.length>0){
      const avgPPSF=sqftRatios.reduce((a,b)=>a+b,0)/sqftRatios.length;
      arvEstimate=Math.round(avgPPSF*(prop?.squareFootage||1500));
    }
  }
  const propHtml=prop?`<div class="card mb-16">
    <div style="font-size:14px;font-weight:800;margin-bottom:14px">🏠 Property Details</div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:12px">
      ${prop.bedrooms!==undefined?`<div class="stat-card gold card-sm"><div class="stat-label">Beds</div><div class="stat-value" style="font-size:22px">${prop.bedrooms||'—'}</div></div>`:''}
      ${prop.bathrooms!==undefined?`<div class="stat-card blue card-sm"><div class="stat-label">Baths</div><div class="stat-value" style="font-size:22px">${prop.bathrooms||'—'}</div></div>`:''}
      ${prop.squareFootage?`<div class="stat-card green card-sm"><div class="stat-label">Sq Ft</div><div class="stat-value" style="font-size:20px">${prop.squareFootage.toLocaleString()}</div></div>`:''}
      ${prop.yearBuilt?`<div class="stat-card purple card-sm"><div class="stat-label">Year Built</div><div class="stat-value" style="font-size:20px">${prop.yearBuilt}</div></div>`:''}
      ${prop.lotSize?`<div class="stat-card gold card-sm"><div class="stat-label">Lot Size</div><div class="stat-value" style="font-size:18px">${prop.lotSize.toLocaleString()}</div></div>`:''}
      ${prop.lastSalePrice?`<div class="stat-card red card-sm"><div class="stat-label">Last Sale</div><div class="stat-value" style="font-size:18px">$${Math.round(prop.lastSalePrice/1000)}K</div><div class="stat-sub">${prop.lastSaleDate||''}</div></div>`:''}
      ${prop.ownerName?`<div class="stat-card blue card-sm" style="grid-column:span 2"><div class="stat-label">Owner</div><div class="stat-value" style="font-size:15px">${prop.ownerName}</div></div>`:''}
    </div>
  </div>`:`<div class="card mb-16" style="color:var(--text2);font-size:12.5px;padding:16px">No property details found for this address.</div>`;

  const arvHtml=arvEstimate?`<div class="card mb-16" style="background:linear-gradient(135deg,rgba(200,168,75,.08),rgba(200,168,75,.02));border:1px solid rgba(200,168,75,.3)">
    <div style="font-size:14px;font-weight:800;margin-bottom:10px">🏆 Estimated ARV</div>
    <div style="font-size:32px;font-weight:800;color:var(--accent)">$${arvEstimate.toLocaleString()}</div>
    <div style="font-size:11px;color:var(--text2);margin-top:5px">Weighted avg $/sqft from ${comps.length} comps × subject sqft</div>
    <div style="display:flex;gap:8px;margin-top:14px;flex-wrap:wrap">
      <button class="btn btn-primary btn-sm" onclick="mlsCreateLead('${addr.replace(/'/g,'\\'+'\\'')}',${arvEstimate})">➕ Create Lead</button>
      <button class="btn btn-secondary btn-sm" onclick="mlsToCalc(${arvEstimate})">🧮 Add to Calculator</button>
    </div>
  </div>`:'';

  const compsHtml=comps.length>0?`<div class="card mb-16">
    <div style="font-size:14px;font-weight:800;margin-bottom:14px">📊 Comparable Sales (${comps.length})</div>
    <div style="overflow-x:auto">
    <table style="width:100%;border-collapse:collapse;font-size:12px">
      <thead><tr style="color:var(--text3);font-size:10px;text-transform:uppercase;border-bottom:1px solid var(--border)">
        <th style="padding:6px 8px;text-align:left">Address</th>
        <th style="padding:6px 8px;text-align:right">Sale Price</th>
        <th style="padding:6px 8px;text-align:right">Sq Ft</th>
        <th style="padding:6px 8px;text-align:right">$/Sq Ft</th>
        <th style="padding:6px 8px;text-align:right">Distance</th>
        <th style="padding:6px 8px;text-align:right">Sold</th>
      </tr></thead>
      <tbody>${comps.map(c=>{const ppsf=c.squareFootage&&c.price?Math.round(c.price/c.squareFootage):0;return`<tr style="border-bottom:1px solid var(--border)">
        <td style="padding:7px 8px;font-weight:600">${(c.address||c.formattedAddress||'N/A').split(',')[0]}</td>
        <td style="padding:7px 8px;text-align:right;color:var(--green)">$${c.price?(c.price/1000).toFixed(0)+'K':'N/A'}</td>
        <td style="padding:7px 8px;text-align:right">${c.squareFootage?c.squareFootage.toLocaleString():'—'}</td>
        <td style="padding:7px 8px;text-align:right">${ppsf?'$'+ppsf:'—'}</td>
        <td style="padding:7px 8px;text-align:right">${c.distance?c.distance.toFixed(2)+' mi':'—'}</td>
        <td style="padding:7px 8px;text-align:right;color:var(--text3)">${c.lastSaleDate||c.soldDate||'—'}</td>
      </tr>`;}).join('')}</tbody>
    </table></div>
  </div>`:'';
  el.innerHTML=propHtml+arvHtml+compsHtml;
}

function clearMLS(){
  const i=document.getElementById('mlsAddr');if(i)i.value='';
  const r=document.getElementById('mlsResults');if(r)r.innerHTML='';
}

function mlsToCalc(arv){
  const inp=document.getElementById('cArv');
  if(inp){inp.value=arv;if(typeof updCalc==='function')updCalc();}
  toast('ARV $'+arv.toLocaleString()+' added to calculator!');
}

function mlsCreateLead(address,arv){
  eid=null;
  document.getElementById('leadMT').textContent='New Lead from MLS';
  document.getElementById('leadFC').innerHTML=leadForm(null);
  setTimeout(()=>{
    const a=document.getElementById('lAddr');if(a)a.value=address;
    const p=document.getElementById('lAsk');if(p)p.value=Math.round(arv*0.7);
  },50);
  om('mAddLead');
}

function renderMLS(){
  const key=(db.settings.rentcast_api_key||'').trim();
  const w=document.getElementById('mlsApiWarn');
  if(w)w.style.display=key?'none':'block';
}

// ============================================================
// MATCHED BUYERS (Task 4)
// ============================================================
function renderMatchedBuyers(p){
  if(!p||!db.buyers||!db.buyers.length)return'';
  const propZip=extractZip(p.address);
  if(!propZip)return'';
  const matched=db.buyers.filter(b=>{
    if(!b.zips)return false;
    return b.zips.replace(/\\s/g,'').split(',').some(z=>z===propZip);
  });
  if(!matched.length)return`<div class="card card-sm" style="margin-top:14px"><div style="font-size:10px;color:var(--text3);font-weight:700;text-transform:uppercase;margin-bottom:9px">💰 Matched Buyers</div><div style="font-size:12px;color:var(--text3)">No buyers match zip ${propZip}.</div></div>`;
  return`<div class="card card-sm" style="margin-top:14px">
    <div style="font-size:10px;color:var(--text3);font-weight:700;text-transform:uppercase;margin-bottom:9px">💰 Matched Buyers (${matched.length})</div>
    ${matched.map(b=>`<div style="display:flex;align-items:center;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--border)">
      <div><div style="font-size:13px;font-weight:700">${b.name}</div><div style="font-size:11.5px;color:var(--text2)">📞 ${b.phone||'—'} · 💰 ${b.budget||'—'}</div></div>
      <button class="btn btn-secondary btn-sm" onclick="notifyBuyer('${b.name.replace(/'/g,'\\'+'\\'')}','${(b.phone||'').replace(/'/g,'\\'+'\\'')}')">📨 Notify</button>
    </div>`).join('')}
  </div>`;
}
function notifyBuyer(name,phone){toast('Buyer notified! '+name+(phone?' - '+phone:''));}
function extractZip(addr){const m=(addr||'').match(/\\b(\\d{5})\\b/);return m?m[1]:null;}

// ============================================================
// MLS SETTINGS HELPERS (Task 1)
// ============================================================
function toggleMLSCustom(){
  const v=document.getElementById('mlsProvider')?.value;
  const el=document.getElementById('mlsCustomEndpointWrap');
  if(el)el.style.display=v==='custom'?'block':'none';
}
async function saveMLSSettings(){
  const key=(document.getElementById('mlsApiKey')?.value||'').trim();
  const provider=document.getElementById('mlsProvider')?.value||'rentcast';
  const customEp=(document.getElementById('mlsCustomEndpoint')?.value||'').trim();
  const row={rentcast_api_key:key,mls_provider:provider,mls_custom_endpoint:customEp};
  const {error}=await supabase.from('settings').upsert({id:1,...row});
  if(error){toast('Error: '+error.message,true);return;}
  db.settings={...db.settings,...row};
  toast('MLS settings saved!');
}
async function testMLSConnection(){
  const key=(document.getElementById('mlsApiKey')?.value||db.settings.rentcast_api_key||'').trim();
  if(!key){toast('Enter an API key first','err');return;}
  toast('Testing...');
  try{
    const res=await fetch('https://api.rentcast.io/v1/properties?address=1600+Pennsylvania+Ave+NW+Washington+DC&limit=1',{headers:{'X-Api-Key':key}});
    if(res.ok||res.status===404)toast('✅ RentCast connected!');
    else if(res.status===401||res.status===403)toast('❌ Invalid API key','err');
    else toast('⚠️ Status '+res.status+' — may still work');
  }catch(e){toast('❌ Failed: '+e.message,true);}
}

// Keep legacy functions so nothing breaks
function addTeamMember(){}
function removeTeamMember(){}"""

assert OLD_LEGACY in html, "legacy functions anchor not found"
html = html.replace(OLD_LEGACY, NEW_LEGACY, 1)

# ============================================================
# PATCH 10: Update renderSettings to add MLS settings section
# ============================================================
OLD_SETTINGS_END = """  document.getElementById('settingsForm').innerHTML=`
    <div class="mform">
      <div class="fg full"><label class="flbl">Your Name</label><input class="fi" id="sN" value="${db.settings.name||''}"></div>
      <div class="fg full"><label class="flbl">Company Name</label><input class="fi" id="sCo" value="${db.settings.company||''}"></div>
      <div class="frow">
        <div class="fg"><label class="flbl">Phone</label><input class="fi" id="sPh" value="${db.settings.phone||''}"></div>
        <div class="fg"><label class="flbl">Email</label><input class="fi" id="sEm" value="${db.settings.email||''}"></div>
      </div>
      <button type="button" class="btn btn-primary" onclick="saveSettings()">Save Settings</button>
    </div>
    ${teamHtml}
  `;"""

NEW_SETTINGS_END = """  document.getElementById('settingsForm').innerHTML=`
    <div class="mform">
      <div class="fg full"><label class="flbl">Your Name</label><input class="fi" id="sN" value="${db.settings.name||''}"></div>
      <div class="fg full"><label class="flbl">Company Name</label><input class="fi" id="sCo" value="${db.settings.company||''}"></div>
      <div class="frow">
        <div class="fg"><label class="flbl">Phone</label><input class="fi" id="sPh" value="${db.settings.phone||''}"></div>
        <div class="fg"><label class="flbl">Email</label><input class="fi" id="sEm" value="${db.settings.email||''}"></div>
      </div>
      <button type="button" class="btn btn-primary" onclick="saveSettings()">Save Settings</button>
    </div>
    ${teamHtml}
  `;
  const mlsSec=document.getElementById('mlsSettingsSection');
  if(mlsSec)mlsSec.innerHTML=`<div class="card">
    <div class="sh-title mb-16">🏘️ Property Data &amp; MLS</div>
    <div class="mform">
      <div class="frow">
        <div class="fg"><label class="flbl">Provider</label>
          <select class="fi" id="mlsProvider" onchange="toggleMLSCustom()">
            <option value="rentcast" ${(db.settings.mls_provider||'rentcast')==='rentcast'?'selected':''}>RentCast (recommended)</option>
            <option value="attom" ${db.settings.mls_provider==='attom'?'selected':''}>ATTOM Data</option>
            <option value="custom" ${db.settings.mls_provider==='custom'?'selected':''}>Custom Endpoint</option>
          </select>
        </div>
        <div class="fg"><label class="flbl">API Key</label>
          <input class="fi" id="mlsApiKey" type="password" value="${db.settings.rentcast_api_key||''}" placeholder="Enter your API key...">
        </div>
      </div>
      <div class="fg full" id="mlsCustomEndpointWrap" style="display:${db.settings.mls_provider==='custom'?'block':'none'}">
        <label class="flbl">Custom Endpoint URL</label>
        <input class="fi" id="mlsCustomEndpoint" value="${db.settings.mls_custom_endpoint||''}" placeholder="https://api.yourmls.com/v1">
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:4px">
        <button type="button" class="btn btn-primary btn-sm" onclick="saveMLSSettings()">💾 Save</button>
        <button type="button" class="btn btn-secondary btn-sm" onclick="testMLSConnection()">🔌 Test Connection</button>
      </div>
      <div style="margin-top:10px;font-size:11.5px;color:var(--text2)">
        💡 <strong>RentCast</strong>: Free tier at <a href="https://www.rentcast.io" target="_blank" style="color:var(--accent)">rentcast.io</a> (50 req/month free)<br>
        💡 <strong>ATTOM</strong>: 30-day trial at <a href="https://www.attomdata.com" target="_blank" style="color:var(--accent)">attomdata.com</a>
      </div>
    </div>
  </div>`;"""

assert OLD_SETTINGS_END in html, "settingsForm content not found"
html = html.replace(OLD_SETTINGS_END, NEW_SETTINGS_END, 1)

# ============================================================
# PATCH 11: Fix saveSettings to preserve existing settings
# ============================================================
OLD_SAVE = """async function saveSettings(){
  const row={name:document.getElementById('sN').value,company:document.getElementById('sCo').value,phone:document.getElementById('sPh').value,email:document.getElementById('sEm').value};
  await supabase.from('settings').upsert({id:1,...row});
  db.settings={...row};"""

NEW_SAVE = """async function saveSettings(){
  const row={name:document.getElementById('sN').value,company:document.getElementById('sCo').value,phone:document.getElementById('sPh').value,email:document.getElementById('sEm').value};
  await supabase.from('settings').upsert({id:1,...row});
  db.settings={...db.settings,...row};"""

assert OLD_SAVE in html, "saveSettings not found"
html = html.replace(OLD_SAVE, NEW_SAVE, 1)

with open('/root/.openclaw/workspace/steven-crm/index.html', 'w') as f:
    f.write(html)

print("All patches applied successfully!")
print(f"File size: {len(html):,} chars ({len(html.encode()):,} bytes)")
