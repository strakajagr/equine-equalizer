import React from 'react';
import { Race } from '../../types';
import HorseRow from './HorseRow';
import BetBadge from './BetBadge';

interface RaceCardProps {
  race: Race;
  raceNumber: number;
}

const COLUMN_HEADERS = [
  { label: '#', width: '48px' },
  { label: 'PP', width: '40px' },
  { label: 'HORSE', width: '1fr' },
  { label: 'CONNECTIONS', width: '160px' },
  { label: 'WIN%', width: '72px', align: 'right' as const },
  { label: 'PLC%', width: '72px', align: 'right' as const },
  { label: 'ML', width: '56px', align: 'right' as const },
  { label: 'OVERLAY', width: '80px', align: 'right' as const },
  { label: 'BET', width: '72px', align: 'center' as const },
  { label: 'FLAGS', width: 'auto' },
];

const RaceCard: React.FC<RaceCardProps> = ({ race, raceNumber }) => {
  const sorted = [...race.predictions].sort(
    (a, b) => a.predicted_rank - b.predicted_rank
  );
  const topPick = sorted[0];
  const valueAlerts = sorted.filter(p => p.is_value_flag);

  return (
    <div className="card-shadow" style={{
      backgroundColor: 'var(--bg-card)',
      border: '1px solid var(--bg-hover)',
      borderRadius: 8,
      marginBottom: 24,
      overflow: 'hidden',
    }}>
      {/* Race header */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '12px 16px',
        backgroundColor: 'var(--bg-secondary)',
        borderBottom: '1px solid var(--gold-dim)',
      }}>
        <div style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '0.9rem',
          fontWeight: 500,
          color: 'var(--gold)',
          letterSpacing: '0.05em',
        }}>
          RACE {raceNumber}
        </div>
        <div style={{
          fontFamily: 'var(--font-body)',
          fontSize: '0.8rem',
          color: 'var(--white-dim)',
        }}>
          {sorted.length} starters
        </div>
        {topPick && (
          <BetBadge betType={topPick.recommended_bet_type} />
        )}
      </div>

      {/* Column headers */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '48px 40px 1fr 160px 72px 72px 56px 80px 72px auto',
        gap: 8,
        padding: '8px 16px',
        borderBottom: '1px solid var(--bg-hover)',
      }}>
        {COLUMN_HEADERS.map(({ label, align }) => (
          <div key={label} style={{
            fontFamily: 'var(--font-body)',
            fontSize: '0.65rem',
            fontWeight: 500,
            color: 'var(--white-dim)',
            textTransform: 'uppercase',
            letterSpacing: '0.08em',
            textAlign: align || 'left',
          }}>
            {label}
          </div>
        ))}
      </div>

      {/* Horse rows */}
      {sorted.map((pred, i) => (
        <HorseRow
          key={pred.prediction_id || i}
          prediction={pred}
          rank={pred.predicted_rank}
        />
      ))}

      {/* Value alert footer */}
      {valueAlerts.length > 0 && (
        <div style={{
          padding: '10px 16px',
          backgroundColor: 'rgba(34,197,94,0.05)',
          borderTop: '1px solid rgba(34,197,94,0.15)',
          display: 'flex',
          alignItems: 'center',
          gap: 12,
        }}>
          <span style={{
            color: 'var(--green)',
            fontSize: '0.8rem',
            fontWeight: 500,
          }}>
            VALUE ALERT
          </span>
          {valueAlerts.map(v => (
            <span key={v.prediction_id} style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.75rem',
              color: 'var(--green)',
            }}>
              {v.horse_name} +{((v.overlay_pct || 0) * 100).toFixed(1)}%
            </span>
          ))}
        </div>
      )}
    </div>
  );
};

export default RaceCard;
