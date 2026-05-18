#!/usr/bin/env python3
"""
VIORA EMAIL SENDER v3
Sends cold email sequences via Gmail API (OAuth2).
Reads from SQLite DB. Handles warmup, bounce detection, and sequence timing.

CRITICAL RULES FOR DELIVERABILITY:
- Plain text only (no HTML = less spam score)
- Short emails (under 150 words ideal)
- No images, no attachments
- Personalize subject + body
- 8-second delay between sends
- Warm up new addresses gradually

Usage:
  python3 email-sender.py                    # send up to daily limit
  python3 email-sender.py --dry-run          # preview without sending
  python3 email-sender.py --limit 20         # custom limit
"""

import os
import base64
import pickle
import argparse
import logging
import time
import random
from datetime import datetime
from email.mime.text import MIMEText
from pathlib import Path

import requests as _requests

from config import (
    BOOKING_URL, SENDER_NAME, GMAIL_ADDRESS, TOKEN_FILE, CREDS_FILE,
    LOG_DIR, MAX_EMAILS_PER_DAY, WARMUP_SCHEDULE,
    EMAIL_2_DELAY_DAYS, EMAIL_3_DELAY_DAYS, SEND_DELAY_SECONDS,
    WEBSITE_URL, DB_PATH, DISCORD_WEBHOOK,
)
from db import get_leads_needing_emails, update_lead, log_send, get_conn

LOG_FILE = LOG_DIR / f"sent_{datetime.now().strftime('%Y-%m-%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
log = logging.getLogger(__name__)

# ── Industry-Specific Pain Points ────────────────────────────────────────────
INDUSTRY_HOOKS = {
    "gym":                  ("gym owners", "lose members who call and get voicemail", "gyms"),
    "fitness center":       ("gym owners", "lose members who call and get voicemail", "fitness centers"),
    "personal trainer":     ("trainers", "miss booking calls while you're mid-session", "trainers"),
    "hair salon":           ("salon owners", "lose clients to the salon down the street when you can't answer", "salons"),
    "barbershop":           ("barbershop owners", "miss new client calls while you're cutting", "barbershops"),
    "beauty salon":         ("salon owners", "lose clients when they call and no one picks up", "beauty salons"),
    "nail salon":           ("salon owners", "lose walk-in-ready clients to missed calls", "nail salons"),
    "med spa":              ("med spa owners", "lose $500+ treatment bookings to missed calls", "med spas"),
    "medical spa":          ("med spa owners", "lose $500+ treatment bookings to missed calls", "med spas"),
    "HVAC contractor":      ("HVAC companies", "lose emergency service calls after hours", "HVAC companies"),
    "plumbing contractor":  ("plumbers", "miss emergency calls when you're on a job", "plumbing companies"),
    "roofing contractor":   ("roofers", "miss estimate requests while you're on a roof", "roofing companies"),
    "electrical contractor": ("electricians", "lose jobs when customers can't reach you", "electrical companies"),
    "general contractor":   ("contractors", "miss calls from potential clients while on-site", "contractors"),
    "auto repair shop":     ("shop owners", "lose customers who call and get voicemail", "auto shops"),
    "auto detailing":       ("detailing shop owners", "lose bookings when you can't pick up", "detailing shops"),
    "chiropractor":         ("chiropractors", "lose new patients to missed calls", "chiropractic offices"),
    "physical therapy":     ("PT clinic owners", "lose patient referrals to voicemail", "PT clinics"),
    "massage therapy":      ("massage therapists", "miss booking calls while in session", "massage studios"),
    "law office":           ("attorneys", "lose potential clients to voicemail", "law firms"),
    "attorney":             ("attorneys", "lose potential clients to voicemail", "law firms"),
    "veterinary clinic":    ("vet clinic owners", "miss emergency pet calls after hours", "vet clinics"),
    "tattoo shop":          ("tattoo shop owners", "lose bookings when you're mid-session", "tattoo studios"),
    "cleaning service":     ("cleaning company owners", "miss quote requests while your team is out", "cleaning companies"),
    "insurance agency":     ("insurance agents", "lose leads when they call and can't reach you", "insurance agencies"),
    "real estate office":   ("real estate agents", "lose leads who call once and move on", "real estate offices"),
    "spa":                  ("spa owners", "lose bookings when your front desk is busy", "spas"),
}

DEFAULT_HOOK = ("business owners", "lose customers to missed calls", "service businesses")

def get_hook(industry):
    """Get industry-specific language."""
    if not industry:
        return DEFAULT_HOOK
    for key, val in INDUSTRY_HOOKS.items():
        if key.lower() in industry.lower():
            return val
    return DEFAULT_HOOK

# ── Email Templates ──────────────────────────────────────────────────────────
# KEY PRINCIPLES:
# - Short (under 150 words)
# - One clear question/CTA
# - Sounds like a real person, not marketing
# - Uses "you/your" more than "we/our"
# - Social proof is specific, not vague

