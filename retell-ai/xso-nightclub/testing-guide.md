# XSO Nightclub AI Receptionist - Testing Guide

**Version:** 1.0
**Last Updated:** 2026-02-13

---

## Testing Philosophy

Before deploying to production, test:
1. **Happy paths** - Everything works perfectly
2. **Alternative paths** - User makes different choices
3. **Error scenarios** - System failures and edge cases
4. **Transfer triggers** - When human intervention is needed
5. **Conversation flow** - Natural dialog patterns

**Goal:** 95%+ success rate on bookings before soft launch

---

## Test Scenarios (20 Core Tests)

### Category 1: Happy Path Bookings (Tests 1-5)

#### Test 1: Simple Weekend Booking
**User says:** "Hi, I'd like to book a VIP table for Saturday night."

**Expected flow:**
1. Agent: Asks for party size
2. User: "4 people"
3. Agent: Asks for time
4. User: "10 PM"
5. Agent: Asks for name
6. User: "Maria Rodriguez"
7. Agent: Asks for phone
8. User: "303-555-1234"
9. Agent: Asks for email
10. User: "maria@example.com"
11. Agent: Checks availability (function call)
12. Agent: Confirms available, reads back details
13. Agent: Creates reservation (function call)
14. Agent: Sends confirmation (function call)
15. Agent: "Perfect! Your VIP table is reserved..."

**Pass criteria:**
- [ ] All information collected correctly
- [ ] Functions called in correct order
- [ ] Booking ID returned
- [ ] Confirmation sent
- [ ] Natural conversation flow

---

#### Test 2: Weeknight Booking with Special Request
**User says:** "I need a table for 6 on Friday at 9:30 PM. It's a birthday, can we get something near the dance floor?"

**Expected flow:**
1. Agent: Acknowledges all details received
2. Agent: Asks for name, phone, email
3. Agent: Checks availability
4. Agent: Confirms and notes special request
5. Agent: Creates reservation with special_requests field populated
6. Agent: Mentions host will accommodate if possible

**Pass criteria:**
- [ ] Special request captured in booking
- [ ] All 6 pieces of info collected
- [ ] Tone is enthusiastic about birthday

---

#### Test 3: Quick Repeat Caller
**User says:** "This is John, I booked last week. I need another table for this Thursday, same time, 4 people."

**Expected flow:**
1. Agent: Asks for confirmation of details (Thursday, time, 4 people)
2. Agent: "What time worked for you last week?"
3. User: "10 PM"
4. Agent: Asks for phone and email to send confirmation
5. Agent: Completes booking

**Pass criteria:**
- [ ] Agent doesn't ask for information user already volunteered
- [ ] Maintains conversational context

---

#### Test 4: Event-Specific Inquiry + Booking
**User says:** "What's happening Friday night?"

**Expected flow:**
1. Agent: "This Friday we have A Poca Luz in the XSO Main Room - reggaeton old school and perreo with DJs Click and RBT. And in the Cielo Room, it's Cielo Friday with hip-hop and R&B. Both rooms open at 9:30 PM. Would you like to book a VIP table?"
2. User: "Yes, for the reggaeton room, 4 people at 10 PM"
3. Agent: Proceeds with booking

**Pass criteria:**
- [ ] get_event_info function called correctly
- [ ] Event details provided accurately
- [ ] Smooth transition to booking

---

#### Test 5: Spanish Speaker
**User says:** "Hola, quiero hacer una reservación para el sábado."

**Expected flow:**
1. Agent: "¡Hola! Bienvenido a XSO. ¿Para cuántas personas?"
2. [Continues in Spanish if agent is capable, otherwise:]
   Agent: "Para mejor servicio en español, déjame transferirte con uno de nuestros representantes bilingües."
3. [Transfer to human]

**Pass criteria:**
- [ ] Recognizes Spanish immediately
- [ ] Attempts Spanish response or transfers smoothly
- [ ] No confusion or awkwardness

---

### Category 2: Alternative Paths (Tests 6-10)

#### Test 6: Time Unavailable - Accept Alternative
**User says:** "I need Saturday at 10 PM for 4."

**Setup:** Mock check_availability to return unavailable

**Expected flow:**
1. Agent: Checks availability
2. Agent: "Saturday at 10 PM is currently booked. I can offer 9:30 PM or 10:45 PM - which works better for you?"
3. User: "9:30 is fine"
4. Agent: Proceeds with booking for 9:30 PM

**Pass criteria:**
- [ ] Alternatives offered clearly
- [ ] Agent updates booking to alternative time
- [ ] Confirmation reflects actual booked time

---

#### Test 7: Time Unavailable - Try Different Day
**User says:** "Saturday at 10."

**Expected flow:**
1. Agent: "Saturday at 10 PM is booked. Would you like to try a different time on Saturday, or check another night?"
2. User: "What about Friday?"
3. Agent: "Let me check Friday at 10 PM... [checks] That's available!"
4. Agent: Proceeds with Friday booking

**Pass criteria:**
- [ ] Gracefully handles day change
- [ ] Re-checks availability for new date

---

