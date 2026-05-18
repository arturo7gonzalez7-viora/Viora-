// Trading Assistant Bookmarklet v1.0
// Extracts ticker from current page and gets AI analysis

javascript:(function(){
    // Extract ticker from various trading platforms
    function getTicker() {
        let ticker = '';
        
        // Yahoo Finance
        if (window.location.hostname.includes('finance.yahoo.com')) {
            const h1 = document.querySelector('h1[data-testid="quote-header"]');
            if (h1) {
                ticker = h1.textContent.split('(')[1]?.split(')')[0] || '';
            }
        }
        
        // TradingView
        else if (window.location.hostname.includes('tradingview.com')) {
            const symbolElement = document.querySelector('.js-symbol-text, [class*="symbol"]');
            if (symbolElement) {
                ticker = symbolElement.textContent.replace(/[^A-Z]/g, '');
            }
        }
        
        // Robinhood
        else if (window.location.hostname.includes('robinhood.com')) {
            const pathParts = window.location.pathname.split('/');
            const stockIndex = pathParts.indexOf('stocks');
            if (stockIndex !== -1 && pathParts[stockIndex + 1]) {
                ticker = pathParts[stockIndex + 1].toUpperCase();
            }
        }
        
        // Webull
        else if (window.location.hostname.includes('webull.com')) {
            const tickerElement = document.querySelector('[data-testid="stock-symbol"]');
            if (tickerElement) {
                ticker = tickerElement.textContent.trim();
            }
        }
        
        // Generic fallback - look for ticker patterns in title/url
        if (!ticker) {
            const title = document.title;
            const tickerMatch = title.match(/\b([A-Z]{1,5})\b/);
            if (tickerMatch) {
                ticker = tickerMatch[1];
            }
        }
        
        return ticker;
    }
    
    // Get current price if available
    function getCurrentPrice() {
        const priceSelectors = [
            '[data-testid="qsp-price"]', // Yahoo Finance
            '[class*="last-price"]', // TradingView
            '.price', // Generic
            '[data-testid="price"]' // Generic
        ];
        
        for (let selector of priceSelectors) {
            const element = document.querySelector(selector);
            if (element) {
                return element.textContent.replace(/[^0-9.,]/g, '');
            }
        }
        return 'N/A';
    }
    
    const ticker = getTicker();
    const price = getCurrentPrice();
    
    if (!ticker) {
        alert('Could not detect ticker symbol on this page. Try visiting a stock page first.');
        return;
    }
    
    // Create analysis popup
    const popup = document.createElement('div');
    popup.id = 'jarvis-trading-popup';
    popup.innerHTML = `
        <div style="position: fixed; top: 20px; right: 20px; width: 350px; background: white; border: 2px solid #4CAF50; border-radius: 10px; padding: 20px; z-index: 10000; box-shadow: 0 4px 20px rgba(0,0,0,0.3); font-family: Arial, sans-serif;">
            <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 15px;">
                <h3 style="margin: 0; color: #333;">🤖 Jarvis Analysis</h3>
                <button onclick="document.getElementById('jarvis-trading-popup').remove()" style="background: #ff4444; color: white; border: none; border-radius: 50%; width: 25px; height: 25px; cursor: pointer; float: right;">×</button>
            </div>
            <div style="margin-bottom: 10px;">
                <strong>Stock:</strong> ${ticker}<br>
                <strong>Price:</strong> $${price}
            </div>
            <div id="analysis-content" style="background: #f5f5f5; padding: 10px; border-radius: 5px; min-height: 100px;">
                <div style="text-align: center; padding: 20px;">
                    <div style="border: 2px solid #4CAF50; border-radius: 50%; border-top: 2px solid transparent; width: 30px; height: 30px; animation: spin 1s linear infinite; margin: 0 auto 10px;"></div>
                    Analyzing ${ticker}...
                </div>
            </div>
            <style>
                @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            </style>
        </div>
    `;
    
    document.body.appendChild(popup);
    
    // Simulate getting analysis (for now, we'll use placeholder)
    // In real version, this would call OpenClaw API
    setTimeout(() => {
        const analysisDiv = document.getElementById('analysis-content');
        if (analysisDiv) {
            analysisDiv.innerHTML = `
                <div style="color: #333;">
                    <div style="margin-bottom: 10px;">
                        <strong style="color: #4CAF50;">📈 Quick Analysis:</strong><br>
                        Technical setup looks decent for ${ticker}
                    </div>
                    <div style="margin-bottom: 10px;">
                        <strong>💰 Position Size:</strong> $50-100 max<br>
                        <strong>🎯 Target:</strong> +8-12%<br>
                        <strong>🛑 Stop Loss:</strong> -5%
                    </div>
                    <div style="background: #fff3cd; padding: 8px; border-radius: 4px; font-size: 12px;">
                        ⚠️ This is demo mode. Real analysis coming soon!
                    </div>
                    <button onclick="navigator.clipboard.writeText('${ticker} - Jarvis says decent setup for swing trade')" style="background: #4CAF50; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; width: 100%; margin-top: 10px;">
                        📋 Copy Analysis
                    </button>
                </div>
            `;
        }
    }, 2000);
    
})();