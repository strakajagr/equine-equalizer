import React from 'react';

interface EmptyStateProps {
  title: string;
  subtitle?: string;
}

const EmptyState: React.FC<EmptyStateProps> = ({ title, subtitle }) => {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '80px 0',
      textAlign: 'center',
    }}>
      <div style={{ fontSize: '3rem', opacity: 0.15, marginBottom: 16 }}>
        &#127943;
      </div>
      <div style={{
        fontFamily: 'var(--font-display)',
        fontSize: '1.1rem',
        color: 'var(--white-dim)',
        marginBottom: 8,
      }}>
        {title}
      </div>
      {subtitle && (
        <div style={{
          fontFamily: 'var(--font-body)',
          fontSize: '0.85rem',
          color: 'var(--white-dim)',
          opacity: 0.7,
          maxWidth: 400,
        }}>
          {subtitle}
        </div>
      )}
    </div>
  );
};

export default EmptyState;
