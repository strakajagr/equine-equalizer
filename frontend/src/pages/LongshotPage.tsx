import React, { useState, useEffect, useMemo } from 'react';
import { getLSAlerts, getAvailableDates, getWRRacesByDate } from '../api/client';
import { LSPrediction, AvailableDate } from '../types';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import EmptyState from '../components/Common/EmptyState';
import { OutcomeBadge, PLCell, PL_HEADER_TOOLTIP } from '../components/Common/PredictionOutcome';
import TrackRecordBanner from '../components/Common/TrackRecordBanner';

const fmtProb = (v: number | null): string =>
  v == null ? '--' : `${(v * 100).toFixed(1)}%`;
const fmtOdds = (v: number | null): string =>
  v == null ? '--' : `${Math.round(v)}-1`;
const fmtScore = (v: number | null, digits = 3): string =>
  v == null ? '--' : v.toFixed(digits);
const formatPostTime = (ts: string): string => {
  const m = ts.match(/(\d{2}):(\d{2})/);
  return m ? `${m[1]}:${m[2]} ET` : ts;
};
const confidenceColor = (c: string | null): string => {
  if (!c) return 'var(--white-dim)';
  switch (c.toLowerCase()) {
    case 'high':   return 'var(--gold)';
    case 'medium': return 'var(--green)';
    default:       return 'var(--white-dim)';
  }
};

const LoadFailureBanner: React.FC = () => (
  <div style={{
    padding: '36px 24px', textAlign: 'center',
    backgroundColor: 'var(--bg-card)', borderRadius: 8,
    border: '1px solid var(--gold-dim)',
  }}>
    <div style={{
      fontFamily: 'var(--font-mono)', fontSize: '0.65rem',
      color: 'var(--gold-dim)', letterSpacing: '0.15em', marginBottom: 12,
    }}>
      LS META-MODEL
    </div>
    <div style={{ fontFamily: 'var(--font-display)', fontSize: '1.2rem', color: 'var(--gold)', marginBottom: 10 }}>
      Unable to load longshot data — please retry
    </div>
    <div style={{ fontSize: '0.82rem', color: 'var(--white-dim)', maxWidth: 520, margin: '0 auto', lineHeight: 1.7 }}>
      The LS meta-model is active but the request didn't complete. This usually
      clears with a refresh. The 5 base models are trained and the stacking
      ensemble is deployed:
    </div>
    <div style={{ display: 'flex', gap: 12, justifyContent: 'center', marginTop: 16, flexWrap: 'wrap' }}>
      {['XGBoost Ranker', 'RF Longshot', 'LSTM Trajectory', 'Calibrated Prob', 'Bayesian Angle'].map(m => (
        <span key={m} style={{
          fontSize: '0.65rem', padding: '4px 10px', borderRadius: 12,
          backgroundColor: 'var(--bg-hover)', color: 'var(--white-dim)',
          fontFamily: 'var(--font-mono)', border: '1px solid rgba(255,255,255,0.08)',
        }}>{m}</span>
      ))}
    </div>
    <div style={{ fontSize: '0.72rem', color: 'var(--white-dim)', marginTop: 16, opacity: 0.6 }}>
      If this message persists across reloads, check the API endpoint
      and CloudWatch logs for /aws/lambda/equine-ls-inference.
    </div>
  </div>
);

