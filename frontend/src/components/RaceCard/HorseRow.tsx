import React from 'react';
import { Prediction } from '../../types';
import BetBadge from './BetBadge';

interface HorseRowProps {
  prediction: Prediction;
  rank: number;
}

const toFractionalOdds = (decimal: number | null): string => {
  if (decimal === null || decimal === undefined) return '--';
  const whole = Math.round(decimal);
  return `${whole}-1`;
};

const pct = (v: number): string => `${(v * 100).toFixed(1)}%`;

const HorseRow: React.FC<HorseRowProps> = ({ prediction: p, rank }) => {
  const isTop = p.is_top_pick;
  const isValue = p.is_value_flag;

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: '48px 40px 1fr 160px 72px 72px 56px 80px 72px auto',
      alignItems: 'center',
      gap: 8,
      padding: '12px 16px',
      backgroundColor: isTop ? 'rgba(201,168,76,0.04)' : 'var(--bg-card)',
      borderLeft: isTop
        ? '3px solid var(--gold)'
        : isValue
          ? '3px solid var(--green)'
          : '3px solid transparent',
      borderBottom: '1px solid var(--bg-secondary)',
      transition: 'background-color 0.15s',
      cursor: 'default',
    }}
    onMouseEnter={e => { (e.currentTarget as HTMLElement).style.backgroundColor = 'var(--bg-hover)'; }}
    onMouseLeave={e => { (e.currentTarget as HTMLElement).style.backgroundColor = isTop ? 'rgba(201,168,76,0.04)' : 'var(--bg-card)'; }}
    >
      {/* RANK */}
      <div style={{
        fontFamily: 'var(--font-mono)',
        fontSize: isTop ? '1.5rem' : '1.1rem',
        fontWeight: 500,
        color: isTop ? 'var(--gold)' : 'var(--white-dim)',
        textAlign: 'center',
      }}>
        {rank}
      </div>

      {/* PP (post position) */}
      <div style={{
        width: 28, height: 28,
        borderRadius: '50%',
        border: '1px solid var(--white-dim)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        fontFamily: 'var(--font-mono)',
        fontSize: '0.75rem',
        color: 'var(--white-dim)',
      }}>
        {p.post_position}
      </div>

      {/* HORSE NAME */}
      <div>
        <div style={{
          fontFamily: 'var(--font-display)',
          fontSize: '0.95rem',
          fontWeight: isTop ? 700 : 400,
          color: isTop ? 'var(--gold)' : 'var(--white)',
        }}>
          {p.horse_name}
        </div>
      </div>

      {/* JOCKEY / TRAINER */}
      <div style={{ lineHeight: 1.3 }}>
        <div style={{ fontSize: '0.72rem', color: 'var(--white-dim)' }}>
          {p.jockey_name || 'TBD'}
        </div>
        <div style={{ fontSize: '0.68rem', color: 'var(--white-dim)', opacity: 0.7 }}>
          {p.trainer_name}
        </div>
      </div>

      {/* WIN% */}
      <div style={{
        fontFamily: 'var(--font-mono)',
        fontSize: '0.85rem',
        fontWeight: 500,
        color: p.win_probability >= 0.30
          ? 'var(--gold)'
          : p.win_probability >= 0.20
            ? 'var(--white)'
            : 'var(--white-dim)',
        textAlign: 'right',
      }}>
        {pct(p.win_probability)}
      </div>

      {/* PLACE% */}
      <div style={{
        fontFamily: 'var(--font-mono)',
        fontSize: '0.8rem',
        color: 'var(--white-dim)',
        textAlign: 'right',
      }}>
        {pct(p.place_probability)}
      </div>

      {/* ML */}
      <div style={{
        fontFamily: 'var(--font-mono)',
        fontSize: '0.8rem',
        color: 'var(--white-dim)',
        textAlign: 'right',
      }}>
        {toFractionalOdds(p.morning_line_odds)}
      </div>

      {/* OVERLAY */}
      <div style={{
        fontFamily: 'var(--font-mono)',
        fontSize: '0.8rem',
        fontWeight: p.is_value_flag ? 500 : 400,
        color: p.overlay_pct === null
          ? 'var(--white-dim)'
          : p.overlay_pct > 0
            ? 'var(--green)'
            : 'var(--red)',
        textAlign: 'right',
      }}>
        {p.overlay_pct !== null
          ? `${p.overlay_pct > 0 ? '+' : ''}${(p.overlay_pct * 100).toFixed(1)}%`
          : '--'}
      </div>

      {/* BET */}
      <div style={{ textAlign: 'center' }}>
        <BetBadge betType={p.recommended_bet_type} />
      </div>

      {/* FLAGS */}
      <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
        {p.lasix_first_time && (
          <span style={{
            fontSize: '0.6rem', padding: '2px 6px', borderRadius: 8,
            backgroundColor: 'rgba(201,168,76,0.2)', color: 'var(--gold-light)',
            fontFamily: 'var(--font-mono)', whiteSpace: 'nowrap',
          }}>1st LASIX</span>
        )}
        {p.blinkers_first_time && (
          <span style={{
            fontSize: '0.6rem', padding: '2px 6px', borderRadius: 8,
            backgroundColor: 'rgba(96,165,250,0.2)', color: 'var(--blue)',
            fontFamily: 'var(--font-mono)', whiteSpace: 'nowrap',
          }}>BLINKERS</span>
        )}
        {p.equipment_change && (
          <span style={{
            fontSize: '0.6rem', padding: '2px 6px', borderRadius: 8,
            backgroundColor: 'rgba(160,160,176,0.15)', color: 'var(--white-dim)',
            fontFamily: 'var(--font-mono)', whiteSpace: 'nowrap',
          }}>EQUIP &Delta;</span>
        )}
      </div>
    </div>
  );
};

export default HorseRow;
