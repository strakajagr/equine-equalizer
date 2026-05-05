"""
Option A2 probe — playwright-stealth + page.goto + route capture, no proxy.

Background: the laptop script (download_charts.py) was confirmed to deliver
real PDFs from Equibase using:
  - playwright-stealth wrap (Stealth().use_async(async_playwright()))
  - page.goto(pdf_url) as a top-level navigation request
  - page.route() to inject Content-Disposition for binary capture
The page.evaluate(fetch(...)) pattern (used by the original A1 probe and by
the laptop script before the fix) was rejected by Imperva on the chart-PDF
endpoint with a 4563-byte "Pardon Our Interruption" interstitial regardless
of session cookies.

The earlier Fargate probes were:
  - option B (plain Playwright + fetch from page) — failed
  - option D (Bright Data Web Unlocker)            — gambling-block from vendor

What was never tested: stealth wrap + goto pattern + plain Fargate public IP
(no proxy). That is this probe.

For each target URL we:
  1. Register page.route(url, handler) before navigation
  2. Issue page.goto(url, wait_until="commit", timeout=30s)
  3. In the route handler call route.fetch() (which preserves the navigation
     request shape) then read the response body, then route.abort() to
     prevent Chromium's PDF viewer / download path from getting involved.
  4. Classify the captured body: %PDF- / Imperva interstitial / 404 / unknown.

This isolates the question of whether Fargate's datacenter IP, with stealth,
under a navigation-shaped request, gets the same outcome as Tony's home
residential IP.

Run from a Fargate task with a public IP, no proxy, no Bright Data.
"""
import asyncio
import json
import sys
from datetime import datetime, timezone

from playwright.async_api import async_playwright
from playwright_stealth import Stealth


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Same warmup target as download_charts.py — chart index page, used to
# establish Imperva session cookies (visid_incap, incap_ses, reese84) on
# the .equibase.com domain before we hit the chart-PDF endpoint.
WARMUP_URL = (
    "https://www.equibase.com/premium/pubPDFChartIndex.cfm"
    "?TID=GP&CTRY=USA&DAY=D&DT=03/05/2023&STYLE=EQB&BorP=B&requesttimeout=60"
)

TARGETS = [
    {
        "label": "GP chart 2026-04-26 (real-data, Imperva-protected)",
        "url": (
            "https://www.equibase.com/premium/eqbPDFChartPlus.cfm"
            "?RACE=A&BorP=P&TID=GP&CTRY=USA&DT=04/26/2026&DAY=D&STYLE=EQB"
        ),
        "expect": "PDF",
    },
    {
        "label": "BEL chart 2026-04-25 (real-data Saturday, Imperva-protected)",
        "url": (
            "https://www.equibase.com/premium/eqbPDFChartPlus.cfm"
            "?RACE=A&BorP=P&TID=BEL&CTRY=USA&DT=04/25/2026&DAY=D&STYLE=EQB"
        ),
        "expect": "PDF",
    },
]


def classify(body, content_type, http_status):
    if not body:
        return "EMPTY"
    if isinstance(body, str):
        body = body.encode("utf-8", errors="replace")
    if body.startswith(b"%PDF-"):
        return "PDF"
    head = body[:5000].decode("utf-8", errors="replace").lower()
    if "pardon our interruption" in head or "_incapsula_resource" in head or "imperva" in head:
        return "IMPERVA_CHALLENGE"
    if "system error" in head and "could not be located" in head:
        return "EQB_404"
    if http_status in (403,) and ("forbidden" in head or "access denied" in head):
        return "HARD_FORBIDDEN"
    if http_status in (429,):
        return "RATE_LIMITED"
    if http_status in (503,):
        return "SERVICE_UNAVAILABLE"
    return "UNKNOWN"


async def fetch_via_goto(page, url):
    """Issue page.goto(url) with a route handler that captures the response
    body before the browser can render/download it."""
    captured: dict = {}

    async def route_handler(route):
        try:
            resp = await route.fetch()
            captured["status"] = resp.status
            captured["headers"] = dict(resp.headers)
            captured["ct"] = resp.headers.get("content-type", "")
            captured["body"] = await resp.body()
        except Exception as e:
            captured["error"] = f"{type(e).__name__}: {e}"
        finally:
            try:
                # Abort so Chromium doesn't try to render the response —
                # we already have the bytes.
                await route.abort()
            except Exception:
                pass

    await page.route(url, route_handler)
    t0 = datetime.now(timezone.utc)
    try:
        await page.goto(url, wait_until="commit", timeout=30_000)
    except Exception as e:
        # ERR_ABORTED expected — we aborted in the route handler.
        captured.setdefault("goto_exception", f"{type(e).__name__}: {e}")
    elapsed = (datetime.now(timezone.utc) - t0).total_seconds()
    try:
        await page.unroute(url, route_handler)
    except Exception:
        pass
    captured["elapsed_s"] = round(elapsed, 2)
    return captured


