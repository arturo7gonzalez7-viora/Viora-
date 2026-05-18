import React, { useState, useEffect } from 'react';
import { useWallet } from '@solana/wallet-adapter-react';
import { WalletMultiButton } from '@solana/wallet-adapter-react-ui';
import axios from 'axios';
import ValidatorList from './ValidatorList';
import StakingStats from './StakingStats';
import PremiumModal from './PremiumModal';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';

function Dashboard() {
  const { publicKey, connected } = useWallet();
  const [walletData, setWalletData] = useState(null);
  const [validators, setValidators] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isPremium, setIsPremium] = useState(false);
  const [showPremiumModal, setShowPremiumModal] = useState(false);

  // Fetch wallet data when connected
  useEffect(() => {
    if (connected && publicKey) {
      fetchWalletData();
      fetchUserSubscription();
      registerUser();
    }
  }, [connected, publicKey]);

  // Fetch validators on mount
  useEffect(() => {
    fetchValidators();
  }, []);

  const fetchWalletData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_URL}/api/wallet/${publicKey.toBase58()}`);
      setWalletData(response.data);
    } catch (err) {
      setError('Failed to fetch wallet data: ' + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchValidators = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/validators`);
      setValidators(response.data);
    } catch (err) {
      console.error('Failed to fetch validators:', err);
    }
  };

  const fetchUserSubscription = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/user/${publicKey.toBase58()}/subscription`);
      setIsPremium(response.data.isPremium);
    } catch (err) {
      console.error('Failed to fetch subscription:', err);
    }
  };

  const registerUser = async () => {
    try {
      await axios.post(`${API_URL}/api/user`, {
        wallet_address: publicKey.toBase58()
      });
    } catch (err) {
      console.error('Failed to register user:', err);
    }
  };

  const handleStake = (validator) => {
    if (!isPremium && walletData?.stakeAccounts?.length >= 1) {
      setShowPremiumModal(true);
      return;
    }
    // TODO: Implement actual staking transaction
    alert(`Staking to validator: ${validator.votePubkey}\n\nThis will open a transaction dialog in Seed Vault.`);
  };

  return (
    <div className="container">
      {/* Header */}
      <div className="header">
        <div className="logo">
          ⚡ Seeker Staking Manager
          {isPremium && <span className="premium-badge">PREMIUM</span>}
        </div>
        <WalletMultiButton />
      </div>

      {/* Error display */}
      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {/* Not connected state */}
      {!connected && (
        <div className="card">
          <h2 style={{ marginBottom: '16px' }}>Welcome to Seeker Staking Manager</h2>
          <p style={{ marginBottom: '24px', color: '#666' }}>
            Connect your Seed Vault wallet to start optimizing your Solana staking rewards.
          </p>
          <WalletMultiButton />
        </div>
      )}

      {/* Loading state */}
      {loading && <div className="loading">Loading your staking data...</div>}

      {/* Connected and loaded */}
      {connected && !loading && walletData && (
        <>
          <StakingStats data={walletData} isPremium={isPremium} />
          
          <div className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h2>Top Validators</h2>
              {!isPremium && (
                <button 
                  className="btn btn-primary"
                  onClick={() => setShowPremiumModal(true)}
                >
                  Upgrade to Premium
                </button>
              )}
            </div>
            <ValidatorList 
              validators={validators} 
              onStake={handleStake}
              isPremium={isPremium}
            />
          </div>
        </>
      )}

      {/* Premium Modal */}
      {showPremiumModal && (
        <PremiumModal 
          onClose={() => setShowPremiumModal(false)}
          walletAddress={publicKey?.toBase58()}
        />
      )}
    </div>
  );
}

export default Dashboard;
