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
import time
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
    "policy": {
        "FEDFUNDS": "Fed Funds Rate",
        "DFEDTARU": "Fed Funds Target Upper",
        "DFEDTARL": "Fed Funds Target Lower",
    },
    "yield_curve": {
        "DGS2": "2Y Treasury Yield",
        "DGS10": "10Y Treasury Yield",
        "DGS30": "30Y Treasury Yield",
        "T10Y2Y": "10Y-2Y Spread",
    },
    "inflation": {
        "CPIAUCSL": "CPI YoY",
        "PCEPILFE": "Core PCE",
        "T10YIE": "10Y Breakeven Inflation",
    },
    "growth": {
        "A191RL1Q225SBEA": "Real GDP Growth",
        "UNRATE": "Unemployment Rate",
        "ICSA": "Initial Jobless Claims",
        "INDPRO": "Industrial Production",
    },
    "credit": {
        "BAMLH0A0HYM2": "HY Credit Spread",
        "BAMLC0A0CM": "IG Credit Spread",
        "DTWEXBGS": "Trade-Weighted USD",
    },
    "sentiment": {
        "UMCSENT": "U Michigan Consumer Sentiment",
        "VIXCLS": "VIX",
    },
    "liquidity": {
        "BOGMBASE": "Monetary Base",
    },
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

def fetch_fred_series(series_id: str, api_key: str) -> tuple[float, str] | None:
    """Fetch the most recent value and date for a FRED series.

    Handles 429 rate limiting with exponential backoff (max 3 retries).
    Returns (value, date_str) or None if the series cannot be fetched.
    """
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 10,
    }
    for attempt in range(3):
        try:
            r = requests.get(FRED_BASE_URL, params=params, timeout=20)
            if r.status_code == 429:
                wait = 2 ** attempt
                log.warning(f"FRED rate limit on {series_id}, retrying in {wait}s...")
                time.sleep(wait)
                continue
            r.raise_for_status()
            for obs in r.json().get("observations", []):
                val = obs.get("value", ".")
                if val != ".":
                    return float(val), obs["date"]
            log.warning(f"FRED {series_id}: no non-null observations")
            return None
        except requests.exceptions.HTTPError as e:
            log.warning(f"FRED {series_id}: HTTP {e}")
            return None
        except Exception as e:
            log.warning(f"FRED {series_id}: {e}")
            return None
    log.warning(f"FRED {series_id}: max retries exceeded")
    return None


def _v(data: dict, sid: str) -> float | None:
    result = data.get(sid)
    return result[0] if result else None


def _d(data: dict, sid: str) -> str | None:
    result = data.get(sid)
    return result[1] if result else None