async def main():
    print(f"\n{'='*60}", flush=True)
    print("OPTION A2 PROBE — stealth + goto + route, no proxy", flush=True)
    print(f"  start: {datetime.now(timezone.utc).isoformat()}", flush=True)
    print(f"{'='*60}", flush=True)

    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent=USER_AGENT,
            accept_downloads=True,
        )
        page = await ctx.new_page()

        # Stealth fingerprint sanity
        try:
            wd = await page.evaluate("navigator.webdriver")
            print(f"navigator.webdriver: {wd!r}  (should be False/undefined)", flush=True)
        except Exception as e:
            print(f"navigator.webdriver eval failed: {e}", flush=True)
        try:
            plugins = await page.evaluate("navigator.plugins.length")
            print(f"navigator.plugins.length: {plugins}", flush=True)
        except Exception:
            pass
        try:
            langs = await page.evaluate("JSON.stringify(navigator.languages)")
            print(f"navigator.languages: {langs}", flush=True)
        except Exception:
            pass

        # Warmup: navigate to chart index to establish Imperva session cookies.
        print(f"\n--- WARMUP: {WARMUP_URL} ---", flush=True)
        try:
            t0 = datetime.now(timezone.utc)
            resp = await page.goto(
                WARMUP_URL, wait_until="domcontentloaded", timeout=30_000
            )
            await asyncio.sleep(8)
            elapsed = (datetime.now(timezone.utc) - t0).total_seconds()
            try:
                title = await page.title()
            except Exception:
                title = "<no-title>"
            print(
                f"  warmup HTTP {resp.status if resp else 'None'}  "
                f"final_url={page.url!r}  title={title!r}  elapsed={elapsed:.2f}s",
                flush=True,
            )
            cookies = await ctx.cookies()
            imperva = [
                c["name"] for c in cookies
                if c["name"].startswith(("incap_", "visid_incap", "reese", "rbzid", "nlbi"))
            ]
            print(f"  imperva cookies after warmup: {imperva}", flush=True)
        except Exception as e:
            print(f"  WARMUP EXCEPTION: {type(e).__name__}: {e}", flush=True)
            cookies = []
            imperva = []

        # Probe each chart-PDF target
        results = []
        for target in TARGETS:
            print(f"\n--- {target['label']} ---", flush=True)
            print(f"URL: {target['url']}", flush=True)
            print(f"expect: {target['expect']}", flush=True)
            try:
                captured = await fetch_via_goto(page, target["url"])
            except Exception as e:
                print(f"  PROBE EXCEPTION: {type(e).__name__}: {e}", flush=True)
                results.append({
                    "label": target["label"],
                    "url": target["url"],
                    "expect": target["expect"],
                    "exception": f"{type(e).__name__}: {e}",
                })
                continue

            status = captured.get("status")
            ct = captured.get("ct", "")
            body = captured.get("body", b"")
            size = len(body) if body else 0
            cls = classify(body, ct, status)
            print(
                f"  HTTP {status}  size={size}B  ct={ct!r}  "
                f"elapsed={captured.get('elapsed_s')}s",
                flush=True,
            )
            print(f"  classification: {cls}  (expected {target['expect']})", flush=True)
            if "error" in captured:
                print(f"  route.fetch error: {captured['error']}", flush=True)
            if "goto_exception" in captured:
                print(f"  goto exception (expected for route.abort): {captured['goto_exception']}", flush=True)
            print(f"  response headers ({len(captured.get('headers') or {})}):", flush=True)
            for k, v in (captured.get("headers") or {}).items():
                print(f"    {k}: {v}", flush=True)
            if cls == "PDF":
                print(f"  body sample: PDF binary, first 16 bytes: {body[:16]!r}", flush=True)
            else:
                sample = body[:500].decode("utf-8", errors="replace") if body else ""
                print(f"  body sample (first 500): {sample}", flush=True)

            results.append({
                "label": target["label"],
                "url": target["url"],
                "expect": target["expect"],
                "http_status": status,
                "size_bytes": size,
                "content_type": ct,
                "elapsed_s": captured.get("elapsed_s"),
                "classification": cls,
                "matched_expectation": cls == target["expect"],
                "route_error": captured.get("error"),
            })

        await browser.close()

    print(f"\n{'='*60}", flush=True)
    print("SUMMARY", flush=True)
    print(f"{'='*60}", flush=True)
    classes = [r.get("classification", "EXCEPTION") for r in results]
    print(f"  classifications: {classes}", flush=True)

    pdf_count = sum(1 for c in classes if c == "PDF")
    challenge_count = sum(1 for c in classes if c == "IMPERVA_CHALLENGE")
    forbidden_count = sum(1 for c in classes if c == "HARD_FORBIDDEN")

    if pdf_count == len(classes) and pdf_count > 0:
        verdict = "A2_VIABLE — Fargate IP + stealth + goto delivers real PDFs; full automation feasible"
    elif challenge_count > 0 and pdf_count == 0:
        verdict = "A2_FAILED_IMPERVA — Imperva interstitial on Fargate IP under stealth+goto; residential IP required"
    elif forbidden_count > 0:
        verdict = "A2_FAILED_HARD_BLOCK — datacenter IP categorically blocked"
    elif pdf_count > 0:
        verdict = f"A2_PARTIAL — {pdf_count}/{len(classes)} delivered PDF; review per-URL results"
    else:
        verdict = "A2_INCONCLUSIVE — review per-URL classifications"

    print(f"\nVERDICT: {verdict}", flush=True)
    print("\n=== full results JSON ===", flush=True)
    print(json.dumps(results, indent=2, default=str), flush=True)


if __name__ == "__main__":
    asyncio.run(main())