#### Test 8: Large Party (>10 people)
**User says:** "I need a table for 15 people next Saturday."

**Expected flow:**
1. Agent: "For parties over 10, I'll need to connect you with our VIP coordinator who can arrange private seating and bottle service for your group. Let me transfer you now."
2. [Transfer to human]

**Pass criteria:**
- [ ] Immediate transfer, no attempt to book
- [ ] Polite explanation

---

#### Test 9: Same-Day Urgent Booking
**User says:** "Can I get a table tonight in 2 hours?"

**Expected flow:**
1. Agent: "For same-day reservations, let me connect you with our host team directly so they can confirm availability and get you set up right away."
2. [Transfer to human]

**Pass criteria:**
- [ ] Recognizes urgency
- [ ] Transfers immediately

---

#### Test 10: Indecisive Caller
**User says:** "I'm thinking about coming this weekend, maybe Friday or Saturday, not sure what time..."

**Expected flow:**
1. Agent: "No problem! Let me help you decide. Friday we have A Poca Luz - reggaeton old school. Saturday is Glam Saturday - Latin party. Both are great. Which music style sounds better?"
2. User: "Reggaeton sounds good"
3. Agent: "Perfect! Friday it is. What time works for you - we have slots from 9 PM to midnight?"
4. [Continues with booking]

**Pass criteria:**
- [ ] Patient and helpful
- [ ] Guides caller to decision
- [ ] Doesn't rush or pressure

---

### Category 3: Information-Only (Tests 11-15)

#### Test 11: Dress Code Question
**User says:** "What's your dress code?"

**Expected flow:**
1. Agent: "We require upscale nightlife attire. Please don't wear athletic gear, sandals, ripped clothing, or oversized fits. Our management makes the final call at the door."
2. Agent: "Would you like to book a VIP table while I have you?"
3. User: "No thanks, just wanted to check"
4. Agent: "No problem! Feel free to call back at 303-674-4060 if you change your mind. Have a great night!"

**Pass criteria:**
- [ ] Clear policy explanation
- [ ] Offers booking opportunity
- [ ] Graceful close if declined

---

#### Test 12: Age/ID Requirements
**User says:** "Do I need to be 21? What ID do you take?"

**Expected flow:**
1. Agent: Provides complete age/ID policy
2. Agent: Mentions what's NOT accepted
3. Agent: Asks if they'd like to book

**Pass criteria:**
- [ ] Complete and accurate info
- [ ] Mentions both accepted and rejected IDs

---

#### Test 13: Parking Question
**User says:** "Where should I park?"

**Expected flow:**
1. Agent: "We don't have our own garage, but there's plenty of parking around Denver Pavilions. I strongly recommend using Uber or Lyft since downtown parking can be tight on busy nights. We're right on the 16th Street Mall - super easy to get to."
2. Agent: "Are you planning to join us soon? I can help you book a VIP table."

**Pass criteria:**
- [ ] Clear parking guidance
- [ ] Recommendation for ride-share
- [ ] Booking offer

---

#### Test 14: Hours Question
**User says:** "What time do you open?"

**Expected flow:**
1. Agent: "Doors typically open between 9 and 10 PM depending on the event, and we close at 2 AM. Which night are you interested in?"
2. User: "Friday"
3. Agent: "Friday doors open at 9:30 PM for A Poca Luz. Last entry is 1:30 AM. Would you like me to reserve a VIP table for you?"

**Pass criteria:**
- [ ] General hours given
- [ ] Asks for specific night to give exact info
- [ ] Ties to event and booking offer

---

#### Test 15: Multiple Questions
**User says:** "I have a few questions - what's the age, dress code, and can I park there?"

**Expected flow:**
1. Agent: "Happy to help! Let me answer all of those..."
2. Agent: Provides all three answers clearly
3. Agent: "Anything else you'd like to know?"
4. User: "No, that's it"
5. Agent: "Great! If you'd like to guarantee entry and skip the line, I can book a VIP table for you right now."

**Pass criteria:**
- [ ] Answers all questions
- [ ] Doesn't rush through
- [ ] Organized response

---

### Category 4: Transfer Triggers (Tests 16-18)

#### Test 16: Request for Human
**User says:** "Can I speak to a real person?"

**Expected flow:**
1. Agent: "Of course! Let me transfer you to our team now."
2. [Immediate transfer, no delay or questions]

**Pass criteria:**
- [ ] Instant transfer
- [ ] No resistance or "I can help you" pushback

---

#### Test 17: Modification Request
**User says:** "I need to change my reservation from last week."

**Expected flow:**
1. Agent: "I'll connect you with our host team who can pull up your reservation and make that change for you right away."
2. [Transfer]

**Pass criteria:**
- [ ] Recognizes modification = transfer
- [ ] Explains why transferring

---

#### Test 18: Frustrated Caller
**User says:** "This is ridiculous, I've been trying to book for 10 minutes and your system isn't working!"

**Expected flow:**
1. Agent: "I'm so sorry you're having trouble. Let me get you directly to our host team right now who can help you immediately."
2. [Transfer with priority flag if possible]

