#!/usr/bin/env python3
"""
VIORA CRM SYNC
Syncs SQLite database to Google Sheet every morning.
Arturo opens one tab and sees everything.

Columns: Business | Owner Email | Phone | Industry | City | 
         Email 1 | Email 2 | Email 3 | LinkedIn | Replied | Status | Next Action | Notes
"""

import pickle, os, sys
from datetime import datetime, timedelta
from pathlib import Path

# Add script dir to path
sys.path.insert(0, str(Path(__file__).parent))
from config import GOOGLE_SHEET_ID, LOG_DIR
from db import get_conn

LOG_FILE = LOG_DIR / f"crm_sync_{datetime.now().strftime('%Y-%m-%d')}.log"

def get_sheets_service():
    TOKEN_FILE = Path(__file__).parent / "sheets_token.pickle"
    CREDS_FILE = Path(__file__).parent / "gmail_credentials.json"
    
    SCOPES = [
        'https://mail.google.com/',
        'https://www.googleapis.com/auth/spreadsheets',
    ]
    
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        
        creds = None
        if TOKEN_FILE.exists():
            with open(TOKEN_FILE, 'rb') as f:
                creds = pickle.load(f)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print("❌ Sheets not authorized yet.")
                print("   Run: python3 crm-sync.py --auth")
                return None
            with open(TOKEN_FILE, 'wb') as f:
                pickle.dump(creds, f)
        
        return build('sheets', 'v4', credentials=creds)
    except ImportError:
        print("❌ Run: pip install google-api-python-client")
        return None

def auth_sheets():
    """One-time auth for Google Sheets access."""
    CREDS_FILE = Path(__file__).parent / "gmail_credentials.json"
    TOKEN_FILE = Path(__file__).parent / "sheets_token.pickle"
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    from google_auth_oauthlib.flow import InstalledAppFlow
    flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_FILE), SCOPES)
    flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    print("\n🔗 Open this URL and sign in with arturo@viora.team:")
    print(auth_url)
    code = input("\nPaste the code here: ").strip()
    flow.fetch_token(code=code)
    with open(TOKEN_FILE, 'wb') as f:
        pickle.dump(flow.credentials, f)
    print("✅ Sheets authorized!")

def next_action(row):
    """Determine what Arturo should do next for this lead."""
    replied = row['replied'] or ''
    status = row['status'] or 'new'
    e1 = row['email_1_sent']
    e2 = row['email_2_sent']
    e3 = row['email_3_sent']
    linkedin = row['linkedin_sent']
    
    if replied and 'positive' in replied.lower():
        return '🔥 RESPOND NOW'
    if status == 'interested':
        return '📞 BOOK DEMO'
    if status == 'closed':
        return '✅ CLIENT'
    if row['bounced']:
        return '❌ BOUNCED'
    if row['unsubscribed']:
        return '🚫 UNSUBBED'
    if not e1 and not linkedin:
        return '📧 Send Email + LinkedIn DM'
    if e1 and not e2:
        return f'⏳ Email 2 → {e1} +3 days'
    if e2 and not e3:
        return f'⏳ Email 3 → {e2} +4 days'
    if not linkedin:
        return '💼 Send LinkedIn DM'
    if status == 'sequence_complete':
        return '✅ Done'
    return '👀 Monitor'

def sync_to_sheet():
    if not GOOGLE_SHEET_ID:
        print("❌ GOOGLE_SHEET_ID not set in .env")
        return
    
    service = get_sheets_service()
    if not service:
        return
    
    conn = get_conn()
    leads = conn.execute("""
        SELECT * FROM leads 
        ORDER BY 
            CASE status 
                WHEN 'interested' THEN 0
                WHEN 'contacted' THEN 1
                WHEN 'new' THEN 2
                ELSE 3
            END,
            date_added DESC
    """).fetchall()
    conn.close()
    
    # Build header row
    headers = [
        'Business Name', 'Owner Email', 'Phone', 'Website',
        'Industry', 'City', 'Status',
        'Email 1 Sent', 'Email 2 Sent', 'Email 3 Sent',
        'LinkedIn Sent', 'Replied', 'Demo Booked', 'Closed',
        'Next Action', 'Notes', 'Date Added'
    ]
    
    rows = [headers]
    for lead in leads:
        rows.append([
            lead['business_name'] or '',
            lead['email'] or '',
            lead['phone'] or '',
            lead['website'] or '',
            lead['industry'] or '',
            lead['city'] or '',
            lead['status'] or 'new',
            lead['email_1_sent'] or '',
            lead['email_2_sent'] or '',
            lead['email_3_sent'] or '',
            lead['linkedin_sent'] or '',
            lead['replied'] or '',
            lead['demo_booked'] or '',
            lead['closed'] or '',
            next_action(dict(lead)),
            lead['notes'] or '',
            lead['date_added'] or '',
        ])
    
    # Clear and rewrite sheet
    sheet = service.spreadsheets()
    
    # Clear existing data
    sheet.values().clear(
        spreadsheetId=GOOGLE_SHEET_ID,
        range='Sheet1'
    ).execute()
    
    # Write new data
    sheet.values().update(
        spreadsheetId=GOOGLE_SHEET_ID,
        range='Sheet1!A1',
        valueInputOption='RAW',
        body={'values': rows}
    ).execute()
    
    # Format header row bold
    sheet.batchUpdate(
        spreadsheetId=GOOGLE_SHEET_ID,
        body={'requests': [{
            'repeatCell': {
                'range': {'sheetId': 0, 'startRowIndex': 0, 'endRowIndex': 1},
                'cell': {'userEnteredFormat': {
                    'textFormat': {'bold': True},
                    'backgroundColor': {'red': 0.1, 'green': 0.1, 'blue': 0.1}
                }},
                'fields': 'userEnteredFormat(textFormat,backgroundColor)'
            }
        }]}
    ).execute()
    
    print(f"✅ Google Sheet updated — {len(leads)} leads synced")
    print(f"   View: https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}")

if __name__ == '__main__':
    import sys
    if '--auth' in sys.argv:
        auth_sheets()
    else:
        sync_to_sheet()
