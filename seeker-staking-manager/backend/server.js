require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { Connection, PublicKey, StakeProgram } = require('@solana/web3.js');
const { createClient } = require('@supabase/supabase-js');
const NodeCache = require('node-cache');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Initialize Solana connection
const connection = new Connection(process.env.HELIUS_RPC_URL || 'https://api.mainnet-beta.solana.com');

// Initialize Supabase
const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

// Cache for validator data (5 min TTL)
const cache = new NodeCache({ stdTTL: 300 });

// ===== ROUTES =====

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Get wallet staking info
app.get('/api/wallet/:address', async (req, res) => {
  try {
    const walletPubkey = new PublicKey(req.params.address);
    
    // Get balance
    const balance = await connection.getBalance(walletPubkey);
    
    // Get stake accounts
    const stakeAccounts = await connection.getParsedProgramAccounts(
      StakeProgram.programId,
      {
        filters: [
          {
            memcmp: {
              offset: 12,
              bytes: walletPubkey.toBase58(),
            },
          },
        ],
      }
    );

    const stakes = stakeAccounts.map(account => {
      const data = account.account.data.parsed.info;
      return {
        address: account.pubkey.toBase58(),
        lamports: account.account.lamports,
        state: data.stake?.delegation?.state || 'inactive',
        validator: data.stake?.delegation?.voter || null,
        activationEpoch: data.stake?.delegation?.activationEpoch || null,
      };
    });

    res.json({
      address: req.params.address,
      balance: balance / 1e9, // Convert lamports to SOL
      stakeAccounts: stakes,
      totalStaked: stakes.reduce((sum, s) => sum + s.lamports, 0) / 1e9,
    });
  } catch (error) {
    console.error('Error fetching wallet:', error);
    res.status(500).json({ error: error.message });
  }
});

// Get top validators
app.get('/api/validators', async (req, res) => {
  try {
    // Check cache first
    const cached = cache.get('validators');
    if (cached) {
      return res.json(cached);
    }

    const voteAccounts = await connection.getVoteAccounts();
    
    // Combine and sort by stake
    const allValidators = [...voteAccounts.current, ...voteAccounts.delinquent]
      .sort((a, b) => b.activatedStake - a.activatedStake)
      .slice(0, 100) // Top 100
      .map(v => ({
        votePubkey: v.votePubkey,
        nodePubkey: v.nodePubkey,
        activatedStake: v.activatedStake / 1e9,
        commission: v.commission,
        lastVote: v.lastVote,
        rootSlot: v.rootSlot,
        epochCredits: v.epochCredits?.slice(-5) || [], // Last 5 epochs
        delinquent: voteAccounts.delinquent.some(d => d.votePubkey === v.votePubkey),
      }));

    // Cache for 5 minutes
    cache.set('validators', allValidators);
    
    res.json(allValidators);
  } catch (error) {
    console.error('Error fetching validators:', error);
    res.status(500).json({ error: error.message });
  }
});

// Get validator details
app.get('/api/validator/:votePubkey', async (req, res) => {
  try {
    const voteAccounts = await connection.getVoteAccounts();
    const validator = [...voteAccounts.current, ...voteAccounts.delinquent]
      .find(v => v.votePubkey === req.params.votePubkey);

    if (!validator) {
      return res.status(404).json({ error: 'Validator not found' });
    }

    res.json({
      votePubkey: validator.votePubkey,
      nodePubkey: validator.nodePubkey,
      activatedStake: validator.activatedStake / 1e9,
      commission: validator.commission,
      lastVote: validator.lastVote,
      epochCredits: validator.epochCredits,
      delinquent: voteAccounts.delinquent.some(d => d.votePubkey === req.params.votePubkey),
    });
  } catch (error) {
    console.error('Error fetching validator:', error);
    res.status(500).json({ error: error.message });
  }
});

// User subscription status (requires Supabase setup)
app.get('/api/user/:wallet/subscription', async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('users')
      .select('*')
      .eq('wallet_address', req.params.wallet)
      .single();

    if (error && error.code !== 'PGRST116') { // Not found is ok
      throw error;
    }

    res.json({
      wallet: req.params.wallet,
      isPremium: data?.is_premium || false,
      subscriptionEnd: data?.subscription_end || null,
    });
  } catch (error) {
    console.error('Error fetching subscription:', error);
    res.status(500).json({ error: error.message });
  }
});

// Create/update user (when connecting wallet)
app.post('/api/user', async (req, res) => {
  try {
    const { wallet_address } = req.body;
    
    const { data, error } = await supabase
      .from('users')
      .upsert({ 
        wallet_address,
        last_seen: new Date().toISOString(),
      })
      .select()
      .single();

    if (error) throw error;

    res.json(data);
  } catch (error) {
    console.error('Error creating user:', error);
    res.status(500).json({ error: error.message });
  }
});

// Stripe webhook (for subscription updates)
app.post('/api/webhook/stripe', express.raw({ type: 'application/json' }), async (req, res) => {
  // TODO: Implement Stripe webhook handler when you add payments
  res.json({ received: true });
});

// Start server
app.listen(PORT, () => {
  console.log(`✅ Seeker Staking Manager backend running on port ${PORT}`);
  console.log(`📊 RPC: ${process.env.HELIUS_RPC_URL ? 'Configured' : 'Using public endpoint'}`);
  console.log(`💾 Database: ${process.env.SUPABASE_URL ? 'Connected' : 'Not configured'}`);
});
