#!/usr/bin/env python3
"""
VIORA WARM OUTREACH — Personal Network Outreach Generator
For people Arturo already knows. NOT cold outreach.
Generates personalized DM/text templates and inserts into DB as warm_lead.

Usage:
    python3 warm-outreach.py --input warm-contacts.csv
    python3 warm-outreach.py --input warm-contacts.csv --discord
    python3 warm-outreach.py --input warm-contacts.csv --output warm-messages.txt

CSV format:
    name,business_name,relationship,phone,email
    Mike,Mike's Barbershop,friend,303-555-1234,mike@mikes.com
    Sarah,Glow Med Spa,acquaintance,,sarah@glowspa.com

relationship: friend | acquaintance | met_once
"""

import argparse
import csv
import json
import os
import random
import sys
from datetime import datetime
from pathlib import Path

import requests

from config import DB_PATH, DISCORD_WEBHOOK, OUTPUT_DIR
from db import get_conn, init_db


# ── Message Templates by Relationship ────────────────────────────────────────

TEMPLATES_FRIEND = [
    (
        "Hey {name}, random question — what do you do when {business_name} misses "
        "a call? I've been building an AI receptionist that answers 24/7, books "
        "appointments, the whole thing. Thought of you immediately. Want to see a "
        "quick demo?"
    ),
    (
        "Hey {name}! So I've been working on something cool — an AI that answers "
        "phone calls for businesses like {business_name}. Sounds like sci-fi but "
        "it works. Can I show you a 2-min demo? Honestly think it could help."
    ),
    (
        "{name}! Quick one — do you ever miss calls at {business_name}? I built "
        "an AI receptionist that picks up every call, books appointments, answers "
        "questions. Been getting great results. Would love to show you."
    ),
]

TEMPLATES_ACQUAINTANCE = [
    (
        "Hey {name}, hope you're doing well! Random thought — I've been building "
        "AI receptionists for service businesses and {business_name} popped into "
        "my head. It answers every call 24/7, books appointments automatically. "
        "Would you be open to a quick look?"
    ),
    (
        "Hey {name}! I know this is out of the blue — I've been working on an AI "
        "receptionist for businesses like {business_name}. It picks up calls you'd "
        "normally miss, books appointments on the spot. Would a 15-min demo be "
        "worth your time?"
    ),
]

TEMPLATES_MET_ONCE = [
    (
        "Hey {name}, we met a while back — hope business is going well! I've been "
        "building something I think could help {business_name}: an AI receptionist "
        "that answers calls 24/7 and books appointments. Happy to show you a quick "
        "demo if you're curious."
    ),
    (
        "Hi {name}, reaching out because I've been building AI receptionists for "
        "service businesses and thought of {business_name}. It handles calls you'd "
        "normally miss — nights, weekends, busy times. Would a quick demo interest you?"
    ),
]

TEMPLATE_MAP = {
    "friend": TEMPLATES_FRIEND,
    "acquaintance": TEMPLATES_ACQUAINTANCE,
    "met_once": TEMPLATES_MET_ONCE,
}


def generate_message(name, business_name, relationship):
    """Generate a personalized warm outreach message."""
    rel = relationship.lower().strip()
    templates = TEMPLATE_MAP.get(rel, TEMPLATES_ACQUAINTANCE)
    template = random.choice(templates)
    return template.format(name=name, business_name=business_name)


def insert_warm_lead(contact):
    """Insert a warm lead into the database."""
    conn = get_conn()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        conn.execute("""
            INSERT OR IGNORE INTO leads
            (business_name, phone, email, owner_name, industry, city,
             status, notes, date_added, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, 'warm_lead', ?, ?, ?)
        """, (
            contact.get("business_name", ""),
            contact.get("phone", ""),
            contact.get("email", ""),
            contact.get("name", ""),
            "warm_network",
            "warm",
            f"Relationship: {contact.get('relationship', 'unknown')}",
            now,
            now,
        ))
        conn.commit()
        return conn.total_changes > 0
    except Exception as e:
        print(f"  ⚠️  DB insert failed for {contact.get('name', '?')}: {e}")
        return False
    finally:
        conn.close()


