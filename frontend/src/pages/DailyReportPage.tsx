/**
 * DailyReportPage — multi-strategy daily report dashboard.
 *
 * Tony reads daily report; Tony decides; Tony bets.
 * Renders pre-race report from /api/reports/daily/{race_date}.
 *
 * Features:
 *  - Date picker
 *  - High-conviction race banner (consensus signals)
 *  - No-edge race filter
 *  - Per-race expandable section: layer outputs (top-5 per layer) + all 78 strategy recommendations
 *  - Filtering: by track, by strategy category, by bet type
 *  - Historical context panel: per-strategy rolling P&L
 */
import React, { useEffect, useState, useMemo } from 'react';
import LoadingSpinner from '../components/Common/LoadingSpinner';

interface SkipStats {
  skips_count: number;
  active_count: number;
  total_strategies: number;
  skip_rate: number;
}

interface ConsensusSignals {
  top_pick_consensus: {
    horse_name: string;
    strategies_agreeing: number;
    strategy_names_sample: string[];
    consensus_strength: 'high' | 'medium' | 'low' | 'none';
  } | null;
  top_3_overlap: {
    horses: string[];
    appearance_counts: number[];
    strategies_with_overlap: number;
  } | null;
  bet_type_consensus: {
    dominant_bet_type: string;
    strategies_recommending: number;
  } | null;
  longshot_alerts: Array<{
    horse_name: string;
    morning_line_odds: number | null;
    strategies_picking_longshot: number;
  }> | null;
  high_conviction_flag: boolean;
  no_edge_flag: boolean;
}

interface LayerEntry {
  horse_name: string;
  program_number: string | null;
  morning_line_odds: number | null;
  value: number | null;
}

interface StrategyRec {
  bet_type: string;
  horses: string[];
  legs?: string[][] | null;
  stake: number;
  confidence: number | null;
  rationale: string;
}

interface RaceSection {
  race_id: string;
  track: string;
  race_number: number;
  race_name?: string;
  post_time?: string;
  field_size?: number;
  distance_furlongs?: number;
  surface?: string;
  race_type?: string;
  purse?: number;
  grade?: number;
  layer_outputs: Record<string, LayerEntry[]>;
  skip_stats: SkipStats;
  consensus_signals: ConsensusSignals;
  strategy_recommendations: Record<string, StrategyRec | null>;
}

interface MultiLegRec {
  strategy_name: string;
  race_id: string;
  bet_type: string;
  horses: string[];
  legs: string[][];
  leg_race_ids: string[];
  stake: number;
  confidence: number | null;
  rationale: string;
  track: string;
}

interface DailyReport {
  race_date: string;
  generated_at: string;
  strategy_count: number;
  strategy_categories: Record<string, number>;
  race_count: number;
  historical_context: Record<string, any>;
  races: RaceSection[];
  multi_leg_recommendations: MultiLegRec[];
  errors: any[];
}

const API_BASE = process.env.REACT_APP_API_BASE || '';

