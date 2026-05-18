import React from 'react';

function StakingStats({ data, isPremium }) {
  const formatSOL = (amount) => {
    return amount.toLocaleString('en-US', { 
      minimumFractionDigits: 2, 
      maximumFractionDigits: 4 
    });
  };

  // Calculate estimated APY (simplified - real calculation would be more complex)
  const estimatedAPY = 7.2; // Example APY

  const activeStakes = data.stakeAccounts?.filter(s => s.state !== 'inactive').length || 0;

  return (
    <div className="stats-grid">
      <div className="stat-card">
        <div className="stat-label">Wallet Balance</div>
        <div className="stat-value">{formatSOL(data.balance)} SOL</div>
      </div>
      
      <div className="stat-card">
        <div className="stat-label">Total Staked</div>
        <div className="stat-value">{formatSOL(data.totalStaked)} SOL</div>
      </div>
      
      <div className="stat-card">
        <div className="stat-label">Active Stakes</div>
        <div className="stat-value">{activeStakes}</div>
      </div>
      
      <div className="stat-card">
        <div className="stat-label">Est. APY</div>
        <div className="stat-value">{estimatedAPY}%</div>
        {isPremium && (
          <div style={{ fontSize: '12px', marginTop: '8px', opacity: 0.9 }}>
            Premium: Auto-optimized
          </div>
        )}
      </div>
    </div>
  );
}

export default StakingStats;
