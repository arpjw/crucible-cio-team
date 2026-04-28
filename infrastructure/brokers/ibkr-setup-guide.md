# IBKR Pro Fund Account Setup Guide

Interactive Brokers Pro is the recommended broker for emerging systematic managers. This guide covers account setup, API configuration, and the ib_insync connection used by Crucible's position reconciler and order router.

---

## 1. Account Type Selection

Choose the right account structure before applying. Changing it later requires a new application.

| Structure | When to Use | Key Constraint |
|-----------|-------------|----------------|
| **Individual** | Solo GP, trading your own capital only | Cannot accept outside investors |
| **LLC / Corporation** | Entity trading its own capital, single owner | Cannot pool investor capital without additional registration |
| **Investment Advisor (RIA)** | Managing separate accounts for clients | Requires RIA registration (SEC or state), IBKR Advisor agreement |
| **Hedge Fund** | Pooled investment vehicle (LP or LLC fund) | Requires fund documents, beneficial ownership disclosure, auditor |

For most early-stage systematic funds: open an **LLC account** under your fund entity. This is sufficient for sub-$150M AUM and keeps the structure clean when you bring in LPs later.

---

## 2. Documents Required for LLC Account

Have these ready before starting the application. IBKR will reject the application without them.

- **Certificate of Formation** (or Certificate of Organization) — filed with your state
- **EIN Confirmation Letter** (IRS Form CP-575 or SS-4) — your entity's tax ID
- **Operating Agreement** — signed, including member names and ownership percentages
- **Beneficial Ownership Form** — IBKR's own form, certifying individuals owning ≥25% of the entity
- **Government-issued ID** for each beneficial owner (passport or driver's license)
- **Proof of Address** for the entity (utility bill, bank statement, or formation filing showing address)

If your fund has a Delaware LP structure (GP entity + LP entity), you will need formation documents for both entities and the LP agreement.

---

## 3. Application Process

1. Go to [ibkr.com](https://www.ibkr.com) → Open Account → Select account type
2. Complete the application for the LLC entity (not yourself personally)
3. Upload all documents listed above — scan quality must be legible
4. IBKR compliance review: typically 3–7 business days for entity accounts
5. Fund the account: wire from the LLC's bank account (personal funding will fail compliance)

**Minimum deposit**: $10,000 for a Pro account. No minimum for a paper trading account (paper trading is separate — set it up regardless).

---

## 4. TWS vs. IB Gateway

Two software options for API access:

| Software | Use Case | Notes |
|----------|----------|-------|
| **Trader Workstation (TWS)** | Development, monitoring, manual override | Full GUI. Requires clicking "Accept" on API connection dialog each session. Restarts daily at a configured time. |
| **IB Gateway** | Production / automated pipeline | Headless. No GUI confirmation dialogs. Preferred for scripts and Docker. Lower memory footprint. |

**Recommendation**: Use TWS for initial setup and testing. Switch to IB Gateway for production cron jobs and Docker deployments.

### TWS Installation

1. Download TWS from the IBKR software page
2. Log in with your IBKR credentials
3. Go to **Edit → Global Configuration → API → Settings**
4. Check: **Enable ActiveX and Socket Clients**
5. Set Socket Port: **7497** (live) or **7496** (paper)
6. Check: **Allow connections from localhost only** (unless running remote)
7. Uncheck: **Read-Only API** (required for order submission)
8. Click OK and restart TWS

### IB Gateway Installation

1. Download IB Gateway from the IBKR software page
2. Same API settings as TWS, but configured via the Gateway login screen
3. Socket Port: **4002** (live) or **4001** (paper) — different from TWS defaults

---

## 5. API Access Activation

After enabling the socket in TWS/Gateway:

1. Log in to the IBKR account management portal
2. Navigate to **Settings → API → Trusted IP Addresses**
3. Add `127.0.0.1` (localhost) if running locally
4. Add your server IP if running remotely

IBKR requires explicit IP whitelisting for API connections. Connections from non-whitelisted IPs will be refused silently.

---

## 6. Paper Trading Account

Set up a paper trading account before connecting to live. IBKR provides one automatically with most accounts.

1. Log in to Account Management → Paper Trading → Create Paper Trading Account
2. Paper trading uses port **7496** (TWS) or **4001** (Gateway)
3. Paper trading reflects live market data but uses simulated fills

Always test ib_insync connection and order submission logic on paper before touching live.

---

## 7. ib_insync Connection Setup

`ib_insync` is the recommended Python wrapper for the IBKR API. It wraps the native `ibapi` in an asyncio-friendly interface.

### Install

```bash
pip install ib_insync
```

### Basic Connection

```python
from ib_insync import IB, util

util.startLoop()  # Required in Jupyter notebooks; omit in scripts

ib = IB()
# TWS live: host='127.0.0.1', port=7497, clientId=1
# TWS paper: host='127.0.0.1', port=7496, clientId=1
# Gateway live: host='127.0.0.1', port=4002, clientId=1
ib.connect('127.0.0.1', 7497, clientId=1)

print(f"Connected: {ib.isConnected()}")
print(f"Account: {ib.managedAccounts()}")
```

### Pull Account Summary

```python
account_summary = ib.accountSummary()
for item in account_summary:
    if item.tag in ('NetLiquidation', 'TotalCashValue', 'GrossPositionValue'):
        print(f"{item.tag}: {item.value} {item.currency}")
```

### Pull Current Positions

```python
positions = ib.positions()
for pos in positions:
    contract = pos.contract
    print(f"{contract.symbol} {contract.secType} | avg cost: {pos.avgCost:.4f} | size: {pos.position}")
```

### Submit a Market Order

```python
from ib_insync import Future, MarketOrder

# Define contract — ES front month
contract = Future('ES', '20250321', 'CME')
ib.qualifyContracts(contract)  # Fills in missing contract details

order = MarketOrder('BUY', 1)
trade = ib.placeOrder(contract, order)
ib.sleep(2)  # Wait for fill
print(trade.orderStatus.status)
print(trade.fills)
```

### Disconnect

```python
ib.disconnect()
```

---

## 8. Relevant API Endpoints Summary

| Operation | ib_insync Method | Notes |
|-----------|-----------------|-------|
| Account summary | `ib.accountSummary()` | NAV, cash, gross position value |
| Positions | `ib.positions()` | All open positions across all accounts |
| Portfolio | `ib.portfolio()` | Positions with current market value and unrealized P&L |
| Open orders | `ib.openOrders()` | Pending unfilled orders |
| Executions | `ib.executions()` | Recent fills, with timestamps and prices |
| Place order | `ib.placeOrder(contract, order)` | Returns Trade object with status stream |
| Cancel order | `ib.cancelOrder(trade.order)` | Pass the Order object, not the Trade |
| Contract qualify | `ib.qualifyContracts(contract)` | Required before placing futures orders |
| Market data | `ib.reqMktData(contract)` | Streaming tick data |
| Historical bars | `ib.reqHistoricalData(contract, ...)` | OHLCV bars, up to 1 year |

---

## 9. Common Failure Modes

### "Connection refused" on port 7497

**Cause**: TWS not running, or API not enabled in TWS settings.
**Fix**: Open TWS, go to Edit → Global Configuration → API → Settings, enable socket clients, restart TWS.

### "clientId is already in use"

**Cause**: Another process is connected with the same clientId.
**Fix**: Use a different clientId integer (e.g., `clientId=2`). Each concurrent connection needs a unique clientId.

### Orders rejected with "No security definition has been found"

**Cause**: Contract not fully specified. Futures require exchange, expiry, and sometimes multiplier.
**Fix**: Always call `ib.qualifyContracts(contract)` before placing orders. This resolves the full contract specification from IBKR's database.

### API connection drops after ~10 minutes

**Cause**: TWS has an auto-logoff time configured.
**Fix**: Edit → Global Configuration → Lock and Exit → Auto-Logoff Timer → set to None, or set to a time after your session ends.

### Paper trading fills always at mid (unrealistic)

**Cause**: Expected — paper trading uses simulated fills at or near mid. It does not simulate market impact.
**Fix**: Use ib_insync's `whatIf` order flag to get margin impact estimates without submitting. For slippage modeling, use your own slippage model rather than relying on paper fills.

### "Error 200: No security definition has been found for the request" for futures

**Cause**: Expiry date format is wrong. IBKR uses `YYYYMM` for monthly contracts, not full date strings.
**Fix**: Use `Future('ES', '202503', 'CME')` not `Future('ES', '20250321', 'CME')`. For weeklies, full date is required.

### Gateway disconnects at 11:45 PM ET Sunday

**Cause**: IBKR performs weekly system resets Sunday night ET.
**Fix**: Schedule your pipeline to avoid the 11:30 PM – 12:15 AM ET window. Gateway reconnects automatically after the reset if auto-restart is configured.

---

## 10. Automated Position Sync

`scripts/sync-ibkr.py` is Crucible's read-only position bridge. It connects to IBKR, pulls live positions and account summary, and writes a structured `context/portfolio-state.md` that agents read at invocation time.

### What it writes

```
context/portfolio-state.md
  ├── Account Summary   — NAV, cash, gross exposure, leverage, margin utilization
  ├── Open Positions    — markdown table: symbol, qty, avg cost, mkt price, mkt value, unr. P&L
  ├── Risk Clusters     — auto-classified into Equity Beta / Rates / FX / Commodity
  └── Position Hash     — MD5 of sorted positions; changes on any fill or unwind
```

### How to test it

```bash
# Step 1 — verify the connection is healthy
python scripts/verify-ibkr.py

# Step 2 — run a full sync and inspect the output
python scripts/sync-ibkr.py && cat context/portfolio-state.md
```

`verify-ibkr.py` prints connection status, port, masked account number (last 4 digits only), NAV, and position count. Exits 1 on failure.

### IBKR Gateway configuration required

Before `sync-ibkr.py` can connect, TWS or IB Gateway must be configured:

1. Open TWS → **Edit → Global Configuration → API → Settings**
2. **Check: Enable ActiveX and Socket Clients** — required for any API connection
3. **Set Socket Port**: 7497 for paper trading, 7496 for live
4. **Trusted IP Addresses**: add `127.0.0.1` (localhost) — IBKR refuses non-whitelisted IPs silently
5. **Uncheck: Read-Only API** — required for position data to flow; the bridge is read-only by design but IBKR's read-only flag blocks the data subscription

### Fallback behavior

If IBKR is unreachable, `sync-ibkr.py` preserves the last known `portfolio-state.md` and appends:

```
⚠ IBKR CONNECTION FAILED — showing last known state as of {timestamp}
```

Agents will see the warning and treat portfolio data as potentially stale. The file is never left blank.

### Called automatically by the pipeline

`scripts/update-context.py` calls `sync-ibkr.py` as a subprocess after the FRED pull. An IBKR failure does not block FRED or Kalshi data — the pipeline logs the error and continues.
