import React, { useState, useEffect } from 'react';
import { getTrackRecord } from '../../api/client';
import { TrackRecord } from '../../types';

/**
 * Stream E4 — aggregate track-record banner above each prediction page.
 * Smart ROI display: gates on winners_data_completeness >= ROI_GATE.
 * Window choice persisted per-page via storageKey.
 */

interface Props {
  /** Which model's track record to fetch */
  model: 'wr' | 'pl' | 'ls';
  /** localStorage key suffix so each page persists its own window choice */
  storageKey: string;
}

const WINDOWS = [7, 14, 30, 60, 90];
const ROI_GATE = 0.7;

const TrackRecordBanner: React.FC<Props> = ({ model, storageKey }) => {
  const [days, setDays] = useState<number>(() => {
    const stored = localStorage.getItem(`tr_window_${storageKey}`);
    return stored ? parseInt(stored, 10) : 30;
  });
  const [data, setData] = useState<TrackRecord | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    getTrackRecord(model, days)
      .then((d) => { if (!cancelled) setData(d); })
      .catch(() => { if (!cancelled) setData(null); })
      .finally(() => { if (!cancelled) setLoading(false); });
    localStorage.setItem(`tr_window_${storageKey}`, String(days));
    return () => { cancelled = true; };
  }, [model, days, storageKey]);

  if (loading || !data) {
    return (
      <div style={bannerWrapStyle}>
        <span style={{ color: 'var(--white-dim)', fontSize: '0.75rem' }}>
          {loading ? 'Loading track record…' : 'Track record unavailable'}
        </span>
      </div>
    );
  }

  const showROI = (data.winners_data_completeness ?? 0) >= ROI_GATE;
  const winnersCompletenessPct = Math.round((data.winners_data_completeness ?? 0) * 100);
  const dataCompletenessPct = Math.round((data.data_completeness ?? 0) * 100);

  return (
    <div style={bannerWrapStyle}>
      <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
        <span style={labelStyle}>WINDOW</span>
        <select
          value={days}
          onChange={(e) => setDays(parseInt(e.target.value, 10))}
          style={selectStyle}
        >
          {WINDOWS.map((d) => (
            <option key={d} value={d}>{d}d</option>
          ))}
        </select>
      </div>
      <Stat label="PICKS" value={String(data.n_predictions)} />
      <Stat label="SETTLED" value={String(data.n_settled)} />
      <Stat label="PENDING" value={String(data.n_pending)} />
      <Stat label="WIN%"   value={`${data.hit_rate_win.toFixed(1)}%`}   color="var(--green)" />
      <Stat label="PLACE%" value={`${data.hit_rate_place.toFixed(1)}%`} />
      <Stat label="SHOW%"  value={`${data.hit_rate_show.toFixed(1)}%`} />
      {showROI ? (
        <Stat
          label="ROI"
          value={`${data.flat_bet_roi_pct >= 0 ? '+' : ''}${data.flat_bet_roi_pct.toFixed(1)}%`}
          color={data.flat_bet_roi_pct >= 0 ? 'var(--green)' : 'var(--red)'}
        />
      ) : (
        <div
          style={statWrapStyle}
          title={
            `Flat-bet ROI not displayed — only ${winnersCompletenessPct}% of winners ` +
            `have ingested payout data. Hit rates remain reliable.`
          }
        >
          <span style={labelStyle}>ROI</span>
          <span style={{ ...valueStyle, opacity: 0.5, color: 'var(--white-dim)' }}>—</span>
        </div>
      )}
      <div style={{ marginLeft: 'auto', fontSize: '0.6rem', color: 'var(--white-dim)' }}>
        {showROI
          ? `Data: ${dataCompletenessPct}% complete`
          : `Winners payout coverage: ${winnersCompletenessPct}%`}
      </div>
    </div>
  );
};

const Stat: React.FC<{ label: string; value: string; color?: string }> = ({ label, value, color }) => (
  <div style={statWrapStyle}>
    <span style={labelStyle}>{label}</span>
    <span style={{ ...valueStyle, color: color ?? 'var(--white)' }}>{value}</span>
  </div>
);

const bannerWrapStyle: React.CSSProperties = {
  display: 'flex',
  gap: 18,
  alignItems: 'center',
  padding: '10px 16px',
  marginBottom: 18,
  backgroundColor: 'var(--bg-card)',
  border: '1px solid var(--bg-hover)',
  borderRadius: 8,
};

const statWrapStyle: React.CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  gap: 2,
};

const labelStyle: React.CSSProperties = {
  fontFamily: 'var(--font-mono)',
  fontSize: '0.55rem',
  color: 'var(--white-dim)',
  letterSpacing: '0.1em',
};

const valueStyle: React.CSSProperties = {
  fontFamily: 'var(--font-mono)',
  fontSize: '0.92rem',
  fontWeight: 600,
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

export default TrackRecordBanner;