def email1(biz, first, industry):
    """The Hook — broad AI angle, not just receptionist."""
    # Randomize subject line for better deliverability
    subjects = [
        f"Quick question, {first}",
        f"Has {biz} tried AI yet?",
        f"Question for {biz}",
    ]
    subject = random.choice(subjects)

    body = f"""Hey {first},

Has {biz} started using AI yet?

Most service businesses are still doing everything manually — answering calls, following up with leads, booking appointments, chasing reviews. It eats hours every week that could be automated.

We help businesses like {biz} implement AI that handles all of that automatically — so you and your team can focus on the work that actually makes money.

One client added 70 new bookings in 30 days. Another cut their front desk workload in half. All from automating things they were already doing manually.

Worth a 15-min call to see what we could automate for {biz}?

{BOOKING_URL}

— {SENDER_NAME}
Viora AI | {WEBSITE_URL}"""
    return subject, body

def email2(biz, first, industry):
    """The Pain List — show them what's eating their time."""
    subject = f"Re: Quick question, {first}"

    body = f"""Hey {first}, following up —

Here's what most service businesses waste time on every week:
- Answering the same questions over the phone
- Manually following up with leads who went cold
- Booking appointments back and forth
- Chasing customers for reviews

AI handles all of it. Automatically. For less than $400/month.

Happy to show you exactly what it would look like for {biz} in 15 minutes.

{BOOKING_URL}

— {SENDER_NAME}"""
    return subject, body

def email3(biz, first, industry):
    """The Breakup — clean, no pressure, broad exit."""
    subject = f"Last one — {biz}"

    body = f"""Hey {first},

Last email, I promise.

If AI automation for {biz} is ever worth exploring — whether it's handling calls, following up with leads, or just cutting out the repetitive stuff — we're at {WEBSITE_URL}.

Good luck with everything.

— {SENDER_NAME}"""
    return subject, body

