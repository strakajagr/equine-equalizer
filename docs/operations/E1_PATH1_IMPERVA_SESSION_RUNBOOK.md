# E1 Path 1 — Equibase Imperva Session Re-establish + 13-day Chart Backfill Runbook

**Authored**: 2026-05-12 (Phase A E1 Path 1 bridge dispatch)
**Operator**: Tony (executes from local laptop with browser-capable display)
**Sibling repo**: `/home/strakajagr/equibase_scraper/` (out-of-band to main project repo; out-of-version-control per E1 Step 1 diagnostic)
**Purpose**: Re-establish Equibase Imperva session (currently dead since at least 2026-04-28) + backfill 13-day chart-PDF gap (race-dates 2026-04-30 → 2026-05-12 inclusive)
**Substrate citations**: every command + flag traces to `download_charts.py` and `run_daily_refresh.sh` source verbatim at indicated line ranges.

---

## Section 1 — Pre-Execution Checklist

Operator confirms each item before invoking Section 2. Failure of any pre-execution check → halt; surface for sub-investigation.

### 1.1 Working directory + venv

```bash
cd /home/strakajagr/equibase_scraper
pwd
# Expected output: /home/strakajagr/equibase_scraper
```

```bash
source venv/bin/activate
which python3
# Expected output: /home/strakajagr/equibase_scraper/venv/bin/python3
```

### 1.2 AWS credentials active

```bash
aws sts get-caller-identity
```

Expected output JSON contains `"Account": "584812014683"`. Required because the run will end with `aws s3 sync charts/ s3://equine-raw-data/charts/` (`run_daily_refresh.sh:91-94`).

**Note:** Section 2 invokes `download_charts.py` directly (not via `run_daily_refresh.sh`). The S3 sync is NOT auto-invoked by `download_charts.py` itself; the operator runs an explicit `aws s3 sync` after the scraper completes (Section 4).

### 1.3 Display server / browser-capable session

Imperva CAPTCHA solving requires a browser GUI:

```bash
echo "$DISPLAY"
```

Expected output: non-empty (e.g. `:0`, `:1`, `localhost:10.0` for X-forwarded SSH). If empty:

- If running on Tony's laptop directly: display server should be available; X-server / Wayland should be running.
- If SSH session: must use `ssh -X` or `ssh -Y` X-forwarding (slower; may have responsiveness issues with Imperva slider puzzles); alternatively, run via VNC / RDP session.
- If running headless server: **halt and surface** — interactive CAPTCHA cannot be solved without a display.

### 1.4 Network connectivity

```bash
ping -c 2 www.equibase.com
```

Expected: 2 successful echo replies. If unreachable: halt; investigate network/DNS before retry.

### 1.5 Substrate state confirmation (read-only)

```bash
stat .session_state.json
```

Expected mtime: `2026-04-30 00:16:48 -0400` (stale, ~12 days old at this dispatch). After Section 2 completes successfully, mtime should advance to a current timestamp.

```bash
stat download_charts.py
```

Expected mtime: `2026-04-27 23:50:26 -0400` (unchanged since E1 Step 1 diagnostic substrate read). If mtime differs, halt — scraper has been modified out-of-band and the runbook commands below may not match current scraper behavior.

---

## Section 2 — Session Refresh + Backfill Invocation

### 2.1 Command (verbatim)

```bash
cd /home/strakajagr/equibase_scraper
source venv/bin/activate
python3 download_charts.py --days-back 14
```

**Flag substrate verification.**
- `--days-back 14` per `download_charts.py:69-72` argparse block (`type=int, default=7, metavar="N"`; help: "Iterate from today - N days back through today (default 7)").
- Iteration window: `START_DATE = date.today() - timedelta(days=14)` per `download_charts.py:75` = 2026-04-28; `END_DATE = date.today()` = 2026-05-12. Total date range 15 race-dates inclusive.
- **No `--unattended` flag.** Interactive mode triggers the operator-input pause at `download_charts.py:314-315` (`if not ARGS.unattended: input(">>> Solve CAPTCHA if shown, then press ENTER <<< ")`).
- `< /dev/null` redirection from `run_daily_refresh.sh:71` is **OMITTED** here — interactive mode requires stdin for the `input()` prompt.

