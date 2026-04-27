# Data Pipeline Guide

How to wire FRED, Norgate, Kalshi, and IBKR into a single daily pipeline that keeps Crucible's context files fresh before each Claude Code session. The pipeline writes three files that agents read at invocation time.

---

## What the Pipeline Produces

| File | Source | Updated By |
|------|--------|-----------|
| `context/macro-state.md` | FRED + Norgate | FRED series + futures price summary |
| `context/portfolio-state.md` | IBKR | Live positions, NAV, cash |
| `context/kalshi-state.md` | Kalshi | Prediction market probabilities |

After a successful run, Claude Code sessions start with agents that already have live data. Without this pipeline, agents operate on manually-maintained context files — still useful, but not live.

---

## scripts/update-context.py

Place this file at `scripts/update-context.py` in your Crucible repo root.

```python
#!/usr/bin/env python3
"""
Crucible daily context pipeline.
Pulls FRED, Norgate, Kalshi, and IBKR data and writes context files.
Run each morning before Claude Code sessions.
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


# ── FRED ─────────────────────────────────────────────────────────────────────

import requests
import pandas as pd

FRED_API_KEY = os.environ.get("FRED_API_KEY", "")
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

FRED_SERIES = {
    "DGS10":         ("10Y Treasury Yield", "%"),
    "DGS2":          ("2Y Treasury Yield", "%"),
    "T10Y2Y":        ("Yield Curve (10Y-2Y)", "pp"),
    "FEDFUNDS":      ("Fed Funds Rate", "%"),
    "SOFR":          ("SOFR", "%"),
    "T10YIE":        ("10Y Breakeven Inflation", "%"),
    "CPIAUCSL":      ("CPI (index)", "index"),
    "PCEPILFE":      ("Core PCE (index)", "index"),
    "UNRATE":        ("Unemployment Rate", "%"),
    "ICSA":          ("Initial Jobless Claims", "K"),
    "INDPRO":        ("Industrial Production", "index"),
    "BAMLH0A0HYM2":  ("HY Credit Spread", "bps"),
    "BAMLC0A0CM":    ("IG Credit Spread", "bps"),
    "DTWEXBGS":      ("Broad Dollar Index", "index"),
    "VIXCLS":        ("VIX (1d lag)", "index"),
}


def _fred_latest(series_id: str) -> float | None:
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 5,
    }
    try:
        r = requests.get(FRED_BASE_URL, params=params, timeout=20)
        r.raise_for_status()
        obs = r.json().get("observations", [])
        for o in obs:
            val = o.get("value", ".")
            if val != ".":
                return float(val)
    except Exception as e:
        log.warning(f"FRED {series_id}: {e}")
    return None


def write_macro_state(output_path: Path) -> None:
    log.info("Pulling FRED series...")
    lines = [
        "# Macro State\n",
        f"*Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}*\n",
        "\n## FRED Readings\n",
    ]
    for sid, (name, unit) in FRED_SERIES.items():
        value = _fred_latest(sid)
        val_str = f"{value:.3f}" if value is not None else "N/A"
        lines.append(f"- **{name}** (`{sid}`): {val_str} {unit}")
        log.info(f"  {sid}: {val_str}")

    # ── Norgate futures summary (if available) ────────────────────────────────
    try:
        import norgatedata
        lines += ["\n## Futures Prices (Norgate — Continuous Front Month)\n"]
        NORGATE_SYMBOLS = {
            "&ES": "E-mini S&P 500",
            "&NQ": "E-mini Nasdaq 100",
            "&ZN": "10Y T-Note",
            "&ZB": "30Y T-Bond",
            "&GC": "Gold",
            "&CL": "Crude Oil (WTI)",
            "&6E": "Euro FX",
            "&6J": "Yen FX",
        }
        for sym, desc in NORGATE_SYMBOLS.items():
            try:
                df = norgatedata.historic_price_dataframe(
                    sym,
                    (datetime.today().strftime("%Y-%m-%d")),
                    (datetime.today().strftime("%Y-%m-%d")),
                    norgatedata.StockPriceAdjustmentType.TOTALRETURN,
                    norgatedata.PaddingType.NAN,
                    "pandas-dataframe",
                )
                if not df.empty:
                    close = df["Close"].dropna().iloc[-1]
                    lines.append(f"- **{desc}** (`{sym}`): {close:.2f}")
                    log.info(f"  {sym}: {close:.2f}")
            except Exception as e:
                lines.append(f"- **{desc}** (`{sym}`): UNAVAILABLE — {e}")
    except ImportError:
        lines.append("\n*Norgate not available on this machine — skipping futures prices*")
        log.warning("norgatedata not installed; skipping Norgate pull")

    output_path.write_text("\n".join(lines) + "\n")
    log.info(f"[FRED+Norgate] Written to {output_path}")


# ── IBKR ──────────────────────────────────────────────────────────────────────

def write_portfolio_state(output_path: Path) -> None:
    try:
        from ib_insync import IB, util
        util.patchAsyncio()
        ib = IB()
        ibkr_host = os.environ.get("IBKR_HOST", "127.0.0.1")
        ibkr_port = int(os.environ.get("IBKR_PORT", "7497"))
        ibkr_client_id = int(os.environ.get("IBKR_CLIENT_ID", "10"))

        log.info(f"Connecting to IBKR at {ibkr_host}:{ibkr_port}...")
        ib.connect(ibkr_host, ibkr_port, clientId=ibkr_client_id, timeout=15)

        lines = [
            "# Portfolio State\n",
            f"*Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}*\n",
            "\n## Account Summary\n",
        ]

        summary = ib.accountSummary()
        tags = {item.tag: item for item in summary}
        for tag in ("NetLiquidation", "TotalCashValue", "GrossPositionValue", "MaintMarginReq"):
            if tag in tags:
                lines.append(f"- **{tag}**: {tags[tag].value} {tags[tag].currency}")

        positions = ib.positions()
        lines += ["\n## Open Positions\n"]
        if positions:
            for pos in positions:
                c = pos.contract
                lines.append(
                    f"- **{c.symbol}** ({c.secType}): "
                    f"size={pos.position} | avg_cost={pos.avgCost:.4f}"
                )
        else:
            lines.append("*No open positions*")

        ib.disconnect()
        output_path.write_text("\n".join(lines) + "\n")
        log.info(f"[IBKR] Written to {output_path}")

    except Exception as e:
        log.warning(f"IBKR unavailable: {e} — writing placeholder")
        output_path.write_text(
            f"# Portfolio State\n\n*IBKR unavailable at {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}: {e}*\n"
        )


# ── Kalshi ────────────────────────────────────────────────────────────────────

KALSHI_MARKETS = [
    # Update tickers each event cycle. These are category prefixes — verify current tickers at kalshi.com
    ("KXFEDRATE",   "fed_policy",   "bearish",  "Fed Funds Rate — next meeting"),
    ("KXCPI",       "inflation",    "bearish",  "CPI above consensus"),
    ("KXGDP",       "growth",       "bullish",  "GDP above consensus"),
    ("KXUNRATE",    "labor",        "bearish",  "Unemployment above threshold"),
    ("KXRECESSION", "recession",    "bearish",  "US Recession next 12m"),
    ("KXSPX",       "equity",       "bullish",  "S&P 500 level — year-end"),
]


def _kalshi_to_weight(yes_prob: float, direction: str) -> float:
    centered = (yes_prob - 0.5) * 2
    return round(-centered if direction == "bearish" else centered, 3)


def write_kalshi_state(output_path: Path) -> None:
    kalshi_key = os.environ.get("KALSHI_API_KEY", "")
    if not kalshi_key:
        log.warning("KALSHI_API_KEY not set — skipping Kalshi pull")
        output_path.write_text(
            f"# Kalshi State\n\n*KALSHI_API_KEY not configured — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}*\n"
        )
        return

    try:
        import kalshi_python
        config = kalshi_python.Configuration(
            host="https://trading-api.kalshi.com/trade-api/v2"
        )
        config.api_key["Authorization"] = kalshi_key
        config.api_key_prefix["Authorization"] = "Bearer"
        api_client = kalshi_python.ApiClient(config)
        markets_api = kalshi_python.MarketApi(api_client)

        lines = [
            "# Kalshi State\n",
            f"*Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}*\n",
            "\n## Market Probabilities\n",
        ]

        for ticker, category, direction, description in KALSHI_MARKETS:
            try:
                market = markets_api.get_market(ticker=ticker)
                yes_prob = market.market.yes_ask / 100
                weight = _kalshi_to_weight(yes_prob, direction)
                flag = " **[CONSENSUS DIVERGENCE — REVIEW]**" if abs(weight) > 0.30 else ""
                lines.append(
                    f"- **{description}** (`{ticker}`): "
                    f"{yes_prob:.1%} yes | regime weight: {weight:+.3f}{flag}"
                )
                log.info(f"  {ticker}: {yes_prob:.1%} → weight {weight:+.3f}")
            except Exception as e:
                lines.append(f"- **{description}** (`{ticker}`): UNAVAILABLE — {e}")
                log.warning(f"  {ticker}: {e}")

        output_path.write_text("\n".join(lines) + "\n")
        log.info(f"[Kalshi] Written to {output_path}")

    except ImportError:
        log.warning("kalshi_python not installed; skipping Kalshi pull")
        output_path.write_text(
            f"# Kalshi State\n\n*kalshi_python not installed — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}*\n"
        )


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    context_dir = PROJECT_ROOT / "context"
    context_dir.mkdir(exist_ok=True)

    start = datetime.utcnow()
    log.info("=== Crucible context pipeline starting ===")

    write_macro_state(context_dir / "macro-state.md")
    write_portfolio_state(context_dir / "portfolio-state.md")
    write_kalshi_state(context_dir / "kalshi-state.md")

    elapsed = (datetime.utcnow() - start).total_seconds()
    log.info(f"=== Pipeline complete in {elapsed:.1f}s ===")


if __name__ == "__main__":
    main()
```

