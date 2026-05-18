#!/usr/bin/env python3
"""
VIORA EMAIL FINDER v2
Finds business owner emails from websites.
Strategy: Hunter.io API → pattern guessing → generic fallback.
Reads from SQLite DB instead of CSV.

Free alternatives to Hunter.io:
  - hunter.io: 25 free searches/month
  - Email pattern guessing: unlimited, ~40% accuracy

Usage:
  python3 find-emails.py                    # find emails for all leads missing them
  python3 find-emails.py --limit 50         # process 50 leads max
  python3 find-emails.py --guess-only       # skip API, just guess patterns
  python3 find-emails.py --verify           # verify guessed emails with Hunter
"""

import os
import time
import requests
import argparse
import logging
from datetime import datetime
from urllib.parse import urlparse

from config import HUNTER_API_KEY, LOG_DIR
from db import get_leads_needing_email_lookup, update_lead

LOG_FILE = LOG_DIR / f"emails_found_{datetime.now().strftime('%Y-%m-%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
log = logging.getLogger(__name__)

def clean_domain(website_url):
    """Extract root domain from any URL."""
    if not website_url:
        return None
    url = website_url.strip()
    if not url.startswith("http"):
        url = "https://" + url
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.replace("www.", "").strip()
        # Filter out social media / directory domains
        skip_domains = [
            "facebook.com", "instagram.com", "yelp.com", "google.com",
            "linkedin.com", "twitter.com", "tiktok.com", "youtube.com",
            "wix.com", "squarespace.com", "godaddy.com",
        ]
        if any(domain.endswith(sd) for sd in skip_domains):
            return None
        return domain if "." in domain else None
    except Exception:
        return None

def find_email_hunter(domain, first_name=None, last_name=None):
    """Use Hunter.io to find emails. Returns (email, confidence)."""
    if not HUNTER_API_KEY:
        return None, None

    # Try Email Finder if we have a real name
    if first_name and first_name.lower() not in ("there", "owner", "manager"):
        url = "https://api.hunter.io/v2/email-finder"
        params = {
            "domain": domain,
            "first_name": first_name,
            "api_key": HUNTER_API_KEY
        }
        if last_name:
            params["last_name"] = last_name
        try:
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code == 429:
                log.warning("Hunter.io rate limited — pausing 60s")
                time.sleep(60)
                resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            if data.get("data", {}).get("email"):
                return data["data"]["email"], data["data"].get("score", 0)
        except Exception as e:
            log.warning(f"Hunter email-finder failed for {domain}: {e}")

    # Fallback: Domain Search
    url = "https://api.hunter.io/v2/domain-search"
    params = {
        "domain": domain,
        "api_key": HUNTER_API_KEY,
        "limit": 5,
        "type": "personal"
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 429:
            log.warning("Hunter.io rate limited — pausing 60s")
            time.sleep(60)
            resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        emails = data.get("data", {}).get("emails", [])

        # Prioritize by role
        priority_roles = ["owner", "founder", "president", "ceo", "manager", "director"]
        for priority in priority_roles:
            for e in emails:
                position = (e.get("position") or "").lower()
                if priority in position:
                    return e["value"], e.get("confidence", 0)

        # Take first personal email
        if emails:
            return emails[0]["value"], emails[0].get("confidence", 0)

    except Exception as e:
        log.warning(f"Hunter domain-search failed for {domain}: {e}")

    return None, None

def guess_email(domain):
    """
    Guess the most common small-business email patterns.
    Returns the single best guess (most likely to work).
    """
    if not domain:
        return None
    # For small businesses, info@ and the owner's first name are most common
    # info@ has the highest hit rate across industries
    return f"info@{domain}"

def verify_email_hunter(email):
    """Verify an email address via Hunter.io (uses 1 verification credit)."""
    if not HUNTER_API_KEY:
        return None
    try:
        resp = requests.get("https://api.hunter.io/v2/email-verifier", params={
            "email": email,
            "api_key": HUNTER_API_KEY
        }, timeout=10)
        data = resp.json()
        result = data.get("data", {}).get("result", "")
        return result  # "deliverable", "undeliverable", "risky", "unknown"
    except Exception:
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=50, help="Max leads to process")
    parser.add_argument("--guess-only", action="store_true",
                        help="Skip API, use pattern guessing only")
    parser.add_argument("--verify", action="store_true",
                        help="Verify guessed emails via Hunter")
    # Legacy CSV support
    parser.add_argument("--csv", help="(Legacy) Import CSV then find emails")
    args = parser.parse_args()

    # Legacy CSV import
    if args.csv:
        from db import import_csv
        import_csv(args.csv)

    leads = get_leads_needing_email_lookup()
    if not leads:
        print("✅ All leads with websites already have emails. Nothing to do.")
        return

    leads = leads[:args.limit]
    log.info(f"🔍 Finding emails for {len(leads)} leads...")

    found = 0
    guessed = 0

    for lead in leads:
        domain = clean_domain(lead["website"])
        if not domain:
            continue

        biz = lead["business_name"]
        owner = (lead["owner_name"] or "").strip()
        first = owner.split()[0] if owner else None
        last = owner.split()[-1] if owner and len(owner.split()) > 1 else None

        email = None
        confidence = None

        if not args.guess_only:
            email, confidence = find_email_hunter(domain, first, last)
            if email:
                log.info(f"✅ Hunter found: {email} (score: {confidence}) — {biz}")
                found += 1

        if not email:
            email = guess_email(domain)
            confidence = "guessed"
            if email:
                # Optionally verify the guess
                if args.verify and HUNTER_API_KEY:
                    result = verify_email_hunter(email)
                    if result == "undeliverable":
                        log.info(f"❌ Guess bounced: {email} — {biz}")
                        email = None
                        confidence = None
                    else:
                        log.info(f"✅ Guess verified ({result}): {email} — {biz}")
                else:
                    log.info(f"🔮 Guessed: {email} — {biz}")
                if email:
                    guessed += 1

        if email:
            update_lead(lead["id"], email=email, email_confidence=str(confidence or ""))

        # Rate limit
        time.sleep(0.5 if not args.guess_only else 0.01)

    log.info(f"\n{'='*50}")
    log.info(f"✅ Email finder complete")
    log.info(f"   API found:  {found}")
    log.info(f"   Guessed:    {guessed}")
    log.info(f"   Total:      {found + guessed}")
    log.info(f"{'='*50}\n")

if __name__ == "__main__":
    main()
