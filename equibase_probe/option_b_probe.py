"""
Option B probe — 2Captcha Imperva endpoint test.

Goal: determine whether 2Captcha can solve Equibase's Imperva challenge AND
whether the returned tokens are usable from a different IP (i.e., from our
Fargate IP). If yes, Option B is viable. If no, IP-binding kills B and we'd
need Option D (residential proxy).

Steps:
  1. Read 2Captcha API key from Secrets Manager (never log the value)
  2. Check balance — proves the key works and we have funds
  3. Submit Imperva task to 2Captcha's in.php
  4. Poll res.php every 5s until solution returned (typical 30-60s)
  5. Use returned token(s) as cookies in plain requests.get() to GP chart URL
  6. Check whether response is PDF (success) or Imperva challenge (token IP-bound)
  7. Report 2Captcha cost (1 solve), classification, and recommendation

Caveats logged but not abandoned: 2Captcha's exact request shape for Imperva
varies by Imperva variant. We try the documented "imperva" method first; if
that returns ERROR_CAPTCHA_UNSOLVABLE we'll learn the variant isn't supported.
"""
import json
import os
import sys
import time
from datetime import datetime, timezone

import boto3
import requests

SECRET_ID = "equine-equalizer/2captcha-api-key"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

TARGET_URLS = [
    {
        "label": "GP chart 2026-04-26",
        "url": (
            "https://www.equibase.com/premium/eqbPDFChartPlus.cfm"
            "?RACE=A&BorP=P&TID=GP&CTRY=USA&DT=04/26/2026&DAY=D&STYLE=EQB"
        ),
    },
]


def get_api_key():
    """Pull 2Captcha API key from Secrets Manager. Never returned to logs."""
    sm = boto3.client("secretsmanager", region_name="us-east-1")
    secret = sm.get_secret_value(SecretId=SECRET_ID)["SecretString"].strip()
    return secret


