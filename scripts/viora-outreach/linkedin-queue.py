#!/usr/bin/env python3
"""
VIORA LINKEDIN DM QUEUE v3
Generates copy-paste-ready LinkedIn DMs from the database.
Posts them to Discord AND saves a local backup file.

Usage:
  python3 linkedin-queue.py                  # generate 20 DMs
  python3 linkedin-queue.py --limit 10       # fewer DMs
  python3 linkedin-queue.py --dry-run        # preview only
"""

import argparse
import json
import requests
from datetime import datetime

from config import BOOKING_URL, LOG_DIR, OUTPUT_DIR, DISCORD_WEBHOOK
from db import get_leads_for_linkedin, update_lead, log_send

# ── Industry Mapping ──────────────────────────────────────────────────────────
_INDUSTRY_PLURALS = {
    "gym": "gyms", "fitness center": "fitness centers", "personal trainer": "trainers",
    "hair salon": "salons", "barbershop": "barbershops", "beauty salon": "beauty salons",
    "nail salon": "nail salons", "med spa": "med spas", "medical spa": "med spas",
    "HVAC contractor": "HVAC companies", "plumbing contractor": "plumbing companies",
    "roofing contractor": "roofing companies", "electrical contractor": "electrical companies",
    "general contractor": "contractors", "auto repair shop": "auto shops",
    "auto detailing": "detailing shops", "chiropractor": "chiropractic offices",
    "physical therapy": "PT clinics", "massage therapy": "massage studios",
    "law office": "law firms", "attorney": "law firms",
    "veterinary clinic": "vet clinics", "tattoo shop": "tattoo studios",
    "cleaning service": "cleaning companies", "insurance agency": "insurance agencies",
    "real estate office": "real estate offices", "spa": "spas",
}

def _get_industry_plural(industry):
    """Get friendly plural for an industry."""
    if not industry:
        return "service businesses"
    for key, val in _INDUSTRY_PLURALS.items():
        if key.lower() in industry.lower():
            return val
    return "service businesses"

# ── DM Templates ─────────────────────────────────────────────────────────────

def dm_opener(biz, first, industry):
    """First touch — audit pitch. Under 300 chars including booking URL."""
    import random
    variations = [
        f"Hey {first}, I help {industry} businesses automate the time-consuming stuff — missed calls, follow-ups, reviews, scheduling and more. Free 20 min AI review to show exactly where you're losing time and money. Worth a look for {biz}? {BOOKING_URL}",
        f"Hey {first}, quick question for {biz}. I do free AI business reviews where I look at your whole operation and show which automations would save you the most time and money. Takes 20 min. Worth it? {BOOKING_URL}",
        f"Hey {first}, I help {industry} owners stop doing things manually that AI can handle automatically. Free 20 min review to show what's possible for {biz} — no pitch, just real insight. Interested? {BOOKING_URL}",
    ]
    return random.choice(variations)

def dm_followup(biz, first):
    """Follow-up — only if they respond positively."""
    return (
        f"Hey {first}, thanks for the response!\n\n"
        f"Here's my calendar if you want to see a quick 15-min demo — "
        f"I'll show you exactly how it'd sound for {biz}:\n\n"
        f"{BOOKING_URL}\n\n"
        f"No pressure either way."
    )

# ── Discord Posting ──────────────────────────────────────────────────────────

def send_to_discord(dm_list, today):
    """Send the DM queue to Discord as a formatted message."""
    if not DISCORD_WEBHOOK:
        print("⚠️  No DISCORD_WEBHOOK set — skipping Discord post")
        return False

    # Build compact message (Discord 2000 char limit)
    header = f"**💼 LINKEDIN DMs — {today}**\nSearch each name on LinkedIn → Connect with note → Paste message\n\n"
    
    chunks = []
    current = header
    
    for i, dm in enumerate(dm_list, 1):
        entry = (
            f"**{i}. {dm['biz']}** ({dm['city']})\n"
            f"```\n{dm['message']}\n```\n"
        )
        # If adding this entry would exceed 1900 chars, start a new chunk
        if len(current) + len(entry) > 1900:
            chunks.append(current)
            current = f"**💼 LINKEDIN DMs (cont.)**\n\n{entry}"
        else:
            current += entry
    
    if current:
        chunks.append(current)

    success = True
    for chunk in chunks:
        payload = {"content": chunk}
        try:
            resp = requests.post(DISCORD_WEBHOOK, json=payload, timeout=10)
            if resp.status_code not in (200, 204):
                print(f"⚠️  Discord returned {resp.status_code}: {resp.text[:200]}")
                success = False
        except Exception as e:
            print(f"❌ Discord send failed: {e}")
            success = False

    if success:
        print("✅ LinkedIn DMs posted to Discord")
    return success

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    leads = get_leads_for_linkedin()
    if not leads:
        print("✅ No leads available for LinkedIn DMs.")
        return

    leads = leads[:args.limit]
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = OUTPUT_DIR / f"linkedin_queue_{today}.txt"

    # Build DM list
    dm_list = []
    lines = [
        "=" * 60,
        f"VIORA LINKEDIN DM QUEUE — {today}",
        f"Messages: {len(leads)}",
        "",
        "HOW TO SEND:",
        "1. Search the business name on LinkedIn",
        "2. Find the owner/manager profile",
        "3. Click 'Connect' → Add a note → paste the message",
        "   OR click 'Message' if you're already connected",
        "4. Check off each one as you go",
        "=" * 60,
        ""
    ]

    for idx, lead in enumerate(leads):
        biz = lead["business_name"] or "your business"
        first = (lead["owner_name"] or "").split()[0] if lead["owner_name"] else "there"
        industry = lead["industry"] or "service businesses"
        website = lead["website"] or ""
        city = lead["city"] or ""

        # Map industry to friendly plural
        # NOTE: email-sender.py has a hyphen so can't be imported as module.
        # Use inline lookup from the INDUSTRY_HOOKS concept.
        plural = _get_industry_plural(industry)

        message = dm_opener(biz, first, plural)

        dm_list.append({
            "biz": biz,
            "city": city,
            "website": website,
            "message": message,
        })

        lines += [
            f"── [{idx + 1}/{len(leads)}] {'─' * 45}",
            f"🏢 {biz}",
            f"📍 {city}",
            f"🌐 {website or 'N/A'}",
            f"🔍 LinkedIn search: \"{biz}\" or \"{biz} {city}\"",
            "",
            "📋 PASTE THIS:",
            "─" * 40,
            message,
            "─" * 40,
            "",
            "[ ] Sent  [ ] Connected  [ ] No profile found",
            "",
        ]

        if not args.dry_run:
            # NOTE: Do NOT auto-mark linkedin_sent here.
            # Arturo sends DMs manually. Marking happens only when he
            # clicks "Mark Sent" in the CRM or confirms manually.
            pass  # update_lead(lead["id"], linkedin_sent=today)

    # Append follow-up template
    lines += [
        "=" * 60,
        "",
        "FOLLOW-UP TEMPLATE (use when they respond positively):",
        "─" * 40,
        dm_followup("[Business Name]", "[First Name]"),
        "─" * 40,
        "",
        f"✅ {len(dm_list)} messages queued",
        "=" * 60,
    ]

    # Save backup text file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n✅ LinkedIn queue: {len(dm_list)} messages")
    print(f"📄 Backup: {output_file}")

    # Post to Discord
    if not args.dry_run:
        send_to_discord(dm_list, today)
    else:
        print("🏃 Dry run — skipped Discord post")

if __name__ == "__main__":
    main()
