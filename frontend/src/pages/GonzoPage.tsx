import React from 'react';
import TodayPage from './TodayPage';

/**
 * Gonzo Sauce predictions page.
 * Phase A3 (2026-05-02). Renders TodayPage's existing UI with style='gonzo_sauce'
 * baked in — no UI duplication, single source of presentation logic.
 *
 * The 8th specialist alongside the existing 7-style gallery. Trains on lean53
 * base (53) + 14 new features (speed-at-distance, trajectory routes-only,
 * class established) = 67 features. Backed by wp_full_gonzo_sauce + rk_full_gonzo_sauce
 * artifacts trained 2026-05-02.
 *
 * V1 limitation: workout coverage gap (Bug #7) means most horses fall back to
 * rk_core ranker for both gonzo and general styles, so visible differentiation
 * is muted today. As workout coverage fills in (and Phase A3.5 ships the
 * calibration+0-PP fix per Bug #24), gonzo's signal will grow more pronounced.
 */
const GonzoPage: React.FC = () => {
  return <TodayPage specialistStyle="gonzo_sauce" />;
};

export default GonzoPage;
