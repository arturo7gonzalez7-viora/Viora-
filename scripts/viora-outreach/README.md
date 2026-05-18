# 🤖 VIORA OUTREACH MACHINE v3
## Automated cold outreach for AI receptionist sales — Goal: $20k/month MRR

---

## Architecture

```
jarvis-automate.sh (cron: 8am Mon-Fri)
  │
  ├─ 1. reply-checker.py   → detect replies, bounces, unsubscribes
  ├─ 2. lead-scraper.py    → scrape Google Maps (auto-rotates industry/city)
  ├─ 3. find-emails.py     → Hunter.io lookup + pattern guessing
  ├─ 4. email-sender.py    → send 3-email sequence with warmup
  ├─ 5. linkedin-queue.py  → generate DMs, post to Discord + backup file
  └─ 6. daily-report.py    → action-focused report to Discord
         │
         └── viora.db (SQLite) ← single source of truth
```

## Files

| File | What it does |
|------|-------------|
| `config.py` | All settings, API keys, paths, industry/city lists |
| `db.py` | SQLite CRM — leads, send log, stats, deduplication |
| `lead-scraper.py` | Scrapes Google Maps Places API for service businesses |
| `find-emails.py` | Finds emails via Hunter.io + common pattern guessing |
| `email-sender.py` | Sends 3-email cold sequence via Gmail API (OAuth2) |
| `reply-checker.py` | Auto-detects positive replies, bounces, unsubscribes |
| `linkedin-queue.py` | Generates LinkedIn DMs, posts to Discord webhook |
| `daily-report.py` | Daily action items + stats → Discord |
| `jarvis-automate.sh` | Master script — runs everything in order (cron entry) |
| `setup.sh` | One-time dependency installer |
| `email-sequences.md` | Email copy, subject lines, reply templates |
| `demo-script.md` | 15-min demo call script with objection handling |
| `ARTURO-ACTION-LIST.md` | Step-by-step setup guide (non-technical) |

## Environment Variables (.env)

```
GOOGLE_MAPS_KEY=        # Google Places API key
HUNTER_API_KEY=         # Hunter.io API key (free tier = 25/mo)
DISCORD_WEBHOOK=        # Discord webhook URL for reports
GMAIL_ADDRESS=          # Sending email address
BOOKING_URL=            # Google Calendar booking link
```

Also needs `gmail_credentials.json` (OAuth2) in the project folder.

## How to Run

**First time:**
```bash
bash setup.sh
python3 email-sender.py --dry-run   # authenticate Gmail + preview
```

**Daily (automated via cron):**
```bash
bash jarvis-automate.sh
```

**Manual runs:**
```bash
python3 lead-scraper.py --industry "gym" --city "Denver, CO"
python3 find-emails.py --guess-only
python3 email-sender.py --limit 20
python3 linkedin-queue.py --limit 10
python3 daily-report.py
```

## Import Old CSV Leads

```bash
python3 -c "from db import import_csv; import_csv('old_leads.csv')"
```

CSV should have columns matching the leads table: `business_name`, `phone`, `email`, `website`, `industry`, `city`, etc.

## Daily Limits

- **40 emails/day** (warmup: starts at 5, ramps over 14 days)
- **20 LinkedIn DMs/day**
- Runs Mon–Fri, 8am Denver time
