import React, { useState, useEffect, useMemo } from 'react';
import { getPLValueBets, getAvailableDates } from '../api/client';
import { PLPrediction, AvailableDate } from '../types';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import EmptyState from '../components/Common/EmptyState';
import { OutcomeBadge, PLCell, PL_HEADER_TOOLTIP } from '../components/Common/PredictionOutcome';
import TrackRecordBanner from '../components/Common/TrackRecordBanner';

const fmt = (v: number | null, digits = 1): string =>
  v == null ? '--' : `${(v * 100).toFixed(digits)}%`;
const fmtOdds = (v: number | null): string =>
  v == null ? '--' : `${Math.round(v)}-1`;
const fmtMoney = (v: number | null): string =>
  v == null ? '--' : `$${v.toFixed(0)}`;
const fmtEV = (v: number | null): string =>
  v == null ? '--' : `${v >= 0 ? '+' : ''}$${v.toFixed(2)}`;

const edgeColor = (edge: number | null): string => {
  if (edge == null) return 'var(--white-dim)';
  if (edge >= 0.10) return 'var(--gold)';
  if (edge >= 0.05) return 'var(--green)';
  return 'var(--white-dim)';
};

const edgeLabel = (edge: number | null, isStrong: boolean): string => {
  if (edge == null) return '';
  if (isStrong) return 'STRONG';
  if (edge >= 0.05) return 'VALUE';
  return 'EDGE';
};

const ModelInactiveBanner: React.FC = () => (
  <div style={{
    padding: '28px 24px', textAlign: 'center',
    backgroundColor: 'var(--bg-card)', borderRadius: 8,
    border: '1px solid var(--gold-dim)',
  }}>
    <div style={{ fontFamily: 'var(--font-display)', fontSize: '1.1rem', color: 'var(--gold)', marginBottom: 8 }}>
      P&L Model Not Yet Active
    </div>
    <div style={{ fontSize: '0.82rem', color: 'var(--white-dim)', maxWidth: 480, margin: '0 auto', lineHeight: 1.6 }}>
      Value bet detection requires a trained P&L model. Once the model is trained
      and activated, Kelly-sized overlay bets will appear here, sorted by edge percentage.
    </div>
  </div>
);

