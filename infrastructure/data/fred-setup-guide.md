# FRED API Setup Guide

The Federal Reserve Bank of St. Louis FRED database is the primary source for macro regime data. Free, reliable, and updated daily. Crucible's `/macro`, `/macro-scanner`, and `/regime-classifier` agents ground their analysis in FRED series.

---

## 1. API Key Registration

1. Go to [fred.stlouisfed.org](https://fred.stlouisfed.org)
2. Create a free account
3. Navigate to **My Account → API Keys → Request API Key**
4. Fill in the application (purpose: "systematic macro research") — approved instantly
5. Copy your key and add it to `.env`:

```bash
FRED_API_KEY=your_key_here
```

Rate limit: 120 requests per minute. More than sufficient for daily pulls.

---

## 2. Core Macro Series

The 20 most important FRED series for a systematic macro CTA. These cover the four regime dimensions used by `/regime-classifier`: growth, inflation, liquidity, and risk appetite.

### Monetary Policy

| Series ID | Description | Frequency | Notes |
|-----------|-------------|-----------|-------|
| `FEDFUNDS` | Effective Federal Funds Rate | Monthly | Primary policy rate |
| `DFEDTARU` | Fed Funds Target Rate — Upper Bound | Daily | Forward-looking policy |
| `SOFR` | Secured Overnight Financing Rate | Daily | Replaced LIBOR as benchmark |

### Yield Curve

| Series ID | Description | Frequency | Notes |
|-----------|-------------|-----------|-------|
| `DGS10` | 10-Year Treasury Constant Maturity | Daily | Long-end benchmark |
| `DGS2` | 2-Year Treasury Constant Maturity | Daily | Short-end, policy sensitive |
| `DGS1MO` | 1-Month Treasury | Daily | Front-end cash rate |
| `T10Y2Y` | 10Y–2Y Spread | Daily | Yield curve slope — recession predictor |
| `T10YFF` | 10Y Treasury minus Fed Funds | Daily | Term premium proxy |

### Inflation

| Series ID | Description | Frequency | Notes |
|-----------|-------------|-----------|-------|
| `CPIAUCSL` | CPI All Urban Consumers | Monthly | Headline inflation, YoY |
| `PCEPILFE` | Core PCE Price Index | Monthly | Fed's preferred inflation measure |
| `T10YIE` | 10Y Breakeven Inflation Rate | Daily | Market-implied inflation expectations |
| `MICH` | University of Michigan Inflation Expectations | Monthly | Consumer survey, 1-year ahead |

### Growth

| Series ID | Description | Frequency | Notes |
|-----------|-------------|-----------|-------|
| `A191RL1Q225SBEA` | Real GDP Growth Rate | Quarterly | Official growth measure |
| `UNRATE` | Civilian Unemployment Rate | Monthly | Labor market health |
| `ICSA` | Initial Jobless Claims | Weekly | Leading labor indicator |
| `INDPRO` | Industrial Production Index | Monthly | Manufacturing/output proxy |

### Credit and Liquidity

| Series ID | Description | Frequency | Notes |
|-----------|-------------|-----------|-------|
| `BAMLH0A0HYM2` | ICE BofA HY OAS | Daily | High yield credit spreads — risk appetite |
| `BAMLC0A0CM` | ICE BofA IG OAS | Daily | Investment grade credit spreads |
| `DTWEXBGS` | Broad Dollar Index | Daily | USD strength — risk-off proxy |
| `VIXCLS` | CBOE VIX | Daily | Equity volatility — fear gauge |

---

## 3. Python Pull Function

```python
import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
FRED_API_KEY = os.environ["FRED_API_KEY"]
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"


def pull_fred_series(series_id: str, lookback_days: int = 365) -> pd.DataFrame:
    """Pull a FRED series into a pandas DataFrame."""
    start_date = (datetime.today() - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "sort_order": "desc",
    }
    resp = requests.get(FRED_BASE_URL, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()["observations"]
    df = pd.DataFrame(data)[["date", "value"]]
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"])
    df = df.dropna(subset=["value"]).set_index("date").sort_index()
    df.columns = [series_id]
    return df


def get_latest(series_id: str) -> float | None:
    """Return the most recent non-null value for a series."""
    df = pull_fred_series(series_id, lookback_days=90)
    return float(df.iloc[-1].values[0]) if not df.empty else None


# Example usage
if __name__ == "__main__":
    series_to_pull = [
        "DGS10", "DGS2", "T10Y2Y", "FEDFUNDS",
        "CPIAUCSL", "PCEPILFE", "T10YIE",
        "UNRATE", "ICSA", "INDPRO",
        "BAMLH0A0HYM2", "BAMLC0A0CM", "DTWEXBGS", "VIXCLS"
    ]
    frames = [pull_fred_series(sid, lookback_days=60) for sid in series_to_pull]
    combined = pd.concat(frames, axis=1)
    print(combined.tail())
```

---

## 4. Daily Context Update

The pipeline script writes fresh FRED data to `context/macro-state.md` each morning. Below is the standalone function used by `scripts/update-context.py`.

```python
def write_macro_state(output_path: str = "context/macro-state.md") -> None:
    """Pull key FRED series and write current values to macro-state.md."""
    series_meta = {
        "DGS10":           ("10Y Treasury Yield", "%"),
        "DGS2":            ("2Y Treasury Yield", "%"),
        "T10Y2Y":          ("Yield Curve (10Y-2Y)", "pp"),
        "FEDFUNDS":        ("Fed Funds Rate", "%"),
        "SOFR":            ("SOFR", "%"),
        "CPIAUCSL":        ("CPI YoY", "% (MoM index, compute YoY externally)"),
        "PCEPILFE":        ("Core PCE", "index"),
        "T10YIE":          ("10Y Breakeven Inflation", "%"),
        "UNRATE":          ("Unemployment Rate", "%"),
        "ICSA":            ("Initial Jobless Claims", "thousands"),
        "INDPRO":          ("Industrial Production", "index"),
        "BAMLH0A0HYM2":   ("HY Credit Spread (OAS)", "bps"),
        "BAMLC0A0CM":     ("IG Credit Spread (OAS)", "bps"),
        "DTWEXBGS":        ("Broad Dollar Index", "index"),
        "VIXCLS":          ("VIX", "index"),
    }
    lines = [
        f"# Macro State\n",
        f"*Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}*\n",
        "\n## Current FRED Readings\n",
    ]
    for sid, (name, unit) in series_meta.items():
        try:
            value = get_latest(sid)
            val_str = f"{value:.3f}" if value is not None else "N/A"
            lines.append(f"- **{name}** (`{sid}`): {val_str} {unit}")
        except Exception as e:
            lines.append(f"- **{name}** (`{sid}`): ERROR — {e}")

    with open(output_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[FRED] Written to {output_path}")
```

---

## 5. Cron Setup (Standalone)

If not using the full Docker pipeline, set up a direct cron entry to run the FRED pull each trading morning. The full pipeline cron is covered in `data-pipeline-guide.md`.

**macOS (cron — simplest):**

```bash
# Run at 6:30 AM Mon-Fri
30 6 * * 1-5 /path/to/conda/envs/crucible/bin/python /path/to/crucible-cio-team/scripts/update-fred.py >> /tmp/fred-update.log 2>&1
```

Edit with: `crontab -e`

**Verify it works:**
```bash
/path/to/python scripts/update-fred.py && cat context/macro-state.md
```

---

## Notes

- FRED data is typically available by 8:30 AM ET for series released that day. The 6:30 AM pull catches everything released the prior day.
- Monthly series (CPI, PCE, unemployment) update on release days. Between releases, the value stays flat — this is expected.
- The `VIXCLS` series on FRED is one day lagged. For same-day VIX, use your broker's market data feed.
- Series that return `"."` in the observations array are missing values — `pd.to_numeric(..., errors="coerce")` converts these to `NaN` and `dropna` removes them.