const DailyReportPage: React.FC = () => {
  const [date, setDate] = useState<string>(new Date().toISOString().slice(0, 10));
  const [report, setReport] = useState<DailyReport | null>(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [trackFilter, setTrackFilter] = useState<string>('all');
  const [hideNoEdge, setHideNoEdge] = useState(false);
  const [expandedRaces, setExpandedRaces] = useState<Set<string>>(new Set());

  useEffect(() => {
    setLoading(true); setErr(null);
    fetch(`${API_BASE}/api/reports/daily/${date}`)
      .then(r => r.json())
      .then(setReport)
      .catch(e => setErr(String(e)))
      .finally(() => setLoading(false));
  }, [date]);

  const tracks = useMemo(
    () => report ? Array.from(new Set(report.races.map(r => r.track))).sort() : [],
    [report]
  );

  const filteredRaces = useMemo(() => {
    if (!report) return [];
    return report.races.filter(r => {
      if (trackFilter !== 'all' && r.track !== trackFilter) return false;
      if (hideNoEdge && r.consensus_signals.no_edge_flag) return false;
      return true;
    });
  }, [report, trackFilter, hideNoEdge]);

  const highConvictionRaces = useMemo(
    () => report ? report.races.filter(r => r.consensus_signals.high_conviction_flag) : [],
    [report]
  );

  const toggleRace = (race_id: string) => {
    setExpandedRaces(prev => {
      const next = new Set(prev);
      if (next.has(race_id)) next.delete(race_id);
      else next.add(race_id);
      return next;
    });
  };

  if (loading) return <LoadingSpinner />;
  if (err) return <div className="error">Error: {err}</div>;
  if (!report) return <div>No report.</div>;

  return (
    <div className="daily-report-page">
      <header style={{ marginBottom: 24 }}>
        <h1>EE Daily Report — {report.race_date}</h1>
        <div style={{ display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
          <input type="date" value={date} onChange={e => setDate(e.target.value)} />
          <label>
            Track:{' '}
            <select value={trackFilter} onChange={e => setTrackFilter(e.target.value)}>
              <option value="all">All ({tracks.length})</option>
              {tracks.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </label>
          <label>
            <input type="checkbox" checked={hideNoEdge} onChange={e => setHideNoEdge(e.target.checked)} />
            {' '}Hide no-edge races
          </label>
          <span style={{ color: '#666', fontSize: 13 }}>
            {report.race_count} races • {report.strategy_count} strategies •
            {' '}{report.multi_leg_recommendations.length} multi-leg recs
          </span>
        </div>
      </header>

      {highConvictionRaces.length > 0 && (
        <section style={{ background: '#e7f3e7', padding: 12, borderRadius: 6, marginBottom: 16 }}>
          <h3 style={{ margin: 0, color: '#0a5a0a' }}>
            High-conviction races ({highConvictionRaces.length})
          </h3>
          <ul>
            {highConvictionRaces.map(r => {
              const tp = r.consensus_signals.top_pick_consensus!;
              return (
                <li key={r.race_id}>
                  <strong>{r.track} R{r.race_number}</strong>:{' '}
                  {tp.horse_name} backed by {tp.strategies_agreeing} strategies ({tp.consensus_strength})
                </li>
              );
            })}
          </ul>
        </section>
      )}

      <section>
        <h2>Races ({filteredRaces.length})</h2>
        {filteredRaces.map(race => (
          <RaceCard
            key={race.race_id}
            race={race}
            expanded={expandedRaces.has(race.race_id)}
            onToggle={() => toggleRace(race.race_id)}
          />
        ))}
      </section>

      <section style={{ marginTop: 32 }}>
        <h2>Multi-leg recommendations ({report.multi_leg_recommendations.length})</h2>
        <MultiLegTable recs={report.multi_leg_recommendations} trackFilter={trackFilter} />
      </section>

      <section style={{ marginTop: 32 }}>
        <h2>Historical context (rolling 7d ROI by strategy)</h2>
        <HistoricalContextTable context={report.historical_context} />
      </section>

      {report.errors.length > 0 && (
        <section style={{ marginTop: 32, background: '#fee', padding: 12, borderRadius: 6 }}>
          <h3>Errors ({report.errors.length})</h3>
          <pre style={{ fontSize: 11 }}>{JSON.stringify(report.errors.slice(0, 10), null, 2)}</pre>
        </section>
      )}
    </div>
  );
};

const RaceCard: React.FC<{
  race: RaceSection;
  expanded: boolean;
  onToggle: () => void;
}> = ({ race, expanded, onToggle }) => {
  const cs = race.consensus_signals;
  const bgcolor = cs.high_conviction_flag ? '#e7f3e7' :
                  cs.no_edge_flag ? '#f5f5f5' : '#fff';

  return (
    <div style={{
      border: '1px solid #ddd', borderRadius: 4, padding: 12,
      marginBottom: 8, background: bgcolor,
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', cursor: 'pointer' }}
           onClick={onToggle}>
        <div>
          <strong>{race.track} R{race.race_number}</strong>
          {race.race_name && <span style={{ color: '#666', marginLeft: 8 }}>{race.race_name}</span>}
          <span style={{ color: '#888', marginLeft: 12, fontSize: 12 }}>
            {race.race_type} • fs={race.field_size} • ${race.purse?.toLocaleString()}
          </span>
        </div>
        <div style={{ fontSize: 13 }}>
          Active: {race.skip_stats.active_count} / Skip: {race.skip_stats.skips_count} ({(race.skip_stats.skip_rate * 100).toFixed(0)}%)
        </div>
      </div>

      {cs.top_pick_consensus && (
        <div style={{ marginTop: 8, fontSize: 13 }}>
          Top pick: <strong>{cs.top_pick_consensus.horse_name}</strong>
          {' '}({cs.top_pick_consensus.strategies_agreeing} strategies, {cs.top_pick_consensus.consensus_strength})
          {cs.bet_type_consensus && ` • Dom bet: ${cs.bet_type_consensus.dominant_bet_type} (${cs.bet_type_consensus.strategies_recommending})`}
        </div>
      )}

      {expanded && (
        <div style={{ marginTop: 12 }}>
          <h4>Layer top-5</h4>
          {Object.entries(race.layer_outputs).map(([layer, entries]) => (
            <div key={layer} style={{ marginBottom: 6, fontSize: 12 }}>
              <strong>{layer}:</strong>{' '}
              {Array.isArray(entries) && entries.slice(0, 5).map((e, i) => (
                <span key={i} style={{ marginRight: 12 }}>
                  {e.horse_name} ({e.value?.toFixed(3)})
                </span>
              ))}
            </div>
          ))}
          <h4>Strategy recommendations (active only)</h4>
          <table style={{ width: '100%', fontSize: 12, borderCollapse: 'collapse' }}>
            <thead><tr style={{ background: '#eef' }}>
              <th align="left">Strategy</th><th>Bet</th><th>Horses</th><th>Stake</th><th>Confidence</th>
            </tr></thead>
            <tbody>
              {Object.entries(race.strategy_recommendations)
                .filter(([_, rec]) => rec !== null)
                .map(([name, rec]) => (
                  <tr key={name} style={{ borderBottom: '1px solid #eee' }}>
                    <td>{name}</td>
                    <td>{rec!.bet_type}</td>
                    <td>{rec!.horses.join(', ')}</td>
                    <td>${rec!.stake.toFixed(2)}</td>
                    <td>{rec!.confidence?.toFixed(3) ?? '—'}</td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

const MultiLegTable: React.FC<{ recs: MultiLegRec[]; trackFilter: string }> = ({ recs, trackFilter }) => {
  const filtered = trackFilter === 'all' ? recs : recs.filter(r => r.track === trackFilter);
  return (
    <table style={{ width: '100%', fontSize: 12, borderCollapse: 'collapse' }}>
      <thead><tr style={{ background: '#eef' }}>
        <th align="left">Strategy</th><th>Track</th><th>Bet</th><th>Legs</th><th>Stake</th>
      </tr></thead>
      <tbody>
        {filtered.slice(0, 200).map((r, i) => (
          <tr key={i} style={{ borderBottom: '1px solid #eee' }}>
            <td>{r.strategy_name}</td>
            <td>{r.track}</td>
            <td>{r.bet_type}</td>
            <td>{r.legs.map(l => `[${l.join(',')}]`).join(' → ')}</td>
            <td>${r.stake.toFixed(2)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

const HistoricalContextTable: React.FC<{ context: Record<string, any> }> = ({ context }) => {
  const rows = Object.entries(context)
    .filter(([_, c]: any) => c.rolling_7d && c.rolling_7d.n > 0)
    .sort((a: any, b: any) => (b[1].rolling_7d.roi ?? -999) - (a[1].rolling_7d.roi ?? -999));
  return (
    <table style={{ width: '100%', fontSize: 12, borderCollapse: 'collapse' }}>
      <thead><tr style={{ background: '#eef' }}>
        <th align="left">Strategy</th><th>Bets (7d)</th><th>Wins</th>
        <th>Stake</th><th>P&L</th><th>ROI</th><th>Signals</th>
      </tr></thead>
      <tbody>
        {rows.slice(0, 30).map(([name, c]: any) => (
          <tr key={name} style={{ borderBottom: '1px solid #eee' }}>
            <td>{name}</td>
            <td>{c.rolling_7d.n}</td>
            <td>{c.rolling_7d.wins}</td>
            <td>${c.rolling_7d.stake.toFixed(0)}</td>
            <td style={{ color: c.rolling_7d.pnl >= 0 ? '#0a7a0a' : '#a02020' }}>
              ${c.rolling_7d.pnl?.toFixed(0)}
            </td>
            <td>{c.rolling_7d.roi !== null ? `${c.rolling_7d.roi}%` : '—'}</td>
            <td style={{ fontSize: 11 }}>{(c.signals || []).join('; ')}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default DailyReportPage;