### 2.2 Expected execution flow

| Phase | What happens | Substrate citation |
|---|---|---|
| 1 | Scraper prints header (`Equibase Chart Downloader`, track list, date range, combinations count, output dir) | `download_charts.py:350-355` |
| 2 | If `.session_state.json` exists: prints `Loading session state from .session_state.json` | `download_charts.py:385-388` |
| 3 | Opens Playwright Chromium browser window (`headless=False` because `--unattended` not set) | `download_charts.py:371-374` |
| 4 | Browser navigates to `CAPTCHA_URL` = `https://www.equibase.com/premium/pubPDFChartIndex.cfm?TID=GP&CTRY=USA&DAY=D&DT=03/05/2023&STYLE=EQB&BorP=B&requesttimeout=60` | `download_charts.py:91-95`, `:294-298` |
| 5 | 8-second sleep for Imperva JS challenge to run | `download_charts.py:305` |
| 6 | Diagnostic cookie dumps printed to stdout | `download_charts.py:303-311` |
| 7 | **Prompt**: `>>> Solve CAPTCHA if shown, then press ENTER <<< ` | `download_charts.py:315` |
| 8 | **OPERATOR ACTION**: solve any Imperva challenge in the browser window (CAPTCHA, "Pardon Our Interruption" interstitial, slider puzzle, etc.). If browser already shows the actual chart index page without challenge, no action needed. Then return to terminal and press ENTER. | runbook step |
| 9 | Scraper runs `warmup_check()` on 3 known race-day URLs (GP 2022-04-23, SA 2022-01-07, GP 2023-03-05) | `download_charts.py:260-272`, `:97-110` |
| 10 | If warmup passes: prints `All 3 warmup checks passed — session is live` + saves refreshed session to `.session_state.json` | `download_charts.py:271`, `:320-321` |
| 11 | If warmup fails: prints `Session is NOT ready. Solve the CAPTCHA fully, then press ENTER to retry warmup.` Loop back to step 7. | `download_charts.py:317-333` |
| 12 | After warmup passes, prints `Starting downloads...` and iterates 15 race-dates × 11 tracks = 165 combos | `download_charts.py:392-490` |
| 13 | Per-PDF success log: `  ✓ {track} {race_date} ({downloaded} total, req#{request_count})` | `download_charts.py:417-421` |
| 14 | Per-PDF no-racing case: silent (counted only) | `download_charts.py:474-479` |
| 15 | Per-PDF session_dead during iteration: counted; if `consecutive_dead >= 10` (`SESSION_DEAD_THRESHOLD` per `download_charts.py:112`), scraper opens fresh page (re-prompts for CAPTCHA in interactive mode) | `download_charts.py:424-472` |
| 16 | Sleep delays between requests: `DELAY_HIT=2s`, `DELAY_MISS=0.2s`, `DELAY_ERROR=5s` per `download_charts.py:87-89` |
| 17 | Final summary: `Downloaded: N`, `No racing: N`, `Skipped: N`, `Errors: N` | `download_charts.py:504-509` |
| 18 | Scraper exits (browser closes automatically per `download_charts.py:502`) | `download_charts.py:502` |

### 2.3 Expected duration

CC cannot extract a verifiable baseline duration from sibling-repo substrate (no successful unattended log exists in the captured 2026-04-28 → 2026-05-12 window; the Apr 30 00:16 EDT interactive run completed but its precise duration is not captured in any log file accessible at runbook authorship). **Duration TBD per first execution**; the operator should observe and report the actual duration at Section 4 acceptance check. Order-of-magnitude estimate from per-iteration delays (`DELAY_HIT=2s` × 60 PDFs = ~120s minimum scraper-side; plus 8s warmup + 165 × 2s sleeps = ~330s minimum) suggests **5-15 minutes total** for the 14-day backfill; CAPTCHA solve time adds variable operator-side latency.

### 2.4 What NOT to do

