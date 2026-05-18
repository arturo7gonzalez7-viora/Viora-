#!/usr/bin/env python3
"""
Facebook Messenger Automation for Steven's Real Estate Leads
Handles automated responses and follow-up sequences
"""

import json
import time
from datetime import datetime, timedelta

class MessengerAutomation:
    def __init__(self):
        self.hot_lead_triggers = [
            'yes', 'interested', 'call me', 'tell me more', 
            'how much', 'cash offer', 'when', 'asap', 'quickly'
        ]
        
    def generate_instant_message(self, lead_data):
        """Generate personalized instant response message"""
        name = lead_data.get('first_name', 'there')
        address = lead_data.get('property_address', 'your property')
        situation = lead_data.get('situation', '')
        
        message = f"""Hi {name}! 👋

Thanks for reaching out about your property at {address}. I'm Steven's assistant helping coordinate property evaluations.

Steven specializes in helping Colorado homeowners sell quickly without the hassle of repairs, showings, or realtor fees.

Here's what happens next:
✅ Steven will review your property details today
✅ You'll get a fair cash offer within 24-48 hours  
✅ If you accept, we can close as fast as 7 days

Quick question - what's the main reason you're looking to sell? This helps Steven prepare the best possible offer for your situation.

Looking forward to helping you! 🏠"""
        
        return message
    
    def get_follow_up_message(self, follow_up_number, lead_data):
        """Generate follow-up messages based on sequence"""
        name = lead_data.get('first_name', 'there')
        address = lead_data.get('property_address', 'your property')
        
        messages = {
            1: f"""Hi {name},

Quick follow-up about your property at {address}. 

Steven can have a cash offer to you within 24 hours if you're still interested in selling quickly.

Still exploring your options?""",
            
            2: f"""{name}, 

Are you still looking to sell your house at {address}?

Steven's ready to make a fair cash offer - no repairs needed, close in 7 days.

Worth a quick chat?""",
            
            3: f"""Hi {name},

Last message about your property.

If you ever want a no-pressure cash offer, just reply "YES" and Steven will call you personally.

Best of luck! 🙏"""
        }
        
        return messages.get(follow_up_number, "")
    
    def check_hot_lead(self, message_text):
        """Check if response indicates hot lead"""
        message_lower = message_text.lower()
        return any(trigger in message_lower for trigger in self.hot_lead_triggers)
    
    def schedule_follow_ups(self, lead_id):
        """Schedule follow-up messages"""
        follow_up_schedule = [
            {'days': 7, 'message_type': 'follow_up_1'},
            {'days': 14, 'message_type': 'follow_up_2'}, 
            {'days': 30, 'message_type': 'follow_up_3'}
        ]
        
        return follow_up_schedule

# Example usage and testing
if __name__ == "__main__":
    bot = MessengerAutomation()
    
    # Test lead data
    test_lead = {
        'first_name': 'John',
        'property_address': '123 Main St, Denver, CO',
        'situation': 'Moving',
        'timeline': 'ASAP'
    }
    
    # Generate instant message
    instant = bot.generate_instant_message(test_lead)
    print("INSTANT MESSAGE:")
    print(instant)
    print("\n" + "="*50 + "\n")
    
    # Generate follow-up messages
    for i in range(1, 4):
        follow_up = bot.get_follow_up_message(i, test_lead)
        print(f"FOLLOW-UP {i}:")
        print(follow_up)
        print("\n" + "-"*30 + "\n")