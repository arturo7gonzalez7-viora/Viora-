#!/usr/bin/env python3
"""Scrape leads across all major US cities and industries."""
import sys, os, time
sys.path.insert(0, os.path.dirname(__file__))
from lead_scraper import search_places, bulk_upsert_leads
from config import GOOGLE_MAPS_KEY

CITIES = [
    "New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX",
    "Phoenix, AZ", "Philadelphia, PA", "San Antonio, TX", "San Diego, CA",
    "Dallas, TX", "Austin, TX", "Jacksonville, FL", "Fort Worth, TX",
    "Columbus, OH", "Charlotte, NC", "Indianapolis, IN", "San Francisco, CA",
    "Seattle, WA", "Denver, CO", "Nashville, TN", "Las Vegas, NV",
    "Miami, FL", "Atlanta, GA", "Minneapolis, MN", "Portland, OR",
    "Tampa, FL", "Sacramento, CA", "Kansas City, MO", "Raleigh, NC",
    "Salt Lake City, UT", "Tucson, AZ", "Albuquerque, NM", "Virginia Beach, VA",
    "New Orleans, LA", "Bakersfield, CA", "Honolulu, HI", "Omaha, NE",
    "Cleveland, OH", "Arlington, TX", "Wichita, KS", "Aurora, CO"
]

INDUSTRIES = [
    "med spa", "HVAC contractor", "law firm", "hair salon",
    "roofing contractor", "gym", "auto repair shop", "cleaning service",
    "chiropractor", "tattoo shop"
]

if not GOOGLE_MAPS_KEY:
    print("ERROR: GOOGLE_MAPS_KEY not set")
    sys.exit(1)

total_new = 0
# Rotate: pick 5 random city/industry combos per run
import random
combos = [(c, i) for c in CITIES for i in INDUSTRIES]
random.shuffle(combos)
selected = combos[:8]  # 8 combos = ~400 leads per run

for city, industry in selected:
    print(f"Searching: {industry} in {city}")
    leads = search_places(industry, city, GOOGLE_MAPS_KEY, 50)
    new = bulk_upsert_leads(leads)
    total_new += new
    print(f"  {len(leads)} found, {new} new")
    time.sleep(1)

print(f"\nTotal new leads added: {total_new}")
