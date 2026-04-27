# Local Environment Setup

Complete setup from scratch for the Crucible data pipeline. Follow these steps in order before running any pipeline scripts.

---

## 1. Python Version

Crucible requires Python 3.11 or later. Python 3.12 is also supported.

Check your current version:
```bash
python --version
# Need: Python 3.11.x or 3.12.x
```

### Install via conda (recommended)

If you don't have conda, install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) first.

```bash
# Create the environment
conda create -n crucible python=3.11 -y
conda activate crucible

# Verify
python --version  # Python 3.11.x
which python      # Should point to conda envs/crucible/bin/python
```

### Install via pyenv (alternative)

```bash
pyenv install 3.11.9
pyenv local 3.11.9
python -m venv .venv
source .venv/bin/activate
```

---

## 2. Required Packages

Install with pinned versions to ensure reproducibility:

```bash
pip install \
  "requests==2.32.3" \
  "pandas==2.2.3" \
  "numpy==1.26.4" \
  "python-dotenv==1.0.1" \
  "ib_insync==0.9.86" \
  "kalshi-python==1.0.2" \
  "norgatedata==1.7.2" \
  "schedule==1.2.2" \
  "pytz==2024.1"
```

Or install from the requirements file:

```bash
pip install -r infrastructure/deployment/requirements.txt
```

### requirements.txt (full local environment)

Create at `infrastructure/deployment/requirements.txt`:

```
requests==2.32.3
pandas==2.2.3
numpy==1.26.4
python-dotenv==1.0.1
ib_insync==0.9.86
kalshi-python==1.0.2
norgatedata==1.7.2
schedule==1.2.2
pytz==2024.1
```

---

## 3. .env File

Create `.env` at the project root. This file is read by `python-dotenv` at runtime and by `docker-compose` for the containerized pipeline.

```bash
# .env — DO NOT COMMIT THIS FILE

# FRED (free — register at fred.stlouisfed.org)
FRED_API_KEY=your_key_here

# Kalshi (register at kalshi.com — requires funded account for full API)
KALSHI_API_KEY=your_api_key_here
KALSHI_EMAIL=your_email@example.com
KALSHI_PASSWORD=your_password_here

# IBKR (TWS or IB Gateway must be running when pipeline executes)
IBKR_HOST=127.0.0.1
IBKR_PORT=7497
IBKR_CLIENT_ID=10

# Optional: override context output paths
# CONTEXT_DIR=/path/to/crucible-cio-team/context
```

**Never commit `.env`**. Verify `.gitignore` contains it before your first commit:
```bash
grep "^\.env$" .gitignore  # Should return .env
```

If not present:
```bash
echo ".env" >> .gitignore
echo ".env.*" >> .gitignore
```

---

## 4. .gitignore Entries

Ensure these are in your `.gitignore`:

```gitignore
# Credentials
.env
.env.local
.env.*

# Python artifacts
__pycache__/
*.py[cod]
*.pyo
.venv/
*.egg-info/
dist/
build/

# Norgate database (large, licensed per-machine)
norgate_data/
*.norgatedb

# Logs
*.log
logs/

# macOS
.DS_Store
```

---

## 5. Verify Each Connection

Run these checks in order before running the full pipeline.

### FRED

```bash
python - <<'EOF'
import os, requests
from dotenv import load_dotenv
load_dotenv()
key = os.environ["FRED_API_KEY"]
r = requests.get(
    "https://api.stlouisfed.org/fred/series/observations",
    params={"series_id": "DGS10", "api_key": key, "file_type": "json", "limit": 1, "sort_order": "desc"},
    timeout=10
)
data = r.json()["observations"][0]
print(f"FRED OK — DGS10: {data['value']} on {data['date']}")
EOF
```

Expected: `FRED OK — DGS10: 4.327 on 2026-04-25`

### Norgate

```bash
python - <<'EOF'
import norgatedata
status = norgatedata.status()
print(f"Norgate status: {status}")
df = norgatedata.historic_price_dataframe(
    "&ES",
    "2026-04-20",
    "2026-04-27",
    norgatedata.StockPriceAdjustmentType.TOTALRETURN,
    norgatedata.PaddingType.NAN,
    "pandas-dataframe",
)
print(f"ES rows: {len(df)}")
print(df.tail(2))
EOF
```

Expected: Status OK, 5 rows of OHLCV data.

**Fails with**: `NorgateDataError: Could not connect to Norgate Data service` → NDU is not running. Open the NDU application.

### IBKR

TWS or IB Gateway must be running before this test. See `brokers/ibkr-setup-guide.md` for setup.

```bash
python - <<'EOF'
from ib_insync import IB, util
util.patchAsyncio()
ib = IB()
ib.connect("127.0.0.1", 7497, clientId=99, timeout=10)
print(f"IBKR connected: {ib.isConnected()}")
print(f"Account: {ib.managedAccounts()}")
summary = {i.tag: i.value for i in ib.accountSummary() if i.tag == "NetLiquidation"}
print(f"NAV: {summary.get('NetLiquidation', 'N/A')}")
ib.disconnect()
EOF
```

Expected: `IBKR connected: True` + account number + NAV value.

**Fails with**: `ConnectionRefusedError` → TWS not running or API not enabled. See IBKR guide section 4.

### Kalshi

```bash
python - <<'EOF'
import os, kalshi_python
from dotenv import load_dotenv
load_dotenv()
config = kalshi_python.Configuration(host="https://trading-api.kalshi.com/trade-api/v2")
config.api_key["Authorization"] = os.environ["KALSHI_API_KEY"]
config.api_key_prefix["Authorization"] = "Bearer"
api_client = kalshi_python.ApiClient(config)
markets_api = kalshi_python.MarketApi(api_client)
markets = markets_api.get_markets(status="open", limit=3)
print(f"Kalshi OK — {len(markets.markets)} markets retrieved")
for m in markets.markets:
    print(f"  {m.ticker}: {m.title}")
EOF
```

Expected: Three Kalshi market titles printed.

**Fails with**: `401 Unauthorized` → API key invalid or not set in `.env`.

---

## 6. Full Pipeline Test

Once all four connections pass:

```bash
cd /path/to/crucible-cio-team
conda activate crucible
python scripts/update-context.py
```

Verify output:
```bash
ls -la context/
# Should show: macro-state.md, portfolio-state.md, kalshi-state.md
# All modified within the last 2 minutes

cat context/macro-state.md
# Should show FRED readings with today's date
```

---

## 7. Common Setup Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'ib_insync'` | Wrong conda env active | `conda activate crucible` |
| `KeyError: 'FRED_API_KEY'` | `.env` not found or not loaded | Verify `.env` is in project root; run `python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.environ.get('FRED_API_KEY'))"` |
| `NorgateDataError: service not running` | NDU application not started | Open NDU from Applications |
| `ib_insync Connection timeout` | TWS not started before script | Open TWS, wait for it to fully load, then run script |
| `pip install norgatedata` fails | Norgate license not activated | Install NDU first, activate license, then install Python package |
| Python 3.10 compatibility error | Wrong Python version | `conda activate crucible` should use 3.11 — verify with `python --version` |
