import React, { useEffect, useState, useMemo } from 'react';
import { getDashboardMetrics } from '../api/client';
import api from '../api/client';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import EmptyState from '../components/Common/EmptyState';

type ModelTab = 'wr' | 'pl' | 'ls';

const ModelInactiveSection: React.FC<{ model: string; description: string }> = ({ model, description }) => (
  <div style={{ padding: '28px 20px', textAlign: 'center', backgroundColor: 'var(--bg-card)', borderRadius: 8, border: '1px solid var(--bg-hover)' }}>
    <div style={{ fontSize: '0.62rem', color: 'var(--white-dim)', letterSpacing: '0.12em', marginBottom: 8, fontFamily: 'var(--font-mono)' }}>{model} MODEL</div>
    <div style={{ fontSize: '0.9rem', color: 'var(--white-dim)', marginBottom: 6 }}>Model Not Yet Active</div>
    <div style={{ fontSize: '0.75rem', color: 'var(--white-dim)', opacity: 0.6, maxWidth: 380, margin: '0 auto', lineHeight: 1.6 }}>{description}</div>
  </div>
);

interface RaceResult {
  race_date: string;
  track_code: string;
  race_number: number;
  race_type: string | null;
  purse: number | null;
  picks: { rank: number; horse: string; win_pct: number; actual: number | null; was_win: boolean | null }[];
  exacta_hit: boolean;
  trifecta_hit: boolean;
}

