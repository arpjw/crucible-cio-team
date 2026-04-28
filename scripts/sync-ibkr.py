#!/usr/bin/env python3
"""
IBKR position bridge.
Reads live positions and account summary from Interactive Brokers and writes
context/portfolio-state.md. Called by scripts/update-context.py as a subprocess,
but can also be run standalone.

Requires: TWS or IB Gateway running with API enabled on IBKR_PORT.
See infrastructure/brokers/ibkr-setup-guide.md for setup instructions.
"""

import os
import sys
import json
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

OUTPUT_PATH = PROJECT_ROOT / "context" / "portfolio-state.md"

# Symbol → risk cluster lookup
RISK_BUCKETS: dict[str, set[str]] = {
    "equity_beta": {"ES", "NQ", "RTY", "YM", "MES", "MNQ", "MYM", "M2K"},
    "rates":       {"ZN", "ZB", "ZF", "ZT", "ZQ", "UB"},
    "fx":          {"6E", "6J", "6B", "6A", "6C", "6S", "6N", "M6E", "M6A", "M6B"},
    "commodity":   {"GC", "SI", "CL", "NG", "HG", "RB", "HO", "PL", "PA"},
}


def _classify_symbol(symbol: str) -> str:
    sym = symbol.upper()
    for bucket, symbols in RISK_BUCKETS.items():
        if sym in symbols:
            return bucket
    return "other"


def connect_ibkr(host: str, port: int, client_id: int):
    """Connect to IBKR Gateway or TWS. Returns a connected IB instance.

    Reads IBKR_HOST (default 127.0.0.1), IBKR_PORT (default 7497),
    IBKR_CLIENT_ID (default 1) from .env. Raises ConnectionError with a
    clear message if the connection cannot be established.
    """
    try:
        from ib_insync import IB, util
        util.patchAsyncio()
    except ImportError:
        raise ImportError("ib_insync is not installed — run: pip install ib_insync")

    ib = IB()
    try:
        ib.connect(host, port, clientId=client_id, timeout=15)
    except Exception as e:
        raise ConnectionError(
            f"Could not connect to IBKR at {host}:{port} (clientId={client_id}): {e}. "
            "Ensure TWS or IB Gateway is running with API enabled."
        ) from e

    if not ib.isConnected():
        raise ConnectionError(
            f"Connection to IBKR at {host}:{port} (clientId={client_id}) failed — "
            "check that API sockets are enabled and the trusted IP is whitelisted."
        )

    log.info(f"[IBKR] Connected to {host}:{port} (clientId={client_id})")
    return ib


def get_positions(ib) -> list[dict]:
    """Fetch all open positions with market data and P&L.

    Uses ib.portfolio() to get market values and unrealized P&L alongside
    the position details. Filters out zero-quantity rows from recently
    closed positions.
    """
    items = ib.portfolio()
    positions = []
    for item in items:
        if item.position == 0:
            continue
        c = item.contract
        positions.append({
            "symbol":         c.symbol,
            "exchange":       c.exchange or getattr(c, "primaryExch", "") or "",
            "currency":       c.currency,
            "quantity":       item.position,
            "avg_cost":       item.averageCost,
            "market_price":   item.marketPrice,
            "market_value":   item.marketValue,
            "unrealized_pnl": item.unrealizedPnL,
            "realized_pnl":   item.realizedPnL,
        })
        log.info(
            f"  {c.symbol}: qty={item.position:,.0f} | "
            f"avg={item.averageCost:.4f} | mkt={item.marketPrice:.4f} | "
            f"mkt_val={item.marketValue:,.0f} | unr_pnl={item.unrealizedPnL:,.0f}"
        )
    return positions


def get_account_summary(ib) -> dict:
    """Fetch key account tags from IBKR.

    Returns: NetLiquidation, TotalCashValue, GrossPositionValue,
    MaintMarginReq, InitMarginReq, AvailableFunds (all in USD).
    """
    target_tags = {
        "NetLiquidation",
        "TotalCashValue",
        "GrossPositionValue",
        "MaintMarginReq",
        "InitMarginReq",
        "AvailableFunds",
    }
    summary = ib.accountSummary()
    tags: dict[str, float] = {}
    for item in summary:
        if item.tag not in target_tags:
            continue
        # Prefer the BASE currency row (IBKR's base currency, typically USD)
        if item.currency in ("USD", "BASE"):
            try:
                val = float(item.value)
                if item.tag not in tags or item.currency == "USD":
                    tags[item.tag] = val
            except ValueError:
                pass
    for tag in target_tags:
        if tag in tags:
            log.info(f"  {tag}: {tags[tag]:,.2f}")
    return tags


