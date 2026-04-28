#!/usr/bin/env python3
"""
IBKR connection health check.

Attempts to connect to IBKR, fetches account summary and positions,
and prints a status report:
  - Connection status
  - Port used
  - Account number (masked — last 4 digits only)
  - NAV
  - Position count

Exits with code 1 if connection fails.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def main() -> None:
    host      = os.environ.get("IBKR_HOST", "127.0.0.1")
    port      = int(os.environ.get("IBKR_PORT", "7497"))
    client_id = int(os.environ.get("IBKR_CLIENT_ID", "1"))

    print(f"\nIBKR Connection Check — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Target: {host}:{port} (clientId={client_id})")
    print("─" * 50)

    try:
        from ib_insync import IB, util
        util.patchAsyncio()
    except ImportError:
        print("RESULT: FAILED — ib_insync not installed")
        print("  Run: pip install ib_insync")
        sys.exit(1)

    ib = IB()
    try:
        ib.connect(host, port, clientId=client_id, timeout=15)
    except Exception as e:
        print(f"RESULT: FAILED — {e}")
        print()
        print("Troubleshooting:")
        print("  1. Open TWS or IB Gateway")
        print("  2. Enable API: Edit → Global Configuration → API → Settings")
        print("     → Enable ActiveX and Socket Clients")
        print("     → Set Socket Port to match IBKR_PORT in .env")
        print("  3. Whitelist 127.0.0.1 in Trusted IP Addresses")
        print("  4. Uncheck Read-Only API to allow data flow")
        sys.exit(1)

    if not ib.isConnected():
        print("RESULT: FAILED — connect() returned but isConnected() is False")
        sys.exit(1)

    # Mask account number: show only last 4 characters
    accounts = ib.managedAccounts()
    acct_raw  = accounts[0] if accounts else "UNKNOWN"
    acct_masked = f"***{acct_raw[-4:]}" if len(acct_raw) >= 4 else "***"

    # Fetch account summary
    nav = None
    summary = ib.accountSummary()
    for item in summary:
        if item.tag == "NetLiquidation" and item.currency in ("USD", "BASE"):
            try:
                nav = float(item.value)
                break
            except ValueError:
                pass

    # Fetch one position (just count them)
    positions = ib.portfolio()
    pos_count = sum(1 for p in positions if p.position != 0)

    ib.disconnect()

    print(f"Connection:  OK")
    print(f"Port:        {port}")
    print(f"Account:     {acct_masked}")
    print(f"NAV:         ${nav:,.2f}" if nav is not None else "NAV:         N/A")
    print(f"Positions:   {pos_count}")
    print()
    print("RESULT: OK — IBKR connection healthy")
    print(f"  Run `python scripts/sync-ibkr.py` to write context/portfolio-state.md")


if __name__ == "__main__":
    main()
