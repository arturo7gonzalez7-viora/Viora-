// Email Time Display Fix - for n8n Email Templates
// Problem: moment() function is undefined, showing only "(Mountain Time)"

// BROKEN CODE (current in HTML email):
// {{moment(appointmentTime).format('h:mm A')}} (Mountain Time)
// Result: "(Mountain Time)" - no actual time shown

// FIXED CODE - Option 1: Prepare time in JavaScript node before email
const appointmentDateTime = $json.appointmentDateTime;
const appointmentTime = new Date(appointmentDateTime);

const formattedTime = appointmentTime.toLocaleTimeString('en-US', {
  hour: 'numeric',
  minute: '2-digit',
  timeZone: 'America/Denver',
  hour12: true
});

const formattedDate = appointmentTime.toLocaleDateString('en-US', {
  weekday: 'long',
  year: 'numeric', 
  month: 'long',
  day: 'numeric',
  timeZone: 'America/Denver'
});

return {
  json: {
    ...$json,
    displayTime: formattedTime, // "2:00 PM"
    displayDate: formattedDate, // "Saturday, February 21, 2026"
    displayDateTime: `${formattedTime} (Mountain Time)` // "2:00 PM (Mountain Time)"
  }
};

// FIXED EMAIL TEMPLATES:

// Customer Email HTML:
/*
<p>Your kitchen consultation appointment is confirmed!</p>
<p><strong>Date:</strong> {{displayDate}}</p>
<p><strong>Time:</strong> {{displayDateTime}}</p>
*/

// Dani Email HTML:
/*
<h2>New Appointment Scheduled</h2>
<p><strong>Customer:</strong> {{customerName}}</p>
<p><strong>Phone:</strong> {{customerPhone}}</p>
<p><strong>Email:</strong> {{customerEmail}}</p>
<p><strong>Date:</strong> {{displayDate}}</p>
<p><strong>Time:</strong> {{displayDateTime}}</p>
*/

// Test Cases:
// Input: "2026-02-21T14:00:00" (Mountain Time)
// Output: "2:00 PM (Mountain Time)" ✅
// NOT: "(Mountain Time)" ❌