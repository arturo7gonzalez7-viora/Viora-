# 🏗️ Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Seeker Device                          │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Seed Vault Wallet (on-device)               │    │
│  │         - Private keys stored locally               │    │
│  │         - Signs transactions                        │    │
│  └───────────────────┬─────────────────────────────────┘    │
│                      │                                       │
│  ┌──────────────────┴─────────────────────────────────┐    │
│  │        React PWA Frontend (localhost:3000)          │    │
│  │        - Wallet connection UI                       │    │
│  │        - Dashboard & stats                          │    │
│  │        - Validator browser                          │    │
│  │        - Premium paywall                            │    │
│  └──────────────────┬─────────────────────────────────┘    │
└────────────────────┼──────────────────────────────────────┘
                     │
                     │ HTTP Requests
                     │
         ┌───────────▼────────────┐
         │   Backend API           │
         │   (Node.js + Express)   │
         │   localhost:3001        │
         └───────────┬─────────────┘
                     │
         ┌───────────┴─────────────┐
         │                         │
    ┌────▼─────┐          ┌───────▼────────┐
    │ Solana   │          │   Supabase     │
    │ RPC      │          │   (PostgreSQL) │
    │ (Helius) │          │   - Users      │
    │          │          │   - Validators │
    └──────────┘          │   - Alerts     │
                          └────────────────┘
```

## Data Flow

### 1. Wallet Connection
```
User clicks "Connect Wallet"
  → Wallet Adapter detects available wallets
  → User selects Seed Vault
  → Seed Vault prompts for approval
  → Wallet address returned to frontend
  → Frontend sends address to backend
  → Backend creates/updates user record in Supabase
```

### 2. Loading Dashboard
```
Frontend requests wallet data
  → Backend queries Solana RPC for:
    - Balance (getBalance)
    - Stake accounts (getParsedProgramAccounts)
  → Backend queries validators (getVoteAccounts)
  → Data cached for 5 minutes
  → Response sent to frontend
  → Frontend renders stats and validator list
```

### 3. Staking Flow (TODO: Implement transactions)
```
User clicks "Stake" on a validator
  → Frontend checks if user is premium (multi-stake limit)
  → If not premium and has existing stake → show upgrade modal
  → If allowed:
    - Build stake transaction using @solana/web3.js
    - Request signature from Seed Vault
    - User approves in Seed Vault
    - Transaction submitted to Solana network
    - Frontend polls for confirmation
    - Update UI with new stake
```

### 4. Premium Subscription (TODO: Implement Stripe)
```
User clicks "Upgrade to Premium"
  → Frontend shows premium modal
  → User clicks "Upgrade Now"
  → Redirect to Stripe Checkout
  → User pays $15/mo
  → Stripe webhook fires
  → Backend updates user.is_premium = true
  → User redirected back with success
  → Frontend refreshes subscription status
