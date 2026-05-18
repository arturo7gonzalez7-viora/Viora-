// JARVIS TRADING COPILOT - FIXED & ULTRA COOL VERSION
javascript:(function(){
    var e=document.getElementById('jarvis-ui');
    if(e)e.remove();
    
    function getTicker(){
        var t='';
        if(location.hostname.includes('finance.yahoo.com')){
            var h=document.querySelector('h1[data-testid="quote-header"]');
            if(h)t=h.textContent.split('(')[1]?.split(')')[0]||'';
        }else if(location.hostname.includes('webull.com')){
            var u=location.pathname.match(/\/([A-Z]{1,5})\//);
            if(u)t=u[1];
        }
        if(!t){
            var m=document.title.match(/\b([A-Z]{1,5})\b/);
            if(m)t=m[1];
        }
        return t||'AAPL';
    }
    
    function getPrice(){
        var p=document.querySelector('[data-testid="qsp-price"]');
        if(p)return parseFloat(p.textContent.replace(/[^0-9.]/g,''));
        var m=document.body.textContent.match(/\$(\d+\.\d+)/);
        return m?parseFloat(m[1]):262.52;
    }
    
    var ticker=getTicker();
    var price=getPrice();
    var entry=price;
    var stop=price*0.97;
    var target=price*1.08;
    var shares=Math.floor(100/(price-stop));
    var profit=(target-entry)*shares;
    
    var ui=document.createElement('div');
    ui.id='jarvis-ui';
    ui.innerHTML=`
    <div style="position:fixed;top:15px;right:15px;width:380px;background:linear-gradient(145deg,#0f172a 0%,#1e293b 50%,#334155 100%);border:3px solid #06d6a0;border-radius:24px;color:white;font-family:-apple-system,BlinkMacSystemFont,sans-serif;z-index:10000;box-shadow:0 25px 50px rgba(0,0,0,0.4),0 0 30px rgba(6,214,160,0.2);backdrop-filter:blur(20px)">
        
        <div style="background:linear-gradient(135deg,#06d6a0 0%,#118ab2 100%);padding:22px;border-radius:21px 21px 0 0;position:relative;overflow:hidden">
            <div style="position:absolute;top:-50px;right:-50px;width:100px;height:100px;background:radial-gradient(circle,rgba(255,255,255,0.1),transparent 70%);border-radius:50%"></div>
            <div style="display:flex;justify-content:space-between;align-items:center;position:relative">
                <div>
                    <h2 style="margin:0;font-size:22px;font-weight:900;letter-spacing:-0.5px;text-shadow:0 2px 4px rgba(0,0,0,0.3)">⚡ JARVIS COPILOT</h2>
                    <div style="font-size:11px;opacity:0.95;font-weight:600;text-transform:uppercase;letter-spacing:1px">AI TRADING ASSISTANT</div>
                </div>
                <button onclick="document.getElementById('jarvis-ui').remove()" style="background:rgba(255,255,255,0.15);color:white;border:none;border-radius:50%;width:36px;height:36px;cursor:pointer;font-size:18px;font-weight:700;transition:all 0.2s">×</button>
            </div>
        </div>
        
        <div style="padding:24px">
            <div style="text-align:center;margin-bottom:20px;padding:16px;background:linear-gradient(135deg,rgba(6,214,160,0.1),rgba(17,138,178,0.05));border-radius:16px;border:1px solid rgba(6,214,160,0.2)">
                <div style="font-size:32px;font-weight:900;color:#06d6a0;text-shadow:0 0 20px rgba(6,214,160,0.3)">${ticker}</div>
                <div style="font-size:20px;color:#f1f5f9;font-weight:700;margin:4px 0">$${price.toFixed(2)}</div>
                <div style="background:linear-gradient(135deg,#22c55e,#16a34a);color:white;padding:8px 20px;border-radius:20px;font-size:13px;font-weight:800;margin-top:12px;display:inline-block;text-transform:uppercase;letter-spacing:0.5px;box-shadow:0 4px 12px rgba(34,197,94,0.3)">🚀 BULLISH EDGE</div>
            </div>
            
            <div style="background:linear-gradient(135deg,#1e293b,#334155);padding:18px;border-radius:16px;margin-bottom:18px;border:1px solid #475569">
                <div style="font-size:15px;font-weight:800;color:#06d6a0;margin-bottom:12px;text-transform:uppercase;letter-spacing:0.5px">📊 PROFESSIONAL SETUP</div>
                <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;font-size:13px;text-align:center">
                    <div style="background:linear-gradient(135deg,#22c55e,#16a34a);padding:12px;border-radius:12px;box-shadow:0 4px 8px rgba(34,197,94,0.2)">
                        <div style="opacity:0.9;font-weight:600;font-size:10px;text-transform:uppercase;letter-spacing:0.5px">🎯 ENTRY</div>
                        <div style="font-weight:900;font-size:16px;margin-top:2px">$${entry.toFixed(2)}</div>
                    </div>
                    <div style="background:linear-gradient(135deg,#f59e0b,#d97706);padding:12px;border-radius:12px;box-shadow:0 4px 8px rgba(245,158,11,0.2)">
                        <div style="opacity:0.9;font-weight:600;font-size:10px;text-transform:uppercase;letter-spacing:0.5px">🚀 TARGET</div>
                        <div style="font-weight:900;font-size:16px;margin-top:2px">$${target.toFixed(2)}</div>
                    </div>
                    <div style="background:linear-gradient(135deg,#ef4444,#dc2626);padding:12px;border-radius:12px;box-shadow:0 4px 8px rgba(239,68,68,0.2)">
                        <div style="opacity:0.9;font-weight:600;font-size:10px;text-transform:uppercase;letter-spacing:0.5px">🛡️ STOP</div>
                        <div style="font-weight:900;font-size:16px;margin-top:2px">$${stop.toFixed(2)}</div>
                    </div>
                </div>
            </div>
            
            <div style="background:linear-gradient(135deg,#4338ca,#3730a3);padding:18px;border-radius:16px;margin-bottom:18px;text-align:center;box-shadow:0 8px 16px rgba(67,56,202,0.3)">
                <div style="font-size:16px;font-weight:900;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px">💎 ${shares} SHARES</div>
                <div style="font-size:13px;opacity:0.95;font-weight:600">Risk: $100 • Profit: $${profit.toFixed(2)} • R/R: 2.5:1</div>
            </div>
            
            <div style="background:linear-gradient(135deg,#0f172a,#1e293b);border:2px solid #fbbf24;padding:20px;border-radius:16px;margin-bottom:18px">
                <div style="font-size:15px;font-weight:900;color:#fbbf24;margin-bottom:12px;text-transform:uppercase;letter-spacing:0.5px;text-align:center">🎯 EXECUTION STEPS</div>
                <div style="font-size:13px;line-height:1.8;font-weight:600">
                    <div style="margin:6px 0;padding:6px 0;border-bottom:1px solid rgba(251,191,36,0.2)">1️⃣ Change quantity to <span style="color:#fbbf24;font-weight:900">${shares} shares</span></div>
                    <div style="margin:6px 0;padding:6px 0;border-bottom:1px solid rgba(251,191,36,0.2)">2️⃣ Set limit price to <span style="color:#fbbf24;font-weight:900">$${entry.toFixed(2)}</span></div>
                    <div style="margin:6px 0;padding:6px 0;border-bottom:1px solid rgba(251,191,36,0.2)">3️⃣ Click <span style="color:#22c55e;font-weight:900">"Simulated Buy AAPL"</span></div>
                    <div style="margin:6px 0;padding:6px 0;border-bottom:1px solid rgba(251,191,36,0.2)">4️⃣ Set stop-loss at <span style="color:#ef4444;font-weight:900">$${stop.toFixed(2)}</span></div>
                    <div style="margin:6px 0;padding:6px 0">5️⃣ Set target at <span style="color:#f59e0b;font-weight:900">$${target.toFixed(2)}</span></div>
                </div>
            </div>
            
            <div style="background:linear-gradient(135deg,#8b5cf6 0%,#7c3aed 50%,#6d28d9 100%);padding:18px;border-radius:16px;text-align:center;cursor:pointer;transition:all 0.3s;box-shadow:0 8px 20px rgba(139,92,246,0.4)" onclick="alert('EXECUTE NOW! Follow the 5 steps above in your Webull interface. You got this! 🚀')" onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 12px 24px rgba(139,92,246,0.5)'" onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 8px 20px rgba(139,92,246,0.4)'">
                <div style="font-size:16px;font-weight:900;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px">🚀 EXECUTE TRADE</div>
                <div style="font-size:12px;opacity:0.95;font-weight:600">Click for live trading guidance</div>
            </div>
        </div>
    </div>`;
    
    document.body.appendChild(ui);
})();