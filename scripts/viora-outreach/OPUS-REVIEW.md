# OPUS REVIEW — Viora Outreach System
## Full architecture upgrade completed March 18, 2026

---

## What Changed (and Why)

### 1. Replaced CSVs with SQLite Database (`db.py`)
**Before:** Scattered CSV files — duplicates inevitable, no dedup, scripts couldn't talk to each other cleanly.
**After:** Single `viora.db` SQLite database with:
- Automatic deduplication by phone number + business name
- Full sequence state tracked per lead
- Send log for every email/LinkedIn DM
- Daily stats table for reporting
- Reply, bounce, unsubscribe tracking
- Query functions all scripts share

**Impact:** No more emailing the same business twice. No more lost leads between CSV files.

---

### 2. Added Centralized Config (`config.py`)
**Before:** Every script had its own hardcoded values — booking URL, sender name, API keys in 5 different places.
**After:** Single `config.py` — change one thing, it changes everywhere.

Also added:
- **Email warmup schedule**: ramps from 5/day → 40/day over 14 days automatically. New addresses that send too many emails too fast get blacklisted. This prevents that.
- Industry-specific **pain point hooks** per industry (gym vs. HVAC vs. law office all get different copy)

---

### 3. Added Reply Checker (`reply-checker.py`) — Most Important New Script
**Before:** System had no way to know if someone replied. It would keep emailing people who already responded.
**After:** Runs every morning BEFORE sending. Checks inbox for:
- ✅ Positive replies ("interested", "tell me more", "schedule") → marks as `interested`, stops sequence
- 🚫 Unsubscribes → stops all emails immediately (CAN-SPAM compliance)
- 🔴 Bounces → marks as bounced, never sends again (protects sender rep)
- 💬 Neutral replies → flags for manual review

**Impact:** Stops emailing people who already replied. Keeps your sender score healthy. Tells you who's interested so you can close them.

---

### 4. Upgraded Email Sender (`email-sender.py` v3)
- Industry-specific subject lines and pain points (not generic copy)
- Reads from DB — no CSV argument needed
- Warmup schedule built in
- 8-second delay between sends + random jitter (looks human)
- Proper bounce + unsubscribe detection
- Logs every send to `send_log` table

---

### 5. Upgraded Lead Scraper (`lead-scraper.py`)
- `--rotate` flag: auto-picks industry + city by day of week. No manual args needed in cron.
- Writes directly to DB (deduplication automatic)
- Legacy CSV import still works for importing old files

---

### 6. Upgraded Email Finder (`find-emails.py`)
- Reads from DB (no CSV needed)
- Hunter.io for verified emails, pattern fallback if no API key
- Skips leads that already have emails (no wasted API calls)

---

### 7. Upgraded LinkedIn Queue (`linkedin-queue.py`)
- Reads from DB
- Logs DM queue to `send_log` table so stats are accurate
- Outputs to `output/` directory

---

### 8. Upgraded Automation Script (`jarvis-automate.sh` v3)
**Before:** Could double-send emails (called sender twice), no reply checking, manual CSV selection.
**After:** Clean 5-step pipeline:
1. Check replies first (before anything else)
2. Scrape leads (auto-rotate — no manual args)
3. Find emails
4. Send emails (respects warmup + daily limit)
5. Send Discord report

`set -euo pipefail` — if any critical step errors out, it stops and logs instead of silently failing.

---

## What You Still Need to Set Up (Arturo's Action Items)

```
.env file — fill in:
  GOOGLE_MAPS_KEY=   → console.cloud.google.com (free)
  HUNTER_API_KEY=    → hunter.io (25 free/mo, $49/mo for 500)
  DISCORD_WEBHOOK=   → Discord channel settings → Integrations → Webhooks
  GMAIL_ADDRESS=     arturo.vioraai@gmail.com (already set as default)
  BOOKING_URL=       https://calendar.app.google/pHa5h8Faxr2Qz2LL6 (already set)
```

Gmail OAuth credentials:
- Follow ARTURO-ACTION-LIST.md Step 2
- Runs `gmail_credentials.json` → `gmail_token.pickle` on first run

