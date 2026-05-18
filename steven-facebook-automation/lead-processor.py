#!/usr/bin/env python3
"""
Lead Processing and CRM Integration for Steven's Facebook Leads
Handles incoming leads and determines hot vs cold classification
"""

import json
import requests
from datetime import datetime
from messenger_automation import MessengerAutomation

class LeadProcessor:
    def __init__(self):
        self.messenger_bot = MessengerAutomation()
        self.hot_lead_criteria = {
            'timeline_urgent': ['ASAP', '1-3 months'],
            'situation_motivated': ['Financial hardship', 'Divorce', 'Moving'],
            'condition_distressed': ['Needs major work', 'Poor condition']
        }
    
    def process_facebook_lead(self, lead_data):
        """Process incoming Facebook lead and trigger automation"""
        
        # Extract lead information
        lead_info = {
            'lead_id': lead_data.get('leadgen_id'),
            'timestamp': datetime.now().isoformat(),
            'first_name': self.extract_field(lead_data, 'first_name'),
            'phone': self.extract_field(lead_data, 'phone_number'),
            'property_address': self.extract_field(lead_data, 'property_address'),
            'situation': self.extract_field(lead_data, 'situation'),
            'timeline': self.extract_field(lead_data, 'timeline'),
            'property_condition': self.extract_field(lead_data, 'property_condition'),
            'contact_preference': self.extract_field(lead_data, 'contact_method')
        }
        
        # Classify lead as hot or cold
        lead_score = self.calculate_lead_score(lead_info)
        lead_info['score'] = lead_score
        lead_info['classification'] = 'HOT' if lead_score >= 7 else 'WARM' if lead_score >= 4 else 'COLD'
        
        # Send instant messenger response
        instant_message = self.messenger_bot.generate_instant_message(lead_info)
        self.send_messenger_response(lead_info['lead_id'], instant_message)
        
        # Schedule follow-up sequence
        self.schedule_lead_follow_ups(lead_info)
        
        # Send to Steven's CRM if hot lead
        if lead_info['classification'] in ['HOT', 'WARM']:
            self.send_to_steven_crm(lead_info)
            self.notify_steven(lead_info)
        
        # Log the lead
        self.log_lead(lead_info)
        
        return lead_info
    
    def extract_field(self, lead_data, field_name):
        """Extract specific field from Facebook lead data"""
        field_data = lead_data.get('field_data', [])
        for field in field_data:
            if field.get('name') == field_name:
                return field.get('values', [None])[0]
        return None
    
    def calculate_lead_score(self, lead_info):
        """Calculate lead score based on motivation indicators"""
        score = 0
        
        # Timeline urgency (0-4 points)
        if lead_info['timeline'] == 'ASAP':
            score += 4
        elif lead_info['timeline'] == '1-3 months':
            score += 2
        
        # Situation motivation (0-3 points)
        if lead_info['situation'] in ['Financial hardship', 'Divorce']:
            score += 3
        elif lead_info['situation'] in ['Moving', 'Inherited property']:
            score += 2
        
        # Property condition (0-2 points)
        if lead_info['property_condition'] in ['Poor condition', 'Needs major work']:
            score += 2
        elif lead_info['property_condition'] == 'Needs minor work':
            score += 1
        
        # Contact preference (0-1 points)
        if lead_info['contact_preference'] in ['Call', 'Text']:
            score += 1
        
        return min(score, 10)  # Cap at 10
    
    def send_messenger_response(self, lead_id, message):
        """Send automated messenger response (placeholder)"""
        print(f"SENDING MESSENGER TO LEAD {lead_id}:")
        print(message)
        print("-" * 50)
        # TODO: Implement actual Facebook Messenger API call
        return True
    
    def schedule_lead_follow_ups(self, lead_info):
        """Schedule follow-up messages"""
        follow_ups = self.messenger_bot.schedule_follow_ups(lead_info['lead_id'])
        print(f"SCHEDULED {len(follow_ups)} FOLLOW-UPS for {lead_info['first_name']}")
        # TODO: Implement actual scheduling system
        return follow_ups
    
    def send_to_steven_crm(self, lead_info):
        """Send hot leads to Steven's CRM system"""
        crm_data = {
            'name': lead_info['first_name'],
            'phone': lead_info['phone'],
            'email': f"facebook_lead_{lead_info['lead_id']}@placeholder.com",
            'property_address': lead_info['property_address'],
            'lead_source': 'Facebook Ads',
            'situation': lead_info['situation'],
            'timeline': lead_info['timeline'],
            'score': lead_info['score'],
            'classification': lead_info['classification'],
            'notes': f"Property condition: {lead_info['property_condition']}. Contact preference: {lead_info['contact_preference']}"
        }
        
        print(f"SENDING TO STEVEN'S CRM - {lead_info['classification']} LEAD:")
        print(json.dumps(crm_data, indent=2))
        print("-" * 50)
        # TODO: Implement actual CRM API integration
        return True
    
    def notify_steven(self, lead_info):
        """Notify Steven of hot leads immediately"""
        if lead_info['classification'] == 'HOT':
            notification = f"""🔥 HOT LEAD ALERT! 
            
Name: {lead_info['first_name']}
Phone: {lead_info['phone']}
Address: {lead_info['property_address']}
Situation: {lead_info['situation']}
Timeline: {lead_info['timeline']}
Score: {lead_info['score']}/10

This lead scored {lead_info['score']}/10 - call ASAP!"""
            
            print("STEVEN NOTIFICATION:")
            print(notification)
            print("-" * 50)
            # TODO: Send SMS/email notification to Steven
    
    def log_lead(self, lead_info):
        """Log lead for tracking and analysis"""
        with open('steven-facebook-automation/leads_log.json', 'a') as f:
            f.write(json.dumps(lead_info) + '\n')

# Example usage and testing
if __name__ == "__main__":
    processor = LeadProcessor()
    
    # Test lead data (simulating Facebook webhook)
    test_facebook_lead = {
        'leadgen_id': 'test_lead_12345',
        'field_data': [
            {'name': 'first_name', 'values': ['Sarah']},
            {'name': 'phone_number', 'values': ['+13035551234']},
            {'name': 'property_address', 'values': ['456 Oak St, Denver, CO 80202']},
            {'name': 'situation', 'values': ['Financial hardship']},
            {'name': 'timeline', 'values': ['ASAP']},
            {'name': 'property_condition', 'values': ['Needs major work']},
            {'name': 'contact_method', 'values': ['Call']}
        ]
    }
    
    # Process the test lead
    processed_lead = processor.process_facebook_lead(test_facebook_lead)
    
    print("\nPROCESSED LEAD SUMMARY:")
    print(f"Name: {processed_lead['first_name']}")
    print(f"Score: {processed_lead['score']}/10")
    print(f"Classification: {processed_lead['classification']}")
    print(f"Address: {processed_lead['property_address']}")
    print(f"Timeline: {processed_lead['timeline']}")
    print(f"Situation: {processed_lead['situation']}")