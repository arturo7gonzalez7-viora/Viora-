// Calendar Duration Fix - for n8n Calendar Event Node
// Problem: Currently showing 3-hour appointments instead of 1 hour

// BROKEN CODE (current):
// end: startDateTime + 3 hours

// FIXED CODE:
const startDateTime = $json.appointmentDateTime; // from previous node
const startTime = new Date(startDateTime);
const endTime = new Date(startTime.getTime() + (60 * 60 * 1000)); // Add 1 hour

return {
  json: {
    summary: `NEW APPOINTMENT - ${$json.customerName}`,
    start: {
      dateTime: startTime.toISOString(),
      timeZone: 'America/Denver'
    },
    end: {
      dateTime: endTime.toISOString(), // This is the key fix
      timeZone: 'America/Denver'
    },
    description: `Customer: ${$json.customerName}\nPhone: ${$json.customerPhone}\nEmail: ${$json.customerEmail}`,
    location: 'Next Step Kitchens',
    attendees: [
      { email: $json.customerEmail },
      { email: 'dani@nextstepkitchens.com' }
    ]
  }
};

// Alternative using date math:
// const endDateTime = new Date(startDateTime);
// endDateTime.setHours(endDateTime.getHours() + 1);

// Test example:
// Input: 2026-02-21T14:00:00 (2:00 PM)
// Output: 2026-02-21T15:00:00 (3:00 PM) ✅
// NOT: 2026-02-21T17:00:00 (5:00 PM) ❌