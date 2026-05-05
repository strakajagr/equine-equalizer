import React, { useEffect, useState, useCallback } from 'react';
import { getWRRacesByDate, getAvailableDates, getHorsePPs, runWRPredictions, getPLPredictionsByDate, runPLPredictions, getPLValueBets } from '../api/client';
import { Race, Track, Prediction, AvailableDate, HorsePPsResponse } from '../types';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import EmptyState from '../components/Common/EmptyState';
import { OutcomeBadge, PLCell, PL_HEADER_TOOLTIP } from '../components/Common/PredictionOutcome';
import TrackRecordBanner from '../components/Common/TrackRecordBanner';

const pct = (v: number): string => `${(v * 100).toFixed(1)}%`;
const money = (v: number | null): string => {
  if (!v) return '--';
  return '$' + v.toLocaleString();
};
const surfaceLabel = (s: string | null): string => {
  if (!s) return '';
  return s.charAt(0).toUpperCase() + s.slice(1);
};
const raceTypeLabel = (t: string | null): string => {
  if (!t) return '';
  return t.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
};

interface TodayPageProps {
  specialistStyle?: string;  // Phase A3 — 'gonzo_sauce' or 'general' (default).
                             // Named to avoid collision with JSX `style` prop.
}

const TodayPage: React.FC<TodayPageProps> = ({
  specialistStyle = 'general',
}) => {
  const [races, setRaces] = useState<Race[]>([]);
  const [tracks, setTracks] = useState<Track[]>([]);
  const [selectedTrack, setSelectedTrack] = useState<string | null>(null);
  const [selectedDate, setSelectedDate] = useState('');
  const [availableDates, setAvailableDates] = useState<AvailableDate[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedModel, setSelectedModel] = useState<'wr' | 'pl' | 'ranker' | 'value'>('wr');
  const [drawerHorse, setDrawerHorse] = useState<Prediction | null>(null);
  const [horsePPs, setHorsePPs] = useState<HorsePPsResponse | null>(null);
  const [ppLoading, setPPLoading] = useState(false);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getAvailableDates();
        setAvailableDates(data.dates || []);
        const withPreds = (data.dates || []).find((d: AvailableDate) => d.has_predictions);
        const bestDate = withPreds?.date || data.dates?.[0]?.date || '';
        if (bestDate) setSelectedDate(bestDate);
      } catch {
        setError('Failed to load available dates');
        setLoading(false);
      }
    };
    load();
  }, []);

  useEffect(() => {
    if (!selectedDate) return;
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        // All views use WR data (which now includes rank_score + edge from Layers 2-3)
        // style: 'general' (default) | 'gonzo_sauce' (Phase A3)
        const wrData = await getWRRacesByDate(selectedDate, specialistStyle);
        let racesData = wrData.races || [];
        const tracksData = wrData.tracks || [];

        // Sort/filter based on selected view
        if (selectedModel === 'ranker') {
          // Sort by confidence_score (rank_score stored there) descending
          racesData = racesData.map((race: Race) => ({
            ...race,
            predictions: [...race.predictions].sort(
              (a: Prediction, b: Prediction) =>
                (b.confidence_score || 0) - (a.confidence_score || 0)
            ).map((p: Prediction, i: number) => ({
              ...p, predicted_rank: i + 1, is_top_pick: i === 0,
            })),
          }));
        } else if (selectedModel === 'value') {
          // PL's is_value_bet is the canonical value signal (Kelly + edge).
          // WR's is_value_flag is currently always false (Bug #27 deferred);
          // cross-reference PL value_bets by (race_id, program_number).
          let plKeys = new Set<string>();
          try {
            const plData = await getPLValueBets(selectedDate);
            plKeys = new Set(
              (plData.value_bets || []).map(
                (b: any) => `${b.race_id}::${b.program_number}`
              )
            );
          } catch { /* leave plKeys empty → empty state */ }
          racesData = racesData.map((race: Race) => ({
            ...race,
            predictions: [...race.predictions]
              .filter((p: Prediction) =>
                plKeys.has(`${race.race_id}::${p.program_number}`)
              )
              .sort((a: Prediction, b: Prediction) =>
                (b.overlay_pct || 0) - (a.overlay_pct || 0)
              ),
          })).filter((r: Race) => r.predictions.length > 0);
        }

        setRaces(racesData);
        setTracks(tracksData);
        if (tracksData.length > 0 && !selectedTrack) {
          setSelectedTrack(tracksData[0].track_code);
        }
      } catch {
        setError('Failed to load races');
      }
      setLoading(false);
    };
    load();
  }, [selectedDate, selectedModel, specialistStyle]); // eslint-disable-line react-hooks/exhaustive-deps

  const handleGenerate = useCallback(async () => {
    if (!selectedDate || generating) return;
    setGenerating(true);
    try {
      if (selectedModel === 'pl') {
        await runPLPredictions(selectedDate);
      } else {
        await runWRPredictions(selectedDate);
      }
      // Trigger reload via selectedDate/selectedModel dep
      setSelectedDate(d => d); // force re-render
      const data = await getWRRacesByDate(selectedDate);
      setRaces(data.races || []);
      setTracks(data.tracks || []);
      if (data.tracks?.length > 0) setSelectedTrack(data.tracks[0].track_code);
    } catch {
      setError('Failed to generate predictions');
    }
    setGenerating(false);
  }, [selectedDate, generating, selectedModel]);

  const openDrawer = useCallback(async (pred: Prediction) => {
    setDrawerHorse(pred);
    setPPLoading(true);
    setHorsePPs(null);
    try {
      const data = await getHorsePPs(pred.horse_id);
      setHorsePPs(data);
    } catch { /* silent */ }
    setPPLoading(false);
  }, []);

  const filteredRaces = selectedTrack
    ? races.filter(r => r.track_code === selectedTrack)
    : races;

  const dateInfo = availableDates.find(d => d.date === selectedDate);

  return (
    <div style={{ display: 'flex', gap: 24 }}>
      {/* SIDEBAR */}
      <div style={{ width: 220, flexShrink: 0 }}>
        <div style={{ marginBottom: 20 }}>
          <label style={{ display: 'block', fontSize: '0.65rem', color: 'var(--white-dim)', letterSpacing: '0.1em', marginBottom: 6 }}>RACE DATE</label>
          <select
            value={selectedDate}
            onChange={e => { setSelectedDate(e.target.value); setSelectedTrack(null); }}
            style={{
              width: '100%', padding: '8px 10px', backgroundColor: 'var(--bg-card)',
              color: 'var(--white)', border: '1px solid var(--gold-dim)', borderRadius: 6,
              fontFamily: 'var(--font-mono)', fontSize: '0.78rem', cursor: 'pointer',
            }}
          >
            {availableDates.slice(0, 50).map(d => (
              <option key={d.date} value={d.date}>
                {d.date} ({d.race_count}R{d.has_predictions ? ' *' : ''})
              </option>
            ))}
          </select>
        </div>

        <div style={{ marginBottom: 20 }}>
          <label style={{ display: 'block', fontSize: '0.65rem', color: 'var(--white-dim)', letterSpacing: '0.1em', marginBottom: 6 }}>VIEW</label>
          <div style={{ display: 'flex', gap: 0, borderRadius: 6, overflow: 'hidden', border: '1px solid var(--gold-dim)' }}>
            {([['wr', 'WIN PROB'], ['ranker', 'RANKER'], ['value', 'VALUE']] as const).map(([m, label]) => (
              <button
                key={m}
                onClick={() => setSelectedModel(m)}
                style={{
                  flex: 1, padding: '8px 0', border: 'none', cursor: 'pointer',
                  fontFamily: 'var(--font-mono)', fontSize: '0.62rem', fontWeight: 600,
                  letterSpacing: '0.03em',
                  backgroundColor: selectedModel === m ? 'var(--gold)' : 'var(--bg-card)',
                  color: selectedModel === m ? '#0a0a0f' : 'var(--white-dim)',
                  transition: 'all 0.15s',
                }}
              >
                {label}
              </button>
            ))}
          </div>
          <div style={{ fontSize: '0.58rem', color: 'var(--white-dim)', marginTop: 4, fontStyle: 'italic' }}>
            {selectedModel === 'wr' ? 'Layer 1: Who will win?' : selectedModel === 'ranker' ? 'Layer 2: Finish order (exactas/tris)' : 'Layer 3: Value overlay (edge + Kelly)'}
          </div>
        </div>

        {dateInfo && !dateInfo.has_predictions && !loading && (
          <button
            onClick={handleGenerate}
            disabled={generating}
            style={{
              width: '100%', padding: '10px', marginBottom: 16,
              backgroundColor: generating ? 'var(--bg-hover)' : 'var(--gold)',
              color: generating ? 'var(--white-dim)' : '#0a0a0f',
              border: 'none', borderRadius: 6, cursor: generating ? 'wait' : 'pointer',
              fontFamily: 'var(--font-body)', fontWeight: 600, fontSize: '0.78rem', letterSpacing: '0.05em',
            }}
          >
            {generating ? 'GENERATING...' : 'RUN MODEL'}
          </button>
        )}

        <div style={{ fontSize: '0.65rem', color: 'var(--white-dim)', letterSpacing: '0.1em', marginBottom: 8 }}>TRACKS</div>
        <TrackItem label="All Tracks" count={races.length} active={!selectedTrack} onClick={() => setSelectedTrack(null)} />
        {tracks.map(t => (
          <TrackItem key={t.track_code} label={t.track_code} subtitle={t.track_name} count={t.race_count} active={selectedTrack === t.track_code} onClick={() => setSelectedTrack(t.track_code)} />
        ))}
      </div>

      {/* MAIN */}
      <div style={{ flex: 1, minWidth: 0 }}>
        <TrackRecordBanner model="wr" storageKey="today" />
        {loading ? <LoadingSpinner message="Loading race card..." />
          : error ? <EmptyState title="Error" subtitle={error} />
          : filteredRaces.length === 0 ? (
            <EmptyState
              title="No Predictions"
              subtitle={dateInfo && !dateInfo.has_predictions ? 'Click RUN MODEL to generate predictions' : 'No qualifying races found'}
            />
          ) : (
            <>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 16 }}>
                <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.15rem', color: 'var(--gold)', fontWeight: 600 }}>
                  {selectedDate} &mdash; {filteredRaces.length} Race{filteredRaces.length !== 1 ? 's' : ''}
                  <span style={{ fontSize: '0.65rem', marginLeft: 10, padding: '2px 8px', borderRadius: 4, backgroundColor: selectedModel === 'value' ? 'rgba(34,197,94,0.2)' : selectedModel === 'ranker' ? 'rgba(59,130,246,0.2)' : 'rgba(201,168,76,0.2)', color: selectedModel === 'value' ? 'var(--green)' : selectedModel === 'ranker' ? '#93c5fd' : 'var(--gold-light)', fontFamily: 'var(--font-mono)', verticalAlign: 'middle' }}>
                    {selectedModel === 'wr' ? 'WIN PROB' : selectedModel === 'ranker' ? 'RANKER' : 'VALUE'}
                  </span>
                </h2>
              </div>
              {filteredRaces.map((race, idx) => (
                <RaceCard key={race.race_id} race={race} idx={idx} onHorseClick={openDrawer} />
              ))}
            </>
          )}
      </div>

      {drawerHorse && (
        <HorseDrawer prediction={drawerHorse} horsePPs={horsePPs} loading={ppLoading} onClose={() => { setDrawerHorse(null); setHorsePPs(null); }} />
      )}
    </div>
  );
};