def write_portfolio_state(
    positions: list[dict],
    account: dict,
    output_path: Path = OUTPUT_PATH,
) -> None:
    """Write structured portfolio-state.md from fetched positions and account data."""
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    nav   = account.get("NetLiquidation", 0.0)
    cash  = account.get("TotalCashValue", 0.0)
    gross = account.get("GrossPositionValue", 0.0)
    maint = account.get("MaintMarginReq", 0.0)
    avail = account.get("AvailableFunds", 0.0)

    gross_lev   = (gross / nav) if nav > 0 else 0.0
    margin_util = (maint / nav * 100) if nav > 0 else 0.0

    lines = [
        "# Portfolio State",
        f"_Updated: {ts}_",
        "_Source: IBKR live sync_",
        "",
        "## Account Summary",
        f"- NAV: ${nav:,.2f}",
        f"- Cash: ${cash:,.2f}",
        f"- Gross Exposure: ${gross:,.2f}",
        f"- Gross Leverage: {gross_lev:.2f}x",
        f"- Margin Utilization: {margin_util:.1f}% ({maint:,.0f} used / {nav:,.0f} NAV)",
        f"- Available Funds: ${avail:,.2f}",
    ]

    # Open Positions table
    lines += ["", "## Open Positions"]
    if positions:
        lines.append("| Symbol | Qty | Avg Cost | Mkt Price | Mkt Value | Unr. PnL |")
        lines.append("|--------|-----|----------|-----------|-----------|----------|")
        for p in positions:
            lines.append(
                f"| {p['symbol']} "
                f"| {p['quantity']:,.0f} "
                f"| {p['avg_cost']:.4f} "
                f"| {p['market_price']:.4f} "
                f"| ${p['market_value']:,.0f} "
                f"| ${p['unrealized_pnl']:,.0f} |"
            )
    else:
        lines.append("_No open positions_")

    # Risk Clusters — classify each position and compute NAV exposure per bucket
    clusters: dict[str, list[str]] = {
        "equity_beta": [], "rates": [], "fx": [], "commodity": [], "other": [],
    }
    cluster_exposure: dict[str, float] = {k: 0.0 for k in clusters}
    for p in positions:
        bucket = _classify_symbol(p["symbol"])
        clusters[bucket].append(p["symbol"])
        cluster_exposure[bucket] += abs(p["market_value"])

    lines += ["", "## Risk Clusters", "_Auto-computed from position list_"]
    main_buckets = [
        ("equity_beta", "Equity Beta"),
        ("rates",       "Rates"),
        ("fx",          "FX"),
        ("commodity",   "Commodity"),
    ]
    for bucket, label in main_buckets:
        syms = clusters[bucket]
        pct = (cluster_exposure[bucket] / nav * 100) if nav > 0 else 0.0
        sym_str = ", ".join(syms) if syms else "—"
        lines.append(f"- {label}: {sym_str} ({pct:.1f}% NAV)")

    if clusters["other"]:
        pct = (cluster_exposure["other"] / nav * 100) if nav > 0 else 0.0
        lines.append(f"- Other: {', '.join(clusters['other'])} ({pct:.1f}% NAV)")

    # Position Hash — MD5 of sorted symbol|qty|avg_cost rows
    # Detects any fill, partial unwind, or avg cost drift between runs
    table_content = "\n".join(
        f"{p['symbol']}|{p['quantity']}|{p['avg_cost']:.6f}"
        for p in sorted(positions, key=lambda x: x["symbol"])
    )
    pos_hash = hashlib.md5(table_content.encode()).hexdigest()
    lines += ["", "## Position Hash", pos_hash]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n")
    log.info(f"[IBKR] Written to {output_path} ({len(positions)} position(s))")


def fallback_to_last_known(output_path: Path, error_msg: str) -> None:
    """Preserve the last known portfolio state and append a staleness warning.

    Never leaves portfolio-state.md blank — agents must always have something
    to read even if IBKR is unreachable.
    """
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    if output_path.exists():
        existing = output_path.read_text()
        # Extract the timestamp from the _Updated: line
        last_ts = "unknown"
        for line in existing.splitlines()[:4]:
            if line.startswith("_Updated:"):
                last_ts = line.replace("_Updated:", "").strip().strip("_").strip()
                break
        warning_block = (
            "\n---\n"
            f"⚠ IBKR CONNECTION FAILED — showing last known state as of {last_ts}\n"
            f"Error: {error_msg}\n"
            f"Attempted: {ts}\n"
        )
        output_path.write_text(existing.rstrip() + "\n" + warning_block)
        log.warning(f"[IBKR] Fallback: appended stale warning to existing state")
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            "# Portfolio State\n"
            f"_Updated: {ts}_\n"
            "_Source: fallback — IBKR unavailable_\n\n"
            f"⚠ IBKR CONNECTION FAILED — no prior state available\n"
            f"Error: {error_msg}\n\n"
            "Start TWS or IB Gateway and run `python scripts/sync-ibkr.py` to populate.\n"
        )
        log.warning(f"[IBKR] Fallback: no prior state found — wrote blank with error notice")


def main() -> None:
    host      = os.environ.get("IBKR_HOST", "127.0.0.1")
    port      = int(os.environ.get("IBKR_PORT", "7497"))
    client_id = int(os.environ.get("IBKR_CLIENT_ID", "1"))

    ib = None
    try:
        ib = connect_ibkr(host, port, client_id)
        positions = get_positions(ib)
        account   = get_account_summary(ib)
        write_portfolio_state(positions, account)
    except Exception as e:
        log.error(f"[IBKR] Sync failed: {e}")
        fallback_to_last_known(OUTPUT_PATH, str(e))
        sys.exit(1)
    finally:
        if ib is not None:
            try:
                if ib.isConnected():
                    ib.disconnect()
                    log.info("[IBKR] Disconnected")
            except Exception:
                pass


if __name__ == "__main__":
    main()
