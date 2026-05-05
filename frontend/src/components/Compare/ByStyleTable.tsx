import React, { useState, useEffect } from 'react';
import { getTrackRecordByStyle } from '../../api/client';
import { TrackRecordByStyle } from '../../types';

/**
 * Stream E4 — per-style track-record table for ComparePage.
 * Hits /wr/predictions/track-record-by-style?days=N and renders
 * one row per specialist style with the same ROI gate as the
 * single-model banner (ROI suppressed when winners_data_completeness
 * < ROI_GATE; "—" displayed instead with hover tooltip).
 */

const WINDOWS = [7, 14, 30, 60, 90];
const ROI_GATE = 0.7;

const STYLE_LABELS: Record<string, string> = {
  general: 'General',
  speed: 'Speed',
  closer: 'Closer',
  class_riser: 'Class Riser',
  class_dropper: 'Class Dropper',
  sprint: 'Sprint',
  route: 'Route',
  gonzo_sauce: 'Gonzo Sauce',
};

const STYLE_ORDER = [
  'general', 'speed', 'closer',
  'class_riser', 'class_dropper',
  'sprint', 'route', 'gonzo_sauce',
];

const ByStyleTable: React.FC<{ storageKey?: string }> = ({ storageKey = 'compare' }) => {
  const [days, setDays] = useState<number>(() => {
    const stored = localStorage.getItem(`tr_window_${storageKey}`);
    return stored ? parseInt(stored, 10) : 30;
  });
  const [data, setData] = useState<TrackRecordByStyle | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    getTrackRecordByStyle(days)
      .then((d) => { if (!cancelled) setData(d); })
      .catch(() => { if (!cancelled) setData(null); })
      .finally(() => { if (!cancelled) setLoading(false); });
    localStorage.setItem(`tr_window_${storageKey}`, String(days));
    return () => { cancelled = true; };
  }, [days, storageKey]);

  if (loading || !data || !data.by_style) {
    return (
      <div style={wrapStyle}>
        <span style={{ color: 'var(--white-dim)', fontSize: '0.75rem' }}>
          {loading ? 'Loading by-style track record…' : 'By-style data unavailable'}
        </span>
      </div>
    );
  }

  // Sort by spec'd order, fall back to alphabetical for unknown styles
  const sortedStyles = [...data.by_style].sort((a, b) => {
    const ai = STYLE_ORDER.indexOf(a.style);
    const bi = STYLE_ORDER.indexOf(b.style);
    if (ai !== -1 && bi !== -1) return ai - bi;
    if (ai !== -1) return -1;
    if (bi !== -1) return 1;
    return a.style.localeCompare(b.style);
  });

  return (
    <div style={wrapStyle}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.7rem', color: 'var(--gold)', letterSpacing: '0.1em' }}>
          BY-STYLE TRACK RECORD
        </span>
        <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
          <span style={labelStyle}>WINDOW</span>
          <select
            value={days}
            onChange={(e) => setDays(parseInt(e.target.value, 10))}
            style={selectStyle}
          >
            {WINDOWS.map((d) => <option key={d} value={d}>{d}d</option>)}
          </select>
        </div>
      </div>
      <div style={{
        display: 'grid',
        gridTemplateColumns: '120px 60px 70px 80px 80px 70px',
        gap: 6,
        padding: '6px 12px',
        fontSize: '0.55rem',
        color: 'var(--white-dim)',
        letterSpacing: '0.1em',
        borderBottom: '1px solid var(--bg-hover)',
      }}>
        <div>STYLE</div>
        <div style={{ textAlign: 'right' }}>N</div>
        <div style={{ textAlign: 'right' }}>SETTLED</div>
        <div style={{ textAlign: 'right' }}>WIN%</div>
        <div style={{ textAlign: 'right' }}>PLACE%</div>
        <div style={{ textAlign: 'right' }}>ROI</div>
      </div>
      {sortedStyles.map((s) => {
        const showROI = (s.winners_data_completeness ?? 0) >= ROI_GATE && s.roi != null;
        const winnersPct = Math.round((s.winners_data_completeness ?? 0) * 100);
        return (
          <div key={s.style} style={{
            display: 'grid',
            gridTemplateColumns: '120px 60px 70px 80px 80px 70px',
            gap: 6,
            padding: '8px 12px',
            borderBottom: '1px solid rgba(255,255,255,0.04)',
            alignItems: 'center',
            fontSize: '0.78rem',
            fontFamily: 'var(--font-mono)',
          }}>
            <div style={{ color: 'var(--white)', fontFamily: 'var(--font-body)' }}>
              {STYLE_LABELS[s.style] ?? s.style}
            </div>
            <div style={{ textAlign: 'right', color: 'var(--white-dim)' }}>{s.n}</div>
            <div style={{ textAlign: 'right', color: s.n_settled === 0 ? 'var(--white-dim)' : 'var(--white)', opacity: s.n_settled === 0 ? 0.5 : 1 }}>
              {s.n_settled}
            </div>
            <div style={{ textAlign: 'right', color: s.hit_rate_win == null ? 'var(--white-dim)' : 'var(--green)' }}>
              {s.hit_rate_win == null ? '—' : `${s.hit_rate_win.toFixed(1)}%`}
            </div>
            <div style={{ textAlign: 'right', color: 'var(--white)' }}>
              {s.hit_rate_place == null ? '—' : `${s.hit_rate_place.toFixed(1)}%`}
            </div>
            <div style={{
              textAlign: 'right',
              color: !showROI ? 'var(--white-dim)' : s.roi! >= 0 ? 'var(--green)' : 'var(--red)',
              opacity: !showROI ? 0.5 : 1,
            }} title={
              !showROI && s.n_settled > 0
                ? `ROI suppressed — only ${winnersPct}% of this style's winners have payouts ingested`
                : undefined
            }>
              {showROI ? `${s.roi! >= 0 ? '+' : ''}${s.roi!.toFixed(1)}%` : '—'}
            </div>
          </div>
        );
      })}
    </div>
  );
};

const wrapStyle: React.CSSProperties = {
  padding: '14px 16px',
  marginBottom: 18,
  backgroundColor: 'var(--bg-card)',
  border: '1px solid var(--bg-hover)',
  borderRadius: 8,
};

const labelStyle: React.CSSProperties = {
  fontFamily: 'var(--font-mono)',
  fontSize: '0.55rem',
  color: 'var(--white-dim)',
  letterSpacing: '0.1em',
};

const selectStyle: React.CSSProperties = {
  backgroundColor: 'var(--bg-secondary)',
  border: '1px solid var(--bg-hover)',
  color: 'var(--white)',
  borderRadius: 4,
  padding: '4px 8px',
  fontFamily: 'var(--font-mono)',
  fontSize: '0.75rem',
  cursor: 'pointer',
};

export default ByStyleTable;