---

## Daily Automation Flow (Fully Automatic)

```
8:00 AM Mon-Fri (cron)
  ↓
Check inbox for replies → mark positive/unsubscribe/bounce in DB
  ↓
Scrape 50 new leads → DB (auto-deduplicated)
  ↓
Find emails for leads missing them (Hunter.io or pattern)
  ↓
Send up to 40 emails (respects warmup schedule, 8s between sends)
  ↓
Generate LinkedIn DM queue (20 messages → output/ folder)
  ↓
Discord report: emails sent, replies, demos booked, progress to $20k
```

**Arturo's daily job:** Check Discord at 8am. Reply to positive leads. Send 20 LinkedIn DMs. Show up to demo calls. Close.

---

## Revenue Projection

| Month | New Clients | Setup Revenue | Recurring MRR |
|-------|------------|---------------|---------------|
| 1     | 2-3        | $5k-$7.5k     | $700-$1,050   |
| 2     | 3-4        | $7.5k-$10k    | $2,100-$2,450 |
| 3     | 4-5        | $10k-$12.5k   | $3,850-$4,200 |
| 4     | 4-5        | $10k-$12.5k   | $5,600-$5,950 |
| 5     | 5+         | $12.5k+       | $7,350-$7,700 |
| 6     | 5+         | $12.5k+       | $9,100+       |

**Path to $20k/month:** 33 clients × $600/mo + 4 setups/mo × $2,500 = ~$30k/mo at scale.

---

## Zero-Cost Stack

| Tool | Cost | Used For |
|------|------|----------|
| Google Maps API | Free ($200 credit/mo) | Lead scraping |
| Gmail API | Free | Sending emails |
| SQLite | Free | CRM database |
| Hunter.io | Free (25/mo) or $49/mo | Email finding |
| Discord webhook | Free | Daily reports |
| VPS cron | Already paid | 24/7 automation |

**Total added cost: $0 to start. $49/mo at scale for Hunter.io.**

---

## Opus Review — 2026-03-18 (Tasks 1-6 Completion)

Completed all 6 remaining tasks: (1) Rewrote email-sequences.md with sub-100-word emails — curiosity-driven subject lines, real social proof (70 barbershop appointments, fitness center half workload), cost anchoring ($3-6k human vs $350 AI), a lowercase breakup subject for high open rates, and 3 reply templates for "interested", "how much", and "tell me more" responses. (2) Upgraded linkedin-queue.py to post numbered DMs directly to Discord via webhook with chunking for the 2000-char limit, while keeping the text file backup. (3) Rebuilt daily-report.py as an action-focused report — positive replies with email addresses at top, inline LinkedIn DMs, MRR progress bar toward $20k, and a concrete TODO list, all under 2000 chars. (4) Rewrote demo-script.md as a structured closer: 30-sec opener that frames it as a decision call, 3 discovery questions, live demo walkthrough with engagement questions, price anchoring with "shut up" discipline, 5 objection handlers, and a 3-stage post-call follow-up sequence. (5) Rewrote ARTURO-ACTION-LIST.md for the SQLite DB architecture — added sending domain as Step 1, Hunter.io API key step, Discord webhook setup, .env configuration, and a clear daily routine section. (6) Updated README.md with architecture diagram, one-line file descriptions, env vars, run commands, and CSV import instructions. All 8 Python files pass py_compile with zero errors.


---

## Final Comprehensive Review — 2026-03-18 (Opus Pass)

### Bugs Fixed

1. **linkedin-queue.py — Broken import**: `from email_sender import get_hook` fails because `email-sender.py` (hyphen) isn't importable as a Python module. Replaced with inline `_INDUSTRY_PLURALS` dict and `_get_industry_plural()` function. Before this fix, every LinkedIn DM used generic "service businesses" instead of industry-specific language.

2. **db.py — bulk_upsert_leads inflated count**: Counter incremented for every row including duplicates that `INSERT OR IGNORE` silently skipped. Fixed by checking `cursor.rowcount > 0`. Before this fix, the scraper log showed "50 new" when only 5 were actually new.

