import React from 'react';
import {
  SpecialistStyle, SPECIALIST_STYLES, STYLE_LABELS,
} from '../../types/predictions';

interface Props {
  value: SpecialistStyle;
  onChange: (s: SpecialistStyle) => void;
}

const StyleSelector: React.FC<Props> = ({ value, onChange }) => (
  <div style={{
    display: 'flex',
    gap: 4,
    flexWrap: 'wrap',
  }}>
    {SPECIALIST_STYLES.map((s) => {
      const active = s === value;
      return (
        <button
          key={s}
          onClick={() => onChange(s)}
          style={{
            background: active ? 'var(--gold-dim)' : 'transparent',
            border: `1px solid ${active ? 'var(--gold)' : 'var(--bg-hover)'}`,
            color: active ? 'var(--gold)' : 'var(--white-dim)',
            fontFamily: 'var(--font-body)',
            fontSize: '0.7rem',
            fontWeight: 500,
            letterSpacing: '0.06em',
            textTransform: 'uppercase',
            padding: '4px 10px',
            borderRadius: 4,
            cursor: 'pointer',
            transition: 'all 0.15s',
          }}
        >
          {STYLE_LABELS[s]}
        </button>
      );
    })}
  </div>
);

export default StyleSelector;
