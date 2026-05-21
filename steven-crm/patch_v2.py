#!/usr/bin/env python3
"""Steven CRM v2 — Luxury design + Investors + Photos/Docs/Notes via Supabase"""

with open('/root/.openclaw/workspace/steven-crm/index.html', 'r') as f:
    html = f.read()

def rp(old, new, label):
    if old not in html:
        print(f"[SKIP] ANCHOR NOT FOUND: {label}")
        return html
    print(f"[OK] {label}")
    return html.replace(old, new, 1)

# ============================================================
# 1. LUXURY DARK THEME — CSS Variables
# ============================================================
html = rp(
    ':root{\n  --bg:#f7f5f0;--sidebar:#ffffff;--card:#ffffff;--card2:#f5f3ee;\n  --border:#e8e2d4;--accent:#c8a84b;--accent2:#a8892e;\n  --text:#1a1a1a;--text2:#6b6b6b;--text3:#aaaaaa;',
    ''':root{
  --bg:#050912;--sidebar:#080d1a;--card:rgba(255,255,255,0.05);--card2:rgba(255,255,255,0.03);
  --border:rgba(200,168,75,0.18);--accent:#c8a84b;--accent2:#a8892e;
  --text:#e8e4d8;--text2:#8a96b4;--text3:#4a5680;
  --hot:#ef4444;--warm:#f59e0b;--green:#10b981;--blue:#3b82f6;--purple:#8b5cf6;''',
    'CSS :root vars'
)

# ============================================================
# 2. LUXURY EXTRA CSS — after :root block
# ============================================================
html = rp(
    'body{font-family:\'Inter\',sans-serif;background:var(--bg);color:var(--text);min-height:100vh}',
    '''body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;background-image:radial-gradient(ellipse at 20% 50%, rgba(200,168,75,0.04) 0%, transparent 60%),radial-gradient(ellipse at 80% 20%, rgba(59,130,246,0.04) 0%, transparent 60%)}
/* Luxury login overlay */
#loginOverlay{background:radial-gradient(ellipse at center, #0d1529 0%, #050912 100%)!important}
/* Glassmorphism card upgrade */
.card{background:rgba(255,255,255,0.04)!important;backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid rgba(200,168,75,0.14)!important;box-shadow:0 4px 24px rgba(0,0,0,0.4),0 0 0 1px rgba(200,168,75,0.06) inset!important}
.card:hover{border-color:rgba(200,168,75,0.28)!important;box-shadow:0 8px 32px rgba(0,0,0,0.5),0 0 20px rgba(200,168,75,0.06)!important}
/* Stats */
.stat-card{background:rgba(255,255,255,0.04)!important;border:1px solid rgba(200,168,75,0.14)!important;backdrop-filter:blur(12px)}
.stat-card.gold{background:linear-gradient(135deg,rgba(200,168,75,0.12),rgba(200,168,75,0.04))!important;border-color:rgba(200,168,75,0.3)!important}
.stat-card.green{background:linear-gradient(135deg,rgba(16,185,129,0.1),rgba(16,185,129,0.03))!important;border-color:rgba(16,185,129,0.25)!important}
.stat-card.red{background:linear-gradient(135deg,rgba(239,68,68,0.1),rgba(239,68,68,0.03))!important}
.stat-card.blue{background:linear-gradient(135deg,rgba(59,130,246,0.1),rgba(59,130,246,0.03))!important}
/* Input fields */
.fi,.fi-sm,select.fi{background:rgba(255,255,255,0.05)!important;border:1px solid rgba(200,168,75,0.2)!important;color:var(--text)!important}
.fi:focus,.fi-sm:focus{border-color:rgba(200,168,75,0.5)!important;box-shadow:0 0 0 3px rgba(200,168,75,0.1)!important;outline:none!important}
/* Topbar */
.topbar{background:rgba(8,13,26,0.9)!important;border-bottom:1px solid rgba(200,168,75,0.12)!important;backdrop-filter:blur(20px)!important}
/* Modal */
.modal{background:linear-gradient(135deg,#0d1529,#0a1120)!important;border:1px solid rgba(200,168,75,0.2)!important;box-shadow:0 24px 64px rgba(0,0,0,0.8),0 0 60px rgba(200,168,75,0.05)!important}
.modal-hdr{border-bottom:1px solid rgba(200,168,75,0.12)!important;background:linear-gradient(135deg,rgba(200,168,75,0.06),transparent)!important}
/* Buttons */
.btn-primary{background:linear-gradient(135deg,#d4aa45,#a8892e)!important;box-shadow:0 4px 15px rgba(200,168,75,0.3)!important}
.btn-primary:hover{background:linear-gradient(135deg,#e0b850,#c8a84b)!important;box-shadow:0 6px 20px rgba(200,168,75,0.45)!important;transform:translateY(-1px)}
.btn-secondary{background:rgba(255,255,255,0.06)!important;border:1px solid rgba(200,168,75,0.2)!important;color:var(--text)!important}
.btn-secondary:hover{background:rgba(255,255,255,0.1)!important;border-color:rgba(200,168,75,0.35)!important}
/* Lead/contact cards */
.lead-card,.cc,.kcard{background:rgba(255,255,255,0.04)!important;border:1px solid rgba(200,168,75,0.12)!important}
.lead-card:hover,.cc:hover,.kcard:hover{border-color:rgba(200,168,75,0.35)!important;background:rgba(200,168,75,0.06)!important;box-shadow:0 4px 20px rgba(0,0,0,0.4)!important}
/* Tabs */
.ftabs{background:rgba(255,255,255,0.03)!important;border:1px solid rgba(200,168,75,0.12)!important}
.ftab{color:var(--text2)!important}
.ftab.active{background:linear-gradient(135deg,rgba(200,168,75,0.15),rgba(200,168,75,0.08))!important;color:var(--accent)!important;box-shadow:0 2px 8px rgba(200,168,75,0.2)!important;border:1px solid rgba(200,168,75,0.25)!important}
.tab{color:var(--text2)!important}
.tab.active{color:var(--accent)!important;border-bottom:2px solid var(--accent)!important}
/* Table */
table{background:transparent!important}
thead th{background:rgba(200,168,75,0.08)!important;color:var(--text)!important;border-bottom:1px solid rgba(200,168,75,0.2)!important}
tbody tr:hover{background:rgba(200,168,75,0.05)!important}
/* Scrollbar */
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:rgba(255,255,255,0.02)}
::-webkit-scrollbar-thumb{background:rgba(200,168,75,0.3);border-radius:3px}
/* Sidebar upgraded */
#sidebar{background:linear-gradient(180deg,#080d1a 0%,#060b16 100%)!important;border-right:1px solid rgba(200,168,75,0.1)!important;box-shadow:4px 0 30px rgba(0,0,0,0.6)!important}
.logo-wrap{background:linear-gradient(135deg,rgba(200,168,75,0.1),rgba(200,168,75,0.03))!important;border-bottom:1px solid rgba(200,168,75,0.15)!important}
.nav-item.active{background:linear-gradient(135deg,rgba(200,168,75,0.15),rgba(200,168,75,0.05))!important;color:var(--accent)!important;box-shadow:inset 3px 0 0 var(--accent),0 2px 10px rgba(200,168,75,0.1)!important}
.nav-item:hover{background:rgba(200,168,75,0.07)!important;color:var(--text)!important}
/* Kanban columns */
.kcol{background:rgba(255,255,255,0.03)!important;border:1px solid rgba(200,168,75,0.1)!important}
.kcolh{color:var(--accent)!important;border-bottom:1px solid rgba(200,168,75,0.15)!important}
/* Login screen luxury */
#loginOverlay .login-box{background:linear-gradient(135deg,#0d1529,#080d1a)!important;border:1px solid rgba(200,168,75,0.25)!important;box-shadow:0 32px 80px rgba(0,0,0,0.9),0 0 80px rgba(200,168,75,0.08)!important}
/* Property media tabs */
.prop-tab{padding:8px 16px;border-radius:8px 8px 0 0;cursor:pointer;font-size:12px;font-weight:700;color:var(--text2);border:1px solid transparent;border-bottom:none;transition:all 0.2s;margin-right:2px}
.prop-tab.active{background:rgba(200,168,75,0.12);color:var(--accent);border-color:rgba(200,168,75,0.2)}
.prop-tab:hover{color:var(--text);background:rgba(255,255,255,0.04)}
.prop-tab-content{background:rgba(255,255,255,0.03);border:1px solid rgba(200,168,75,0.15);border-radius:0 10px 10px 10px;padding:16px}
/* Photo grid */
.photo-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(100px,1fr));gap:8px;margin-top:10px}
.photo-item{position:relative;border-radius:8px;overflow:hidden;aspect-ratio:1;border:1px solid rgba(200,168,75,0.2)}
.photo-item img{width:100%;height:100%;object-fit:cover;cursor:pointer;transition:transform 0.2s}
.photo-item:hover img{transform:scale(1.05)}
.photo-del{position:absolute;top:4px;right:4px;background:rgba(239,68,68,0.85);color:#fff;border:none;border-radius:50%;width:20px;height:20px;cursor:pointer;font-size:11px;display:none;align-items:center;justify-content:center}
.photo-item:hover .photo-del{display:flex}
/* Doc list */
.doc-item{display:flex;align-items:center;gap:10px;padding:10px 12px;background:rgba(255,255,255,0.04);border:1px solid rgba(200,168,75,0.12);border-radius:8px;margin-bottom:6px;transition:all 0.2s}
.doc-item:hover{border-color:rgba(200,168,75,0.3);background:rgba(200,168,75,0.05)}
/* Note item */
.note-item{padding:12px;background:rgba(255,255,255,0.04);border:1px solid rgba(200,168,75,0.12);border-radius:8px;margin-bottom:8px}
.note-author{font-size:11px;color:var(--accent);font-weight:700}
.note-time{font-size:10px;color:var(--text3);margin-left:8px}
.note-text{font-size:13px;color:var(--text2);margin-top:5px;line-height:1.5}
/* Investor cards */
.inv-card{background:rgba(255,255,255,0.04);border:1px solid rgba(200,168,75,0.15);border-radius:12px;padding:16px;transition:all 0.2s;cursor:default}
.inv-card:hover{border-color:rgba(200,168,75,0.4);box-shadow:0 4px 20px rgba(200,168,75,0.1);transform:translateY(-2px)}
/* Upload zone */
.upload-zone{border:2px dashed rgba(200,168,75,0.3);border-radius:10px;padding:20px;text-align:center;cursor:pointer;transition:all 0.2s;margin-bottom:12px}
.upload-zone:hover{border-color:rgba(200,168,75,0.6);background:rgba(200,168,75,0.04)}
/* Activity log */
.act-item{display:flex;align-items:flex-start;gap:10px;padding:12px;border-bottom:1px solid rgba(200,168,75,0.08);transition:background 0.2s}
.act-item:hover{background:rgba(255,255,255,0.03)}
.act-icon{width:32px;height:32px;background:rgba(200,168,75,0.1);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0}
.act-text{font-size:12.5px;color:var(--text2)}
.act-time{font-size:10.5px;color:var(--text3);margin-top:2px}
/* Divider */
.divider{background:rgba(200,168,75,0.1)!important}
/* Global search */
#globalSearchResults{background:linear-gradient(135deg,#0d1529,#080d1a)!important;border:1px solid rgba(200,168,75,0.25)!important;box-shadow:0 16px 40px rgba(0,0,0,0.7)!important}
/* Float tools */
.ftool-panel{background:linear-gradient(135deg,#0d1529,#080d1a)!important;border:1px solid rgba(200,168,75,0.2)!important;box-shadow:0 16px 50px rgba(0,0,0,0.8)!important}
''',
    'luxury extra CSS'
)

