# VIORA BUILD CHEATSHEET
## The Complete Guide to Building & Delivering Every Tier

**Last Updated:** March 2026
**Stack:** Retell AI + Twilio + n8n + Google Calendar + Google Sheets/Airtable

---

## 📋 MASTER TOOLS LIST

| Tool | What It Does | Free Tier? | Paid Cost | Sign Up |
|------|-------------|-----------|-----------|---------|
| **Retell AI** | AI voice agent — the brain that answers calls | Free trial (limited mins) | ~$0.07–0.12/min | [retell.ai](https://www.retell.ai) |
| **Twilio** | Phone number + call routing | Free trial ($15 credit) | ~$1/mo per number + $0.013/min | [twilio.com](https://www.twilio.com) |
| **n8n Cloud** | Automation workflows (connects everything) | Free (5 workflows) | $24/mo (starter) | [n8n.io](https://n8n.io) |
| **Google Calendar** | Appointment booking | Free | Free | Already have it |
| **Google Sheets** | Lead tracking CRM (Tier 2+) | Free | Free | Already have it |
| **Airtable** | Advanced CRM (optional upgrade) | Free (1000 records) | $20/mo | [airtable.com](https://www.airtable.com) |
| **SendGrid** | Email sending for follow-ups | Free (100/day) | $15/mo (50k emails) | [sendgrid.com](https://sendgrid.com) |
| **Twilio SMS** | SMS follow-ups (same Twilio account) | Included in trial | ~$0.0079/SMS | Same Twilio account |

### Which Tools for Which Tier?

| Tool | Tier 1 | Tier 2 | Tier 3 |
|------|--------|--------|--------|
| Retell AI | ✓ | ✓ | ✓ |
| Twilio (phone) | ✓ | ✓ | ✓ |
| n8n | ✓ | ✓ | ✓ |
| Google Calendar | ✓ | ✓ | ✓ |
| Google Sheets | — | ✓ | ✓ |
| SendGrid | — | ✓ | ✓ |
| Twilio SMS | — | ✓ | ✓ |

---

## 💰 YOUR COST PER CLIENT (Margins)

### Tier 1 — AI Receptionist
| | Setup | Monthly |
|--|-------|---------|
| **Client pays** | $1,500 | $350/mo |
| Retell AI | — | ~$15–40/mo (depends on call volume) |
| Twilio number | — | ~$2/mo |
| Twilio minutes | — | ~$5–15/mo |
| n8n Cloud | — | ~$5/mo (shared across clients) |
| **Your cost** | ~$0 | **~$27–62/mo** |
| **Your profit** | **$1,500** | **~$288–323/mo** |

### Tier 2 — AI Receptionist + Follow-Up
| | Setup | Monthly |
|--|-------|---------|
| **Client pays** | $2,500 | $750/mo |
| Retell AI | — | ~$15–40/mo |
| Twilio (calls + SMS) | — | ~$10–25/mo |
| SendGrid | — | ~$5/mo (shared) |
| n8n Cloud | — | ~$8/mo |
| Google Sheets | — | Free |
| **Your cost** | ~$0 | **~$38–78/mo** |
| **Your profit** | **$2,500** | **~$672–712/mo** |

### Tier 3 — Full AI Business System
| | Setup | Monthly |
|--|-------|---------|
| **Client pays** | $3,500 | $1,500/mo |
| Retell AI | — | ~$20–50/mo |
| Twilio (calls + SMS) | — | ~$15–35/mo |
| SendGrid | — | ~$8/mo |
| n8n Cloud | — | ~$12/mo |
| Lead scraping tools | — | ~$20–50/mo |
| **Your cost** | ~$0 | **~$75–155/mo** |
| **Your profit** | **$3,500** | **~$1,345–1,425/mo** |

---

## 🏗️ TIER 1 BUILD: AI RECEPTIONIST

**Estimated Build Time:** 4–6 hours
**What client gets:** AI answers every call 24/7, qualifies, books into Google Calendar

### Step-by-Step Build Process

#### Step 1: Set Up Twilio Phone Number (15 min)
1. Go to [twilio.com](https://www.twilio.com) → Sign up / Log in
2. Go to **Phone Numbers** → **Buy a Number**
3. Search for a local number in the client's area code
4. Buy it (~$1.15/mo)
5. Note the phone number — you'll give this to Retell
6. **Important:** Go to **Phone Numbers** → click the number → under **Voice**, set "Configure With" to **Webhook** (we'll add the Retell webhook URL in step 3)

#### Step 2: Create a Retell AI Agent (60 min)
1. Go to [retell.ai](https://www.retell.ai) → Sign up / Log in
2. Click **Create Agent**
3. **Agent Name:** "[Client Business Name] Receptionist"
4. **Voice:** Pick a natural-sounding voice (test a few — "Rachel" or "Mark" work well for service businesses)
5. **Language:** Enable both English and Spanish
6. **System Prompt** — This is the brain. Write it like this:

```
You are the AI receptionist for [Business Name], a [type of business] located in [City, State].

Your job:
- Answer incoming calls professionally and warmly
- Answer common questions about the business (services, hours, pricing, location)
- Qualify callers by asking: What service do you need? When would you like to come in? What's your name and phone number?
- Book appointments into the calendar
- If you can't answer something, say "Let me have [Owner Name] call you back about that. What's the best number to reach you?"

Business Info:
- Name: [Business Name]
- Hours: [Hours]
- Services: [List main services and prices]
- Location: [Address]
- Owner: [Name]

Rules:
- Always be friendly, professional, and efficient
- Never make up information you don't have
- Always confirm the appointment details before ending the call
- If someone is upset, empathize and offer to have the owner call back
- Speak Spanish if the caller speaks Spanish
```

7. **Knowledge Base:** Upload any documents about the business (menu, service list, pricing sheet, FAQ)
8. Save the agent

#### Step 3: Connect Retell to Twilio (15 min)
1. In Retell dashboard → **Phone Numbers** → **Import Twilio Number**
2. Enter your Twilio Account SID and Auth Token (found in Twilio Console dashboard)
3. Enter the Twilio phone number you bought
4. Retell will automatically configure the Twilio webhook
5. **Test it:** Call the number from your phone. The AI should answer!

#### Step 4: Set Up Google Calendar Integration via n8n (45 min)
1. Go to [n8n.io](https://n8n.io) → Sign up for n8n Cloud (free tier works)
2. Create a new workflow: **"[Client] - Appointment Booking"**
3. Add these nodes in order:

**Node 1: Webhook (Trigger)**
- Type: Webhook
- HTTP Method: POST
- Copy the webhook URL — you'll add this to Retell

**Node 2: Parse Call Data**
- Type: Code (JavaScript)
- Code:
```javascript
const data = $input.first().json;
return [{
  json: {
    callerName: data.caller_name || 'Unknown',
    callerPhone: data.caller_phone || data.from_number,
    service: data.service_requested || 'General',
    preferredDate: data.preferred_date,
    preferredTime: data.preferred_time,
    notes: data.call_summary || ''
  }
}];
```

**Node 3: Google Calendar — Create Event**
- Type: Google Calendar
- Connect your Google account (OAuth)
- Calendar: Select the client's calendar
- Event Title: `{{$json.service}} - {{$json.callerName}}`
- Start Time: `{{$json.preferredDate}} {{$json.preferredTime}}`
- Duration: 60 minutes (adjust per business)
- Description: `Phone: {{$json.callerPhone}}\nService: {{$json.service}}\nNotes: {{$json.notes}}`

**Node 4: Send Notification Email**
- Type: Send Email (or Gmail)
- To: [client's email]
- Subject: "New Appointment Booked: {{$json.callerName}}"
- Body: Include all the appointment details

4. **Activate the workflow**
5. Go back to Retell → Agent Settings → **Custom Functions** → Add a function that sends a POST to your n8n webhook with the appointment data

#### Step 5: Configure Retell Custom Function for Booking (20 min)
1. In Retell → your agent → **Functions**
2. Create function: `book_appointment`
3. Description: "Book an appointment for the caller"
4. Parameters:
   - `caller_name` (string, required)
   - `caller_phone` (string, required)
   - `service_requested` (string, required)
   - `preferred_date` (string, required)
   - `preferred_time` (string, required)
5. Webhook URL: Paste your n8n webhook URL
6. Method: POST

#### Step 6: Set Up Weekly Summary Report via n8n (30 min)
1. Create new n8n workflow: **"[Client] - Weekly Call Summary"**
2. **Trigger:** Schedule → Every Monday at 9am
3. **Node:** Retell API → Get call logs for past 7 days
4. **Node:** Code → Summarize (total calls, booked appointments, common questions)
5. **Node:** Send Email → Client gets a clean summary

#### Step 7: Test Everything (30 min)
1. Call the Twilio number → AI should answer
2. Go through a full booking conversation
3. Check Google Calendar → appointment should appear
4. Check client's email → notification should arrive
5. Test in Spanish
6. Test edge cases: "Can I talk to a person?" / wrong number / spam

### ✅ Tier 1 Launch Checklist
- [ ] Twilio number bought and configured
- [ ] Retell agent created with business-specific prompt
- [ ] English + Spanish tested
- [ ] n8n webhook receives call data
- [ ] Google Calendar creates appointments correctly
- [ ] Client gets email notifications for new bookings
- [ ] Weekly summary workflow active
- [ ] Client's existing number forwarded to Twilio number
- [ ] 3 test calls completed successfully
- [ ] Client shown how to check their calendar

---

## 🏗️ TIER 2 BUILD: AI RECEPTIONIST + FOLLOW-UP SYSTEM

**Estimated Build Time:** 7–10 hours (includes Tier 1)
**What client gets:** Everything in Tier 1 + automated SMS/email follow-up + lead CRM

### Additional Steps (on top of Tier 1)

#### Step 8: Set Up Lead Tracking CRM — Google Sheets (30 min)
1. Create a Google Sheet: **"[Client] Lead Tracker"**
2. Column headers:
   - A: Date | B: Name | C: Phone | D: Email | E: Service | F: Call Outcome (Booked/Missed/Inquiry) | G: Follow-Up Status | H: Notes
3. In your n8n booking workflow, add a node BEFORE the calendar node:
   - **Google Sheets → Append Row** → writes every call to the sheet
4. This becomes the CRM — client can see every lead in real time

#### Step 9: Build Follow-Up SMS Sequence in n8n (60 min)

Create new n8n workflow: **"[Client] - Lead Follow-Up"**

This triggers for missed calls or calls that didn't result in a booking.

**The 3-Touch Sequence:**

**Touch 1 — Same Day (within 1 hour of missed call):**
```
Hi [Name], this is [Business Name]! We noticed we missed your call. 
We'd love to help — reply to this text or call us back at [number]. 
We have availability this week! 😊
```

**Touch 2 — Day 3:**
```
Hey [Name]! Just following up from [Business Name]. 
We still have openings this week if you'd like to schedule. 
Reply YES and we'll get you booked! 📅
```

**Touch 3 — Day 7:**
```
Hi [Name], last check-in from [Business Name]! 
We don't want you to miss out. Book anytime at [booking link] 
or reply to this text. We're here when you're ready! 🙌
```

**n8n Workflow Structure:**
1. **Trigger:** Webhook from Retell (when call outcome = missed or no booking)
2. **Node: Wait 1 hour** → then send Touch 1 via Twilio SMS
3. **Node: Wait 3 days** → then send Touch 2 via Twilio SMS
4. **Node: Wait 4 more days** → then send Touch 3 via Twilio SMS
5. **Node: Update Google Sheet** → mark follow-up status after each touch

**Setting up Twilio SMS in n8n:**
1. In n8n, add a **Twilio** node
2. Connect with your Twilio Account SID + Auth Token
3. From: Your Twilio number
4. To: `{{$json.callerPhone}}`
5. Body: The follow-up message

#### Step 10: Build Follow-Up Email Sequence (30 min)

Same logic as SMS, but via email. In the same n8n workflow:
1. Add **SendGrid** nodes (or Gmail nodes) parallel to SMS
2. **Email 1 (Day 1):** "We missed your call — here's how to book"
3. **Email 2 (Day 3):** "Still interested? We have openings this week"
4. **Email 3 (Day 7):** "Last chance to grab this week's availability"

Keep emails SHORT. 3-4 sentences max. Big "BOOK NOW" button linking to Google Calendar booking or the Twilio number.

#### Step 11: Monthly Performance Report (30 min)

Create n8n workflow: **"[Client] - Monthly Report"**
1. **Trigger:** Schedule → 1st of every month at 9am
2. **Node:** Google Sheets → Read all rows from past month
3. **Node:** Code → Calculate:
   - Total inbound calls
   - Calls that booked an appointment
   - Conversion rate
   - Missed calls recovered via follow-up
   - Total follow-up messages sent
4. **Node:** Send Email → Beautiful HTML email to client with these stats

### ✅ Tier 2 Launch Checklist (in addition to Tier 1)
- [ ] Google Sheet CRM created and receiving data
- [ ] 3-touch SMS sequence tested (send to your own phone first!)
- [ ] 3-touch email sequence tested
- [ ] Wait/delay timers working correctly in n8n
- [ ] Follow-up only triggers for missed/unbooked calls (not already-booked)
- [ ] Monthly report workflow scheduled and tested
- [ ] Client shown how to view their CRM sheet

---

## 🏗️ TIER 3 BUILD: FULL AI BUSINESS SYSTEM

**Estimated Build Time:** 12–16 hours (includes Tier 1 + 2)
**What client gets:** Everything in T1 + T2 + outbound lead gen + review automation + strategy sessions

### Additional Steps (on top of Tier 1 + 2)

#### Step 12: Outbound Lead Generation System (2-3 hours)

**What it does:** Scrapes potential customers → finds their email → sends personalized cold email

**n8n Workflow: "[Client] - Outbound Lead Gen"**

1. **Trigger:** Schedule → runs daily or weekly
2. **Node: HTTP Request** → Google Maps API or a scraping tool to find local businesses that could be clients OF your client
   - Example: If client is an HVAC company, scrape real estate agents who might refer HVAC services
   - Or: Scrape local businesses in the client's service area
3. **Node: Code** → Clean and format the data
4. **Node: HTTP Request** → Use an email finder API (Hunter.io, Apollo.io) to find emails
5. **Node: SendGrid** → Send personalized outreach email:

```
Subject: Quick question about [Their Business]

Hi [Name],

I noticed [Their Business] is doing great work in [City]. 
I work with [Client Business Name] — we handle [service] 
in the area and wanted to see if there's an opportunity 
to help each other out.

Would you be open to a quick 5-minute chat?

Best,
[Client Name]
[Client Business]
```

6. **Node: Google Sheets** → Log every outreach + response

#### Step 13: Automated Review Request System (60 min)

**n8n Workflow: "[Client] - Review Requests"**

**Trigger options:**
- Option A: After every completed appointment (check Google Calendar for past events)
- Option B: Manual trigger — client marks a job as complete in Google Sheet

**Workflow:**
1. **Trigger:** Schedule (daily at 6pm) → check Google Calendar for today's completed appointments
2. **Node: Twilio SMS** → Send review request:
```
Hi [Name]! Thanks for choosing [Business Name] today! 🙏

If you had a great experience, we'd really appreciate a quick 
Google review — it helps us a ton!

Leave a review here: [Google Review Link]

Thanks so much!
```
3. **Node: Wait 3 days** → If no review, send a gentle reminder
4. **Node: Google Sheets** → Track who was asked and who reviewed

**Getting the Google Review Link:**
1. Search for the business on Google Maps
2. Click "Write a review" → copy that URL
3. Or use: `https://search.google.com/local/writereview?placeid=[PLACE_ID]`

#### Step 14: Monthly AI Optimization Session (ongoing)
- Review call transcripts in Retell dashboard
- Identify common questions the AI struggled with
- Update the system prompt with better answers
- Add new services/pricing as the business changes
- Adjust the voice or tone based on feedback
- This is a 30-60 min task per client per month

#### Step 15: Quarterly Strategy Call (ongoing)
- Review 3 months of data
- Present: total calls, bookings, follow-up conversions, reviews generated, leads generated
- Discuss: what's working, what needs improvement, new opportunities
- Plan: next quarter's focus areas

### ✅ Tier 3 Launch Checklist (in addition to Tier 1 + 2)
- [ ] Outbound lead gen workflow built and tested
- [ ] Review request SMS workflow active
- [ ] Google Review link tested and working
- [ ] Monthly optimization process documented
- [ ] Quarterly strategy call template ready
- [ ] Full monthly report includes all Tier 3 metrics
- [ ] Client has priority support channel (WhatsApp/text)

---

## 📅 MONTHLY CLIENT MANAGEMENT

### Month 1 (Launch Month)
- [ ] Days 1–7: Build everything
- [ ] Days 8–10: Internal testing (call 10+ times, test every scenario)
- [ ] Day 11: Soft launch — forward 50% of calls to AI
- [ ] Day 14: Full launch — all calls go to AI
- [ ] Day 15: Check-in call with client — "How's it going?"
- [ ] Day 21: Review first week of live data, make adjustments
- [ ] Day 30: 30-day optimization call — show results, make improvements

### Month 2
- [ ] Review all call transcripts from month 1
- [ ] Update AI prompt based on common issues
- [ ] Send monthly report (Tier 2+)
- [ ] Check follow-up sequence performance (Tier 2+)
- [ ] Optimize SMS/email copy if needed
- [ ] Quick check-in message to client

### Month 3+
- [ ] Monthly report + optimization (always)
- [ ] Quarterly strategy call (Tier 3)
- [ ] Review and update AI knowledge base
- [ ] Check for new services/pricing changes
- [ ] Look for upsell opportunities (Tier 1 → Tier 2, etc.)

### What the Monthly Report Looks Like

**Subject: "[Business Name] AI Performance Report — [Month Year]"**

Include:
1. **Total Calls Handled:** X
2. **Appointments Booked:** X (Y% conversion)
3. **Missed Calls Recovered (Tier 2+):** X
4. **Follow-Up Messages Sent (Tier 2+):** X SMS, X emails
5. **Reviews Requested (Tier 3):** X → Y new reviews
6. **Leads Generated (Tier 3):** X outreach → Y responses
7. **Top Questions Asked:** List the 5 most common questions
8. **Recommendations:** What to improve next month

### How to Handle Issues/Complaints

1. **"The AI said something wrong"**
   - Pull the call transcript from Retell
   - Fix the prompt immediately
   - Apologize to client, show the fix
   - Follow up in 48 hours to confirm it's resolved

2. **"It's not booking appointments correctly"**
   - Check n8n workflow logs for errors
   - Test the webhook manually
   - Check Google Calendar permissions
   - Fix and re-test

3. **"I want to cancel"**
   - Ask why — most issues are fixable
   - Offer a free month of optimization
   - If they insist: process cancellation per contract (30 days)
   - Keep it professional — they might come back or refer someone

---

## 🚀 DAILY LEAD GENERATION SYSTEM

### The Pipeline That Gets You to $20K/Month

You have TWO lead generation channels running simultaneously:

---

### Channel 1: Automated Cold Email (VPS Outreach Machine)

**What's running:** Your VPS scrapes Google Maps for service businesses → finds owner emails → sends personalized cold email sequences automatically at 8am Mon-Fri.

**Daily output:** 12-16 emails/day (60-80/week)
**Expected response rate:** 3-5%
**Expected demo calls from email:** 2-4/week

**The email sequence (3-touch):**

**Email 1 (Day 1):**
```
Subject: [Business Name] — are you losing calls after hours?

Hi [Name],

I checked out [Business Name] and it looks like you're doing 
great work. Quick question — do you know how many calls you 
miss when you're busy or after hours?

Most [industry] businesses lose 30-40% of inbound calls. 
We built an AI system that answers every call 24/7 and books 
appointments directly into your calendar.

Would you be open to a quick 15-min call to see if it'd 
work for [Business Name]?

— Arturo
Viora AI | viora-co.com
```

**Email 2 (Day 3):**
```
Subject: Re: [Business Name] — are you losing calls after hours?

Hey [Name], just bumping this up. 

We recently helped a barbershop capture 70+ appointments in 
30 days from calls they were already missing.

Happy to show you a quick demo — takes 15 min.

Book a time here: [booking link]

— Arturo
```

**Email 3 (Day 7):**
```
Subject: Re: [Business Name] — last one from me

[Name] — don't want to be annoying, so this is my last note.

If you ever want to see how AI can answer your calls and 
book appointments 24/7, the offer stands: [booking link]

Either way, wishing you a great rest of the week! 🙌

— Arturo
```

---

### Channel 2: LinkedIn DMs (Manual — 40/day)

**Daily target:** 40 DMs per day, Mon-Fri
**Weekly total:** 200 DMs
**Expected response rate:** 8-12%
**Expected demo calls from LinkedIn:** 3-5/week

**DM Template:**
```
Hey [Name]! I saw you run [Business Name] — looks great.

Quick question: do you know roughly how many calls you 
miss when you're on a job or after hours?

I help service businesses like yours set up AI that 
answers every call 24/7 and books appointments automatically. 

No pressure — just curious if that's something you'd 
find useful?
```

**Follow-up DM (Day 3 if no response):**
```
Hey [Name], no worries if you're busy! Just wanted to 
mention — we helped a barbershop capture 70+ extra 
appointments in a month from calls they were already missing.

Happy to do a quick 15-min call to see if it'd work 
for you. Either way, keep crushing it! 💪
```

**Who to target:**
- Barbershop owners
- HVAC company owners
- Plumbing company owners
- Med spa owners
- Real estate agents
- Dental practice managers
- Fitness center owners
- Any service business with a phone number

---

### 📊 PIPELINE MATH: How You Get to $20K/Month

**Weekly Activity:**
| Channel | Volume | Response Rate | Demo Calls |
|---------|--------|--------------|------------|
| Cold Email | 60-80/week | 3-5% | 2-4 |
| LinkedIn DMs | 200/week | 8-12% | 3-5 |
| **Total** | **260-280/week** | — | **5-9 demo calls/week** |

**Conversion Funnel:**
| Stage | Number | Rate |
|-------|--------|------|
| Demo calls/week | 5-9 | — |
| Close rate | 20-30% | — |
| **New clients/week** | **1-2** | — |
| **New clients/month** | **4-8** | — |

**Revenue Build-Up (Conservative — all Tier 1 at $350/mo + $1,500 setup):**

| Month | New Clients | Total Clients | Monthly Recurring | Setup Revenue | Total Revenue |
|-------|------------|---------------|-------------------|---------------|---------------|
| Month 1 | 4 | 4 | $1,400 | $6,000 | $7,400 |
| Month 2 | 4 | 8 | $2,800 | $6,000 | $8,800 |
| Month 3 | 5 | 13 | $4,550 | $7,500 | $12,050 |
| Month 4 | 5 | 18 | $6,300 | $7,500 | $13,800 |
| Month 5 | 5 | 23 | $8,050 | $7,500 | $15,550 |
| Month 6 | 5 | 28 | $9,800 | $7,500 | $17,300 |
| **Month 7** | **5** | **33** | **$11,550** | **$7,500** | **$19,050** |
| **Month 8** | **5** | **38** | **$13,300** | **$7,500** | **$20,800** ✅ |

**With Tier Mix (more realistic — some Tier 2 and 3):**

| Month | New Clients | Avg Setup | Avg Monthly | Recurring Base | Total |
|-------|------------|-----------|-------------|----------------|-------|
| Month 1 | 4 | $2,000 avg | $550 avg | $2,200 | $10,200 |
| Month 2 | 4 | $2,000 avg | $550 avg | $4,400 | $12,400 |
| Month 3 | 5 | $2,000 avg | $550 avg | $7,150 | $17,150 |
| **Month 4** | **5** | **$2,000** | **$550** | **$9,900** | **$19,900** ✅ |

**$20K/month is realistic by month 4-8** depending on tier mix.

**Key insight:** Every client you close is RECURRING revenue. Month over month, your base grows while your effort stays the same. By month 8, even if you stop selling, you're collecting $13K+/mo from existing clients.

---

### 🎯 Daily Schedule for Lead Gen

**Monday - Friday:**
| Time | Activity |
|------|----------|
| 8:00 AM | Automated emails send (already running on VPS) |
| 9:00-10:00 AM | Send 40 LinkedIn DMs |
| 10:00-10:30 AM | Reply to yesterday's responses (email + LinkedIn) |
| 10:30 AM-12:00 PM | Demo calls (book these in the 10:30-12 window) |
| 1:00-2:00 PM | Client work (building, optimizing) |
| 2:00-2:30 PM | Follow up on any warm leads |

**Saturday-Sunday:** Rest. Automated emails don't send on weekends. Let LinkedIn DMs marinate.

---

## 🏆 HOW TO OVERDELIVER (What to Do Each Month)

### Month 1 — First Impressions Matter
- Send a "welcome package" email (use onboarding doc)
- Call them on day 7 to check in (even if everything's fine)
- Send a screenshot of the first few AI-handled calls
- Send the 30-day optimization report with enthusiasm

### Month 2+ — Be the Partner, Not the Vendor
- Send monthly report without being asked
- Proactively suggest improvements ("I noticed callers keep asking about X — I updated the AI to handle that")
- Share a quick tip or industry insight
- Ask for a Google review after month 2 (they're happy by now)
- Ask for referrals — "Know anyone else who could use this?"

### Tier 3 Extras
- Monthly strategy call — come prepared with data and recommendations
- Quarterly deep dive — present a full ROI analysis
- Priority response — reply to their messages within 2 hours during business hours

---

## 🔧 TROUBLESHOOTING

### "Retell agent isn't answering calls"
1. Check Twilio → is the webhook URL pointing to Retell?
2. Check Retell → is the agent active and the phone number connected?
3. Test: call the number from a different phone
4. Check Retell dashboard → look at call logs for errors

### "n8n workflow isn't triggering"
1. Check if the workflow is **activated** (toggle at top)
2. Check the webhook URL matches what's in Retell
3. Look at n8n execution logs for errors
4. Test the webhook manually with Postman or curl

### "Google Calendar isn't creating events"
1. Check Google Calendar OAuth connection in n8n
2. Make sure the date/time format matches what Google expects
3. Check Calendar permissions — is n8n allowed to create events?
4. Test with a hardcoded date first to isolate the issue

### "SMS not sending"
1. Check Twilio balance (needs funds)
2. Check the "From" number is SMS-capable
3. Check phone number format (+1XXXXXXXXXX)
4. Look at Twilio logs for error messages

---

*This cheat sheet is your bible. Follow it step by step and you can't go wrong. When in doubt, test everything with your own phone number first before going live with a client.*