def send_discord(content):
    """Send a message to Discord webhook."""
    if not DISCORD_WEBHOOK:
        print("  ⚠️  No DISCORD_WEBHOOK set — skipping Discord post.")
        return
    # Discord has 2000 char limit
    chunks = [content[i:i + 1900] for i in range(0, len(content), 1900)]
    for chunk in chunks:
        try:
            requests.post(DISCORD_WEBHOOK, json={"content": chunk}, timeout=10)
        except Exception as e:
            print(f"  ⚠️  Discord post failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="Generate warm outreach messages")
    parser.add_argument("--input", required=True, help="Path to CSV file with warm contacts")
    parser.add_argument("--output", default=None, help="Output text file (default: output/warm-messages-DATE.txt)")
    parser.add_argument("--discord", action="store_true", help="Post messages to Discord")
    parser.add_argument("--no-db", action="store_true", help="Don't insert into database")
    args = parser.parse_args()

    csv_path = Path(args.input)
    if not csv_path.exists():
        print(f"❌ CSV not found: {csv_path}")
        sys.exit(1)

    # Initialize DB
    if not args.no_db:
        init_db()

    # Read contacts
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        contacts = list(reader)

    if not contacts:
        print("❌ No contacts found in CSV.")
        sys.exit(1)

    print(f"📋 Found {len(contacts)} warm contacts")

    # Generate messages
    messages = []
    db_inserted = 0

    for contact in contacts:
        name = contact.get("name", "").strip()
        business = contact.get("business_name", "").strip()
        relationship = contact.get("relationship", "acquaintance").strip()

        if not name or not business:
            print(f"  ⚠️  Skipping row — missing name or business_name")
            continue

        msg = generate_message(name, business, relationship)
        messages.append({
            "name": name,
            "business_name": business,
            "relationship": relationship,
            "phone": contact.get("phone", "").strip(),
            "email": contact.get("email", "").strip(),
            "message": msg,
        })

        # Insert into DB
        if not args.no_db:
            if insert_warm_lead(contact):
                db_inserted += 1

        print(f"  ✅ {name} ({business}) — {relationship}")

    # Write to text file
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_path = Path(args.output) if args.output else OUTPUT_DIR / f"warm-messages-{date_str}.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"WARM OUTREACH MESSAGES — {date_str}\n")
        f.write(f"Generated for {len(messages)} contacts\n")
        f.write("=" * 60 + "\n\n")

        for m in messages:
            channel = "TEXT" if m["phone"] else "LINKEDIN DM"
            f.write(f"📱 {m['name']} — {m['business_name']} ({m['relationship']})\n")
            f.write(f"   Channel: {channel}\n")
            if m["phone"]:
                f.write(f"   Phone: {m['phone']}\n")
            if m["email"]:
                f.write(f"   Email: {m['email']}\n")
            f.write(f"\n   {m['message']}\n")
            f.write("\n" + "-" * 40 + "\n\n")

    print(f"\n📄 Messages saved to: {output_path}")
    print(f"💾 {db_inserted} new leads inserted into DB as 'warm_lead'")

    # Post to Discord
    if args.discord or DISCORD_WEBHOOK:
        discord_msg = f"🔥 **WARM OUTREACH — {len(messages)} contacts ready**\n\n"
        for m in messages:
            channel = "📱 TEXT" if m["phone"] else "💬 LINKEDIN"
            discord_msg += f"**{m['name']}** ({m['business_name']}) — {channel}\n"
            discord_msg += f"> {m['message']}\n\n"
        send_discord(discord_msg)
        print("📨 Posted to Discord")

    print(f"\n🚀 Done! Send these messages NOW — warm leads convert 5-10x better than cold.")


if __name__ == "__main__":
    main()
