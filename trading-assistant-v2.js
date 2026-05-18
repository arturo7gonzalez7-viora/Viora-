// Trading Assistant Bookmarklet v2.0 - Enhanced UI & Beginner-Friendly
javascript:(function(){
    function getTicker(){
        let ticker='';
        if(window.location.hostname.includes('finance.yahoo.com')){
            const h1=document.querySelector('h1[data-testid="quote-header"]');
            if(h1){ticker=h1.textContent.split('(')[1]?.split(')')[0]||'';}
        }else if(window.location.hostname.includes('tradingview.com')){
            const symbolElement=document.querySelector('.js-symbol-text, [class*="symbol"]');
            if(symbolElement){ticker=symbolElement.textContent.replace(/[^A-Z]/g,'');}
        }else if(window.location.hostname.includes('robinhood.com')){
            const pathParts=window.location.pathname.split('/');
            const stockIndex=pathParts.indexOf('stocks');
            if(stockIndex!==-1&&pathParts[stockIndex+1]){ticker=pathParts[stockIndex+1].toUpperCase();}
        }
        if(!ticker){
            const title=document.title;
            const tickerMatch=title.match(/\b([A-Z]{1,5})\b/);
            if(tickerMatch){ticker=tickerMatch[1];}
        }
        return ticker;
    }
    
    function getCurrentPrice(){
        const priceSelectors=['[data-testid="qsp-price"]','[class*="last-price"]','.price','[data-testid="price"]'];
        for(let selector of priceSelectors){
            const element=document.querySelector(selector);
            if(element){return element.textContent.replace(/[^0-9.,]/g,'');}
        }
        return 'N/A';
    }
    
    const ticker=getTicker();
    const price=getCurrentPrice();
    
    if(!ticker){
        alert('🤖 Go to a stock page first (like Apple, Tesla, etc.)');
        return;
    }
    
    // Remove any existing popup
    const existing=document.getElementById('jarvis-trading-popup-v2');
    if(existing){existing.remove();}
    
    const popup=document.createElement('div');
    popup.id='jarvis-trading-popup-v2';
    popup.innerHTML=`
        <div style="
            position:fixed;
            top:15px;
            right:15px;
            width:380px;
            background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border:none;
            border-radius:20px;
            padding:0;
            z-index:10000;
            box-shadow:0 20px 40px rgba(0,0,0,0.3);
            font-family:'Segoe UI',Arial,sans-serif;
            color:white;
            overflow:hidden;
        ">
            <!-- Header -->
            <div style="
                background:rgba(255,255,255,0.1);
                padding:20px;
                display:flex;
                justify-content:space-between;
                align-items:center;
                backdrop-filter:blur(10px);
            ">
                <div>
                    <h2 style="margin:0;font-size:24px;font-weight:bold;">🤖 Jarvis</h2>
                    <div style="font-size:12px;opacity:0.8;">Your Trading Copilot</div>
                </div>
                <button onclick="document.getElementById('jarvis-trading-popup-v2').remove()" style="
                    background:rgba(255,255,255,0.2);
                    color:white;
                    border:none;
                    border-radius:50%;
                    width:35px;
                    height:35px;
                    cursor:pointer;
                    font-size:18px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                ">×</button>
            </div>
            
            <!-- Stock Info -->
            <div style="padding:20px;background:rgba(255,255,255,0.05);">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:15px;">
                    <div>
                        <div style="font-size:28px;font-weight:bold;">${ticker}</div>
                        <div style="font-size:16px;opacity:0.8;">$${price}</div>
                    </div>
                    <div style="
                        background:rgba(76,175,80,0.3);
                        padding:8px 16px;
                        border-radius:20px;
                        font-size:14px;
                        border:1px solid rgba(76,175,80,0.5);
                    ">📈 Swing Trade</div>
                </div>
            </div>
            
            <!-- Analysis Content -->
            <div style="padding:20px;">
                <h3 style="margin:0 0 15px 0;font-size:18px;color:#4CAF50;">💡 Beginner-Friendly Analysis</h3>
                
                <div style="background:rgba(255,255,255,0.1);padding:15px;border-radius:12px;margin-bottom:15px;">
                    <div style="font-size:16px;margin-bottom:10px;"><strong>What This Means:</strong></div>
                    <div style="font-size:14px;line-height:1.5;opacity:0.9;">
                        ${ticker} looks decent for a swing trade (hold 1-2 weeks). Not financial advice - just what the patterns suggest!
                    </div>
                </div>
                
                <!-- Trading Plan -->
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:15px;">
                    <div style="background:rgba(76,175,80,0.2);padding:12px;border-radius:8px;text-align:center;">
                        <div style="font-size:12px;opacity:0.8;">💰 RISK ONLY</div>
                        <div style="font-size:18px;font-weight:bold;">$50-100</div>
                        <div style="font-size:11px;">Money you can lose</div>
                    </div>
                    <div style="background:rgba(255,193,7,0.2);padding:12px;border-radius:8px;text-align:center;">
                        <div style="font-size:12px;opacity:0.8;">🎯 TARGET</div>
                        <div style="font-size:18px;font-weight:bold;">+10-15%</div>
                        <div style="font-size:11px;">Realistic profit</div>
                    </div>
                </div>
                
                <!-- Action Steps -->
                <div style="background:rgba(255,255,255,0.1);padding:15px;border-radius:12px;margin-bottom:15px;">
                    <div style="font-size:14px;font-weight:bold;margin-bottom:8px;">🎯 Action Plan:</div>
                    <div style="font-size:13px;line-height:1.6;">
                        1. Only use "fun money" you can afford to lose<br>
                        2. Set a stop-loss at -5% (sell if it drops)<br>
                        3. Take profit around +10-15%<br>
                        4. Don't get greedy - profit is profit!
                    </div>
                </div>
                
                <!-- Warning -->
                <div style="
                    background:rgba(255,152,0,0.2);
                    border:1px solid rgba(255,152,0,0.4);
                    padding:12px;
                    border-radius:8px;
                    font-size:12px;
                    text-align:center;
                    margin-bottom:15px;
                ">
                    ⚠️ This is demo mode. Real AI analysis coming soon!<br>
                    Never risk money you can't afford to lose.
                </div>
                
                <!-- Action Buttons -->
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                    <button onclick="
                        navigator.clipboard.writeText('${ticker} - Jarvis says decent swing trade setup. Risk $50-100 max, target +10-15%, stop at -5%');
                        this.innerHTML='✅ Copied!';
                        setTimeout(()=>this.innerHTML='📋 Copy Analysis',2000);
                    " style="
                        background:rgba(76,175,80,0.3);
                        color:white;
                        border:1px solid rgba(76,175,80,0.5);
                        padding:12px;
                        border-radius:8px;
                        cursor:pointer;
                        font-size:12px;
                        font-weight:bold;
                    ">📋 Copy Analysis</button>
                    
                    <button onclick="
                        window.open('https://finance.yahoo.com/quote/${ticker}/chart','_blank');
                    " style="
                        background:rgba(33,150,243,0.3);
                        color:white;
                        border:1px solid rgba(33,150,243,0.5);
                        padding:12px;
                        border-radius:8px;
                        cursor:pointer;
                        font-size:12px;
                        font-weight:bold;
                    ">📊 View Chart</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(popup);
})();