- **Do NOT close the browser window manually.** Scraper closes it automatically at `download_charts.py:502`. Premature manual close will likely raise a Playwright exception.
- **Do NOT pass `--unattended`.** This is the bridge specifically because automated mode requires session refresh that cron cannot perform.
- **Do NOT interrupt with Ctrl-C unless scraper has clearly hung** (no stdout activity for > 5 minutes). Mid-iteration interruption may leave partial state in `.session_state.json` or `download_log.txt`.

---

## Section 3 — During-Execution Monitoring

### 3.1 Log surface

**Interactive run does not write to `logs/{YYYYMMDD}/charts.log`.** That log path is populated only when invoked via `run_daily_refresh.sh:71` which redirects via `> "$charts_log" 2>&1`. The Section 2 command runs `python3 download_charts.py --days-back 14` directly — stdout goes to the terminal, not to a log file.

Operator monitors directly in the terminal where the command runs.

**Optional: tee stdout to a transcript file** for post-run review:

```bash
python3 download_charts.py --days-back 14 2>&1 | tee /tmp/e1_path1_run.log
```

### 3.2 Observable success signals (stdout patterns)

| Signal | Pattern | Substrate |
|---|---|---|
| Header printed | `Equibase Chart Downloader` | `download_charts.py:350` |
| Session loaded | `Loading session state from .session_state.json` | `download_charts.py:387` |
| Browser opened | (Chromium window appears on screen) | `download_charts.py:371-374` |
| Cookie dump on navigation | `[DIAG after-goto] N cookies:` | `download_charts.py:303-304` |
| Prompt awaiting CAPTCHA solve | `>>> Solve CAPTCHA if shown, then press ENTER <<< ` | `download_charts.py:315` |
| Warmup probing | `Warmup check — testing 3 known race days...` | `download_charts.py:261` |
| Warmup pass per URL | `  ✓ GP 2022-04-23 — PDF received` | `download_charts.py:267` |
| Warmup all-pass | `All 3 warmup checks passed — session is live` | `download_charts.py:271` |
| Session state saved | `  [session state] saved to .session_state.json` | `download_charts.py:321` |
| Iteration start | `Starting downloads...` | `download_charts.py:392` |
| Per-PDF success | `  ✓ {TRACK} {YYYY-MM-DD} ({N} total, req#{N})` | `download_charts.py:417-421` |
| Final summary | `Downloaded: N` / `No racing: N` / `Skipped: N` / `Errors: N` | `download_charts.py:504-509` |

### 3.3 Observable failure signals + first-response action

| Signal | Pattern | First response |
|---|---|---|
| Warmup-per-URL fail | `  ✗ GP 2022-04-23 — got session_dead` | Solve CAPTCHA in browser window; press ENTER at prompt; loop continues (`download_charts.py:317-333`) |
| Session_dead during iteration | `  ? {TRACK} {DATE} session_dead ({N}/10)` | Wait — at 10 consecutive, scraper re-opens fresh page automatically (`download_charts.py:428-436`); if interactive, will re-prompt for CAPTCHA |
| Hung warmup (no stdout for > 5 min) | (silence) | Likely Imperva slider puzzle requiring interaction; check browser window for unsolved challenge |
| Browser failed to open | `[DIAG open_fresh_page ...] EXCEPTION during goto/sleep: ...` | Playwright install issue; check `pip list | grep playwright` and re-run `playwright install chromium` from venv |
| Network error mid-iteration | `[DIAG goto] aborted/exception: ...` | Transient — scraper continues; if persistent across multiple PDFs, halt and check network |
| Rate-limit indication | HTTP 429 / 403 in any cookie dump or response | **Halt + surface** — runbook does not cover rate-limit recovery; substrate has no rate-limit-handling logic; if encountered, abort scraper and wait 30+ minutes before retry |
| Per-PDF retry-failed | `  ✗ {TRACK} {DATE} (retry failed: {STATUS})` | Logged; iteration continues (`download_charts.py:457-464`) |

---

## Section 4 — Post-Execution Verification

### 4.1 Scraper exit code

```bash
echo $?
```

Expected: `0`. Non-zero → check final summary output for `Errors:` count; if errors > 0, surface for sub-investigation.