# ============================================================
# 3. NAV — Add Investors + Admin items before Settings
# ============================================================
html = rp(
    '    <div class="nav-item" onclick="go(\'settings\',this)" data-p="settings"><span class="nav-icon">⚙️</span>Settings</div>',
    '''    <div class="nav-item" onclick="go('investors',this)" data-p="investors" id="navInvestors"><span class="nav-icon">💼</span>Investors</div>
    <div class="nav-item" onclick="go('admin',this)" data-p="admin" id="navAdmin" style="display:none"><span class="nav-icon" style="color:#c8a84b">👑</span><span style="background:linear-gradient(135deg,#d4aa45,#a8892e);-webkit-background-clip:text;-webkit-text-fill-color:transparent">Admin Hub</span></div>
    <div class="nav-item" onclick="go('settings',this)" data-p="settings"><span class="nav-icon">⚙️</span>Settings</div>''',
    'nav investors + admin'
)

# ============================================================
# 4. HTML PAGES — Investors + Admin before end #main
# ============================================================
INVESTORS_PAGE = '''
<!-- INVESTORS PAGE -->
<div id="page-investors" class="page">
  <div class="topbar">
    <div class="page-title">💼 Investors</div>
    <button class="btn btn-primary" onclick="om('mAddInvestor')">+ Add Investor</button>
  </div>
  <div class="stats-grid" id="invStats"></div>
  <div id="invList"></div>
</div>

<!-- ADMIN HUB PAGE -->
<div id="page-admin" class="page">
  <div class="topbar">
    <div class="page-title">👑 Admin Hub</div>
    <button class="btn btn-secondary" onclick="loadAdminActivity()">🔄 Refresh</button>
  </div>
  <div class="grid-2 mb-16">
    <div class="card">
      <div style="font-size:11px;color:var(--text3);font-weight:700;text-transform:uppercase;letter-spacing:.7px;margin-bottom:12px">Team Members</div>
      <div id="adminTeamList"></div>
    </div>
    <div class="card">
      <div style="font-size:11px;color:var(--text3);font-weight:700;text-transform:uppercase;letter-spacing:.7px;margin-bottom:12px">Quick Stats</div>
      <div id="adminQuickStats"></div>
    </div>
  </div>
  <div class="card">
    <div style="font-size:11px;color:var(--text3);font-weight:700;text-transform:uppercase;letter-spacing:.7px;margin-bottom:12px">Live Activity Feed</div>
    <div id="adminActivityFeed"></div>
  </div>
</div>

<!-- ADD INVESTOR MODAL -->
<div class="overlay" id="mAddInvestor"><div class="modal modal-lg">
  <div class="modal-hdr"><div class="modal-title" id="invMT">Add Investor</div><button class="modal-x" onclick="cm('mAddInvestor')">✕</button></div>
  <div class="mform" id="invFC"></div>
</div></div>
'''