3. **email-sender.py — No bounce rate monitoring**: Added `check_bounce_rate()` that pauses all sending and fires a Discord alert if bounce rate exceeds 10% on 20+ sends. Without this, a bad email list could destroy sender reputation before anyone noticed.

4. **email-sender.py — No unsubscribe footer**: Added `UNSUB_FOOTER` appended to every outgoing email ("Reply 'unsubscribe' to be removed"). CAN-SPAM compliance — without this, recipients mark as spam instead of unsubscribing, which kills deliverability.

5. **email-sender.py — Insufficient send jitter**: Changed from `SEND_DELAY_SECONDS ± small range` (7-11 seconds) to `random.uniform(5, 18)` — much more human-looking pattern. Also added `requests` import for Discord alerting.

6. **reply-checker.py — No instant alert for positive replies**: Added `alert_discord()` call when positive replies are detected. Before, positive replies only showed up in the daily report (could be hours late). Now fires immediately via Discord webhook.

### Created

- **GAME-PLAN.md** — Complete $20k roadmap with exact conversion math, week-by-week 60-day launch plan, daily 15-minute routine, demo call playbook with objection handling, common mistake avoidance, full cost breakdown at launch vs scale, and month-by-month revenue projections (conservative + realistic scenarios).

### Syntax Check

All 8 Python files pass `py_compile` with zero errors: config.py, db.py, email-sender.py, find-emails.py, lead-scraper.py, linkedin-queue.py, reply-checker.py, daily-report.py.

---

## 30-Day Sprint Overhaul — 2026-03-18

### What Changed

**1. GAME-PLAN.md — Complete rewrite from 9-month slow burn to 30-day sprint**
- New pricing: $3,500 setup (was $2,500)
- New target: 6 clients in 30 days = $21k setup + $2,100 MRR
- Day-by-day plan: Days 1-3 (warm network blitz), Days 4-7 (LinkedIn blitz at 40/day), Days 8-14 (email warmup + first closes), Days 15-21 (full volume), Days 22-30 (close hard)
- Added fast-track tactics: warm network first, LinkedIn blitz (40-50 DMs/day), referral partner strategy ($200/referral), high-ticket industry targeting (med spas, law firms, HVAC, plastic surgeons, cosmetic dentists), same-day close technique
- Retained demo playbook and objection handling, updated for $3,500 pricing

**2. config.py — Updated for sprint mode**
- MAX_LINKEDIN_PER_DAY: 20 → 40
- TARGET_INDUSTRIES reordered with Tier 1 (highest-paying, fastest-close) at top: medspa, medical spa, law firm, personal injury attorney, HVAC company, plastic surgeon, cosmetic dentist
- All existing industries preserved in Tier 2

**3. warm-outreach.py — New script for personal network outreach**
- Accepts CSV with name, business_name, relationship, phone, email
- Generates personalized warm DMs by relationship type (friend/acquaintance/met_once)
- Inserts leads into DB with status='warm_lead'
- Posts to Discord webhook and saves to output/ text file
- Multiple template variants per relationship tier for natural variety

**4. email-sequences.md — Added REFERRAL PARTNER OUTREACH section**
- Email template for web designers/agencies/SEO companies
- $200/referral offer, short and friendly
- Includes copy-paste one-liner partners can forward to their clients
- Follow-up email for Day 5
- Updated pricing in "How much?" reply template: $2,500 → $3,500

**5. ARTURO-ACTION-LIST.md — Added FAST TRACK section at top**
- 4 immediate actions for Days 1-3 before cold system warms up
- Write warm contact list (20+ names)
- Run warm-outreach.py with that list
- Post LinkedIn inbound-generating update
- Email 5 referral partners
- Estimated: first demo call within 48 hours

### Syntax Check

All 9 Python files pass `py_compile` with zero errors: config.py, db.py, email-sender.py, find-emails.py, lead-scraper.py, linkedin-queue.py, reply-checker.py, daily-report.py, warm-outreach.py.
