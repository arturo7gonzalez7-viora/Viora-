-- SK Home Solutions CRM — Schema v2 Additions
-- Run this AFTER the original setup.sql
-- Adds: investors, property_notes, property_photos, property_documents
-- Plus: investor_id/investor_name columns on properties

-- ============================================================
-- INVESTORS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS investors (
  id TEXT PRIMARY KEY,
  name TEXT,
  company TEXT DEFAULT '',
  phone TEXT DEFAULT '',
  email TEXT DEFAULT '',
  budget TEXT DEFAULT '',
  focus TEXT DEFAULT '',        -- fix-flip, buy-hold, both
  zips TEXT DEFAULT '',
  deals_done INTEGER DEFAULT 0,
  active_deals INTEGER DEFAULT 0,
  notes TEXT DEFAULT '',
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE investors DISABLE ROW LEVEL SECURITY;

-- ============================================================
-- PROPERTY NOTES (timestamped, multi-user)
-- ============================================================
CREATE TABLE IF NOT EXISTS property_notes (
  id BIGSERIAL PRIMARY KEY,
  property_id TEXT REFERENCES properties(id) ON DELETE CASCADE,
  author_id TEXT DEFAULT '',
  author_name TEXT DEFAULT '',
  note TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE property_notes DISABLE ROW LEVEL SECURITY;

-- ============================================================
-- PROPERTY PHOTOS (Supabase Storage paths)
-- ============================================================
CREATE TABLE IF NOT EXISTS property_photos (
  id BIGSERIAL PRIMARY KEY,
  property_id TEXT REFERENCES properties(id) ON DELETE CASCADE,
  url TEXT,
  filename TEXT DEFAULT '',
  uploaded_by TEXT DEFAULT '',
  uploaded_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE property_photos DISABLE ROW LEVEL SECURITY;

-- ============================================================
-- PROPERTY DOCUMENTS (Supabase Storage paths)
-- ============================================================
CREATE TABLE IF NOT EXISTS property_documents (
  id BIGSERIAL PRIMARY KEY,
  property_id TEXT REFERENCES properties(id) ON DELETE CASCADE,
  url TEXT,
  filename TEXT,
  doc_type TEXT DEFAULT '',     -- contract, inspection, title, other
  uploaded_by TEXT DEFAULT '',
  uploaded_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE property_documents DISABLE ROW LEVEL SECURITY;

-- ============================================================
-- ADD INVESTOR COLUMNS TO PROPERTIES
-- ============================================================
ALTER TABLE properties ADD COLUMN IF NOT EXISTS investor_id TEXT DEFAULT '';
ALTER TABLE properties ADD COLUMN IF NOT EXISTS investor_name TEXT DEFAULT '';

-- ============================================================
-- ADD user_name TO ACTIVITIES
-- ============================================================
ALTER TABLE activities ADD COLUMN IF NOT EXISTS user_name TEXT DEFAULT '';

-- ============================================================
-- NOTES
-- ============================================================
-- 1. Storage buckets must be created manually in Supabase dashboard:
--    - bucket name: "property-media"  (for photos)  — set as public
--    - bucket name: "property-docs"   (for documents) — set as public
--
-- 2. After creating buckets, go to Storage > Policies and add:
--    INSERT policy: allow anon/service key inserts
--    SELECT policy: public read (or anon read)
--
-- 3. The CRM upload function uses the anon key (SKEY) for uploads.
--    If uploads fail, check bucket policies in the Supabase dashboard.
