import React from 'react';
import { NavLink } from 'react-router-dom';
import { format } from 'date-fns';

const isDerbyDay = (): boolean => {
  const today = new Date();
  if (today.getMonth() !== 4) return false; // May
  const day = today.getDate();
  const dow = today.getDay();
  return dow === 6 && day >= 1 && day <= 7;
};

const Header: React.FC = () => {
  const today = new Date();
  const dateStr = format(today, 'EEEE, MMMM d, yyyy');

  return (
    <header style={{
      position: 'sticky',
      top: 0,
      zIndex: 100,
      backgroundColor: 'var(--bg-primary)',
      borderBottom: '1px solid var(--gold-dim)',
      padding: '16px 24px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      backdropFilter: 'blur(12px)',
    }}>
      <div>
        <div style={{
          fontFamily: 'var(--font-display)',
          fontSize: '1.4rem',
          fontWeight: 700,
          color: 'var(--gold)',
          letterSpacing: '0.15em',
          lineHeight: 1.2,
        }}>
          EQUINE EQUALIZER
        </div>
        <div style={{
          fontFamily: 'var(--font-body)',
          fontSize: '0.75rem',
          color: 'var(--white-dim)',
          letterSpacing: '0.08em',
          marginTop: 2,
        }}>
          Precision Handicapping
        </div>
      </div>

      <div style={{
        fontFamily: 'var(--font-mono)',
        fontSize: '0.85rem',
        color: 'var(--gold-dim)',
        animation: isDerbyDay() ? 'goldPulse 3s ease-in-out infinite' : undefined,
      }}>
        {dateStr}
      </div>

      <nav style={{ display: 'flex', gap: 28 }}>
        {[
          { to: '/today', label: 'TODAY' },
          { to: '/value', label: 'VALUE' },
          { to: '/history', label: 'HISTORY' },
        ].map(({ to, label }) => (
          <NavLink
            key={to}
            to={to}
            style={({ isActive }) => ({
              fontFamily: 'var(--font-body)',
              fontSize: '0.8rem',
              fontWeight: 500,
              letterSpacing: '0.12em',
              color: isActive ? 'var(--gold)' : 'var(--white-dim)',
              borderBottom: isActive ? '2px solid var(--gold)' : '2px solid transparent',
              paddingBottom: 4,
              transition: 'color 0.2s, border-color 0.2s',
            })}
          >
            {label}
          </NavLink>
        ))}
      </nav>
    </header>
  );
};

export default Header;
