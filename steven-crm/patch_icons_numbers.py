#!/usr/bin/env python3
"""Fix numbers accuracy + replace emoji icons with Lucide SVG icons"""

with open('/root/.openclaw/workspace/steven-crm/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

def rp(old, new, label):
    if old not in html:
        print(f'[SKIP] {label}')
        return html
    print(f'[OK] {label}')
    return html.replace(old, new, 1)

# ============================================================
# 1. Add Lucide icons CDN in <head>
# ============================================================
html = rp(
    '<link rel="icon"',
    '<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>\n<link rel="icon"',
    'lucide CDN'
)

# ============================================================
# 2. nav-icon CSS — make it a proper icon container
# ============================================================
html = rp(
    '.nav-icon{font-size:15px;width:18px;text-align:center;flex-shrink:0}',
    '.nav-icon{width:18px;height:18px;display:flex;align-items:center;justify-content:center;flex-shrink:0;opacity:0.75}.nav-item.active .nav-icon{opacity:1}.nav-icon svg{width:15px;height:15px;stroke-width:2;vertical-align:middle}',
    'nav-icon CSS'
)

# ============================================================
# 3. stat-icon CSS — clean icon container
# ============================================================
html = rp(
    '.stat-icon{font-size:20px;margin-bottom:10px}',
    '.stat-icon{width:32px;height:32px;display:flex;align-items:center;justify-content:center;border-radius:8px;margin-bottom:10px;background:rgba(255,255,255,0.06)}.stat-icon svg{width:18px;height:18px;stroke-width:2}',
    'stat-icon CSS'
)

# ============================================================
# 4. Replace sidebar nav emoji icons with Lucide SVG
# ============================================================
ICON = lambda name: f'<i data-lucide="{name}"></i>'

NAV_REPLACEMENTS = [
    ('<span class="nav-icon">🏠</span>Dashboard', f'<span class="nav-icon">{ICON("layout-dashboard")}</span>Dashboard'),
    ('<span class="nav-icon">👥</span>Sellers & Leads', f'<span class="nav-icon">{ICON("users")}</span>Sellers & Leads'),
    ('<span class="nav-icon">📋</span>Pipeline', f'<span class="nav-icon">{ICON("kanban")}</span>Pipeline'),
    ('<span class="nav-icon">📢</span>Ads Center', f'<span class="nav-icon">{ICON("megaphone")}</span>Ads Center'),
    ('<span class="nav-icon">📊</span>Analytics', f'<span class="nav-icon">{ICON("bar-chart-2")}</span>Analytics'),
    ('<span class="nav-icon">💰</span>Cash Buyers', f'<span class="nav-icon">{ICON("wallet")}</span>Cash Buyers'),
    ('<span class="nav-icon">🤝</span>Realtors', f'<span class="nav-icon">{ICON("handshake")}</span>Realtors'),
    ('<span class="nav-icon">📁</span>All Contacts', f'<span class="nav-icon">{ICON("book-user")}</span>All Contacts'),
    ('<span class="nav-icon">📅</span>Follow-Ups', f'<span class="nav-icon">{ICON("calendar-check")}</span>Follow-Ups'),
    ('<span class="nav-icon">💬</span>SMS Templates', f'<span class="nav-icon">{ICON("message-square")}</span>SMS Templates'),
    ('<span class="nav-icon">🏘️</span>MLS Data', f'<span class="nav-icon">{ICON("home")}</span>MLS Data'),
    ('<span class="nav-icon">💼</span>Investors', f'<span class="nav-icon">{ICON("briefcase")}</span>Investors'),
    ('<span class="nav-icon">⚙️</span>Settings', f'<span class="nav-icon">{ICON("settings")}</span>Settings'),
    # Admin hub (special)
    ('<span class="nav-icon" style="color:#c8a84b">👑</span>', f'<span class="nav-icon">{ICON("shield-check")}</span>'),
]

for old, new in NAV_REPLACEMENTS:
    if old in html:
        html = html.replace(old, new, 1)
        print(f'[OK] nav icon: {old[:40]}...')
    else:
        print(f'[SKIP] nav: {old[:40]}')

# ============================================================
# 5. Fix dashboard stat card icons (replace emoji with Lucide)
# ============================================================
STAT_ICONS = [
    ('"stat-icon">👥</div>', f'"stat-icon">{ICON("users")}</div>'),
    ('"stat-icon">📋</div>', f'"stat-icon">{ICON("kanban")}</div>'),
    ('"stat-icon">💰</div>', f'"stat-icon">{ICON("trending-up")}</div>'),
    ('"stat-icon">🏆</div>', f'"stat-icon">{ICON("trophy")}</div>'),
    ('"stat-icon">🎯</div>', f'"stat-icon">{ICON("target")}</div>'),
    ('"stat-icon">📈</div>', f'"stat-icon">{ICON("chart-line")}</div>'),
    ('"stat-icon">📅</div>', f'"stat-icon">{ICON("calendar-check")}</div>'),
    ('"stat-icon">🏠</div>', f'"stat-icon">{ICON("building-2")}</div>'),
    ('"stat-icon">💼</div>', f'"stat-icon">{ICON("briefcase")}</div>'),
    ('"stat-icon">🔄</div>', f'"stat-icon">{ICON("refresh-cw")}</div>'),
    ('"stat-icon">✅</div>', f'"stat-icon">{ICON("check-circle")}</div>'),
]
for old, new in STAT_ICONS:
    count = html.count(old)
    html = html.replace(old, new)
    if count:
        print(f'[OK] stat icon x{count}: {old[:40]}')

# ============================================================
# 6. Fix dashboard NUMBERS
#    - Pipeline Value: show total ARV of active deals (not capped profit)
#    - Total Pipeline Value → "Est. Total Profit" with actual sum (not Math.max capped)
#    - "This Month Revenue" → also check if there's data
# ============================================================
# The pipeVal currently uses Math.max(0,...) which caps negatives to 0
# Fix: separate total ARV vs total est profit

html = rp(
    '  const pipeVal=db.properties.filter(p=>!\'closed\',\'dead\'].includes(p.stage)).reduce((s,p)=>s+Math.max(0,p.arv*.7-p.repairs-p.offerPrice),0);',
    '  const pipeVal=db.properties.filter(p=>![\'closed\',\'dead\'].includes(p.stage)).reduce((s,p)=>s+(p.arv||0),0);\n  const estProfit=db.properties.filter(p=>![\'closed\',\'dead\'].includes(p.stage)).reduce((s,p)=>s+(p.arv*.7-p.repairs-p.offerPrice),0);',
    'pipeVal fix - ARV based'
)

# Try alternate format in case the above had wrong quote escaping
if '  const pipeVal=db.properties.filter' not in html or 'estProfit' not in html:
    # find and fix with Python string approach
    OLD_PIPE = "  const pipeVal=db.properties.filter(p=>!['closed','dead'].includes(p.stage)).reduce((s,p)=>s+Math.max(0,p.arv*.7-p.repairs-p.offerPrice),0);"
    NEW_PIPE = "  const pipeVal=db.properties.filter(p=>!['closed','dead'].includes(p.stage)).reduce((s,p)=>s+(p.arv||0),0);\n  const estProfit=db.properties.filter(p=>!['closed','dead'].includes(p.stage)).reduce((s,p)=>s+(p.arv*.7-p.repairs-p.offerPrice),0);"
    if OLD_PIPE in html:
        html = html.replace(OLD_PIPE, NEW_PIPE, 1)
        print('[OK] pipeVal fix via direct string')
    else:
        print('[SKIP] pipeVal - trying inline search')
        # Try to find the line
        idx = html.find("Math.max(0,p.arv*.7-p.repairs-p.offerPrice),0);")
        if idx != -1:
            line_start = html.rfind('\n', 0, idx) + 1
            line_end = html.find('\n', idx)
            old_line = html[line_start:line_end]
            new_line = "  const pipeVal=db.properties.filter(p=>!['closed','dead'].includes(p.stage)).reduce((s,p)=>s+(p.arv||0),0);\n  const estProfit=db.properties.filter(p=>!['closed','dead'].includes(p.stage)).reduce((s,p)=>s+(p.arv*.7-p.repairs-p.offerPrice),0);"
            html = html[:line_start] + new_line + html[line_end:]
            print('[OK] pipeVal fix via line search')

# Fix stat cards to use new values
html = rp(
    '<div class="stat-card green"><div class="stat-icon"><i data-lucide="trending-up"></i></div><div class="stat-label">Pipeline Value</div><div class="stat-value">$${Math.round(pipeVal/1000)}K</div><div class="stat-sub">Est. profit</div></div>',
    '<div class="stat-card green"><div class="stat-icon"><i data-lucide="trending-up"></i></div><div class="stat-label">Pipeline ARV</div><div class="stat-value">$${Math.round(pipeVal/1000)}K</div><div class="stat-sub">Total deal value</div></div>',
    'stat card Pipeline Value label'
)

html = rp(
    '<div class="stat-card red"><div class="stat-icon"><i data-lucide="building-2"></i></div><div class="stat-label">Total Pipeline Value</div><div class="stat-value">$${Math.round(pipeVal/1000)}K</div><div class="stat-sub">active deals</div></div>',
    '<div class="stat-card gold"><div class="stat-icon"><i data-lucide="circle-dollar-sign"></i></div><div class="stat-label">Est. Total Profit</div><div class="stat-value" style="color:${estProfit>=0?\'var(--green)\':(\'var(--hot)\')}">$${Math.round(Math.abs(estProfit)/1000)}K${estProfit<0?\' ▼\':\'\'}</div><div class="stat-sub">${estProfit>=0?\'active pipeline\':\'currently negative\'}</div></div>',
    'stat card Total Pipeline Value → Est Profit'
)

# ============================================================
# 7. Call lucide.createIcons() after any render that updates DOM
# ============================================================
# Add after the closing splash screen removal (after DOMContentLoaded init)
html = rp(
    'setTimeout(function(){\n  const sp=document.getElementById(\'splash\');',
    'setTimeout(function(){\n  if(window.lucide) lucide.createIcons();\n  const sp=document.getElementById(\'splash\');',
    'lucide createIcons on load'
)

# Also call after renderDash, renderKanban, go() navigation
html = rp(
    "  document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));",
    "  document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));\n  if(window.lucide) setTimeout(()=>lucide.createIcons(),50);",
    'lucide createIcons on nav'
)

# ============================================================
# 8. Write
# ============================================================
with open('/root/.openclaw/workspace/steven-crm/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\n✅ Done. Size: {len(html):,} bytes')
