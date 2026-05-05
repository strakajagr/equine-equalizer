import React from 'react';
import { CompareHorse, CompareSidePair } from '../../types/predictions';

interface Props {
  horse: CompareHorse;
  side: 'general' | 'specialist';
  highlightDiff: boolean;
  rankShift: number; // signed: specialist_rank − general_rank
}

const RANK_HIGHLIGHT_THRESHOLD = 3;

function fmtPct(v: number | null | undefined, digits = 1): string {
  if (v === null || v === undefined) return '—';
  return (v * 100).toFixed(digits) + '%';
}

function fmtRank(v: number | null | undefined): string {
  if (v === null || v === undefined) return '—';
  return String(v);
}

const ProbBar: React.FC<{ v: number | null; color: string }> = ({ v, color }) => {
  const pct = Math.min(100, Math.max(0, (v ?? 0) * 100));
  return (
    <div style={{
      width: '100%',
      height: 6,
      backgroundColor: 'var(--bg-hover)',
      borderRadius: 3,
      overflow: 'hidden',
      marginTop: 2,
    }}>
      <div style={{
        height: '100%',
        width: `${pct}%`,
        backgroundColor: color,
        transition: 'width 0.25s',
      }} />
    </div>
  );
};

const CompareHorseRow: React.FC<Props> = ({
  horse, side, highlightDiff, rankShift,
}) => {
  const pair: CompareSidePair = side === 'general' ? horse.general : horse.specialist;
  const rank = pair.wr.predicted_rank;
  const wp = pair.wr.win_probability;
  const edge = pair.wr.edge_pct;
  const kelly = pair.wr.kelly_fraction;
  const plWp = pair.pl.win_probability;
  const plKelly = pair.pl.kelly_fraction;
  const isTop = pair.wr.is_top_pick;
  const isValue = pair.wr.is_value_flag;

  // Highlight when rank shift is meaningful (≥ threshold, abs value)
  const showShiftBadge = highlightDiff && Math.abs(rankShift) >= RANK_HIGHLIGHT_THRESHOLD;
  const shiftColor = rankShift > 0 ? 'var(--green)' : '#ef4444';

  const borderLeft = isTop
    ? '3px solid var(--gold)'
    : (showShiftBadge
      ? `3px solid ${shiftColor}`
      : '3px solid transparent');

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: '34px 1fr 56px',
      gap: 8,
      padding: '8px 12px',
      borderBottom: '1px solid var(--bg-hover)',
      borderLeft,
      alignItems: 'center',
      backgroundColor: isTop ? 'rgba(212,175,55,0.04)' : 'transparent',
    }}>
      {/* rank */}
      <div style={{
        fontFamily: 'var(--font-mono)',
        fontSize: '0.95rem',
        fontWeight: 600,
        color: isTop ? 'var(--gold)' : 'var(--white-dim)',
        textAlign: 'center',
      }}>
        {fmtRank(rank)}
      </div>

      {/* horse name + bars */}
      <div>
        <div style={{
          display: 'flex',
          alignItems: 'baseline',
          gap: 8,
        }}>
          <span style={{
            fontFamily: 'var(--font-body)',
            fontSize: '0.85rem',
            fontWeight: 500,
            color: 'var(--white)',
          }}>
            {horse.horse_name || '?'}
          </span>
          {horse.program_number && (
            <span style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.65rem',
              color: 'var(--white-dim)',
              opacity: 0.7,
            }}>
              #{horse.program_number}
            </span>
          )}
          {isValue && (
            <span style={{
              fontSize: '0.55rem',
              fontFamily: 'var(--font-mono)',
              color: 'var(--green)',
              border: '1px solid var(--green)',
              padding: '0px 4px',
              borderRadius: 2,
              letterSpacing: '0.05em',
            }}>VALUE</span>
          )}
          {showShiftBadge && side === 'specialist' && (
            <span style={{
              fontSize: '0.55rem',
              fontFamily: 'var(--font-mono)',
              color: shiftColor,
              padding: '0px 4px',
              border: `1px solid ${shiftColor}`,
              borderRadius: 2,
              letterSpacing: '0.05em',
            }}>
              {rankShift > 0 ? `+${rankShift}` : rankShift}
            </span>
          )}
        </div>

        {/* WR win-prob bar */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: 6,
          marginTop: 4,
        }}>
          <span style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '0.62rem',
            color: 'var(--white-dim)',
            width: 22,
          }}>WR</span>
          <div style={{ flex: 1 }}>
            <ProbBar v={wp} color="var(--gold)" />
          </div>
          <span style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '0.7rem',
            color: 'var(--white)',
            minWidth: 48,
            textAlign: 'right',
          }}>{fmtPct(wp, 2)}</span>
        </div>

        {/* PL place-prob bar */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: 6,
          marginTop: 2,
        }}>
          <span style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '0.62rem',
            color: 'var(--white-dim)',
            width: 22,
          }}>PL</span>
          <div style={{ flex: 1 }}>
            <ProbBar v={plWp} color="var(--green)" />
          </div>
          <span style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '0.7rem',
            color: 'var(--white-dim)',
            minWidth: 48,
            textAlign: 'right',
          }}>{fmtPct(plWp, 2)}</span>
        </div>
      </div>

      {/* edge / kelly */}
      <div style={{
        textAlign: 'right',
        fontFamily: 'var(--font-mono)',
        fontSize: '0.65rem',
        color: 'var(--white-dim)',
      }}>
        <div style={{
          color: edge && edge > 0 ? 'var(--green)' : 'var(--white-dim)',
        }}>
          edge {fmtPct(edge, 1)}
        </div>
        <div style={{ marginTop: 2 }}>
          k {kelly === null || kelly === undefined ? '—' : kelly.toFixed(2)}
        </div>
        <div style={{ marginTop: 2, color: '#9ca3af' }}>
          ML {horse.morning_line_odds === null ? '—' :
              `${horse.morning_line_odds.toFixed(1)}`}
        </div>
      </div>
    </div>
  );
};

export default CompareHorseRow;
