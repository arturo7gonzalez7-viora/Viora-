-- Run this in your Supabase SQL Editor
-- This creates the tables needed for the staking manager

-- Users table
CREATE TABLE IF NOT EXISTS users (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  wallet_address TEXT UNIQUE NOT NULL,
  is_premium BOOLEAN DEFAULT FALSE,
  subscription_end TIMESTAMP,
  stripe_customer_id TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  last_seen TIMESTAMP DEFAULT NOW()
);

-- Validators cache (optional, for faster lookups)
CREATE TABLE IF NOT EXISTS validators (
  vote_pubkey TEXT PRIMARY KEY,
  node_pubkey TEXT,
  activated_stake BIGINT,
  commission INTEGER,
  name TEXT,
  website TEXT,
  last_updated TIMESTAMP DEFAULT NOW()
);

-- User alerts/preferences
CREATE TABLE IF NOT EXISTS user_alerts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  alert_type TEXT NOT NULL, -- 'stake_reward', 'validator_change', 'large_transfer'
  enabled BOOLEAN DEFAULT TRUE,
  threshold NUMERIC, -- Optional threshold for alerts
  created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_wallet ON users(wallet_address);
CREATE INDEX IF NOT EXISTS idx_user_alerts_user_id ON user_alerts(user_id);
CREATE INDEX IF NOT EXISTS idx_validators_stake ON validators(activated_stake DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_alerts ENABLE ROW LEVEL SECURITY;

-- RLS Policies (users can only see their own data)
CREATE POLICY "Users can view own data" ON users
  FOR SELECT USING (true); -- Public read for subscription checks

CREATE POLICY "Users can update own data" ON users
  FOR UPDATE USING (wallet_address = current_setting('request.jwt.claims', true)::json->>'wallet');

CREATE POLICY "Users can view own alerts" ON user_alerts
  FOR ALL USING (
    user_id IN (
      SELECT id FROM users WHERE wallet_address = current_setting('request.jwt.claims', true)::json->>'wallet'
    )
  );