html = rp(
    '</div><!-- end #main -->',
    INVESTORS_PAGE + '\n</div><!-- end #main -->',
    'investors+admin pages'
)

# ============================================================
# 5. go() map — add investors + admin
# ============================================================
html = rp(
    'const map={dashboard:renderDash,leads:renderLeads,pipeline:renderKanban,ads:renderAds,analytics:renderAnalytics,buyers:renderBuyers,realtors:renderRealtors,contacts:renderContacts,followups:renderFU,templates:renderTemplates,settings:renderSettings,mls:renderMLS};',
    'const map={dashboard:renderDash,leads:renderLeads,pipeline:renderKanban,ads:renderAds,analytics:renderAnalytics,buyers:renderBuyers,realtors:renderRealtors,contacts:renderContacts,followups:renderFU,templates:renderTemplates,settings:renderSettings,mls:renderMLS,investors:renderInvestors,admin:renderAdmin};',
    'go() map'
)

# ============================================================
# 6. loadAll — add investors to Promise.all
# ============================================================
html = rp(
    '''    const [settings, leads, props, buyers, realtors, contacts, fus, ads, acts] = await Promise.all([
      supabase.from('settings').select('*').eq('id',1).single(),
      leadsQ,
      propsQ,
      supabase.from('buyers').select('*').order('created_at',{ascending:false}),
      supabase.from('realtors').select('*').order('referrals',{ascending:false}),
      supabase.from('contacts').select('*').order('created_at',{ascending:false}),
      supabase.from('followups').select('*').order('date',{ascending:true}),
      supabase.from('ad_campaigns').select('*').order('created_at',{ascending:false}),
      supabase.from('activities').select('*').order('created_at',{ascending:false}).limit(20)
    ]);
    db.settings = settings.data || {};
    db.leads = (leads.data||[]).map(mapLead);
    db.properties = (props.data||[]).map(mapProp);
    // Tag which leads are already in pipeline
    const pipelineLeadIds = new Set(db.properties.map(p=>p.leadId).filter(Boolean));
    db.leads.forEach(l => { l.inPipeline = pipelineLeadIds.has(l.id); });
    db.buyers = buyers.data||[];
    db.realtors = realtors.data||[];
    db.contacts = contacts.data||[];
    db.followups = (fus.data||[]).map(mapFU);
    db.adCampaigns = (ads.data||[]).map(mapAd);
    db.activities = (acts.data||[]).map(a=>({icon:a.icon,text:a.text,time:a.time}));''',
    '''    const [settings, leads, props, buyers, realtors, contacts, fus, ads, acts, investors] = await Promise.all([
      supabase.from('settings').select('*').eq('id',1).single(),
      leadsQ,
      propsQ,
      supabase.from('buyers').select('*').order('created_at',{ascending:false}),
      supabase.from('realtors').select('*').order('referrals',{ascending:false}),
      supabase.from('contacts').select('*').order('created_at',{ascending:false}),
      supabase.from('followups').select('*').order('date',{ascending:true}),
      supabase.from('ad_campaigns').select('*').order('created_at',{ascending:false}),
      supabase.from('activities').select('*').order('created_at',{ascending:false}).limit(50),
      supabase.from('investors').select('*').order('created_at',{ascending:false})
    ]);
    db.settings = settings.data || {};
    db.leads = (leads.data||[]).map(mapLead);
    db.properties = (props.data||[]).map(mapProp);
    // Tag which leads are already in pipeline
    const pipelineLeadIds = new Set(db.properties.map(p=>p.leadId).filter(Boolean));
    db.leads.forEach(l => { l.inPipeline = pipelineLeadIds.has(l.id); });
    db.buyers = buyers.data||[];
    db.realtors = realtors.data||[];
    db.contacts = contacts.data||[];
    db.followups = (fus.data||[]).map(mapFU);
    db.adCampaigns = (ads.data||[]).map(mapAd);
    db.activities = (acts.data||[]).map(a=>({icon:a.icon,text:a.text,time:a.time,user:a.user_name||''}));
    db.investors = investors.data||[];''',
    'loadAll Promise.all + investors'
)

# ============================================================
# 7. Show admin nav for admin users
# ============================================================
html = rp(
    "  if(roleEl) roleEl.textContent = currentUser.role === 'admin' ? 'Owner & Admin' : 'Team Member';",
    """  if(roleEl) roleEl.textContent = currentUser.role === 'admin' ? 'Owner & Admin' : 'Team Member';
  // Show admin nav only for admins
  const navAdmin = document.getElementById('navAdmin');
  if(navAdmin) navAdmin.style.display = isAdmin() ? 'flex' : 'none';""",
    'show admin nav'
)

# ============================================================
# 8. db initialization — add investors array
# ============================================================
html = rp(
    "db.activities = (acts.data||[]).map(a=>({icon:a.icon,text:a.text,time:a.time,user:a.user_name||''}));",
    """db.activities = (acts.data||[]).map(a=>({icon:a.icon,text:a.text,time:a.time,user:a.user_name||''}));
    db.investors = investors.data||[];""",
    'db.investors init'
)

