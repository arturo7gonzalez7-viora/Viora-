# 🚀 Deployment Guide

Deploy when you're ready to go live (after testing locally).

---

## Option 1: Railway (Recommended for Backend)

**Free tier: $5 credit/month, then $5/month for hobby plan**

### Backend Deployment

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login:
```bash
railway login
```

3. Deploy backend:
```bash
cd backend
railway init
# Follow prompts, create new project
railway up
```

4. Add environment variables in Railway dashboard:
- Go to railway.app → Your project → Variables
- Add all vars from your `.env`:
  - `HELIUS_RPC_URL`
  - `SUPABASE_URL`
  - `SUPABASE_KEY`
  - `NODE_ENV=production`

5. Copy your Railway URL (looks like: `https://your-app.railway.app`)

---

## Option 2: Vercel (Recommended for Frontend)

**Free tier: Unlimited hobby projects**

### Frontend Deployment

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
cd frontend
vercel login
vercel
```

3. Follow prompts:
- Project name: `seeker-staking-manager`
- Build command: `npm run build`
- Output directory: `build`

4. Add environment variables in Vercel dashboard:
- Go to vercel.com → Your project → Settings → Environment Variables
- Add:
  - `REACT_APP_API_URL` = your Railway backend URL
  - `REACT_APP_STRIPE_PUBLISHABLE_KEY` (when ready)

5. Redeploy:
```bash
vercel --prod
```

Your app is now live at: `https://your-app.vercel.app`

---

## Option 3: DigitalOcean App Platform

**Costs: ~$10-15/month for both services**

Good for when you want more control and are scaling up.

1. Create account at digitalocean.com
2. Create new App
3. Connect GitHub repo
4. Configure:
   - Backend: Node.js, detect from `backend/package.json`
   - Frontend: Static site, build from `frontend/`
5. Add environment variables
6. Deploy

---

## Custom Domain (Optional)

**Cost: ~$12/year**

### Buy Domain
- Namecheap.com
- Cloudflare Registrar (cheapest)
- Any registrar you like

### Point to Vercel
1. Vercel dashboard → Your project → Settings → Domains
2. Add your domain
3. Copy DNS records shown
4. Add to your domain registrar's DNS settings
5. Wait 5-60 minutes for propagation

### Point to Railway
Similar process, Railway will give you DNS records.

---

## Stripe Setup (For Payments)

1. Go to stripe.com → Create account

2. Create product:
- Dashboard → Products → Add Product
- Name: "Seeker Staking Manager Premium"
- Price: $15/month recurring
- Copy Price ID (starts with `price_...`)

3. Get API keys:
- Dashboard → Developers → API Keys
- Copy:
  - Publishable key (starts with `pk_...`)
  - Secret key (starts with `sk_...`)

4. Add to environment variables:
- Backend: `STRIPE_SECRET_KEY`
- Frontend: `REACT_APP_STRIPE_PUBLISHABLE_KEY`

5. Set up webhook (for subscription events):
- Dashboard → Developers → Webhooks → Add endpoint
- URL: `https://your-backend.railway.app/api/webhook/stripe`
- Events: `customer.subscription.created`, `customer.subscription.deleted`
- Copy webhook secret to backend env: `STRIPE_WEBHOOK_SECRET`

---

## SSL/HTTPS

Both Vercel and Railway provide free SSL automatically. Nothing to configure!

---

## Monitoring (Free Tier Options)

### Backend Health Check
Use UptimeRobot (free):
- uptimerobot.com
- Add monitor for `https://your-backend/health`
- Get alerts if backend goes down

### Error Tracking
Use Sentry (free tier):
- sentry.io
- Add SDK to backend and frontend
- Get notified of crashes

---

## Scaling Costs

**100 users (Goal: $1,500/mo revenue):**
- Hosting: $0-15/mo (free tiers or basic plans)
- Helius RPC: $0 (free tier handles it)
- Supabase: $0 (free tier)
- Stripe: ~$50/mo (3% of $1,500)
- **Total: ~$50-65/mo**

**500 users (Goal: $7,500/mo revenue):**
- Hosting: $30-50/mo (upgraded plans)
- Helius RPC: $0-20/mo (might need paid tier)
- Supabase: $25/mo (Pro plan)
- Stripe: ~$250/mo (3% + 30¢ per transaction)
- **Total: ~$305-345/mo**

**Profit margins are great even at scale!**

---

## Pre-Launch Checklist

Before announcing publicly:

- [ ] Test all flows on actual Seeker device
- [ ] Verify stake/unstake transactions work with real SOL
- [ ] Test premium upgrade flow with Stripe test mode
- [ ] Check mobile responsive design
- [ ] Add privacy policy page (required for Stripe)
- [ ] Add terms of service page
- [ ] Set up customer support email
- [ ] Create error monitoring (Sentry)
- [ ] Test with small amount of real money first
- [ ] Have refund policy ready

---

## Marketing Launch Plan

1. **Week before:**
   - Soft launch to Seeker Discord (alpha testers)
   - Offer 30-day free Premium trial for first 50 users
   - Collect feedback, fix bugs

2. **Launch day:**
   - Post in Seeker Discord
   - Tweet with screenshots
   - Post in Solana subreddit
   - Email Solana Mobile team

3. **Week after:**
   - Post tutorial video on YouTube
   - Write blog post about how it works
   - Reach out to crypto influencers
   - Consider small ad spend on Twitter ($100 test)

---

Need help deploying? Ping me and I'll walk you through it step-by-step.
