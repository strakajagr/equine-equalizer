import React, { useState } from 'react';
import { getRacesByDate } from '../api/client';
import { TodayResponse } from '../types';
import RaceCard from '../components/RaceCard/RaceCard';
import ModelStats from '../components/Stats/ModelStats';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import EmptyState from '../components/Common/EmptyState';

const HistoryPage: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState('');
  const [data, setData] = useState<TodayResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDateChange = async (dateStr: string) => {
    setSelectedDate(dateStr);
    if (!dateStr) return;

    setLoading(true);
    setError(null);
    try {
      const res = await getRacesByDate(dateStr);
      setData(res);
    } catch (err: any) {
      setError(err.message || 'Failed to load races');
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  // Compute performance summary from predictions
  const computeStats = () => {
    if (!data?.races) return { races: 0, exactaHits: 0, trifectaHits: 0 };

    let races = data.races.length;
    let exactaHits = 0;
    let trifectaHits = 0;

    // These would come from the actual results data in a full implementation
    // For now we show the race count and placeholder zeros
    return { races, exactaHits, trifectaHits };
  };

  const stats = computeStats();

  return (
    <div>
      {/* Page header */}
      <div style={{ marginBottom: 24 }}>
        <h1 style={{
          fontFamily: 'var(--font-display)',
          fontSize: '1.8rem',
          fontWeight: 700,
          color: 'var(--gold)',
          marginBottom: 16,
        }}>
          HISTORY
        </h1>

        {/* Date picker */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <label style={{
            fontFamily: 'var(--font-body)',
            fontSize: '0.8rem',
            color: 'var(--white-dim)',
            textTransform: 'uppercase',
            letterSpacing: '0.08em',
          }}>
            SELECT DATE
          </label>
          <input
            type="date"
            value={selectedDate}
            onChange={e => handleDateChange(e.target.value)}
            style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.85rem',
              padding: '8px 12px',
              backgroundColor: 'var(--bg-secondary)',
              color: 'var(--white)',
              border: '1px solid var(--bg-hover)',
              borderRadius: 6,
              outline: 'none',
              cursor: 'pointer',
            }}
            onFocus={e => { e.target.style.borderColor = 'var(--gold)'; }}
            onBlur={e => { e.target.style.borderColor = 'var(--bg-hover)'; }}
          />
        </div>
      </div>

      <hr className="gold-rule" />

      {/* Performance summary */}
      {data && data.races && data.races.length > 0 && (
        <div style={{ marginBottom: 24 }}>
          <ModelStats
            raceCount={stats.races}
            exactaHits={stats.exactaHits}
            trifectaHits={stats.trifectaHits}
          />
        </div>
      )}

      {/* Content */}
      {loading && <LoadingSpinner message="Loading historical data..." />}

      {error && <EmptyState title="Error" subtitle={error} />}

      {!loading && !error && !selectedDate && (
        <EmptyState
          title="Select a date to view historical predictions"
          subtitle="See how the model performed on past race cards."
        />
      )}

      {!loading && !error && selectedDate && data && data.races?.length === 0 && (
        <EmptyState
          title="No predictions found for this date"
          subtitle="Either no qualifying races ran or predictions were not generated."
        />
      )}

      {!loading && !error && data && data.races && data.races.length > 0 && (
        <div>
          {data.races.map((race, idx) => (
            <div key={race.race_id} className={`stagger-${Math.min(idx + 1, 10)}`}>
              <RaceCard race={race} raceNumber={idx + 1} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default HistoryPage;