def check_balance(api_key):
    """Verify the key works and we have funds."""
    r = requests.get(
        "https://2captcha.com/res.php",
        params={"key": api_key, "action": "getbalance", "json": 1},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    if data.get("status") != 1:
        raise RuntimeError(f"2Captcha balance error: {data}")
    return float(data.get("request", 0))


def solve_imperva(api_key, page_url):
    """Submit Imperva task, poll for solution.

    2Captcha's Imperva method (documented at 2captcha.com/2captcha-api#imperva)
    expects: method=imperva, websiteUrl, userAgent, optionally sitekey.

    Returns the cookie/token bundle 2Captcha provides.
    """
    print(f"  submitting Imperva task to 2Captcha for {page_url}", flush=True)
    submit = requests.post(
        "https://2captcha.com/in.php",
        data={
            "key": api_key,
            "method": "imperva",
            "websiteUrl": page_url,
            "userAgent": USER_AGENT,
            "json": 1,
        },
        timeout=30,
    )
    submit.raise_for_status()
    sub = submit.json()
    if sub.get("status") != 1:
        raise RuntimeError(f"2Captcha submit failed: {sub}")
    task_id = sub["request"]
    print(f"  task_id={task_id}, polling for solution...", flush=True)

    deadline = time.time() + 180  # 3-minute polling window
    while time.time() < deadline:
        time.sleep(5)
        poll = requests.get(
            "https://2captcha.com/res.php",
            params={"key": api_key, "action": "get", "id": task_id, "json": 1},
            timeout=30,
        )
        poll.raise_for_status()
        data = poll.json()
        if data.get("status") == 1:
            print(f"  solution received after {int(time.time() - (deadline - 180))}s", flush=True)
            return data.get("request"), task_id
        request = data.get("request", "")
        if request == "CAPCHA_NOT_READY":
            continue
        # Any other non-success request is an error
        raise RuntimeError(f"2Captcha solve failed: {data}")
    raise RuntimeError("2Captcha solve timed out after 3 minutes")


def parse_solution(raw):
    """2Captcha's Imperva solution is typically a JSON string with cookies/tokens.

    Common shapes (from 2captcha docs):
      - dict with "cookies": [{name, value}, ...]
      - dict with "reese84": "...", "incap_ses_*": "...", etc.
      - or a raw token string

    We accept any of these and normalize to a {name: value} dict.
    """
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        # Try JSON parse
        try:
            obj = json.loads(raw)
            return obj
        except Exception:
            # Plain token string — caller can use as 'reese84' cookie
            return {"reese84": raw}
    return {}


def fetch_chart_with_tokens(url, tokens):
    """Use tokens as cookies in a plain requests.get(). Returns
    (http_status, content_type, size, body_first_500_b)."""
    cookies = {}
    if isinstance(tokens, dict):
        # Possibility 1: {"cookies": [{"name":..., "value":...}, ...]}
        if "cookies" in tokens and isinstance(tokens["cookies"], list):
            for c in tokens["cookies"]:
                if "name" in c and "value" in c:
                    cookies[c["name"]] = c["value"]
        # Possibility 2: top-level {name: value} mapping (filter to imperva-shaped names)
        for k, v in tokens.items():
            if k == "cookies":
                continue
            if isinstance(v, str) and (
                k.startswith(("incap_", "visid_incap", "reese", "rbzid", "nlbi"))
                or k == "reese84"
            ):
                cookies[k] = v

    if not cookies:
        return (None, "", 0, b"", "no cookies parsed from solution")

    r = requests.get(
        url,
        cookies=cookies,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/pdf,*/*",
            "Accept-Language": "en-US,en;q=0.9",
        },
        timeout=60,
        allow_redirects=True,
    )
    return (
        r.status_code,
        r.headers.get("content-type", ""),
        len(r.content),
        r.content[:500],
        None,
    )


def classify(body, ct):
    if not body:
        return "EMPTY"
    if body.startswith(b"%PDF-"):
        return "PDF"
    head = body[:2000].decode("utf-8", errors="replace").lower()
    if "pardon our interruption" in head:
        return "CHALLENGE_STILL"
    if "incapsula_resource" in head:
        return "CHALLENGE_IFRAME"
    if "system error" in head and "could not be located" in head:
        return "ERROR_404"
    return "UNKNOWN"


def main():
    print(f"\n{'='*60}", flush=True)
    print(f"OPTION B PROBE — 2Captcha Imperva @ {datetime.now(timezone.utc).isoformat()}", flush=True)
    print(f"{'='*60}", flush=True)

    api_key = get_api_key()
    print(f"  API key loaded (length={len(api_key)})", flush=True)

    # Step 1: balance check
    try:
        balance = check_balance(api_key)
        print(f"  2Captcha balance: ${balance:.4f}", flush=True)
        if balance < 0.05:
            print(f"  WARNING: balance below $0.05 — may not have funds for an Imperva solve (~$0.0029)", flush=True)
    except Exception as e:
        print(f"  BALANCE CHECK FAILED: {e}", flush=True)
        sys.exit(1)

    # Step 2: solve + retrieve cookies
    target = TARGET_URLS[0]
    try:
        raw, task_id = solve_imperva(api_key, target["url"])
        print(f"  raw solution preview: {str(raw)[:400]}", flush=True)
        tokens = parse_solution(raw)
        # Don't log full token values — print only key names
        print(f"  parsed token keys: {list(tokens.keys()) if isinstance(tokens, dict) else 'not-a-dict'}", flush=True)
    except Exception as e:
        print(f"  SOLVE FAILED: {e}", flush=True)
        # Final balance for cost accounting
        try:
            print(f"  final 2Captcha balance: ${check_balance(api_key):.4f}", flush=True)
        except Exception:
            pass
        sys.exit(0)  # not 1 — failure here is itself diagnostic data

    # Step 3: try the chart URL with the tokens
    print(f"\n  --- {target['label']} ---", flush=True)
    print(f"  URL: {target['url']}", flush=True)
    status, ct, size, body_first_500, err = fetch_chart_with_tokens(target["url"], tokens)
    if err:
        print(f"  FETCH ERROR: {err}", flush=True)
    else:
        cls = classify(body_first_500, ct)
        print(f"  HTTP {status}  size={size}  ct={ct}", flush=True)
        print(f"  classification: {cls}", flush=True)
        sample_text = body_first_500[:500].decode("utf-8", errors="replace") if cls != "PDF" else f"(PDF; first 16 bytes: {body_first_500[:16]!r})"
        print(f"  body sample: {sample_text}", flush=True)

    # Final balance — tells us how much one solve cost
    try:
        final_balance = check_balance(api_key)
        print(f"\n  final 2Captcha balance: ${final_balance:.4f}", flush=True)
        print(f"  (cost of this solve = starting - final, after refund window if any)", flush=True)
    except Exception:
        pass

    # Verdict
    print(f"\n{'='*60}", flush=True)
    print(f"VERDICT", flush=True)
    print(f"{'='*60}", flush=True)
    if not err and 'cls' in locals():
        if cls == "PDF":
            print(f"  OPTION_B_VIABLE — token from 2Captcha worked from Fargate IP. Build full fetcher.", flush=True)
        elif cls in ("CHALLENGE_STILL", "CHALLENGE_IFRAME"):
            print(f"  OPTION_B_IP_BOUND — token did not pass from Fargate IP. Imperva binds tokens to issuing IP.", flush=True)
            print(f"    Next step: Option D (residential proxy) or Option C (manual).", flush=True)
        elif cls == "ERROR_404":
            print(f"  PARTIAL — past Imperva but Equibase has no chart on that date+track. Pick a different test URL.", flush=True)
        else:
            print(f"  REVIEW — classification={cls}", flush=True)


if __name__ == "__main__":
    main()
