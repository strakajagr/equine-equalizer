import React, { useState, useEffect } from 'react';
import { getRacesByDate, getAvailableDates } from '../api/client';
import { Race, AvailableDate } from '../types';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import EmptyState from '../components/Common/EmptyState';

const pct = (v: number): string => `${(v * 100).toFixed(1)}%`;
const money = (v: number | null): string => v ? '$' + v.toLocaleString() : '--';
const surfaceLabel = (s: string | null): string => s ? s.charAt(0).toUpperCase() + s.slice(1) : '';
const raceTypeLabel = (t: string | null): string => t ? t.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()) : '';

const HistoryPage: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState('');
  const [availableDates, setAvailableDates] = useState<AvailableDate[]>([]);
  const [races, setRaces] = useState<Race[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getAvailableDates().then(d => setAvailableDates(d.dates || [])).catch(() => {});
  }, []);

  useEffect(() => {
    if (!selectedDate) return;
    setLoading(true);
    getRacesByDate(selectedDate).then(d => setRaces(d.races || [])).catch(() => {}).finally(() => setLoading(false));
  }, [selectedDate]);

  // Compute stats from predictions that have actual results
  const allPreds = races.flatMap(r => r.predictions || []);
  const withResults = allPreds.filter(p => (p as any).was_win !== undefined && (p as any).was_win !== null);
  const raceCount = races.length;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.2rem', color: 'var(--gold)' }}>HISTORY</h2>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <label style={{ fontSize: '0.7rem', color: 'var(--white-dim)', letterSpacing: '0.1em' }}>DATE</label>
          <select
            value={selectedDate}
            onChange={e => setSelectedDate(e.target.value)}
            style={{
              padding: '8px 12px', backgroundColor: 'var(--bg-card)', color: 'var(--white)',
              border: '1px solid var(--gold-dim)', borderRadius: 6, fontFamily: 'var(--font-mono)', fontSize: '0.8rem',
            }}
          >
            <option value="">Select date...</option>
            {availableDates.filter(d => d.has_predictions).map(d => (
              <option key={d.date} value={d.date}>{d.date} ({d.race_count}R)</option>
            ))}
          </select>
        </div>
      </div>

      {/* Stats bar */}
      {races.length > 0 && (
        <div style={{ display: 'flex', gap: 32, marginBottom: 20, padding: '14px 20px', backgroundColor: 'var(--bg-card)', borderRadius: 8 }}>
          <Stat label="Races" value={String(raceCount)} />
          <Stat label="Predictions" value={String(allPreds.length)} />
          <Stat label="With Results" value={String(withResults.length)} />
        </div>
      )}

      {loading ? <LoadingSpinner message="Loading history..." />
        : !selectedDate ? <EmptyState title="Select a Date" subtitle="Choose a date with predictions to view historical race cards" />
        : races.length === 0 ? <EmptyState title="No Data" subtitle="No predictions found for this date" />
        : races.map((r, i) => (
          <div key={r.race_id} className={`stagger-${Math.min(i + 1, 10)}`} style={{ backgroundColor: 'var(--bg-card)', borderRadius: 8, marginBottom: 16, overflow: 'hidden', boxShadow: '0 2px 8px rgba(0,0,0,0.3)' }}>
            <div style={{ padding: '10px 16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--bg-hover)' }}>
              <div style={{ display: 'flex', gap: 12, alignItems: 'baseline' }}>
                <span style={{ fontFamily: 'var(--font-display)', fontSize: '1rem', fontWeight: 700, color: 'var(--gold)' }}>R{r.race_number}</span>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: 'var(--white)' }}>{r.distance_furlongs}f {surfaceLabel(r.surface)}</span>
                <span style={{ fontSize: '0.7rem', color: 'var(--white-dim)' }}>{raceTypeLabel(r.race_type)}</span>
              </div>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: 'var(--gold-dim)' }}>{money(r.purse)} &bull; {r.track_code}</span>
            </div>
            {(r.predictions || []).sort((a, b) => a.predicted_rank - b.predicted_rank).map(p => (
              <div key={p.prediction_id || p.horse_id} style={{ display: 'grid', gridTemplateColumns: '36px 1fr 56px 64px', gap: 8, padding: '8px 16px', borderBottom: '1px solid rgba(255,255,255,0.03)', alignItems: 'center' }}>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.9rem', color: p.is_top_pick ? 'var(--gold)' : 'var(--white-dim)', textAlign: 'center' }}>{p.predicted_rank}</div>
                <div style={{ fontFamily: 'var(--font-display)', fontSize: '0.85rem', color: p.is_top_pick ? 'var(--gold)' : 'var(--white)' }}>{p.horse_name}</div>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', textAlign: 'right', color: p.win_probability >= 0.2 ? 'var(--gold)' : 'var(--white-dim)' }}>{pct(p.win_probability)}</div>
                <div style={{ fontSize: '0.68rem', color: 'var(--white-dim)', textAlign: 'right' }}>{p.top_feature || ''}</div>
              </div>
            ))}
          </div>
        ))}
    </div>
  );
};

const Stat: React.FC<{ label: string; value: string }> = ({ label, value }) => (
  <div style={{ textAlign: 'center' }}>
    <div style={{ fontSize: '0.6rem', color: 'var(--white-dim)', letterSpacing: '0.08em' }}>{label}</div>
    <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.1rem', fontWeight: 600, color: 'var(--gold)' }}>{value}</div>
  </div>
);

export default HistoryPage;
