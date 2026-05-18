# Table AI — The Restaurant OS

> "So easy, your abuela could run it."

A premium restaurant management platform built with Next.js 14, Tailwind CSS, and Supabase.

## Features

- **Dashboard** — Daily stats, quick actions, activity feed
- **Reservations** — List, add, and manage reservations with status badges
- **AI Call Log** — View AI-answered calls with expandable summaries
- **Reviews** — Star ratings with AI-drafted responses and approve workflow
- **Loyalty Program** — Member list with points and tier badges (Bronze → Platinum)
- **Inventory** — Stock tracking with low-stock alerts
- **Compliance** — Checklists for health/safety
- **Finance** — Daily sales logging, expense tracking, weekly summary
- **Marketing** — Promotions and content scheduling
- **Settings** — Restaurant info management

## Tech Stack

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Supabase (PostgreSQL)

## Getting Started

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## Environment Variables

Copy `.env.local.example` to `.env.local` and fill in:

```
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
NEXT_PUBLIC_RESTAURANT_ID=
```

## Design

- **Primary:** #0A0F1E (deep navy)
- **Accent:** #00C9A7 (teal)
- **Font:** Inter
- Dark theme, mobile-first, responsive
