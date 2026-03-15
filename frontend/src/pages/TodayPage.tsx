import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import { getRacesToday } from '../api/client';
import { TodayResponse } from '../types';
import RaceCard from '../components/RaceCard/RaceCard';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import EmptyState from '../components/Common/EmptyState';

const TodayPage: React.FC = () => {
  const [data, setData] = useState<TodayResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await getRacesToday();
        setData(res);
      } catch (err: any) {
        setError(err.message || 'Failed to load races');
      } finally {
        setLoading(false);
      }
    };
    fetch();
  }, []);

  const dateStr = format(new Date(), 'EEEE, MMMM d');

  const raceCount = data?.race_count ?? 0;

  return (
    <div>
      {/* Page header */}
      <div style={{
        display: 'flex',
        alignItems: 'baseline',
        justifyContent: 'space-between',
        marginBottom: 24,
      }}>
        <div>
          <h1 style={{
            fontFamily: 'var(--font-display)',
            fontSize: '1.8rem',
            fontWeight: 700,
            color: 'var(--gold)',
            marginBottom: 4,
          }}>
            TODAY'S CARD
          </h1>
          <div style={{
            fontFamily: 'var(--font-body)',
            fontSize: '0.85rem',
            color: 'var(--white-dim)',
          }}>
            {data?.race_count ?? 0} qualifying races
          </div>
        </div>
        <div style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '0.85rem',
          color: 'var(--gold-dim)',
        }}>
          {dateStr}
        </div>
      </div>

      <hr className="gold-rule" />

      {/* Content */}
      {loading && (
        <LoadingSpinner message="Loading today's card..." />
      )}

      {error && (
        <EmptyState
          title="Connection Error"
          subtitle={error}
        />
      )}

      {!loading && !error && (!data?.races || data.races.length === 0) && (
        <EmptyState
          title="No qualifying races today"
          subtitle="Check back tomorrow."
        />
      )}

      {!loading && !error && data?.races && data.races.length > 0 && (
        <div>
          {data.races.map((race, idx) => (
            <div
              key={race.race_id}
              className={`stagger-${Math.min(idx + 1, 10)}`}
            >
              <RaceCard race={race} raceNumber={idx + 1} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TodayPage;
