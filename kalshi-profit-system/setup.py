#!/usr/bin/env python3
"""
Kalshi Profit System Setup
Configures APIs and dependencies
"""

import subprocess
import sys
import os

def setup_web_search():
    """Configure Brave Search API for market research"""
    print("🔍 Setting up web search...")
    print("You need a Brave Search API key from: https://api.search.brave.com/")
    
    api_key = input("Enter your Brave Search API key (or skip to configure later): ").strip()
    
    if api_key:
        # Configure via OpenClaw
        cmd = f'openclaw configure --section web --set brave_api_key={api_key}'
        try:
            subprocess.run(cmd, shell=True, check=True)
            print("✅ Brave Search API configured!")
        except subprocess.CalledProcessError:
            print("❌ Failed to configure API. Run manually:")
            print(f"openclaw configure --section web --set brave_api_key={api_key}")
    else:
        print("⏭️ Skipping web search setup. Configure later with:")
        print("openclaw configure --section web")

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    
    packages = [
        'requests',
        'beautifulsoup4', 
        'tweepy',
        'pandas',
        'numpy',
        'schedule',
        'python-telegram-bot',
        'websockets',
        'aiohttp'
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")

def create_config():
    """Create configuration file"""
    config = '''
{
  "kalshi": {
    "base_url": "https://kalshi.com/api/",
    "username": "",
    "password": "",
    "demo_mode": true
  },
  "alerts": {
    "discord_webhook": "",
    "telegram_bot_token": "",
    "telegram_chat_id": ""
  },
  "monitoring": {
    "check_interval": 60,
    "min_volume": 1000,
    "min_probability_change": 0.05
  },
  "strategy": {
    "max_position_size": 0.1,
    "stop_loss": 0.2,
    "take_profit": 0.3
  }
}
'''
    
    with open('config.json', 'w') as f:
        f.write(config)
    print("✅ Created config.json - edit with your settings")

if __name__ == "__main__":
    print("🚀 Setting up Kalshi Profit System...")
    
    setup_web_search()
    install_dependencies() 
    create_config()
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Edit config.json with your Kalshi credentials")
    print("2. Run: python monitor.py")
    print("3. Set up alerts in Discord/Telegram")