---

## Cron Setup

### macOS — crontab (simplest)

Edit your crontab:
```bash
crontab -e
```

Add:
```cron
# Crucible context pipeline — 6:30 AM Mon-Fri
30 6 * * 1-5 /path/to/conda/envs/crucible/bin/python /path/to/crucible-cio-team/scripts/update-context.py >> /tmp/crucible-pipeline.log 2>&1
```

Verify:
```bash
crontab -l  # Should show the entry
# Test run manually
/path/to/python /path/to/crucible-cio-team/scripts/update-context.py
```

### macOS — launchd (recommended for reliability)

Create `~/Library/LaunchAgents/com.crucible.pipeline.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.crucible.pipeline</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/conda/envs/crucible/bin/python</string>
        <string>/path/to/crucible-cio-team/scripts/update-context.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>6</integer>
        <key>Minute</key>
        <integer>30</integer>
        <key>Weekday</key>
        <!-- 1=Monday through 5=Friday; repeat entry for each day -->
        <integer>1</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/crucible-pipeline.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/crucible-pipeline-err.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
```

**Note on launchd weekday scheduling**: launchd does not support `1-5` range syntax. The correct approach for Mon-Fri is a cron job via `crontab -e`. Use launchd only if you need run-at-load or other launchd-specific features.

