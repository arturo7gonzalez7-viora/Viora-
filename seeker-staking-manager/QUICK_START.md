# ⚡ Quick Start Guide

## Step 1: Install Dependencies (2 minutes)

```bash
cd seeker-staking-manager

# Backend
cd backend
npm install
cd ..

# Frontend
cd frontend
npm install
cd ..
```

## Step 2: Create Free Accounts (10 minutes)

### A) Helius (Solana RPC) - Free Tier
1. Go to: https://www.helius.dev/
2. Click "Sign Up" (free)
3. Create a new project
4. Copy your API key (looks like: `abc123...`)

### B) Supabase (Database) - Free Tier
1. Go to: https://supabase.com/
2. Click "Start your project" (free)
3. Create new project (pick a password you'll remember)
4. Wait 2 mins for setup
5. Go to Settings → API
6. Copy:
   - Project URL (looks like: `https://abc123.supabase.co`)
   - `anon` `public` key (long string)
7. Go to SQL Editor → New Query
8. Copy-paste contents of `backend/database-schema.sql`
9. Click "Run"

### C) Firebase (Push Notifications) - Optional for Now
Skip this for MVP. You can add it later when you want push alerts.

## Step 3: Configure Environment (2 minutes)

### Backend `.env`
```bash
cd backend
cp .env.example .env
nano .env  # or use any text editor
```

Fill in:
```
HELIUS_RPC_URL=https://mainnet.helius-rpc.com/?api-key=YOUR_KEY_FROM_STEP_2A
SUPABASE_URL=https://YOUR_PROJECT.supabase.co
SUPABASE_KEY=YOUR_ANON_KEY_FROM_STEP_2B
PORT=3001
```

Save and exit (Ctrl+X, Y, Enter in nano)

### Frontend `.env`
```bash
cd ../frontend
cp .env.example .env
nano .env
```

Fill in:
```
REACT_APP_API_URL=http://localhost:3001
```

Save and exit.

## Step 4: Run It! (1 minute)

Open 2 terminal windows:

**Terminal 1 - Backend:**
```bash
cd seeker-staking-manager/backend
npm run dev
```

You should see:
```
✅ Seeker Staking Manager backend running on port 3001
📊 RPC: Configured
💾 Database: Connected
```

**Terminal 2 - Frontend:**
```bash
cd seeker-staking-manager/frontend
npm start
```

Browser will auto-open to `http://localhost:3000`

## Step 5: Test It

1. Click "Connect Wallet"
2. Select your wallet (Phantom, Solflare, or Seed Vault if on Seeker device)
3. Approve connection
4. You should see:
   - Your wallet balance
   - Your staked SOL
   - List of top validators
   - "Stake" buttons

## Testing on Seeker Device

1. Find your computer's local IP:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   # Look for something like 192.168.1.100
   ```

2. Update frontend `.env`:
   ```
   REACT_APP_API_URL=http://192.168.1.100:3001
   ```

3. Restart frontend (`npm start`)

4. On Seeker device, open browser and go to:
   ```
   http://192.168.1.100:3000
   ```

5. Connect Seed Vault wallet and test!

## Troubleshooting

### "Cannot connect to backend"
- Check backend terminal is running
- Check `REACT_APP_API_URL` in frontend `.env`
- Make sure port 3001 is not in use

### "Database error"
- Check Supabase credentials in backend `.env`
- Make sure you ran the SQL schema (`database-schema.sql`)

### "RPC error"
- Check Helius API key is correct
- Free tier has rate limits, but should be fine for testing

### Wallet won't connect
- Make sure you have a Solana wallet extension installed
- Try refreshing the page
- Check browser console for errors (F12)

## Next Steps

Once it's working:
1. Test staking flow (it will show alert for now, actual transaction coming soon)
2. Give me feedback on what you like/don't like
3. Tell me what features to prioritize
4. Next week when you're ready: add Stripe for payments

---

## Need Help?

Just ping me in Discord. I'll fix any issues immediately.

The hard part is done. You just run commands and test! 🚀
