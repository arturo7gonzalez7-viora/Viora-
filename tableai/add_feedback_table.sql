-- Add new columns to restaurants table (safe to run if they already exist)
ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS logo_url TEXT;
ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS google_place_id TEXT;

CREATE TABLE IF NOT EXISTS review_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  guest_name TEXT,
  guest_phone TEXT,
  rating INTEGER,
  feedback_text TEXT,
  sent_to_google BOOLEAN DEFAULT false,
  is_private BOOLEAN DEFAULT false,
  reservation_id UUID REFERENCES reservations(id),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE POLICY "Allow public read" ON review_requests FOR SELECT USING (true);
CREATE POLICY "Allow public insert" ON review_requests FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public update" ON review_requests FOR UPDATE USING (true);
ALTER TABLE review_requests ENABLE ROW LEVEL SECURITY;