/* ─── Track Sidebar Item ─── */
const TrackItem: React.FC<{ label: string; subtitle?: string; count: number; active: boolean; onClick: () => void }> = ({ label, subtitle, count, active, onClick }) => (
  <div onClick={onClick} style={{
    padding: '10px 12px', marginBottom: 4, borderRadius: 6, cursor: 'pointer',
    backgroundColor: active ? 'rgba(201,168,76,0.12)' : 'transparent',
    borderLeft: active ? '3px solid var(--gold)' : '3px solid transparent',
    display: 'flex', justifyContent: 'space-between', alignItems: 'center', transition: 'background-color 0.15s',
  }}>
    <div>
      <div style={{ fontFamily: 'var(--font-body)', fontSize: '0.85rem', fontWeight: 500, color: active ? 'var(--gold)' : 'var(--white)' }}>{label}</div>
      {subtitle && <div style={{ fontSize: '0.62rem', color: 'var(--white-dim)' }}>{subtitle}</div>}
    </div>
    <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.72rem', color: 'var(--white-dim)', backgroundColor: 'var(--bg-hover)', padding: '2px 8px', borderRadius: 10 }}>{count}</span>
  </div>
);

/* ─── Race Card ─── */
const RaceCard: React.FC<{ race: Race; idx: number; onHorseClick: (p: Prediction) => void }> = ({ race: r, idx, onHorseClick }) => {
  const preds = r.predictions || [];
  const hasResults = preds.some(p => p.prediction_outcome && p.prediction_outcome !== 'pending');
  const exactaHit = preds.some(p => p.exacta_hit === true);
  const trifectaHit = preds.some(p => p.trifecta_hit === true);
  const top1 = preds.find(p => p.predicted_rank === 1);
  const top1Won = top1?.prediction_outcome === 'win';
  return (
  <div className={`stagger-${Math.min(idx + 1, 10)}`} style={{ backgroundColor: 'var(--bg-card)', borderRadius: 8, marginBottom: 20, overflow: 'hidden', boxShadow: '0 2px 8px rgba(0,0,0,0.3)' }}>
    <div style={{ padding: '12px 18px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--bg-hover)' }}>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 12 }}>
        <span style={{ fontFamily: 'var(--font-display)', fontSize: '1.05rem', fontWeight: 700, color: 'var(--gold)' }}>R{r.race_number}</span>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: 'var(--white)' }}>{r.distance_furlongs}f {surfaceLabel(r.surface)}</span>
        <span style={{ fontSize: '0.72rem', color: 'var(--white-dim)' }}>{raceTypeLabel(r.race_type)}</span>
        {r.grade && <span style={{ fontSize: '0.62rem', padding: '2px 7px', borderRadius: 8, backgroundColor: 'rgba(201,168,76,0.2)', color: 'var(--gold-light)', fontFamily: 'var(--font-mono)' }}>G{r.grade}</span>}
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        {hasResults && exactaHit && <span style={{ fontSize: '0.58rem', padding: '2px 7px', borderRadius: 6, backgroundColor: 'rgba(34,197,94,0.2)', color: 'var(--green)', fontFamily: 'var(--font-mono)' }}>EXACTA HIT</span>}
        {hasResults && trifectaHit && <span style={{ fontSize: '0.58rem', padding: '2px 7px', borderRadius: 6, backgroundColor: 'rgba(34,197,94,0.2)', color: 'var(--green)', fontFamily: 'var(--font-mono)' }}>TRIFECTA HIT</span>}
        {hasResults && top1Won && <span style={{ fontSize: '0.58rem', padding: '2px 7px', borderRadius: 6, backgroundColor: 'rgba(201,168,76,0.2)', color: 'var(--gold-light)', fontFamily: 'var(--font-mono)' }}>#1 WON</span>}
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: 'var(--gold-dim)' }}>{money(r.purse)}</span>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.68rem', color: 'var(--white-dim)' }}>{r.track_code}</span>
      </div>
    </div>
    <div style={{ display: 'grid', gridTemplateColumns: '40px 34px 1fr 125px 60px 70px 74px 60px 70px 1fr', gap: 6, padding: '7px 18px', fontSize: '0.58rem', color: 'var(--white-dim)', letterSpacing: '0.1em', borderBottom: '1px solid var(--bg-secondary)' }}>
      <div style={{ textAlign: 'center' }}>RNK</div>
      <div style={{ textAlign: 'center' }}>PP</div>
      <div>HORSE</div>
      <div>CONNECTIONS</div>
      <div style={{ textAlign: 'right' }}>WIN%</div>
      <div style={{ textAlign: 'right' }}>ML</div>
      <div style={{ textAlign: 'right' }} title="Green VALUE = model likes more than odds. Red FADE = model likes less than odds.">EDGE</div>
      <div style={{ textAlign: 'center' }}>RESULT</div>
      <div style={{ textAlign: 'right' }} title={PL_HEADER_TOOLTIP}>P/L</div>
      <div>TOP FACTOR</div>
    </div>
    {(r.predictions || []).sort((a, b) => a.predicted_rank - b.predicted_rank).map(p => (
      <HorseRowInline key={p.prediction_id || p.horse_id} p={p} hasResults={hasResults} onClick={() => onHorseClick(p)} />
    ))}
  </div>
  );
};