# ============================================================
# 9. Replace openPropD — add tabs for photos/docs/notes/investor
# ============================================================
OLD_OPEN_PROP = '''function openPropD(id){
  const p=db.properties.find(x=>x.id===id);if(!p)return;
  const pr=Math.round(p.arv*.7-p.repairs-p.offerPrice);
  const buyer=db.buyers.find(b=>b.id===p.buyerId);
  const agentId=JSON.parse(localStorage.getItem('prop_agent_'+p.id)||'""');
  const agent=agentId?db.realtors.find(r=>r.id===agentId):null;
  const fin=JSON.parse(localStorage.getItem('prop_fin_'+p.id)||'{}');
  const hasFinancials=fin.revenue||fin.wholesaleFee||fin.feeEarned||fin.referralFee||fin.concessions;
  document.getElementById('propDC').innerHTML=`
    <div style="margin-bottom:16px"><div style="font-size:17px;font-weight:800">${p.address} <button class="btn btn-secondary btn-sm" style="font-size:10px" onclick="event.stopPropagation();openMLSFor('${p.address}')">🔍 Pull Data</button></div><div style="font-size:12px;color:var(--text2)">Seller: ${p.seller}${agent?' · 🤝 Agent: '+agent.name:''}</div></div>
    <div class="grid-3 mb-16">
      <div class="stat-card green"><div class="stat-label">Est. Profit</div><div class="stat-value" style="font-size:19px">$${pr.toLocaleString()}</div></div>
      <div class="stat-card gold"><div class="stat-label">Offer</div><div class="stat-value" style="font-size:19px">$${p.offerPrice.toLocaleString()}</div></div>
      <div class="stat-card blue"><div class="stat-label">ARV</div><div class="stat-value" style="font-size:19px">$${p.arv.toLocaleString()}</div></div>
    </div>
    ${hasFinancials?`<div class="card card-sm mb-16">
      <div style="font-size:10px;color:var(--text3);font-weight:700;text-transform:uppercase;margin-bottom:9px">💵 Financial Details</div>
      <div style="display:flex;flex-wrap:wrap;gap:14px;font-size:12.5px">
        <div>Revenue: <strong style="color:var(--green)">$${(fin.revenue||0).toLocaleString()}</strong></div>
        <div>Wholesale Fee: <strong style="color:var(--accent)">$${(fin.wholesaleFee||0).toLocaleString()}</strong></div>
        <div>Fee Earned: <strong style="color:var(--green)">$${(fin.feeEarned||0).toLocaleString()}</strong></div>
        <div>Referral: <strong style="color:var(--purple)">$${(fin.referralFee||0).toLocaleString()}</strong></div>
        <div>Concessions: <strong style="color:var(--hot)">$${(fin.concessions||0).toLocaleString()}</strong></div>
      </div>
    </div>`:''}
    <div class="grid-2">
      <div class="card card-sm">
        <div style="font-size:10px;color:var(--text3);font-weight:700;text-transform:uppercase;margin-bottom:9px">Details</div>
        <div style="font-size:12.5px">🔨 Repairs: $${p.repairs.toLocaleString()}</div>
        <div style="font-size:12.5px;margin-top:4px">📋 Stage: ${SLBLS[p.stage]}</div>
        <div style="font-size:12.5px;margin-top:4px">💰 Buyer: ${buyer?.name||'None'}</div>
        ${agent?`<div style="font-size:12.5px;margin-top:4px">🤝 Agent: ${agent.name}</div>`:''}
        <div style="font-size:12.5px;margin-top:4px">📅 Days: ${p.daysInStage}</div>
        <div style="margin-top:12px;display:flex;gap:7px;flex-wrap:wrap">
          <button class="btn btn-secondary btn-sm" onclick="editProp('${p.id}')">✏️ Edit</button>
          <button class="btn btn-danger btn-sm" onclick="confDel('property','${p.id}')">🗑️</button>
        </div>
        <div style="margin-top:9px"><select class="fi" onchange="moveStage('${p.id}',this.value)" style="font-size:11.5px;padding:7px 10px">${STAGES.map(s=>`<option value="${s}" ${p.stage===s?'selected':''}>${SLBLS[s]}</option>`).join('')}</select></div>
      </div>
      <div class="card card-sm">
        <div style="font-size:10px;color:var(--text3);font-weight:700;text-transform:uppercase;margin-bottom:9px">Closing Checklist</div>
        ${(p.checklist||[]).map((it,i)=>`<div style="display:flex;align-items:center;gap:8px;margin-bottom:7px"><input type="checkbox" ${it.done?'checked':''} onchange="togCL('${p.id}',${i},this.checked)" style="cursor:pointer;accent-color:var(--accent)"><span style="font-size:12.5px;${it.done?'text-decoration:line-through;color:var(--text3)':''}">${it.item}</span></div>`).join('')}
      </div>
    </div>
    ${p.notes?`<div class="card card-sm" style="margin-top:14px"><div style="font-size:10px;color:var(--text3);font-weight:700;text-transform:uppercase;margin-bottom:7px">Notes</div><div style="font-size:12.5px;color:var(--text2)">${p.notes}</div></div>`:''}
    ${renderMatchedBuyers(p)}
    <div class="card card-sm" style="margin-top:14px">
      <div style="font-size:10px;color:var(--text3);font-weight:700;text-transform:uppercase;margin-bottom:9px">📷 Property Photos</div>
      <label style="display:inline-flex;align-items:center;gap:6px;cursor:pointer;padding:8px 14px;background:var(--card2);border:1px solid var(--border);border-radius:8px;font-size:12px;font-weight:600">
        📷 Add Photo
        <input type="file" accept="image/*" multiple style="display:none" onchange="uploadPropImages('${p.id}',this)">
      </label>
      <div id="propImages_${p.id}" style="display:flex;flex-wrap:wrap;gap:8px;margin-top:10px"></div>
    </div>
  `;
  renderPropImages(p.id);
  om('mPropDetail');
}'''

