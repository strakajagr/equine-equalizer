import React from 'react';
import {
  CompareRace, SpecialistStyle, STYLE_LABELS,
} from '../../types/predictions';
import StyleSelector from './StyleSelector';
import CompareHorseRow from './CompareHorseRow';
import { OutcomeBadge, PLCell, PL_HEADER_TOOLTIP } from '../Common/PredictionOutcome';

interface Props {
  race: CompareRace;
  compareStyle: SpecialistStyle;
  onStyleChange: (s: SpecialistStyle) => void;
  showStyleSelector: boolean; // only show on the FIRST card to avoid 30 selectors
}

const CompareRaceCard: React.FC<Props> = ({
  race, compareStyle, onStyleChange, showStyleSelector,
}) => {
  // Sort horses by general predicted_rank ascending; nulls last.
  const horses = [...race.horses].sort((a, b) => {
    const ar = a.general.wr.predicted_rank;
    const br = b.general.wr.predicted_rank;
    if (ar === null && br === null) return 0;
    if (ar === null) return 1;
    if (br === null) return -1;
    return ar - br;
  });

  // Derive top-1 picks for each side
  const generalTop = horses.find(h => h.general.wr.is_top_pick);
  const specialistTop = horses.find(h => h.specialist.wr.is_top_pick);
  const disagree = generalTop && specialistTop &&
    generalTop.entry_id !== specialistTop.entry_id;

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
        gap: 16,
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'baseline',
          gap: 12,
        }}>
          <span style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '0.9rem',
            fontWeight: 500,
            color: 'var(--gold)',
            letterSpacing: '0.05em',
          }}>
            {race.track_code} R{race.race_number}
          </span>
          {race.race_name && (
            <span style={{
              fontFamily: 'var(--font-body)',
              fontSize: '0.85rem',
              color: 'var(--white)',
            }}>
              {race.race_name}
            </span>
          )}
        </div>
        <div style={{
          fontFamily: 'var(--font-body)',
          fontSize: '0.75rem',
          color: 'var(--white-dim)',
        }}>
          {race.purse !== null && (
            <span style={{ marginRight: 12 }}>
              ${race.purse.toLocaleString()}
            </span>
          )}
          {horses.length} starters
        </div>
      </div>

      {/* Disagreement chip */}
      {disagree && (
        <div style={{
          padding: '8px 16px',
          backgroundColor: 'rgba(212,175,55,0.08)',
          borderBottom: '1px solid var(--gold-dim)',
          fontFamily: 'var(--font-body)',
          fontSize: '0.78rem',
          color: 'var(--gold)',
          letterSpacing: '0.04em',
        }}>
          ⚠ <b>SPECIALIST DISAGREES</b>:
          {' '}General picks <b>{generalTop?.horse_name}</b>;
          {' '}{STYLE_LABELS[compareStyle]} picks <b>{specialistTop?.horse_name}</b>
        </div>
      )}

      {/* Three-column body: General | Specialist | Result+P/L */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr 130px',
        gap: 0,
      }}>
        {/* LEFT — General */}
        <div style={{
          borderRight: '1px solid var(--bg-hover)',
        }}>
          <div style={{
            padding: '8px 12px',
            backgroundColor: 'var(--bg-primary)',
            borderBottom: '1px solid var(--bg-hover)',
            fontFamily: 'var(--font-body)',
            fontSize: '0.7rem',
            fontWeight: 600,
            color: 'var(--white-dim)',
            letterSpacing: '0.1em',
            textTransform: 'uppercase',
          }}>
            General
          </div>
          {horses.map((h) => (
            <CompareHorseRow
              key={`${h.entry_id}-g`}
              horse={h}
              side="general"
              highlightDiff={!!h.general.wr.predicted_rank
                && !!h.specialist.wr.predicted_rank}
              rankShift={
                ((h.specialist.wr.predicted_rank ?? 0)
                  - (h.general.wr.predicted_rank ?? 0))
              }
            />
          ))}
        </div>

        {/* MIDDLE — Specialist */}
        <div style={{
          borderRight: '1px solid var(--bg-hover)',
        }}>
          <div style={{
            padding: '8px 12px',
            backgroundColor: 'var(--bg-primary)',
            borderBottom: '1px solid var(--bg-hover)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: 8,
          }}>
            <span style={{
              fontFamily: 'var(--font-body)',
              fontSize: '0.7rem',
              fontWeight: 600,
              color: 'var(--gold)',
              letterSpacing: '0.1em',
              textTransform: 'uppercase',
            }}>
              {STYLE_LABELS[compareStyle]}
            </span>
            {showStyleSelector && (
              <StyleSelector
                value={compareStyle}
                onChange={onStyleChange}
              />
            )}
          </div>
          {horses.map((h) => (
            <CompareHorseRow
              key={`${h.entry_id}-s`}
              horse={h}
              side="specialist"
              highlightDiff={!!h.general.wr.predicted_rank
                && !!h.specialist.wr.predicted_rank}
              rankShift={
                ((h.specialist.wr.predicted_rank ?? 0)
                  - (h.general.wr.predicted_rank ?? 0))
              }
            />
          ))}
        </div>

        {/* RIGHT — Entry-level Result + P/L (single column shared across both sides) */}
        <div>
          <div style={{
            padding: '8px 12px',
            backgroundColor: 'var(--bg-primary)',
            borderBottom: '1px solid var(--bg-hover)',
            fontFamily: 'var(--font-body)',
            fontSize: '0.7rem',
            fontWeight: 600,
            color: 'var(--white-dim)',
            letterSpacing: '0.1em',
            textTransform: 'uppercase',
            textAlign: 'center',
          }} title={PL_HEADER_TOOLTIP}>
            Result / P/L
          </div>
          {horses.map((h) => (
            <div key={`${h.entry_id}-r`} style={{
              padding: '8px 12px',
              borderBottom: '1px solid var(--bg-hover)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              gap: 4,
              minHeight: 64,
            }}>
              <OutcomeBadge outcome={h.prediction_outcome} size="compact" />
              <PLCell pl={h.flat_bet_pl} size="compact" align="center" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CompareRaceCard;
