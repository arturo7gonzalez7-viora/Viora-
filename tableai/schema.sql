-- ============================================
-- TABLE AI — FULL DATABASE SCHEMA
-- ============================================

-- RESTAURANTS (core — every module links here)
CREATE TABLE restaurants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  phone TEXT,
  address TEXT,
  city TEXT,
  state TEXT,
  zip TEXT,
  timezone TEXT DEFAULT 'America/Denver',
  google_place_id TEXT,
  hours JSONB, -- {"mon": "11-9", "tue": "11-9", ...}
  logo_url TEXT,
  primary_color TEXT DEFAULT '#0A0F1E',
  accent_color TEXT DEFAULT '#00C9A7',
  plan TEXT DEFAULT 'starter', -- starter | pro | elite
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- USERS (restaurant owners/staff)
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  role TEXT DEFAULT 'owner', -- owner | manager | staff
  phone TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- MODULE 1: AI RECEPTIONIST
-- ============================================
CREATE TABLE calls (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  caller_phone TEXT,
  caller_name TEXT,
  duration_seconds INTEGER,
  intent TEXT, -- reservation | question | complaint | other
  summary TEXT,
  recording_url TEXT,
  retell_call_id TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- MODULE 2: RESERVATIONS & SMS
-- ============================================
CREATE TABLE reservations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  guest_name TEXT NOT NULL,
  guest_phone TEXT,
  guest_email TEXT,
  party_size INTEGER,
  date DATE,
  time TIME,
  status TEXT DEFAULT 'confirmed', -- confirmed | cancelled | completed | no_show
  notes TEXT,
  source TEXT DEFAULT 'phone', -- phone | web | walk_in
  reminder_sent BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE sms_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  to_phone TEXT,
  message TEXT,
  type TEXT, -- confirmation | reminder | followup | promo | loyalty
  status TEXT DEFAULT 'sent',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- MODULE 3: REVIEW RESPONSE BOT
-- ============================================
CREATE TABLE reviews (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  platform TEXT DEFAULT 'google', -- google | yelp
  reviewer_name TEXT,
  rating INTEGER, -- 1-5
  review_text TEXT,
  ai_response TEXT,
  response_posted BOOLEAN DEFAULT false,
  response_approved BOOLEAN DEFAULT false,
  external_review_id TEXT,
  review_date DATE,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- MODULE 4: INVENTORY AI
-- ============================================
CREATE TABLE inventory_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  name TEXT NOT NULL,
  category TEXT, -- protein | produce | dairy | dry | beverage | alcohol
  unit TEXT, -- lbs | oz | each | case | bottle
  current_qty DECIMAL,
  par_level DECIMAL, -- minimum before reorder alert
  cost_per_unit DECIMAL,
  supplier TEXT,
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE inventory_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  item_id UUID REFERENCES inventory_items(id),
  action TEXT, -- restock | usage | waste | adjustment
  quantity DECIMAL,
  notes TEXT,
  logged_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- MODULE 5: COMPLIANCE & OPS
-- ============================================
CREATE TABLE checklist_templates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  name TEXT, -- "Opening Checklist" | "Closing Checklist" | "Weekly Deep Clean"
  frequency TEXT, -- daily | weekly | monthly
  items JSONB, -- [{"task": "Check fridge temp", "required": true}]
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE checklist_completions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  template_id UUID REFERENCES checklist_templates(id),
  completed_by UUID REFERENCES users(id),
  items_completed JSONB, -- {"task": "Check fridge temp", "done": true, "value": "38F"}
  all_complete BOOLEAN DEFAULT false,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE incidents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  type TEXT, -- accident | complaint | equipment | health | other
  description TEXT,
  reported_by UUID REFERENCES users(id),
  photo_url TEXT,
  resolved BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- MODULE 7: WIFI MARKETING
-- ============================================
CREATE TABLE wifi_guests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  name TEXT,
  email TEXT,
  phone TEXT,
  visit_count INTEGER DEFAULT 1,
  last_visit TIMESTAMPTZ DEFAULT now(),
  opted_in_sms BOOLEAN DEFAULT false,
  opted_in_email BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- MODULE 8: LOYALTY PROGRAM
-- ============================================
CREATE TABLE loyalty_members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  name TEXT,
  phone TEXT UNIQUE,
  email TEXT,
  points INTEGER DEFAULT 0,
  total_spent DECIMAL DEFAULT 0,
  visit_count INTEGER DEFAULT 0,
  tier TEXT DEFAULT 'bronze', -- bronze | silver | gold | vip
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE loyalty_transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  member_id UUID REFERENCES loyalty_members(id),
  type TEXT, -- earn | redeem | bonus | expire
  points INTEGER,
  amount_spent DECIMAL,
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE loyalty_rewards (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  name TEXT, -- "Free Appetizer" | "$10 Off" | "Free Drink"
  points_required INTEGER,
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- MODULE 10: FINANCE & PAYROLL
-- ============================================
CREATE TABLE daily_sales (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  date DATE NOT NULL,
  total_revenue DECIMAL DEFAULT 0,
  cash_sales DECIMAL DEFAULT 0,
  card_sales DECIMAL DEFAULT 0,
  delivery_sales DECIMAL DEFAULT 0,
  covers INTEGER DEFAULT 0, -- number of guests served
  avg_ticket DECIMAL,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE expenses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  date DATE,
  category TEXT, -- food_cost | labor | rent | utilities | marketing | supplies | other
  amount DECIMAL,
  description TEXT,
  vendor TEXT,
  receipt_url TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE staff (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  name TEXT NOT NULL,
  role TEXT, -- server | cook | host | manager | bartender | busser
  hourly_rate DECIMAL,
  phone TEXT,
  email TEXT,
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE timesheets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  staff_id UUID REFERENCES staff(id),
  date DATE,
  clock_in TIME,
  clock_out TIME,
  hours_worked DECIMAL,
  tips DECIMAL DEFAULT 0,
  gross_pay DECIMAL,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- MODULE 6: MARKETING ENGINE
-- ============================================
CREATE TABLE content_posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  platform TEXT, -- instagram | facebook | tiktok
  caption TEXT,
  media_url TEXT,
  hashtags TEXT,
  scheduled_for TIMESTAMPTZ,
  posted BOOLEAN DEFAULT false,
  posted_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE promotions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  restaurant_id UUID REFERENCES restaurants(id),
  name TEXT, -- "Taco Tuesday" | "Happy Hour Wednesday"
  description TEXT,
  start_date DATE,
  end_date DATE,
  day_of_week TEXT, -- monday | tuesday | ...
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================
CREATE INDEX idx_calls_restaurant ON calls(restaurant_id);
CREATE INDEX idx_reservations_restaurant ON reservations(restaurant_id);
CREATE INDEX idx_reservations_date ON reservations(date);
CREATE INDEX idx_reviews_restaurant ON reviews(restaurant_id);
CREATE INDEX idx_loyalty_phone ON loyalty_members(phone);
CREATE INDEX idx_daily_sales_date ON daily_sales(date);
CREATE INDEX idx_timesheets_date ON timesheets(date);
CREATE INDEX idx_inventory_restaurant ON inventory_items(restaurant_id);
