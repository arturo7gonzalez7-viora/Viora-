# VIORA 30-DAY SPRINT — $20K IN 30 DAYS
## No slow burn. No 9-month timeline. 30 days. All out.

---

## THE MATH

```
Target:     $21,000 in setup revenue + $2,100 MRR
How:        6 clients × $3,500 setup + $350/mo
To close 6: 12 demo calls (50% close rate with live demo)
To get 12:  240 quality outreach touches (5% demo booking rate)
Per day:    8 touches/day = $21k in 30 days

Channel breakdown:
  LinkedIn DMs:      40/day (no warmup needed, starts Day 4)
  Warm network:      20+ people (Days 1-3, highest conversion)
  Cold email:        ramps to 20-30/day by Day 15
  Referral partners: 5-10 active (each sends 1-2 leads/month)
```

### Pricing (Updated)
- **Setup fee:** $3,500 (50/50 split: $1,750 upfront, $1,750 on launch)
- **Monthly recurring:** $350/mo
- **Why $3,500:** Still 50-60% cheaper than a human receptionist ($3-6k/mo). Business owners understand the value.

### The 30-Day Revenue Target

| Week | New Clients | Setup Revenue | Running Total |
|------|------------|---------------|---------------|
| 1    | 0          | $0            | $0            |
| 2    | 1-2        | $3,500-$7,000 | $3,500-$7,000 |
| 3    | 2-3        | $7,000-$10,500| $10,500-$17,500|
| 4    | 2-3        | $7,000-$10,500| $17,500-$28,000|

**Conservative: $17,500. Realistic: $21,000+. Aggressive: $28,000.**

---

## THE 30-DAY PLAN

### DAYS 1-3: SETUP + WARM NETWORK BLITZ

**Goal: System configured. Warm outreach launched. First demo booked.**

This is the highest-leverage window. Your personal network converts at 20-30%, not 5%.

- [ ] **Day 1 — System Setup**
  - Buy sending domain (getvioraai.com or similar) + set up Google Workspace ($6/mo)
  - Configure SPF, DKIM, DMARC
  - Set up Gmail API + OAuth (`gmail_credentials.json`)
  - Fill in `.env` (Google Maps key, Hunter.io key, Discord webhook)
  - Run `bash setup.sh` → verify "SETUP COMPLETE"
  - Test: `python3 email-sender.py --dry-run`

- [ ] **Day 1 — Warm Network List**
  - Write down EVERY business owner you know (target 20+ names)
  - Friends, acquaintances, met-once contacts — all of them
  - Fill in `warm-contacts.csv` (name, business_name, relationship, phone, email)
  - Run `python3 warm-outreach.py --input warm-contacts.csv`
  - Send those warm DMs TODAY via LinkedIn/text

- [ ] **Day 2 — LinkedIn Content + Referral Partners**
  - Post on LinkedIn: *"Helping 3 service businesses this month never miss another call. DM me if interested."* (creates inbound)
  - Identify 5-10 web designers / marketing agencies / SEO companies who serve service businesses
  - Email them the referral partner pitch ($200/referral — see email-sequences.md)
  - Follow up with any warm contacts who haven't replied

- [ ] **Day 3 — Demo Prep + First Scrape**
  - Record 2-3 AI call demo recordings (med spa, law firm, HVAC)
  - Practice demo-script.md once
  - Run first lead scrape: `python3 lead-scraper.py --industry "medical spa" --city "Denver, CO"`
  - Find emails: `python3 find-emails.py`
  - Confirm booking link works

**By end of Day 3:** Warm outreach sent to 20+ contacts. LinkedIn post live. Referral partners emailed. System tested and ready.

### DAYS 4-7: LINKEDIN BLITZ + FIRST DEMOS

**Goal: 200+ LinkedIn DMs sent. First demo calls happening.**

LinkedIn requires ZERO warmup. You can start at full volume immediately.

**Daily routine (45 min):**
1. Run `python3 linkedin-queue.py` → get today's 40 DMs
2. Send all 40 on LinkedIn (copy-paste from Discord/output folder)
3. Respond to any warm network replies (these are HOT — book same-day demos)
4. Check for referral partner responses

