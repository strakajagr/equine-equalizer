"""
Equibase Imperva Probe — v4 (A1: playwright-stealth).

Same network/wait pattern as v3, but with playwright-stealth applied to mask
common headless tells (navigator.webdriver, missing plugins, permissions API
shape, etc.).

Three URLs:
  - GP chart 2026-04-26 (the URL that returned CHALLENGE_STILL on v3)
  - BEL chart 2026-04-25 (Saturday Belmont — should have a real chart PDF)
  - BEL workout 2026-04-26 (Belmont workouts existed on NYRA same day)

For each: navigate with networkidle+3s wait, capture HTTP, body size, body
sample, cookies, and CRITICALLY for chart URLs: verify body starts with %PDF-.

Classification:
  PDF              — first 8 bytes start with %PDF-
  WORKOUT_HTML     — sizeable HTML with workout-table markers
  ERROR_404        — Equibase's "System Error / could not be located" stub
                     (past Imperva, no data on date+track)
  CHALLENGE_STILL  — Imperva "Pardon Our Interruption" challenge persisted
  UNKNOWN          — none of the above; needs human review

Reports navigator.webdriver value after stealth wrap.
"""
import asyncio
import json
from datetime import datetime, timezone

from playwright.async_api import async_playwright
from playwright_stealth import Stealth


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

URLS = [
    {
        "label": "GP chart 2026-04-26",
        "kind": "chart",
        "url": (
            "https://www.equibase.com/premium/eqbPDFChartPlus.cfm"
            "?RACE=A&BorP=P&TID=GP&CTRY=USA&DT=04/26/2026&DAY=D&STYLE=EQB"
        ),
    },
    {
        "label": "BEL chart 2026-04-25",
        "kind": "chart",
        "url": (
            "https://www.equibase.com/premium/eqbPDFChartPlus.cfm"
            "?RACE=A&BorP=P&TID=BEL&CTRY=USA&DT=04/25/2026&DAY=D&STYLE=EQB"
        ),
    },
    {
        "label": "BEL workout 2026-04-26",
        "kind": "workout",
        "url": (
            "https://www.equibase.com/workouts/work.cfm"
            "?track=BEL&raceDate=04/26/2026&cy=USA"
        ),
    },
]


def classify(http_status, title, body_bytes_or_text, content_type, kind):
    """Return classification string."""
    # Body might be bytes (chart) or string (HTML page from page.content())
    if isinstance(body_bytes_or_text, bytes):
        if body_bytes_or_text.startswith(b"%PDF-"):
            return "PDF"
        text_sample = body_bytes_or_text[:3000].decode("utf-8", errors="replace").lower()
    else:
        text_sample = (body_bytes_or_text or "")[:3000].lower()

    if "pardon our interruption" in text_sample:
        return "CHALLENGE_STILL"
    if "system error" in text_sample and "could not be located" in text_sample:
        return "ERROR_404"
    if "application/pdf" in (content_type or "").lower():
        return "PDF"
    if kind == "workout":
        if len(text_sample) > 5000 and ("workout" in text_sample or "<table" in text_sample):
            return "WORKOUT_HTML"
    if http_status in (403, 429, 503):
        return "BLOCK"
    return "UNKNOWN"


async def fetch_chart_via_browser(page, url):
    """For chart URLs, fetch raw bytes via in-browser fetch() so cookies+UA apply
    and we get the actual response body (PDF or HTML challenge)."""
    # Run the fetch from the current page origin (same-origin if we navigated to equibase first)
    result = await page.evaluate(
        f"""
        async () => {{
          try {{
            const r = await fetch({json.dumps(url)}, {{
              credentials: "include",
              headers: {{"Accept": "application/pdf,*/*"}}
            }});
            const ct = r.headers.get("content-type") || "";
            const buf = await r.arrayBuffer();
            const bytes = new Uint8Array(buf);
            // base64 of first 5000 bytes is plenty for fingerprinting
            const sample = btoa(String.fromCharCode(...bytes.slice(0, 5000)));
            return {{
              status: r.status,
              content_type: ct,
              size: buf.byteLength,
              sample_b64: sample
            }};
          }} catch(e) {{
            return {{ error: e.toString() }};
          }}
        }}
        """
    )
    return result


