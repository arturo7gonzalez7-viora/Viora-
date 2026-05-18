# Voice Selection Guide for XSO Nightclub Agent

**Target:** Female voice with subtle Latin accent, bilingual (English primary/Spanish secondary), clear and professional

---

## Quick Selection Process

### Step 1: Filter in Retell Dashboard
When creating your agent, go to Voice settings and filter:
- **Gender:** Female
- **Language:** Look for "Bilingual" or "Spanish/English" tags
- **Provider:** Try ElevenLabs first (best for accents), then Azure, then Play.ht

### Step 2: Preview with These Test Phrases

**English (must sound clear, professional, welcoming):**
```
"Hi, thanks for calling Excesso Nightclub! How can I help you tonight?"
"Your VIP table is reserved for Saturday at 10 PM for 4 guests."
"We require upscale nightlife attire and valid photo ID for all guests."
```

**Spanish (must sound natural, not robotic):**
```
"¡Hola! Bienvenido a Excesso. ¿En qué puedo ayudarte?"
"¿Para cuántas personas?"
"Perfecto, tu mesa está reservada."
```

**Mixed (code-switching - common in Denver Latin nightclub scene):**
```
"Hi, thanks for calling Excesso! We have A Poca Luz tonight - reggaeton old school. ¿Te gustaría hacer una reservación?"
```

**Pronunciation Check:**
```
"XSO" should sound like "excesso" (ex-SESS-oh), NOT "X-S-O" spelled out.
```

### Step 3: Evaluate

Rate each voice on:
- **Clarity (critical):** Can you understand every word clearly? (Must be 9/10+)
- **Accent (important):** Is there a subtle Latin accent present? (Target: 5-7/10 accent strength)
- **Energy (important):** Does it match nightclub vibe - friendly, upscale, welcoming? (Target: 7/10)
- **Naturalness (critical):** Does it sound like a real person, not a robot? (Must be 8/10+)
- **Bilingual flow (nice to have):** Does Spanish sound as natural as English? (Target: 7/10+)

---

## Recommended Voices by Provider

### 🏆 ElevenLabs (Best for Natural Accent)

**Top picks:**
1. **"Valentina"** - Warm Mexican/Latin accent, excellent English clarity, professional tone
2. **"Sofia"** - Colombian-influenced, friendly, good energy
3. **"Isabella"** - General Latin, slightly more formal
4. **"Maria"** - Clear Spanish, very good English

**How to test in Retell:**
- Voice provider: ElevenLabs
- Search: "Valentina" or browse bilingual/Spanish voices
- Preview with test phrases above

---

### 🥈 Azure Neural Voices (Excellent Quality, Free Tier)

**Top picks:**
1. **"es-MX-DaliaNeural"** - Mexican Spanish, crystal clear English, professional
2. **"es-CO-SalomeNeural"** - Colombian accent, warm tone, good phone quality
3. **"es-US-PalomaNeural"** - US Latina, very clear English, subtle accent
4. **"es-MX-CarlotaNeural"** - Mexican, friendly, good energy

**Settings to adjust in Retell:**
- Voice provider: Azure
- Language: Spanish (Mexico) or Spanish (Colombia)
- Test English phrases to confirm clarity

---

### 🥉 Play.ht (Good Alternative)

**Top picks:**
1. **"Lucia"** - Latin American Spanish, clear English
2. **"Camila"** - Warm, friendly, bilingual
3. Search for: "Spanish female bilingual" in Play.ht voice library

---

## Voice Tuning Settings (in Retell)

Once you pick a voice, adjust these:

### Stability/Consistency
- Set to: **Medium-High (70-80%)**
- Why: Keeps voice consistent across long calls

### Clarity/Similarity
- Set to: **High (80-90%)**
- Why: Ensures clear pronunciation, especially on phone

### Speaking Rate
- Set to: **Medium (1.0x)**
- Why: Accent should enhance, not confuse - don't rush