def _compute_regime_summary(data: dict) -> dict:
    # Growth: GDP primary, UNRATE secondary
    gdp = _v(data, "A191RL1Q225SBEA")
    unrate = _v(data, "UNRATE")
    if gdp is not None:
        if gdp >= 2.5:
            growth = "EXPANDING"
        elif gdp >= 0:
            growth = "SLOWING"
        else:
            growth = "CONTRACTING"
    elif unrate is not None:
        growth = "EXPANDING" if unrate < 4.5 else "SLOWING"
    else:
        growth = "UNKNOWN"

    # Inflation: 10Y breakeven primary (already in % terms)
    t10yie = _v(data, "T10YIE")
    if t10yie is not None:
        if t10yie >= 3.0:
            inflation = "RISING"
        elif t10yie >= 2.5:
            inflation = "ELEVATED"
        elif t10yie >= 2.0:
            inflation = "FALLING"
        else:
            inflation = "LOW"
    else:
        inflation = "UNKNOWN"

    # Financial Conditions: HY spread primary, VIX modifier
    hy = _v(data, "BAMLH0A0HYM2")
    vix = _v(data, "VIXCLS")
    if hy is not None:
        if hy >= 600:
            fin_cond = "TIGHT"
        elif hy >= 450:
            fin_cond = "TIGHTENING"
        elif hy >= 350:
            fin_cond = "EASING"
        else:
            fin_cond = "EASY"
        if vix is not None and vix >= 30 and fin_cond in ("EASY", "EASING"):
            fin_cond = "TIGHTENING"
    elif vix is not None:
        fin_cond = "TIGHT" if vix >= 30 else ("TIGHTENING" if vix >= 20 else "EASY")
    else:
        fin_cond = "UNKNOWN"

    # Policy: Fed Funds vs target upper bound
    fedfunds = _v(data, "FEDFUNDS")
    target_upper = _v(data, "DFEDTARU")
    if fedfunds is not None and target_upper is not None:
        diff = target_upper - fedfunds
        if diff > 0.75:
            policy = "CUTTING"
        elif diff < -0.25:
            policy = "HIKING"
        else:
            policy = "HOLD"
    elif fedfunds is not None:
        if fedfunds <= 0.25:
            policy = "EMERGENCY"
        elif fedfunds < 2.5:
            policy = "CUTTING"
        else:
            policy = "HOLD"
    else:
        policy = "UNKNOWN"

    return {
        "growth": growth,
        "inflation": inflation,
        "financial_conditions": fin_cond,
        "policy": policy,
    }


