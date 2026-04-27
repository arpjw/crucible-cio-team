# Kalshi API Setup Guide

Kalshi is a regulated prediction market exchange. Crucible's `/kalshi-reader` agent uses Kalshi market probabilities to surface consensus divergence signals and convert binary probabilities into regime weights. This guide covers account setup, the Python client, and the daily context update.

---

## 1. Account Creation

1. Go to [kalshi.com](https://kalshi.com)
2. Create an account — US residents only (regulatory requirement)
3. Complete identity verification (KYC): government ID + SSN last 4
4. Fund the account (minimum $10 to access all markets via API)
5. Navigate to **Account Settings → API Keys → Create API Key**
6. Copy your API key and email

Add to `.env`:
```bash
KALSHI_API_KEY=your_key_here
KALSHI_EMAIL=your_email@example.com
```

**Note**: Kalshi offers two environments — demo and production. Use the demo environment (`demo-api.kalshi.co`) for testing. The API structure is identical; only the base URL changes.

---

## 2. Python Client Installation

Kalshi provides an official Python client:

```bash
pip install kalshi-python
```

Or install directly from the Kalshi GitHub if the PyPI version is outdated:

```bash
pip install git+https://github.com/Kalshi/kalshi-python.git
```

---

## 3. Connection and Authentication

```python
import os
import kalshi_python
from kalshi_python.models import LoginRequest
from dotenv import load_dotenv

load_dotenv()

# Configure client
config = kalshi_python.Configuration(host="https://trading-api.kalshi.com/trade-api/v2")
api_client = kalshi_python.ApiClient(config)
auth_api = kalshi_python.AuthApi(api_client)

# Login — returns a token stored in the session
login_response = auth_api.login(
    LoginRequest(email=os.environ["KALSHI_EMAIL"], password=os.environ["KALSHI_PASSWORD"])
)
config.api_key["Authorization"] = login_response.token
config.api_key_prefix["Authorization"] = "Bearer"

markets_api = kalshi_python.MarketApi(api_client)
```

**Note**: Kalshi moved to API key-based auth in 2024. If using an API key directly (not email/password), set:
```python
config.api_key["Authorization"] = os.environ["KALSHI_API_KEY"]
config.api_key_prefix["Authorization"] = "Bearer"
```

---

## 4. Pull Current Market Probabilities

```python
def get_market_probability(ticker: str) -> dict | None:
    """
    Pull current yes/no probability for a Kalshi market.
    Returns dict with yes_price, no_price, volume, and implied_probability.
    """
    try:
        market = markets_api.get_market(ticker=ticker)
        yes_price = market.market.yes_ask / 100  # Kalshi prices in cents (0-100)
        return {
            "ticker": ticker,
            "title": market.market.title,
            "yes_probability": yes_price,
            "no_probability": 1 - yes_price,
            "volume_24h": market.market.volume_24h,
            "open_interest": market.market.open_interest,
            "close_time": market.market.close_time,
        }
    except Exception as e:
        print(f"[Kalshi] Error fetching {ticker}: {e}")
        return None


# Example
fed_market = get_market_probability("FED-25DEC-T525")
print(f"Fed holds at 5.25%: {fed_market['yes_probability']:.1%}")
```

### Search for Markets by Keyword

```python
def search_markets(query: str, limit: int = 10) -> list[dict]:
    """Search for active markets matching a keyword."""
    results = markets_api.get_markets(
        status="open",
        series_ticker=query,  # or use 'title' search depending on API version
        limit=limit
    )
    return [
        {
            "ticker": m.ticker,
            "title": m.title,
            "yes_price": m.yes_ask,
            "close_time": m.close_time,
        }
        for m in results.markets
    ]
```

---

## 5. Core Market Categories for Macro Trading

The 15 most relevant Kalshi market categories for a systematic macro fund. Check [kalshi.com/markets](https://kalshi.com/markets) for current active tickers within each category — tickers update each event cycle.

### Federal Reserve Policy

| Category | What It Answers | Why It Matters |
|----------|----------------|----------------|
| **Fed Funds Rate — Meeting Outcome** | Will the Fed cut/hold/hike at the next FOMC? | Direct signal for rates regime; compare to CME FedWatch |
| **Year-End Fed Funds Rate** | Where does the market see rates by Dec 31? | Cumulative easing/tightening expectations |
| **Fed Pause Length** | How many meetings until the next rate change? | Forward guidance confidence gauge |

### Inflation

| Category | What It Answers | Why It Matters |
|----------|----------------|----------------|
| **CPI Release Outcome** | Will CPI print above/below consensus? | Inflation regime confirmation |
| **Core PCE Outcome** | Will core PCE be above/below X%? | Fed's preferred measure — policy-relevant |
| **Breakeven vs. Realized** | Will 10Y breakeven diverge from realized? | Inflation expectations alignment |

### Growth and Labor

| Category | What It Answers | Why It Matters |
|----------|----------------|----------------|
| **GDP Growth — Quarterly** | Will GDP come in above/below consensus? | Growth regime signal |
| **Recession Probability** | Will the US enter recession in the next 12m? | Tail risk pricing |
| **Unemployment Rate** | Will the unemployment rate exceed X%? | Labor market regime |
| **NFP Print** | Will nonfarm payrolls beat consensus? | Risk-on/off positioning |

### Elections and Policy

| Category | What It Answers | Why It Matters |
|----------|----------------|----------------|
| **Presidential Election** | Who wins the next presidential election? | Long-dated policy regime |
| **Congressional Control** | Which party controls the House/Senate? | Fiscal policy constraints |
| **Debt Ceiling Resolution** | Will the debt ceiling be raised by X date? | Liquidity cliff event |

### Geopolitical / Other

| Category | What It Answers | Why It Matters |
|----------|----------------|----------------|
| **Oil Price** | Will WTI close above/below $X on date Y? | Energy and inflation signal |
| **Equity Index Level** | Will the S&P 500 be above X by Y date? | Sentiment / tail risk |

---

## 6. Converting Kalshi Probabilities to Regime Weights

The `/kalshi-reader` agent expects probabilities in the format written to `context/kalshi-state.md`. The conversion logic:

```python
def kalshi_to_regime_weight(
    yes_probability: float,
    category: str,
    signal_direction: str = "bullish"
) -> float:
    """
    Convert a binary Kalshi probability to a regime weight in [-1, +1].

    yes_probability: float in [0, 1] from Kalshi market
    signal_direction: 'bullish' if yes=good for risk, 'bearish' if yes=bad for risk
    Returns: weight in [-1, +1], where 0 = neutral, ±1 = maximum conviction
    """
    # Center around 0.5 (neutral), scale to [-1, 1]
    centered = (yes_probability - 0.5) * 2  # [-1, +1]

    if signal_direction == "bearish":
        centered = -centered

    return round(centered, 3)


# Examples
# Fed hike probability = 0.15 → bearish for risk assets
hike_weight = kalshi_to_regime_weight(0.15, "fed_policy", "bearish")
# 0.15 centered = -0.70, bearish flip → +0.70 (bullish: less hike = good for risk)

# Recession probability = 0.35 → bearish for risk assets
recession_weight = kalshi_to_regime_weight(0.35, "recession", "bearish")
# 0.35 centered = -0.30, bearish flip → +0.30

print(f"Fed hike weight: {hike_weight}")     # +0.70
print(f"Recession weight: {recession_weight}")  # +0.30
```

**Consensus divergence flag**: `/kalshi-reader` flags any market where the Kalshi probability diverges from analyst consensus by ≥15 percentage points. This requires a parallel consensus data source (Bloomberg survey or Fed model) — see `data-pipeline-guide.md` for the full implementation.

---

## 7. Daily Pull → context/kalshi-state.md

```python
from datetime import datetime


KALSHI_MARKETS = [
    # (ticker_pattern, category, signal_direction, description)
    # Update tickers each FOMC/event cycle — these are template patterns
    ("KXFEDRATE",   "fed_policy",   "bearish",  "Fed Funds Rate — next meeting"),
    ("KXCPI",       "inflation",    "bearish",  "CPI above consensus"),
    ("KXGDP",       "growth",       "bullish",  "GDP above consensus"),
    ("KXUNRATE",    "labor",        "bearish",  "Unemployment above threshold"),
    ("KXRECESSION", "recession",    "bearish",  "US Recession next 12m"),
    ("KXSPX",       "equity",       "bullish",  "S&P 500 level by year-end"),
]


def write_kalshi_state(output_path: str = "context/kalshi-state.md") -> None:
    """Pull Kalshi markets and write current probabilities to kalshi-state.md."""
    lines = [
        "# Kalshi State\n",
        f"*Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}*\n",
        "\n## Market Probabilities\n",
    ]
    for ticker, category, direction, description in KALSHI_MARKETS:
        result = get_market_probability(ticker)
        if result:
            weight = kalshi_to_regime_weight(result["yes_probability"], category, direction)
            flag = " **[CONSENSUS DIVERGENCE]**" if abs(weight) > 0.30 else ""
            lines.append(
                f"- **{description}** (`{ticker}`): "
                f"{result['yes_probability']:.1%} yes | "
                f"regime weight: {weight:+.3f}{flag}"
            )
        else:
            lines.append(f"- **{description}** (`{ticker}`): UNAVAILABLE")

    with open(output_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[Kalshi] Written to {output_path}")
```

---

## Notes

- Kalshi tickers change each event cycle. A ticker like `KXFEDRATE-25DEC-T525` expires after the December 2025 FOMC meeting. You need to update tickers in `KALSHI_MARKETS` after each event resolves.
- Kalshi market hours: markets trade 24/7 but liquidity concentrates around market hours and event windows.
- The free tier allows read-only API access. Writing orders requires a funded account.
- Kalshi is a CFTC-regulated exchange, not a securities exchange — no securities regulations apply to prediction market contracts.
- For a complete list of current active markets and their tickers, use `search_markets()` or browse [kalshi.com/markets](https://kalshi.com/markets) directly.
