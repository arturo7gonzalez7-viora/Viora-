import React, { useState } from 'react';

function ValidatorList({ validators, onStake, isPremium }) {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredValidators = validators
    .filter(v => 
      !v.delinquent && 
      (searchTerm === '' || 
       v.votePubkey.toLowerCase().includes(searchTerm.toLowerCase()))
    )
    .slice(0, 20); // Show top 20

  const formatStake = (stake) => {
    if (stake > 1000000) {
      return `${(stake / 1000000).toFixed(2)}M SOL`;
    }
    return `${stake.toLocaleString()} SOL`;
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search validators..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        style={{
          width: '100%',
          padding: '12px',
          marginBottom: '20px',
          borderRadius: '8px',
          border: '1px solid #ddd',
          fontSize: '16px'
        }}
      />

      <div className="validator-grid">
        {filteredValidators.map((validator, index) => (
          <div key={validator.votePubkey} className="validator-card">
            <div className="validator-info">
              <div className="validator-name">
                #{index + 1} • Commission: {validator.commission}%
              </div>
              <div className="validator-stats">
                {formatStake(validator.activatedStake)} staked
              </div>
              <div style={{ fontSize: '12px', color: '#999', marginTop: '4px' }}>
                {validator.votePubkey.slice(0, 8)}...{validator.votePubkey.slice(-6)}
              </div>
            </div>
            
            <button
              className="btn btn-primary"
              onClick={() => onStake(validator)}
              style={{ minWidth: '100px' }}
            >
              Stake
            </button>
          </div>
        ))}
      </div>

      {!isPremium && filteredValidators.length > 0 && (
        <div style={{
          marginTop: '20px',
          padding: '16px',
          background: '#f8f9fa',
          borderRadius: '8px',
          textAlign: 'center'
        }}>
          <p style={{ color: '#666', marginBottom: '12px' }}>
            <strong>Free tier:</strong> Limited to 1 active stake account
          </p>
          <p style={{ color: '#999', fontSize: '14px' }}>
            Upgrade to Premium for unlimited stakes, auto-optimizer, and advanced analytics
          </p>
        </div>
      )}
    </div>
  );
}

export default ValidatorList;