const ValuePlaysPage: React.FC = () => {
  const [bets, setBets] = useState<PLPrediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [modelInactive, setModelInactive] = useState(false);
  const [selectedDate, setSelectedDate] = useState('');
  const [availableDates, setAvailableDates] = useState<AvailableDate[]>([]);
  const [trackFilter, setTrackFilter] = useState('ALL');

  useEffect(() => {
    getAvailableDates().then(d => {
      const dates = d.dates || [];
      setAvailableDates(dates);
      const withPreds = dates.find((dd: AvailableDate) => dd.has_predictions);
      const best = withPreds?.date || dates[0]?.date || '';
      if (best) setSelectedDate(best);
    }).catch(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (!selectedDate) return;
    setLoading(true);
    setModelInactive(false);
    getPLValueBets(selectedDate).then(d => {
      const sorted = (d.value_bets || []).sort(
        (a: PLPrediction, b: PLPrediction) =>
          (b.edge_pct || 0) - (a.edge_pct || 0)
      );
      setBets(sorted);
    }).catch(err => {
      // 404 or empty = model not active yet
      setModelInactive(true);
      setBets([]);
    }).finally(() => setLoading(false));
  }, [selectedDate]);

  const tracks = useMemo(() => {
    const s = new Set(bets.map(b => (b as any).track_code || 'UNK'));
    return ['ALL', ...Array.from(s).sort()];
  }, [bets]);

  const filteredBets = useMemo(() =>
    trackFilter === 'ALL' ? bets : bets.filter(b => (b as any).track_code === trackFilter),
  [bets, trackFilter]);

  // Header stats
  const totalBets = filteredBets.length;
  const avgEdge = totalBets > 0
    ? filteredBets.reduce((s, b) => s + (b.edge_pct || 0), 0) / totalBets
    : 0;
  const totalKellyOutlay = filteredBets.reduce((s, b) => s + (b.kelly_bet_size || 0), 0);
  const strongCount = filteredBets.filter(b => b.is_strong_value).length;

  return (
    <div style={{ display: 'flex', gap: 24 }}>
      {/* SIDEBAR */}
      <div style={{ width: 220, flexShrink: 0 }}>
        <div style={{ marginBottom: 20 }}>
          <label style={{ display: 'block', fontSize: '0.65rem', color: 'var(--white-dim)', letterSpacing: '0.1em', marginBottom: 6 }}>DATE</label>
          <select
            value={selectedDate}
            onChange={e => { setSelectedDate(e.target.value); setTrackFilter('ALL'); }}
            style={{ width: '100%', padding: '8px 10px', backgroundColor: 'var(--bg-card)', color: 'var(--white)', border: '1px solid var(--gold-dim)', borderRadius: 6, fontFamily: 'var(--font-mono)', fontSize: '0.78rem', cursor: 'pointer' }}
          >
            {availableDates.slice(0, 50).map(d => (
              <option key={d.date} value={d.date}>{d.date}</option>
            ))}
          </select>
        </div>

        {tracks.length > 1 && (
          <>
            <div style={{ fontSize: '0.65rem', color: 'var(--white-dim)', letterSpacing: '0.1em', marginBottom: 8 }}>TRACKS</div>
            {tracks.map(t => (
              <div
                key={t}
                onClick={() => setTrackFilter(t)}
                style={{
                  padding: '8px 12px', marginBottom: 3, borderRadius: 6, cursor: 'pointer',
                  backgroundColor: trackFilter === t ? 'rgba(201,168,76,0.12)' : 'transparent',
                  borderLeft: trackFilter === t ? '3px solid var(--gold)' : '3px solid transparent',
                  fontSize: '0.82rem', color: trackFilter === t ? 'var(--gold)' : 'var(--white)',
                }}
              >
                {t}
              </div>
            ))}
          </>
        )}

        {/* Stat summary in sidebar */}
        {totalBets > 0 && (
          <div style={{ marginTop: 24, padding: '12px', backgroundColor: 'var(--bg-card)', borderRadius: 8 }}>
            <div style={{ fontSize: '0.6rem', color: 'var(--white-dim)', letterSpacing: '0.08em', marginBottom: 8 }}>TODAY&apos;S BETS</div>
            <div style={{ marginBottom: 6 }}>
              <div style={{ fontSize: '0.58rem', color: 'var(--white-dim)' }}>TOTAL BETS</div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.1rem', fontWeight: 700, color: 'var(--white)' }}>{totalBets}</div>
            </div>
            <div style={{ marginBottom: 6 }}>
              <div style={{ fontSize: '0.58rem', color: 'var(--white-dim)' }}>AVG EDGE</div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1rem', fontWeight: 600, color: 'var(--green)' }}>{fmt(avgEdge)}</div>
            </div>
            <div style={{ marginBottom: 6 }}>
              <div style={{ fontSize: '0.58rem', color: 'var(--white-dim)' }}>KELLY OUTLAY</div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1rem', fontWeight: 600, color: 'var(--gold)' }}>{fmtMoney(totalKellyOutlay)}</div>
            </div>
            {strongCount > 0 && (
              <div>
                <div style={{ fontSize: '0.58rem', color: 'var(--white-dim)' }}>STRONG VALUE</div>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1rem', fontWeight: 600, color: 'var(--gold)' }}>{strongCount}</div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* MAIN */}
      <div style={{ flex: 1, minWidth: 0 }}>
        <TrackRecordBanner model="pl" storageKey="value-plays" />
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 20 }}>
          <div>
            <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.15rem', color: 'var(--gold)', fontWeight: 600, marginBottom: 2 }}>
              VALUE BETS
            </h2>
            <div style={{ fontSize: '0.68rem', color: 'var(--white-dim)' }}>
              P&amp;L Model &mdash; Kelly-Sized Overlays &mdash; Sorted by Edge %
            </div>
          </div>
          {totalBets > 0 && (
            <div style={{ display: 'flex', gap: 20 }}>
              <StatPill label="BETS" value={String(totalBets)} />
              <StatPill label="AVG EDGE" value={fmt(avgEdge)} color="var(--green)" />
              <StatPill label="OUTLAY" value={fmtMoney(totalKellyOutlay)} color="var(--gold)" />
            </div>
          )}
        </div>

        {loading ? (
          <LoadingSpinner message="Loading P&L value bets..." />
        ) : modelInactive ? (
          <ModelInactiveBanner />
        ) : filteredBets.length === 0 ? (
          <EmptyState
            title="No Value Bets Today"
            subtitle="The P&L model found no overlays exceeding the 5% edge threshold for this date."
          />
        ) : (
          <>
            {/* Column headers */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: '34px 70px 1fr 90px 110px 90px 90px 80px 90px 60px 70px',
              gap: 8, padding: '6px 16px',
              fontSize: '0.55rem', color: 'var(--white-dim)', letterSpacing: '0.1em',
              backgroundColor: 'var(--bg-card)', borderRadius: '8px 8px 0 0',
              borderBottom: '1px solid var(--bg-hover)',
            }}>
              <div>PP</div>
              <div>RACE</div>
              <div>HORSE</div>
              <div style={{ textAlign: 'right' }}>WIN %</div>
              <div style={{ textAlign: 'right' }}>EDGE %</div>
              <div style={{ textAlign: 'right' }}>ODDS</div>
              <div style={{ textAlign: 'right' }}>EV / $2</div>
              <div style={{ textAlign: 'right' }}>KELLY</div>
              <div style={{ textAlign: 'right' }}>BET SIZE</div>
              <div style={{ textAlign: 'center' }}>RESULT</div>
              <div style={{ textAlign: 'right' }} title={PL_HEADER_TOOLTIP}>P/L</div>
            </div>

            <div style={{ backgroundColor: 'var(--bg-card)', borderRadius: '0 0 8px 8px', overflow: 'hidden' }}>
              {filteredBets.map((b, idx) => (
                <ValueBetRow key={b.prediction_id || `${b.horse_id}-${idx}`} b={b} />
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

const ValueBetRow: React.FC<{ b: PLPrediction }> = ({ b }) => {
  const isStrong = b.is_strong_value;
  const edge = b.edge_pct;
  const color = edgeColor(edge);
  const label = edgeLabel(edge, isStrong);
  const topFactors = Object.entries(b.feature_importance || {})
    .sort((a, z) => Math.abs(z[1]) - Math.abs(a[1]))
    .slice(0, 3)
    .map(([k]) => k.replace(/_/g, ' '));

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: '34px 70px 1fr 90px 110px 90px 90px 80px 90px 60px 70px',
      gap: 8, padding: '12px 16px',
      borderLeft: isStrong
        ? '3px solid var(--gold)'
        : '3px solid var(--green)',
      borderBottom: '1px solid rgba(255,255,255,0.04)',
      alignItems: 'center',
      transition: 'background-color 0.12s',
    }}
      onMouseEnter={e => { e.currentTarget.style.backgroundColor = 'var(--bg-hover)'; }}
      onMouseLeave={e => { e.currentTarget.style.backgroundColor = 'transparent'; }}
    >
      {/* PP */}
      <div style={{
        width: 26, height: 26, borderRadius: '50%',
        border: '1px solid var(--white-dim)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--white-dim)',
      }}>{b.post_position}</div>

      {/* Track + race */}
      <div style={{
        fontFamily: 'var(--font-mono)', fontSize: '0.7rem', color: 'var(--gold-dim)',
      }}>
        {(b as any).track_code || '—'} R{(b as any).race_number ?? '?'}
      </div>

      {/* Horse info */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 2 }}>
          <span style={{ fontFamily: 'var(--font-display)', fontSize: '0.92rem', fontWeight: 700, color: 'var(--white)' }}>
            {b.horse_name}
          </span>
          {isStrong && (
            <span style={{ fontSize: '0.5rem', padding: '1px 5px', borderRadius: 4, backgroundColor: 'rgba(201,168,76,0.25)', color: 'var(--gold)', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
              STRONG
            </span>
          )}
          {b.lasix_first_time && (
            <span style={{ fontSize: '0.5rem', padding: '1px 4px', borderRadius: 4, backgroundColor: 'rgba(201,168,76,0.15)', color: 'var(--gold-light)', fontFamily: 'var(--font-mono)' }}>1stL</span>
          )}
        </div>
        <div style={{ fontSize: '0.65rem', color: 'var(--white-dim)' }}>
          {b.jockey_name || 'TBD'} / {b.trainer_name}
        </div>
        {topFactors.length > 0 && (
          <div style={{ fontSize: '0.58rem', color: 'var(--white-dim)', opacity: 0.6, marginTop: 2, fontStyle: 'italic' }}>
            {topFactors.join(' · ')}
          </div>
        )}
      </div>

      {/* Win % */}
      <div style={{ textAlign: 'right', fontFamily: 'var(--font-mono)', fontSize: '0.88rem', color: 'var(--gold)' }}>
        {fmt(b.win_probability)}
      </div>

      {/* Edge % */}
      <div style={{ textAlign: 'right' }}>
        <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.1rem', fontWeight: 700, color }}>
          {edge != null ? `+${(edge * 100).toFixed(1)}%` : '--'}
        </div>
        <div style={{ fontSize: '0.52rem', color, opacity: 0.8, fontFamily: 'var(--font-mono)' }}>{label}</div>
      </div>

      {/* Odds */}
      <div style={{ textAlign: 'right', fontFamily: 'var(--font-mono)', fontSize: '0.82rem', color: 'var(--white-dim)' }}>
        {fmtOdds(b.closing_odds || b.morning_line_odds)}
      </div>

      {/* EV */}
      <div style={{
        textAlign: 'right', fontFamily: 'var(--font-mono)', fontSize: '0.82rem',
        color: b.predicted_ev != null && b.predicted_ev > 0 ? 'var(--green)' : 'var(--white-dim)',
      }}>
        {fmtEV(b.predicted_ev)}
      </div>

      {/* Kelly fraction */}
      <div style={{ textAlign: 'right', fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: 'var(--white-dim)' }}>
        {b.kelly_fraction != null ? `${(b.kelly_fraction * 100).toFixed(1)}%` : '--'}
      </div>

      {/* Kelly bet size */}
      <div style={{ textAlign: 'right', fontFamily: 'var(--font-mono)', fontSize: '0.9rem', fontWeight: 600, color: 'var(--white)' }}>
        {fmtMoney(b.kelly_bet_size)}
      </div>

      {/* Result */}
      <div style={{ textAlign: 'center' }}>
        <OutcomeBadge outcome={b.prediction_outcome} size="compact" />
      </div>

      {/* P/L */}
      <div style={{ textAlign: 'right' }}>
        <PLCell pl={b.flat_bet_pl} size="compact" />
      </div>
    </div>
  );
};

const StatPill: React.FC<{ label: string; value: string; color?: string }> = ({ label, value, color }) => (
  <div style={{ textAlign: 'right' }}>
    <div style={{ fontSize: '0.55rem', color: 'var(--white-dim)', letterSpacing: '0.08em' }}>{label}</div>
    <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.95rem', fontWeight: 600, color: color || 'var(--white)' }}>{value}</div>
  </div>
);

export default ValuePlaysPage;
