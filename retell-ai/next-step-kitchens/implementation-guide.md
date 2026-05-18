# Next Step Kitchens - Implementation Guide

## Quick Summary
System is 95% complete! Just need these 3 fixes:

1. **Calendar Duration** → Fix end time calculation (3 hours → 1 hour)
2. **Email Time Display** → Replace broken moment() with native Date()  
3. **Sophia Over-Talking** → Update Retell AI prompt to be concise

---

## Implementation Order

### Step 1: Calendar Duration Fix (n8n) 🗓️
**Location:** n8n workflow → Calendar Event node  
**Fix:** Replace end time calculation

```javascript
// Current (showing 3 hours):
end: startTime + 3 hours

// Fixed (showing 1 hour):
const startTime = new Date($json.appointmentDateTime);
const endTime = new Date(startTime.getTime() + (60 * 60 * 1000));
```

**Test:** Book appointment for 2:00 PM → Calendar should show 2:00-3:00 PM ✅

### Step 2: Email Time Fix (n8n) 📧
**Location:** n8n workflow → Email template preparation node

```javascript
// Add this before email nodes:
const appointmentTime = new Date($json.appointmentDateTime);
const displayTime = appointmentTime.toLocaleTimeString('en-US', {
  hour: 'numeric',
  minute: '2-digit', 
  timeZone: 'America/Denver',
  hour12: true
});

return {
  json: {
    ...$json,
    displayDateTime: `${displayTime} (Mountain Time)`
  }
};
```

**Update Email Templates:**
- Replace: `{{moment(appointmentTime).format('h:mm A')}} (Mountain Time)`
- With: `{{displayDateTime}}`

**Test:** Email should show "2:00 PM (Mountain Time)" ✅

### Step 3: Sophia Prompt Fix (Retell AI) 🤖
**Location:** Retell AI Dashboard → Agent Configuration

**Current prompt section:**
> When confirming appointments, provide full details including the day, date, and time with complete information.

**Replace with:**
> When confirming appointments, be concise and natural. Say "Your appointment is [day] at [time]" - avoid repeating dates unnecessarily.

**Test:** Sophia should say "Your appointment is Saturday at 2 PM" ✅

---

## Testing Protocol

Use these test details for all 3 fixes:
- **Customer:** Chris  
- **Phone:** 12345678910
- **Email:** chris@test.com
- **Appointment:** Saturday Feb 21 at 2:00 PM

### Expected Results After Fixes:
1. **Calendar Event:** 2:00-3:00 PM (1 hour duration)
2. **Customer Email:** "2:00 PM (Mountain Time)" appears correctly
3. **Dani Email:** "2:00 PM (Mountain Time)" appears correctly  
4. **Sophia Confirmation:** "Your appointment is Saturday at 2 PM"

### Success Criteria:
- ✅ No 3-hour appointments in calendar
- ✅ No "(Mountain Time)" without actual time in emails
- ✅ No verbose date repetition in AI confirmations
- ✅ All 3 components working together smoothly

---

## File References:
- `calendar-duration-fix.js` → Copy into n8n Calendar Event node
- `email-time-fix.js` → Add new JavaScript node before emails
- `sophia-prompt-fix.md` → Update Retell AI agent prompt

**Status:** Ready to implement → 100% completion! 🚀