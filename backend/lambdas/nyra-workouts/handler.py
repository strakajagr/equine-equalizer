"""
NYRA Workout Scraper

Scrapes daily workouts from NYRA's free public pages for Saratoga, Belmont,
and Aqueduct, then writes a JSON batch to S3 and triggers
load_workouts_from_s3 in equine-ingestion to load into RDS.

Event payload (all optional):
    {"date": "YYYY-MM-DD"}    # default = today UTC
    {"tracks": ["BEL", "SAR"]} # default = all 3
    {"trigger_load": false}    # default = true

Returns: dict with per-track scrape counts, S3 key, and load Lambda response.
"""
import json
import logging
import os
import re
from datetime import date, datetime, timezone
from urllib.parse import urlparse, parse_qs

import boto3
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_BUCKET = os.environ.get("RAW_DATA_BUCKET", "equine-raw-data")
S3_PREFIX = "workout-loads"
INGESTION_LAMBDA = os.environ.get("INGESTION_LAMBDA", "equine-ingestion")

NYRA_TRACKS = {
    "SAR": "saratoga",
    "BEL": "belmont",
    "AQU": "aqueduct",
}

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Sanity gates against error / rate-limit / stub pages
MIN_PAGE_BYTES = 3000
REQUIRED_MARKERS = ["nyra", "workouts"]

# Regex compiled once
_FURLONG_RE = re.compile(
    r"^(\d+(?:\.\d+)?)\s+Furlongs?\s*[•·]\s*(\w+)\s+training\s*[•·]\s*(\w+)\s*$",
    re.IGNORECASE,
)
_HEADER_DATE_RE = re.compile(
    r"((?:January|February|March|April|May|June|July|"
    r"August|September|October|November|December)\s+\d+,\s+\d{4})"
    r"\s*-\s*(\d+)\s+workouts",
    re.IGNORECASE,
)
_REFNO_RE = re.compile(r"refno=(\d+)")
_STATE_SUFFIX_RE = re.compile(r"\s*\([A-Z]{2,3}\)\s*$")
_RANK_RE = re.compile(r"^(\d+)\s*/\s*(\d+)$")
_TIME_RE = re.compile(r"^(\d+):?(\d*)\.(\d+)$")


def _parse_time(raw):
    """Parse '39.95' or '1:02.40' into decimal seconds. Returns float or None."""
    raw = (raw or "").strip()
    if not raw:
        return None
    m = _TIME_RE.match(raw)
    if not m:
        return None
    minutes_or_secs, secs_part, frac = m.groups()
    if secs_part:
        # mm:ss.ff
        return float(minutes_or_secs) * 60 + float(f"{secs_part}.{frac}")
    # ss.ff
    return float(f"{minutes_or_secs}.{frac}")


def _clean_horse_name(raw):
    """Strip trailing ' (STATE)' suffix."""
    return _STATE_SUFFIX_RE.sub("", raw).strip()


def _is_unnamed(raw):
    return raw.strip().lower().startswith("unnamed")


def _find_preceding_furlong_heading(soup, table):
    """Walk back through string nodes preceding a table to find
    'N Furlongs • Surface training • Condition'. Returns
    (distance_furlongs:float, surface:str, condition:str) or (None, None, None).
    """
    for prev in table.find_all_previous(string=True, limit=400):
        s = prev.strip() if hasattr(prev, "strip") else str(prev).strip()
        if not s:
            continue
        # Compress internal whitespace in the bullet-separated heading
        compact = re.sub(r"\s+", " ", s)
        m = _FURLONG_RE.match(compact)
        if m:
            return float(m.group(1)), m.group(2).lower(), m.group(3).lower()
    return None, None, None


def _parse_active_date(soup, fallback):
    """Look for the prominent date header on the page. Returns ISO date string."""
    for hdr in soup.find_all(["header", "h1", "h2"]):
        m = _HEADER_DATE_RE.search(hdr.get_text(" ", strip=True))
        if m:
            try:
                return datetime.strptime(m.group(1), "%B %d, %Y").date().isoformat()
            except ValueError:
                continue
    return fallback


def _validate_page(html, track_code):
    """Bail loudly on error stub / rate-limit / structural change."""
    if len(html) < MIN_PAGE_BYTES:
        raise RuntimeError(
            f"NYRA {track_code}: page is {len(html)} bytes "
            f"(min {MIN_PAGE_BYTES}); likely error stub or rate-limit"
        )
    lowered = html.lower()
    for marker in REQUIRED_MARKERS:
        if marker not in lowered:
            raise RuntimeError(
                f"NYRA {track_code}: page missing structural marker '{marker}'"
            )


def fetch_track_page(track_slug, target_date_iso):
    """Fetch a NYRA workouts page for one track + date.
    Returns the raw HTML. Raises on error/empty/structurally-broken response.
    """
    url = f"https://www.nyra.com/{track_slug}/racing/workouts/?detail={target_date_iso}"
    resp = requests.get(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "text/html,*/*;q=0.8"},
        timeout=30,
    )
    resp.raise_for_status()
    return url, resp.text


