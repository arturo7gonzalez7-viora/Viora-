#!/usr/bin/env python3
"""
VIORA LEAD SCRAPER v2
Scrapes Google Maps for local service businesses → saves to SQLite DB.
Handles deduplication automatically. Rotates through cities/industries.

Usage:
  python3 lead-scraper.py --industry "gym" --city "Denver, CO"
  python3 lead-scraper.py --rotate              # auto-rotate by day
  python3 lead-scraper.py --all-cities --all-industries  # full scrape
"""

import requests
import json
import time
import argparse
import logging
from datetime import datetime

from config import (
    GOOGLE_MAPS_KEY, TARGET_INDUSTRIES, TARGET_CITIES,
    LOG_DIR, BASE_DIR
)
from db import bulk_upsert_leads, get_conn

# ── Logging ──────────────────────────────────────────────────────────────────
LOG_FILE = LOG_DIR / f"scrape_{datetime.now().strftime('%Y-%m-%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
log = logging.getLogger(__name__)

# ── Excluded keywords (filter out irrelevant results) ────────────────────────
EXCLUDE_KEYWORDS = [
    "restaurant", "dentist", "dental", "pizza", "taco", "sushi",
    "burger", "cafe", "coffee", "bakery", "church", "school",
    "hospital", "pharmacy", "bank",
]

def is_excluded(name):
    """Check if business name contains excluded keywords."""
    name_lower = name.lower()
    return any(kw in name_lower for kw in EXCLUDE_KEYWORDS)

def search_places(industry, city, api_key, max_results=60):
    """Search Google Maps for businesses. Returns list of lead dicts."""
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    leads = []
    next_token = None
    pages = 0

    while pages < 3:  # Google returns max 3 pages (60 results)
        params = {
            "query": f"{industry} in {city}",
            "key": api_key,
            "type": "establishment"
        }
        if next_token:
            params["pagetoken"] = next_token
            time.sleep(2)  # Required by Google API between page requests

        try:
            resp = requests.get(url, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            log.error(f"API request failed: {e}")
            break

        if data.get("status") not in ("OK", "ZERO_RESULTS"):
            log.error(f"API error: {data.get('status')} — {data.get('error_message', '')}")
            break

        for place in data.get("results", []):
            name = place.get("name", "")
            if is_excluded(name):
                continue

            lead = {
                "business_name": name,
                "address": place.get("formatted_address", ""),
                "rating": place.get("rating", None),
                "total_reviews": place.get("user_ratings_total", 0),
                "place_id": place.get("place_id", ""),
                "industry": industry,
                "city": city,
                "phone": "",
                "website": "",
                "email": "",
                "owner_name": "",
            }

            # Get place details (phone + website) — costs 1 detail request each
            if place.get("place_id"):
                details = get_place_details(place["place_id"], api_key)
                lead["phone"] = details.get("phone", "")
                lead["website"] = details.get("website", "")

            # Only keep leads with a phone number (real businesses)
            if lead["phone"]:
                leads.append(lead)
                log.info(f"  ✅ {lead['business_name']} — {lead['phone']} — {lead['website'] or 'no website'}")

            if len(leads) >= max_results:
                break

        next_token = data.get("next_page_token")
        pages += 1
        if not next_token or len(leads) >= max_results:
            break

    return leads

def get_place_details(place_id, api_key):
    """Get phone and website for a place."""
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "formatted_phone_number,website",
        "key": api_key
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        result = resp.json().get("result", {})
        return {
            "phone": result.get("formatted_phone_number", ""),
            "website": result.get("website", "")
        }
    except requests.RequestException as e:
        log.warning(f"Detail lookup failed for {place_id}: {e}")
        return {"phone": "", "website": ""}

def get_rotation_index():
    """Get today's rotation index based on day of year."""
    return datetime.now().timetuple().tm_yday

def main():
    parser = argparse.ArgumentParser(description="Viora Lead Scraper v2")
    parser.add_argument("--industry", help="Industry to search")
    parser.add_argument("--city", help="City to search")
    parser.add_argument("--limit", type=int, default=50, help="Max leads per search")
    parser.add_argument("--rotate", action="store_true",
                        help="Auto-rotate industry+city by day")
    parser.add_argument("--all-cities", action="store_true")
    parser.add_argument("--all-industries", action="store_true")
    args = parser.parse_args()

    if not GOOGLE_MAPS_KEY:
        print("❌ Set GOOGLE_MAPS_KEY in .env first")
        print("   Get free key at: console.cloud.google.com")
        return

    # Determine what to scrape
    if args.rotate:
        idx = get_rotation_index()
        # Rotate through industry/city combos — different combo each day
        industry_idx = idx % len(TARGET_INDUSTRIES)
        city_idx = idx % len(TARGET_CITIES)
        industries = [TARGET_INDUSTRIES[industry_idx]]
        cities = [TARGET_CITIES[city_idx]]
        log.info(f"🔄 Auto-rotation day {idx}: {industries[0]} in {cities[0]}")
    elif args.all_cities and args.all_industries:
        industries = TARGET_INDUSTRIES
        cities = TARGET_CITIES
    elif args.all_cities:
        industries = [args.industry or "gym"]
        cities = TARGET_CITIES
    elif args.all_industries:
        industries = TARGET_INDUSTRIES
        cities = [args.city or "Denver, CO"]
    else:
        industries = [args.industry or "gym"]
        cities = [args.city or "Denver, CO"]

    total_found = 0
    total_new = 0

    for city in cities:
        for industry in industries:
            log.info(f"\n🔍 Searching: {industry} in {city}")
            leads = search_places(industry, city, GOOGLE_MAPS_KEY, args.limit)
            total_found += len(leads)

            if leads:
                new_count = bulk_upsert_leads(leads)
                total_new += new_count
                log.info(f"  📊 Found {len(leads)}, {new_count} new (rest were duplicates)")

            time.sleep(1)  # Be nice to the API

    log.info(f"\n{'='*50}")
    log.info(f"✅ Scraping complete")
    log.info(f"   Total found:  {total_found}")
    log.info(f"   New leads:    {total_new}")
    log.info(f"   Duplicates:   {total_found - total_new}")

    # Show DB totals
    conn = get_conn()
    total = conn.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
    with_email = conn.execute("SELECT COUNT(*) FROM leads WHERE email != ''").fetchone()[0]
    conn.close()
    log.info(f"   DB total:     {total} leads ({with_email} with emails)")
    log.info(f"{'='*50}\n")

if __name__ == "__main__":
    main()
