#!/usr/bin/env python3
"""Replace Lucide CDN with inline SVG icons that always work"""

with open('/root/.openclaw/workspace/steven-crm/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove Lucide CDN and DOMContentLoaded block
html = html.replace(
    '<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>\n'
    '<script>\ndocument.addEventListener(\'DOMContentLoaded\', function() {\n'
    '  if (window.lucide) lucide.createIcons();\n});\n</script>\n', '', 1
)

# Remove any lucide.createIcons() calls
import re
html = re.sub(r'\s*if\(window\.lucide\)[^;]+;', '', html)

# Compact inline SVG icon function
def svg(path_d, viewbox="0 0 24 24", extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" '
            f'width="16" height="16" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
            f'style="display:inline-block;vertical-align:middle;flex-shrink:0" {extra}>'
            f'{path_d}</svg>')

# Icon definitions — clean minimal SVG paths
ICONS = {
    'layout-dashboard': svg('<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>'),
    'users': svg('<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>'),
    'kanban': svg('<rect x="3" y="3" width="5" height="18" rx="1"/><rect x="10" y="3" width="5" height="12" rx="1"/><rect x="17" y="3" width="5" height="8" rx="1"/>'),
    'megaphone': svg('<path d="M3 11l19-9-9 19-2-8-8-2z"/>'),
    'bar-chart-2': svg('<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>'),
    'wallet': svg('<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M16 12h2"/>'),
    'handshake': svg('<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>'),
    'book-user': svg('<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><circle cx="12" cy="10" r="2"/><path d="M9 14c0-1.1 1.3-2 3-2s3 .9 3 2"/>'),
    'calendar-check': svg('<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="M9 16l2 2 4-4"/>'),
    'message-square': svg('<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'),
    'home': svg('<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>'),
    'briefcase': svg('<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/><line x1="12" y1="12" x2="12" y2="12.01"/>'),
    'shield-check': svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/>'),
    'settings': svg('<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>'),
    # Stat icons
    'trending-up': svg('<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>'),
    'trophy': svg('<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 22v-4"/><path d="M14 22v-4"/><rect x="6" y="2" width="12" height="13" rx="2"/><path d="M12 17v1"/>'),
    'target': svg('<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>'),
    'chart-line': svg('<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>'),
    'building-2': svg('<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18"/><path d="M6 12h4"/><path d="M14 12h4"/><path d="M6 7h4"/><path d="M14 7h4"/><path d="M6 17h4"/><path d="M14 17h4"/><line x1="2" y1="22" x2="22" y2="22"/>'),
    'refresh-cw': svg('<polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>'),
    'check-circle': svg('<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>'),
    'circle-dollar-sign': svg('<circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><line x1="12" y1="6" x2="12" y2="8"/><line x1="12" y1="16" x2="12" y2="18"/>'),
}

# Replace all <i data-lucide="name"></i> with inline SVG
for name, svg_html in ICONS.items():
    old = f'<i data-lucide="{name}"></i>'
    if old in html:
        html = html.replace(old, svg_html)
        print(f'[OK] replaced {name}')
    else:
        print(f'[SKIP] {name}')

# Update nav-icon CSS to work with inline SVG
html = html.replace(
    '.nav-icon{width:18px;height:18px;display:flex;align-items:center;justify-content:center;flex-shrink:0;opacity:0.75}.nav-item.active .nav-icon{opacity:1}.nav-icon svg{width:15px;height:15px;stroke-width:2;vertical-align:middle}',
    '.nav-icon{width:20px;height:20px;display:flex;align-items:center;justify-content:center;flex-shrink:0;opacity:0.65}.nav-item.active .nav-icon{opacity:1}.nav-item:hover .nav-icon{opacity:0.9}.nav-icon svg{width:16px;height:16px}'
)

# Update stat-icon CSS
html = html.replace(
    '.stat-icon{width:32px;height:32px;display:flex;align-items:center;justify-content:center;border-radius:8px;margin-bottom:10px;background:rgba(255,255,255,0.06)}.stat-icon svg{width:18px;height:18px;stroke-width:2}',
    '.stat-icon{width:34px;height:34px;display:flex;align-items:center;justify-content:center;border-radius:8px;margin-bottom:10px;background:rgba(255,255,255,0.06)}.stat-icon svg{width:18px;height:18px}'
)

with open('/root/.openclaw/workspace/steven-crm/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\n✅ Done. Size: {len(html):,} bytes')
