"""
Option D probe — Bright Data Web Unlocker.

Goal: confirm Bright Data Web Unlocker can deliver real Equibase content
(chart PDFs, workout HTML) given a target URL, and report per-request billing
so we can verify the $1.50/1K rate.

Steps:
  1. Read Bright Data API key from Secrets Manager (never log the value)
  2. Read zone name from env var BRIGHTDATA_ZONE (default 'web_unlocker1')
  3. For each of 3 test URLs, POST to api.brightdata.com/request
     - GP chart 4/26   — should return PDF bytes (Imperva-protected real data)
     - GP workout 4/26 — should return real workout HTML or genuine 404
     - SAR chart 4/26  — Saratoga inactive; Equibase returns 404. Verify
                          Bright Data passes the 404 through cleanly
  4. Capture HTTP status, response headers (esp. x-brd-* billing/cost),
     content-type, body size, body first 500 bytes
  5. Classify: PDF / WORKOUT_HTML / CLEAN_404 / IMPERVA_CHALLENGE / WRAPPED_ERROR
  6. Verdict: D-VIABLE / D-PARTIAL / D-FAILED

Cost ceiling: 3 successful unlocks × $0.0015 = $0.0045. PAYG.
"""
import json
import os
import sys
from datetime import datetime, timezone

import boto3
import requests

SECRET_ID = "equine-equalizer/brightdata-api-key"
ZONE = os.environ.get("BRIGHTDATA_ZONE", "web_unlocker1")
API_ENDPOINT = "https://api.brightdata.com/request"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

TARGETS = [
    {
        "label": "GP chart 2026-04-26 (real data, Imperva-protected)",
        "kind": "chart",
        "url": (
            "https://www.equibase.com/premium/eqbPDFChartPlus.cfm"
            "?RACE=A&BorP=P&TID=GP&CTRY=USA&DT=04/26/2026&DAY=D&STYLE=EQB"
        ),
        "expect": "PDF",
    },
    {
        "label": "GP workout 2026-04-26 (no-data; expect 404)",
        "kind": "workout",
        "url": (
            "https://www.equibase.com/workouts/work.cfm"
            "?track=GP&raceDate=04/26/2026&cy=USA"
        ),
        "expect": "CLEAN_404",
    },
    {
        "label": "SAR chart 2026-04-26 (no-data; expect 404 redirect to static-CDN)",
        "kind": "chart",
        "url": (
            "https://www.equibase.com/premium/eqbPDFChartPlus.cfm"
            "?RACE=A&BorP=P&TID=SAR&CTRY=USA&DT=04/26/2026&DAY=D&STYLE=EQB"
        ),
        "expect": "CLEAN_404",
    },
]


def get_api_key():
    sm = boto3.client("secretsmanager", region_name="us-east-1")
    secret = sm.get_secret_value(SecretId=SECRET_ID)["SecretString"].strip()
    return secret


def classify(body, content_type, http_status):
    """Classify response body."""
    if not body:
        return "EMPTY"
    if isinstance(body, str):
        body = body.encode("utf-8", errors="replace")
    if body.startswith(b"%PDF-"):
        return "PDF"
    head = body[:3000].decode("utf-8", errors="replace").lower()
    if "pardon our interruption" in head:
        return "IMPERVA_CHALLENGE"
    if "_incapsula_resource" in head:
        return "IMPERVA_CHALLENGE"
    if "system error" in head and "could not be located" in head:
        return "CLEAN_404"
    if http_status in (403, 429, 503):
        return "WRAPPED_ERROR"
    # Workout-shaped HTML detection
    if (
        "<table" in head
        and ("workout" in head or "fractional" in head or "breeze" in head)
    ):
        return "WORKOUT_HTML"
    # Plain Equibase HTML (workout page is real but might have no table when track is dark)
    if len(body) > 1500 and "<html" in head and "equibase" in head:
        return "EQUIBASE_HTML_OTHER"
    if "404" in head and ("not found" in head or "<title>" in head):
        return "CLEAN_404"
    return "UNKNOWN"