/* ─── Horse Row ─── */
const HorseRowInline: React.FC<{ p: Prediction; hasResults?: boolean; onClick: () => void }> = ({ p, hasResults, onClick }) => {
  const isTop = p.is_top_pick;
  const isValue = p.is_value_flag;
  return (
    <div onClick={onClick} style={{
      display: 'grid', gridTemplateColumns: '40px 34px 1fr 125px 60px 70px 74px 60px 70px 1fr',
      alignItems: 'center', gap: 6, padding: '9px 18px',
      backgroundColor: isTop ? 'rgba(201,168,76,0.05)' : 'transparent',
      borderLeft: isTop ? '3px solid var(--gold)' : isValue ? '3px solid var(--green)' : '3px solid transparent',
      borderBottom: '1px solid rgba(255,255,255,0.03)', cursor: 'pointer', transition: 'background-color 0.15s',
    }} onMouseEnter={e => { e.currentTarget.style.backgroundColor = 'var(--bg-hover)'; }} onMouseLeave={e => { e.currentTarget.style.backgroundColor = isTop ? 'rgba(201,168,76,0.05)' : 'transparent'; }}>
      <div style={{ fontFamily: 'var(--font-mono)', fontSize: isTop ? '1.2rem' : '0.95rem', fontWeight: 600, color: isTop ? 'var(--gold)' : 'var(--white-dim)', textAlign: 'center' }}>{p.predicted_rank}</div>
      <div style={{ width: 24, height: 24, borderRadius: '50%', border: '1px solid var(--white-dim)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--white-dim)' }}>{p.post_position}</div>
      <div>
        <span style={{ fontFamily: 'var(--font-display)', fontSize: '0.88rem', fontWeight: isTop ? 700 : 400, color: isTop ? 'var(--gold)' : 'var(--white)' }}>{p.horse_name}</span>
        {p.lasix_first_time && <span style={{ fontSize: '0.52rem', marginLeft: 5, color: 'var(--gold-light)', fontFamily: 'var(--font-mono)' }}>1stL</span>}
        {p.blinkers_first_time && <span style={{ fontSize: '0.52rem', marginLeft: 3, color: 'var(--blue)', fontFamily: 'var(--font-mono)' }}>BL</span>}
        {(p as any).has_workout_data && <span style={{ fontSize: '0.48rem', marginLeft: 4, padding: '1px 3px', borderRadius: 3, backgroundColor: 'rgba(168,85,247,0.2)', color: '#c084fc', fontFamily: 'var(--font-mono)' }}>W</span>}
        {(p as any).longshot_alert && <span style={{ fontSize: '0.48rem', marginLeft: 4, padding: '1px 3px', borderRadius: 3, backgroundColor: 'rgba(239,68,68,0.2)', color: '#f87171', fontFamily: 'var(--font-mono)' }}>LS</span>}
        {isValue && <span style={{ fontSize: '0.52rem', marginLeft: 5, padding: '1px 4px', borderRadius: 5, backgroundColor: 'rgba(34,197,94,0.2)', color: 'var(--green)', fontFamily: 'var(--font-mono)' }}>VALUE</span>}
      </div>
      <div style={{ lineHeight: 1.3 }}>
        <div style={{ fontSize: '0.68rem', color: 'var(--white-dim)' }}>{p.jockey_name || 'TBD'}</div>
        <div style={{ fontSize: '0.62rem', color: 'var(--white-dim)', opacity: 0.6 }}>{p.trainer_name}</div>
      </div>
      <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem', fontWeight: 500, textAlign: 'right', color: p.win_probability >= 0.25 ? 'var(--gold)' : p.win_probability >= 0.15 ? 'var(--white)' : 'var(--white-dim)' }}>{pct(p.win_probability)}</div>
      <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', textAlign: 'right', color: 'var(--white-dim)' }}>{p.morning_line_odds ? `${Math.round(p.morning_line_odds)}-1` : '--'}</div>
      <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', textAlign: 'right', fontWeight: isValue ? 600 : 400, color: p.overlay_pct == null ? 'var(--white-dim)' : p.overlay_pct > 0 ? 'var(--green)' : 'var(--red)' }}>
        {p.overlay_pct != null ? <>{p.overlay_pct > 0 ? '+' : ''}{(p.overlay_pct * 100).toFixed(1)}% <span style={{ fontSize: '0.5rem', opacity: 0.8 }}>{p.overlay_pct >= 0.15 ? 'VALUE' : p.overlay_pct > 0 ? 'edge' : 'FADE'}</span></> : '--'}
      </div>
      <div style={{ textAlign: 'center' }}>
        <OutcomeBadge outcome={p.prediction_outcome} size="compact" />
      </div>
      <div style={{ textAlign: 'right' }}>
        <PLCell pl={p.flat_bet_pl} size="compact" />
      </div>
      <div style={{ fontSize: '0.68rem', color: 'var(--white-dim)', fontStyle: 'italic', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{p.top_feature || ''}</div>
    </div>
  );
};

/* ─── Horse Drawer ─── */
const HorseDrawer: React.FC<{ prediction: Prediction; horsePPs: HorsePPsResponse | null; loading: boolean; onClose: () => void }> = ({ prediction: p, horsePPs, loading, onClose }) => (
  <>
    <div onClick={onClose} style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.65)', zIndex: 200 }} />
    <div style={{
      position: 'fixed',
      top: '50%', left: '50%',
      transform: 'translate(-50%, -50%)',
      width: '90%',
      maxWidth: 720,
      maxHeight: '90vh',
      overflowY: 'auto',
      backgroundColor: 'var(--bg-primary)',
      border: '1px solid var(--gold-dim)',
      borderRadius: 8,
      boxShadow: '0 12px 48px rgba(0,0,0,0.6)',
      zIndex: 201,
      animation: 'modalIn 0.2s ease-out',
    }}>
      <style>{`@keyframes modalIn { from { opacity: 0; transform: translate(-50%, -48%) scale(0.97); } to { opacity: 1; transform: translate(-50%, -50%) scale(1); } }`}</style>
      <div style={{ padding: '20px 24px', borderBottom: '1px solid var(--gold-dim)', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <div style={{ fontFamily: 'var(--font-display)', fontSize: '1.4rem', fontWeight: 700, color: 'var(--gold)' }}>{p.horse_name}</div>
          <div style={{ fontSize: '0.78rem', color: 'var(--white-dim)', marginTop: 4 }}>
            {horsePPs?.sex || p.sex || ''}{(horsePPs?.sire || p.sire) ? ` \u2022 by ${horsePPs?.sire || p.sire}` : ''}{horsePPs?.dam ? ` out of ${horsePPs.dam}` : ''}{horsePPs?.dam_sire ? ` (${horsePPs.dam_sire})` : ''}
          </div>
          <div style={{ fontSize: '0.72rem', color: 'var(--white-dim)', marginTop: 2 }}>J: {p.jockey_name || 'TBD'} &bull; T: {p.trainer_name}</div>
        </div>
        <button onClick={onClose} style={{ background: 'none', border: '1px solid var(--white-dim)', borderRadius: 4, color: 'var(--white-dim)', padding: '4px 10px', cursor: 'pointer', fontSize: '0.8rem' }}>X</button>
      </div>
      <div style={{ padding: '14px 24px', display: 'flex', gap: 20, borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
        <SB label="Win%" value={pct(p.win_probability)} gold />
        <SB label="Rank" value={`#${p.predicted_rank}`} />
        <SB label="ML" value={p.morning_line_odds ? `${Math.round(p.morning_line_odds)}-1` : '--'} />
        {p.overlay_pct != null && <SB label="Overlay" value={`${(p.overlay_pct * 100).toFixed(1)}%`} green={p.overlay_pct > 0} />}
        {horsePPs?.best_speed_figure != null && <SB label="Best Fig" value={String(horsePPs.best_speed_figure)} />}
      </div>
      {horsePPs && horsePPs.speed_figures.length > 1 && (
        <div style={{ padding: '12px 24px', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
          <div style={{ fontSize: '0.62rem', color: 'var(--white-dim)', letterSpacing: '0.1em', marginBottom: 6 }}>SPEED FIGURES</div>
          <Spark values={horsePPs.speed_figures.slice().reverse()} />
        </div>
      )}
      <div style={{ padding: '16px 24px' }}>
        <div style={{ fontSize: '0.62rem', color: 'var(--white-dim)', letterSpacing: '0.1em', marginBottom: 10 }}>PAST PERFORMANCES</div>
        {loading ? <LoadingSpinner message="Loading PPs..." /> : !horsePPs || horsePPs.past_performances.length === 0 ? (
          <div style={{ fontSize: '0.78rem', color: 'var(--white-dim)', padding: 20, textAlign: 'center' }}>No past performances</div>
        ) : (
          <div style={{ fontSize: '0.68rem', overflowX: 'auto' }}>
            {/* PP Header */}
            <div style={{ display: 'grid', gridTemplateColumns: '72px 32px 44px 36px 30px 34px 38px 38px 60px 28px 1fr', gap: 4, padding: '5px 0', color: 'var(--white-dim)', fontSize: '0.52rem', letterSpacing: '0.06em', borderBottom: '1px solid var(--bg-hover)', minWidth: 480 }}>
              <div>DATE</div><div>TRK</div><div>DIST</div><div>SRF</div><div>FIN</div><div>LB</div><div>FIG</div><div>ODDS</div><div>JOCKEY</div><div>MDL</div><div>RUNNING</div>
            </div>
            {horsePPs.past_performances.map((pp: any, i: number) => {
              const fin = pp.official_finish;
              const finColor = fin === 1 ? 'var(--gold)' : fin != null && fin <= 3 ? 'var(--green)' : 'var(--white-dim)';
              const runLine = [pp.call_1_position, pp.call_2_position, pp.stretch_position, fin].filter((v: any) => v != null).join('-');
              return (
                <div key={i} style={{ display: 'grid', gridTemplateColumns: '72px 32px 44px 36px 30px 34px 38px 38px 60px 28px 1fr', gap: 4, padding: '4px 0', borderBottom: '1px solid rgba(255,255,255,0.03)', fontFamily: 'var(--font-mono)', fontSize: '0.65rem', minWidth: 480 }}>
                  <div style={{ color: 'var(--white-dim)' }}>{pp.race_date || '--'}</div>
                  <div style={{ color: 'var(--white)' }}>{pp.track_code}</div>
                  <div>{pp.distance_furlongs}f</div>
                  <div style={{ color: 'var(--white-dim)' }}>{pp.surface || '--'}</div>
                  <div style={{ color: finColor, fontWeight: fin === 1 ? 600 : 400 }}>{fin === 'SCR' ? 'SCR' : fin || '--'}</div>
                  <div style={{ color: 'var(--white-dim)' }}>{pp.lengths_behind != null ? Number(pp.lengths_behind).toFixed(1) : '--'}</div>
                  <div style={{ color: pp.beyer_speed_figure ? 'var(--white)' : 'var(--white-dim)' }}>{pp.beyer_speed_figure || '--'}</div>
                  <div style={{ color: 'var(--white-dim)' }}>{pp.closing_odds != null ? Number(pp.closing_odds).toFixed(1) : '--'}</div>
                  <div style={{ color: 'var(--white-dim)', fontSize: '0.58rem', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{pp.jockey_name?.split(',')[0] || '--'}</div>
                  <div style={{ color: pp.model_rank ? 'var(--gold)' : 'var(--white-dim)', fontSize: '0.58rem' }}>{pp.model_rank ? `#${pp.model_rank}` : ''}</div>
                  <div style={{ color: 'var(--white-dim)', fontSize: '0.58rem' }}>
                    {runLine || '--'}
                    {pp.lasix && <span style={{ marginLeft: 3, color: 'var(--gold-light)', fontSize: '0.48rem' }}>L</span>}
                    {pp.blinkers_on && <span style={{ marginLeft: 2, color: 'var(--blue)', fontSize: '0.48rem' }}>B</span>}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  </>
);

const SB: React.FC<{ label: string; value: string; gold?: boolean; green?: boolean }> = ({ label, value, gold, green }) => (
  <div style={{ textAlign: 'center' }}>
    <div style={{ fontSize: '0.58rem', color: 'var(--white-dim)', letterSpacing: '0.08em', marginBottom: 2 }}>{label}</div>
    <div style={{ fontFamily: 'var(--font-mono)', fontSize: gold ? '1.15rem' : '0.9rem', fontWeight: 600, color: green ? 'var(--green)' : gold ? 'var(--gold)' : 'var(--white)' }}>{value}</div>
  </div>
);

const Spark: React.FC<{ values: number[] }> = ({ values }) => {
  if (values.length < 2) return null;
  const mn = Math.min(...values) - 5, mx = Math.max(...values) + 5;
  const w = 450, h = 44;
  const pts = values.map((v, i) => `${(i / (values.length - 1)) * w},${h - ((v - mn) / (mx - mn)) * h}`).join(' ');
  return (
    <svg width={w} height={h} style={{ display: 'block' }}>
      <polyline points={pts} fill="none" stroke="var(--gold)" strokeWidth="1.5" />
      {values.map((v, i) => <circle key={i} cx={(i / (values.length - 1)) * w} cy={h - ((v - mn) / (mx - mn)) * h} r={2} fill="var(--gold)" />)}
    </svg>
  );
};

export default TodayPage;
