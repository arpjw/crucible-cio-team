# Norgate Data Setup Guide

Norgate Data provides clean, point-in-time, back-adjusted futures data — the primary price source for Crucible's signal research, backtest designer, and regime classifier agents. This guide covers subscription selection, the NDU updater, the Python API, and the 24 core futures contracts for a global macro CTA.

---

## 1. Subscription Tier Guide

Norgate offers several tiers. For a global macro CTA the relevant options are:

| Tier | Monthly (USD) | Annual (USD) | What It Covers | Use When |
|------|--------------|--------------|----------------|----------|
| **Futures Standard** | ~$27 | ~$270 | US futures: equity indices, rates, energies, metals, grains, softs | Single-market strategies, US-only |
| **Futures Professional** | ~$55 | ~$549 | All Futures Standard + FX futures, international futures (Eurex, SGX, etc.) | Multi-asset global macro, FX carry |
| **Futures + Equities** | ~$83 | ~$829 | All futures + US equities (S&P 500 history, delisted securities) | Equity factor strategies or stat arb |

**Recommendation for Crucible**: Start with **Futures Standard**. Upgrade to **Futures Professional** if your strategy trades FX futures or international index futures (Nikkei, DAX, etc.).

Sign up at [norgatedata.com](https://norgatedata.com). License is per-machine — you need a separate license for a production server if you're not running locally.

---

## 2. NDU (Norgate Data Updater) Installation

NDU is the desktop application that downloads and maintains the local Norgate database. The Python API reads from this local database — it does not make live internet calls.

1. Download NDU from your Norgate account portal
2. Install on Windows or macOS (Windows preferred — the native client is more stable)
3. Log in with your Norgate credentials
4. Click **Update All** — initial download is 5–15 minutes depending on subscription
5. Configure auto-update: **Settings → Schedule → Daily at 6:00 AM**

**Important**: NDU must run on the same machine as your Python scripts. If running on a Linux server, use Wine to run NDU on the server, or run NDU on a Windows machine and expose the database via NFS/SMB.

**Alternative for Linux production servers**: Run NDU on a Windows VM or local machine, then `rsync` the Norgate data directory to your Linux server before the pipeline runs.

---

## 3. Python API Installation

```bash
pip install norgatedata
```

No API key required — the package reads from the local NDU database. If NDU isn't installed and up to date, calls will fail with a "database not found" error.

Verify installation:
```python
import norgatedata
print(norgatedata.status())
# Should return: {'status': 'ok', 'securities_count': N}
```

---

## 4. Continuous Futures Data Pull

```python
import norgatedata
import pandas as pd
from datetime import datetime


def pull_continuous_futures(
    symbol: str,
    start_date: str = "2010-01-01",
    back_adjust: bool = True,
    padding_type: str = "NAN"
) -> pd.DataFrame:
    """
    Pull continuous front-month futures into a pandas DataFrame.

    symbol: Norgate symbol (e.g., '&ES' for continuous ES)
    back_adjust: True = Panama Canal (ratio-based) back-adjustment
    padding_type: 'NAN' to leave gaps on non-trading days
    """
    timeseriesformat = "pandas-dataframe"
    priceadjust = (
        norgatedata.StockPriceAdjustmentType.TOTALRETURN
        if back_adjust
        else norgatedata.StockPriceAdjustmentType.NONE
    )
    padding = norgatedata.PaddingType.NAN if padding_type == "NAN" else norgatedata.PaddingType.ALLCALENDARDAYS

    df = norgatedata.historic_price_dataframe(
        symbol,
        start_date,
        datetime.today().strftime("%Y-%m-%d"),
        priceadjust,
        padding,
        timeseriesformat,
    )
    df.index = pd.to_datetime(df.index)
    df = df.dropna(subset=["Close"])
    return df


# Example: pull ES continuous and compute 20-day return
if __name__ == "__main__":
    es = pull_continuous_futures("&ES")
    es["ret_20d"] = es["Close"].pct_change(20)
    print(es[["Close", "ret_20d"]].tail(10))
```

### Back-Adjustment Methods

| Method | Norgate Enum | Use When |
|--------|-------------|----------|
| Ratio (Panama Canal) | `TOTALRETURN` | Trend following — preserves return proportions, no negative prices |
| Difference (classic) | `BACK_ADJUSTED` | Mean reversion — preserves level changes, can create negative prices in old data |
| None (raw roll) | `NONE` | Roll cost calculation, term structure analysis |

For signal research and backtesting, **always use ratio back-adjustment** unless you have a specific reason not to. Unback-adjusted data will produce misleading signals around contract rolls.

---

## 5. Core Futures Contracts — 24 Symbols

The 24 most relevant futures contracts for a global macro CTA. Norgate uses `&SYMBOL` for continuous front-month contracts.

### Equity Indices (US)

| Symbol | Norgate Code | Exchange | Notes |
|--------|-------------|----------|-------|
| E-mini S&P 500 | `&ES` | CME | Primary US equity proxy |
| E-mini Nasdaq 100 | `&NQ` | CME | Tech/growth exposure |
| E-mini Dow Jones | `&YM` | CBOT | Value/cyclical tilt |
| E-mini Russell 2000 | `&RTY` | CME | Small cap / risk appetite |

### Rates (US)

| Symbol | Norgate Code | Exchange | Notes |
|--------|-------------|----------|-------|
| 10-Year T-Note | `&ZN` | CBOT | Belly of the curve |
| 30-Year T-Bond | `&ZB` | CBOT | Long end duration |
| 5-Year T-Note | `&ZF` | CBOT | Mid curve |
| 2-Year T-Note | `&ZT` | CBOT | Short end, policy sensitive |

### FX (Major Pairs vs USD)

| Symbol | Norgate Code | Exchange | Notes |
|--------|-------------|----------|-------|
| Euro FX | `&6E` | CME | EUR/USD |
| Japanese Yen | `&6J` | CME | JPY/USD — risk-off proxy |
| British Pound | `&6B` | CME | GBP/USD |
| Australian Dollar | `&6A` | CME | Commodity currency / risk-on |
| Canadian Dollar | `&6C` | CME | Oil-linked |
| Swiss Franc | `&6S` | CME | Safe haven |

### Energies

| Symbol | Norgate Code | Exchange | Notes |
|--------|-------------|----------|-------|
| Crude Oil (WTI) | `&CL` | NYMEX | Global energy benchmark |
| Natural Gas | `&NG` | NYMEX | High volatility, seasonal |
| RBOB Gasoline | `&RB` | NYMEX | Crack spread component |
| Heating Oil | `&HO` | NYMEX | Distillate proxy |

### Metals

| Symbol | Norgate Code | Exchange | Notes |
|--------|-------------|----------|-------|
| Gold | `&GC` | COMEX | Inflation hedge, safe haven |
| Silver | `&SI` | COMEX | More volatile than gold |
| Copper | `&HG` | COMEX | Global growth proxy |

### Agricultural / Softs (Selected)

| Symbol | Norgate Code | Exchange | Notes |
|--------|-------------|----------|-------|
| Corn | `&ZC` | CBOT | Grain complex anchor |
| Soybeans | `&ZS` | CBOT | Protein / energy crop |
| Wheat | `&ZW` | CBOT | Geopolitical sensitivity |

---

## 6. Handling Roll Conventions

Norgate's continuous contracts handle roll automatically, but you need to understand the method to interpret returns correctly.

### Default Roll: Volume-Based

Norgate's default is to roll when the next contract's volume exceeds the front month. This is the most common convention for trend following.

```python
# Explicit roll type specification
norgatedata.historic_price_dataframe(
    "&ES",
    "2020-01-01",
    "2025-01-01",
    norgatedata.StockPriceAdjustmentType.TOTALRETURN,
    norgatedata.PaddingType.NAN,
    "pandas-dataframe",
    # Default roll is volume-based — no extra parameter needed
)
```

### Contract-Level Data (for Roll Cost Calculation)

To compute actual roll cost, pull individual contract data and compare prices at expiry:

```python
# Pull specific ES contract
es_mar25 = norgatedata.historic_price_dataframe(
    "ESH25",  # March 2025 contract
    "2025-01-01",
    "2025-03-21",
    norgatedata.StockPriceAdjustmentType.NONE,  # No adjustment for raw prices
    norgatedata.PaddingType.NAN,
    "pandas-dataframe",
)
```

Norgate contract month codes follow standard futures convention: F=Jan, G=Feb, H=Mar, J=Apr, K=May, M=Jun, N=Jul, Q=Aug, U=Sep, V=Oct, X=Nov, Z=Dec.

### Verifying Data Quality

```python
def check_data_quality(symbol: str) -> dict:
    df = pull_continuous_futures(symbol, start_date="2020-01-01")
    gaps = df["Close"].isna().sum()
    daily_ret = df["Close"].pct_change().dropna()
    large_moves = (daily_ret.abs() > 0.10).sum()
    return {
        "symbol": symbol,
        "rows": len(df),
        "null_closes": int(gaps),
        "daily_moves_gt_10pct": int(large_moves),
        "start": str(df.index[0].date()),
        "end": str(df.index[-1].date()),
    }

for sym in ["&ES", "&ZN", "&GC", "&CL", "&6E"]:
    print(check_data_quality(sym))
```

---

## Notes

- Norgate's free trial includes 30 days of full data access. Use the trial to build and test the full pipeline before subscribing.
- The Python API requires the NDU application to be running at the time of the call. If NDU isn't active, you'll get `NorgateDataError: Could not connect to Norgate Data service`.
- Do not store Norgate data files in Git — the database is large and licensed per-machine. Add the NDU data directory to `.gitignore`.
- Norgate does not cover crypto futures. For BTC/ETH futures, use CME data via IBKR's market data subscription or a separate provider.