def parse_nyra_html(html, track_code, target_date_iso):
    """Parse a NYRA workouts page into a list of workout-load JSON dicts.

    Returns list of dicts in load_workouts_from_s3 format.
    Skips Unnamed-foal rows and rows that fail to parse.
    """
    soup = BeautifulSoup(html, "html.parser")
    active_date = _parse_active_date(soup, fallback=target_date_iso)

    workouts = []
    skipped_unnamed = 0
    skipped_parse = 0

    tables = soup.find_all(
        "table",
        class_=lambda c: c and "w-full" in c and "text-sm" in c,
    )

    for table in tables:
        distance, surface, condition = _find_preceding_furlong_heading(soup, table)
        if distance is None:
            continue

        tbody = table.find("tbody")
        if not tbody:
            continue

        for tr in tbody.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) < 6:
                continue

            try:
                horse_cell = tds[0]
                horse_raw = horse_cell.get_text(" ", strip=True)

                if _is_unnamed(horse_raw):
                    skipped_unnamed += 1
                    continue

                horse_name = _clean_horse_name(horse_raw)
                if not horse_name:
                    skipped_parse += 1
                    continue

                # Extract Equibase refno from horse profile link if present
                eq_refno = None
                anchor = horse_cell.find("a", href=True)
                if anchor:
                    m = _REFNO_RE.search(anchor["href"])
                    if m:
                        eq_refno = m.group(1)

                age_raw = tds[1].get_text(strip=True)
                sex = tds[2].get_text(strip=True) or None
                workout_type = tds[3].get_text(strip=True) or None
                time_raw = tds[4].get_text(strip=True)
                rank_raw = tds[5].get_text(strip=True)

                workout_time = _parse_time(time_raw)
                if workout_time is None:
                    skipped_parse += 1
                    continue

                rank_match = _RANK_RE.match(rank_raw)
                if not rank_match:
                    skipped_parse += 1
                    continue
                rank_on_day = int(rank_match.group(1))
                total_works_on_day = int(rank_match.group(2))

                workouts.append({
                    "horse_name": horse_name,
                    "eq_refno": eq_refno,
                    "sex": sex,
                    "workout_date": active_date,
                    "track_code": track_code,
                    "distance_furlongs": distance,
                    "workout_time": round(workout_time, 2),
                    "is_bullet": rank_on_day == 1,
                    "track_condition": condition,
                    "workout_type": workout_type,
                    "rank_on_day": rank_on_day,
                    "total_works_on_day": total_works_on_day,
                })
            except Exception as e:
                logger.warning(
                    f"NYRA {track_code} row parse failed: {e}; row text: "
                    f"{tr.get_text(' | ', strip=True)[:120]}"
                )
                skipped_parse += 1
                continue

    return workouts, {
        "tables": len(tables),
        "skipped_unnamed": skipped_unnamed,
        "skipped_parse": skipped_parse,
    }


def handler(event, context):
    target_date = event.get("date") or date.today().isoformat()
    requested_tracks = event.get("tracks") or list(NYRA_TRACKS.keys())
    trigger_load = event.get("trigger_load", True)

    logger.info(
        f"NYRA workout scrape: date={target_date} tracks={requested_tracks} "
        f"trigger_load={trigger_load}"
    )

    s3 = boto3.client("s3")
    lam = boto3.client("lambda")

    all_workouts = []
    per_track = {}
    errors = []

    for track_code in requested_tracks:
        if track_code not in NYRA_TRACKS:
            errors.append(f"Unknown NYRA track code: {track_code}")
            continue

        slug = NYRA_TRACKS[track_code]
        try:
            url, html = fetch_track_page(slug, target_date)
            _validate_page(html, track_code)
            workouts, stats = parse_nyra_html(html, track_code, target_date)
            all_workouts.extend(workouts)
            per_track[track_code] = {
                "url": url,
                "found": len(workouts),
                **stats,
            }
            logger.info(
                f"NYRA {track_code}: {len(workouts)} workouts ({stats})"
            )
        except Exception as e:
            err = f"NYRA {track_code} failed: {e}"
            logger.error(err)
            errors.append(err)
            per_track[track_code] = {"error": str(e)}

    # If every track failed, fail the Lambda — likely structural change
    if not per_track or all(t.get("error") for t in per_track.values()):
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "All tracks failed to scrape",
                "per_track": per_track,
                "errors": errors,
            }),
        }

    if not all_workouts:
        logger.info("NYRA: scraped zero workouts across all tracks; skipping S3 upload + load")
        return {
            "statusCode": 200,
            "body": json.dumps({
                "date": target_date,
                "per_track": per_track,
                "total_workouts": 0,
                "s3_key": None,
                "load_response": None,
                "errors": errors,
            }),
        }

    # Upload to S3 — fail loudly on error (no silent failure)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    date_str = target_date.replace("-", "")
    s3_key = f"{S3_PREFIX}/{date_str}_nyra_{timestamp}.json"

    s3.put_object(
        Bucket=S3_BUCKET,
        Key=s3_key,
        Body=json.dumps(all_workouts).encode("utf-8"),
        ContentType="application/json",
    )
    logger.info(f"Uploaded {len(all_workouts)} workouts to s3://{S3_BUCKET}/{s3_key}")

    # Trigger load
    load_response = None
    if trigger_load:
        try:
            invoke = lam.invoke(
                FunctionName=INGESTION_LAMBDA,
                InvocationType="RequestResponse",
                Payload=json.dumps({
                    "action": "load_workouts_from_s3",
                    "s3_key": s3_key,
                }).encode("utf-8"),
            )
            payload = invoke["Payload"].read().decode("utf-8")
            load_response = json.loads(payload) if payload else None
            logger.info(f"load_workouts_from_s3 response: {load_response}")
        except Exception as e:
            logger.error(f"Failed to invoke load Lambda: {e}")
            errors.append(f"load invoke failed: {e}")
            # Don't fail — data is in S3, can be re-loaded manually

    return {
        "statusCode": 200,
        "body": json.dumps({
            "date": target_date,
            "per_track": per_track,
            "total_workouts": len(all_workouts),
            "s3_key": s3_key,
            "load_response": load_response,
            "errors": errors,
        }),
    }
