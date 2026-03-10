javascript:(function(){
  'use strict';
  
  // ============================================
  // JARVIS TRADING COPILOT v3.0 - GPT-5.4 ENHANCED
  // Universal stock detection, smart calculations, pro-level guidance
  // ============================================
  
  // Configuration
  const CONFIG = {
    RISK_PER_TRADE: 100,
    STOP_LOSS_PERCENT: 0.03,
    PROFIT_TARGET_PERCENT: 0.08,
    MAX_SCAN_RETRIES: 5,
    SCAN_INTERVAL: 800,
    UPDATE_FREQUENCY: 2000
  };
  
  // State management
  let state = {
    isActive: true,
    detectedPosition: null,
    detectedOrders: [],
    currentStep: 'detect', // detect, analyze, buy, wait_fill, set_stop, set_target, monitor
    scanAttempts: 0,
    lastUpdate: null,
    ui: null
  };
  
  // Kill existing instance
  const existing = document.getElementById('jarvis-copilot-v3');
  if (existing) {
    existing.remove();
    window.jarvisState = null;
  }
  
  if (window.jarvisInterval) clearInterval(window.jarvisInterval);
  if (window.jarvisUpdateInterval) clearInterval(window.jarvisUpdateInterval);
  
  // ============================================
  // STOCK SYMBOL DETECTION ENGINE
  // ============================================
  
  function detectSymbols() {
    const symbols = [];
    const seen = new Set();
    
    // Pattern 1: Look in URLs
    const urlPatterns = window.location.pathname.match(/\/(stock|trade|positions|orders)\/([A-Z]{1,5})/gi);
    if (urlPatterns) {
      urlPatterns.forEach(match => {
        const symbol = match.split('/').pop().toUpperCase();
        if (!seen.has(symbol) && isValidSymbol(symbol)) {
          symbols.push({ symbol, source: 'url' });
          seen.add(symbol);
        }
      });
    }
    
    // Pattern 2: Page title
    const titleMatch = document.title.match(/\b([A-Z]{2,5})\b/);
    if (titleMatch && !seen.has(titleMatch[1]) && isValidSymbol(titleMatch[1])) {
      symbols.push({ symbol: titleMatch[1], source: 'title' });
      seen.add(titleMatch[1]);
    }
    
    // Pattern 3: DOM content scanning
    const bodyText = document.body.innerText;
    const symbolRegex = /\b(AAPL|TSLA|NVDA|MSFT|GOOGL|AMZN|META|NFLX|AMD|INTC|JPM|BAC|DIS|UBER|COIN|PLTR|SOFI|HOOD|NVAX|PFE|XOM|CVX|WMT|HD|TGT|LOW|COST|NKE|LULU|SHOP|CRM|ORCL|ADBE|INTU|ROKU|PENN|DKNG|TWLO|NET|CRWD|SNOW|DDOG|PLUG|QS|SPCE|RKLB|ASTS|ABNB|DASH|UPST|LCID|RIVN|F|GM|V|MA|PYPL|SQ|ADYEN|SE|CPNG|MELI|JD|BABA|PDD|NTES|TCOM|BIDU|TME|IQ|HUYA|DOYU|FUTU|TIGR)\b/g;
    const matches = bodyText.match(symbolRegex);
    if (matches) {
      matches.forEach(symbol => {
        if (!seen.has(symbol)) {
          symbols.push({ symbol, source: 'dom' });
          seen.add(symbol);
        }
      });
    }
    
    // Pattern 4: Look for data attributes
    const dataElements = document.querySelectorAll('[data-symbol], [data-ticker], [data-stock], [testid*="symbol"], [class*="ticker"], [class*="symbol"]');
    dataElements.forEach(el => {
      const text = el.textContent || el.getAttribute('data-symbol') || el.getAttribute('data-ticker');
      if (text) {
        const match = text.match(/\b([A-Z]{1,5})\b/);
        if (match && !seen.has(match[1]) && isValidSymbol(match[1])) {
          symbols.push({ symbol: match[1], source: 'data-attr' });
          seen.add(match[1]);
        }
      }
    });
    
    return symbols;
  }
  
  function isValidSymbol(str) {
    return /^[A-Z]{1,5}$/.test(str) && !['THE','AND','FOR','ARE','BUT','NOT'].includes(str);
  }
  
  // ============================================
  // PRICE DETECTION ENGINE
  // ============================================
  
  function detectPrice(symbol) {
    const bodyText = document.body.innerText;
    const bodyHTML = document.body.innerHTML;
    let price = null;
    
    // Strategy 1: Look near symbol in text
    const symbolIndex = bodyText.indexOf(symbol);
    if (symbolIndex > -1) {
      const nearbyText = bodyText.substring(symbolIndex - 200, symbolIndex + 400);
      const priceMatch = nearbyText.match(/\$?(\d{1,4}\.\d{2})/);
      if (priceMatch && isReasonablePrice(parseFloat(priceMatch[1]))) {
        price = parseFloat(priceMatch[1]);
      }
    }
    
    // Strategy 2: Search for price patterns with $ symbol
    if (!price) {
      const dollarPrices = bodyText.match(/\$(\d{1,4}\.\d{2})/g);
      if (dollarPrices) {
        const parsed = dollarPrices.map(p => parseFloat(p.replace('$', '')));
        const valid = parsed.filter(p => isReasonablePrice(p));
        if (valid.length > 0) {
          // Take the most common price or first reasonable one
          price = valid[0];
        }
      }
    }
    
    // Strategy 3: Look in data attributes
    if (!price) {
      const priceElements = document.querySelectorAll('[data-price], [data-last], [data-current], [testid*="price"]');
      for (let el of priceElements) {
        const text = el.textContent || el.getAttribute('data-price');
        const match = text && text.match(/(\d{1,4}\.\d{2})/);
        if (match) {
          const p = parseFloat(match[1]);
          if (isReasonablePrice(p)) {
            price = p;
            break;
          }
        }
      }
    }
    
    // Strategy 4: Look at input fields
    if (!price) {
      const inputs = document.querySelectorAll('input[type="text"], input[type="number"]');
      for (let input of inputs) {
        const val = input.value;
        if (val && val.match(/^\d{1,4}\.\d{2}$/)) {
          const p = parseFloat(val);
          if (isReasonablePrice(p)) {
            price = p;
            break;
          }
        }
      }
    }
    
    return price;
  }
  
  function isReasonablePrice(price) {
    return price >= 0.50 && price <= 50000;
  }
  
  // ============================================
  // POSITION DETECTION ENGINE
  // ============================================
  
  function detectPositions() {
    const positions = [];
    const bodyText = document.body.innerText.toLowerCase();
    
    // Look for position indicators
    const positionIndicators = [
      /position|positions|holdings|portfolio|owned|shares/i,
      /qty|quantity|# of shares/i,
      /avg cost|entry|bought at/i
    ];
    
    // Scan tables
    const tables = document.querySelectorAll('table');
    for (let table of tables) {
      const headers = table.querySelectorAll('th, thead td');
      const headerText = Array.from(headers).map(h => h.textContent.toLowerCase()).join(' ');
      
      if (headerText.includes('symbol') || headerText.includes('ticker') || 
          headerText.includes('position') || headerText.includes('qty')) {
        const rows = table.querySelectorAll('tbody tr, tr');
        for (let row of rows) {
          const cells = row.querySelectorAll('td');
          if (cells.length >= 2) {
            const rowText = row.textContent;
            const symbolMatch = rowText.match(/\b([A-Z]{1,5})\b/);
            const qtyMatch = rowText.match(/\b(\d{1,6})\s*(shares?|qty)?\b/i);
            const priceMatch = rowText.match(/\$?(\d{1,4}\.\d{2})/);
            
            if (symbolMatch) {
              positions.push({
                symbol: symbolMatch[1],
                shares: qtyMatch ? parseInt(qtyMatch[1]) : 0,
                avgPrice: priceMatch ? parseFloat(priceMatch[1]) : null,
                isReal: false // detected, not confirmed
              });
            }
          }
        }
      }
    }
    
    // Look for "You own X shares" text patterns
    const ownPatterns = bodyText.match(/(you own|position|have)\s+(\d+)\s+(shares? of|of)?\s+([a-z]+)/i);
    if (ownPatterns) {
      positions.push({
        symbol: ownPatterns[4].toUpperCase(),
        shares: parseInt(ownPatterns[2]),
        isReal: true
      });
    }
    
    return positions;
  }
  
  // ============================================
  // ORDER DETECTION ENGINE
  // ============================================
  
  function detectOrders() {
    const orders = [];
    const bodyText = document.body.innerText.toLowerCase();
    
    // Look for active orders
    const hasWorkingOrders = bodyText.includes('working') || bodyText.includes('pending') || 
                           bodyText.includes('open order');
    
    if (hasWorkingOrders) {
      // Scan for order tables
      const tables = document.querySelectorAll('table');
      for (let table of tables) {
        if (table.textContent.toLowerCase().includes('order')) {
          const rows = table.querySelectorAll('tr');
          for (let row of rows) {
            const text = row.textContent;
            if (text.toLowerCase().includes('stop') || text.toLowerCase().includes('limit')) {
              const type = text.toLowerCase().includes('stop') ? 'stop' : 'limit';
              const priceMatch = text.match(/\$?(\d{1,4}\.\d{2})/);
              const symbolMatch = text.match(/\b([A-Z]{1,5})\b/);
              
              if (priceMatch) {
                orders.push({
                  type: type,
                  price: parseFloat(priceMatch[1]),
                  symbol: symbolMatch ? symbolMatch[1] : null,
                  status: 'active'
                });
              }
            }
          }
        }
      }
    }
    
    return orders;
  }
  
  // ============================================
  // TRADE CALCULATION ENGINE
  // ============================================
  
  function calculateTrade(entryPrice) {
    if (!entryPrice || entryPrice <= 0) return null;
    
    const stopLoss = entryPrice * (1 - CONFIG.STOP_LOSS_PERCENT);
    const profitTarget = entryPrice * (1 + CONFIG.PROFIT_TARGET_PERCENT);
    const riskPerShare = entryPrice - stopLoss;
    
    if (riskPerShare <= 0) return null;
    
    const shares = Math.floor(CONFIG.RISK_PER_TRADE / riskPerShare);
    const totalCost = shares * entryPrice;
    const potentialProfit = shares * (profitTarget - entryPrice);
    const potentialLoss = shares * riskPerShare;
    
    return {
      entryPrice: entryPrice,
      stopLoss: stopLoss,
      profitTarget: profitTarget,
      riskPerShare: riskPerShare,
      shares: shares,
      totalCost: totalCost,
      potentialProfit: potentialProfit,
      potentialLoss: potentialLoss,
      riskRewardRatio: (profitTarget - entryPrice) / riskPerShare,
      stopPercent: CONFIG.STOP_LOSS_PERCENT * 100,
      targetPercent: CONFIG.PROFIT_TARGET_PERCENT * 100
    };
  }
  
  // ============================================
  // SMART STATE ANALYSIS
  // ============================================
  
  function analyzeCurrentState() {
    const symbols = detectSymbols();
    const price = symbols.length > 0 ? detectPrice(symbols[0].symbol) : null;
    const positions = detectPositions();
    const orders = detectOrders();
    
    // Determine scenario
    let scenario = 'new_analysis';
    let activePosition = null;
    let activeOrders = { stop: null, target: null };
    
    // Check if we have a filled position
    if (positions.length > 0) {
      const ownPosition = positions.find(p => p.shares > 0);
      if (ownPosition) {
        scenario = 'position_owned';
        activePosition = ownPosition;
        
        // Check for protective orders
        orders.forEach(order => {
          if (order.symbol === ownPosition.symbol) {
            if (order.type === 'stop' && order.price < ownPosition.avgPrice) {
              activeOrders.stop = order;
            } else if (order.type === 'limit' && order.price > ownPosition.avgPrice) {
              activeOrders.target = order;
            }
          }
        });
        
        // Determine what step we're on
        if (!activeOrders.stop) {
          scenario = 'needs_stop_loss';
        } else if (!activeOrders.target) {
          scenario = 'needs_profit_target';
        } else {
          scenario = 'fully_protected';
        }
      }
    }
    
    // Calculate trade if we have a price
    let tradeCalc = null;
    if (price) {
      tradeCalc = calculateTrade(price);
    }
    
    return {
      symbols: symbols,
      detectedPrice: price,
      positions: positions,
      orders: orders,
      scenario: scenario,
      activePosition: activePosition,
      activeOrders: activeOrders,
      tradeCalc: tradeCalc,
      timestamp: new Date()
    };
  }
  
  // ============================================
  // UI CREATION
  // ============================================
  
  function createUI() {
    const container = document.createElement('div');
    container.id = 'jarvis-copilot-v3';
    container.style.cssText = `
      position: fixed !important;
      top: 15px !important;
      right: 15px !important;
      width: 380px !important;
      max-height: calc(100vh - 30px) !important;
      overflow-y: auto !important;
      background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
      border: 2px solid #22c55e !important;
      border-radius: 16px !important;
      color: white !important;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
      z-index: 2147483647 !important;
      box-shadow: 0 25px 50px -12px rgba(0,0,0,0.9), 0 0 0 1px rgba(34,197,94,0.3) !important;
      font-size: 13px !important;
      line-height: 1.5 !important;
    `;
    
    container.innerHTML = `
      <div id="jv-header" style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); padding: 14px 16px; border-radius: 14px 14px 0 0; display: flex; justify-content: space-between; align-items: center;">
        <div>
          <div style="font-size: 16px; font-weight: 800; color: #000; letter-spacing: -0.5px;">🤖 JARVIS COPILOT</div>
          <div style="font-size: 10px; color: #064e3b; font-weight: 600; margin-top: 2px;">PRO TRADING ASSISTANT v3.0</div>
        </div>
        <div style="display: flex; gap: 6px;">
          <button id="jv-minimize" style="background: rgba(0,0,0,0.2); border: none; color: #000; width: 28px; height: 28px; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 800;">−</button>
          <button id="jv-close" style="background: rgba(0,0,0,0.2); border: none; color: #000; width: 28px; height: 28px; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 800;">×</button>
        </div>
      </div>
      
      <div id="jv-content" style="padding: 16px;">
        <!-- Content injected by updateUI() -->
      </div>
      
      <div style="background: rgba(0,0,0,0.3); padding: 8px 16px; border-radius: 0 0 14px 14px; border-top: 1px solid rgba(255,255,255,0.1);">
        <div style="font-size: 9px; color: #64748b; text-align: center;">
          Risk: $${CONFIG.RISK_PER_TRADE}/trade • Stop: ${CONFIG.STOP_LOSS_PERCENT * 100}% • Target: ${CONFIG.PROFIT_TARGET_PERCENT * 100}%
        </div>
      </div>
    `;
    
    document.body.appendChild(container);
    
    // Event listeners
    document.getElementById('jv-close').addEventListener('click', () => {
      container.remove();
      state.isActive = false;
      clearInterval(window.jarvisInterval);
      clearInterval(window.jarvisUpdateInterval);
    });
    
    document.getElementById('jv-minimize').addEventListener('click', () => {
      const content = document.getElementById('jv-content');
      if (content.style.display === 'none') {
        content.style.display = 'block';
      } else {
        content.style.display = 'none';
      }
    });
    
    return container;
  }
  
  // ============================================
  // UI UPDATE BASED ON STATE
  // ============================================
  
  function updateUI(analysis) {
    if (!state.ui) return;
    
    const content = document.getElementById('jv-content');
    if (!content) return;
    
    let html = '';
    
    // Detection Status
    html += `<div style="background: rgba(34,197,94,0.1); border: 1px solid rgba(34,197,94,0.3); padding: 12px; border-radius: 10px; margin-bottom: 12px;">`;
    html += `<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">`;
    html += `<div style="width: 8px; height: 8px; background: #22c55e; border-radius: 50%; animation: pulse 1s infinite;"></div>`;
    html += `<span style="font-size: 11px; font-weight: 700; color: #22c55e;">LIVE SCANNING WEBULL</span>`;
    html += `</div>`;
    
    if (analysis.detectedPrice && analysis.symbols.length > 0) {
      html += `<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">`;
      html += `<div style="background: rgba(0,0,0,0.2); padding: 8px; border-radius: 6px;">`;
      html += `<div style="font-size: 9px; color: #94a3b8;">TICKER</div>`;
      html += `<div style="font-size: 18px; font-weight: 900; color: #22c55e;">${analysis.symbols[0].symbol}</div>`;
      html += `</div>`;
      html += `<div style="background: rgba(0,0,0,0.2); padding: 8px; border-radius: 6px;">`;
      html += `<div style="font-size: 9px; color: #94a3b8;">PRICE</div>`;
      html += `<div style="font-size: 18px; font-weight: 900; color: #22c55e;">$${analysis.detectedPrice.toFixed(2)}</div>`;
      html += `</div>`;
      html += `</div>`;
    } else {
      html += `<div style="text-align: center; padding: 8px;">`;
      html += `<div style="font-size: 10px; color: #94a3b8;">🔍 Scanning for stock data...</div>`;
      html += `<div style="font-size: 9px; color: #64748b; margin-top: 4px;">Open a stock detail page</div>`;
      html += `</div>`;
    }
    html += `</div>`;
    
    // Trade Calculator
    if (analysis.tradeCalc) {
      const tc = analysis.tradeCalc;
      html += `<div style="background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.3); padding: 12px; border-radius: 10px; margin-bottom: 12px;">`;
      html += `<div style="font-size: 11px; font-weight: 700; color: #3b82f6; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">`;
      html += `<span>📊</span> TRADE CALCULATION`;
      html += `</div>`;
      
      html += `<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 10px; margin-bottom: 8px;">`;
      html += `<div style="background: rgba(0,0,0,0.2); padding: 6px; border-radius: 5px;"><div style="color: #94a3b8;">Entry</div><div style="font-weight: 700;">$${tc.entryPrice.toFixed(2)}</div></div>`;
      html += `<div style="background: rgba(0,0,0,0.2); padding: 6px; border-radius: 5px;"><div style="color: #94a3b8;">Shares</div><div style="font-weight: 700; color: #22c55e;">${tc.shares}</div></div>`;
      html += `<div style="background: rgba(239,68,68,0.2); padding: 6px; border-radius: 5px;"><div style="color: #fca5a5;">Stop</div><div style="font-weight: 700; color: #ef4444;">$${tc.stopLoss.toFixed(2)}</div></div>`;
      html += `<div style="background: rgba(34,197,94,0.2); padding: 6px; border-radius: 5px;"><div style="color: #86efac;">Target</div><div style="font-weight: 700; color: #22c55e;">$${tc.profitTarget.toFixed(2)}</div></div>`;
      html += `</div>`;
      
      html += `<div style="display: flex; justify-content: space-between; background: rgba(0,0,0,0.2); padding: 8px; border-radius: 5px; font-size: 9px;">`;
      html += `<div><div style="color: #94a3b8;">Total Cost</div><div style="font-weight: 700;">$${tc.totalCost.toFixed(2)}</div></div>`;
      html += `<div style="text-align: right;"><div style="color: #94a3b8;">Risk/Reward</div><div style="font-weight: 700; color: #fbbf24;">1:${tc.riskRewardRatio.toFixed(1)}</div></div>`;
      html += `</div>`;
      html += `</div>`;
    }
    
    // Action Steps Based on Scenario
    html += `<div style="background: rgba(139,92,246,0.1); border: 1px solid rgba(139,92,246,0.3); padding: 12px; border-radius: 10px;">`;
    html += `<div style="font-size: 11px; font-weight: 700; color: #8b5cf6; margin-bottom: 10px;">🎯 NEXT ACTIONS</div>`;
    
    if (analysis.scenario === 'new_analysis') {
      html += `<div style="font-size: 10px; color: #e2e8f0; line-height: 1.6;">`;
      html += `<div style="margin-bottom: 6px;"><strong style="color: #22c55e;">1.</strong> Navigate to a stock in Webull</div>`;
      html += `<div style="margin-bottom: 6px;"><strong style="color: #22c55e;">2.</strong> Click "Buy" button</div>`;
      html += `<div style="margin-bottom: 6px;"><strong style="color: #22c55e;">3.</strong> Set limit order at calculated entry price</div>`;
      html += `<div><strong style="color: #22c55e;">4.</strong> Enter shares from calculation above</div>`;
      html += `</div>`;
    } else if (analysis.scenario === 'needs_stop_loss') {
      html += `<div style="background: rgba(239,68,68,0.2); border: 1px solid rgba(239,68,68,0.4); padding: 10px; border-radius: 6px; font-size: 10px;">`;
      html += `<div style="color: #fca5a5; font-weight: 700; margin-bottom: 6px;">⚠️ CRITICAL: Set Stop-Loss Now!</div>`;
      html += `<div style="color: #e2e8f0; margin-bottom: 8px;">You own ${analysis.activePosition.shares} shares but have NO protection!</div>`;
      html += `<div style="color: #94a3b8; font-size: 9px;">`;
      html += `→ Click "Sell" next to ${analysis.activePosition.symbol}<br>`;
      html += `→ Order Type: STOP LIMIT<br>`;
      html += `→ Stop Price: $${(analysis.activePosition.avgPrice * 0.97).toFixed(2)}<br>`;
      html += `→ Limit Price: $${(analysis.activePosition.avgPrice * 0.965).toFixed(2)}`;
      html += `</div>`;
      html += `</div>`;
    } else if (analysis.scenario === 'needs_profit_target') {
      html += `<div style="background: rgba(34,197,94,0.2); border: 1px solid rgba(34,197,94,0.4); padding: 10px; border-radius: 6px; font-size: 10px;">`;
      html += `<div style="color: #86efac; font-weight: 700; margin-bottom: 6px;">✅ Stop-loss set! Set profit target:</div>`;
      html += `<div style="color: #94a3b8; font-size: 9px;">`;
      html += `→ Create new SELL order<br>`;
      html += `→ Order Type: LIMIT<br>`;
      html += `→ Limit Price: $${(analysis.activePosition.avgPrice * 1.08).toFixed(2)}<br>`;
      html += `→ Quantity: ${analysis.activePosition.shares}`;
      html += `</div>`;
      html += `</div>`;
    } else if (analysis.scenario === 'fully_protected') {
      html += `<div style="background: rgba(34,197,94,0.3); border: 1px solid rgba(34,197,94,0.5); padding: 10px; border-radius: 6px; font-size: 10px;">`;
      html += `<div style="color: #22c55e; font-weight: 700; margin-bottom: 6px;">🛡️ FULLY PROTECTED</div>`;
      html += `<div style="color: #e2e8f0;">`;
      html += `✅ Position: ${analysis.activePosition.shares} shares<br>`;
      html += `✅ Stop-loss: ACTIVE<br>`;
      html += `✅ Profit target: ACTIVE<br>`;
      html += `📊 Monitor in My Positions tab`;
      html += `</div>`;
      html += `</div>`;
    }
    
    html += `</div>`;
    
    // Refresh button
    html += `<button id="jv-refresh" style="width: 100%; margin-top: 10px; background: linear-gradient(135deg, #6366f1, #8b5cf6); border: none; color: white; padding: 10px; border-radius: 8px; cursor: pointer; font-weight: 700; font-size: 11px; display: flex; align-items: center; justify-content: center; gap: 6px;">`;
    html += `🔄 SCAN WEBULL AGAIN`;
    html += `</button>`;
    
    content.innerHTML = html;
    
    // Add refresh handler
    const refreshBtn = document.getElementById('jv-refresh');
    if (refreshBtn) {
      refreshBtn.addEventListener('click', () => {
        state.scanAttempts = 0;
        runAnalysis();
      });
    }
  }
  
  // ============================================
  // MAIN ANALYSIS LOOP
  // ============================================
  
  function runAnalysis() {
    if (!state.isActive) return;
    
    const analysis = analyzeCurrentState();
    updateUI(analysis);
    
    state.scanAttempts++;
    
    // Keep scanning until we find price or max attempts
    if (!analysis.detectedPrice && state.scanAttempts < CONFIG.MAX_SCAN_RETRIES) {
      console.log(`[Jarvis] Scan attempt ${state.scanAttempts}/${CONFIG.MAX_SCAN_RETRIES}`);
    }
  }
  
  // ============================================
  // INITIALIZE
  // ============================================
  
  function init() {
    console.log('🤖 JARVIS COPILOT v3.0 Initializing...');
    
    // Create UI
    state.ui = createUI();
    
    // Initial analysis
    runAnalysis();
    
    // Set up intervals
    window.jarvisInterval = setInterval(() => {
      if (state.scanAttempts < CONFIG.MAX_SCAN_RETRIES) {
        runAnalysis();
      }
    }, CONFIG.SCAN_INTERVAL);
    
    // Continuous updates for active positions
    window.jarvisUpdateInterval = setInterval(() => {
      runAnalysis();
    }, CONFIG.UPDATE_FREQUENCY);
    
    // Expose for debugging
    window.jarvisState = state;
    window.jarvisAnalyze = runAnalysis;
    
    console.log('🤖 JARVIS COPILOT v3.0 ACTIVE - Scanning Webull...');
  }
  
  // Start
  init();
  
})();