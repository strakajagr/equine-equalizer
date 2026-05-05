import React, { useState, useEffect } from 'react';
import { getDashboardMetrics } from '../api/client';
import { DashboardMetrics } from '../types';
import LoadingSpinner from '../components/Common/LoadingSpinner';

const DashboardPage: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDashboardMetrics()
      .then(d => setMetrics(d))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner message="Loading dashboard..." />;
  if (!metrics) return <div style={{ color: 'var(--white-dim)', textAlign: 'center', padding: 40 }}>Failed to load metrics</div>;

  const am = metrics.active_model;
  const c = metrics.counts;

  return (
    <div>
      <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.2rem', color: 'var(--gold)', marginBottom: 20 }}>DASHBOARD</h2>

      {/* Active Model */}
      {am && (
        <div style={{ backgroundColor: 'var(--bg-card)', borderRadius: 8, padding: '20px 24px', marginBottom: 20, borderLeft: '3px solid var(--gold)' }}>
          <div style={{ fontSize: '0.65rem', color: 'var(--white-dim)', letterSpacing: '0.1em', marginBottom: 12 }}>ACTIVE MODEL</div>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: 16, marginBottom: 16 }}>
            <span style={{ fontFamily: 'var(--font-display)', fontSize: '1.1rem', fontWeight: 700, color: 'var(--gold)' }}>{am.version_name}</span>
            <span style={{ fontSize: '0.72rem', color: 'var(--white-dim)' }}>Trained {am.training_date?.slice(0, 10)}</span>
            <span style={{ fontSize: '0.72rem', color: 'var(--white-dim)' }}>{am.training_race_count} races</span>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 16 }}>
            <MetricCard label="Exacta Hit Rate" value={am.exacta_hit_rate != null ? `${(am.exacta_hit_rate * 100).toFixed(1)}%` : '--'} />
            <MetricCard label="Trifecta Hit Rate" value={am.trifecta_hit_rate != null ? `${(am.trifecta_hit_rate * 100).toFixed(1)}%` : '--'} />
            <MetricCard label="Top-1 Accuracy" value={am.top1_accuracy != null ? `${(am.top1_accuracy * 100).toFixed(1)}%` : '--'} />
            <MetricCard label="Top-3 Accuracy" value={am.top3_accuracy != null ? `${(am.top3_accuracy * 100).toFixed(1)}%` : '--'} />
            <MetricCard label="Calibration" value={am.calibration_score != null ? am.calibration_score.toFixed(3) : '--'} />
          </div>
          {am.notes && <div style={{ fontSize: '0.72rem', color: 'var(--white-dim)', marginTop: 12, fontStyle: 'italic' }}>{am.notes}</div>}
        </div>
      )}

      {/* Data Coverage */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: 16, marginBottom: 20 }}>
        <StatCard label="Total Races" value={c?.races?.toLocaleString() || '--'} />
        <StatCard label="Horses" value={c?.horses?.toLocaleString() || '--'} />
        <StatCard label="Entries" value={c?.entries?.toLocaleString() || '--'} />
        <StatCard label="Results" value={c?.results?.toLocaleString() || '--'} />
        <StatCard label="Predictions" value={c?.predictions?.toLocaleString() || '--'} />
        <StatCard label="Date Range" value={c ? `${c.earliest_date?.slice(0, 7)} to ${c.latest_date?.slice(0, 7)}` : '--'} small />
      </div>

      {/* Model History */}
      {metrics.model_history.length > 0 && (
        <div style={{ backgroundColor: 'var(--bg-card)', borderRadius: 8, padding: '20px 24px', marginBottom: 20 }}>
          <div style={{ fontSize: '0.65rem', color: 'var(--white-dim)', letterSpacing: '0.1em', marginBottom: 12 }}>MODEL VERSIONS</div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 100px 80px 80px 80px', gap: 8, fontSize: '0.6rem', color: 'var(--white-dim)', letterSpacing: '0.08em', padding: '6px 0', borderBottom: '1px solid var(--bg-hover)' }}>
            <div>VERSION</div><div>DATE</div><div style={{ textAlign: 'right' }}>EXACTA</div><div style={{ textAlign: 'right' }}>TRIFECTA</div><div style={{ textAlign: 'right' }}>TOP-1</div>
          </div>
          {metrics.model_history.map(m => (
            <div key={m.model_version_id} style={{ display: 'grid', gridTemplateColumns: '1fr 100px 80px 80px 80px', gap: 8, padding: '8px 0', borderBottom: '1px solid rgba(255,255,255,0.03)', alignItems: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: m.is_active ? 'var(--gold)' : 'var(--white)' }}>{m.version_name}</span>
                {m.is_active && <span style={{ fontSize: '0.55rem', padding: '1px 6px', borderRadius: 6, backgroundColor: 'rgba(201,168,76,0.2)', color: 'var(--gold-light)', fontFamily: 'var(--font-mono)' }}>ACTIVE</span>}
              </div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.72rem', color: 'var(--white-dim)' }}>{m.training_date?.slice(0, 10)}</div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', textAlign: 'right', color: 'var(--white)' }}>{m.exacta_hit_rate != null ? `${(m.exacta_hit_rate * 100).toFixed(1)}%` : '--'}</div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', textAlign: 'right', color: 'var(--white)' }}>{m.trifecta_hit_rate != null ? `${(m.trifecta_hit_rate * 100).toFixed(1)}%` : '--'}</div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', textAlign: 'right', color: 'var(--white)' }}>{m.top1_accuracy != null ? `${(m.top1_accuracy * 100).toFixed(1)}%` : '--'}</div>
            </div>
          ))}
        </div>
      )}

      {/* Prediction Dates */}
      {metrics.prediction_dates.length > 0 && (
        <div style={{ backgroundColor: 'var(--bg-card)', borderRadius: 8, padding: '20px 24px' }}>
          <div style={{ fontSize: '0.65rem', color: 'var(--white-dim)', letterSpacing: '0.1em', marginBottom: 12 }}>DATES WITH PREDICTIONS</div>
          <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
            {metrics.prediction_dates.map(d => (
              <div key={d.date} style={{ padding: '6px 12px', backgroundColor: 'var(--bg-hover)', borderRadius: 6, fontFamily: 'var(--font-mono)', fontSize: '0.72rem' }}>
                <span style={{ color: 'var(--white)' }}>{d.date}</span>
                <span style={{ color: 'var(--white-dim)', marginLeft: 6 }}>{d.count}p</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const MetricCard: React.FC<{ label: string; value: string }> = ({ label, value }) => (
  <div style={{ textAlign: 'center', padding: '12px', backgroundColor: 'var(--bg-secondary)', borderRadius: 6 }}>
    <div style={{ fontSize: '0.58rem', color: 'var(--white-dim)', letterSpacing: '0.08em', marginBottom: 4 }}>{label}</div>
    <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.3rem', fontWeight: 700, color: 'var(--gold)' }}>{value}</div>
  </div>
);

const StatCard: React.FC<{ label: string; value: string; small?: boolean }> = ({ label, value, small }) => (
  <div style={{ backgroundColor: 'var(--bg-card)', borderRadius: 8, padding: '14px 18px', textAlign: 'center' }}>
    <div style={{ fontSize: '0.58rem', color: 'var(--white-dim)', letterSpacing: '0.08em', marginBottom: 4 }}>{label}</div>
    <div style={{ fontFamily: 'var(--font-mono)', fontSize: small ? '0.82rem' : '1.1rem', fontWeight: 600, color: 'var(--white)' }}>{value}</div>
  </div>
);

export default DashboardPage;