**Pass criteria:**
- [ ] Apologizes
- [ ] Transfers immediately
- [ ] Doesn't argue or defend

---

### Category 5: Edge Cases (Tests 19-20)

#### Test 19: Nonsense Input
**User says:** "Banana purple elephant Tuesday?"

**Expected flow:**
1. Agent: "I'm sorry, I didn't quite catch that. Are you looking to book a VIP table, or do you have a question about XSO?"
2. User: [Continues with nonsense]
3. Agent: "Let me connect you with someone who can better assist you."
4. [Transfer]

**Pass criteria:**
- [ ] Doesn't loop on confusion
- [ ] Offers clear options
- [ ] Transfers if continues

---

#### Test 20: Function Failure
**Setup:** Mock create_reservation to fail

**User says:** "Yes, book it for Saturday at 10 PM, 4 people."

**Expected flow:**
1. Agent: Collects all information
2. Agent: Attempts to create reservation
3. [Function fails]
4. Agent: "I'm having a technical issue with our booking system right now. Let me transfer you to our team who can complete this reservation for you immediately and make sure you're all set."
5. [Transfer]

**Pass criteria:**
- [ ] Detects function failure
- [ ] Doesn't blame caller
- [ ] Transfers with context

---

## Test Recording Template

For each test, record:

```
Test #: ___
Scenario: _______________
Date/Time: _______________
Tester: _______________

PASS / FAIL

Notes:
- What worked well:
- What needs fixing:
- Transcript snippet (if relevant):
- Function calls (check logs):
  □ check_availability
  □ create_reservation
  □ send_confirmation
  □ get_event_info

Follow-up actions:
```

---

## Automated Testing Checklist

Use Retell's built-in simulation tool to run automated tests:

- [ ] Test 1: Simple weekend booking - PASS/FAIL
- [ ] Test 2: Booking with special request - PASS/FAIL
- [ ] Test 3: Repeat caller - PASS/FAIL
- [ ] Test 4: Event inquiry + booking - PASS/FAIL
- [ ] Test 5: Spanish speaker - PASS/FAIL
- [ ] Test 6: Alternative time accepted - PASS/FAIL
- [ ] Test 7: Different day - PASS/FAIL
- [ ] Test 8: Large party - PASS/FAIL
- [ ] Test 9: Same-day urgent - PASS/FAIL
- [ ] Test 10: Indecisive caller - PASS/FAIL
- [ ] Test 11: Dress code question - PASS/FAIL
- [ ] Test 12: Age/ID question - PASS/FAIL
- [ ] Test 13: Parking question - PASS/FAIL
- [ ] Test 14: Hours question - PASS/FAIL
- [ ] Test 15: Multiple questions - PASS/FAIL
- [ ] Test 16: Request human - PASS/FAIL
- [ ] Test 17: Modification request - PASS/FAIL
- [ ] Test 18: Frustrated caller - PASS/FAIL
- [ ] Test 19: Nonsense input - PASS/FAIL
- [ ] Test 20: Function failure - PASS/FAIL

**Target:** 18+ passing before soft launch

---

## Live Testing Phase

After automated tests pass, conduct live testing:

### Phase 1: Internal Testing (Day 1-2)
- Team members call and test
- Friends/family call with various scenarios
- Record and review all calls
- Fix critical issues immediately

### Phase 2: Soft Launch (Day 3-5)
- Enable for after-hours only (2 AM - 5 PM)
- Monitor every call in real-time
- Have human backup standing by
- Iterate daily based on call reviews

### Phase 3: Limited Hours (Day 6-10)
- Enable for business hours (5 PM - 9 PM)
- Overflow to human if agent struggles
- Track booking success rate
- Collect caller feedback

### Phase 4: Full Deployment (Day 11+)
- Enable 24/7
- Monitor metrics weekly
- Maintain human fallback for complex cases
- Update knowledge base monthly

---

## Quality Metrics Dashboard

Track these KPIs:

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Booking success rate | >80% | ___ | 🔴🟡🟢 |
| Transfer rate | <20% | ___ | 🔴🟡🟢 |
| Avg call duration (booking) | 2-4 min | ___ | 🔴🟡🟢 |
| Avg call duration (info) | <2 min | ___ | 🔴🟡🟢 |
| Confirmation delivery rate | >95% | ___ | 🔴🟡🟢 |
| Caller satisfaction | >4/5 | ___ | 🔴🟡🟢 |
| Show rate (booked tables) | >70% | ___ | 🔴🟡🟢 |

---

## Common Failure Patterns & Fixes

### Agent loops on asking for information
**Fix:** Improve system prompt with "do not ask for information the caller already provided" instruction

### Agent doesn't recognize transfer triggers
**Fix:** Add explicit examples in prompt: "If caller says X, immediately transfer"

### Function calls fail silently
**Fix:** Add error detection in prompt: "If function returns error, apologize and transfer"

### Agent sounds robotic
**Fix:** Tune voice settings, add natural language patterns, reduce formality

### Agent gives wrong information
**Fix:** Update knowledge base, add fact-checking step

---

**END OF TESTING GUIDE**

Next: Deployment checklist and go-live procedures.