const PerformancePage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<ModelTab>('wr');
  const [races, setRaces] = useState<RaceResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [trackFilter, setTrackFilter] = useState('ALL');
  const [dateRange, setDateRange] = useState<[string, string]>(['', '']);

  useEffect(() => {
    const load = async () => {
      try {
        // Get all prediction dates
        const metrics = await getDashboardMetrics();
        const dates = (metrics.prediction_dates || []).map((d: any) => d.date).sort();
        if (dates.length === 0) { setLoading(false); return; }

        // Load races for all dates with predictions
        const allRaces: RaceResult[] = [];
        // Load up to 15 most recent dates to avoid timeout
        const recentDates = dates.slice(-15);
        setDateRange([recentDates[0], recentDates[recentDates.length - 1]]);

        for (const d of recentDates) {
          try {
            const res = await api.get(`/races/${d}`);
            const data = res.data;
            for (const r of (data.races || [])) {
              const preds = (r.predictions || []).sort((a: any, b: any) => a.predicted_rank - b.predicted_rank);
              const top3 = preds.slice(0, 3);
              allRaces.push({
                race_date: d,
                track_code: r.track_code || 'UNK',
                race_number: r.race_number,
                race_type: r.race_type,
                purse: r.purse,
                picks: top3.map((p: any) => ({
                  rank: p.predicted_rank,
                  horse: p.horse_name,
                  win_pct: p.win_probability,
                  actual: p.actual_finish,
                  was_win: p.was_win,
                })),
                exacta_hit: preds.some((p: any) => p.exacta_hit),
                trifecta_hit: preds.some((p: any) => p.trifecta_hit),
              });
            }
          } catch { /* skip failed dates */ }
        }
        setRaces(allRaces);
      } catch { }
      setLoading(false);
    };
    load();
  }, []);

  const tracks = useMemo(() => {
    const s = new Set(races.map(r => r.track_code));
    return ['ALL', ...Array.from(s).sort()];
  }, [races]);

  const filtered = useMemo(() => {
    return trackFilter === 'ALL' ? races : races.filter(r => r.track_code === trackFilter);
  }, [races, trackFilter]);

  // Stats
  const withResults = filtered.filter(r => r.picks[0]?.actual != null);
  const totalRaces = withResults.length;
  const top1Wins = withResults.filter(r => r.picks[0]?.was_win).length;
  const exactaHits = withResults.filter(r => r.exacta_hit).length;
  const trifectaHits = withResults.filter(r => r.trifecta_hit).length;
  const winRate = totalRaces > 0 ? top1Wins / totalRaces : 0;
  const exactaRate = totalRaces > 0 ? exactaHits / totalRaces : 0;
  const trifectaRate = totalRaces > 0 ? trifectaHits / totalRaces : 0;

  // P&L: $2 win bet on every top pick. Average win odds ~ 4-1 for simplicity
  // More accurate: count wins * avg_payout - total_bets * $2
  const totalBets = totalRaces * 2;
  const avgWinPayout = 9.60; // ~4-1 odds average for winners at qualifying tracks
  const estimatedPL = (top1Wins * avgWinPayout) - totalBets;

  // Rolling exacta chart data (by date)
  const chartData = useMemo(() => {
    const byDate: Record<string, { total: number; hits: number }> = {};
    for (const r of withResults) {
      if (!byDate[r.race_date]) byDate[r.race_date] = { total: 0, hits: 0 };
      byDate[r.race_date].total++;
      if (r.exacta_hit) byDate[r.race_date].hits++;
    }
    return Object.entries(byDate).sort((a, b) => a[0].localeCompare(b[0])).map(([d, v]) => ({
      date: d,
      rate: v.total > 0 ? v.hits / v.total : 0,
    }));
  }, [withResults]);

  const pct = (v: number) => `${(v * 100).toFixed(1)}%`;

  // CSV export
  const exportCSV = () => {
    const header = 'Date,Track,Race,Type,Purse,Pick1,Win%,Actual,Win?,Pick2,Pick3,Exacta,Trifecta';
    const rows = filtered.map(r => {
      const p1 = r.picks[0]; const p2 = r.picks[1]; const p3 = r.picks[2];
      return [r.race_date, r.track_code, r.race_number, r.race_type || '', r.purse || '',
        p1?.horse || '', ((p1?.win_pct || 0) * 100).toFixed(1), p1?.actual ?? '', p1?.was_win ? 'Y' : 'N',
        p2?.horse || '', p3?.horse || '', r.exacta_hit ? 'Y' : 'N', r.trifecta_hit ? 'Y' : 'N'
      ].join(',');
    });
    const csv = [header, ...rows].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `equine-performance-${new Date().toISOString().slice(0, 10)}.csv`;
    a.click(); URL.revokeObjectURL(url);
  };

  return (
    <div>
      {/* Model tab switcher */}
      <div style={{ display: 'flex', gap: 6, marginBottom: 20, borderBottom: '1px solid var(--bg-hover)', paddingBottom: 12 }}>
        {([
          { id: 'wr', label: 'WR MODEL', badge: 'Win Rate', active: true },
          { id: 'pl', label: 'P&L MODEL', badge: 'Profit & Loss', active: false },
          { id: 'ls', label: 'LS MODEL', badge: 'Longshot', active: false },
        ] as { id: ModelTab; label: string; badge: string; active: boolean }[]).map(({ id, label, badge }) => (
          <button
            key={id}
            onClick={() => setActiveTab(id)}
            style={{
              padding: '8px 18px', borderRadius: 6, cursor: 'pointer', border: 'none',
              backgroundColor: activeTab === id ? 'rgba(201,168,76,0.15)' : 'var(--bg-card)',
              borderBottom: activeTab === id ? '2px solid var(--gold)' : '2px solid transparent',
              color: activeTab === id ? 'var(--gold)' : 'var(--white-dim)',
              fontFamily: 'var(--font-body)', fontSize: '0.75rem', fontWeight: 500, letterSpacing: '0.08em',
            }}
          >
            {label}
            <span style={{ display: 'block', fontSize: '0.52rem', color: activeTab === id ? 'var(--gold-dim)' : 'rgba(255,255,255,0.3)', fontFamily: 'var(--font-mono)', marginTop: 1 }}>{badge}</span>
          </button>
        ))}
      </div>

      {/* P&L Model section */}
      {activeTab === 'pl' && (
        <ModelInactiveSection
          model="P&L"
          description="P&L model performance metrics — flat bet ROI, Kelly ROI, value bet win rate, and average edge on winners — will appear here once the P&L model is trained and activated."
        />
      )}

      {/* LS Model section */}
      {activeTab === 'ls' && (
        <ModelInactiveSection
          model="LS"
          description="Longshot meta-model metrics — alert hit rate, average payout on winners, longshot ROI, and alert breakdown by confidence level — will appear here once all 5 base models and the ensemble are trained."
        />
      )}

      {/* WR Model section — existing content */}
      {activeTab === 'wr' && <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.15rem', color: 'var(--gold)' }}>WR MODEL — PERFORMANCE TRACKER</h2>
        <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
          <select value={trackFilter} onChange={e => setTrackFilter(e.target.value)} style={{ padding: '6px 10px', backgroundColor: 'var(--bg-card)', color: 'var(--white)', border: '1px solid var(--gold-dim)', borderRadius: 6, fontFamily: 'var(--font-mono)', fontSize: '0.72rem' }}>
            {tracks.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
          <button onClick={exportCSV} style={{ padding: '6px 12px', backgroundColor: 'var(--bg-card)', color: 'var(--white-dim)', border: '1px solid var(--gold-dim)', borderRadius: 6, cursor: 'pointer', fontFamily: 'var(--font-mono)', fontSize: '0.72rem' }}>EXPORT CSV</button>
        </div>
      </div>

      {loading ? <LoadingSpinner message="Loading performance data..." /> : filtered.length === 0 ? <EmptyState title="No Data" subtitle="No predictions found" /> : (
        <>
          {/* Summary Stats */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: 12, marginBottom: 20 }}>
            <StatCard label="Races" value={String(totalRaces)} sub={`${dateRange[0]} to ${dateRange[1]}`} />
            <StatCard label="Win Rate" value={pct(winRate)} sub={`${top1Wins} wins`} gold />
            <StatCard label="Exacta Rate" value={pct(exactaRate)} sub={`${exactaHits} hits`} />
            <StatCard label="Trifecta Rate" value={pct(trifectaRate)} sub={`${trifectaHits} hits`} />
            <StatCard label="$2 Flat P&L" value={`${estimatedPL >= 0 ? '+' : ''}$${estimatedPL.toFixed(0)}`} sub={`$${totalBets} wagered`} green={estimatedPL > 0} />
            <StatCard label="ROI" value={totalBets > 0 ? `${((estimatedPL / totalBets) * 100).toFixed(1)}%` : '--'} green={estimatedPL > 0} />
          </div>

          {/* Exacta Rate Chart */}
          {chartData.length > 1 && (
            <div style={{ backgroundColor: 'var(--bg-card)', borderRadius: 8, padding: '16px 20px', marginBottom: 20 }}>
              <div style={{ fontSize: '0.62rem', color: 'var(--white-dim)', letterSpacing: '0.1em', marginBottom: 8 }}>EXACTA HIT RATE BY DATE</div>
              <ExactaChart data={chartData} />
            </div>
          )}

          {/* Race Table */}
          <div style={{ backgroundColor: 'var(--bg-card)', borderRadius: 8, overflow: 'hidden' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '76px 36px 32px 1fr 1fr 1fr 56px 56px', gap: 6, padding: '8px 16px', fontSize: '0.55rem', color: 'var(--white-dim)', letterSpacing: '0.08em', borderBottom: '1px solid var(--bg-hover)' }}>
              <div>DATE</div><div>TRK</div><div>R#</div><div>PICK #1</div><div>PICK #2</div><div>PICK #3</div><div style={{ textAlign: 'center' }}>EX</div><div style={{ textAlign: 'center' }}>TRI</div>
            </div>
            {filtered.map((r, i) => {
              const hasResult = r.picks[0]?.actual != null;
              return (
                <div key={`${r.race_date}-${r.track_code}-${r.race_number}`} style={{ display: 'grid', gridTemplateColumns: '76px 36px 32px 1fr 1fr 1fr 56px 56px', gap: 6, padding: '6px 16px', borderBottom: '1px solid rgba(255,255,255,0.03)', fontSize: '0.7rem', alignItems: 'center' }}>
                  <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--white-dim)' }}>{r.race_date.slice(5)}</div>
                  <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.68rem', color: 'var(--white)' }}>{r.track_code}</div>
                  <div style={{ fontFamily: 'var(--font-mono)', color: 'var(--gold)' }}>{r.race_number}</div>
                  {r.picks.slice(0, 3).map((p, pi) => (
                    <div key={pi} style={{ display: 'flex', gap: 4, alignItems: 'center' }}>
                      <span style={{ fontFamily: 'var(--font-body)', fontSize: '0.68rem', color: p.was_win ? 'var(--gold)' : 'var(--white)' }}>{p.horse?.slice(0, 14)}</span>
                      <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.58rem', color: 'var(--white-dim)' }}>{(p.win_pct * 100).toFixed(0)}%</span>
                      {hasResult && <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.58rem', fontWeight: 600, color: p.actual === 1 ? 'var(--gold)' : p.actual != null && p.actual <= 3 ? 'var(--green)' : 'var(--white-dim)' }}>{p.actual != null ? `(${p.actual})` : ''}</span>}
                    </div>
                  ))}
                  {r.picks.length < 3 && Array(3 - r.picks.length).fill(0).map((_, j) => <div key={`empty-${j}`} />)}
                  <div style={{ textAlign: 'center' }}>{hasResult ? (r.exacta_hit ? <span style={{ color: 'var(--green)' }}>HIT</span> : <span style={{ color: 'var(--white-dim)', fontSize: '0.6rem' }}>miss</span>) : ''}</div>
                  <div style={{ textAlign: 'center' }}>{hasResult ? (r.trifecta_hit ? <span style={{ color: 'var(--green)' }}>HIT</span> : <span style={{ color: 'var(--white-dim)', fontSize: '0.6rem' }}>miss</span>) : ''}</div>
                </div>
              );
            })}
          </div>
        </>
      )}
      </div>}
    </div>
  );
};