Load the agent:
```bash
launchctl load ~/Library/LaunchAgents/com.crucible.pipeline.plist
launchctl start com.crucible.pipeline  # Run immediately for testing
```

### Linux — crontab

```bash
crontab -e
# Add:
30 6 * * 1-5 /home/user/miniconda3/envs/crucible/bin/python /home/user/crucible-cio-team/scripts/update-context.py >> /var/log/crucible-pipeline.log 2>&1
```

### Linux — systemd timer (production server)

Create `/etc/systemd/system/crucible-pipeline.service`:
```ini
[Unit]
Description=Crucible context pipeline

[Service]
Type=oneshot
User=crucible
WorkingDirectory=/home/crucible/crucible-cio-team
EnvironmentFile=/home/crucible/crucible-cio-team/.env
ExecStart=/home/crucible/miniconda3/envs/crucible/bin/python scripts/update-context.py
StandardOutput=journal
StandardError=journal
```

Create `/etc/systemd/system/crucible-pipeline.timer`:
```ini
[Unit]
Description=Run Crucible pipeline at 6:30 AM weekdays

[Timer]
OnCalendar=Mon-Fri 06:30:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable:
```bash
systemctl daemon-reload
systemctl enable --now crucible-pipeline.timer
systemctl status crucible-pipeline.timer
```

---

## Verifying a Run

```bash
# Check context files were updated today
ls -la context/macro-state.md context/portfolio-state.md context/kalshi-state.md

# Spot-check content
head -5 context/macro-state.md

# View pipeline log
tail -50 /tmp/crucible-pipeline.log
```

Expected output tail for a clean run:
```
2026-04-27 06:30:01 [INFO] === Crucible context pipeline starting ===
2026-04-27 06:30:02 [INFO] Pulling FRED series...
2026-04-27 06:30:04 [INFO] [FRED+Norgate] Written to context/macro-state.md
2026-04-27 06:30:05 [INFO] Connecting to IBKR at 127.0.0.1:7497...
2026-04-27 06:30:07 [INFO] [IBKR] Written to context/portfolio-state.md
2026-04-27 06:30:08 [INFO] [Kalshi] Written to context/kalshi-state.md
2026-04-27 06:30:08 [INFO] === Pipeline complete in 7.3s ===
```

---

## Failure Modes

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `macro-state.md` not updated | FRED key missing or rate limit | Check `.env`, verify `FRED_API_KEY` is set |
| Norgate section shows UNAVAILABLE | NDU not running | Start NDU and run update |
| Portfolio state shows IBKR error | TWS/Gateway not running | Open TWS before 6:30 AM, or switch to IB Gateway with auto-start |
| Kalshi tickers return 404 | Event resolved, ticker expired | Update `KALSHI_MARKETS` list with new tickers |
| Pipeline runs but files are stale | Script found cached values | Check `sort_order=desc` in FRED call; check NDU date |