```

## Tech Stack

### Frontend
- **React 18** - UI framework
- **@solana/wallet-adapter-react** - Wallet connection (works with Seed Vault)
- **@solana/web3.js** - Solana transactions and data
- **Axios** - HTTP client
- **@stripe/stripe-js** - Payment processing (when added)

### Backend
- **Node.js + Express** - API server
- **@solana/web3.js** - Blockchain interaction
- **@supabase/supabase-js** - Database client
- **node-cache** - In-memory caching (5 min TTL for validators)
- **Stripe** - Subscription billing (when added)

### Infrastructure (Free Tiers)
- **Helius** - Solana RPC endpoint (free: thousands of requests/day)
- **Supabase** - PostgreSQL database + auth (free: 500MB + 2 projects)
- **Vercel** - Frontend hosting (free: unlimited hobby projects)
- **Railway** - Backend hosting (free: $5 credit/mo)

## API Endpoints

### Public
- `GET /health` - Health check
- `GET /api/validators` - List top 100 validators (cached)
- `GET /api/validator/:votePubkey` - Get single validator details

### Authenticated (Requires wallet)
- `GET /api/wallet/:address` - Get wallet balance + stake accounts
- `GET /api/user/:wallet/subscription` - Check premium status
- `POST /api/user` - Create/update user record
- `POST /api/webhook/stripe` - Handle Stripe events (TODO)

## Database Schema

### users
```sql
- id (UUID, PK)
- wallet_address (TEXT, unique)
- is_premium (BOOLEAN, default: false)
- subscription_end (TIMESTAMP, nullable)
- stripe_customer_id (TEXT, nullable)
- created_at (TIMESTAMP)
- last_seen (TIMESTAMP)
```

### validators (cache, optional)
```sql
- vote_pubkey (TEXT, PK)
- node_pubkey (TEXT)
- activated_stake (BIGINT)
- commission (INTEGER)
- name (TEXT, nullable)
- website (TEXT, nullable)
- last_updated (TIMESTAMP)
```

### user_alerts
```sql
- id (UUID, PK)
- user_id (UUID, FK → users.id)
- alert_type (TEXT: 'stake_reward' | 'validator_change' | 'large_transfer')
- enabled (BOOLEAN, default: true)
- threshold (NUMERIC, nullable)
- created_at (TIMESTAMP)
```

## Security Considerations

### What We Handle
- ✅ Read-only wallet data (no private keys)
- ✅ HTTPS in production (Vercel/Railway auto)
- ✅ Row-level security in Supabase
- ✅ Input validation on API endpoints
- ✅ Rate limiting (add later for production)

### What User Controls
- ✅ Private keys stay in Seed Vault (never leave device)
- ✅ User approves every transaction
- ✅ User can revoke connection anytime

### What to Add Before Launch
- [ ] CSRF protection
- [ ] API rate limiting (prevent abuse)
- [ ] Request signing (prevent replay attacks)
- [ ] Comprehensive error handling
- [ ] Audit logs for sensitive actions

## Performance

### Caching Strategy
- Validator list: **5 minutes** (rarely changes)
- Wallet data: **No caching** (always fresh)
- User subscription: **1 minute** (cached in frontend)

### Optimization Opportunities
1. Use WebSocket for real-time updates (instead of polling)
2. Lazy-load validator images
3. Paginate validator list (show 20, load more on scroll)
4. Service worker for offline functionality
5. IndexedDB for client-side data persistence

## Monitoring & Observability

### What to Track
- API response times (p50, p95, p99)
- Error rates by endpoint
- Wallet connection success rate
- Transaction success rate
- Premium conversion rate
- Churn rate

### Tools (Add Later)
- **Sentry** - Error tracking
- **PostHog** - Product analytics
- **UptimeRobot** - Uptime monitoring
- **Stripe Dashboard** - Payment metrics

## Scaling Plan

### 100 Users (Target: $1,500/mo)
- Current architecture handles easily
- Free tiers cover all costs
- No infrastructure changes needed

### 500 Users (Target: $7,500/mo)
- Upgrade Helius to paid tier: ~$20/mo
- Upgrade Supabase to Pro: $25/mo
- Keep Railway/Vercel on free or basic paid tiers
- Add Redis for caching: ~$10/mo

### 5,000 Users (Goal: $75,000/mo)
- Dedicated database server: ~$100/mo
- Load balancer: ~$20/mo
- CDN for static assets: ~$30/mo
- Multiple backend instances: ~$200/mo
- Total infrastructure: ~$400-500/mo (0.67% of revenue)

## Development Workflow

### Local Development
```bash
# Terminal 1: Backend
cd backend
npm run dev  # nodemon watches for changes

# Terminal 2: Frontend
cd frontend
npm start  # Hot reload enabled
```

### Testing
```bash
# Unit tests (add later)
npm test

# Integration tests (add later)
npm run test:integration

# E2E tests (add later)
npm run test:e2e
```

### Deployment
```bash
# Backend to Railway
cd backend
railway up

# Frontend to Vercel
cd frontend
vercel --prod
```

---

This architecture is designed for:
- **Fast development** (simple, proven stack)
- **Low cost** (free tiers cover MVP)
- **Easy scaling** (add resources as you grow)
- **Security** (keys never leave device)
- **Great UX** (fast, responsive, mobile-first)

Any questions? Ask me and I'll explain or adjust anything!