### 4.2 Session state refresh confirmation

```bash
stat .session_state.json
```

Expected: mtime within the last hour (i.e. timestamp from current run). If mtime still `2026-04-30 00:16:48 -0400` → session was not saved → warmup likely never passed → surface.

### 4.3 New PDF count (filesystem-side)

```bash
find charts/ -newer .session_state.json -name '*.pdf' | wc -l
```

Wait — `.session_state.json` mtime advanced during the run, so this would only count PDFs written AFTER session-save. Better query:

```bash
find charts/ -name '*.pdf' -newer download_log.txt.bak2 | wc -l
```

`download_log.txt.bak2` mtime is 2026-04-30T00:10:00 EDT (per E1 Step 1 inventory; predates the current run). The query counts all PDFs created since.

**Expected new-PDF count: 30-80** (per E1 Step 1 cardinality analysis — backfill window May 1 → May 12 = 12 race-dates, typical 4-5 PDFs/day pre-failure window, gives 48-60 expected; Apr 30 already in `download_log.txt` as 11 NR entries → 0 new from Apr 30; some May dates may have lower or higher counts).

Acceptance threshold: **≥ 30 new PDFs** = bridge succeeded.

### 4.4 S3 sync confirmation

Section 2 command does NOT auto-invoke S3 sync. Operator runs the sync command verbatim from `run_daily_refresh.sh:92-94`:

```bash
aws s3 sync charts/ s3://equine-raw-data/charts/ \
    --exclude "*" --include "*.pdf" \
    --region us-east-1
```

Expected output: list of `upload:` lines, one per new PDF + final summary. If no upload lines printed but `find` from § 4.3 reported new PDFs → check AWS credentials + bucket permissions.

### 4.5 S3 inventory delta verification

```bash
aws s3 ls s3://equine-raw-data/charts/ --recursive | awk '$1 >= "2026-05-12"' | wc -l
```