async def probe(target, page, ctx, kind):
    label = target["label"]
    url = target["url"]
    print(f"\n--- {label} ---", flush=True)
    print(f"URL: {url}", flush=True)

    t0 = datetime.now(timezone.utc)
    http_status = None
    body_bytes_or_text = b""
    content_type = ""
    final_url = None
    title = None
    nav_error = None

    try:
        if kind == "chart":
            # Make sure we're on an equibase.com origin so fetch() runs same-origin
            # (challenges set cookies on equibase.com domain)
            if "equibase.com" not in (page.url or ""):
                # Navigate to a benign Equibase URL to establish cookie scope.
                # Use the workout index as warmup — it's tiny and triggers Imperva once.
                try:
                    await page.goto(
                        "https://www.equibase.com/static/workout/index.html",
                        wait_until="networkidle",
                        timeout=60000,
                    )
                    await asyncio.sleep(3)
                except Exception:
                    pass

            result = await fetch_chart_via_browser(page, url)
            if "error" in result:
                nav_error = result["error"]
                print(f"  fetch error: {nav_error}", flush=True)
                cls = "UNKNOWN"
                http_status = None
                size = 0
                body_sample_text = ""
            else:
                import base64
                body_bytes = base64.b64decode(result["sample_b64"])
                http_status = result["status"]
                content_type = result["content_type"]
                size = result["size"]
                body_bytes_or_text = body_bytes
                cls = classify(http_status, None, body_bytes, content_type, kind)
                if cls == "PDF":
                    body_sample_text = f"(PDF; first 16 bytes: {body_bytes[:16]!r})"
                else:
                    body_sample_text = body_bytes[:500].decode("utf-8", errors="replace")
            final_url = page.url

        else:  # workout: page.goto, wait networkidle, read content
            response = await page.goto(url, wait_until="networkidle", timeout=60000)
            if response:
                http_status = response.status
                try:
                    headers = await response.all_headers()
                    content_type = headers.get("content-type", "")
                except Exception:
                    pass
            await asyncio.sleep(3)
            final_url = page.url
            try:
                title = await page.title()
            except Exception:
                title = "<no-title>"
            body_text = await page.content()
            body_bytes_or_text = body_text
            size = len(body_text)
            cls = classify(http_status, title, body_text, content_type, kind)
            body_sample_text = body_text[:500]

    except Exception as e:
        nav_error = str(e)
        cls = "UNKNOWN"
        http_status = None
        size = 0
        body_sample_text = ""

    cookies = await ctx.cookies()
    imperva_cookies = [c["name"] for c in cookies if c["name"].startswith(("incap_", "visid_incap", "reese", "rbzid", "nlbi"))]
    elapsed = (datetime.now(timezone.utc) - t0).total_seconds()

    print(f"  HTTP {http_status}  size={size}B  ct={content_type}  elapsed={elapsed:.2f}s", flush=True)
    print(f"  classification: {cls}", flush=True)
    print(f"  final_url: {final_url}", flush=True)
    if title is not None:
        print(f"  title: {title!r}", flush=True)
    print(f"  imperva cookies: {imperva_cookies}", flush=True)
    print(f"  body sample (first 500): {body_sample_text[:500]}", flush=True)

    return {
        "label": label,
        "url": url,
        "kind": kind,
        "http_status": http_status,
        "size_bytes": size,
        "content_type": content_type,
        "elapsed_s": round(elapsed, 2),
        "classification": cls,
        "imperva_cookies": imperva_cookies,
        "title": title,
        "nav_error": nav_error,
    }


async def main():
    print(f"\n{'='*60}", flush=True)
    print(f"PROBE v4 (A1: playwright-stealth) @ {datetime.now(timezone.utc).isoformat()}", flush=True)
    print(f"{'='*60}", flush=True)

    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent=USER_AGENT,
        )
        page = await ctx.new_page()

        # Verify stealth applied
        try:
            wd = await page.evaluate("navigator.webdriver")
            print(f"navigator.webdriver: {wd!r}  (should be False or undefined under stealth)", flush=True)
        except Exception as e:
            print(f"navigator.webdriver eval failed: {e}", flush=True)

        try:
            plugin_count = await page.evaluate("navigator.plugins.length")
            print(f"navigator.plugins.length: {plugin_count}  (real Chrome typically 3-5)", flush=True)
        except Exception:
            pass

        try:
            languages = await page.evaluate("JSON.stringify(navigator.languages)")
            print(f"navigator.languages: {languages}", flush=True)
        except Exception:
            pass

        results = []
        for target in URLS:
            r = await probe(target, page, ctx, target["kind"])
            results.append(r)
            await asyncio.sleep(2)

        await browser.close()

    print(f"\n{'='*60}", flush=True)
    print(f"SUMMARY", flush=True)
    print(f"{'='*60}", flush=True)
    classes = [r["classification"] for r in results]
    print(f"  classifications: {classes}", flush=True)

    # Verdict
    chart_classes = [r["classification"] for r in results if r["kind"] == "chart"]
    workout_classes = [r["classification"] for r in results if r["kind"] == "workout"]

    chart_pdf_count = sum(1 for c in chart_classes if c == "PDF")
    chart_total = len(chart_classes)
    workout_real = sum(1 for c in workout_classes if c == "WORKOUT_HTML")
    any_challenge = any(c == "CHALLENGE_STILL" for c in classes)
    any_block = any(c == "BLOCK" for c in classes)

    if any_block:
        verdict = "A1_FAILED — hard block(s) seen"
    elif chart_pdf_count == chart_total and not any_challenge:
        verdict = "A1_VIABLE — all chart URLs returned real PDFs, no Imperva challenge"
    elif chart_pdf_count == 0 and any_challenge:
        verdict = "A1_FAILED — chart URLs still return Imperva challenge under stealth"
    elif 0 < chart_pdf_count < chart_total:
        verdict = "A1_PARTIAL — some chart URLs delivered PDFs, others did not"
    else:
        verdict = "A1_PARTIAL — review per-URL results"

    print(f"\nVERDICT: {verdict}", flush=True)
    print(f"\n=== full results JSON ===", flush=True)
    print(json.dumps(results, indent=2, default=str), flush=True)


if __name__ == "__main__":
    asyncio.run(main())
