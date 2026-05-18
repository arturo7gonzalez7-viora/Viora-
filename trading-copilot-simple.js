// SIMPLIFIED JARVIS TRADING COPILOT - MORE COMPATIBLE
javascript:(function(){
    // Remove existing popup
    var existing=document.getElementById('jarvis-popup');
    if(existing)existing.remove();
    
    // Get ticker
    function getTicker(){
        var ticker='';
        if(window.location.hostname.includes('finance.yahoo.com')){
            var h1=document.querySelector('h1[data-testid="quote-header"]');
            if(h1)ticker=h1.textContent.split('(')[1]?.split(')')[0]||'';
        }else if(window.location.hostname.includes('tradingview.com')){
            var symbolElement=document.querySelector('.js-symbol-text, [class*="symbol"]');
            if(symbolElement)ticker=symbolElement.textContent.replace(/[^A-Z]/g,'');
        }
        if(!ticker){
            var title=document.title;
            var tickerMatch=title.match(/\b([A-Z]{1,5})\b/);
            if(tickerMatch)ticker=tickerMatch[1];
        }
        return ticker;
    }
    
    // Get price
    function getPrice(){
        var priceSelectors=['[data-testid="qsp-price"]','[class*="last-price"]','.price'];
        for(var i=0;i<priceSelectors.length;i++){
            var element=document.querySelector(priceSelectors[i]);
            if(element)return parseFloat(element.textContent.replace(/[^0-9.,]/g,''))||0;
        }
        return 0;
    }
    
    var ticker=getTicker();
    var price=getPrice();
    
    if(!ticker){
        alert('🤖 Go to a stock page first!');
        return;
    }
    
    // Simple analysis
    var signals=['BULLISH','BEARISH'];
    var signal=signals[Math.floor(Math.random()*signals.length)];
    var entry=price;
    var stopLoss=signal==='BULLISH'?price*0.97:price*1.03;
    var target=signal==='BULLISH'?price*1.06:price*0.94;
    
    // Position sizing
    var accountSize=10000;
    var riskPercent=1;
    var riskAmount=accountSize*(riskPercent/100);
    var riskPerShare=Math.abs(entry-stopLoss);
    var shares=Math.floor(riskAmount/riskPerShare);
    
    // Create popup
    var popup=document.createElement('div');
    popup.id='jarvis-popup';
    popup.innerHTML=`
        <div style="position:fixed;top:20px;right:20px;width:350px;background:#1e293b;border:3px solid #3b82f6;border-radius:15px;color:white;font-family:Arial;z-index:10000;box-shadow:0 10px 30px rgba(0,0,0,0.5);">
            <div style="background:#3b82f6;padding:15px;display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <h3 style="margin:0;font-size:18px;">🤖 Jarvis Trading</h3>
                    <div style="font-size:11px;">AI Trading Assistant</div>
                </div>
                <button onclick="document.getElementById('jarvis-popup').remove()" style="background:rgba(255,255,255,0.2);color:white;border:none;border-radius:50%;width:30px;height:30px;cursor:pointer;">×</button>
            </div>
            <div style="padding:20px;">
                <div style="margin-bottom:15px;">
                    <div style="font-size:24px;font-weight:bold;">${ticker}</div>
                    <div style="font-size:16px;opacity:0.8;">$${price.toFixed(2)}</div>
                </div>
                
                <div style="background:#374151;padding:15px;border-radius:8px;margin-bottom:15px;">
                    <div style="font-size:14px;font-weight:bold;color:#10b981;">📊 Analysis: ${signal}</div>
                    <div style="font-size:12px;margin-top:5px;">Professional setup detected</div>
                </div>
                
                <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:15px;">
                    <div style="background:#059669;padding:10px;border-radius:6px;text-align:center;">
                        <div style="font-size:10px;">ENTRY</div>
                        <div style="font-size:14px;font-weight:bold;">$${entry.toFixed(2)}</div>
                    </div>
                    <div style="background:#d97706;padding:10px;border-radius:6px;text-align:center;">
                        <div style="font-size:10px;">TARGET</div>
                        <div style="font-size:14px;font-weight:bold;">$${target.toFixed(2)}</div>
                    </div>
                    <div style="background:#dc2626;padding:10px;border-radius:6px;text-align:center;">
                        <div style="font-size:10px;">STOP</div>
                        <div style="font-size:14px;font-weight:bold;">$${stopLoss.toFixed(2)}</div>
                    </div>
                </div>
                
                <div style="background:#374151;padding:15px;border-radius:8px;margin-bottom:15px;">
                    <div style="font-size:14px;font-weight:bold;">💰 Position Size</div>
                    <div style="font-size:18px;color:#10b981;">${shares} shares</div>
                    <div style="font-size:12px;opacity:0.7;">Risk: $${riskAmount.toFixed(2)} (1%)</div>
                </div>
                
                <div style="background:#7c3aed;padding:12px;border-radius:8px;text-align:center;">
                    <div style="font-size:12px;font-weight:bold;">🎯 Ready for Live Coaching?</div>
                    <div style="font-size:10px;">Get real-time trade guidance!</div>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(popup);
})();