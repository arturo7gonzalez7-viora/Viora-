// JARVIS TRADING COPILOT - COMPACT PREMIUM VERSION (Browser-Safe)
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
    <div style="position:fixed;top:20px;right:20px;width:360px;background:linear-gradient(135deg,#1a202c,#2d3748);border:2px solid #4fd1c5;border-radius:20px;color:white;font-family:-apple-system,BlinkMacSystemFont,sans-serif;z-index:10000;box-shadow:0 20px 40px rgba(0,0,0,0.3)">
        <div style="background:linear-gradient(135deg,#4fd1c5,#38b2ac);padding:20px;border-radius:18px 18px 0 0">
            <div style="display:flex;justify-content:space-between;align-items:center">
                <div>
                    <h2 style="margin:0;font-size:20px;font-weight:800">⚡ JARVIS COPILOT</h2>
                    <div style="font-size:11px;opacity:0.9">Step-by-Step Trading Guide</div>
                </div>
                <button onclick="document.getElementById('jarvis-ui').remove()" style="background:rgba(255,255,255,0.2);color:white;border:none;border-radius:50%;width:32px;height:32px;cursor:pointer;font-size:16px">×</button>
            </div>
        </div>
        
        <div style="padding:20px">
            <div style="margin-bottom:20px;text-align:center">
                <div style="font-size:28px;font-weight:800;color:#4fd1c5">${ticker}</div>
                <div style="font-size:18px;color:#e2e8f0">$${price.toFixed(2)}</div>
                <div style="background:#22c55e;color:white;padding:8px 16px;border-radius:12px;font-size:12px;font-weight:700;margin-top:8px;display:inline-block">🚀 BULLISH SETUP</div>
            </div>
            
            <div style="background:#2d3748;padding:16px;border-radius:12px;margin-bottom:16px">
                <div style="font-size:14px;font-weight:700;color:#4fd1c5;margin-bottom:8px">📊 TRADE PLAN</div>
                <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;font-size:12px;text-align:center">
                    <div style="background:#22c55e;padding:8px;border-radius:6px">
                        <div style="opacity:0.8">ENTRY</div>
                        <div style="font-weight:800">$${entry.toFixed(2)}</div>
                    </div>
                    <div style="background:#f59e0b;padding:8px;border-radius:6px">
                        <div style="opacity:0.8">TARGET</div>
                        <div style="font-weight:800">$${target.toFixed(2)}</div>
                    </div>
                    <div style="background:#ef4444;padding:8px;border-radius:6px">
                        <div style="opacity:0.8">STOP</div>
                        <div style="font-weight:800">$${stop.toFixed(2)}</div>
                    </div>
                </div>
            </div>
            
            <div style="background:#4338ca;padding:16px;border-radius:12px;margin-bottom:16px;text-align:center">
                <div style="font-size:14px;font-weight:700;margin-bottom:4px">💎 POSITION: ${shares} SHARES</div>
                <div style="font-size:12px;opacity:0.9">Risk: $100 | Profit Potential: $${profit.toFixed(2)}</div>
            </div>
            
            <div style="background:#1f2937;border:2px solid #fbbf24;padding:16px;border-radius:12px;margin-bottom:16px">
                <div style="font-size:14px;font-weight:700;color:#fbbf24;margin-bottom:8px">🎯 STEP-BY-STEP EXECUTION:</div>
                <div style="font-size:12px;line-height:1.6">
                    <div style="margin:4px 0;padding:4px 0">1️⃣ Change quantity to <strong>${shares} shares</strong></div>
                    <div style="margin:4px 0;padding:4px 0">2️⃣ Set limit price to <strong>$${entry.toFixed(2)}</strong></div>
                    <div style="margin:4px 0;padding:4px 0">3️⃣ Click <strong>"Simulated Buy"</strong></div>
                    <div style="margin:4px 0;padding:4px 0">4️⃣ Set stop-loss at <strong>$${stop.toFixed(2)}</strong></div>
                    <div style="margin:4px 0;padding:4px 0">5️⃣ Set target at <strong>$${target.toFixed(2)}</strong></div>
                </div>
            </div>
            
            <div style="background:linear-gradient(135deg,#8b5cf6,#7c3aed);padding:16px;border-radius:12px;text-align:center;cursor:pointer" onclick="alert('Ready to execute! Follow the 5 steps above in your Webull trading panel.')">
                <div style="font-size:14px;font-weight:800;margin-bottom:4px">🚀 READY TO EXECUTE</div>
                <div style="font-size:11px;opacity:0.9">Click here when you're ready for live guidance</div>
            </div>
        </div>
    </div>`;
    
    document.body.appendChild(ui);
})();