### Pitch
- Set to: **Default or slightly lower** (more professional)
- Avoid: Too high pitch (sounds young/unprofessional)

### Emotional Range
- Set to: **Medium (50-60%)**
- Why: Friendly and warm, but not overly dramatic

---

## Testing Checklist

Before finalizing voice, test these scenarios:

**Call 1: English booking**
- [ ] "Hi, I'd like to book a table for Saturday."
- [ ] Does she sound welcoming?
- [ ] Is English pronunciation clear?
- [ ] Does accent feel subtle and natural?

**Call 2: Spanish greeting**
- [ ] "Hola, quiero hacer una reservación."
- [ ] Does she switch to Spanish smoothly?
- [ ] Does Spanish sound natural (not Google Translate robotic)?

**Call 3: Information query**
- [ ] "What's your dress code?"
- [ ] Does she sound professional explaining policies?
- [ ] Is tone appropriate (not too casual, not too formal)?

**Call 4: Phone quality check**
- [ ] Call the test number from your actual phone (not computer)
- [ ] Does voice quality degrade on phone line?
- [ ] Is accent still subtle (not stronger on phone)?

**Call 5: Long response**
- [ ] Ask: "Tell me about this Friday's event"
- [ ] Does she maintain energy through longer explanation?
- [ ] Does voice stay consistent (not robotic or monotone)?

---

## Common Pitfalls to Avoid

❌ **Too much accent** - English becomes hard to understand
- Fix: Choose voice with lighter accent (aim for 5-7/10, not 9/10)

❌ **Robotic Spanish** - Spanish sounds like text-to-speech
- Fix: Choose native Spanish voice, not English voice trying Spanish

❌ **Energy mismatch** - Sounds too formal or too bubbly
- Fix: XSO is upscale nightclub, not bank or kids party - find that middle ground

❌ **Inconsistent across calls** - Voice changes pitch/tone call-to-call
- Fix: Increase stability setting in Retell

❌ **Loses quality on phone** - Sounds great in dashboard preview, flat on actual call
- Fix: Always test with real phone call before finalizing

---

## Quick Decision Matrix

**If you value clarity above all:**
→ Azure "es-MX-DaliaNeural" (Mexican Spanish, perfect English)

**If you want most natural accent:**
→ ElevenLabs "Valentina" (warm, authentic, bilingual)

**If you need best phone quality:**
→ Azure voices (optimized for telephony)

**If you want friendly/high-energy:**
→ ElevenLabs "Sofia" (Colombian, upbeat, welcoming)

**If budget matters:**
→ Azure (included in many plans) or Retell's default voices

---

## Final Recommendation

**Start with:** ElevenLabs "Valentina" or Azure "es-MX-DaliaNeural"

**Why:**
- Both have subtle, natural Latin accent
- Excellent English clarity (critical for phone)
- Professional tone matches upscale nightclub
- Good bilingual capability
- Proven track record in production voice agents

**Test both with 3-5 calls, pick whichever sounds better on YOUR actual phone.**

**Critical: Make sure "XSO" is pronounced "excesso" (ex-SESS-oh) in test calls!**

---

## Voice Settings to Copy/Paste into Retell

```json
{
  "voice_provider": "elevenlabs",
  "voice_id": "valentina",
  "stability": 0.75,
  "clarity": 0.85,
  "speaking_rate": 1.0,
  "enable_ssml": true,
  "language": "en-US",
  "secondary_language": "es-MX"
}
```

Or for Azure:

```json
{
  "voice_provider": "azure",
  "voice_name": "es-MX-DaliaNeural",
  "speaking_rate": 1.0,
  "pitch": "default",
  "language": "es-MX"
}
```

---

**Next Step:** Open Retell dashboard → Create Agent → Voice Settings → Test these voices → Pick winner → Save

---

**Pro Tip:** Record a test call with each top candidate and send to a friend/team member - ask "does this sound like a real receptionist at an upscale Latin nightclub?" Pick the one that gets "yes, sounds real" responses.