**Scraping in parallel:**
- Auto-scrape runs via cron: 50 leads/day across high-ticket industries
- Focus scraper on: med spas, law firms, HVAC, plastic surgeons, cosmetic dentists
- Find emails for all new leads

**By end of Day 7:** 160+ LinkedIn DMs sent. 8-16 positive replies. 2-4 demos booked. Warm network may have already produced 1-2 demos.

### DAYS 8-14: EMAIL WARMUP + CLOSING FIRST DEALS

**Goal: Email starts ramping. Close first 1-2 clients.**

The email warmup begins automatically (5/day → 15/day by Day 14). Meanwhile, LinkedIn is still generating demos.

**Daily routine (60 min):**
1. Check Discord report (2 min)
2. Reply to ALL positive leads within 2 hours (5 min)
3. Send 40 LinkedIn DMs (15 min)
4. Follow up with demo no-shows / interested leads (10 min)
5. Run demo calls — use same-day close technique (see below)

**Same-day close technique:**
- After the demo, don't say "think about it." Say: *"I can start building this for [Business Name] today. We split setup 50/50 — $1,750 now, $1,750 when it goes live next week. Want to get started?"*
- Send the invoice WHILE ON THE CALL. Don't wait.
- If they hesitate: *"I'm only taking 3 more clients this month to keep quality high."* (Scarcity is real — you can only onboard so many at once.)

**By end of Day 14:** Email system warmed to 15/day. 320+ LinkedIn DMs sent. 2-4 demo calls completed. First 1-2 clients closed = $3,500-$7,000 collected.

### DAYS 15-21: FULL VOLUME + REFERRAL ENGINE

**Goal: Email hits 20-30/day. Referral partners sending leads. Close clients 3-4.**

Both channels now running at volume:
- **Email:** 20-30/day (warmup complete)
- **LinkedIn:** 40/day
- **Referral partners:** hopefully producing 1-2 warm intros/week
- **Total:** 60-70 touches/day = 420-490/week

**Daily routine (60 min):**
1. Check Discord report → handle positive replies FIRST
2. Send LinkedIn DMs (40/day)
3. Follow up with all pending demos / interested leads
4. Check in with referral partners: *"Sent anyone our way yet? Happy to do a quick call with anyone you think would benefit."*

**Key optimization:**
- Which industries are booking demos? Double down.
- Which subject lines get replies? Don't change them.
- Reply rate < 2%? Test new subject lines.
- Demo no-shows? Send SMS reminder 1 hour before.

**By end of Day 21:** 500+ emails sent. 700+ LinkedIn DMs sent. 6-8 demos completed. 3-4 clients closed = $10,500-$14,000 collected.

### DAYS 22-30: CLOSE HARD + HIT THE TARGET

**Goal: Close remaining 2-3 clients. Hit $21,000.**

This is full sprint mode. Every lead in your pipeline gets follow-up.

