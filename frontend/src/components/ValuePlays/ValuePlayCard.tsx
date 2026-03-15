import React from 'react';
import { Prediction } from '../../types';
import BetBadge from '../RaceCard/BetBadge';

interface ValuePlayCardProps {
  prediction: Prediction;
}

const ValuePlayCard: React.FC<ValuePlayCardProps> = ({ prediction: p }) => {
  const overlayStr = p.overlay_pct !== null
    ? `+${(p.overlay_pct * 100).toFixed(1)}%`
    : '--';

  return (
    <div
      className="card-shadow"
      style={{
        backgroundColor: 'var(--bg-card)',
        border: '1px solid rgba(34,197,94,0.2)',
        borderLeft: '4px solid var(--green)',
        borderRadius: 8,
        padding: '20px 24px',
        transition: 'transform 0.15s, box-shadow 0.15s',
        cursor: 'default',
      }}
      onMouseEnter={e => {
        (e.currentTarget as HTMLElement).style.transform = 'translateY(-2px)';
        (e.currentTarget as HTMLElement).style.boxShadow = '0 6px 20px rgba(34,197,94,0.1)';
      }}
      onMouseLeave={e => {
        (e.currentTarget as HTMLElement).style.transform = 'translateY(0)';
        (e.currentTarget as HTMLElement).style.boxShadow = '';
      }}
    >
      {/* Horse name */}
      <div style={{
        fontFamily: 'var(--font-display)',
        fontSize: '1.25rem',
        fontWeight: 700,
        color: 'var(--white)',
        marginBottom: 8,
      }}>
        {p.horse_name}
      </div>

      {/* Overlay — the hero number */}
      <div style={{
        fontFamily: 'var(--font-mono)',
        fontSize: '2rem',
        fontWeight: 500,
        color: 'var(--green)',
        lineHeight: 1.1,
        marginBottom: 12,
      }}>
        {overlayStr}
        <span style={{
          fontSize: '0.85rem',
          color: 'var(--green)',
          marginLeft: 8,
          opacity: 0.8,
        }}>
          OVERLAY
        </span>
      </div>

      {/* Stats row */}
      <div style={{
        display: 'flex',
        gap: 24,
        marginBottom: 16,
        fontSize: '0.8rem',
      }}>
        <div>
          <span style={{ color: 'var(--white-dim)' }}>Win </span>
          <span style={{
            fontFamily: 'var(--font-mono)',
            color: 'var(--white)',
            fontWeight: 500,
          }}>
            {(p.win_probability * 100).toFixed(1)}%
          </span>
        </div>
        <div>
          <span style={{ color: 'var(--white-dim)' }}>ML </span>
          <span style={{
            fontFamily: 'var(--font-mono)',
            color: 'var(--white)',
          }}>
            {p.morning_line_odds !== null ? `${Math.round(p.morning_line_odds)}-1` : '--'}
          </span>
        </div>
        <div>
          <span style={{ color: 'var(--white-dim)' }}>Rank </span>
          <span style={{
            fontFamily: 'var(--font-mono)',
            color: p.predicted_rank === 1 ? 'var(--gold)' : 'var(--white)',
          }}>
            #{p.predicted_rank}
          </span>
        </div>
      </div>

      {/* Connections + badge */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
      }}>
        <div style={{ fontSize: '0.75rem', color: 'var(--white-dim)' }}>
          {p.trainer_name} / {p.jockey_name || 'TBD'}
        </div>
        <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
          {p.lasix_first_time && (
            <span style={{
              fontSize: '0.6rem', padding: '2px 6px', borderRadius: 8,
              backgroundColor: 'rgba(201,168,76,0.2)', color: 'var(--gold-light)',
              fontFamily: 'var(--font-mono)',
            }}>1st LASIX</span>
          )}
          {p.blinkers_first_time && (
            <span style={{
              fontSize: '0.6rem', padding: '2px 6px', borderRadius: 8,
              backgroundColor: 'rgba(96,165,250,0.2)', color: 'var(--blue)',
              fontFamily: 'var(--font-mono)',
            }}>BLINKERS</span>
          )}
          <BetBadge betType={p.recommended_bet_type} />
        </div>
      </div>
    </div>
  );
};

export default ValuePlayCard;
