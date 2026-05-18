#!/usr/bin/env python3
"""
Breaking News Alert System
Detects news that could impact Kalshi markets
"""

import requests
import json
import time
import logging
from datetime import datetime, timedelta
import hashlib
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsMonitor:
    def __init__(self, config_path='config.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.seen_articles = set()
        self.market_keywords = self.load_market_keywords()
        
    def load_market_keywords(self):
        """Keywords that indicate tradeable news"""
        return {
            'politics': [
                'election', 'vote', 'poll', 'candidate', 'primary', 
                'biden', 'trump', 'congress', 'senate', 'house'
            ],
            'economics': [
                'fed', 'interest rate', 'inflation', 'gdp', 'unemployment',
                'recession', 'jobs report', 'powell', 'federal reserve'
            ],
            'weather': [
                'hurricane', 'storm', 'tornado', 'flood', 'earthquake',
                'wildfire', 'heat wave', 'blizzard', 'drought'
            ],
            'tech': [
                'apple', 'google', 'microsoft', 'tesla', 'ai', 'openai',
                'cryptocurrency', 'bitcoin', 'stock market crash'
            ],
            'sports': [
                'super bowl', 'world series', 'olympics', 'championship',
                'trade', 'draft', 'injury', 'playoffs'
            ]
        }
    
    def get_breaking_news(self):
        """Fetch latest breaking news"""
        news_sources = [
            {
                'name': 'Reuters',
                'url': 'https://www.reuters.com/arc/outboundfeeds/rss/',
                'type': 'rss'
            },
            {
                'name': 'AP News',
                'url': 'https://apnews.com/rss',
                'type': 'rss'
            },
            # Add more sources as needed
        ]
        
        all_articles = []
        for source in news_sources:
            try:
                articles = self.fetch_from_source(source)
                all_articles.extend(articles)
            except Exception as e:
                logger.error(f"Failed to fetch from {source['name']}: {e}")
        
        return all_articles
    
    def fetch_from_source(self, source):
        """Fetch articles from a news source"""
        # This is a simplified implementation
        # In reality, you'd parse RSS feeds or use news APIs
        
        try:
            response = requests.get(source['url'], timeout=10)
            if response.status_code == 200:
                # Parse RSS or JSON depending on source type
                # For now, return mock data structure
                return [{
                    'title': 'Sample breaking news',
                    'url': 'https://example.com',
                    'published': datetime.now().isoformat(),
                    'source': source['name']
                }]
            return []
        except Exception as e:
            logger.error(f"Error fetching from {source['url']}: {e}")
            return []
    
    def analyze_article(self, article):
        """Analyze article for market relevance"""
        title = article['title'].lower()
        content = article.get('content', '').lower()
        text = f"{title} {content}"
        
        relevant_categories = []
        
        # Check each category for keyword matches
        for category, keywords in self.market_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in text)
            if matches > 0:
                relevant_categories.append({
                    'category': category,
                    'matches': matches,
                    'keywords_found': [kw for kw in keywords if kw in text]
                })
        
        return relevant_categories
    
    def generate_trading_suggestions(self, article, categories):
        """Generate trading suggestions based on news"""
        suggestions = []
        
        for cat in categories:
            if cat['category'] == 'politics':
                suggestions.append({
                    'market_type': 'Election outcomes',
                    'suggestion': 'Check candidate prediction markets for impact',
                    'urgency': 'high',
                    'keywords': cat['keywords_found']
                })
            
            elif cat['category'] == 'economics':
                suggestions.append({
                    'market_type': 'Fed rates / Inflation',
                    'suggestion': 'Trade rate decision and economic indicator markets',
                    'urgency': 'medium',
                    'keywords': cat['keywords_found']
                })
            
            elif cat['category'] == 'weather':
                suggestions.append({
                    'market_type': 'Weather events',
                    'suggestion': 'Check disaster/weather prediction markets',
                    'urgency': 'high',
                    'keywords': cat['keywords_found']
                })
        
        return suggestions
    
    def process_news_batch(self):
        """Process latest news for trading opportunities"""
        logger.info("📰 Fetching breaking news...")
        
        articles = self.get_breaking_news()
        opportunities = []
        
        for article in articles:
            # Skip if we've already processed this article
            article_hash = hashlib.md5(article['title'].encode()).hexdigest()
            if article_hash in self.seen_articles:
                continue
            
            self.seen_articles.add(article_hash)
            
            # Analyze for market relevance
            categories = self.analyze_article(article)
            
            if categories:
                suggestions = self.generate_trading_suggestions(article, categories)
                
                opportunity = {
                    'type': 'news_driven',
                    'article': article,
                    'categories': categories,
                    'suggestions': suggestions,
                    'timestamp': datetime.now().isoformat()
                }
                
                opportunities.append(opportunity)
                logger.info(f"📈 Trading opportunity from: {article['title']}")
        
        return opportunities
    
    def format_news_alert(self, opportunity):
        """Format news opportunity as alert"""
        article = opportunity['article']
        suggestions = opportunity['suggestions']
        
        alert = f"🚨 NEWS ALERT: {article['title']}\n"
        alert += f"Source: {article['source']}\n"
        alert += f"URL: {article['url']}\n\n"
        
        alert += "💡 TRADING SUGGESTIONS:\n"
        for i, suggestion in enumerate(suggestions, 1):
            alert += f"{i}. {suggestion['market_type']}: {suggestion['suggestion']}\n"
            alert += f"   Urgency: {suggestion['urgency'].upper()}\n"
        
        return alert
    
    def send_news_alert(self, opportunity):
        """Send news-based trading alert"""
        alert = self.format_news_alert(opportunity)
        logger.info(f"📢 {alert}")
        
        # Send to Discord if configured
        discord_webhook = self.config['alerts'].get('discord_webhook')
        if discord_webhook:
            try:
                payload = {"content": f"```\n{alert}\n```"}
                response = requests.post(discord_webhook, json=payload)
                if response.status_code == 204:
                    logger.info("✅ News alert sent to Discord")
            except Exception as e:
                logger.error(f"Failed to send Discord alert: {e}")
    
    def monitor_continuous(self):
        """Run continuous news monitoring"""
        logger.info("🔍 Starting continuous news monitoring...")
        
        try:
            while True:
                opportunities = self.process_news_batch()
                
                for opp in opportunities:
                    self.send_news_alert(opp)
                
                # Wait 2 minutes between checks
                time.sleep(120)
                
        except KeyboardInterrupt:
            logger.info("👋 News monitoring stopped")

if __name__ == "__main__":
    monitor = NewsMonitor()
    
    # Test run
    print("🧪 Testing news monitoring...")
    opportunities = monitor.process_news_batch()
    
    if opportunities:
        print(f"Found {len(opportunities)} news-driven opportunities!")
        for opp in opportunities:
            print(monitor.format_news_alert(opp))
            print("-" * 50)
    else:
        print("No relevant news found in this batch.")
    
    # Ask for continuous monitoring
    response = input("\nStart continuous news monitoring? (y/n): ").lower()
    if response == 'y':
        monitor.monitor_continuous()