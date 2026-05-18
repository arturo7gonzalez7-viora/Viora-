# Sophia's Over-Talking Fix - Retell AI Prompt Update

## Problem
Sophia says too much when confirming appointments:
❌ **Current:** "tomorrow we have your appointment Saturday at two February 21, 2026"

## Solution
Update Sophia's prompt in Retell AI to be more concise:

---

## UPDATED RETELL AI PROMPT:

### Confirmation Style (ADD THIS SECTION):
When confirming appointments, be brief and natural:
- Say "Your appointment is [day] at [time]"  
- Don't repeat the date if you just said "tomorrow" or "this [day]"
- Use simple time format: "2 PM" not "two" or full dates
- Keep confirmations under 10 words when possible

### Examples:
✅ **Good:** "Your appointment is tomorrow Saturday at 2 PM"
✅ **Good:** "Your appointment is Saturday at 2 PM"  
✅ **Good:** "See you Saturday at 2!"
❌ **Bad:** "tomorrow we have your appointment Saturday at two February 21, 2026"

---

## CURRENT PROMPT SECTION TO UPDATE:

**Find this section in Retell AI:**
> When confirming appointments, provide full details including the day, date, and time with complete information.

**Replace with:**
> When confirming appointments, be concise and natural. Say "Your appointment is [day] at [time]" - avoid repeating dates unnecessarily.

---

## Implementation Steps:
1. Log into Retell AI dashboard
2. Find Next Step Kitchens agent (Sophia)
3. Go to Agent Configuration → Prompt
4. Locate the confirmation instructions
5. Replace verbose instructions with concise ones
6. Test with a booking to verify shorter responses

## Test Cases:
- Book for "tomorrow" → Should not say the full date
- Book for specific day → Should just say the day + time
- All confirmations should be under 15 words