NEW_OPEN_PROP = '''function openPropD(id){
  const p=db.properties.find(x=>x.id===id);if(!p)return;
  const pr=Math.round(p.arv*.7-p.repairs-p.offerPrice);
  const buyer=db.buyers.find(b=>b.id===p.buyerId);
  const investor=db.investors?db.investors.find(inv=>inv.id===p.investor_id):null;
  const agentId=JSON.parse(localStorage.getItem('prop_agent_'+p.id)||'""');
  const agent=agentId?db.realtors.find(r=>r.id===agentId):null;
  const fin=JSON.parse(localStorage.getItem('prop_fin_'+p.id)||'{}');
  const hasFinancials=fin.revenue||fin.wholesaleFee||fin.feeEarned||fin.referralFee||fin.concessions;
  document.getElementById('propDC').innerHTML=`
    <div style="padding:16px 20px 0">
      <div style="margin-bottom:12px">
        <div style="font-size:17px;font-weight:800">${p.address} <button class="btn btn-secondary btn-sm" style="font-size:10px" onclick="event.stopPropagation();openMLSFor('${p.address}')">🔍 Pull Data</button></div>
        <div style="font-size:12px;color:var(--text2);margin-top:3px">Seller: ${p.seller}${agent?' · 🤝 '+agent.name:''}${investor?' · 💼 '+investor.name:''}</div>
      </div>
      <div class="grid-3 mb-12">
        <div class="stat-card green"><div class="stat-label">Est. Profit</div><div class="stat-value" style="font-size:19px">$${pr.toLocaleString()}</div></div>
        <div class="stat-card gold"><div class="stat-label">Offer</div><div class="stat-value" style="font-size:19px">$${p.offerPrice.toLocaleString()}</div></div>
        <div class="stat-card blue"><div class="stat-label">ARV</div><div class="stat-value" style="font-size:19px">$${p.arv.toLocaleString()}</div></div>
      </div>
      ${hasFinancials?`<div class="card card-sm mb-12">
        <div style="font-size:10px;color:var(--text3);font-weight:700;text-transform:uppercase;margin-bottom:9px">💵 Financial Details</div>
        <div style="display:flex;flex-wrap:wrap;gap:14px;font-size:12.5px">
          <div>Revenue: <strong style="color:var(--green)">$${(fin.revenue||0).toLocaleString()}</strong></div>
          <div>Wholesale Fee: <strong style="color:var(--accent)">$${(fin.wholesaleFee||0).toLocaleString()}</strong></div>
          <div>Fee Earned: <strong style="color:var(--green)">$${(fin.feeEarned||0).toLocaleString()}</strong></div>
          <div>Referral: <strong style="color:var(--purple)">$${(fin.referralFee||0).toLocaleString()}</strong></div>
          <div>Concessions: <strong style="color:var(--hot)">$${(fin.concessions||0).toLocaleString()}</strong></div>
        </div>
      </div>`:''}
      <div class="grid-2 mb-12">
        <div class="card card-sm">
          <div style="font-size:10px;color:var(--text3);font-weight:700;text-transform:uppercase;margin-bottom:9px">Details</div>
          <div style="font-size:12.5px">🔨 Repairs: $${p.repairs.toLocaleString()}</div>
          <div style="font-size:12.5px;margin-top:4px">📋 Stage: ${SLBLS[p.stage]}</div>
          <div style="font-size:12.5px;margin-top:4px">💰 Buyer: ${buyer?.name||'None'}</div>
          <div style="font-size:12.5px;margin-top:4px">💼 Investor: ${investor?.name||'<span style="color:var(--text3)">Not assigned</span>'}</div>
          ${agent?`<div style="font-size:12.5px;margin-top:4px">🤝 Agent: ${agent.name}</div>`:''}
          <div style="font-size:12.5px;margin-top:4px">📅 Days: ${p.daysInStage}</div>
          <div style="margin-top:12px;display:flex;gap:7px;flex-wrap:wrap">
            <button class="btn btn-secondary btn-sm" onclick="editProp('${p.id}')">✏️ Edit</button>
            <button class="btn btn-danger btn-sm" onclick="confDel('property','${p.id}')">🗑️</button>
          </div>
          <div style="margin-top:9px"><select class="fi" onchange="moveStage('${p.id}',this.value)" style="font-size:11.5px;padding:7px 10px">${STAGES.map(s=>`<option value="${s}" ${p.stage===s?'selected':''}>${SLBLS[s]}</option>`).join('')}</select></div>
        </div>
        <div class="card card-sm">
          <div style="font-size:10px;color:var(--text3);font-weight:700;text-transform:uppercase;margin-bottom:9px">Closing Checklist</div>
          ${(p.checklist||[]).map((it,i)=>`<div style="display:flex;align-items:center;gap:8px;margin-bottom:7px"><input type="checkbox" ${it.done?'checked':''} onchange="togCL('${p.id}',${i},this.checked)" style="cursor:pointer;accent-color:var(--accent)"><span style="font-size:12.5px;${it.done?'text-decoration:line-through;color:var(--text3)':''}">${it.item}</span></div>`).join('')}
        </div>
      </div>
      ${renderMatchedBuyers(p)}
    </div>
    <!-- MEDIA TABS -->
    <div style="padding:0 20px 16px">
      <div style="display:flex;margin-bottom:-1px;margin-top:16px">
        <div class="prop-tab active" onclick="switchPropTab('${p.id}','photos',this)">📷 Photos</div>
        <div class="prop-tab" onclick="switchPropTab('${p.id}','docs',this)">📄 Documents</div>
        <div class="prop-tab" onclick="switchPropTab('${p.id}','notes',this)">📝 Notes</div>
        <div class="prop-tab" onclick="switchPropTab('${p.id}','investor',this)">💼 Investor</div>
      </div>
      <div class="prop-tab-content" id="propTabContent_${p.id}">
        <div id="propTab_photos_${p.id}">
          <label class="upload-zone">
            <span style="font-size:24px;display:block;margin-bottom:6px">📷</span>
            <span style="font-size:12.5px;color:var(--text2)">Click to upload photos</span>
            <input type="file" accept="image/*" multiple style="display:none" onchange="uploadPropPhotos('${p.id}',this)">
          </label>
          <div class="photo-grid" id="propPhotos_${p.id}"></div>
        </div>
        <div id="propTab_docs_${p.id}" style="display:none">
          <div style="display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap">
            <select class="fi" id="docType_${p.id}" style="width:160px;padding:7px 10px;font-size:12px">
              <option value="contract">📑 Contract</option>
              <option value="inspection">🔍 Inspection</option>
              <option value="title">📜 Title</option>
              <option value="photo">📷 Media</option>
              <option value="other">📎 Other</option>
            </select>
            <label class="btn btn-secondary" style="cursor:pointer;display:inline-flex;align-items:center;gap:5px">
              📎 Upload Document
              <input type="file" style="display:none" onchange="uploadPropDoc('${p.id}',this)">
            </label>
          </div>
          <div id="propDocs_${p.id}"></div>
        </div>
        <div id="propTab_notes_${p.id}" style="display:none">
          <div style="display:flex;gap:8px;margin-bottom:12px">
            <textarea class="fi" id="noteInput_${p.id}" placeholder="Add a note..." style="flex:1;min-height:70px;resize:vertical"></textarea>
          </div>
          <button class="btn btn-primary btn-sm" onclick="addPropNote('${p.id}')">+ Add Note</button>
          <div id="propNotes_${p.id}" style="margin-top:12px"></div>
        </div>
        <div id="propTab_investor_${p.id}" style="display:none">
          <div style="margin-bottom:12px">
            <label style="font-size:11px;color:var(--text3);font-weight:700;text-transform:uppercase;display:block;margin-bottom:6px">Assign Investor</label>
            <select class="fi" id="propInvestorSel_${p.id}" style="width:100%;max-width:340px" onchange="assignPropInvestor('${p.id}',this.value)">
              <option value="">— No investor assigned —</option>
              ${(db.investors||[]).map(inv=>`<option value="${inv.id}" ${p.investor_id===inv.id?'selected':''}>${inv.name}${inv.company?' ('+inv.company+')':''}</option>`).join('')}
            </select>
          </div>
          ${investor?`<div class="inv-card" style="max-width:400px">
            <div style="font-size:15px;font-weight:800;color:var(--accent)">${investor.name}</div>
            ${investor.company?`<div style="font-size:12px;color:var(--text2);margin-top:2px">${investor.company}</div>`:''}
            <div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:10px;font-size:12px;color:var(--text2)">
              ${investor.phone?`<div>📞 ${investor.phone}</div>`:''}
              ${investor.email?`<div>✉️ ${investor.email}</div>`:''}
              ${investor.budget?`<div>💰 ${investor.budget}</div>`:''}
              ${investor.focus?`<div>🎯 ${investor.focus}</div>`:''}
            </div>
          </div>`:'<div style="color:var(--text3);font-size:13px;padding:16px 0">No investor assigned to this property yet.</div>'}
        </div>
      </div>
    </div>
  `;
  // Load photos + docs + notes async
  loadPropPhotos(p.id);
  loadPropDocs(p.id);
  loadPropNotes(p.id);
  om('mPropDetail');
}

function switchPropTab(propId,tab,el){
  const tabs=['photos','docs','notes','investor'];
  tabs.forEach(t=>{
    const c=document.getElementById('propTab_'+t+'_'+propId);
    if(c) c.style.display=t===tab?'block':'none';
  });
  const parent=el.parentElement;
  parent.querySelectorAll('.prop-tab').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');
}

// ---- Photos ----
async function uploadPropPhotos(propId,input){
  if(!input.files.length)return;
  const user=currentUser?.name||'Unknown';
  let uploaded=0;
  for(const file of input.files){
    try{
      toast('Uploading '+file.name+'...');
      const url=await uploadFile('property-media',file,propId);
      await supabase.from('property_photos').insert({property_id:propId,url,filename:file.name,uploaded_by:user});
      addAct('📷',user+' uploaded photo to '+propId.substring(0,8)+'…');
      uploaded++;
    }catch(e){toast('Upload failed: '+e.message,true);}
  }
  if(uploaded)loadPropPhotos(propId);
}
async function loadPropPhotos(propId){
  const {data}=await supabase.from('property_photos').select('*').eq('property_id',propId).order('uploaded_at',{ascending:false});
  const el=document.getElementById('propPhotos_'+propId);
  if(!el)return;
  el.innerHTML=(data||[]).map(ph=>`
    <div class="photo-item">
      <img src="${ph.url}" onclick="window.open('${ph.url}')" title="${ph.filename}">
      <button class="photo-del" onclick="deletePropPhoto(${ph.id},'${propId}')">✕</button>
    </div>`).join('');
}
async function deletePropPhoto(photoId,propId){
  await supabase.from('property_photos').delete().eq('id',photoId);
  loadPropPhotos(propId);
  toast('Photo removed');
}

// ---- Documents ----
async function uploadPropDoc(propId,input){
  const file=input.files[0];if(!file)return;
  const user=currentUser?.name||'Unknown';
  const docType=document.getElementById('docType_'+propId)?.value||'other';
  try{
    toast('Uploading '+file.name+'...');
    const url=await uploadFile('property-docs',file,propId);
    await supabase.from('property_documents').insert({property_id:propId,url,filename:file.name,doc_type:docType,uploaded_by:user});
    addAct('📄',user+' uploaded doc to '+propId.substring(0,8)+'…');
    loadPropDocs(propId);
    toast('Document uploaded!');
  }catch(e){toast('Upload failed: '+e.message,true);}
}
async function loadPropDocs(propId){
  const {data}=await supabase.from('property_documents').select('*').eq('property_id',propId).order('uploaded_at',{ascending:false});
  const el=document.getElementById('propDocs_'+propId);
  if(!el)return;
  const TYPE_ICONS={contract:'📑',inspection:'🔍',title:'📜',photo:'📷',other:'📎'};
  el.innerHTML=(data||[]).length===0?'<div style="color:var(--text3);font-size:13px;padding:8px 0">No documents yet</div>':
    (data||[]).map(d=>`
      <div class="doc-item">
        <span style="font-size:18px">${TYPE_ICONS[d.doc_type]||'📎'}</span>
        <div style="flex:1;min-width:0">
          <div style="font-size:12.5px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${d.filename}</div>
          <div style="font-size:11px;color:var(--text3)">${d.uploaded_by} · ${new Date(d.uploaded_at).toLocaleDateString()}</div>
        </div>
        <a href="${d.url}" target="_blank" class="btn btn-secondary btn-sm">↗</a>
        <button class="btn btn-danger btn-sm" onclick="deletePropDoc(${d.id},'${propId}')">🗑️</button>
      </div>`).join('');
}
async function deletePropDoc(docId,propId){
  await supabase.from('property_documents').delete().eq('id',docId);
  loadPropDocs(propId);
  toast('Document removed');
}

// ---- Notes ----
async function addPropNote(propId){
  const inp=document.getElementById('noteInput_'+propId);
  const note=(inp?.value||'').trim();
  if(!note)return toast('Enter a note first',true);
  const user=currentUser?.name||'Unknown';
  const userId=currentUser?.id||'';
  await supabase.from('property_notes').insert({property_id:propId,author_id:userId,author_name:user,note});
  addAct('📝',user+' added note to '+propId.substring(0,8)+'…');
  inp.value='';
  loadPropNotes(propId);
  toast('Note saved!');
}
async function loadPropNotes(propId){
  const {data}=await supabase.from('property_notes').select('*').eq('property_id',propId).order('created_at',{ascending:false});
  const el=document.getElementById('propNotes_'+propId);
  if(!el)return;
  el.innerHTML=(data||[]).length===0?'<div style="color:var(--text3);font-size:13px;padding:8px 0">No notes yet</div>':
    (data||[]).map(n=>`
      <div class="note-item">
        <div><span class="note-author">${n.author_name||'Unknown'}</span><span class="note-time">${new Date(n.created_at).toLocaleString()}</span></div>
        <div class="note-text">${n.note}</div>
      </div>`).join('');
}

// ---- Investor assignment ----
async function assignPropInvestor(propId,investorId){
  const investor=db.investors?db.investors.find(i=>i.id===investorId):null;
  const investorName=investor?.name||'';
  const {error}=await supabase.from('properties').update({investor_id:investorId,investor_name:investorName}).eq('id',propId);
  if(error){toast('Error: '+error.message,true);return;}
  const p=db.properties.find(x=>x.id===propId);
  if(p){p.investor_id=investorId;p.investor_name=investorName;}
  toast(investorId?'Investor assigned!':'Investor removed');
  addAct('💼',(currentUser?.name||'Someone')+' assigned investor to '+propId.substring(0,8)+'…');
}

// ---- File upload to Supabase Storage ----
async function uploadFile(bucket,file,folder=''){
  const safe=file.name.replace(/[^a-zA-Z0-9._-]/g,'_');
  const filename=(folder?folder+'/':'')+Date.now()+'_'+safe;
  const res=await fetch(SURL+'/storage/v1/object/'+bucket+'/'+filename,{
    method:'POST',
    headers:{'Authorization':'Bearer '+SKEY,'Content-Type':file.type||'application/octet-stream'},
    body:file
  });
  if(!res.ok){const t=await res.text();throw new Error(t);}
  return SURL+'/storage/v1/object/public/'+bucket+'/'+filename;
}'''

