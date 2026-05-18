#!/usr/bin/env python3
"""
VIORA REPLY CHECKER
Checks Gmail inbox for replies to outreach emails.
Marks leads as replied, detects unsubscribes and bounces.

Usage: python3 reply-checker.py
"""

import pickle
import logging
import re
import requests as _requests
from datetime import datetime
from pathlib import Path

from config import TOKEN_FILE, CREDS_FILE, LOG_DIR, GMAIL_ADDRESS, DISCORD_WEBHOOK
from db import get_conn, update_lead


def alert_discord(message):
    """Send an urgent alert to Discord."""
    if not DISCORD_WEBHOOK:
        return
    try:
        _requests.post(DISCORD_WEBHOOK, json={"content": message}, timeout=10)
    except Exception:
        pass

LOG_FILE = LOG_DIR / f"replies_{datetime.now().strftime('%Y-%m-%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
log = logging.getLogger(__name__)

UNSUB_KEYWORDS = ["unsubscribe", "remove me", "stop emailing", "opt out", "take me off"]
BOUNCE_KEYWORDS = ["delivery failed", "undeliverable", "mailbox not found", "user unknown",
                   "does not exist", "rejected", "550 ", "invalid recipient"]
POSITIVE_KEYWORDS = ["interested", "tell me more", "sounds good", "let's chat",
                     "set up a call", "I'm open", "schedule", "demo", "learn more",
                     "how much", "pricing", "cost"]

def get_gmail_service():
    """Get authenticated Gmail service."""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        SCOPES = [
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/gmail.readonly",
        ]
        creds = None
        if TOKEN_FILE.exists():
            with open(TOKEN_FILE, "rb") as f:
                creds = pickle.load(f)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                log.error("Gmail credentials not set up. Run email-sender.py --dry-run first.")
                return None
            with open(TOKEN_FILE, "wb") as f:
                pickle.dump(creds, f)
        return build("gmail", "v1", credentials=creds)
    except ImportError:
        print("❌ Run: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        return None

def extract_email_address(header_value):
    """Extract email address from a From header."""
    match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', header_value or "")
    return match.group(0).lower() if match else None

def classify_reply(body_text):
    """Classify a reply as positive, negative, unsubscribe, or neutral."""
    text = (body_text or "").lower()

    for kw in UNSUB_KEYWORDS:
        if kw in text:
            return "unsubscribe"

    for kw in BOUNCE_KEYWORDS:
        if kw in text:
            return "bounce"

    for kw in POSITIVE_KEYWORDS:
        if kw in text:
            return "positive"

    # "Not interested" variants
    if any(phrase in text for phrase in ["not interested", "no thanks", "no thank you", "pass on this"]):
        return "negative"

    return "neutral"

def get_message_body(service, msg_id):
    """Get plain text body from a Gmail message."""
    try:
        msg = service.users().messages().get(userId="me", id=msg_id, format="full").execute()
        payload = msg.get("payload", {})

        # Try to get plain text
        if payload.get("mimeType") == "text/plain":
            data = payload.get("body", {}).get("data", "")
        else:
            parts = payload.get("parts", [])
            data = ""
            for part in parts:
                if part.get("mimeType") == "text/plain":
                    data = part.get("body", {}).get("data", "")
                    break

        if data:
            import base64
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
    except Exception as e:
        log.warning(f"Failed to get message body: {e}")
    return ""

def main():
    service = get_gmail_service()
    if not service:
        return

    # Get all emails in inbox from last 7 days that are replies
    log.info("🔍 Checking for replies...")
    try:
        results = service.users().messages().list(
            userId="me",
            q=f"is:inbox newer_than:7d -from:{GMAIL_ADDRESS}",
            maxResults=100
        ).execute()
    except Exception as e:
        log.error(f"Failed to list messages: {e}")
        return

    messages = results.get("messages", [])
    if not messages:
        log.info("✅ No new replies found.")
        return

    log.info(f"📬 Found {len(messages)} inbox messages to check")

    conn = get_conn()
    new_replies = 0
    unsubscribes = 0
    bounces = 0
    positive = 0

    for msg_meta in messages:
        msg_id = msg_meta["id"]
        try:
            msg = service.users().messages().get(
                userId="me", id=msg_id, format="metadata",
                metadataHeaders=["From", "Subject"]
            ).execute()
        except Exception:
            continue

        headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
        from_email = extract_email_address(headers.get("From", ""))
        subject = headers.get("Subject", "")

        if not from_email:
            continue

        # Check if this email matches a lead in our DB
        lead = conn.execute(
            "SELECT * FROM leads WHERE LOWER(email) = ? AND replied IS NULL",
            (from_email,)
        ).fetchone()

        if not lead:
            continue

        # Get message body for classification
        body = get_message_body(service, msg_id)
        classification = classify_reply(body)

        today = datetime.now().strftime("%Y-%m-%d")

        if classification == "unsubscribe":
            update_lead(lead["id"], unsubscribed=1, replied="unsubscribe", reply_date=today,
                       status="not_interested")
            log.info(f"🚫 Unsubscribe: {from_email} ({lead['business_name']})")
            unsubscribes += 1

        elif classification == "bounce":
            update_lead(lead["id"], bounced=1, status="bounced")
            log.info(f"🔴 Bounce: {from_email} ({lead['business_name']})")
            bounces += 1

        elif classification == "positive":
            update_lead(lead["id"], replied="positive", reply_date=today,
                       status="interested")
            log.info(f"🟢 POSITIVE reply: {from_email} ({lead['business_name']}) — RESPOND ASAP!")
            positive += 1

        elif classification == "negative":
            update_lead(lead["id"], replied="negative", reply_date=today,
                       status="not_interested")
            log.info(f"🔴 Not interested: {from_email} ({lead['business_name']})")

        else:
            update_lead(lead["id"], replied="neutral", reply_date=today)
            log.info(f"💬 Reply: {from_email} ({lead['business_name']}) — check manually")

        new_replies += 1

    conn.close()

    log.info(f"\n{'='*50}")
    log.info(f"✅ Reply check complete")
    log.info(f"   New replies:    {new_replies}")
    log.info(f"   Positive:       {positive} ← RESPOND TO THESE!")
    log.info(f"   Unsubscribes:   {unsubscribes}")
    log.info(f"   Bounces:        {bounces}")
    log.info(f"{'='*50}\n")

    if positive > 0:
        log.info("🔥🔥🔥 You have POSITIVE replies! Check your email and respond NOW! 🔥🔥🔥")
        # Immediate Discord alert for positive replies
        alert_discord(
            f"🔥🔥🔥 **{positive} POSITIVE REPLY{'S' if positive > 1 else ''}!** "
            f"Check your email and respond NOW! Every hour you wait = lower close rate."
        )

if __name__ == "__main__":
    main()
