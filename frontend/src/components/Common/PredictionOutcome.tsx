import React from 'react';
import { PredictionOutcome } from '../../types';

/**
 * Stream E3 — color-coded outcome badge + signed P/L cell.
 * Shared across TodayPage, ValuePlaysPage, LongshotPage, ComparePage so
 * every prediction surface renders the same shape.
 *
 * Outcome enum semantics (from backend Stream E1):
 *   'win'       → finish_position = 1
 *   'place'     → finish_position = 2
 *   'show'      → finish_position = 3
 *   'lose'      → finish_position 4..N
 *   'pending'   → race not yet settled (no results row)
 *   'scratched' → entry.is_scratched = TRUE
 */

export const OutcomeBadge: React.FC<{
  outcome: PredictionOutcome | null | undefined;
  /** Optional: 'compact' shaves padding/font for narrow grids */
  size?: 'compact' | 'default';
}> = ({ outcome, size = 'default' }) => {
  const compact = size === 'compact';
  const baseStyle: React.CSSProperties = {
    display: 'inline-block',
    fontFamily: 'var(--font-mono)',
    fontSize: compact ? '0.55rem' : '0.65rem',
    fontWeight: 600,
    letterSpacing: '0.08em',
    padding: compact ? '1px 6px' : '2px 8px',
    borderRadius: 4,
    textAlign: 'center',
    minWidth: compact ? 36 : 50,
  };

  switch (outcome) {
    case 'win':
      return <span style={{ ...baseStyle,
        backgroundColor: 'rgba(34,197,94,0.22)',
        color: 'var(--green)',
        border: '1px solid rgba(34,197,94,0.35)',
      }}>WIN</span>;
    case 'place':
      return <span style={{ ...baseStyle,
        backgroundColor: 'rgba(234,179,8,0.18)',
        color: '#facc15',
        border: '1px solid rgba(234,179,8,0.3)',
      }}>Place</span>;
    case 'show':
      return <span style={{ ...baseStyle,
        backgroundColor: 'rgba(234,179,8,0.10)',
        color: '#facc15',
        border: '1px solid rgba(234,179,8,0.2)',
      }}>Show</span>;
    case 'lose':
      return <span style={{ ...baseStyle,
        backgroundColor: 'var(--bg-hover)',
        color: 'var(--white-dim)',
        border: '1px solid rgba(255,255,255,0.06)',
      }}>—</span>;
    case 'pending':
      return <span style={{ ...baseStyle,
        backgroundColor: 'rgba(59,130,246,0.18)',
        color: '#60a5fa',
        border: '1px solid rgba(59,130,246,0.3)',
      }}>Pending</span>;
    case 'scratched':
      return <span style={{ ...baseStyle,
        backgroundColor: 'transparent',
        color: 'var(--white-dim)',
        border: '1px dashed rgba(255,255,255,0.25)',
        textDecoration: 'line-through',
      }}>SCR</span>;
    default:
      return <span style={{ ...baseStyle,
        backgroundColor: 'transparent',
        color: 'var(--white-dim)',
        opacity: 0.4,
      }}>—</span>;
  }
};

/**
 * Signed P/L cell. NULL renders as a muted "—" — covers both pending
 * races AND winners-with-incomplete-payout-data (the chart-parser gap).
 * See deferred bug #5 for the data quality issue.
 */
export const PLCell: React.FC<{
  pl: number | null | undefined;
  size?: 'compact' | 'default';
  align?: 'left' | 'right' | 'center';
}> = ({ pl, size = 'default', align = 'right' }) => {
  const compact = size === 'compact';
  const baseStyle: React.CSSProperties = {
    fontFamily: 'var(--font-mono)',
    fontSize: compact ? '0.7rem' : '0.78rem',
    fontWeight: 500,
    textAlign: align,
  };
  if (pl == null) {
    return <span style={{ ...baseStyle, color: 'var(--white-dim)', opacity: 0.4 }}>—</span>;
  }
  const positive = pl >= 0;
  return (
    <span style={{
      ...baseStyle,
      color: positive ? 'var(--green)' : 'var(--red)',
    }}>
      {positive ? '+' : ''}{pl < 0 ? '-' : ''}${Math.abs(pl).toFixed(2)}
    </span>
  );
};

/**
 * Tooltip text for the P/L column header. Reuse across all pages so
 * the disclosure language is consistent.
 */
export const PL_HEADER_TOOLTIP =
  'Hypothetical $2 win bet on this horse. ' +
  'Some winners have incomplete payout data ingested — see deferred chart-parser bug.';