html = rp(OLD_OPEN_PROP, NEW_OPEN_PROP, 'openPropD replacement')

# ============================================================
# 10. Replace old localStorage-based photo functions
# ============================================================
html = rp(
    '''function uploadPropImages(propId,input){
  const existing=JSON.parse(localStorage.getItem('prop_imgs_'+propId)||'[]');
  Array.from(input.files).forEach(file=>{
    const reader=new FileReader();
    reader.onload=(e)=>{
      existing.push(e.target.result);
      localStorage.setItem('prop_imgs_'+propId,JSON.stringify(existing));
      renderPropImages(propId);
    };
    reader.readAsDataURL(file);
  });
}
function renderPropImages(propId){
  const imgs=JSON.parse(localStorage.getItem('prop_imgs_'+propId)||'[]');
  const el=document.getElementById('propImages_'+propId);
  if(el) el.innerHTML=imgs.map((src,i)=>
    `<div style="position:relative"><img src="${src}" style="width:80px;height:80px;object-fit:cover;border-radius:8px;border:1px solid var(--border);cursor:pointer" onclick="window.open(this.src)"><button onclick="deletePropImg('${propId}',${i})" style="position:absolute;top:-5px;right:-5px;background:var(--hot);color:#fff;border:none;border-radius:50%;width:18px;height:18px;cursor:pointer;font-size:10px;line-height:1">✕</button></div>`
  ).join('');
}
function deletePropImg(propId,idx){
  const imgs=JSON.parse(localStorage.getItem('prop_imgs_'+propId)||'[]');
  imgs.splice(idx,1);
  localStorage.setItem('prop_imgs_'+propId,JSON.stringify(imgs));
  renderPropImages(propId);
}''',
    '// Legacy photo functions replaced by Supabase-based uploadPropPhotos/loadPropPhotos',
    'remove old photo functions'
)

