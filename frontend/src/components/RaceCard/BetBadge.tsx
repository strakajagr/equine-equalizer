import React from 'react';

interface BetBadgeProps {
  betType: string;
}

const CONFIG: Record<string, { bg: string; text: string; label: string }> = {
  single:       { bg: 'var(--gold)',   text: '#0a0a0f', label: 'WIN' },
  exacta_box:   { bg: 'var(--blue)',   text: '#0a0a0f', label: 'EX BOX' },
  trifecta_box: { bg: 'var(--purple)', text: '#0a0a0f', label: 'TRI BOX' },
  skip:         { bg: 'var(--bg-hover)', text: 'var(--white-dim)', label: '\u2014' },
};

const BetBadge: React.FC<BetBadgeProps> = ({ betType }) => {
  const cfg = CONFIG[betType] || CONFIG.skip;

  return (
    <span style={{
      display: 'inline-block',
      fontFamily: 'var(--font-mono)',
      fontSize: '0.65rem',
      fontWeight: 500,
      textTransform: 'uppercase',
      letterSpacing: '0.05em',
      background: cfg.bg,
      color: cfg.text,
      padding: '3px 8px',
      borderRadius: 12,
      whiteSpace: 'nowrap',
    }}>
      {cfg.label}
    </span>
  );
};

export default BetBadge;