Expected: ≥ number of new PDFs reported in § 4.3 (current-run uploads stamped with today's date). Should match the upload-lines count from § 4.4.

### 4.6 Per-race-date PDF presence spot-check

Operator picks 2 sample race-dates in the gap window for verification:

- **2026-05-02 (Kentucky Derby day):** Saturday; high-cardinality day. Expected ≥ 4 PDFs across CD/GP/SAR/KEE/SA etc.
  ```bash
  aws s3 ls s3://equine-raw-data/charts/ --recursive | grep '_20260502\.pdf'
  ```
- **2026-05-08 (Friday before Preakness week):** Expected ≥ 3 PDFs.
  ```bash
  aws s3 ls s3://equine-raw-data/charts/ --recursive | grep '_20260508\.pdf'
  ```

If both spot-checks return 0 results → some race-dates may have had no actual races OR scraper iterations for those dates failed silently. Cross-check with `download_log.txt` (`grep _20260502 download_log.txt` to see PDF_ vs NR_ entries per track).

---

## Section 5 — Next-Day Cron Verification

### 5.1 Expected cron firing

Cron schedule (verbatim from operator crontab per Phase A handoff § 2.6):
```
0 3 * * * SNS_TOPIC_ARN=arn:aws:sns:us-east-1:584812014683:equine-equalizer-alerts AWS_DEFAULT_REGION=us-east-1 PATH=...:/home/strakajagr/equibase_scraper/venv/bin /home/strakajagr/equibase_scraper/run_daily_refresh.sh >> /home/strakajagr/equibase_scraper/logs/cron.log 2>&1
```

Next firing: **2026-05-13 03:00 EDT / 07:00 UTC**.

### 5.2 SNS notification expected behavior

`run_daily_refresh.sh:175-181` publishes SNS only on `final_exit != 0`. If charts step succeeds (exit=0) AND workouts succeeds AND sync succeeds AND lambdas succeed → `final_exit=0` → **no SNS notification fires**. Operator confirms success via:

```bash
# Check today's status.json after 07:01 UTC (i.e. after 03:01 EDT)
cat /home/strakajagr/equibase_scraper/logs/$(date +%Y%m%d)/status.json | jq .
```

Expected: `"final_exit_code": 0`, `"steps": {"charts": {"exit": 0, "new_pdfs": N}, ...}` where `N` may be 0 (if no new races since the May 12 backfill) or > 0 (if May 12 race-day data published overnight).

### 5.3 Session_dead recurrence on first post-bridge cron

If next-day cron's charts.log shows `RuntimeError: warmup_check failed in --unattended mode — session dead or CAPTCHA needed`:

- **Session was invalidated within < 20 hours of operator save.** This indicates Imperva session lifetime is shorter than the cron interval — bridge is unstable.
- **Halt + surface** to QB for Path 2 acceleration (operator-action-required-daily is not a viable steady-state).
- Operationally: noted per E1 Step 1 diagnostic context, the Apr 30 timeline (00:16 EDT save → 03:00 EDT cron failure ≈ 3-hour invalidation window) already suggests this is the likely outcome. The bridge is a one-shot recovery; Path 2 needed for durable operation.

### 5.4 7-day observation window

If next-day cron succeeds: track for 7 consecutive daily SNS notifications (or absence-of-notification when exit=0). Each day operator inspects `logs/{YYYYMMDD}/status.json` to confirm `charts.exit=0`. Step 3 of dispatch handles this observation; runbook here only documents what to look for.

---

## Section 6 — Troubleshooting Addenda

### 6.1 Browser window opens but does not navigate

Symptom: Chromium window opens, but page is blank or shows network error after 30-second timeout.

Substrate reference: `download_charts.py:294-298` uses `wait_until="domcontentloaded", timeout=30_000`. If timeout fires, exception is caught at `:312-313` and printed as `[DIAG open_fresh_page] EXCEPTION during goto/sleep`.

First response:
1. Check Playwright Chromium install: `playwright install chromium` (from inside `venv`)
2. Check the URL is reachable from the laptop: `curl -I https://www.equibase.com/premium/pubPDFChartIndex.cfm` should return HTTP headers
3. Check no corporate firewall / proxy is blocking the request

### 6.2 CAPTCHA challenge unsolvable

Symptom: After pressing ENTER at the prompt, warmup_check loops back with `session_dead` repeatedly. Or browser shows a challenge that is not solvable (e.g. Imperva served a hard-block "Access Denied" page with no challenge to solve).

Substrate reference: `download_charts.py:317-333` retry loop.

First response:
1. Wait 10-15 minutes; Imperva sometimes lifts soft-block after a delay
2. Switch IP if possible (mobile hotspot fallback; different network)
3. Halt + surface for QB synthesis — likely Path 2 acceleration is needed if Imperva is hard-blocking this IP entirely

### 6.3 Scraper hangs > 5 minutes on warmup

Symptom: After pressing ENTER, no further stdout for > 5 minutes. Browser window may show partially loaded page.

First response:
1. Inspect browser window — Imperva may have served an unsolved interactive challenge (slider puzzle, click-and-hold, etc.) that wasn't visible at first ENTER press
2. If challenge visible, solve it; warmup will continue
3. If browser is unresponsive: `Ctrl-C` to kill scraper; restart from Section 2

### 6.4 Browser closes mid-iteration

Symptom: Browser window closes before final summary prints; scraper exits with non-zero code.

First response:
1. Check stdout for last error message
2. If Playwright TargetClosedError or similar: re-run Section 2; session_state may still be valid (saved after warmup-pass at `:320-321`), so warmup should pass on retry without operator re-solving CAPTCHA

### 6.5 Final summary shows Errors > 0

Symptom: `Errors: N` line in final summary shows non-zero count.

First response:
1. Errors per `download_charts.py:481-488` are non-fatal — counted and iteration continues
2. Inspect terminal output for `  ✗ {TRACK} {DATE} (retry failed: {STATUS})` lines (`:457-464`)
3. Acceptance criterion: if Errors < 10% of total combos AND new PDFs ≥ 30 per § 4.3, bridge succeeded; if Errors > 30%, surface for sub-investigation

---

## Backfill Scope Quantification

### Failure window

- Race-dates in gap: 2026-04-30 → 2026-05-12 inclusive = **13 race-dates**.
- Apr 30 already exhausted in `download_log.txt` as 11 NR entries (one per qualifying track); scraper will skip via `is_done()` at `download_charts.py:397`.
- Actual backfill iteration: May 1 → May 12 = **12 race-dates** producing new PDFs.

### Expected chart-PDF count matrix

S3 `s3://equine-raw-data/charts/` per-race-date cardinality distribution for pre-failure period (substrate from E1 Step 1):

| Race-date sample | PDFs in S3 |
|---|---|
| 2026-04-19 | 5 |
| 2026-04-22 | 1 |
| 2026-04-23 | 4 |
| 2026-04-24 | 5 |
| 2026-04-25 | 5 |
| 2026-04-26 | 5 |
| 2026-04-28 | 1 (partial; interactive truncated) |
| 2026-04-29 | 1 (partial; interactive truncated) |

Pre-failure typical: **3-5 PDFs per race-date** (Saturday-heavy distribution; weekday racing is lower).

12 race-dates × 3-5 PDFs = **36-60 expected new PDFs** for the backfill.

### Per-track distribution (substrate from `download_log.txt` aggregate PDF_ counts)

| Track | Total PDFs in scraper history |
|---|---|
| GP | 603 |
| AQU | 432 |
| SA | 376 |
| CD | 300 |
| OP | 282 |
| MTH | 196 |
| SAR | 152 |
| KEE | 145 |
| DMR | 135 |
| BEL | 84 |
| PIM | 50 |

Skewed distribution: GP / AQU / SA dominate; BEL / PIM tail. Current-season active tracks (per the May 2026 window) likely: CD (post-Derby Spring meet), GP (year-round), AQU (Belmont-meet relocated to Aqueduct per HRN `belmont-at-aqueduct` slug — see `data_pipeline_bible:4.4` D6 patch), SA (Spring meet), KEE (Spring meet through April; meet may have closed early May), MTH (opens May), PIM (Preakness week mid-May). Expected backfill PDFs concentrated in CD / GP / AQU / SA / MTH for May 1-12.

### Acceptance threshold

**≥ 30 new PDFs landed in S3 with `LastModified >= 2026-05-12` AND `.session_state.json` mtime refreshed AND scraper exit=0 = bridge succeeded.**

Sub-30 PDF count is not necessarily failure — operator inspects `download_log.txt` for per-date NR vs PDF breakdown; if many days were genuine "no racing" days (e.g. Tuesday/Wednesday dark days at qualifying tracks), low PDF count is operationally correct.

---

## End-of-Runbook Summary

| Section | Operator action | CC observable signal |
|---|---|---|
| 1 | Pre-execution checks (5 commands) | Each returns expected output |
| 2 | One scraper invocation + CAPTCHA solve | Terminal stdout matches signal table § 3.2 |
| 3 | Monitor terminal during ~5-15 min run | Per-PDF success lines accumulate |
| 4 | Post-execution verification (6 commands) | Exit code 0 + ≥ 30 new PDFs + S3 sync upload-lines |
| 5 | Next-day cron verification (2026-05-13 07:00 UTC) | `status.json.charts.exit=0` OR SNS notification with session_dead recurrence (halt) |
| 6 | Troubleshooting (referenced only if abnormal signal observed) | Per-signal first-response actions |

**Bridge success criteria summary:**

1. ✅ Scraper exit=0
2. ✅ `.session_state.json` mtime refreshed (current timestamp, not 2026-04-30)
3. ✅ ≥ 30 new PDFs in S3 with `LastModified >= 2026-05-12`
4. ✅ Spot-check race-dates 2026-05-02 + 2026-05-08 have ≥ 1 PDF each in S3
5. ✅ Next-day cron (2026-05-13 07:00 UTC) reports `charts.exit=0` in `status.json`

If all 5 criteria met: bridge stable; Step 3 7-day observation begins.
If criteria 1-4 met but criterion 5 fails: bridge one-shot succeeded but Imperva session lifetime < cron-interval; Path 2 acceleration required.
If any of criteria 1-4 fails: halt at Section 4 + surface for sub-investigation.