# ============================================================
# 11. INVESTORS JS — render + CRUD
# ============================================================
INVESTORS_JS = '''
// ============================================================
// INVESTORS
// ============================================================
function renderInvestors(){
  const investors=db.investors||[];
  const totalActive=investors.reduce((s,i)=>s+(i.active_deals||0),0);
  const totalDone=investors.reduce((s,i)=>s+(i.deals_done||0),0);
  document.getElementById('invStats').innerHTML=`
    <div class="stat-card gold"><div class="stat-icon">💼</div><div class="stat-label">Total Investors</div><div class="stat-value">${investors.length}</div></div>
    <div class="stat-card blue"><div class="stat-icon">🔄</div><div class="stat-label">Active Deals</div><div class="stat-value">${totalActive}</div></div>
    <div class="stat-card green"><div class="stat-icon">✅</div><div class="stat-label">Deals Closed</div><div class="stat-value">${totalDone}</div></div>
  `;
  if(!investors.length){
    document.getElementById('invList').innerHTML=`<div class="card" style="text-align:center;padding:40px"><div style="font-size:40px;margin-bottom:12px">💼</div><div style="font-size:16px;font-weight:700;margin-bottom:6px">No investors yet</div><div style="color:var(--text2);margin-bottom:20px;font-size:13px">Add your first investor to start tracking deals</div><button class="btn btn-primary" onclick="om('mAddInvestor')">+ Add Investor</button></div>`;
    return;
  }
  const FOCUS_COLORS={flip:'var(--accent)',hold:'var(--blue)',both:'var(--green)'};
  document.getElementById('invList').innerHTML=`
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px">
      ${investors.map(inv=>{
        const propCount=db.properties?db.properties.filter(p=>p.investor_id===inv.id).length:0;
        return `<div class="inv-card">
          <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:10px">
            <div>
              <div style="font-size:15px;font-weight:800;color:var(--accent)">${inv.name}</div>
              ${inv.company?`<div style="font-size:11.5px;color:var(--text2)">${inv.company}</div>`:''}
            </div>
            ${inv.focus?`<span style="font-size:10px;padding:2px 8px;border-radius:10px;background:rgba(200,168,75,0.12);color:var(--accent);font-weight:700;border:1px solid rgba(200,168,75,0.2);white-space:nowrap">${inv.focus}</span>`:''}
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:8px;font-size:12px;color:var(--text2);margin-bottom:10px">
            ${inv.phone?`<div>📞 ${inv.phone}</div>`:''}
            ${inv.email?`<div>✉️ ${inv.email}</div>`:''}
            ${inv.budget?`<div>💰 ${inv.budget}</div>`:''}
          </div>
          ${inv.zips?`<div style="font-size:11px;color:var(--text3);margin-bottom:8px">📍 ${inv.zips}</div>`:''}
          <div style="display:flex;gap:12px;font-size:11.5px;margin-bottom:12px">
            <div style="padding:5px 10px;background:rgba(16,185,129,0.1);border-radius:6px;color:var(--green)">${propCount} active deal${propCount!==1?'s':''}</div>
            ${inv.deals_done?`<div style="padding:5px 10px;background:rgba(200,168,75,0.08);border-radius:6px;color:var(--accent)">${inv.deals_done} closed</div>`:''}
          </div>
          <div style="display:flex;gap:7px">
            <button class="btn btn-secondary btn-sm" onclick="editInvestor('${inv.id}')">✏️ Edit</button>
            <button class="btn btn-danger btn-sm" onclick="deleteInvestor('${inv.id}')">🗑️</button>
          </div>
        </div>`;
      }).join('')}
    </div>
  `;
}

function invForm(inv){
  return `
    <div class="fg"><label>Name *</label><input class="fi" id="iName" value="${inv?.name||''}" placeholder="John Smith"></div>
    <div class="fg"><label>Company</label><input class="fi" id="iCo" value="${inv?.company||''}" placeholder="ABC Capital LLC"></div>
    <div class="grid-2">
      <div class="fg"><label>Phone</label><input class="fi" id="iPh" value="${inv?.phone||''}" placeholder="(720) 555-0000"></div>
      <div class="fg"><label>Email</label><input class="fi" id="iEm" value="${inv?.email||''}" placeholder="investor@email.com"></div>
    </div>
    <div class="grid-2">
      <div class="fg"><label>Budget Range</label><input class="fi" id="iBudget" value="${inv?.budget||''}" placeholder="$50k-$200k per deal"></div>
      <div class="fg"><label>Focus</label>
        <select class="fi" id="iFocus">
          <option value="">Select...</option>
          <option value="fix-flip" ${inv?.focus==='fix-flip'?'selected':''}>🔨 Fix & Flip</option>
          <option value="buy-hold" ${inv?.focus==='buy-hold'?'selected':''}>🏦 Buy & Hold</option>
          <option value="both" ${inv?.focus==='both'?'selected':''}>🎯 Both</option>
          <option value="wholesale" ${inv?.focus==='wholesale'?'selected':''}>📋 Wholesale</option>
        </select>
      </div>
    </div>
    <div class="fg"><label>Target Zip Codes</label><input class="fi" id="iZips" value="${inv?.zips||''}" placeholder="80202, 80203, 80204"></div>
    <div class="grid-2">
      <div class="fg"><label>Active Deals</label><input class="fi" id="iActive" type="number" value="${inv?.active_deals||0}" min="0"></div>
      <div class="fg"><label>Deals Closed</label><input class="fi" id="iDone" type="number" value="${inv?.deals_done||0}" min="0"></div>
    </div>
    <div class="fg"><label>Notes</label><textarea class="fi" id="iNotes" rows="2">${inv?.notes||''}</textarea></div>
    <div class="faction">
      <button class="btn btn-secondary" onclick="cm('mAddInvestor')">Cancel</button>
      <button class="btn btn-primary" onclick="saveInvestor('${inv?.id||''}')">💾 Save</button>
    </div>
  `;
}

function addInvestor(){document.getElementById('invMT').textContent='Add Investor';document.getElementById('invFC').innerHTML=invForm(null);om('mAddInvestor');}
function editInvestor(id){const inv=db.investors.find(x=>x.id===id);document.getElementById('invMT').textContent='Edit Investor';document.getElementById('invFC').innerHTML=invForm(inv);om('mAddInvestor');}

async function saveInvestor(eid){
  const name=document.getElementById('iName').value.trim();
  if(!name)return toast('Name required',true);
  const row={
    name,company:document.getElementById('iCo').value,phone:document.getElementById('iPh').value,
    email:document.getElementById('iEm').value,budget:document.getElementById('iBudget').value,
    focus:document.getElementById('iFocus').value,zips:document.getElementById('iZips').value,
    active_deals:parseInt(document.getElementById('iActive').value)||0,
    deals_done:parseInt(document.getElementById('iDone').value)||0,
    notes:document.getElementById('iNotes').value
  };
  if(eid){
    const {error}=await supabase.from('investors').update(row).eq('id',eid);
    if(error){toast('Error: '+error.message,true);return;}
    const idx=db.investors.findIndex(x=>x.id===eid);
    if(idx>=0)db.investors[idx]={...db.investors[idx],...row};
    toast('Investor updated!');addAct('💼','Updated investor: '+name);
  } else {
    const id='inv_'+Date.now();
    const {error}=await supabase.from('investors').insert({...row,id});
    if(error){toast('Error: '+error.message,true);return;}
    db.investors.push({...row,id,created_at:new Date().toISOString()});
    toast('Investor added!');addAct('💼','Added investor: '+name);
  }
  cm('mAddInvestor');renderInvestors();
}

async function deleteInvestor(id){
  const inv=db.investors.find(x=>x.id===id);
  if(!confirm('Delete investor '+inv?.name+'?'))return;
  await supabase.from('investors').delete().eq('id',id);
  db.investors=db.investors.filter(x=>x.id!==id);
  renderInvestors();
  toast('Investor deleted');
}

// ============================================================
// ADMIN HUB
// ============================================================
function renderAdmin(){
  if(!isAdmin())return;
  loadAdminActivity();
  // Team members
  document.getElementById('adminTeamList').innerHTML=(allUsers||[]).map(u=>`
    <div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid rgba(200,168,75,0.08)">
      <div style="width:34px;height:34px;border-radius:50%;background:${u.role==='admin'?'linear-gradient(135deg,#d4aa45,#a8892e)':'rgba(59,130,246,0.2)'};display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;color:${u.role==='admin'?'#000':'var(--blue)'}">${u.name.split(' ').map(x=>x[0]).join('').toUpperCase().substring(0,2)}</div>
      <div style="flex:1">
        <div style="font-size:12.5px;font-weight:700">${u.name} ${u.role==='admin'?'<span style="font-size:9px;background:linear-gradient(135deg,#d4aa45,#a8892e);color:#000;padding:1px 6px;border-radius:8px">ADMIN</span>':''}</div>
        <div style="font-size:11px;color:var(--text3)">${u.email||'No email'}</div>
      </div>
    </div>`).join('');
  // Quick stats
  document.getElementById('adminQuickStats').innerHTML=`
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
      <div style="padding:10px;background:rgba(200,168,75,0.06);border-radius:8px;border:1px solid rgba(200,168,75,0.12)">
        <div style="font-size:22px;font-weight:800;color:var(--accent)">${(db.leads||[]).length}</div>
        <div style="font-size:10px;color:var(--text3);text-transform:uppercase;letter-spacing:.5px">Total Leads</div>
      </div>
      <div style="padding:10px;background:rgba(16,185,129,0.06);border-radius:8px;border:1px solid rgba(16,185,129,0.15)">
        <div style="font-size:22px;font-weight:800;color:var(--green)">${(db.properties||[]).length}</div>
        <div style="font-size:10px;color:var(--text3);text-transform:uppercase;letter-spacing:.5px">Properties</div>
      </div>
      <div style="padding:10px;background:rgba(59,130,246,0.06);border-radius:8px;border:1px solid rgba(59,130,246,0.15)">
        <div style="font-size:22px;font-weight:800;color:var(--blue)">${(db.buyers||[]).length}</div>
        <div style="font-size:10px;color:var(--text3);text-transform:uppercase;letter-spacing:.5px">Cash Buyers</div>
      </div>
      <div style="padding:10px;background:rgba(200,168,75,0.06);border-radius:8px;border:1px solid rgba(200,168,75,0.12)">
        <div style="font-size:22px;font-weight:800;color:var(--accent)">${(db.investors||[]).length}</div>
        <div style="font-size:10px;color:var(--text3);text-transform:uppercase;letter-spacing:.5px">Investors</div>
      </div>
    </div>`;
}

async function loadAdminActivity(){
  const {data}=await supabase.from('activities').select('*').order('created_at',{ascending:false}).limit(100);
  const el=document.getElementById('adminActivityFeed');
  if(!el)return;
  el.innerHTML=(data||[]).length===0?'<div style="color:var(--text3);padding:20px;text-align:center">No activity yet</div>':
    (data||[]).map(a=>`
      <div class="act-item">
        <div class="act-icon">${a.icon||'📋'}</div>
        <div>
          <div class="act-text">${a.text}</div>
          <div class="act-time">${a.user_name?'<strong>'+a.user_name+'</strong> · ':''} ${a.time||new Date(a.created_at).toLocaleString()}</div>
        </div>
      </div>`).join('');
}
'''