# ── Gmail API ────────────────────────────────────────────────────────────────
def get_gmail_service():
    """Authenticate and return Gmail API service."""
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
                if not CREDS_FILE.exists():
                    print(f"\n❌ Missing: {CREDS_FILE}")
                    print("   Follow ARTURO-ACTION-LIST.md Step 2 to set up Gmail API\n")
                    return None
                flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_FILE), SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, "wb") as f:
                pickle.dump(creds, f)

        return build("gmail", "v1", credentials=creds)
    except ImportError:
        print("❌ Run: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        return None

def send_email(service, to_email, subject, body):
    """Send a plain-text email via Gmail API."""
    msg = MIMEText(body, "plain")
    msg["to"] = to_email
    msg["from"] = f"{SENDER_NAME} <{GMAIL_ADDRESS}>"
    msg["subject"] = subject
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    result = service.users().messages().send(userId="me", body={"raw": raw}).execute()
    return result

def get_warmup_limit():
    """Calculate today's send limit based on warmup schedule."""
    # Check when first email was ever sent
    conn = get_conn()
    first = conn.execute(
        "SELECT MIN(sent_at) FROM send_log WHERE channel='email'"
    ).fetchone()[0]
    conn.close()

    if not first:
        return WARMUP_SCHEDULE.get(1, 5)

    try:
        first_date = datetime.strptime(first[:10], "%Y-%m-%d")
        days_active = (datetime.now() - first_date).days + 1
        if days_active <= 14:
            return WARMUP_SCHEDULE.get(days_active, MAX_EMAILS_PER_DAY)
    except (ValueError, TypeError):
        pass

    return MAX_EMAILS_PER_DAY

# ── Bounce Rate Monitor ──────────────────────────────────────────────────────
def check_bounce_rate():
    """Check bounce rate. Returns (bounce_rate, should_pause).
    Only counts leads that were actually sent to AND bounced back.
    Pre-emptively blocked emails (info@) are NOT counted as bounces."""
    conn = get_conn()
    # Only count real bounces = leads that were sent to AND bounced
    total_contacted = conn.execute(
        "SELECT COUNT(*) FROM leads WHERE email_1_sent IS NOT NULL"
    ).fetchone()[0]
    real_bounced = conn.execute(
        "SELECT COUNT(*) FROM leads WHERE bounced = 1 AND email_1_sent IS NOT NULL"
    ).fetchone()[0]
    conn.close()

    if total_contacted < 20:
        return 0.0, False  # Not enough data yet

    bounce_rate = real_bounced / total_contacted
    if bounce_rate > 0.10:
        alert_discord(
            f"🚨 **BOUNCE RATE ALERT — SENDING PAUSED**\n"
            f"Bounce rate: {bounce_rate:.1%} ({real_bounced}/{total_contacted})\n"
            f"Sending paused to protect sender reputation.\n"
            f"Action: Check email list quality, remove bad domains, then restart."
        )
        return bounce_rate, True
    return bounce_rate, False


def alert_discord(message):
    """Send an urgent alert to Discord."""
    if not DISCORD_WEBHOOK:
        log.warning(f"Discord alert (no webhook): {message}")
        return
    try:
        _requests.post(DISCORD_WEBHOOK, json={"content": message}, timeout=10)
    except Exception as e:
        log.warning(f"Failed to send Discord alert: {e}")


# ── Unsubscribe Footer ──────────────────────────────────────────────────────
UNSUB_FOOTER = (
    "\n\n---\n"
    "Not relevant? Reply 'unsubscribe' and I'll remove you immediately."
)


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Viora Email Sender v3")
    parser.add_argument("--limit", type=int, default=0,
                        help="Override daily limit (0 = use warmup/config)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without sending")
    # Legacy CSV support
    parser.add_argument("--csv", help="(Legacy) ignored — reads from DB now")
    args = parser.parse_args()

    # Check bounce rate before doing anything
    bounce_rate, should_pause = check_bounce_rate()
    if should_pause:
        log.error(f"🚨 Bounce rate too high ({bounce_rate:.1%}). PAUSING all sends.")
        log.error("   Fix: review lead quality, remove bad emails, then restart.")
        return

    # Determine daily limit
    if args.limit > 0:
        daily_limit = args.limit
    else:
        daily_limit = get_warmup_limit()

    log.info(f"📧 Email sender starting — daily limit: {daily_limit} (bounce rate: {bounce_rate:.1%})")

    # Check how many already sent today
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_conn()
    already_sent = conn.execute(
        "SELECT COUNT(*) FROM send_log WHERE channel='email' AND sent_at LIKE ?",
        (f"{today}%",)
    ).fetchone()[0]
    conn.close()

    remaining = max(0, daily_limit - already_sent)
    if remaining == 0:
        log.info(f"✅ Already sent {already_sent} today (limit: {daily_limit}). Done.")
        return

    log.info(f"   Already sent today: {already_sent}, remaining: {remaining}")

    # Get leads ready for next email in sequence
    leads = get_leads_needing_emails()
    if not leads:
        log.info("✅ No leads ready for emails right now.")
        return

    service = None if args.dry_run else get_gmail_service()
    if not args.dry_run and not service:
        return

    sent = 0

    for lead in leads:
        if sent >= remaining:
            break

        email = (lead["email"] or "").strip()

        # HARD BLOCK: never send to generic/guessed emails. Ever.
        BLOCKED_PREFIXES = ('info@', 'contact@', 'hello@', 'admin@', 'office@',
                            'support@', 'team@', 'mail@', 'sales@', 'help@',
                            'noreply@', 'no-reply@', 'billing@', 'accounts@')
        if not email or '@' not in email or email.lower().startswith(BLOCKED_PREFIXES):
            continue

        biz = lead["business_name"] or "your business"
        owner = (lead["owner_name"] or "").strip()
        first = owner.split()[0] if owner else "there"
        industry = lead["industry"] or ""

        e1 = lead["email_1_sent"]
        e2 = lead["email_2_sent"]
        e3 = lead["email_3_sent"]

        subject, body, seq_num = None, None, None
        update_fields = {}

        if not e1:
            subject, body = email1(biz, first, industry)
            seq_num = 1
            update_fields["email_1_sent"] = today
            update_fields["status"] = "contacted"
        elif not e2:
            subject, body = email2(biz, first, industry)
            seq_num = 2
            update_fields["email_2_sent"] = today
        elif not e3:
            subject, body = email3(biz, first, industry)
            seq_num = 3
            update_fields["email_3_sent"] = today
            update_fields["status"] = "sequence_complete"
        else:
            continue

        # Append unsubscribe footer for CAN-SPAM compliance
        body += UNSUB_FOOTER

        if args.dry_run:
            print(f"\n[DRY RUN] Email {seq_num} → {email}")
            print(f"  Subject: {subject}")
            print(f"  Biz: {biz} | First: {first} | Industry: {industry}")
            sent += 1
        else:
            try:
                send_email(service, email, subject, body)
                update_lead(lead["id"], **update_fields)
                log_send(lead["id"], email, subject, seq_num, "email")
                log.info(f"✅ Email {seq_num} → {email} ({biz})")
                sent += 1
                # Random jitter: 5-18 seconds between sends (looks human, not a bot)
                delay = random.uniform(5, 18)
                time.sleep(delay)
            except Exception as e:
                error_str = str(e).lower()
                if "bounce" in error_str or "invalid" in error_str or "not found" in error_str:
                    update_lead(lead["id"], bounced=1, status="bounced")
                    log.warning(f"🔴 Bounced: {email} ({biz}) — marked as bounced")
                else:
                    log.error(f"❌ Failed → {email} ({biz}): {e}")

    mode = "DRY RUN" if args.dry_run else "SENT"
    log.info(f"\n{'='*50}")
    log.info(f"✅ Email sender complete [{mode}]")
    log.info(f"   Emails sent:     {sent}")
    log.info(f"   Daily limit:     {daily_limit}")
    log.info(f"   Already today:   {already_sent}")
    log.info(f"   Log: {LOG_FILE}")
    log.info(f"{'='*50}\n")

if __name__ == "__main__":
    main()
