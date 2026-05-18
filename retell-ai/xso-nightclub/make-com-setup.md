# Make.com Webhook Setup for XSO Nightclub AI Receptionist

**Purpose:** Connect Retell AI functions to Google Calendar, email, SMS, and CRM

---

## Overview

You'll create 4 Make.com scenarios (webhooks) that handle:
1. **check_availability** - Check if table slot is available
2. **create_reservation** - Create booking in calendar/system
3. **send_confirmation** - Send email + SMS confirmation
4. **get_event_info** - Return upcoming events

---

## Prerequisites

Before starting, have ready:
- [ ] Make.com account (free tier works for demo)
- [ ] Google Calendar access (for demo bookings)
- [ ] Email service (Gmail/SendGrid/other)
- [ ] SMS service (Twilio account + phone number) - optional for demo
- [ ] Google Sheets (for storing reservations) - optional

---

## Scenario 1: check_availability

**Webhook Trigger:** Custom webhook (instant)

### Steps:

1. **Trigger: Webhook**
   - Create a new webhook
   - Copy webhook URL → paste into Retell function definition

2. **Router: Check Date/Time**
   - Parse incoming date and time
   - Convert to America/Denver timezone if needed

3. **Google Calendar: Search Events**
   - Calendar: XSO Bookings (create dedicated calendar)
   - Search query: events on specified date/time
   - Time window: ±2 hours around requested time

4. **Condition: Check Slot Availability**
   - If no conflicting events found → available = true
   - If conflict found → available = false, generate alternatives

5. **Generate Alternatives (if unavailable)**
   - Array of times: -30 min, +30 min, +60 min from requested
   - Filter out conflicting times
   - Return up to 3 alternatives

6. **Response: Webhook Reply**
```json
{
  "available": true|false,
  "alternatives": [
    {"time": "21:30", "room": "XSO Main Room"},
    {"time": "22:30", "room": "Cielo Room"}
  ],
  "message": "Table available at requested time" or "Requested time is booked"
}
```

### Quick Setup (Demo - Always Available)

For demo purposes, you can simplify:

1. **Trigger: Webhook**
2. **Response: Webhook Reply** (always return available = true)
```json
{
  "available": true,
  "alternatives": [],
  "message": "Demo mode - all times available"
}
```

Later, replace with real calendar checking.

---

## Scenario 2: create_reservation

**Webhook Trigger:** Custom webhook (instant)

### Steps:

1. **Trigger: Webhook**
   - Receives: first_name, last_name, phone, email, party_size, date, time, special_requests

2. **Generate Booking ID**
   - Use Make.com function: `{{formatDate(now; "YYYYMMDDHHmmss")}}-{{floor(random * 1000)}}`
   - Example: 20260214223045-742

3. **Generate Confirmation Number**
   - Use Make.com function: `XSO-{{floor(random * 90000 + 10000)}}`
   - Example: XSO-57239

4. **Google Calendar: Create Event**
   - Calendar: XSO Bookings
   - Summary: `VIP Table - {{first_name}} {{last_name}} ({{party_size}} guests)`
   - Start time: {{date}} {{time}} (America/Denver)
   - End time: +2 hours from start
   - Description:
     ```
     VIP Table Reservation
     Name: {{first_name}} {{last_name}}
     Phone: {{phone}}
     Email: {{email}}
     Party Size: {{party_size}}
     Special Requests: {{special_requests}}
     Booking ID: {{booking_id}}
     Confirmation #: {{confirmation_number}}
     ```
   - Add guests: {{email}}

5. **Google Sheets: Add Row** (optional)
   - Spreadsheet: XSO Reservations
   - Columns: booking_id, confirmation_number, first_name, last_name, phone, email, party_size, date, time, special_requests, room, created_at

6. **Response: Webhook Reply**
```json
{
  "success": true,
  "booking_id": "{{booking_id}}",
  "confirmation_number": "{{confirmation_number}}",
  "room_assigned": "XSO Main Room",
  "deposit_required": false,
  "message": "Reservation confirmed"
}
```

### Error Handling

Add error path:
- If Google Calendar create fails → success: false, message: "Booking system error - please call"
- Log error to Google Sheets

---

## Scenario 3: send_confirmation

