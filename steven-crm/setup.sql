-- SK Home Solutions CRM — Supabase Schema
-- Run this in your Supabase SQL Editor

CREATE TABLE IF NOT EXISTS settings (
  id INTEGER PRIMARY KEY DEFAULT 1,
  name TEXT DEFAULT 'Steven K.',
  company TEXT DEFAULT 'SK Home Solutions',
  phone TEXT DEFAULT '',
  email TEXT DEFAULT ''
);
INSERT INTO settings (id) VALUES (1) ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS leads (
  id TEXT PRIMARY KEY,
  name TEXT,
  phone TEXT,
  email TEXT,
  address TEXT,
  situation TEXT,
  timeline TEXT,
  condition TEXT,
  ask_price INTEGER DEFAULT 0,
  score INTEGER DEFAULT 0,
  status TEXT DEFAULT 'new',
  last_contact TEXT,
  notes JSONB DEFAULT '[]',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS properties (
  id TEXT PRIMARY KEY,
  address TEXT,
  seller TEXT,
  arv INTEGER DEFAULT 0,
  repairs INTEGER DEFAULT 0,
  offer_price INTEGER DEFAULT 0,
  buyer_id TEXT DEFAULT '',
  stage TEXT DEFAULT 'new',
  days_in_stage INTEGER DEFAULT 0,
  notes TEXT DEFAULT '',
  checklist JSONB DEFAULT '[]',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS buyers (
  id TEXT PRIMARY KEY,
  name TEXT,
  company TEXT DEFAULT '',
  phone TEXT DEFAULT '',
  email TEXT DEFAULT '',
  budget TEXT DEFAULT '',
  zips TEXT DEFAULT '',
  types TEXT DEFAULT '',
  deals INTEGER DEFAULT 0,
  last_contact TEXT DEFAULT '',
  notes TEXT DEFAULT '',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS realtors (
  id TEXT PRIMARY KEY,
  name TEXT,
  brokerage TEXT DEFAULT '',
  phone TEXT DEFAULT '',
  email TEXT DEFAULT '',
  zips TEXT DEFAULT '',
  referrals INTEGER DEFAULT 0,
  deals INTEGER DEFAULT 0,
  last_contact TEXT DEFAULT '',
  notes TEXT DEFAULT '',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS contacts (
  id TEXT PRIMARY KEY,
  type TEXT,
  name TEXT,
  company TEXT DEFAULT '',
  phone TEXT DEFAULT '',
  email TEXT DEFAULT '',
  detail TEXT DEFAULT '',
  notes TEXT DEFAULT '',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS followups (
  id TEXT PRIMARY KEY,
  name TEXT,
  description TEXT DEFAULT '',
  date TEXT,
  status TEXT DEFAULT 'upcoming',
  lead_id TEXT DEFAULT '',
  priority TEXT DEFAULT 'medium',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ad_campaigns (
  id TEXT PRIMARY KEY,
  platform TEXT,
  name TEXT,
  impressions INTEGER DEFAULT 0,
  clicks INTEGER DEFAULT 0,
  leads_count INTEGER DEFAULT 0,
  spend INTEGER DEFAULT 0,
  status TEXT DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS activities (
  id BIGSERIAL PRIMARY KEY,
  icon TEXT DEFAULT '📋',
  text TEXT,
  time TEXT DEFAULT 'Just now',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- TEAM MEMBERS / AUTH
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  pin TEXT NOT NULL,
  role TEXT DEFAULT 'member',  -- 'admin' or 'member'
  email TEXT DEFAULT '',
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
-- Steven is always admin. Change the PIN below before going live!
INSERT INTO users (id, name, pin, role) VALUES ('u_steven', 'Steven K.', '1234', 'admin') ON CONFLICT (id) DO NOTHING;

-- Add assigned_to to leads (which team member owns this lead)
ALTER TABLE leads ADD COLUMN IF NOT EXISTS assigned_to TEXT DEFAULT '';
-- Add lead_id to properties so we can link property back to originating lead
ALTER TABLE properties ADD COLUMN IF NOT EXISTS lead_id TEXT DEFAULT '';
-- Add assigned_to to properties
ALTER TABLE properties ADD COLUMN IF NOT EXISTS assigned_to TEXT DEFAULT '';

-- Disable RLS so anyone with the key can access (private CRM)
ALTER TABLE settings DISABLE ROW LEVEL SECURITY;
ALTER TABLE leads DISABLE ROW LEVEL SECURITY;
ALTER TABLE properties DISABLE ROW LEVEL SECURITY;
ALTER TABLE buyers DISABLE ROW LEVEL SECURITY;
ALTER TABLE realtors DISABLE ROW LEVEL SECURITY;
ALTER TABLE contacts DISABLE ROW LEVEL SECURITY;
ALTER TABLE followups DISABLE ROW LEVEL SECURITY;
ALTER TABLE ad_campaigns DISABLE ROW LEVEL SECURITY;
ALTER TABLE activities DISABLE ROW LEVEL SECURITY;
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
