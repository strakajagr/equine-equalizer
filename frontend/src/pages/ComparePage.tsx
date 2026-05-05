import React, { useState, useEffect, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { format } from 'date-fns';
import { getCompareView } from '../api/client';
import {
  CompareResponse, SpecialistStyle, SPECIALIST_STYLES,
} from '../types/predictions';
import CompareRaceCard from '../components/Compare/CompareRaceCard';
import ByStyleTable from '../components/Compare/ByStyleTable';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import EmptyState from '../components/Common/EmptyState';

function isValidStyle(s: string | null): s is SpecialistStyle {
  return !!s && (SPECIALIST_STYLES as string[]).includes(s);
}

const ComparePage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();

  const initialDate = searchParams.get('date') ||
    format(new Date(), 'yyyy-MM-dd');
  const initialStyleParam = searchParams.get('style');
  const initialStyle: SpecialistStyle =
    isValidStyle(initialStyleParam) ? initialStyleParam : 'route';

  const [date, setDate] = useState<string>(initialDate);
  const [style, setStyle] = useState<SpecialistStyle>(initialStyle);
  const [data, setData] = useState<CompareResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const updateUrl = useCallback((d: string, s: SpecialistStyle) => {
    setSearchParams({ date: d, style: s }, { replace: true });
  }, [setSearchParams]);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    getCompareView(date, style)
      .then((resp: CompareResponse) => {
        if (!cancelled) {
          setData(resp);
          setLoading(false);
        }
      })
      .catch((e: any) => {
        if (!cancelled) {
          setError(e?.message || String(e));
          setLoading(false);
        }
      });
    return () => { cancelled = true; };
  }, [date, style]);

  const handleStyleChange = (s: SpecialistStyle) => {
    setStyle(s);
    updateUrl(date, s);
  };

  const handleDateChange = (d: string) => {
    setDate(d);
    updateUrl(d, style);
  };

  return (
    <div style={{ padding: '24px', maxWidth: 1600, margin: '0 auto' }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginBottom: 24,
        gap: 16,
      }}>
        <div>
          <h1 style={{
            fontFamily: 'var(--font-display)',
            fontSize: '1.6rem',
            fontWeight: 700,
            color: 'var(--gold)',
            letterSpacing: '0.1em',
            margin: 0,
          }}>
            COMPARE — General vs Specialist
          </h1>
          <div style={{
            fontFamily: 'var(--font-body)',
            fontSize: '0.85rem',
            color: 'var(--white-dim)',
            marginTop: 4,
          }}>
            Side-by-side: General predictions on the left, specialist style on the right.
            Top-1 disagreements and rank shifts ≥ 3 are highlighted.
          </div>
        </div>
        <div>
          <label style={{
            fontFamily: 'var(--font-body)',
            fontSize: '0.7rem',
            color: 'var(--white-dim)',
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
            marginRight: 8,
          }}>
            Race Date
          </label>
          <input
            type="date"
            value={date}
            onChange={(e) => handleDateChange(e.target.value)}
            style={{
              backgroundColor: 'var(--bg-secondary)',
              border: '1px solid var(--bg-hover)',
              color: 'var(--white)',
              padding: '6px 10px',
              borderRadius: 4,
              fontFamily: 'var(--font-mono)',
              fontSize: '0.85rem',
            }}
          />
        </div>
      </div>

      {loading && <LoadingSpinner />}

      {!loading && error && (
        <EmptyState
          title="Failed to load compare view"
          subtitle={error}
        />
      )}

      {!loading && !error && data && data.races.length === 0 && (
        <EmptyState
          title="No races for this date"
          subtitle={`No predictions available for ${date}.`}
        />
      )}

      {!loading && !error && data && data.races.length > 0 && (
        <>
          <ByStyleTable storageKey="compare" />
          {data.races.map((race, i) => (
            <CompareRaceCard
              key={race.race_id}
              race={race}
              compareStyle={style}
              onStyleChange={handleStyleChange}
              showStyleSelector={i === 0}
            />
          ))}
        </>
      )}
    </div>
  );
};

export default ComparePage;