**Webhook Trigger:** Custom webhook (instant)

### Steps:

1. **Trigger: Webhook**
   - Receives: booking_id, email, phone, confirmation_data

2. **Email: Send via Gmail/SendGrid**
   - To: {{email}}
   - From: hello@xsodenver.com (or your email)
   - Subject: `Your XSO Nightclub VIP Reservation - {{confirmation_number}}`
   - Body (HTML template):
```html
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
  <div style="background: #000; color: #EFB810; padding: 20px; text-align: center;">
    <h1 style="margin: 0;">EXCESSO NIGHTCLUB</h1>
    <p style="margin: 5px 0;">Nada con Medida, Todo con XSO</p>
  </div>
  
  <div style="padding: 30px; background: #f5f5f5;">
    <h2 style="color: #333;">Reservation Confirmed!</h2>
    
    <p>Hi {{name}},</p>
    
    <p>Your VIP table at XSO Nightclub is confirmed:</p>
    
    <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
      <tr>
        <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Confirmation #:</strong></td>
        <td style="padding: 10px; border-bottom: 1px solid #ddd;">{{confirmation_number}}</td>
      </tr>
      <tr>
        <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Date:</strong></td>
        <td style="padding: 10px; border-bottom: 1px solid #ddd;">{{date}}</td>
      </tr>
      <tr>
        <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Time:</strong></td>
        <td style="padding: 10px; border-bottom: 1px solid #ddd;">{{time}}</td>
      </tr>
      <tr>
        <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Party Size:</strong></td>
        <td style="padding: 10px; border-bottom: 1px solid #ddd;">{{party_size}} guests</td>
      </tr>
      <tr>
        <td style="padding: 10px;"><strong>Room:</strong></td>
        <td style="padding: 10px;">{{room}}</td>
      </tr>
    </table>
    
    <h3 style="color: #EFB810;">Important Reminders:</h3>
    <ul>
      <li>Arrive by 10:30 PM to claim your table</li>
      <li>Bring valid photo ID for all guests (21+ only)</li>
      <li>Dress code: Upscale nightlife attire</li>
      <li>Last entry: 1:30 AM or at capacity</li>
      <li>No re-entry permitted</li>
    </ul>
    
    <p style="margin-top: 30px;">
      <strong>Location:</strong><br>
      Excesso Nightclub (XSO)<br>
      500 16th Street Mall, Suite 322<br>
      Denver, CO 80202<br>
      (Inside Denver Pavilions)
    </p>
    
    <p>
      <strong>Questions?</strong><br>
      Call/Text: (303) 674-4060<br>
      Email: hello@xsodenver.com
    </p>
    
    <p style="text-align: center; margin-top: 30px;">
      <a href="https://xsodenver.com" style="background: #EFB810; color: #000; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">View Our Events</a>
    </p>
  </div>
  
  <div style="background: #000; color: #888; padding: 20px; text-align: center; font-size: 12px;">
    <p>Follow us: @xsonightclub</p>
    <p>© 2026 XSO Nightclub. All rights reserved.</p>
  </div>
</div>
```

3. **SMS: Send via Twilio** (optional)
   - To: {{phone}}
   - From: Your Twilio number
   - Message:
     ```
     Excesso Nightclub: Your VIP table is confirmed!
     
     Date: {{date}}
     Time: {{time}}
     Party: {{party_size}}
     Confirmation: {{confirmation_number}}
     
     Arrive by 10:30 PM. Bring valid ID (21+).
     
     500 16th St Mall, Denver
     Questions? (303) 674-4060
     ```

4. **Response: Webhook Reply**
```json
{
  "email_sent": true,
  "sms_sent": true,
  "message": "Confirmations sent successfully"
}
```

### Error Handling
- Track email/SMS failures
- Return partial success if one method fails

---

## Scenario 4: get_event_info

**Webhook Trigger:** Custom webhook (instant)

### Steps:

1. **Trigger: Webhook**
   - Receives: date (optional), day_of_week (optional)

2. **Static Data Store or Google Sheets**
   - For demo: return hardcoded events
   - For production: query event database or Google Sheets

3. **Filter by Date/Day**
   - If date provided: return events on that date
   - If day_of_week provided: return recurring event for that day
   - If neither: return next 7 days of events

