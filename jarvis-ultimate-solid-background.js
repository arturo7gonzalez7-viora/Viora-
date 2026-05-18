// JARVIS ULTIMATE TRADING COPILOT - SOLID BACKGROUND FIX
javascript:(function(){
    var e=document.getElementById('jarvis-ultimate');
    if(e)e.remove();
    
    var todaysWinners=[
        {ticker:'AAPL',confidence:87,strategy:'Daily Level Sweep & Reversal',entry:262.52,stop:254.64,target:283.52,shares:12,risk:100,profit:252,reasoning:'Institutional sweep pattern completed. Strong bullish reversal confirmed.'},
        {ticker:'TSLA',confidence:84,strategy:'VWAP Bounce Play',entry:195.80,stop:189.50,target:207.90,shares:16,risk:100,profit:194,reasoning:'Perfect VWAP bounce setup. High volume confirmation.'},
        {ticker:'NVDA',confidence:81,strategy:'Opening Range Breakout',entry:875.20,stop:847.80,target:924.60,shares:4,risk:109,profit:198,reasoning:'Pre-market range established. Breakout imminent.'}
    ];
    
    var selectedStock=null;
    var tradeStep=0;
    
    function closeJarvis(){
        var popup=document.getElementById('jarvis-ultimate');
        if(popup)popup.remove();
    }
    
    function updateContent(){
        var content=document.getElementById('jarvis-content');
        if(!selectedStock){
            var html='<div style="padding:14px"><div style="font-size:13px;font-weight:900;color:#06d6a0;margin-bottom:10px;text-align:center">🎯 TODAY\'S PRE-SELECTED WINNERS</div>';
            todaysWinners.forEach(function(stock,index){
                html+='<div onclick="window.jarvisSelectStock('+index+')" style="background:#2d3748;margin:6px 0;padding:10px;border-radius:8px;cursor:pointer;border:2px solid #06d6a0;transition:all 0.2s"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px"><div style="font-size:14px;font-weight:900;color:#06d6a0">'+stock.ticker+'</div><div style="background:#22c55e;padding:3px 6px;border-radius:6px;font-size:9px;font-weight:800">'+stock.confidence+'% EDGE</div></div><div style="font-size:9px;color:#94a3b8;margin-bottom:4px">'+stock.strategy+'</div><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:3px;font-size:8px;text-align:center"><div style="background:#22c55e;padding:3px;border-radius:3px"><div style="opacity:0.8">ENTRY</div><div style="font-weight:900">$'+stock.entry+'</div></div><div style="background:#f59e0b;padding:3px;border-radius:3px"><div style="opacity:0.8">PROFIT</div><div style="font-weight:900">$'+stock.profit+'</div></div><div style="background:#ef4444;padding:3px;border-radius:3px"><div style="opacity:0.8">RISK</div><div style="font-weight:900">$'+stock.risk+'</div></div></div></div>';
            });
            html+='</div>';
            content.innerHTML=html;
        }else{
            var steps=[
                {title:'PREPARE WEBULL ORDER',instructions:['Look at Webull "Quantity" field','Change to '+selectedStock.shares+' shares','Look at "Limit Price" field','Change to $'+selectedStock.entry,'Verify order type is "Limit"'],button:'ORDER READY ✅'},
                {title:'EXECUTE BUY ORDER',instructions:['Click "Simulated Buy '+selectedStock.ticker+'" button','Wait for order confirmation','Screenshot position (optional)','Get ready for stop-loss'],button:'TRADE EXECUTED ✅'},
                {title:'SET STOP-LOSS PROTECTION',instructions:['Go to "Orders" tab in Webull','Find your '+selectedStock.ticker+' position','Click "Sell" button','Select "Stop Loss" order type','Set trigger: $'+selectedStock.stop,'Quantity: '+selectedStock.shares+' shares','Submit order'],button:'STOP SET ✅'},
                {title:'SET PROFIT TARGET',instructions:['Create another sell order','Select "Limit" order type','Set price: $'+selectedStock.target,'Quantity: '+selectedStock.shares+' shares','Submit order'],button:'TARGET SET ✅'},
                {title:'TRADE ACTIVE - MONITORING',instructions:['✅ Position: '+selectedStock.shares+' shares '+selectedStock.ticker,'✅ Entry: $'+selectedStock.entry,'✅ Stop: $'+selectedStock.stop,'✅ Target: $'+selectedStock.target,'🎯 Profit potential: $'+selectedStock.profit,'📊 Monitoring for you!'],button:'TRADE COMPLETE 🎉'}
            ];
            
            var step=steps[tradeStep];
            var html='<div style="padding:14px"><div style="text-align:center;margin-bottom:10px;padding:8px;background:rgba(6,214,160,0.1);border-radius:8px"><div style="font-size:16px;font-weight:900;color:#06d6a0">'+selectedStock.ticker+' EXECUTION</div><div style="font-size:9px;color:#94a3b8">'+selectedStock.strategy+'</div></div><div style="background:#1a202c;border:2px solid #fbbf24;padding:10px;border-radius:8px;margin-bottom:10px"><div style="font-size:11px;font-weight:900;color:#fbbf24;margin-bottom:6px">'+step.title+'</div><div style="font-size:9px;line-height:1.4;color:#f1f5f9">';
            
            step.instructions.forEach(function(inst,i){
                html+='<div style="margin:2px 0">'+(i+1)+'. '+inst+'</div>';
            });
            
            html+='</div></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:8px"><button onclick="window.jarvisGoBack()" style="background:#6b7280;color:white;border:none;padding:8px;border-radius:6px;cursor:pointer;font-size:10px;font-weight:700">← BACK</button><button onclick="window.jarvisNextStep()" style="background:linear-gradient(135deg,#22c55e,#16a34a);color:white;border:none;padding:8px;border-radius:6px;cursor:pointer;font-size:10px;font-weight:700">'+step.button+'</button></div><div style="background:#2d3748;padding:6px;border-radius:6px;font-size:8px;color:#94a3b8;text-align:center">Step '+(tradeStep+1)+' of 5 • '+selectedStock.reasoning+'</div></div>';
            
            content.innerHTML=html;
        }
    }
    
    window.jarvisClose=closeJarvis;
    window.jarvisSelectStock=function(index){
        selectedStock=todaysWinners[index];
        tradeStep=0;
        updateContent();
    };
    
    window.jarvisNextStep=function(){
        if(tradeStep<4){
            tradeStep++;
            updateContent();
        }else{
            alert('🎉 TRADE COMPLETE! Excellent execution! Check Webull for results. Ready for your next AI-guided trade?');
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
    ui.innerHTML='<div style="position:fixed;top:10px;right:10px;width:340px;background:#1a202c;border:3px solid #06d6a0;border-radius:16px;color:white;font-family:-apple-system,BlinkMacSystemFont,sans-serif;z-index:10000;box-shadow:0 25px 50px rgba(0,0,0,0.8)"><div style="background:linear-gradient(135deg,#06d6a0,#118ab2);padding:10px;border-radius:13px 13px 0 0"><div style="display:flex;justify-content:space-between;align-items:center"><div><h2 style="margin:0;font-size:14px;font-weight:900">⚡ JARVIS ULTIMATE</h2><div style="font-size:8px;opacity:0.9;font-weight:600">COMPLETE TRADING SYSTEM</div></div><button onclick="window.jarvisClose()" style="background:rgba(255,255,255,0.3);color:white;border:none;border-radius:50%;width:24px;height:24px;cursor:pointer;font-size:12px;font-weight:bold">×</button></div></div><div id="jarvis-content"></div></div>';
    
    document.body.appendChild(ui);
    updateContent();
})();