# Insert investors JS before addAct function
html = rp(
    'async function addAct(icon,text){',
    INVESTORS_JS + '\nasync function addAct(icon,text){',
    'investors JS'
)

# ============================================================
# 12. addAct — include user name in activity log
# ============================================================
html = rp(
    'async function addAct(icon,text){\n  await supabase.from(\'activities\').insert({icon,text,time:\'Just now\'});',
    """async function addAct(icon,text){
  const userName=currentUser?.name||'';
  await supabase.from('activities').insert({icon,text,time:'Just now',user_name:userName});""",
    'addAct with user_name'
)

# ============================================================
# 13. Add user_name column hint in activities (add to setup-v2.sql note)
# ============================================================
# (already handled - the activities table gets user_name as unlogged column via insert)

# ============================================================
# 14. Register investors button on investors page
# ============================================================
html = rp(
    '    <button class="btn btn-primary" onclick="om(\'mAddInvestor\')">+ Add Investor</button>',
    '    <button class="btn btn-primary" onclick="addInvestor()">+ Add Investor</button>',
    'investors add button'
)

# ============================================================
# 15. Fix db.investors initialization at top
# ============================================================
html = rp(
    "let db = { settings:{}, leads:[], properties:[], buyers:[], realtors:[], contacts:[], followups:[], adCampaigns:[], activities:[] };",
    "let db = { settings:{}, leads:[], properties:[], buyers:[], realtors:[], contacts:[], followups:[], adCampaigns:[], activities:[], investors:[] };",
    'db init with investors'
)

# ============================================================
# Write output
# ============================================================
out_path = '/root/.openclaw/workspace/steven-crm/index.html'
with open(out_path, 'w') as f:
    f.write(html)

print('\n✅ DONE — index.html written')
print(f'Size: {len(html):,} bytes')
