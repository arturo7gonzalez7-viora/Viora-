#!/usr/bin/env python3
"""
VIORA OUTREACH — Centralized Configuration
Single source of truth for all settings, paths, and constants.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent
LOG_DIR     = BASE_DIR / "logs"
OUTPUT_DIR  = BASE_DIR / "output"
DB_PATH     = BASE_DIR / "viora.db"
ENV_FILE    = BASE_DIR / ".env"

LOG_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Load environment
load_dotenv(ENV_FILE)

# ── API Keys ─────────────────────────────────────────────────────────────────
GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_KEY", "")
HUNTER_API_KEY  = os.getenv("HUNTER_API_KEY", "")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")

# ── Email Config ─────────────────────────────────────────────────────────────
GMAIL_ADDRESS    = os.getenv("GMAIL_ADDRESS", "arturo.vioraai@gmail.com")
SENDER_NAME      = "Arturo"
BOOKING_URL      = os.getenv("BOOKING_URL", "https://calendar.app.google/pHa5h8Faxr2Qz2LL6")
WEBSITE_URL      = "viora-co.com"
TOKEN_FILE       = BASE_DIR / "gmail_token.pickle"
CREDS_FILE       = BASE_DIR / "gmail_credentials.json"

# ── Daily Limits ─────────────────────────────────────────────────────────────
# Gmail sending limits for arturo.vioraai@gmail.com
# Start LOW and ramp up to protect sender reputation
MAX_EMAILS_PER_DAY   = int(os.getenv("MAX_EMAILS_PER_DAY", "40"))
MAX_LINKEDIN_PER_DAY = 40

# Warm-up schedule: day_number -> max_emails
# Used for the first 14 days of sending from a new address
WARMUP_SCHEDULE = {
    1: 5,   2: 5,   3: 8,   4: 8,
    5: 12,  6: 12,  7: 15,  8: 15,
    9: 20, 10: 25, 11: 30, 12: 35,
   13: 40, 14: 40,
}
# After day 14, use MAX_EMAILS_PER_DAY

# ── Sequence Timing ──────────────────────────────────────────────────────────
EMAIL_2_DELAY_DAYS = 3   # days after email 1
EMAIL_3_DELAY_DAYS = 4   # days after email 2 (7 total)
SEND_DELAY_SECONDS = 8   # pause between sends (anti-spam)

# ── Target Industries (no restaurants, no dentists) ──────────────────────────
TARGET_INDUSTRIES = [
    # TIER 1 — Highest-paying, fastest-close industries (30-day sprint priority)
    "medspa", "medical spa", "med spa",
    "law firm", "personal injury attorney", "law office", "attorney",
    "HVAC company", "HVAC contractor",
    "plastic surgeon", "plastic surgery",
    "cosmetic dentist", "cosmetic dentistry",
    # TIER 2 — Strong fit, good close rates
    "hair salon", "barbershop", "beauty salon",
    "plumbing contractor", "roofing contractor",
    "electrical contractor", "general contractor",
    "auto repair shop", "auto detailing",
    "gym", "fitness center", "personal trainer",
    "chiropractor", "physical therapy",
    "veterinary clinic",
    "tattoo shop",
    "cleaning service",
    "insurance agency",
    "real estate office",
    "massage therapy",
    "nail salon",
    "spa",
]

# ── Target Cities (major US metros) ─────────────────────────────────────────
TARGET_CITIES = [
    "Denver, CO", "Los Angeles, CA", "Houston, TX", "Phoenix, AZ",
    "Dallas, TX", "San Antonio, TX", "Austin, TX", "San Diego, CA",
    "San Jose, CA", "Jacksonville, FL", "Fort Worth, TX",
    "Columbus, OH", "Charlotte, NC", "Indianapolis, IN",
    "Seattle, WA", "Nashville, TN", "Oklahoma City, OK", "Las Vegas, NV",
    "Miami, FL", "Atlanta, GA", "Chicago, IL", "Philadelphia, PA",
    "San Francisco, CA", "Portland, OR", "Tampa, FL",
    "Minneapolis, MN", "Sacramento, CA", "Kansas City, MO",
    "Raleigh, NC", "Salt Lake City, UT",
]
