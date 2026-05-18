#!/usr/bin/env python3
"""
Kalshi Market Monitor
Tracks markets for profit opportunities
"""

import requests
import json
import time
import logging
from datetime import datetime, timedelta
import schedule

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kalshi_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class KalshiMonitor:
    def __init__(self, config_path='config.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.base_url = self.config['kalshi']['base_url']
        self.session = requests.Session()
        self.opportunities = []
        
    def get_markets(self):
        """Fetch current markets from Kalshi"""
        try:
            # This would need actual Kalshi API endpoints
            # For now, using placeholder structure
            url = f"{self.base_url}markets"
            response = self.session.get(url)
            
            if response.status_code == 200:
                return response.json().get('markets', [])
            else:
                logger.error(f"Failed to fetch markets: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching markets: {e}")
            return []
    
    def analyze_market(self, market):
        """Analyze a market for opportunities"""
        opportunities = []
        
        # Check for high-volume sudden changes
        volume = market.get('volume', 0)
        price_change = market.get('price_change_24h', 0)
        
        if volume > self.config['monitoring']['min_volume']:
            if abs(price_change) > self.config['monitoring']['min_probability_change']:
                opportunities.append({
                    'type': 'volume_spike',
                    'market': market['title'],
                    'volume': volume,
                    'price_change': price_change,
                    'current_price': market.get('yes_price', 0),
                    'timestamp': datetime.now().isoformat()
                })
        
        # Check for undervalued/overvalued markets
        yes_price = market.get('yes_price', 50)
        implied_prob = yes_price / 100
        
        # Simple heuristic - look for extreme prices
        if yes_price < 10 or yes_price > 90:
            opportunities.append({
                'type': 'extreme_pricing',
                'market': market['title'],
                'yes_price': yes_price,
                'implied_probability': implied_prob,
                'timestamp': datetime.now().isoformat()
            })
        
        return opportunities
    
    def scan_markets(self):
        """Main scanning function"""
        logger.info("🔍 Scanning Kalshi markets...")
        
        markets = self.get_markets()
        all_opportunities = []
        
        for market in markets:
            opportunities = self.analyze_market(market)
            all_opportunities.extend(opportunities)
        
        if all_opportunities:
            logger.info(f"💡 Found {len(all_opportunities)} opportunities!")
            self.send_alerts(all_opportunities)
            
        self.opportunities.extend(all_opportunities)
        return all_opportunities
    
    def send_alerts(self, opportunities):
        """Send alerts via Discord/Telegram"""
        for opp in opportunities:
            message = self.format_alert(opp)
            logger.info(f"🚨 ALERT: {message}")
            
            # Send to Discord if configured
            discord_webhook = self.config['alerts'].get('discord_webhook')
            if discord_webhook:
                self.send_discord_alert(message, discord_webhook)
    
    def format_alert(self, opportunity):
        """Format opportunity as alert message"""
        if opportunity['type'] == 'volume_spike':
            return (
                f"📈 VOLUME SPIKE: {opportunity['market']}\n"
                f"Volume: {opportunity['volume']:,}\n"
                f"Price Change: {opportunity['price_change']:.1%}\n"
                f"Current Price: ${opportunity['current_price']:.2f}"
            )
        elif opportunity['type'] == 'extreme_pricing':
            return (
                f"🎯 EXTREME PRICING: {opportunity['market']}\n"
                f"Yes Price: ${opportunity['yes_price']:.2f}\n"
                f"Implied Prob: {opportunity['implied_probability']:.1%}"
            )
    
    def send_discord_alert(self, message, webhook_url):
        """Send alert to Discord"""
        try:
            payload = {
                "content": f"🤖 **Kalshi Alert**\n```\n{message}\n```"
            }
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 204:
                logger.info("✅ Discord alert sent")
            else:
                logger.error(f"❌ Discord alert failed: {response.status_code}")
        except Exception as e:
            logger.error(f"Error sending Discord alert: {e}")
    
    def run_continuous(self):
        """Run continuous monitoring"""
        logger.info("🚀 Starting continuous monitoring...")
        
        # Schedule scans every minute
        schedule.every(1).minutes.do(self.scan_markets)
        
        # Schedule daily summary
        schedule.every().day.at("09:00").do(self.daily_summary)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(10)
        except KeyboardInterrupt:
            logger.info("👋 Monitoring stopped by user")
    
    def daily_summary(self):
        """Generate daily summary of opportunities"""
        today_opps = [
            opp for opp in self.opportunities
            if datetime.fromisoformat(opp['timestamp']).date() == datetime.now().date()
        ]
        
        logger.info(f"📊 Daily Summary: {len(today_opps)} opportunities found")
        
        # Group by type
        by_type = {}
        for opp in today_opps:
            opp_type = opp['type']
            if opp_type not in by_type:
                by_type[opp_type] = []
            by_type[opp_type].append(opp)
        
        for opp_type, opps in by_type.items():
            logger.info(f"  {opp_type}: {len(opps)} alerts")

if __name__ == "__main__":
    monitor = KalshiMonitor()
    
    # Single scan for testing
    print("🧪 Running single market scan...")
    opportunities = monitor.scan_markets()
    
    if opportunities:
        print(f"Found {len(opportunities)} opportunities!")
        for i, opp in enumerate(opportunities, 1):
            print(f"{i}. {monitor.format_alert(opp)}")
    else:
        print("No opportunities found in this scan.")
    
    # Ask if user wants continuous monitoring
    response = input("\nStart continuous monitoring? (y/n): ").lower()
    if response == 'y':
        monitor.run_continuous()