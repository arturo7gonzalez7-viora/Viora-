# 🎯 ARTURO'S ACTION LIST
## 30-Day Sprint to $20K — Do these in order.

---

## ⚡ FAST TRACK — DO THIS FIRST (Days 1-3)

**These 4 moves can get your first demo call within 48 hours — before the automated system even warms up.**

### 1. Write Down Every Business Owner You Know
Aim for 20+ names. Friends, acquaintances, people you met once at a networking event. Anyone who owns a service business — salon, gym, contractor, med spa, law firm, whatever.

Put them in a CSV file: `warm-contacts.csv`
```
name,business_name,relationship,phone,email
Mike,Mike's Barbershop,friend,303-555-1234,mike@mikes.com
Sarah,Glow Med Spa,acquaintance,,sarah@glowspa.com
```

### 2. Run warm-outreach.py — Hit Them TODAY
```bash
cd /root/.openclaw/workspace/scripts/viora-outreach
python3 warm-outreach.py --input warm-contacts.csv --discord
```
This generates personalized DMs for each person. Send them via LinkedIn or text RIGHT NOW. These people know you — conversion rate is 5-10x higher than cold outreach.

### 3. Post One LinkedIn Update
Copy-paste this and post it:

> "Helping 3 service businesses this month never miss another call. Built an AI receptionist that answers 24/7, books appointments, sounds completely human. If you own a service business and want to see a demo — DM me."

This alone creates inbound leads. People who come to you close at 50%+.

### 4. Set Up Your Referral Partner List
Write down 5 web designers, marketing agencies, or SEO companies you know (or can find on LinkedIn/Google). Email them the referral partner pitch — $200/referral, no strings.

See **email-sequences.md → REFERRAL PARTNER OUTREACH** for the exact email.

**Bottom line:** These 4 moves take ~2 hours total and can produce your first demo call before the cold email system even finishes warming up.

---

## STEP 1: Buy a Sending Domain
**Time: 5 min · Cost: ~$10/year**

You need a separate domain for cold emails so your main domain stays clean.

1. Go to **Namecheap** or **Google Domains**
2. Buy something like `getvioraai.com` or `tryvioraai.com`
3. Set up **Google Workspace** on it ($6/mo) — this gives you a real Gmail inbox on the new domain
4. Set up SPF, DKIM, and DMARC records (Google Workspace walks you through it)

**Why:** If cold emails get flagged, it doesn't touch your main viora-co.com domain.

---

## STEP 2: Set Up Gmail API
**Time: 10 min · Cost: Free**

1. Go to **console.cloud.google.com**
2. Click "Select a project" → "New Project" → Name it "Viora Outreach" → Create
3. Search **"Gmail API"** → Enable it
4. Click **"Create Credentials"** → "OAuth client ID"
5. Application type: **Desktop app** → Name: "Viora" → Create
6. Download the JSON → rename to `gmail_credentials.json`
7. Move it to the viora-outreach folder:
   ```
   /root/.openclaw/workspace/scripts/viora-outreach/gmail_credentials.json
   ```
8. Test it:
   ```
   cd /root/.openclaw/workspace/scripts/viora-outreach
   python3 email-sender.py --dry-run
   ```
9. Browser opens → sign in → click Allow

**Done when:** dry-run shows emails it WOULD send (without actually sending)

---

## STEP 3: Get Google Maps API Key
**Time: 5 min · Cost: Free ($200/mo free credit)**

1. Same Google Cloud project from Step 2
2. Search **"Places API"** → Enable
3. Click **"Credentials"** → "Create Credentials" → "API Key"
4. Copy the key → paste in your `.env` file (Step 6)

---

## STEP 4: Get Hunter.io API Key
**Time: 2 min · Cost: Free (25 lookups/mo)**

1. Go to **hunter.io** → sign up free
2. Go to API → copy your API key
3. Paste in your `.env` file (Step 6)

**Optional:** Paid plan ($49/mo) gives 1,000 lookups — 10x more emails found.

---

## STEP 5: Set Up Discord Webhook
**Time: 2 min · Cost: Free**

1. In Discord, go to your Viora channel
2. Edit Channel → Integrations → Webhooks → **New Webhook**
3. Name: "Jarvis Reports" → **Copy Webhook URL**
4. Paste in your `.env` file (Step 6)

---

## STEP 6: Fill In Your .env File
**Time: 2 min**

Open (or create) `/root/.openclaw/workspace/scripts/viora-outreach/.env` and fill in:

```
GOOGLE_MAPS_KEY=your_key_here
HUNTER_API_KEY=your_key_here
DISCORD_WEBHOOK=your_webhook_url_here
GMAIL_ADDRESS=arturo@yoursendingdomain.com
BOOKING_URL=https://calendar.app.google/pHa5h8Faxr2Qz2LL6
```

---

## STEP 7: Run Setup
**Time: 1 min**

```bash
cd /root/.openclaw/workspace/scripts/viora-outreach
bash setup.sh
```

**Done when:** Says "SETUP COMPLETE"

---

## STEP 8: First Run
**Time: 5 min**

```bash
cd /root/.openclaw/workspace/scripts/viora-outreach

# Scrape some leads
python3 lead-scraper.py --industry "gym" --city "Denver, CO"
python3 lead-scraper.py --industry "hair salon" --city "Denver, CO"

# Find emails for those leads
python3 find-emails.py --guess-only

# Preview emails (doesn't actually send)
python3 email-sender.py --dry-run

# If that looks good — go live:
python3 email-sender.py
```

Or run everything at once:
```bash
bash jarvis-automate.sh
```

The cron job runs `jarvis-automate.sh` automatically at 8am Denver time, Mon–Fri.

---

## 🚀 YOUR DAILY ROUTINE (15 min/day)

**Every morning:**

1. **Open Discord** → check the daily report from Jarvis
2. **Look for 🔥 POSITIVE REPLIES** → respond using templates in `email-sequences.md`
3. **Send LinkedIn DMs** → they're posted to Discord, just copy-paste each one (~10 min)
4. **Check calendar** → do any demo calls using `demo-script.md`

**That's it. Everything else runs on autopilot.**

---

## 📊 WHAT TO EXPECT

| Timeframe | Emails Sent | Replies | Demos | Clients | MRR |
|-----------|-------------|---------|-------|---------|-----|
| Week 1-2 | 100-150 | 3-5 | 1-2 | 0 | $0 |
| Month 1 | 400-500 | 12-18 | 4-6 | 1-2 | $350-700 |
| Month 2 | 800+ | 25-30 | 8-12 | 3-5 | $1,400-2,100 |
| Month 6 | cumulative | cumulative | — | 15-20 | $5,250-7,000 |

MRR compounds — every client stays and pays $350/mo. At **57 clients** you hit $20k/mo.

---

## 🆘 SOMETHING BROKEN?

| Problem | Fix |
|---------|-----|
| "Gmail credentials missing" | Redo Step 2 |
| "GOOGLE_MAPS_KEY not set" | Check .env file |
| Emails going to spam | Buy the sending domain (Step 1) |
| Low reply rate (<2%) | Check email-sequences.md, try new subject lines |
| No leads found | Try different industries/cities |

Or just tell Jarvis: "X is broken" — he'll fix it.
