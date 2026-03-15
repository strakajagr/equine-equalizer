import React from 'react';

interface ModelStatsProps {
  raceCount: number;
  exactaHits: number;
  trifectaHits: number;
}

const ModelStats: React.FC<ModelStatsProps> = ({
  raceCount,
  exactaHits,
  trifectaHits,
}) => {
  const exactaPct = raceCount > 0 ? ((exactaHits / raceCount) * 100).toFixed(0) : '0';
  const trifectaPct = raceCount > 0 ? ((trifectaHits / raceCount) * 100).toFixed(0) : '0';

  return (
    <div style={{
      display: 'flex',
      gap: 32,
      padding: '12px 20px',
      backgroundColor: 'var(--bg-secondary)',
      borderRadius: 8,
      border: '1px solid var(--bg-hover)',
      fontFamily: 'var(--font-mono)',
      fontSize: '0.8rem',
    }}>
      <div>
        <span style={{ color: 'var(--white-dim)' }}>{raceCount}</span>
        <span style={{ color: 'var(--white-dim)', opacity: 0.6, marginLeft: 6 }}>races</span>
      </div>
      <div>
        <span style={{ color: 'var(--gold)' }}>{exactaHits}</span>
        <span style={{ color: 'var(--white-dim)', opacity: 0.6, marginLeft: 6 }}>
          exacta hits ({exactaPct}%)
        </span>
      </div>
      <div>
        <span style={{ color: 'var(--gold)' }}>{trifectaHits}</span>
        <span style={{ color: 'var(--white-dim)', opacity: 0.6, marginLeft: 6 }}>
          trifecta hits ({trifectaPct}%)
        </span>
      </div>
    </div>
  );
};

export default ModelStats;
