import React from 'react';

interface LoadingSpinnerProps {
  message?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ message }) => {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '80px 0',
    }}>
      <div style={{
        width: 40,
        height: 40,
        border: '3px solid var(--bg-hover)',
        borderTop: '3px solid var(--gold)',
        borderRadius: '50%',
        animation: 'spin 0.8s linear infinite',
        marginBottom: 16,
      }} />
      {message && (
        <div style={{
          fontFamily: 'var(--font-body)',
          fontSize: '0.85rem',
          color: 'var(--white-dim)',
        }}>
          {message}
        </div>
      )}
    </div>
  );
};

export default LoadingSpinner;