const LongshotPage: React.FC = () => {
  const [alerts, setAlerts] = useState<LSPrediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [modelInactive, setModelInactive] = useState(false);
  const [selectedDate, setSelectedDate] = useState('');
  const [availableDates, setAvailableDates] = useState<AvailableDate[]>([]);
  const [trackFilter, setTrackFilter] = useState('ALL');

  useEffect(() => {
    getAvailableDates().then(d => {
      const dates = d.dates || [];
      setAvailableDates(dates);
      const best = dates[0]?.date || '';
      if (best) setSelectedDate(best);
    }).catch(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (!selectedDate) return;
    setLoading(true);
    setModelInactive(false);
    // Try LS endpoint first, fall back to WR predictions filtered to longshots
    getLSAlerts(selectedDate).then(d => {
      if (d.status === 'no_active_model' || d.status === 'stub_not_implemented' || !(d.longshot_alerts?.length)) {
        // Fall back to WR predictions filtered to high-odds horses
        return getWRRacesByDate(selectedDate).then(wrData => {
          const longshots: any[] = [];
          for (const race of (wrData.races || [])) {
            for (const p of (race.predictions || [])) {
              const ml = p.morning_line_odds || 0;
              if (ml >= 10 || p.longshot_alert) {
                longshots.push({
                  ...p,
                  final_win_probability: p.ensemble_win_prob || p.win_probability,
                  track_code: race.track_code,
                  race_number: race.race_number,
                  race_date: selectedDate,
                  post_time: race.post_time || null,
                  closing_odds: ml,
                  confidence_level: p.confidence || (p.longshot_alert ? 'MEDIUM' : null),
                  angle_description: p.angle_name ? `Angle: ${p.angle_name}` : null,
                  rf_longshot_prob: p.longshot_prob || null,
                  lstm_trajectory: p.trajectory_score || null,
                });
              }
            }
          }
          longshots.sort((a, b) => (b.final_win_probability || 0) - (a.final_win_probability || 0));
          setAlerts(longshots as any);
          setModelInactive(false);
        });
      }
      const sorted = (d.longshot_alerts || []).sort(
        (a: LSPrediction, b: LSPrediction) =>
          (b.final_win_probability || 0) - (a.final_win_probability || 0)
      );
      setAlerts(sorted);
    }).catch(() => {
      setModelInactive(true);
      setAlerts([]);
    }).finally(() => setLoading(false));
  }, [selectedDate]);

  const tracks = useMemo(() => {
    const s = new Set(alerts.map(a => (a as any).track_code || 'UNK'));
    return ['ALL', ...Array.from(s).sort()];
  }, [alerts]);

  const filteredAlerts = useMemo(() =>
    trackFilter === 'ALL' ? alerts : alerts.filter(a => (a as any).track_code === trackFilter),
  [alerts, trackFilter]);

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

        {/* Legend */}
        <div style={{ marginTop: 24, padding: '12px', backgroundColor: 'var(--bg-card)', borderRadius: 8 }}>
          <div style={{ fontSize: '0.6rem', color: 'var(--white-dim)', letterSpacing: '0.08em', marginBottom: 8 }}>BASE MODELS</div>
          {[
            { abbr: 'RANK',  label: 'XGBoost Ranker (raw)' },
            { abbr: 'RF',    label: 'RF Longshot' },
            { abbr: 'LSTM',  label: 'LSTM Trajectory' },
            { abbr: 'CAL',   label: 'Calibrated Prob' },
            { abbr: 'BAY',   label: 'Bayesian Angle EV' },
          ].map(({ abbr, label }) => (
            <div key={abbr} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--gold-dim)' }}>{abbr}</span>
              <span style={{ fontSize: '0.62rem', color: 'var(--white-dim)' }}>{label}</span>
            </div>
          ))}
        </div>
      </div>

      {/* MAIN */}
      <div style={{ flex: 1, minWidth: 0 }}>
        <TrackRecordBanner model="ls" storageKey="longshots" />
        <div style={{ marginBottom: 20 }}>
          <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.15rem', color: 'var(--gold)', fontWeight: 600, marginBottom: 2 }}>
            LONGSHOTS
          </h2>
          <div style={{ fontSize: '0.68rem', color: 'var(--white-dim)' }}>
            LS Meta-Model &mdash; Top Longshot Pick Per Race
          </div>
        </div>

        {loading ? (
          <LoadingSpinner message="Loading longshot alerts..." />
        ) : modelInactive ? (
          <LoadFailureBanner />
        ) : filteredAlerts.length === 0 ? (
          <EmptyState
            title="No Longshot Alerts Today"
            subtitle="The LS model found no qualifying longshot angles for this date."
          />
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {filteredAlerts.map((a, idx) => (
              <LongshotCard key={a.prediction_id || `${a.horse_id}-${idx}`} alert={a} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

const LongshotCard: React.FC<{ alert: LSPrediction }> = ({ alert: a }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div style={{
      backgroundColor: 'var(--bg-card)', borderRadius: 10,
      border: a.longshot_alert ? '1px solid rgba(201,168,76,0.35)' : '1px solid var(--bg-hover)',
      overflow: 'hidden', boxShadow: '0 2px 12px rgba(0,0,0,0.35)',
    }}>
      {/* Alert badge bar */}
      {a.longshot_alert && (
        <div style={{
          padding: '5px 20px', display: 'flex', alignItems: 'center', gap: 8,
          background: 'linear-gradient(90deg, rgba(201,168,76,0.2), rgba(201,168,76,0.05))',
          borderBottom: '1px solid rgba(201,168,76,0.2)',
          flexWrap: 'wrap',
        }}>
          <span style={{ fontSize: '0.58rem', fontFamily: 'var(--font-mono)', fontWeight: 700, letterSpacing: '0.15em', color: 'var(--gold)' }}>
            ⚡ LONGSHOT ALERT
          </span>
          {a.confidence && (
            <span style={{
              fontSize: '0.52rem', padding: '1px 6px', borderRadius: 4,
              backgroundColor: 'rgba(0,0,0,0.3)',
              color: confidenceColor(a.confidence),
              fontFamily: 'var(--font-mono)', fontWeight: 600, letterSpacing: '0.08em',
            }}>
              {a.confidence.toUpperCase()} CONFIDENCE
            </span>
          )}
          {(a.track_code || a.race_number || a.race_date || a.post_time) && (
            <span style={{
              marginLeft: 'auto',
              fontFamily: 'var(--font-mono)',
              fontSize: '0.62rem',
              color: 'var(--white-dim)',
              letterSpacing: '0.06em',
            }}>
              {a.track_code || ''} {a.race_number ? `R${a.race_number}` : ''}
              {a.race_date && ` · ${a.race_date}`}
              {a.post_time && ` · ${formatPostTime(a.post_time)}`}
            </span>
          )}
        </div>
      )}

      <div style={{ padding: '18px 20px' }}>
        {/* Header row */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 14 }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: 10 }}>
              <div style={{
                width: 28, height: 28, borderRadius: '50%',
                border: '1px solid var(--white-dim)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontFamily: 'var(--font-mono)', fontSize: '0.68rem', color: 'var(--white-dim)',
                flexShrink: 0,
              }}>{a.post_position}</div>
              <span style={{ fontFamily: 'var(--font-display)', fontSize: '1.3rem', fontWeight: 700, color: 'var(--white)' }}>
                {a.horse_name}
              </span>
            </div>
            <div style={{ fontSize: '0.72rem', color: 'var(--white-dim)', marginTop: 4 }}>
              {a.jockey_name || 'TBD'} / {a.trainer_name}
            </div>
          </div>

          {/* Big odds display */}
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '2rem', fontWeight: 700, color: 'var(--gold)', lineHeight: 1 }}>
              {fmtOdds(a.morning_line_odds)}
            </div>
            <div style={{ fontSize: '0.58rem', color: 'var(--white-dim)', letterSpacing: '0.08em' }}>MORNING LINE</div>
          </div>
        </div>

        {/* Key metrics row */}
        <div style={{ display: 'flex', gap: 24, marginBottom: 14 }}>
          <Metric label="META WIN %" value={fmtProb(a.final_win_probability)} gold />
          <Metric label="KELLY" value={a.kelly_fraction != null ? `${(a.kelly_fraction * 100).toFixed(1)}%` : '--'} />
          <Metric label="RANK" value={a.predicted_rank != null ? `#${a.predicted_rank}` : '--'} />
        </div>

        {/* Angle description */}
        {a.angle_description && (
          <div style={{
            padding: '10px 14px', marginBottom: 14,
            backgroundColor: 'rgba(201,168,76,0.08)',
            borderLeft: '3px solid var(--gold-dim)',
            borderRadius: '0 6px 6px 0',
          }}>
            <div style={{ fontSize: '0.6rem', color: 'var(--gold-dim)', letterSpacing: '0.1em', marginBottom: 4 }}>ANGLE</div>
            <div style={{ fontSize: '0.8rem', color: 'var(--white)', fontStyle: 'italic', lineHeight: 1.5 }}>
              {a.angle_description}
            </div>
          </div>
        )}

        {/* Expand/collapse for base model scores */}
        <button
          onClick={() => setExpanded(e => !e)}
          style={{
            background: 'none', border: '1px solid var(--bg-hover)', borderRadius: 5,
            color: 'var(--white-dim)', padding: '4px 12px', cursor: 'pointer',
            fontSize: '0.65rem', fontFamily: 'var(--font-mono)', letterSpacing: '0.08em',
          }}
        >
          {expanded ? '▲ HIDE BASE MODELS' : '▼ BASE MODEL SCORES'}
        </button>

        {expanded && (
          <div style={{ marginTop: 12, display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 8 }}>
            <BaseScore label="RANK SCORE" value={fmtScore(a.xgb_rank_score)} />
            <BaseScore label="RF" value={fmtProb(a.rf_longshot_prob)} />
            <BaseScore label="LSTM" value={
              a.lstm_trajectory != null
                ? `${a.lstm_trajectory >= 0 ? '+' : ''}${a.lstm_trajectory.toFixed(3)}`
                : '--'
            } />
            <BaseScore label="CAL" value={fmtProb(a.calibrated_win_prob)} />
            <BaseScore
              label="BAY EV"
              value={
                a.bayesian_angle_ev != null
                  ? `${a.bayesian_angle_ev >= 0 ? '+' : ''}${a.bayesian_angle_ev.toFixed(2)}`
                  : '--'
              }
              titleAttr="Bayesian Angle EV — fires when horse triggers known trainer angles (lasix-first-time, blinkers-on, class-drop). Empty when no angle matches."
            />
          </div>
        )}

        {/* Stream E result block — prediction_outcome + flat_bet_pl come from
            results LEFT JOIN at read time; replaces legacy denormalized fields. */}
        {a.prediction_outcome && a.prediction_outcome !== 'pending' && (
          <div style={{
            marginTop: 12, padding: '8px 12px',
            backgroundColor: a.prediction_outcome === 'win' ? 'rgba(201,168,76,0.1)' : 'var(--bg-hover)',
            borderRadius: 6, display: 'flex', gap: 12, alignItems: 'center',
          }}>
            <span style={{ fontSize: '0.62rem', color: 'var(--white-dim)', letterSpacing: '0.08em' }}>RESULT</span>
            <OutcomeBadge outcome={a.prediction_outcome} />
            {a.actual_finish_position != null && a.actual_finish_position > 3 && (
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: 'var(--white-dim)' }}>
                Finished {a.actual_finish_position}
              </span>
            )}
            {a.actual_odds != null && (
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: 'var(--white-dim)' }}>
                @ {fmtOdds(a.actual_odds)}
              </span>
            )}
            <span style={{
              marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 6,
            }} title={PL_HEADER_TOOLTIP}>
              <span style={{ fontSize: '0.55rem', color: 'var(--white-dim)', letterSpacing: '0.08em' }}>P/L</span>
              <PLCell pl={a.flat_bet_pl} />
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

const Metric: React.FC<{ label: string; value: string; gold?: boolean }> = ({ label, value, gold }) => (
  <div>
    <div style={{ fontSize: '0.55rem', color: 'var(--white-dim)', letterSpacing: '0.08em', marginBottom: 2 }}>{label}</div>
    <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1rem', fontWeight: 600, color: gold ? 'var(--gold)' : 'var(--white)' }}>{value}</div>
  </div>
);

const BaseScore: React.FC<{ label: string; value: string; titleAttr?: string }> = ({ label, value, titleAttr }) => (
  <div title={titleAttr} style={{ backgroundColor: 'var(--bg-secondary)', borderRadius: 6, padding: '8px 10px', textAlign: 'center', cursor: titleAttr ? 'help' : undefined }}>
    <div style={{ fontSize: '0.55rem', color: 'var(--white-dim)', letterSpacing: '0.08em', marginBottom: 3 }}>{label}</div>
    <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.82rem', color: value === '--' ? 'var(--white-dim)' : 'var(--white)' }}>{value}</div>
  </div>
);

export default LongshotPage;
