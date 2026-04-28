#!/usr/bin/env python3
"""
Crucible daily context pipeline.
Pulls FRED, Norgate, Kalshi, and IBKR data and writes:
  context/macro-state.md
  context/portfolio-state.md
  context/kalshi-state.md

Run each morning before Claude Code sessions, or via cron at 6:30 AM Mon-Fri.
See infrastructure/data/data-pipeline-guide.md for full documentation.
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

import subprocess
import requests
import pandas as pd

FRED_API_KEY = os.environ.get("FRED_API_KEY", "")
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

FRED_SERIES = {
    "DGS10":        ("10Y Treasury Yield", "%"),
    "DGS2":         ("2Y Treasury Yield", "%"),
    "T10Y2Y":       ("Yield Curve (10Y-2Y)", "pp"),
    "FEDFUNDS":     ("Fed Funds Rate", "%"),
    "SOFR":         ("SOFR", "%"),
    "T10YIE":       ("10Y Breakeven Inflation", "%"),
    "CPIAUCSL":     ("CPI (index)", "index"),
    "PCEPILFE":     ("Core PCE (index)", "index"),
    "UNRATE":       ("Unemployment Rate", "%"),
    "ICSA":         ("Initial Jobless Claims", "K"),
    "INDPRO":       ("Industrial Production", "index"),
    "BAMLH0A0HYM2": ("HY Credit Spread", "bps"),
    "BAMLC0A0CM":   ("IG Credit Spread", "bps"),
    "DTWEXBGS":     ("Broad Dollar Index", "index"),
    "VIXCLS":       ("VIX (1d lag)", "index"),
}

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

KALSHI_MARKETS = [
    # (ticker, category, signal_direction, description)
    # Update tickers each event cycle — verify current tickers at kalshi.com
    ("KXFEDRATE",   "fed_policy",  "bearish", "Fed Funds Rate — next meeting"),
    ("KXCPI",       "inflation",   "bearish", "CPI above consensus"),
    ("KXGDP",       "growth",      "bullish", "GDP above consensus"),
    ("KXUNRATE",    "labor",       "bearish", "Unemployment above threshold"),
    ("KXRECESSION", "recession",   "bearish", "US Recession next 12m"),
    ("KXSPX",       "equity",      "bullish", "S&P 500 level — year-end"),
]


# ── FRED ──────────────────────────────────────────────────────────────────────

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
        for obs in r.json().get("observations", []):
            val = obs.get("value", ".")
            if val != ".":
                return float(val)
    except Exception as e:
        log.warning(f"FRED {series_id}: {e}")
    return None


def write_macro_state(output_path: Path) -> None:
    log.info("Pulling FRED series...")
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Macro State\n",
        f"*Updated: {ts}*\n",
        "\n## FRED Readings\n",
    ]
    for sid, (name, unit) in FRED_SERIES.items():
        value = _fred_latest(sid)
        val_str = f"{value:.3f}" if value is not None else "N/A"
        lines.append(f"- **{name}** (`{sid}`): {val_str} {unit}")
        log.info(f"  {sid}: {val_str}")

    try:
        import norgatedata
        lines += ["\n## Futures Prices (Norgate — Continuous Front Month)\n"]
        today = datetime.today().strftime("%Y-%m-%d")
        for sym, desc in NORGATE_SYMBOLS.items():
            try:
                df = norgatedata.historic_price_dataframe(
                    sym, today, today,
                    norgatedata.StockPriceAdjustmentType.TOTALRETURN,
                    norgatedata.PaddingType.NAN,
                    "pandas-dataframe",
                )
                if not df.empty:
                    close = float(df["Close"].dropna().iloc[-1])
                    lines.append(f"- **{desc}** (`{sym}`): {close:.2f}")
                    log.info(f"  {sym}: {close:.2f}")
                else:
                    lines.append(f"- **{desc}** (`{sym}`): no data today")
            except Exception as e:
                lines.append(f"- **{desc}** (`{sym}`): UNAVAILABLE — {e}")
    except ImportError:
        lines.append("\n*Norgate not available — skipping futures prices*")
        log.warning("norgatedata not installed; skipping")

    output_path.write_text("\n".join(lines) + "\n")
    log.info(f"[FRED+Norgate] Written to {output_path}")


# ── IBKR ──────────────────────────────────────────────────────────────────────

def write_portfolio_state(output_path: Path) -> None:
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    try:
        from ib_insync import IB, util
        util.patchAsyncio()
        ib = IB()
        host = os.environ.get("IBKR_HOST", "127.0.0.1")
        port = int(os.environ.get("IBKR_PORT", "7497"))
        client_id = int(os.environ.get("IBKR_CLIENT_ID", "10"))

        log.info(f"Connecting to IBKR at {host}:{port}...")
        ib.connect(host, port, clientId=client_id, timeout=15)

        lines = [
            "# Portfolio State\n",
            f"*Updated: {ts}*\n",
            "\n## Account Summary\n",
        ]
        tags = {item.tag: item for item in ib.accountSummary()}
        for tag in ("NetLiquidation", "TotalCashValue", "GrossPositionValue", "MaintMarginReq"):
            if tag in tags:
                lines.append(f"- **{tag}**: {tags[tag].value} {tags[tag].currency}")
                log.info(f"  {tag}: {tags[tag].value}")

        positions = ib.positions()
        lines.append("\n## Open Positions\n")
        if positions:
            for pos in positions:
                c = pos.contract
                lines.append(
                    f"- **{c.symbol}** ({c.secType}): "
                    f"size={pos.position} | avg_cost={pos.avgCost:.4f}"
                )
                log.info(f"  {c.symbol}: {pos.position} @ {pos.avgCost:.4f}")
        else:
            lines.append("*No open positions*")

        ib.disconnect()
        output_path.write_text("\n".join(lines) + "\n")
        log.info(f"[IBKR] Written to {output_path}")

    except Exception as e:
        log.warning(f"IBKR unavailable: {e}")
        output_path.write_text(
            f"# Portfolio State\n\n*IBKR unavailable at {ts}: {e}*\n"
        )


# ── Kalshi ────────────────────────────────────────────────────────────────────

def _kalshi_weight(yes_prob: float, direction: str) -> float:
    centered = (yes_prob - 0.5) * 2
    return round(-centered if direction == "bearish" else centered, 3)


def write_kalshi_state(output_path: Path) -> None:
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    kalshi_key = os.environ.get("KALSHI_API_KEY", "")

    if not kalshi_key:
        log.warning("KALSHI_API_KEY not set — skipping Kalshi pull")
        output_path.write_text(f"# Kalshi State\n\n*KALSHI_API_KEY not configured — {ts}*\n")
        return

    try:
        import kalshi_python
        config = kalshi_python.Configuration(
            host="https://trading-api.kalshi.com/trade-api/v2"
        )
        config.api_key["Authorization"] = kalshi_key
        config.api_key_prefix["Authorization"] = "Bearer"
        markets_api = kalshi_python.MarketApi(kalshi_python.ApiClient(config))

        lines = [
            "# Kalshi State\n",
            f"*Updated: {ts}*\n",
            "\n## Market Probabilities\n",
        ]
        for ticker, category, direction, description in KALSHI_MARKETS:
            try:
                market = markets_api.get_market(ticker=ticker)
                yes_prob = market.market.yes_ask / 100
                weight = _kalshi_weight(yes_prob, direction)
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
        log.warning("kalshi_python not installed; skipping")
        output_path.write_text(
            f"# Kalshi State\n\n*kalshi_python not installed — {ts}*\n"
        )


# ── Main ──────────────────────────────────────────────────────────────────────

def _ensure_db() -> None:
    db_init = PROJECT_ROOT / "db" / "init.py"
    result = subprocess.run([sys.executable, str(db_init)], capture_output=True, text=True)
    log.info(result.stdout.strip() or "[crucible-db] init ran")
    if result.returncode != 0:
        log.warning(f"[crucible-db] init exited {result.returncode}: {result.stderr.strip()}")


def main() -> None:
    _ensure_db()

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
