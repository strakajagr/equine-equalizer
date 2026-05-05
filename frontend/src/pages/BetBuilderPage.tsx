import React, { useEffect, useState, useCallback, useMemo } from 'react';
import { getRacesByDate, getAvailableDates } from '../api/client';
import { Race, Prediction, AvailableDate } from '../types';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import EmptyState from '../components/Common/EmptyState';

const pct = (v: number): string => `${(v * 100).toFixed(1)}%`;

type BetType = 'exacta_box' | 'trifecta_box' | 'exacta_key' | 'trifecta_key' | 'daily_double' | 'pick3' | 'pick4';
const BET_LABELS: Record<BetType, string> = {
  exacta_box: 'Exacta Box', trifecta_box: 'Trifecta Box',
  exacta_key: 'Exacta Key', trifecta_key: 'Trifecta Key',
  daily_double: 'Daily Double', pick3: 'Pick 3', pick4: 'Pick 4',
};

interface TicketLeg {
  race: Race;
  selectedHorses: Set<string>; // horse_ids
  keyHorse: string | null; // for key bets
}

const BetBuilderPage: React.FC = () => {
  const [races, setRaces] = useState<Race[]>([]);
  const [selectedDate, setSelectedDate] = useState('');
  const [availableDates, setAvailableDates] = useState<AvailableDate[]>([]);
  const [loading, setLoading] = useState(true);
  const [betType, setBetType] = useState<BetType>('exacta_box');
  const [legs, setLegs] = useState<TicketLeg[]>([]);
  const [expandedRace, setExpandedRace] = useState<string | null>(null);
  const [exportText, setExportText] = useState('');

  useEffect(() => {
    getAvailableDates().then(d => {
      const dates = d.dates || [];
      setAvailableDates(dates);
      const withPreds = dates.find((dd: AvailableDate) => dd.has_predictions);
      if (withPreds) setSelectedDate(withPreds.date);
    }).catch(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (!selectedDate) return;
    setLoading(true);
    getRacesByDate(selectedDate).then(d => {
      setRaces(d.races || []);
      setLegs([]);
      setExpandedRace(null);
    }).catch(() => {}).finally(() => setLoading(false));
  }, [selectedDate]);

  const toggleHorse = useCallback((race: Race, horseId: string) => {
    setLegs(prev => {
      const existing = prev.find(l => l.race.race_id === race.race_id);
      if (existing) {
        const newSet = new Set(existing.selectedHorses);
        if (newSet.has(horseId)) newSet.delete(horseId);
        else newSet.add(horseId);
        if (newSet.size === 0) return prev.filter(l => l.race.race_id !== race.race_id);
        return prev.map(l => l.race.race_id === race.race_id ? { ...l, selectedHorses: newSet } : l);
      }
      return [...prev, { race, selectedHorses: new Set([horseId]), keyHorse: null }];
    });
  }, []);

  const setKey = useCallback((raceId: string, horseId: string | null) => {
    setLegs(prev => prev.map(l => l.race.race_id === raceId ? { ...l, keyHorse: horseId } : l));
  }, []);

  const autoPickModel = useCallback(() => {
    const newLegs: TicketLeg[] = [];
    const isMulti = ['daily_double', 'pick3', 'pick4'].includes(betType);
    const isKey = betType.includes('key');
    // Smarter defaults: exacta=top3, trifecta=top4, key=top4 with #1 key
    const topN = betType === 'trifecta_box' ? 4
      : betType === 'trifecta_key' ? 4
      : betType === 'exacta_box' ? 3
      : betType === 'exacta_key' ? 4
      : 2;

    if (isMulti) {
      const numLegs = betType === 'daily_double' ? 2 : betType === 'pick3' ? 3 : 4;
      // Use filtered races for current track, or all
      const sortedRaces = [...races].sort((a, b) => (a.race_number || 0) - (b.race_number || 0));
      for (let i = 0; i < Math.min(numLegs, sortedRaces.length); i++) {
        const r = sortedRaces[i];
        const sorted = [...(r.predictions || [])].sort((a, b) => a.predicted_rank - b.predicted_rank);
        const selected = new Set(sorted.slice(0, 2).map(p => p.horse_id));
        newLegs.push({ race: r, selectedHorses: selected, keyHorse: sorted[0]?.horse_id || null });
        if (!expandedRace) setExpandedRace(r.race_id);
      }
    } else if (expandedRace) {
      const r = races.find(rc => rc.race_id === expandedRace);
      if (r) {
        const sorted = [...(r.predictions || [])].sort((a, b) => a.predicted_rank - b.predicted_rank);
        const selected = new Set(sorted.slice(0, topN).map(p => p.horse_id));
        const key = isKey ? sorted[0]?.horse_id || null : null;
        newLegs.push({ race: r, selectedHorses: selected, keyHorse: key });
      }
    }
    setLegs(newLegs);
  }, [races, betType, expandedRace]);

  // Compute combinations and cost
  const ticket = useMemo(() => {
    if (legs.length === 0) return { combos: [] as string[][], cost: 0, probs: [] as number[] };
    const isMulti = ['daily_double', 'pick3', 'pick4'].includes(betType);
    const isKey = betType.includes('key');
    const isBox = betType.includes('box');
    const baseCost = 2;

    if (isMulti) {
      // Multi-race: cartesian product of all legs
      const legArrays = legs.map(l => {
        const sorted = [...(l.race.predictions || [])].sort((a, b) => a.predicted_rank - b.predicted_rank);
        return sorted.filter(p => l.selectedHorses.has(p.horse_id));
      });
      const combos: string[][] = [];
      const probs: number[] = [];
      const cart = (current: Prediction[], depth: number) => {
        if (depth === legArrays.length) {
          combos.push(current.map((p, i) => `R${legs[i].race.race_number} #${p.post_position} ${p.horse_name}`));
          probs.push(current.reduce((acc, p) => acc * p.win_probability, 1));
          return;
        }
        for (const p of legArrays[depth]) cart([...current, p], depth + 1);
      };
      if (legArrays.every(a => a.length > 0)) cart([], 0);
      return { combos, cost: combos.length * baseCost, probs };
    }

    // Single-race exotic
    const leg = legs[0];
    if (!leg) return { combos: [], cost: 0, probs: [] };
    const sorted = [...(leg.race.predictions || [])].sort((a, b) => a.predicted_rank - b.predicted_rank);
    const selected = sorted.filter(p => leg.selectedHorses.has(p.horse_id));
    const combos: string[][] = [];
    const probs: number[] = [];
    const n = selected.length;

    if (isKey && leg.keyHorse) {
      const keyP = selected.find(p => p.horse_id === leg.keyHorse);
      const others = selected.filter(p => p.horse_id !== leg.keyHorse);
      if (keyP) {
        if (betType === 'exacta_key') {
          for (const o of others) {
            combos.push([`#${keyP.post_position} ${keyP.horse_name}`, `#${o.post_position} ${o.horse_name}`]);
            probs.push(keyP.win_probability * o.win_probability);
          }
        } else { // trifecta_key
          for (let i = 0; i < others.length; i++) {
            for (let j = 0; j < others.length; j++) {
              if (i !== j) {
                combos.push([`#${keyP.post_position} ${keyP.horse_name}`, `#${others[i].post_position} ${others[i].horse_name}`, `#${others[j].post_position} ${others[j].horse_name}`]);
                probs.push(keyP.win_probability * others[i].win_probability * others[j].win_probability);
              }
            }
          }
        }
      }
    } else if (isBox) {
      if (betType === 'exacta_box') {
        for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
          if (i !== j) {
            combos.push([`#${selected[i].post_position} ${selected[i].horse_name}`, `#${selected[j].post_position} ${selected[j].horse_name}`]);
            probs.push(selected[i].win_probability * selected[j].win_probability);
          }
        }
      } else { // trifecta_box
        for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) for (let k = 0; k < n; k++) {
          if (i !== j && i !== k && j !== k) {
            combos.push([`#${selected[i].post_position} ${selected[i].horse_name}`, `#${selected[j].post_position} ${selected[j].horse_name}`, `#${selected[k].post_position} ${selected[k].horse_name}`]);
            probs.push(selected[i].win_probability * selected[j].win_probability * selected[k].win_probability);
          }
        }
      }
    }
    return { combos, cost: combos.length * baseCost, probs };
  }, [legs, betType]);

  const handleExport = useCallback(() => {
    const lines: string[] = [`${BET_LABELS[betType]} - ${selectedDate}`, ''];
    const isMulti = ['daily_double', 'pick3', 'pick4'].includes(betType);
    if (isMulti) {
      legs.forEach(l => {
        const selected = [...(l.race.predictions || [])].filter(p => l.selectedHorses.has(p.horse_id)).sort((a, b) => a.post_position - b.post_position);
        lines.push(`Race ${l.race.race_number} ${l.race.track_code}: ${selected.map(p => `#${p.post_position}`).join(', ')}`);
      });
    } else if (legs[0]) {
      const l = legs[0];
      const selected = [...(l.race.predictions || [])].filter(p => l.selectedHorses.has(p.horse_id)).sort((a, b) => a.post_position - b.post_position);
      const key = l.keyHorse ? selected.find(p => p.horse_id === l.keyHorse) : null;
      lines.push(`Race ${l.race.race_number} ${l.race.track_code}: ${BET_LABELS[betType]} ${key ? `Key #${key.post_position} with ` : ''}${selected.filter(p => p.horse_id !== l.keyHorse).map(p => `#${p.post_position}`).join('-')}`);
    }
    lines.push('', `$2 base x ${ticket.combos.length} combos = $${ticket.cost}`);
    const text = lines.join('\n');
    setExportText(text);
    navigator.clipboard?.writeText(text).catch(() => {});
  }, [legs, betType, selectedDate, ticket]);

  // Group races by track
  const racesByTrack: Record<string, Race[]> = {};
  races.forEach(r => {
    const k = r.track_code || 'UNK';
    if (!racesByTrack[k]) racesByTrack[k] = [];
    racesByTrack[k].push(r);
  });

  return (
    <div style={{ display: 'flex', gap: 24 }}>
      {/* LEFT PANEL - Race List */}
      <div style={{ width: 320, flexShrink: 0 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.15rem', color: 'var(--gold)' }}>BET BUILDER</h2>
          <select value={selectedDate} onChange={e => setSelectedDate(e.target.value)} style={{ padding: '6px 10px', backgroundColor: 'var(--bg-card)', color: 'var(--white)', border: '1px solid var(--gold-dim)', borderRadius: 6, fontFamily: 'var(--font-mono)', fontSize: '0.72rem' }}>
            {availableDates.filter(d => d.has_predictions).map(d => (<option key={d.date} value={d.date}>{d.date}</option>))}
          </select>
        </div>

        {/* Bet Type Selector */}
        <div style={{ marginBottom: 16 }}>
          <div style={{ fontSize: '0.62rem', color: 'var(--white-dim)', letterSpacing: '0.1em', marginBottom: 6 }}>TICKET TYPE</div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
            {(Object.keys(BET_LABELS) as BetType[]).map(bt => (
              <button key={bt} onClick={() => { setBetType(bt); setLegs([]); }} style={{
                padding: '6px 10px', borderRadius: 6, border: betType === bt ? '1px solid var(--gold)' : '1px solid var(--bg-hover)',
                backgroundColor: betType === bt ? 'rgba(201,168,76,0.15)' : 'var(--bg-card)',
                color: betType === bt ? 'var(--gold)' : 'var(--white-dim)', cursor: 'pointer',
                fontFamily: 'var(--font-mono)', fontSize: '0.65rem',
              }}>{BET_LABELS[bt]}</button>
            ))}
          </div>
        </div>

        {/* Model Auto-Pick */}
        <button onClick={autoPickModel} style={{
          width: '100%', padding: '10px', marginBottom: 16, backgroundColor: 'var(--gold)',
          color: '#0a0a0f', border: 'none', borderRadius: 6, cursor: 'pointer',
          fontFamily: 'var(--font-body)', fontWeight: 600, fontSize: '0.78rem', letterSpacing: '0.05em',
        }}>MODEL AUTO-PICK</button>

        {/* Race List */}
        {loading ? <LoadingSpinner message="Loading races..." /> : (
          <div>
            {Object.entries(racesByTrack).map(([track, trackRaces]) => (
              <div key={track} style={{ marginBottom: 12 }}>
                <div style={{ fontSize: '0.62rem', color: 'var(--gold-dim)', letterSpacing: '0.1em', marginBottom: 6, padding: '0 4px' }}>{track}</div>
                {trackRaces.sort((a, b) => (a.race_number || 0) - (b.race_number || 0)).map(r => {
                  const isExpanded = expandedRace === r.race_id;
                  const leg = legs.find(l => l.race.race_id === r.race_id);
                  const selCount = leg ? leg.selectedHorses.size : 0;
                  return (
                    <div key={r.race_id}>
                      <div onClick={() => setExpandedRace(isExpanded ? null : r.race_id)} style={{
                        padding: '8px 10px', marginBottom: 2, borderRadius: 6, cursor: 'pointer',
                        backgroundColor: isExpanded ? 'rgba(201,168,76,0.1)' : selCount > 0 ? 'rgba(34,197,94,0.06)' : 'transparent',
                        borderLeft: selCount > 0 ? '3px solid var(--green)' : '3px solid transparent',
                        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                      }}>
                        <div>
                          <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.82rem', fontWeight: 600, color: 'var(--gold)' }}>R{r.race_number}</span>
                          <span style={{ fontSize: '0.68rem', color: 'var(--white-dim)', marginLeft: 8 }}>{r.distance_furlongs}f {r.surface?.slice(0, 1).toUpperCase()}</span>
                        </div>
                        {selCount > 0 && <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--green)', backgroundColor: 'rgba(34,197,94,0.15)', padding: '2px 7px', borderRadius: 8 }}>{selCount} sel</span>}
                      </div>

                      {/* Expanded: show horses with checkboxes */}
                      {isExpanded && (
                        <div style={{ padding: '4px 0 8px 12px' }}>
                          {(r.predictions || []).sort((a, b) => a.predicted_rank - b.predicted_rank).map(p => {
                            const isSelected = leg?.selectedHorses.has(p.horse_id) || false;
                            const isKeyHorse = leg?.keyHorse === p.horse_id;
                            return (
                              <div key={p.horse_id} style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '5px 6px', borderRadius: 4, cursor: 'pointer', backgroundColor: isSelected ? 'rgba(34,197,94,0.06)' : 'transparent' }} onClick={() => toggleHorse(r, p.horse_id)}>
                                <div style={{ width: 18, height: 18, borderRadius: 3, border: isSelected ? '2px solid var(--green)' : '1px solid var(--white-dim)', backgroundColor: isSelected ? 'rgba(34,197,94,0.3)' : 'transparent', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.6rem', color: 'var(--green)', flexShrink: 0 }}>
                                  {isSelected && '\u2713'}
                                </div>
                                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.72rem', color: 'var(--white-dim)', width: 20 }}>{p.predicted_rank}</span>
                                <span style={{ fontSize: '0.78rem', color: p.is_top_pick ? 'var(--gold)' : 'var(--white)', flex: 1 }}>{p.horse_name}</span>
                                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.72rem', color: 'var(--white-dim)' }}>{pct(p.win_probability)}</span>
                                {betType.includes('key') && isSelected && (
                                  <button onClick={e => { e.stopPropagation(); setKey(r.race_id, isKeyHorse ? null : p.horse_id); }} style={{
                                    fontSize: '0.5rem', padding: '2px 5px', borderRadius: 4, cursor: 'pointer',
                                    border: isKeyHorse ? '1px solid var(--gold)' : '1px solid var(--white-dim)',
                                    backgroundColor: isKeyHorse ? 'rgba(201,168,76,0.2)' : 'transparent',
                                    color: isKeyHorse ? 'var(--gold)' : 'var(--white-dim)',
                                  }}>KEY</button>
                                )}
                              </div>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* RIGHT PANEL - Ticket */}
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ backgroundColor: 'var(--bg-card)', borderRadius: 8, padding: '20px 24px', position: 'sticky', top: 80 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <div>
              <div style={{ fontFamily: 'var(--font-display)', fontSize: '1.1rem', fontWeight: 700, color: 'var(--gold)' }}>{BET_LABELS[betType]}</div>
              <div style={{ fontSize: '0.72rem', color: 'var(--white-dim)', marginTop: 2 }}>{selectedDate}</div>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.4rem', fontWeight: 700, color: 'var(--gold)' }}>${ticket.cost}</div>
              <div style={{ fontSize: '0.65rem', color: 'var(--white-dim)' }}>{ticket.combos.length} combo{ticket.combos.length !== 1 ? 's' : ''} x $2</div>
            </div>
          </div>

          <hr style={{ border: 'none', height: 1, background: 'linear-gradient(90deg, transparent, var(--gold-dim), transparent)', margin: '12px 0' }} />

          {/* Selected Legs Summary */}
          {legs.length > 0 && (
            <div style={{ marginBottom: 16 }}>
              <div style={{ fontSize: '0.6rem', color: 'var(--white-dim)', letterSpacing: '0.1em', marginBottom: 8 }}>SELECTIONS</div>
              {legs.map(l => {
                const selected = [...(l.race.predictions || [])].filter(p => l.selectedHorses.has(p.horse_id)).sort((a, b) => a.post_position - b.post_position);
                return (
                  <div key={l.race.race_id} style={{ marginBottom: 8 }}>
                    <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: 'var(--gold)' }}>R{l.race.race_number} {l.race.track_code}</span>
                    <span style={{ fontSize: '0.72rem', color: 'var(--white-dim)', marginLeft: 8 }}>
                      {l.keyHorse ? 'Key ' : ''}{selected.map(p => `#${p.post_position} ${p.horse_name}${p.horse_id === l.keyHorse ? ' (K)' : ''}`).join(', ')}
                    </span>
                  </div>
                );
              })}
            </div>
          )}

          {/* Combinations */}
          {ticket.combos.length > 0 ? (
            <div>
              <div style={{ fontSize: '0.6rem', color: 'var(--white-dim)', letterSpacing: '0.1em', marginBottom: 8 }}>COMBINATIONS</div>
              <div style={{ maxHeight: 400, overflowY: 'auto' }}>
                {ticket.combos.map((combo, i) => {
                  const prob = ticket.probs[i] || 0;
                  const isBest = prob === Math.max(...ticket.probs);
                  return (
                    <div key={i} style={{
                      display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                      padding: '6px 10px', marginBottom: 2, borderRadius: 4, fontSize: '0.72rem',
                      backgroundColor: isBest ? 'rgba(201,168,76,0.08)' : 'transparent',
                      borderLeft: isBest ? '2px solid var(--gold)' : '2px solid transparent',
                    }}>
                      <div style={{ fontFamily: 'var(--font-mono)', color: 'var(--white)' }}>
                        {combo.join(' / ')}
                      </div>
                      <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: isBest ? 'var(--gold)' : 'var(--white-dim)' }}>
                        {(prob * 100).toFixed(2)}%
                        {isBest && <span style={{ marginLeft: 4, fontSize: '0.55rem', color: 'var(--gold)' }}>BEST</span>}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ) : (
            <EmptyState title="Select Horses" subtitle="Click races on the left and check horses to build your ticket" />
          )}

          {/* Export */}
          {ticket.combos.length > 0 && (
            <div style={{ marginTop: 16 }}>
              <button onClick={handleExport} style={{
                width: '100%', padding: '10px', backgroundColor: 'var(--bg-hover)',
                color: 'var(--white)', border: '1px solid var(--gold-dim)', borderRadius: 6,
                cursor: 'pointer', fontFamily: 'var(--font-body)', fontSize: '0.78rem', letterSpacing: '0.05em',
              }}>EXPORT TICKET</button>
              {exportText && (
                <pre style={{ marginTop: 8, padding: '10px', backgroundColor: 'var(--bg-secondary)', borderRadius: 6, fontSize: '0.68rem', color: 'var(--white-dim)', fontFamily: 'var(--font-mono)', whiteSpace: 'pre-wrap', lineHeight: 1.5 }}>{exportText}</pre>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default BetBuilderPage;
