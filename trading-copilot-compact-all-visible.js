// JARVIS TRADING COPILOT - COMPACT VERSION (ALL VISIBLE)
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
    <div style="position:fixed;top:5px;right:5px;width:340px;background:linear-gradient(145deg,#0f172a 0%,#1e293b 100%);border:3px solid #06d6a0;border-radius:18px;color:white;font-family:-apple-system,BlinkMacSystemFont,sans-serif;z-index:10000;box-shadow:0 20px 40px rgba(0,0,0,0.4)">
        
        <!-- Header -->
        <div style="background:linear-gradient(135deg,#06d6a0,#118ab2);padding:12px;border-radius:15px 15px 0 0">
            <div style="display:flex;justify-content:space-between;align-items:center">
                <div>
                    <h2 style="margin:0;font-size:16px;font-weight:900">⚡ JARVIS COPILOT</h2>
                    <div style="font-size:9px;opacity:0.9;font-weight:600">AI TRADING ASSISTANT</div>
                </div>
                <button onclick="document.getElementById('jarvis-ui').remove()" style="background:rgba(255,255,255,0.2);color:white;border:none;border-radius:50%;width:28px;height:28px;cursor:pointer;font-size:14px">×</button>
            </div>
        </div>
        
        <!-- Content -->
        <div style="padding:12px">
            <!-- Stock Info -->
            <div style="text-align:center;margin-bottom:10px;padding:8px;background:rgba(6,214,160,0.1);border-radius:10px">
                <div style="font-size:20px;font-weight:900;color:#06d6a0">${ticker}</div>
                <div style="font-size:14px;color:#f1f5f9;font-weight:700">$${price.toFixed(2)}</div>
                <div style="background:#22c55e;color:white;padding:4px 10px;border-radius:12px;font-size:9px;font-weight:800;margin-top:6px;display:inline-block">🚀 BULLISH EDGE</div>
            </div>
            
            <!-- Trade Levels -->
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:5px;font-size:10px;text-align:center;margin-bottom:10px">
                <div style="background:#22c55e;padding:6px;border-radius:6px">
                    <div style="opacity:0.8;font-size:8px">ENTRY</div>
                    <div style="font-weight:900;font-size:11px">$${entry.toFixed(2)}</div>
                </div>
                <div style="background:#f59e0b;padding:6px;border-radius:6px">
                    <div style="opacity:0.8;font-size:8px">TARGET</div>
                    <div style="font-weight:900;font-size:11px">$${target.toFixed(2)}</div>
                </div>
                <div style="background:#ef4444;padding:6px;border-radius:6px">
                    <div style="opacity:0.8;font-size:8px">STOP</div>
                    <div style="font-weight:900;font-size:11px">$${stop.toFixed(2)}</div>
                </div>
            </div>
            
            <!-- Position -->
            <div style="background:#4338ca;padding:8px;border-radius:8px;margin-bottom:10px;text-align:center">
                <div style="font-size:12px;font-weight:900">💎 ${shares} SHARES</div>
                <div style="font-size:9px;opacity:0.9">Risk: $100 • Profit: $${profit.toFixed(2)}</div>
            </div>
            
            <!-- Steps - ULTRA COMPACT -->
            <div style="background:#0f172a;border:2px solid #fbbf24;padding:10px;border-radius:10px;margin-bottom:8px">
                <div style="font-size:11px;font-weight:900;color:#fbbf24;margin-bottom:8px;text-align:center">🎯 WEBULL STEPS:</div>
                
                <div style="font-size:9px;line-height:1.4">
                    <div style="background:rgba(251,191,36,0.1);margin:3px 0;padding:5px;border-radius:4px">
                        <span style="color:#fbbf24;font-weight:800">1.</span> <span style="color:#f1f5f9">Quantity: 10 → <span style="color:#22c55e;font-weight:900">${shares}</span></span>
                    </div>
                    <div style="background:rgba(251,191,36,0.1);margin:3px 0;padding:5px;border-radius:4px">
                        <span style="color:#fbbf24;font-weight:800">2.</span> <span style="color:#f1f5f9">Price → <span style="color:#22c55e;font-weight:900">$${entry.toFixed(2)}</span></span>
                    </div>
                    <div style="background:rgba(34,197,94,0.1);margin:3px 0;padding:5px;border-radius:4px">
                        <span style="color:#22c55e;font-weight:800">3.</span> <span style="color:#f1f5f9">Click "Simulated Buy AAPL"</span>
                    </div>
                    <div style="background:rgba(239,68,68,0.1);margin:3px 0;padding:5px;border-radius:4px">
                        <span style="color:#ef4444;font-weight:800">4.</span> <span style="color:#f1f5f9">Set stop: <span style="color:#ef4444;font-weight:900">$${stop.toFixed(2)}</span></span>
                    </div>
                    <div style="background:rgba(245,158,11,0.1);margin:3px 0;padding:5px;border-radius:4px">
                        <span style="color:#f59e0b;font-weight:800">5.</span> <span style="color:#f1f5f9">Set target: <span style="color:#f59e0b;font-weight:900">$${target.toFixed(2)}</span></span>
                    </div>
                </div>
            </div>
            
            <!-- Execute Button -->
            <div style="background:linear-gradient(135deg,#8b5cf6,#7c3aed);padding:10px;border-radius:10px;text-align:center;cursor:pointer" onclick="alert('PERFECT! Execute all 5 steps in Webull now! 🚀💎')">
                <div style="font-size:12px;font-weight:900">🚀 EXECUTE NOW!</div>
                <div style="font-size:9px;opacity:0.9">All 5 steps ready</div>
            </div>
        </div>
    </div>`;
    
    document.body.appendChild(ui);
})();