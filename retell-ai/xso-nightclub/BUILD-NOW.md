# XSO AI Receptionist - 1 HOUR BUILD GUIDE

**Goal:** Working demo in 60 minutes
**Strategy:** Demo mode first (simplified webhooks), upgrade to real calendar later

---

## ⏱️ TIMELINE

- **0-20 min:** Make.com webhook setup (demo mode)
- **20-35 min:** Retell agent creation
- **35-50 min:** Import prompt + functions, configure voice
- **50-60 min:** Test calls and iterate

---

## 🚀 PHASE 1: Make.com Setup (20 min)

### What You're Building
4 webhook scenarios that return demo responses (no real calendar yet - just testing the agent)

### Step 1: Create Make.com Account
1. Go to https://make.com
2. Sign up (free plan is fine for demo)
3. Click "Create a new scenario"

---

### Webhook 1: check_availability (5 min)

**Purpose:** Tell the agent if a table is available

1. Click "+" → Search "Webhook" → Select "Custom webhook"
2. Click "Add" → Name it "check_availability_xso"
3. Click "Copy address to clipboard" - **SAVE THIS URL** (you'll need it for Retell)
4. Click "OK"
5. Right-click the webhook → "Run this module only"
6. In another tab, test it by visiting the webhook URL - should say "Accepted"
7. Go back to Make.com - click the webhook module, you'll see the test data
8. Click "+" after webhook → Search "HTTP" → Select "Make a request"
9. Configure the HTTP response:
   - **URL:** Leave blank (this is a response)
   - Click "Show advanced settings"
   - **Status code:** 200
   - **Body:**
   ```json
   {
     "available": true,
     "message": "Table available for your party",
     "alternative_times": []
   }
   ```
   - **Headers:** Add one:
     - Name: `Content-Type`
     - Value: `application/json`

10. Click "OK"
11. Turn scenario ON (toggle at bottom left)
12. **SAVE THE WEBHOOK URL** - label it "check_availability"

---

### Webhook 2: create_reservation (5 min)

1. Create new scenario (click "Create a new scenario" from dashboard)
2. Add Custom webhook → Name: "create_reservation_xso"
3. Copy webhook URL and **SAVE IT**
4. Click "OK" → Run module only → Visit URL in browser to generate sample data
5. Add HTTP response after webhook:
   - Status: 200
   - Body:
   ```json
   {
     "success": true,
     "booking_id": "XSO-DEMO-{{now}}",
     "message": "Reservation created successfully",
     "confirmation_sent": true
   }
   ```
   - Headers: `Content-Type: application/json`

6. Turn scenario ON
7. **SAVE THE WEBHOOK URL** - label it "create_reservation"

---

### Webhook 3: send_confirmation (5 min)

1. Create new scenario
2. Add Custom webhook → Name: "send_confirmation_xso"
3. Copy and **SAVE** webhook URL
4. Add HTTP response:
   - Status: 200
   - Body:
   ```json
   {
     "success": true,
     "email_sent": true,
     "sms_sent": true,
     "message": "Confirmation sent to guest"
   }
   ```
   - Headers: `Content-Type: application/json`

5. Turn scenario ON
6. **SAVE THE WEBHOOK URL** - label it "send_confirmation"

---

### Webhook 4: get_event_info (5 min)

1. Create new scenario
2. Add Custom webhook → Name: "get_event_info_xso"
3. Copy and **SAVE** webhook URL
4. Add HTTP response:
   - Status: 200
   - Body:
   ```json
   {
     "event_name": "Glam Saturday",
     "event_type": "Latin Party Night",
     "door_time": "10:00 PM",
     "music": "Reggaeton, Bachata, Salsa",
     "special_guest": "TBA"
   }
   ```
   - Headers: `Content-Type: application/json`

5. Turn scenario ON
6. **SAVE THE WEBHOOK URL** - label it "get_event_info"

---

### ✅ Make.com Checklist
By now you should have **4 webhook URLs** saved:
- [ ] check_availability webhook URL
- [ ] create_reservation webhook URL  
- [ ] send_confirmation webhook URL
- [ ] get_event_info webhook URL

All 4 scenarios should be ON (green toggle).

---

## 🎙️ PHASE 2: Retell Agent Setup (15 min)

### Step 1: Create Retell Account (3 min)
1. Go to https://retellai.com
2. Click "Get Started" or "Sign Up"
3. Create account (you get $10 free credits)
4. Verify email if needed

### Step 2: Create New Agent (2 min)
1. Click "Agents" in left sidebar
2. Click "Create Agent" (or "+ New Agent")
3. Name: **XSO Nightclub Receptionist**
4. Click "Create"

### Step 3: Configure Basic Settings (10 min)

**General Settings:**
- **Agent Name:** XSO Nightclub Receptionist
- **Language:** English
- **Response Type:** Voice (not text)

**Voice Settings:**
- **Provider:** ElevenLabs (or Azure if ElevenLabs not available)
- **Voice:** 
  - **ElevenLabs:** Search for "Valentina" or "Sofia" (warm, Latin-inflected, high energy)
  - **Azure:** Search for "es-MX-DaliaNeural" (Mexican Spanish, clear English)
  - **Must be FEMALE voice**
- **Speed:** 1.0 (moderate)
- **Stability:** 0.75 (high)
- **Similarity:** 0.75 (high)
- Test the voice with: "Hi! Thanks for calling Excesso Nightclub! How can I help you tonight?"

**Advanced Voice Settings (if available):**
- **Responsiveness:** Fast (600ms target)
- **Turn-taking:** High sensitivity (let caller finish)
- **Interruption handling:** Enabled
- **Filler words:** Minimal

---

## 📝 PHASE 3: Import Prompt & Functions (15 min)

### Step 1: Import System Prompt (5 min)

1. In your Retell agent, find "System Prompt" or "General Prompt" section
2. Open `/root/.openclaw/workspace/retell-ai/xso-nightclub/system-prompt.md` 
3. Copy the ENTIRE text between the first set of triple backticks (the big prompt starting with "You are Sofia...")
4. Paste into Retell's prompt field
5. Click "Save"

**Quick verification:** Scroll through and make sure:
- Mentions "Sofia"
- Says "ONE QUESTION AT A TIME"
- Has the business details (phone, address, hours)
- Has the booking flow steps

---

### Step 2: Add Functions (10 min)

1. In Retell agent, find "Functions" or "Tools" section
2. Click "Add Function" or "Create Function"
3. For EACH function below, create one:

---

#### Function 1: check_availability

**Name:** `check_availability`

**Description:** 
```
Check if VIP table is available for specified date, time, and party size
```

**Parameters (JSON Schema):**
```json
{
  "type": "object",
  "properties": {
    "date": {
      "type": "string",
      "description": "Date in YYYY-MM-DD format"
    },
    "time": {
      "type": "string", 
      "description": "Preferred time (e.g. '10:00 PM')"
    },
    "party_size": {
      "type": "integer",
      "description": "Number of people in party"
    }
  },
  "required": ["date", "time", "party_size"]
}
```

**Webhook URL:** [Paste your check_availability webhook from Make.com]

**Method:** POST

Click "Save" or "Add"

---

#### Function 2: create_reservation

**Name:** `create_reservation`

**Description:**
```
Create a new VIP table reservation with guest details
```

**Parameters (JSON Schema):**
```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "Guest first and last name"
    },
    "phone": {
      "type": "string",
      "description": "Guest phone number"
    },
    "email": {
      "type": "string",
      "description": "Guest email address"
    },
    "party_size": {
      "type": "integer",
      "description": "Number of people"
    },
    "date": {
      "type": "string",
      "description": "Reservation date (YYYY-MM-DD)"
    },
    "time": {
      "type": "string",
      "description": "Reservation time"
    },
    "special_requests": {
      "type": "string",
      "description": "Any special requests or notes"
    }
  },
  "required": ["name", "phone", "email", "party_size", "date", "time"]
}
```

**Webhook URL:** [Paste your create_reservation webhook]

**Method:** POST

Save.

---

#### Function 3: send_confirmation

**Name:** `send_confirmation`

**Description:**
```
Send email and SMS confirmation to guest
```

**Parameters (JSON Schema):**
```json
{
  "type": "object",
  "properties": {
    "booking_id": {
      "type": "string",
      "description": "Booking reference ID"
    },
    "email": {
      "type": "string",
      "description": "Guest email"
    },
    "phone": {
      "type": "string",
      "description": "Guest phone"
    }
  },
  "required": ["booking_id", "email", "phone"]
}
```

**Webhook URL:** [Paste your send_confirmation webhook]

**Method:** POST

Save.

---

#### Function 4: get_event_info

**Name:** `get_event_info`

**Description:**
```
Get event details for a specific date or day of week
```

**Parameters (JSON Schema):**
```json
{
  "type": "object",
  "properties": {
    "date": {
      "type": "string",
      "description": "Date to check (YYYY-MM-DD) or day name (e.g. 'Saturday')"
    }
  },
  "required": ["date"]
}
```

**Webhook URL:** [Paste your get_event_info webhook]

**Method:** POST

Save.

---

### ✅ Functions Checklist
You should now have 4 functions configured:
- [ ] check_availability (with your Make.com webhook)
- [ ] create_reservation (with your Make.com webhook)
- [ ] send_confirmation (with your Make.com webhook)
- [ ] get_event_info (with your Make.com webhook)

---

## 🧪 PHASE 4: Testing (10 min)

### Get Your Test Number

1. In Retell dashboard, find your agent
2. Look for "Test Number" or "Phone Number" section
3. Copy the test phone number (format: +1-XXX-XXX-XXXX)
4. **SAVE THIS** - this is how you'll call Sofia

### Test Scenarios (Run These)

**Call the test number and try:**

#### Test 1: Simple Booking (3 min)
- Call number
- Wait for Sofia: "Hi! Thanks for calling Excesso Nightclub! How can I help you tonight?"
- Say: "I'd like to book a VIP table"
- Follow her questions ONE AT A TIME:
  - Name: "John Smith"
  - Phone: "303-555-1234"
  - Email: "john@example.com"
  - Party size: "4"
  - Date: "This Saturday" (she should confirm the date)
  - Time: "10 PM"
- She should check availability, create booking, send confirmation, and give you a booking ID

**✅ What to check:**
- Does she ask ONE question at a time? (Critical!)
- Does she sound high-energy and friendly?
- Does she wait for your answer before moving on?
- Does she successfully complete the booking?
- Does she say "Awesome!" "Perfect!" naturally?

#### Test 2: Event Question (2 min)
- Call again
- Say: "What's happening Saturday night?"
- She should tell you about Glam Saturday event
- Then ask if you want to book a table

#### Test 3: Policy Question (2 min)
- Call again
- Ask: "What's the dress code?"
- She should explain upscale attire naturally
- Ask: "What time do you open?"
- She should explain door time

#### Test 4: Transfer Request (1 min)
- Call again
- Say: "Can I speak to a person?"
- She should immediately say "Of course! Let me transfer you right now" and transfer

---

## 🐛 TROUBLESHOOTING

### Sofia Asks Multiple Questions at Once
**Fix:** Go back to system prompt in Retell, make sure this text is there:
```
CRITICAL: ASK ONE QUESTION AT A TIME
- Never ask multiple questions in one response
- Wait for the caller to answer before moving to the next question
```

Also check voice settings → Turn-taking sensitivity = HIGH

### Functions Not Working
1. Test your Make.com webhooks directly in browser
2. Make sure all 4 scenarios are ON (green toggle)
3. Check webhook URLs in Retell functions match Make.com URLs exactly
4. Look at Make.com execution history to see if webhook was called

### Voice Sounds Robotic or Low-Energy
1. Try different voice in Retell:
   - ElevenLabs: "Valentina" or "Nova"
   - Azure: "es-MX-DaliaNeural"
2. Adjust settings:
   - Stability: 0.5-0.75 (lower = more variation)
   - Expressiveness: High
   - Speed: 1.0-1.1

### Agent Not Following Prompt
- Make sure you pasted the FULL system prompt (it's long!)
- Save and wait 30 seconds for changes to propagate
- Try a fresh call (previous call context might interfere)

---

## ✅ DEMO CHECKLIST

Before showing to client:

- [ ] Agent answers calls with Sofia's greeting
- [ ] Voice is female, high-energy, friendly
- [ ] Asks ONE question at a time and waits
- [ ] Can complete a full booking (collects all info)
- [ ] Functions work (check availability, create reservation, send confirmation)
- [ ] Can answer policy questions (dress code, hours, age)
- [ ] Can answer event questions
- [ ] Transfers when asked
- [ ] Sounds natural and human-like (uses "Awesome!", "Perfect!", etc.)
- [ ] Says "Excesso" not "X-S-O"

---

## 🎯 NEXT STEPS (After Demo)

**If client approves:**

1. **Upgrade Make.com webhooks** to real calendar integration:
   - Connect Google Calendar or Tablelist API
   - Add real email/SMS sending (Twilio, SendGrid)
   - Add availability checking logic

2. **Get real phone number:**
   - Buy number through Retell or Twilio
   - Forward XSO's existing number to AI agent

3. **Advanced features:**
   - Multi-language support (full Spanish)
   - Knowledge base upload (FAQ document)
   - Call analytics dashboard
   - CRM integration

4. **Testing & QA:**
   - Run full testing suite (20 scenarios)
   - Soft launch (test number for staff first)
   - Monitor first 100 calls
   - Iterate based on feedback

---

## 📞 RETELL SUPPORT

If you get stuck:
- **Docs:** https://docs.retellai.com
- **Discord:** https://discord.gg/retellai
- **Support:** support@retellai.com

---

## 💾 FILES YOU NEED

All in: `/root/.openclaw/workspace/retell-ai/xso-nightclub/`

- `system-prompt.md` - Copy the prompt from here
- `functions.json` - Reference for function schemas
- `business-profile.md` - All XSO details if you need to reference
- `testing-guide.md` - Full testing scenarios for later

---

**GO TIME! 🚀**

Start with Make.com webhooks, then Retell setup, then test. You got this, twin!
