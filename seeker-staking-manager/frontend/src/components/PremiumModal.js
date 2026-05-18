import React from 'react';

function PremiumModal({ onClose, walletAddress }) {
  const handleUpgrade = () => {
    // TODO: Integrate with Stripe when you add payment processing
    alert(`Premium upgrade for wallet: ${walletAddress}\n\nStripe integration coming soon!\n\nFor now, this is just a demo.`);
    onClose();
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0,0,0,0.7)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '20px'
    }}>
      <div style={{
        background: 'white',
        borderRadius: '16px',
        padding: '32px',
        maxWidth: '500px',
        width: '100%'
      }}>
        <h2 style={{ marginBottom: '16px' }}>Upgrade to Premium</h2>
        
        <div style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          padding: '24px',
          borderRadius: '12px',
          marginBottom: '24px',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '48px', fontWeight: 'bold', marginBottom: '8px' }}>
            $15
          </div>
          <div style={{ opacity: 0.9 }}>per month</div>
        </div>

        <h3 style={{ marginBottom: '16px' }}>Premium Features:</h3>
        <ul style={{ 
          marginBottom: '24px', 
          paddingLeft: '20px',
          lineHeight: '2'
        }}>
          <li>✅ Unlimited active stake accounts</li>
          <li>✅ Auto-optimizer algorithm (max APY)</li>
          <li>✅ Advanced performance analytics</li>
          <li>✅ Multi-wallet support</li>
          <li>✅ Real-time push alerts</li>
          <li>✅ Validator ratings & reviews</li>
          <li>✅ Priority support</li>
        </ul>

        <div style={{ display: 'flex', gap: '12px' }}>
          <button 
            className="btn btn-primary"
            onClick={handleUpgrade}
            style={{ flex: 1 }}
          >
            Upgrade Now
          </button>
          <button 
            className="btn btn-secondary"
            onClick={onClose}
            style={{ flex: 1 }}
          >
            Maybe Later
          </button>
        </div>

        <p style={{ 
          marginTop: '16px', 
          fontSize: '12px', 
          color: '#999',
          textAlign: 'center' 
        }}>
          Cancel anytime. No long-term commitments.
        </p>
      </div>
    </div>
  );
}

export default PremiumModal;
