# Table AI — Vision & Core Rules

## What We're Building
The all-in-one restaurant OS that replaces Toast, Square, Gusto, Mailchimp, and Yelp.
Built for independent restaurants. Tested at Casa Mariachi. Designed to bury Toast.

## The Golden Rule (NEVER compromise this)
**If a 60-year-old restaurant owner who's never used software can't figure it out in 60 seconds — we rebuild it.**

- No jargon. Ever. "Reservations today" not "CRM pipeline"
- One screen = one job. Never overwhelm.
- Mobile first. Owners are on their phone, not a laptop.
- Setup must feel like magic — plug it in and it works
- Onboarding: owner should be live in under 30 minutes
- Every feature must have a "why this helps you" explanation built in

## The Integration Promise
Going into a restaurant and setting this up must feel effortless.
- Step 1: Create account (2 min)
- Step 2: Enter restaurant info — name, hours, menu basics (5 min)
- Step 3: Forward their phone number to Retell (2 min)
- Step 4: Done. AI receptionist is live.
Every additional module follows the same pattern: simple, fast, no tech knowledge needed.

## The 11 Modules
1. AI Receptionist (Retell) — answers calls 24/7, bilingual
2. SMS Automation — reservations, reminders, follow-ups
3. Review Response Bot — Google reviews on autopilot
4. Inventory AI — waste tracking, low stock alerts
5. Compliance & Ops — digital checklists, health inspection ready
6. Marketing Engine — content, promos, social
7. WiFi Marketing — capture guest emails/phones at login
8. Loyalty Program — points, rewards, repeat customers
9. Revenue Brain — analytics, menu optimization, reduce DoorDash fees
10. Finance & Payroll — sales tracking, P&L, payroll prep, tax estimates
11. Owner Dashboard — everything in one dead-simple interface

## Target Market
- Independent restaurants (not chains)
- Hispanic-owned restaurants (massively underserved, 70K+ in US)
- 1-3 locations, $500K-$3M annual revenue
- Owner-operated, time-starved, tech-hesitant

## Pricing
- Starter: $149/mo (Receptionist + Reviews + SMS)
- Pro: $349/mo (+ Loyalty + WiFi + Finance)
- Elite: $599/mo (all 11 modules, full white glove setup)

## Tech Stack
- Database: Supabase
- Voice AI: Retell
- Automation: n8n
- AI brain: Claude (Anthropic API)
- Frontend: Next.js (deployed on Vercel)
- SMS: Twilio or OpenPhone
- Payments: Stripe

## Competition
Toast: $110-165/mo + 0.15% per transaction + $600-1000 hardware
Table AI: Half the price. No hardware. Actually speaks their language. Has AI.

## Internationalization (i18n)
Settings page must have a language selector. First two languages: English and Spanish.
Roadmap: Portuguese, French, Mandarin.
Every single UI string must use a translation key — no hardcoded English text.
Spanish must be perfect, natural, restaurant-owner friendly. Not Google Translate quality.
Language switch applies instantly to the entire app with no page reload.
Use next-intl or i18next for implementation.

## No Dashes Rule
Zero dashes anywhere in the UI. Ever.
Use proper punctuation: commas, periods, colons, parentheses.
This applies to all copy, labels, buttons, descriptions, and AI generated text.

## Delivery Intelligence Module
A dedicated Revenue page showing all delivery platform data:
- Revenue per platform (DoorDash, UberEats, Grubhub, Direct)
- Commission fees paid per platform per month
- Total money lost to platforms
- AI insights: what to do with the data, how to improve
- Direct order goal tracker with progress bar
Connect to DoorDash Merchant API, UberEats API, Grubhub API when restaurant grants access.
Build UI with sample data first, real API data later.

## Mantra
**"So easy, your abuela could run it."**
