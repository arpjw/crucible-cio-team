#!/usr/bin/env python3
"""
FRED data health check.

Pulls all 20 core series and prints a status table:
  series ID | name | latest value | latest date | status

Status codes:
  OK     — fetched successfully, date within 7 days
  STALE  — fetched but date is more than 7 days old
  FAILED — could not fetch

Exits with code 1 if any series is FAILED.
"""

import os
import sys
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")

FRED_API_KEY = os.environ.get("FRED_API_KEY", "")
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

FRED_SERIES = {
    "FEDFUNDS":         "Fed Funds Rate",
    "DFEDTARU":         "Fed Funds Target Upper",
    "DFEDTARL":         "Fed Funds Target Lower",
    "DGS2":             "2Y Treasury Yield",
    "DGS10":            "10Y Treasury Yield",
    "DGS30":            "30Y Treasury Yield",
    "T10Y2Y":           "10Y-2Y Spread",
    "CPIAUCSL":         "CPI YoY",
    "PCEPILFE":         "Core PCE",
    "T10YIE":           "10Y Breakeven Inflation",
    "A191RL1Q225SBEA":  "Real GDP Growth",
    "UNRATE":           "Unemployment Rate",
    "ICSA":             "Initial Jobless Claims",
    "INDPRO":           "Industrial Production",
    "BAMLH0A0HYM2":     "HY Credit Spread",
    "BAMLC0A0CM":       "IG Credit Spread",
    "DTWEXBGS":         "Trade-Weighted USD",
    "UMCSENT":          "U Michigan Consumer Sentiment",
    "VIXCLS":           "VIX",
    "BOGMBASE":         "Monetary Base",
}

STALE_DAYS = 7


def fetch_series(series_id: str) -> tuple[float, str] | None:
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 10,
    }
    for attempt in range(3):
        try:
            r = requests.get(FRED_BASE_URL, params=params, timeout=20)
            if r.status_code == 429:
                wait = 2 ** attempt
                print(f"  [rate limit] {series_id} — retrying in {wait}s...")
                time.sleep(wait)
                continue
            r.raise_for_status()
            for obs in r.json().get("observations", []):
                val = obs.get("value", ".")
                if val != ".":
                    return float(val), obs["date"]
            return None
        except Exception:
            return None
    return None


def classify_status(date_str: str) -> str:
    try:
        obs_date = datetime.strptime(date_str, "%Y-%m-%d")
        return "OK" if (datetime.now() - obs_date).days <= STALE_DAYS else "STALE"
    except Exception:
        return "STALE"


def main() -> None:
    if not FRED_API_KEY:
        print("ERROR: FRED_API_KEY not set. Add it to .env or export it.")
        print("See infrastructure/data/fred-setup-guide.md for instructions.")
        sys.exit(1)

    print(f"\nFRED Health Check — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Pulling {len(FRED_SERIES)} series...\n")

    col_id    = 20
    col_name  = 34
    col_val   = 14
    col_date  = 12
    col_stat  = 8

    header = (
        f"{'Series ID':<{col_id}} "
        f"{'Name':<{col_name}} "
        f"{'Latest Value':>{col_val}} "
        f"{'Date':<{col_date}} "
        f"{'Status':<{col_stat}}"
    )
    print(header)
    print("─" * len(header))

    any_failed = False
    counts = {"OK": 0, "STALE": 0, "FAILED": 0}

    for sid, name in FRED_SERIES.items():
        result = fetch_series(sid)
        if result is None:
            status = "FAILED"
            val_str = "—"
            date_str = "—"
            any_failed = True
        else:
            val, date_str = result
            status = classify_status(date_str)
            val_str = f"{val:.4g}"

        counts[status] += 1
        status_display = f"[{status}]"
        print(
            f"{sid:<{col_id}} "
            f"{name:<{col_name}} "
            f"{val_str:>{col_val}} "
            f"{date_str:<{col_date}} "
            f"{status_display:<{col_stat}}"
        )

    print("─" * len(header))
    print(f"  OK: {counts['OK']}   STALE: {counts['STALE']}   FAILED: {counts['FAILED']}\n")

    if any_failed:
        print("RESULT: FAILED — one or more series could not be fetched.")
        sys.exit(1)
    elif counts["STALE"] > 0:
        print("RESULT: STALE — all series fetched but some data is older than 7 days.")
        print("  Monthly/quarterly series (GDP, CPI, PCE) are expected to be stale between releases.")
    else:
        print("RESULT: OK — all series fetched with recent data.")


if __name__ == "__main__":
    main()