def fetch_via_brightdata(api_key, target_url):
    """POST to Bright Data Web Unlocker, return (resp, elapsed_s)."""
    t0 = datetime.now(timezone.utc)
    payload = {
        "zone": ZONE,
        "url": target_url,
        "format": "raw",
        # Optional fields per Bright Data docs that may matter for the response shape:
        "method": "GET",
        "country": "us",
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    resp = requests.post(
        API_ENDPOINT,
        headers=headers,
        data=json.dumps(payload),
        timeout=120,
    )
    elapsed = (datetime.now(timezone.utc) - t0).total_seconds()
    return resp, elapsed


def main():
    print(f"\n{'='*60}", flush=True)
    print(f"OPTION D PROBE — Bright Data Web Unlocker", flush=True)
    print(f"  start: {datetime.now(timezone.utc).isoformat()}", flush=True)
    print(f"  zone:  {ZONE}", flush=True)
    print(f"{'='*60}", flush=True)

    try:
        api_key = get_api_key()
        print(f"  API key loaded (length={len(api_key)})", flush=True)
    except Exception as e:
        print(f"  FATAL: could not load API key: {e}", flush=True)
        sys.exit(1)

    results = []
    for target in TARGETS:
        print(f"\n--- {target['label']} ---", flush=True)
        print(f"URL: {target['url']}", flush=True)
        print(f"expected classification: {target['expect']}", flush=True)
        try:
            resp, elapsed = fetch_via_brightdata(api_key, target["url"])
        except Exception as e:
            print(f"  REQUEST EXCEPTION: {e}", flush=True)
            results.append({
                "label": target["label"],
                "url": target["url"],
                "exception": str(e),
            })
            continue

        # Capture all x-brd-* and other Bright-Data-specific headers for billing analysis
        brd_headers = {
            k: v for k, v in resp.headers.items()
            if k.lower().startswith(("x-brd", "x-luminati", "x-brightdata"))
        }
        # Also capture any header that looks like cost/billing
        cost_headers = {
            k: v for k, v in resp.headers.items()
            if any(t in k.lower() for t in ("cost", "billed", "bandwidth", "credits"))
        }

        body = resp.content
        size = len(body)
        ct = resp.headers.get("Content-Type", "")
        cls = classify(body, ct, resp.status_code)

        print(f"  HTTP {resp.status_code}  size={size}B  ct={ct}  elapsed={elapsed:.2f}s", flush=True)
        print(f"  classification: {cls}  (expected {target['expect']})", flush=True)
        if brd_headers:
            print(f"  Bright Data headers: {brd_headers}", flush=True)
        if cost_headers:
            print(f"  cost/billing headers: {cost_headers}", flush=True)
        # If body is small, print all of it; otherwise first 500
        if cls == "PDF":
            sample = f"(PDF; first 16 bytes: {body[:16]!r})"
        else:
            sample = body[:500].decode("utf-8", errors="replace")
        print(f"  body sample: {sample}", flush=True)

        results.append({
            "label": target["label"],
            "url": target["url"],
            "expect": target["expect"],
            "http_status": resp.status_code,
            "size_bytes": size,
            "content_type": ct,
            "elapsed_s": round(elapsed, 2),
            "classification": cls,
            "matched_expectation": cls == target["expect"]
                or (target["expect"] == "PDF" and cls == "PDF")
                or (target["expect"] == "CLEAN_404" and cls in ("CLEAN_404", "EQUIBASE_HTML_OTHER")),
            "brd_headers": brd_headers,
            "cost_headers": cost_headers,
        })

    # Verdict
    print(f"\n{'='*60}", flush=True)
    print(f"SUMMARY", flush=True)
    print(f"{'='*60}", flush=True)
    classes = [r.get("classification", "EXCEPTION") for r in results]
    matches = [r.get("matched_expectation", False) for r in results]
    print(f"  classifications: {classes}", flush=True)
    print(f"  matched expectation: {matches}", flush=True)

    pdf_results = [r for r in results if r.get("expect") == "PDF"]
    pdf_passed = all(r.get("classification") == "PDF" for r in pdf_results)

    no_data_results = [r for r in results if r.get("expect") == "CLEAN_404"]
    no_data_passed = all(
        r.get("classification") in ("CLEAN_404", "EQUIBASE_HTML_OTHER")
        for r in no_data_results
    )

    challenges = [r for r in results if r.get("classification") == "IMPERVA_CHALLENGE"]

    if challenges:
        verdict = "D-FAILED — Bright Data returned Imperva challenge for at least one URL"
    elif pdf_passed and no_data_passed:
        verdict = "D-VIABLE — all expected outcomes matched; build full fetcher"
    elif pdf_passed and not no_data_passed:
        verdict = "D-PARTIAL — PDFs delivered but no-data URLs returned unexpected shape"
    elif no_data_passed and not pdf_passed:
        verdict = "D-PARTIAL — no-data URLs passed through but real-data URLs did not deliver content"
    else:
        verdict = "D-FAILED — neither real-data nor no-data URLs returned expected content"

    print(f"\nVERDICT: {verdict}", flush=True)
    print(f"\n=== full results JSON ===", flush=True)
    print(json.dumps(results, indent=2, default=str), flush=True)


if __name__ == "__main__":
    main()
