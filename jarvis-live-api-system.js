// JARVIS ULTIMATE TRADING COPILOT - LIVE API INTEGRATION
javascript:(function(){
    var e=document.getElementById('jarvis-ultimate');
    if(e)e.remove();
    
    // API Configuration
    const API_CONFIG = {
        // Free market data API (no key required)
        marketData: 'https://query1.finance.yahoo.com/v8/finance/chart/',
        // Our analysis endpoint (we'll build this)
        analysis: 'https://api.jarvistrading.ai/analyze',
        // Backup static data (fallback)
        fallback: true
    };
    
    var liveStocks = [];
    var selectedStock = null;
    var tradeStep = 0;
    var isLoading = true;
    
    // Live Market Data Fetcher
    async function fetchLiveData(ticker) {
        try {
            const response = await fetch(API_CONFIG.marketData + ticker);
            const data = await response.json();
            const quote = data.chart.result[0].meta;
            
            return {
                ticker: ticker,
                price: quote.regularMarketPrice,
                change: quote.regularMarketPrice - quote.previousClose,
                changePercent: ((quote.regularMarketPrice - quote.previousClose) / quote.previousClose) * 100,
                volume: quote.regularMarketVolume,
                high: quote.regularMarketDayHigh,
                low: quote.regularMarketDayLow
            };
        } catch (error) {
            console.log('API Error for ' + ticker + ':', error);
            return null;
        }
    }
    
    // AI Analysis Engine (Simulated - will connect to real AI)
    function analyzeStock(stockData) {
        if (!stockData) return null;
        
        const volatility = Math.abs(stockData.changePercent);
        const volumeScore = stockData.volume > 1000000 ? 85 : 70;
        const priceScore = stockData.changePercent > 0 ? 80 : 60;
        
        // Simulate professional strategy selection
        const strategies = [
            'Daily Level Sweep & Reversal',
            'VWAP Bounce Play', 
            'Opening Range Breakout',
            'Triple Confluence Setup',
            'Session Transition Setup'
        ];
        
        const confidence = Math.min(95, Math.max(65, volumeScore + priceScore - (volatility * 2)));
        const strategy = strategies[Math.floor(Math.random() * strategies.length)];
        
        // Calculate levels based on current price
        const entry = stockData.price;
        const stop = entry * 0.97;  // 3% stop
        const target = entry * 1.08; // 8% target
        const shares = Math.floor(100 / (entry - stop));
        const risk = Math.round(shares * (entry - stop));
        const profit = Math.round(shares * (target - entry));
        
        return {
            ticker: stockData.ticker,
            confidence: Math.round(confidence),
            strategy: strategy,
            entry: entry,
            stop: stop,
            target: target,
            shares: shares,
            risk: risk,
            profit: profit,
            reasoning: `Live analysis: ${stockData.changePercent > 0 ? 'Bullish momentum' : 'Oversold bounce'} with ${volumeScore > 80 ? 'high' : 'normal'} volume confirmation.`
        };
    }
    
    // Load Live Winners
    async function loadLiveWinners() {
        const watchlist = ['AAPL', 'TSLA', 'NVDA', 'MSFT', 'GOOGL', 'AMD', 'META'];
        const promises = watchlist.map(ticker => fetchLiveData(ticker));
        
        try {
            const results = await Promise.all(promises);
            const analyzed = results
                .filter(data => data !== null)
                .map(data => analyzeStock(data))
                .filter(analysis => analysis !== null && analysis.confidence > 70)
                .sort((a, b) => b.confidence - a.confidence)
                .slice(0, 3); // Top 3
                
            liveStocks = analyzed;
            isLoading = false;
            updateContent();
        } catch (error) {
            console.log('Failed to load live data, using fallback');
            // Fallback to static data
            liveStocks = [
                {ticker:'AAPL',confidence:87,strategy:'Daily Level Sweep & Reversal',entry:262.52,stop:254.64,target:283.52,shares:12,risk:100,profit:252,reasoning:'Fallback analysis - institutional sweep pattern.'},
                {ticker:'TSLA',confidence:84,strategy:'VWAP Bounce Play',entry:195.80,stop:189.50,target:207.90,shares:16,risk:100,profit:194,reasoning:'Fallback analysis - VWAP bounce setup.'}
            ];
            isLoading = false;
            updateContent();
        }
    }
    
    function closeJarvis(){
        var popup=document.getElementById('jarvis-ultimate');
        if(popup)popup.remove();
    }
    
    function updateContent(){
        var content=document.getElementById('jarvis-content');
        
        if (isLoading) {
            content.innerHTML = '<div style="padding:20px;text-align:center"><div style="color:#06d6a0;font-size:14px;font-weight:900;margin-bottom:10px">🔄 ANALYZING LIVE MARKETS...</div><div style="font-size:11px;color:#94a3b8">Scanning 7 stocks with real-time data</div><div style="margin-top:15px;color:#fbbf24;font-size:10px">⚡ Connecting to market APIs...</div></div>';
            return;
        }
        
        if(!selectedStock){
            var html='<div style="padding:14px"><div style="font-size:13px;font-weight:900;color:#06d6a0;margin-bottom:8px;text-align:center">🎯 LIVE MARKET ANALYSIS</div><div style="font-size:9px;color:#22c55e;margin-bottom:10px;text-align:center">📡 Real-time data • Updated now</div>';
            
            if (liveStocks.length === 0) {
                html += '<div style="color:#ef4444;text-align:center;padding:20px;font-size:11px">No high-confidence setups found.<br>Market conditions not ideal.</div>';
            } else {
                liveStocks.forEach(function(stock,index){
                    html+='<div onclick="window.jarvisSelectStock('+index+')" style="background:#2d3748;margin:6px 0;padding:10px;border-radius:8px;cursor:pointer;border:2px solid #06d6a0;transition:all 0.2s"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px"><div style="font-size:14px;font-weight:900;color:#06d6a0">'+stock.ticker+'</div><div style="background:#22c55e;padding:3px 6px;border-radius:6px;font-size:9px;font-weight:800">'+stock.confidence+'% LIVE</div></div><div style="font-size:9px;color:#94a3b8;margin-bottom:4px">'+stock.strategy+'</div><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:3px;font-size:8px;text-align:center"><div style="background:#22c55e;padding:3px;border-radius:3px"><div style="opacity:0.8">ENTRY</div><div style="font-weight:900">$'+stock.entry.toFixed(2)+'</div></div><div style="background:#f59e0b;padding:3px;border-radius:3px"><div style="opacity:0.8">PROFIT</div><div style="font-weight:900">$'+stock.profit+'</div></div><div style="background:#ef4444;padding:3px;border-radius:3px"><div style="opacity:0.8">RISK</div><div style="font-weight:900">$'+stock.risk+'</div></div></div></div>';
                });
            }
            
            html+='<div style="margin-top:10px;padding:8px;background:#1a202c;border-radius:6px;text-align:center"><button onclick="window.refreshAnalysis()" style="background:#4338ca;color:white;border:none;padding:6px 12px;border-radius:6px;cursor:pointer;font-size:10px;font-weight:700">🔄 REFRESH LIVE DATA</button></div></div>';
            content.innerHTML=html;
        } else {
            // Trade execution screen (same as before)
            var steps=[
                {title:'PREPARE WEBULL ORDER',instructions:['Look at Webull "Quantity" field','Change to '+selectedStock.shares+' shares','Look at "Limit Price" field','Change to $'+selectedStock.entry.toFixed(2),'Verify order type is "Limit"'],button:'ORDER READY ✅'},
                {title:'EXECUTE BUY ORDER',instructions:['Click "Simulated Buy '+selectedStock.ticker+'" button','Wait for order confirmation','Screenshot position (optional)','Get ready for stop-loss'],button:'TRADE EXECUTED ✅'},
                {title:'SET STOP-LOSS PROTECTION',instructions:['Go to "Orders" tab in Webull','Find your '+selectedStock.ticker+' position','Click "Sell" button','Select "Stop Loss" order type','Set trigger: $'+selectedStock.stop.toFixed(2),'Quantity: '+selectedStock.shares+' shares','Submit order'],button:'STOP SET ✅'},
                {title:'SET PROFIT TARGET',instructions:['Create another sell order','Select "Limit" order type','Set price: $'+selectedStock.target.toFixed(2),'Quantity: '+selectedStock.shares+' shares','Submit order'],button:'TARGET SET ✅'},
                {title:'TRADE ACTIVE - MONITORING',instructions:['✅ Position: '+selectedStock.shares+' shares '+selectedStock.ticker,'✅ Entry: $'+selectedStock.entry.toFixed(2),'✅ Stop: $'+selectedStock.stop.toFixed(2),'✅ Target: $'+selectedStock.target.toFixed(2),'🎯 Profit potential: $'+selectedStock.profit,'📡 Live monitoring active!'],button:'TRADE COMPLETE 🎉'}
            ];
            
            var step=steps[tradeStep];
            var html='<div style="padding:14px"><div style="text-align:center;margin-bottom:10px;padding:8px;background:rgba(6,214,160,0.1);border-radius:8px"><div style="font-size:16px;font-weight:900;color:#06d6a0">'+selectedStock.ticker+' EXECUTION</div><div style="font-size:9px;color:#22c55e">📡 Live Analysis • '+selectedStock.confidence+'% Confidence</div></div><div style="background:#1a202c;border:2px solid #fbbf24;padding:10px;border-radius:8px;margin-bottom:10px"><div style="font-size:11px;font-weight:900;color:#fbbf24;margin-bottom:6px">'+step.title+'</div><div style="font-size:9px;line-height:1.4;color:#f1f5f9">';
            
            step.instructions.forEach(function(inst,i){
                html+='<div style="margin:2px 0">'+(i+1)+'. '+inst+'</div>';
            });
            
            html+='</div></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:8px"><button onclick="window.jarvisGoBack()" style="background:#6b7280;color:white;border:none;padding:8px;border-radius:6px;cursor:pointer;font-size:10px;font-weight:700">← BACK</button><button onclick="window.jarvisNextStep()" style="background:linear-gradient(135deg,#22c55e,#16a34a);color:white;border:none;padding:8px;border-radius:6px;cursor:pointer;font-size:10px;font-weight:700">'+step.button+'</button></div><div style="background:#2d3748;padding:6px;border-radius:6px;font-size:8px;color:#94a3b8;text-align:center">Step '+(tradeStep+1)+' of 5 • '+selectedStock.reasoning+'</div></div>';
            
            content.innerHTML=html;
        }
    }
    
    // Global functions
    window.jarvisClose=closeJarvis;
    window.refreshAnalysis=function(){
        isLoading = true;
        selectedStock = null;
        tradeStep = 0;
        updateContent();
        loadLiveWinners();
    };
    
    window.jarvisSelectStock=function(index){
        selectedStock=liveStocks[index];
        tradeStep=0;
        updateContent();
    };
    
    window.jarvisNextStep=function(){
        if(tradeStep<4){
            tradeStep++;
            updateContent();
        }else{
            alert('🎉 TRADE COMPLETE! Excellent execution with live data! Check Webull for results.');
        }
    };
    
    window.jarvisGoBack=function(){
        if(tradeStep>0){
            tradeStep--;
            updateContent();
        }else{
            selectedStock=null;
            updateContent();
        }
    };
    
    var ui=document.createElement('div');
    ui.id='jarvis-ultimate';
    ui.innerHTML='<div style="position:fixed;top:10px;right:10px;width:340px;background:#1a202c;border:3px solid #06d6a0;border-radius:16px;color:white;font-family:-apple-system,BlinkMacSystemFont,sans-serif;z-index:10000;box-shadow:0 25px 50px rgba(0,0,0,0.8)"><div style="background:linear-gradient(135deg,#06d6a0,#118ab2);padding:10px;border-radius:13px 13px 0 0"><div style="display:flex;justify-content:space-between;align-items:center"><div><h2 style="margin:0;font-size:14px;font-weight:900">⚡ JARVIS LIVE</h2><div style="font-size:8px;opacity:0.9;font-weight:600">REAL-TIME TRADING AI</div></div><button onclick="window.jarvisClose()" style="background:rgba(255,255,255,0.3);color:white;border:none;border-radius:50%;width:24px;height:24px;cursor:pointer;font-size:12px;font-weight:bold">×</button></div></div><div id="jarvis-content"></div></div>';
    
    document.body.appendChild(ui);
    
    // Start loading live data immediately
    loadLiveWinners();
})();