const StatCard: React.FC<{ label: string; value: string; sub?: string; gold?: boolean; green?: boolean }> = ({ label, value, sub, gold, green }) => (
  <div style={{ backgroundColor: 'var(--bg-card)', borderRadius: 8, padding: '12px 14px', textAlign: 'center' }}>
    <div style={{ fontSize: '0.55rem', color: 'var(--white-dim)', letterSpacing: '0.08em', marginBottom: 3 }}>{label}</div>
    <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.15rem', fontWeight: 700, color: green ? 'var(--green)' : gold ? 'var(--gold)' : 'var(--white)' }}>{value}</div>
    {sub && <div style={{ fontSize: '0.55rem', color: 'var(--white-dim)', marginTop: 2 }}>{sub}</div>}
  </div>
);

const ExactaChart: React.FC<{ data: { date: string; rate: number }[] }> = ({ data }) => {
  const w = 700, h = 80;
  const maxRate = Math.max(...data.map(d => d.rate), 0.3);
  const pts = data.map((d, i) => `${(i / Math.max(data.length - 1, 1)) * w},${h - (d.rate / maxRate) * h}`).join(' ');
  return (
    <svg width={w} height={h + 20} style={{ display: 'block' }}>
      {/* Grid lines */}
      <line x1={0} y1={h} x2={w} y2={h} stroke="var(--bg-hover)" />
      <line x1={0} y1={h / 2} x2={w} y2={h / 2} stroke="var(--bg-hover)" strokeDasharray="4" />
      <text x={w + 4} y={h / 2 + 4} fill="var(--white-dim)" fontSize="9">{(maxRate / 2 * 100).toFixed(0)}%</text>
      <polyline points={pts} fill="none" stroke="var(--gold)" strokeWidth="2" />
      {data.map((d, i) => (
        <circle key={i} cx={(i / Math.max(data.length - 1, 1)) * w} cy={h - (d.rate / maxRate) * h} r={3} fill={d.rate > 0 ? 'var(--green)' : 'var(--white-dim)'} />
      ))}
      {/* Date labels */}
      {data.filter((_, i) => i === 0 || i === data.length - 1 || i === Math.floor(data.length / 2)).map((d, i) => {
        const idx = i === 0 ? 0 : i === 1 ? Math.floor(data.length / 2) : data.length - 1;
        return <text key={idx} x={(idx / Math.max(data.length - 1, 1)) * w} y={h + 14} fill="var(--white-dim)" fontSize="9" textAnchor="middle">{d.date.slice(5)}</text>;
      })}
    </svg>
  );
};

export default PerformancePage;