**Daily routine (90 min):**
1. Morning: Discord report → reply to all positive leads
2. Send 40 LinkedIn DMs + 25-30 emails/day (system handles)
3. Follow up with EVERY open opportunity (call, text, email)
4. Close aggressively — offer to build a custom demo for hesitant prospects (*"Let me show you exactly how it'll sound for YOUR business. If you don't like it, no charge."*)
5. Onboard closed clients (don't let fulfillment slip while selling)

**Pipeline pressure moves:**
- Anyone who said "interested" but hasn't booked → call them directly
- Anyone who did a demo but didn't close → send a 60-second video of their custom AI answering
- Referral partners → ask for specific intros: *"Do you have any med spa or law firm clients who've mentioned missed calls?"*

**By end of Day 30:** 800+ emails sent. 1,200+ LinkedIn DMs sent. 10-14 demos total. 6+ clients closed = $21,000+ in setup revenue + $2,100 MRR.

---

## FAST-TRACK TACTICS

### 1. Warm Network First (Days 1-3)
Your personal contacts convert 5-10x better than cold outreach. A warm DM saying *"Hey, I built something that might help your business"* gets a meeting. A cold email to a stranger might not.

**Action:** List 20+ business owners you know. DM/text all of them before touching cold outreach.

### 2. LinkedIn Blitz (40-50 DMs/Day)
LinkedIn doesn't require warmup like email. You can send 40-50 connection requests + messages per day safely from day one. This is your primary channel for the first 2 weeks while email warms up.

**Safe limits:**
- 40 connection requests/day (with personalized note)
- Mix in some without notes to look organic
- Don't send at 3 AM — space between 8 AM and 6 PM
- If LinkedIn warns you, drop to 30/day for 48 hours then resume

### 3. Referral Partner Strategy ($200/Referral)
Web designers, marketing agencies, and SEO companies already serve your target market. They have the relationships. You have the product.

**The deal:** $200 cash for every client they refer who signs. Their clients get better service. They make passive income. No effort required.

**Target:** 5-10 active referral partners. If each sends 1 lead/month, that's 5-10 warm leads you didn't have to find.

**How to find them:**
- Search LinkedIn: "web designer [city]", "marketing agency [city]"
- Search Google: "web design for small businesses [city]"
- Check who built your target businesses' websites (footer credits)

### 4. High-Ticket Industry Targeting
Not all service businesses are equal. These industries pay fastest and have the biggest missed-call pain:

| Industry | Why They Close Fast | Avg Customer Value |
|----------|--------------------|--------------------|
| Med spas / plastic surgeons | High-ticket services ($2k-$15k). Every missed call = thousands lost. | $2,000-$15,000 |
| Personal injury attorneys | Cases worth $50k-$500k. Missing ONE call can cost six figures. | $50,000+ |
| HVAC companies | Emergency calls = urgent jobs. Miss the call, lose the $500+ service call. | $500-$5,000 |
| Cosmetic dentists | Elective procedures, high margins. Patients shop around — first to answer wins. | $1,000-$8,000 |
| Home remodeling | Leads cost $50-200 in ads. Missing the call = wasting ad spend. | $5,000-$50,000 |

**Action:** Prioritize these industries in the scraper rotation. They convert faster because the pain is sharper and the ROI is obvious.

### 5. Same-Day Close Technique
Most AI receptionist demos result in "let me think about it." Here's how to close on the first call:

1. **Set the frame at the start:** *"This call is 15 minutes — I'll show you the demo, we'll see if it's a fit, and if so I can get you set up this week."*
2. **Demo first, price second.** Let them hear it. Let them react. THEN talk money.
3. **Anchor hard:** *"A front desk person: $3-6k/month, works 9-5. This: $3,500 setup, $350/month, works 24/7."*
4. **Ask for the sale directly:** *"I can have this live for [Business Name] in a week. $1,750 to start, $1,750 when it goes live. Want to get started?"*
5. **SHUT UP.** First person to talk loses.
6. **Send the invoice while on the call.** *"I just sent over the invoice — take a look while we're still on."*
7. **Create scarcity:** *"I'm only onboarding 3 more clients this month to keep quality high."*

---

## THE DEMO CALL PLAYBOOK

### Before the Call (2 min prep)
- Their website open in a tab
- Know their services, hours, location
- Have industry-matched demo recording ready
- Invoice template ready to send immediately

### Discovery Questions (3 min)
1. *"How are you handling incoming calls right now?"*
2. *"What happens when nobody can pick up?"*
3. *"When someone calls and gets voicemail, what do they usually do?"*
   → They'll say "call the next place." That's the pain. Repeat it back.

### The Demo (5 min)
> "Let me play you a 60-second recording of the AI answering for a [similar industry]."

**Play the recording. SHUT UP for 3 seconds.**

> "That's an AI. Answers in under 2 seconds. Works 24/7."

**Ask:** *"What would capturing just 5 extra calls a week look like for [Business Name]?"*

### The Close (3 min)
> "A receptionist: $3,000-$6,000/mo, works 9-5, calls in sick."
> "This: $3,500 setup, $350/mo. Works 24/7. Never misses."

> "I can have this live in a week. $1,750 to start, $1,750 on launch. Want to get started?"

**SHUT UP.**

### Objection Responses

**"I need to think about it"**
> "Totally fair. What's the main thing — price, or something else?"
> *(Handle the real objection. Then:)*
> "How about this — I'll build a quick custom demo for [Business Name] tonight. You'll hear how YOUR customers would experience it. I'll send it over by tomorrow morning."

**"Too expensive"**
> "How many calls do you miss per week? ... And what's your average customer worth?"
> *(Let them do the math. $350/mo to capture $2,000+/mo in missed revenue.)*

**"We already have someone"**
> "This covers the gaps — after hours, weekends, when they're on another call or with a client. It doesn't replace them. It backs them up."

**"Not sure it'll work for us"**
> "I'll build a custom demo for [Business Name] — you'll hear exactly how it sounds for YOUR customers. If you don't like it, no charge."

**"Can I try it first?"**
> "The setup IS the trial — I build it custom for you, we tweak it until you love it."

**"I need to talk to my partner"**
> "Makes sense. Want to do a quick 10-minute call with both of you? Easier than explaining secondhand."

### Post-Call Follow-Up
- **Within 2 hours:** Recap email + invoice link
- **48 hours later:** Custom demo recording (if you promised one)
- **7 days later:** *"Last note. If missed calls become worth solving: viora-co.com"*

---

## DAILY ROUTINE BY PHASE

### Days 1-7 (45 min/day + demos)
1. Send warm network outreach (Day 1-3)
2. Send 40 LinkedIn DMs (Day 4+)
3. Reply to all responses within 2 hours
4. Run demos as they come in
5. Email referral partners

### Days 8-21 (60 min/day + demos)
1. Check Discord at 8:15 AM
2. Reply to positive leads IMMEDIATELY
3. Send 40 LinkedIn DMs
4. Follow up with all pending opportunities
5. Run demos — close same day

### Days 22-30 (90 min/day + demos)
1. Everything above PLUS:
2. Direct follow-up with every open opportunity
3. Push referral partners for specific intros
4. Aggressive close on all pending demos
5. Begin onboarding closed clients

---

## WHAT KILLS THE SPRINT

| Mistake | Consequence | Prevention |
|---------|-------------|------------|
| Slow replies | Lead goes cold in 24 hours | Reply within 2 HOURS. Set phone alerts for Discord. |
| Skipping LinkedIn DMs | You lose 40% of your outreach channel | Non-negotiable. 40/day, every day. |
| Not doing warm outreach first | You waste Days 1-7 waiting for cold to work | Hit your personal network before ANYTHING else. |
| Bad demos | 0% close rate | Practice the script. Record yourself. Get better. |
| Perfectionism on onboarding | You stop selling to build | Sell first, deliver on a 1-week timeline. Don't over-build. |
| Not following up | 80% of deals close on follow-up 2-5 | Every lead gets 3 touches minimum. |

---

## THE COST STACK (30-Day Sprint)

| Tool | Cost | Notes |
|------|------|-------|
| Gmail (sending) | $0 | Free, 500/day limit |
| Google Workspace (sending domain) | $6/mo | Professional sender domain |
| Google Maps API | $0 | Free $200/mo credit |
| Hunter.io | $0-$49/mo | Free tier or $49 for volume |
| Discord | $0 | Webhook = free |
| SQLite DB | $0 | Built-in |
| VPS (Hostinger) | $0 | Already paid through March 2026 |
| Domain | ~$10/yr | Already have it |
| **TOTAL** | **$6-$55/mo** | |

---

## THE BOTTOM LINE

$21,000 in 30 days requires 6 clients at $3,500 setup.

To close 6, you need 12 demos. To book 12 demos, you need 240 quality touches.

The system handles email automation, lead scraping, email finding, and reporting. Your job:

1. **Days 1-3:** Hit your warm network hard. Post on LinkedIn. Email referral partners.
2. **Days 4-30:** Send 40 LinkedIn DMs/day. Reply to positive leads within 2 hours. Show up to demos and close.
3. **Every demo:** Use the same-day close technique. Send the invoice on the call.

240 touches ÷ 30 days = 8 per day minimum. You're doing 40+ between LinkedIn and email.

The math works. The system is built. The only variable is execution.

**Sprint starts now.**
