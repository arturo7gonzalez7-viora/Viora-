#!/usr/bin/env python3
"""Patch the property detail modal with polished design"""

with open('/root/.openclaw/workspace/steven-crm/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the innerHTML assignment start and the closing backtick + semicolon
START = "  document.getElementById('propDC').innerHTML=`"
END = "  `;\n  // Load photos + docs + notes async"

s = html.find(START)
e = html.find(END)
assert s != -1, "START not found"
assert e != -1, "END not found"

NEW_CONTENT = '''  document.getElementById('propDC').innerHTML=`
    <!-- PROPERTY HEADER -->
    <div style="padding:20px 24px 16px">
      <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:16px">
        <div style="flex:1;min-width:0">
          <div style="font-size:18px;font-weight:900;letter-spacing:-.3px;line-height:1.2;color:var(--text)">${p.address}</div>
          <div style="display:flex;align-items:center;gap:8px;margin-top:5px;flex-wrap:wrap">
            <span style="font-size:11px;background:rgba(200,168,75,0.12);color:var(--accent);border:1px solid rgba(200,168,75,0.2);border-radius:6px;padding:2px 8px;font-weight:700">${SLBLS[p.stage]}</span>
            <span style="font-size:12px;color:var(--text2)">Seller: <strong>${p.seller||'—'}</strong></span>
            ${agent?`<span style="font-size:12px;color:var(--blue)">· ${agent.name}</span>`:''}
            ${investor?`<span style="font-size:12px;color:var(--accent);font-weight:700">· ${investor.name}</span>`:''}
          </div>
        </div>
        <button class="btn btn-secondary btn-sm" style="flex-shrink:0;font-size:11px;white-space:nowrap" onclick="event.stopPropagation();openMLSFor('${p.address}')">Pull MLS Data</button>
      </div>

      <!-- STAT CARDS -->
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:16px">
        <div style="padding:12px 14px;background:linear-gradient(135deg,rgba(16,185,129,0.12),rgba(16,185,129,0.03));border:1px solid rgba(16,185,129,0.25);border-radius:10px">
          <div style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:var(--green);margin-bottom:4px">Est. Profit</div>
          <div style="font-size:20px;font-weight:900;color:${pr>=0?'var(--green)':'var(--hot)'}">$${Math.abs(pr).toLocaleString()}</div>
        </div>
        <div style="padding:12px 14px;background:linear-gradient(135deg,rgba(200,168,75,0.12),rgba(200,168,75,0.03));border:1px solid rgba(200,168,75,0.25);border-radius:10px">
          <div style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:var(--accent);margin-bottom:4px">Offer Price</div>
          <div style="font-size:20px;font-weight:900;color:var(--accent)">$${p.offerPrice.toLocaleString()}</div>
        </div>
        <div style="padding:12px 14px;background:linear-gradient(135deg,rgba(59,130,246,0.12),rgba(59,130,246,0.03));border:1px solid rgba(59,130,246,0.25);border-radius:10px">
          <div style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:var(--blue);margin-bottom:4px">ARV</div>
          <div style="font-size:20px;font-weight:900;color:var(--blue)">$${p.arv.toLocaleString()}</div>
        </div>
      </div>

      ${hasFinancials?`
      <div style="background:rgba(200,168,75,0.06);border:1px solid rgba(200,168,75,0.15);border-radius:10px;padding:12px 14px;margin-bottom:14px">
        <div style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:var(--accent);margin-bottom:10px">Financial Breakdown</div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(100px,1fr));gap:8px;font-size:12px">
          <div><div style="color:var(--text3);font-size:10px">Revenue</div><div style="font-weight:700;color:var(--green)">$${(fin.revenue||0).toLocaleString()}</div></div>
          <div><div style="color:var(--text3);font-size:10px">Wholesale Fee</div><div style="font-weight:700;color:var(--accent)">$${(fin.wholesaleFee||0).toLocaleString()}</div></div>
          <div><div style="color:var(--text3);font-size:10px">Fee Earned</div><div style="font-weight:700;color:var(--green)">$${(fin.feeEarned||0).toLocaleString()}</div></div>
          <div><div style="color:var(--text3);font-size:10px">Referral</div><div style="font-weight:700;color:var(--purple)">$${(fin.referralFee||0).toLocaleString()}</div></div>
          <div><div style="color:var(--text3);font-size:10px">Concessions</div><div style="font-weight:700;color:var(--hot)">$${(fin.concessions||0).toLocaleString()}</div></div>
        </div>
      </div>`:''}

      <!-- DETAILS + CHECKLIST GRID -->
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px">
        <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(200,168,75,0.12);border-radius:10px;padding:14px">
          <div style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:var(--text3);margin-bottom:10px">Property Details</div>
          <div style="display:flex;flex-direction:column;gap:7px">
            <div style="display:flex;justify-content:space-between;align-items:center;font-size:12.5px">
              <span style="color:var(--text3)">Repairs</span>
              <span style="font-weight:700">$${p.repairs.toLocaleString()}</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;font-size:12.5px">
              <span style="color:var(--text3)">Buyer</span>
              <span style="font-weight:600">${buyer?.name||'—'}</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;font-size:12.5px">
              <span style="color:var(--text3)">Investor</span>
              <span style="font-weight:700;color:${investor?'var(--accent)':'var(--text3)'}; ">${investor?.name||'—'}</span>
            </div>
            ${agent?`<div style="display:flex;justify-content:space-between;align-items:center;font-size:12.5px"><span style="color:var(--text3)">Agent</span><span style="font-weight:600;color:var(--blue)">${agent.name}</span></div>`:''}
            <div style="display:flex;justify-content:space-between;align-items:center;font-size:12.5px">
              <span style="color:var(--text3)">Days in Stage</span>
              <span style="font-weight:600">${p.daysInStage}</span>
            </div>
          </div>
          <div style="margin-top:12px;padding-top:10px;border-top:1px solid rgba(200,168,75,0.1)">
            <select class="fi" onchange="moveStage('${p.id}',this.value)" style="width:100%;font-size:12px;margin-bottom:8px">${STAGES.map(s=>`<option value="${s}" ${p.stage===s?'selected':''}>${SLBLS[s]}</option>`).join('')}</select>
            <div style="display:flex;gap:6px">
              <button class="btn btn-secondary btn-sm" style="flex:1;font-size:11.5px" onclick="editProp('${p.id}')">Edit</button>
              <button class="btn btn-danger btn-sm" style="font-size:11.5px" onclick="confDel('property','${p.id}')">Delete</button>
            </div>
          </div>
        </div>
        <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(200,168,75,0.12);border-radius:10px;padding:14px">
          <div style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:var(--text3);margin-bottom:10px">Closing Checklist</div>
          ${(p.checklist||[]).length===0?'<div style="font-size:12px;color:var(--text3);padding:4px 0">No checklist items</div>':''}
          ${(p.checklist||[]).map((it,i)=>`
            <label style="display:flex;align-items:center;gap:9px;margin-bottom:9px;cursor:pointer;user-select:none">
              <input type="checkbox" ${it.done?'checked':''} onchange="togCL('${p.id}',${i},this.checked)" style="width:16px;height:16px;cursor:pointer;accent-color:var(--accent);flex-shrink:0;border-radius:4px">
              <span style="font-size:12.5px;line-height:1.3;${it.done?'text-decoration:line-through;color:var(--text3)':'color:var(--text2)'}">${it.item}</span>
            </label>`).join('')}
        </div>
      </div>
      ${renderMatchedBuyers(p)}
    </div>

    <!-- TABS -->
    <div style="padding:0 24px 22px;border-top:1px solid rgba(200,168,75,0.1)">
      <div style="display:flex;gap:2px;margin-top:16px;margin-bottom:-1px;overflow-x:auto">
        <div class="prop-tab active" onclick="switchPropTab('${p.id}','photos',this)">📷 Photos</div>
        <div class="prop-tab" onclick="switchPropTab('${p.id}','docs',this)">📄 Documents</div>
        <div class="prop-tab" onclick="switchPropTab('${p.id}','notes',this)">📝 Notes</div>
        <div class="prop-tab" onclick="switchPropTab('${p.id}','investor',this)">💼 Investor</div>
      </div>
      <div class="prop-tab-content" id="propTabContent_${p.id}">
        <!-- PHOTOS TAB -->
        <div id="propTab_photos_${p.id}">
          <label class="upload-zone">
            <span style="font-size:28px;margin-bottom:6px">📷</span>
            <span style="font-size:13px;font-weight:700;color:var(--text)">Upload Photos</span>
            <span style="font-size:11px;color:var(--text3);margin-top:3px">JPG, PNG, HEIC — click or drop files</span>
            <input type="file" accept="image/*" multiple style="display:none" onchange="uploadPropPhotos('${p.id}',this)">
          </label>
          <div class="photo-grid" id="propPhotos_${p.id}"></div>
        </div>
        <!-- DOCUMENTS TAB -->
        <div id="propTab_docs_${p.id}" style="display:none">
          <div style="display:flex;gap:8px;margin-bottom:14px;flex-wrap:wrap;align-items:center">
            <select class="fi" id="docType_${p.id}" style="flex:1;min-width:150px;max-width:200px;font-size:12px">
              <option value="contract">Contract</option>
              <option value="inspection">Inspection Report</option>
              <option value="title">Title Document</option>
              <option value="other">Other</option>
            </select>
            <label class="btn btn-primary" style="cursor:pointer;display:inline-flex;align-items:center;gap:6px;font-size:12px">
              + Upload Document
              <input type="file" style="display:none" onchange="uploadPropDoc('${p.id}',this)">
            </label>
          </div>
          <div id="propDocs_${p.id}"><div style="color:var(--text3);font-size:13px;text-align:center;padding:20px">No documents yet</div></div>
        </div>
        <!-- NOTES TAB -->
        <div id="propTab_notes_${p.id}" style="display:none">
          <textarea class="fi" id="noteInput_${p.id}" placeholder="Write a note about this property..." style="width:100%;min-height:80px;resize:vertical;font-size:13px;margin-bottom:10px;box-sizing:border-box"></textarea>
          <button class="btn btn-primary" style="font-size:12px;padding:9px 20px" onclick="addPropNote('${p.id}')">Save Note</button>
          <div id="propNotes_${p.id}" style="margin-top:14px"><div style="color:var(--text3);font-size:13px;text-align:center;padding:20px">No notes yet</div></div>
        </div>
        <!-- INVESTOR TAB -->
        <div id="propTab_investor_${p.id}" style="display:none">
          <div style="margin-bottom:16px">
            <label style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.7px;color:var(--text3);display:block;margin-bottom:8px">Assign Investor</label>
            <select class="fi" id="propInvestorSel_${p.id}" style="width:100%;max-width:360px" onchange="assignPropInvestor('${p.id}',this.value)">
              <option value="">No investor assigned</option>
              ${(db.investors||[]).map(inv=>`<option value="${inv.id}" ${p.investor_id===inv.id?'selected':''}>${inv.name}${inv.company?' — '+inv.company:''}</option>`).join('')}
            </select>
            ${(db.investors||[]).length===0?'<div style="font-size:11px;color:var(--text3);margin-top:6px">No investors in your list yet. Add them in the Investors section.</div>':''}
          </div>
          ${investor?`<div class="inv-card" style="max-width:440px">
            <div style="font-size:16px;font-weight:900;color:var(--accent);margin-bottom:3px">${investor.name}</div>
            ${investor.company?`<div style="font-size:12px;color:var(--text2);margin-bottom:12px">${investor.company}</div>`:''}
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:12px">
              ${investor.phone?`<div style="background:rgba(255,255,255,0.05);border-radius:7px;padding:8px 10px"><div style="color:var(--text3);font-size:10px;margin-bottom:2px">Phone</div><div style="font-weight:600">${investor.phone}</div></div>`:''}
              ${investor.email?`<div style="background:rgba(255,255,255,0.05);border-radius:7px;padding:8px 10px"><div style="color:var(--text3);font-size:10px;margin-bottom:2px">Email</div><div style="font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${investor.email}</div></div>`:''}
              ${investor.budget?`<div style="background:rgba(200,168,75,0.08);border:1px solid rgba(200,168,75,0.15);border-radius:7px;padding:8px 10px"><div style="color:var(--text3);font-size:10px;margin-bottom:2px">Budget</div><div style="font-weight:700;color:var(--accent)">${investor.budget}</div></div>`:''}
              ${investor.focus?`<div style="background:rgba(255,255,255,0.05);border-radius:7px;padding:8px 10px"><div style="color:var(--text3);font-size:10px;margin-bottom:2px">Focus</div><div style="font-weight:600">${investor.focus}</div></div>`:''}
            </div>
          </div>`:`<div style="text-align:center;padding:28px 0;color:var(--text3)"><div style="font-size:32px;margin-bottom:10px">💼</div><div style="font-size:13px">No investor assigned to this property</div></div>`}'''

html = html[:s] + NEW_CONTENT + '\n  `;\n  // Load photos + docs + notes async' + html[e + len(END):]

with open('/root/.openclaw/workspace/steven-crm/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Done. File size: {len(html):,} bytes')