def write_macro_state(output_path: Path) -> None:
    log.info("Pulling FRED series...")
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # Fetch all series
    data: dict[str, tuple[float, str] | None] = {}
    for series_dict in FRED_SERIES.values():
        for sid in series_dict:
            data[sid] = fetch_fred_series(sid, FRED_API_KEY)
            log.info(f"  {sid}: {data[sid]}")

    def fmt(sid, unit="", precision=2):
        result = data.get(sid)
        if result:
            val, date = result
            return f"{val:.{precision}f}{unit} (as of {date})"
        return "N/A"

    lines = [
        "# Macro State",
        f"_Updated: {ts}_",
        "",
        "## Policy",
    ]

    fedfunds = data.get("FEDFUNDS")
    if fedfunds:
        lines.append(f"- Fed Funds Rate: {fedfunds[0]:.2f}% (as of {fedfunds[1]})")
    else:
        lines.append("- Fed Funds Rate: N/A")

    dfedtarl = data.get("DFEDTARL")
    dfedtaru = data.get("DFEDTARU")
    if dfedtarl and dfedtaru:
        lines.append(f"- Fed Funds Target: {dfedtarl[0]:.2f}–{dfedtaru[0]:.2f}%")
    elif dfedtaru:
        lines.append(f"- Fed Funds Target Upper: {dfedtaru[0]:.2f}%")
    else:
        lines.append("- Fed Funds Target: N/A")

    lines += ["", "## Yield Curve"]

    dgs2 = data.get("DGS2")
    dgs10 = data.get("DGS10")
    dgs30 = data.get("DGS30")
    t10y2y = data.get("T10Y2Y")

    lines.append(f"- 2Y Treasury: {dgs2[0]:.2f}%" if dgs2 else "- 2Y Treasury: N/A")
    lines.append(f"- 10Y Treasury: {dgs10[0]:.2f}%" if dgs10 else "- 10Y Treasury: N/A")
    lines.append(f"- 30Y Treasury: {dgs30[0]:.2f}%" if dgs30 else "- 30Y Treasury: N/A")
    if t10y2y:
        bps = t10y2y[0] * 100
        qualifier = "INVERTED" if bps < -10 else ("FLAT" if bps <= 10 else "NORMAL")
        lines.append(f"- 10Y-2Y Spread: {bps:.0f}bps ({qualifier})")
    else:
        lines.append("- 10Y-2Y Spread: N/A")

    lines += ["", "## Inflation"]

    cpiaucsl = data.get("CPIAUCSL")
    pcepilfe = data.get("PCEPILFE")
    t10yie = data.get("T10YIE")

    if cpiaucsl:
        lines.append(f"- CPI YoY: {cpiaucsl[0]:.2f} (index) (as of {cpiaucsl[1]})")
    else:
        lines.append("- CPI YoY: N/A")

    if pcepilfe:
        lines.append(f"- Core PCE: {pcepilfe[0]:.2f} (index) (as of {pcepilfe[1]})")
    else:
        lines.append("- Core PCE: N/A")

    lines.append(f"- 10Y Breakeven Inflation: {t10yie[0]:.2f}%" if t10yie else "- 10Y Breakeven Inflation: N/A")

    lines += ["", "## Growth"]

    gdp = data.get("A191RL1Q225SBEA")
    unrate = data.get("UNRATE")
    icsa = data.get("ICSA")
    indpro = data.get("INDPRO")

    if gdp:
        lines.append(f"- Real GDP Growth: {gdp[0]:.2f}% (as of {gdp[1]})")
    else:
        lines.append("- Real GDP Growth: N/A")

    if unrate:
        lines.append(f"- Unemployment Rate: {unrate[0]:.1f}% (as of {unrate[1]})")
    else:
        lines.append("- Unemployment Rate: N/A")

    if icsa:
        lines.append(f"- Initial Jobless Claims: {icsa[0]:.0f}K (as of {icsa[1]})")
    else:
        lines.append("- Initial Jobless Claims: N/A")

    if indpro:
        lines.append(f"- Industrial Production: {indpro[0]:.2f} (index) (as of {indpro[1]})")
    else:
        lines.append("- Industrial Production: N/A")

    lines += ["", "## Credit"]

    hy = data.get("BAMLH0A0HYM2")
    ig = data.get("BAMLC0A0CM")
    usd = data.get("DTWEXBGS")

    if hy:
        lines.append(f"- HY Credit Spread: {hy[0]:.0f}bps (as of {hy[1]})")
    else:
        lines.append("- HY Credit Spread: N/A")

    if ig:
        lines.append(f"- IG Credit Spread: {ig[0]:.0f}bps (as of {ig[1]})")
    else:
        lines.append("- IG Credit Spread: N/A")

    if usd:
        lines.append(f"- Trade-Weighted USD: {usd[0]:.2f} (index) (as of {usd[1]})")
    else:
        lines.append("- Trade-Weighted USD: N/A")

    lines += ["", "## Sentiment"]

    umcsent = data.get("UMCSENT")
    vixcls = data.get("VIXCLS")

    if umcsent:
        lines.append(f"- U Michigan Consumer Sentiment: {umcsent[0]:.1f} (index) (as of {umcsent[1]})")
    else:
        lines.append("- U Michigan Consumer Sentiment: N/A")

    lines.append(f"- VIX: {vixcls[0]:.2f} (as of {vixcls[1]})" if vixcls else "- VIX: N/A")

    lines += ["", "## Liquidity"]

    bogmbase = data.get("BOGMBASE")
    if bogmbase:
        lines.append(f"- Monetary Base: {bogmbase[0]:,.1f} billion USD (as of {bogmbase[1]})")
    else:
        lines.append("- Monetary Base: N/A")

    # Regime Signal Summary — auto-computed from fetched data
    regime = _compute_regime_summary(data)
    lines += [
        "",
        "## Regime Signal Summary",
        "_Auto-computed from above data_",
        f"- Growth: {regime['growth']} — based on GDP + unemployment + industrial production",
        f"- Inflation: {regime['inflation']} — based on CPI + core PCE + breakeven",
        f"- Financial Conditions: {regime['financial_conditions']} — based on credit spreads + USD + VIX",
        f"- Policy: {regime['policy']} — based on Fed Funds + target range",
    ]

    # Norgate futures prices (optional — skipped if norgatedata not installed)
    try:
        import norgatedata
        lines += ["", "## Futures Prices (Norgate — Continuous Front Month)"]
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
    log.info(f"[FRED] Written to {output_path}")


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
