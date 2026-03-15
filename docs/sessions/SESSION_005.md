# SESSION 005 — React Frontend
**Date:** 2026-03-15
**Model:** Opus 4.6
**Goal:** Build complete React frontend with dark luxury racing aesthetic

---

## Aesthetic Direction: Dark Luxury Racing

The UI is designed for a serious handicapper reviewing a form, not a casual bettor browsing an app. Every design choice serves data density and readability:

- **Deep near-black backgrounds** (#0a0a0f) — reduces eye strain during long form study sessions
- **Gold accents** (#c9a84c) — the color of winner's silks and trophy metal. Used for rankings, headers, and the top pick
- **Green for value** (#22c55e) — overlays and value plays. Green means money.
- **Monospace for all numbers** (IBM Plex Mono) — speed figures, probabilities, odds all align in columns like a DRF form
- **Serif for horse names** (Playfair Display) — the elegance of Saratoga, not the noise of DraftKings
- **Subtle grain texture** — SVG noise overlay at 3% opacity gives the dark backgrounds depth
- **Gold rule lines** — horizontal dividers that evoke traditional racing print

## Component Hierarchy

```
App
  BrowserRouter
    Layout
      Header (sticky, gold branding, nav links)
      Routes
        TodayPage
          RaceCard (per race)
            BetBadge (race-level recommendation)
            HorseRow (per horse, densest component)
              BetBadge (per-horse)
              Flag pills (LASIX, BLINKERS, EQUIP)
        ValuePlaysPage
          ValuePlayCard (per overlay horse)
            BetBadge
        HistoryPage
          ModelStats (performance summary bar)
          RaceCard (reused from Today)
```

## Data Flow: API to UI

1. **TodayPage** calls `getRacesToday()` on mount
2. API returns `{ date, race_count, races: [{ race_id, predictions }] }`
3. Each `Race` maps to a `RaceCard`, predictions sorted by `predicted_rank`
4. Each `Prediction` maps to a `HorseRow` with all 10 data columns
5. **Value plays** are identified by `is_value_flag: true` — shown in race card footer AND on dedicated ValuePlaysPage
6. **Overlay percentage** is computed post-inference in the backend — the UI simply displays it, never computes it

## Odds-Blindness Maintained in UI

The UI displays overlay information, but the presentation makes it clear this is a post-hoc comparison:
- Rankings (#1, #2, etc.) are determined by model probability alone
- The OVERLAY column appears to the RIGHT of WIN% — visually secondary
- The Value Plays page methodology card explicitly states: "Odds were only consulted after ranking was complete"
- Morning line odds are shown for reference but never influence sort order

## Morning Line Conversion

Backend stores decimal odds (e.g., `5.0`). Frontend converts to fractional display (`5-1`) via `toFractionalOdds()` in HorseRow. This matches how morning lines appear on actual track programs.

## Derby Day Easter Egg

`Header.tsx` checks if today is the first Saturday in May. If so, the date string gets a subtle gold pulse animation (`goldPulse` keyframe), adding a celebratory feel on the biggest day in racing.

## HistoryPage: Manual P&L Review

The History page allows selecting any past date to review predictions vs actual results. This enables:
- Reviewing which predictions hit exactas/trifectas
- Spotting patterns in model performance by track, distance, or class
- Building confidence (or identifying weaknesses) before live betting

The `ModelStats` component shows race count, exacta hits, and trifecta hits as a quick performance summary bar.

---

## Files Created

| File | Role |
|------|------|
| `src/types/index.ts` | TypeScript interfaces: Prediction, Race, TodayResponse, ValuePlaysResponse |
| `src/api/client.ts` | Axios client with 5 API functions |
| `src/index.css` | Global styles: CSS variables, grain texture, animations, scrollbar |
| `src/App.tsx` | Router setup with 3 routes + redirect |
| `src/components/Layout/Header.tsx` | Sticky header: branding, date, nav |
| `src/components/Layout/Layout.tsx` | Max-width wrapper with fade-in |
| `src/components/RaceCard/BetBadge.tsx` | Colored pill badge for bet type |
| `src/components/RaceCard/HorseRow.tsx` | Dense 10-column horse data row |
| `src/components/RaceCard/RaceCard.tsx` | Full race card with header, rows, value alerts |
| `src/components/ValuePlays/ValuePlayCard.tsx` | Focused overlay card with hero overlay number |
| `src/components/Stats/ModelStats.tsx` | Performance summary bar |
| `src/components/Common/LoadingSpinner.tsx` | Gold spinning loader |
| `src/components/Common/EmptyState.tsx` | Centered empty state with emoji |
| `src/pages/TodayPage.tsx` | Main page: all qualifying races |
| `src/pages/ValuePlaysPage.tsx` | Overlay horses with methodology explanation |
| `src/pages/HistoryPage.tsx` | Date picker + historical review |
| `.env.example` | API URL template |
| `.env.local` | Local dev API URL |

**18 files created. Build compiles clean.**

---

## Next Steps (Session 006+)

1. **Deploy CDK stacks** — `cdk deploy` to create all AWS infrastructure
2. **Configure environment variables** — Set API URL, DB secrets, S3 bucket names
3. **Run database migration** — `python migrate.py --seed` to create tables and seed tracks
4. **Download Equibase 2023 dataset** — Confirm file format, implement parser
5. **Historical backfill** — Load 2023 data into database
6. **Train first model** — `python train.py` with 2023 data
7. **Activate model** — Review metrics, set active
8. **Live testing** — Run daily pipeline, review predictions vs actual results