4. **Response: Webhook Reply**
```json
{
  "events": [
    {
      "name": "Thirsty Thursday",
      "date": "2026-02-13",
      "day_of_week": "Thursday",
      "time": "21:30",
      "room": "XSO Main Room + Cielo Room",
      "description": "Regional Mexican battle night",
      "djs": ["Karma Music", "Adixion", "Proximo Nivel"],
      "ticket_url": "https://buy.tablelist.com/v/xso/events"
    },
    {
      "name": "A Poca Luz",
      "date": "2026-02-14",
      "day_of_week": "Friday",
      "time": "21:30",
      "room": "XSO Main Room",
      "description": "Reggaeton Old School + Perreo",
      "djs": ["DJ Click", "DJ RBT"],
      "ticket_url": "https://buy.tablelist.com/v/xso/events"
    }
  ]
}
```

### Quick Setup (Demo)

For demo, use hardcoded weekly schedule:
- Thursday: Thirsty Thursday
- Friday: A Poca Luz + Cielo Friday
- Saturday: Glam Saturday
- Sunday: Sunday Funday

---

## Testing Your Webhooks

### 1. Test check_availability

Send POST request to webhook:
```json
{
  "date": "2026-02-14",
  "time": "22:00",
  "party_size": 4
}
```

Expected response:
```json
{
  "available": true,
  "alternatives": [],
  "message": "Table available at requested time"
}
```

### 2. Test create_reservation

Send POST request:
```json
{
  "first_name": "Test",
  "last_name": "User",
  "phone": "303-555-1234",
  "email": "test@example.com",
  "party_size": 4,
  "date": "2026-02-14",
  "time": "22:00",
  "special_requests": "Test booking"
}
```

Expected: Calendar event created, Google Sheets row added, booking_id returned

### 3. Test send_confirmation

Send POST request:
```json
{
  "booking_id": "20260214223045-742",
  "email": "test@example.com",
  "phone": "303-555-1234",
  "confirmation_data": {
    "name": "Test User",
    "party_size": 4,
    "date": "Friday, February 14, 2026",
    "time": "10:00 PM",
    "room": "XSO Main Room",
    "confirmation_number": "XSO-57239"
  }
}
```

Expected: Email received, SMS received (if configured)

### 4. Test get_event_info

Send POST request:
```json
{
  "day_of_week": "friday"
}
```

Expected: Array of Friday events returned

---

## Webhook URLs to Add to Retell

After creating each scenario in Make.com:

1. Copy the webhook URL from each scenario
2. Paste into `functions.json` file
3. Import functions into Retell agent

Example URLs (replace with your actual URLs):
```
check_availability: https://hook.us1.make.com/abc123xyz/check_availability
create_reservation: https://hook.us1.make.com/abc123xyz/create_reservation
send_confirmation: https://hook.us1.make.com/abc123xyz/send_confirmation
get_event_info: https://hook.us1.make.com/abc123xyz/get_event_info
```

---

## Production Considerations

### Security
- [ ] Add API key authentication to webhooks
- [ ] Validate incoming data structure
- [ ] Rate limit requests
- [ ] Log all requests for audit

### Error Handling
- [ ] Retry logic for failed API calls
- [ ] Alert on critical failures (email not sent, booking not created)
- [ ] Fallback to human transfer on system errors

### Monitoring
- [ ] Track webhook success/failure rates
- [ ] Monitor response times
- [ ] Alert on abnormal patterns

### Integration Upgrades
- [ ] Replace Google Calendar with Tablelist API (production)
- [ ] Connect to real CRM (HubSpot, Salesforce)
- [ ] Professional email service (SendGrid, Mailgun)
- [ ] Dedicated SMS service (Twilio, AWS SNS)

---

## Quick Start Checklist

For rapid demo deployment:

- [ ] Create Make.com account
- [ ] Create Google Calendar "XSO Bookings"
- [ ] Create 4 webhook scenarios (can start with simple always-available versions)
- [ ] Test each webhook with Postman or curl
- [ ] Copy webhook URLs into functions.json
- [ ] Import functions to Retell agent
- [ ] Test full flow with Retell voice call

---

**END OF MAKE.COM SETUP GUIDE**

Next: Testing scenarios and deployment checklist.
