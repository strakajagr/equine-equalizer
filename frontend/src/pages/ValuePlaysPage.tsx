import React, { useState, useEffect } from 'react';
import { getValuePlays } from '../api/client';
import { Prediction } from '../types';
import ValuePlayCard from '../components/ValuePlays/ValuePlayCard';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import EmptyState from '../components/Common/EmptyState';

const ValuePlaysPage: React.FC = () => {
  const [plays, setPlays] = useState<Prediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await getValuePlays();
        setPlays(res.value_plays || []);
      } catch (err: any) {
        setError(err.message || 'Failed to load value plays');
      } finally {
        setLoading(false);
      }
    };
    fetch();
  }, []);

  const sorted = [...plays].sort(
    (a, b) => (b.overlay_pct || 0) - (a.overlay_pct || 0)
  );

  return (
    <div>
      {/* Page header */}
      <div style={{ marginBottom: 24 }}>
        <h1 style={{
          fontFamily: 'var(--font-display)',
          fontSize: '1.8rem',
          fontWeight: 700,
          color: 'var(--gold)',
          marginBottom: 4,
        }}>
          VALUE PLAYS
        </h1>
        <div style={{
          fontFamily: 'var(--font-body)',
          fontSize: '0.85rem',
          color: 'var(--white-dim)',
          fontStyle: 'italic',
        }}>
          Horses where the model sees more than the market
        </div>
      </div>

      {/* Methodology explanation */}
      <div style={{
        backgroundColor: 'var(--bg-secondary)',
        borderLeft: '3px solid var(--gold-dim)',
        borderRadius: 4,
        padding: '14px 20px',
        marginBottom: 28,
        fontSize: '0.8rem',
        color: 'var(--white-dim)',
        lineHeight: 1.6,
      }}>
        These horses have a model win probability at least 15% higher than what their
        morning line odds imply. The model ranked these horses using 72 performance
        features — speed figures, pace analysis, workouts, trainer patterns,
        class movement, and equipment changes. Odds were only consulted after
        ranking was complete, to identify where the market may be wrong.
      </div>

      <hr className="gold-rule" />

      {loading && <LoadingSpinner message="Scanning for overlays..." />}

      {error && (
        <EmptyState title="Connection Error" subtitle={error} />
      )}

      {!loading && !error && sorted.length === 0 && (
        <EmptyState
          title="No significant overlays identified today"
          subtitle="The market and model agree."
        />
      )}

      {!loading && !error && sorted.length > 0 && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(400px, 1fr))',
          gap: 20,
        }}>
          {sorted.map((play, idx) => (
            <div key={play.prediction_id || idx} className={`stagger-${Math.min(idx + 1, 10)}`}>
              <ValuePlayCard prediction={play} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ValuePlaysPage;
