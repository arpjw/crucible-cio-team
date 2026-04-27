# Strategy Starter Packs

Three pre-built strategy templates for Crucible. Each pack is self-contained: signal construction, context file defaults, backtest parameters, and the specific Crucible agents most relevant to that strategy.

## How to Use

**Option 1 — Via `/setup`:** When running the onboarding wizard, select a strategy type. The wizard will automatically copy the appropriate context defaults into `context/`.

**Option 2 — Manual drop-in:** Copy the files from `strategies/<pack>/context-defaults/` into `context/` directly, then customize the values for your specific fund.

```
cp strategies/tsmom/context-defaults/fund-mandate.md context/fund-mandate.md
cp strategies/tsmom/context-defaults/risk-limits.md context/risk-limits.md
```

After copying, edit both files to reflect your actual AUM, legal entity, prime broker, and any deviations from the template defaults.

---

## Strategy Packs

### 1. Time-Series Momentum (`strategies/tsmom/`)

A systematic trend-following strategy using price momentum signals across a diversified futures universe. The edge comes from behavioral underreaction to information and the structural demand from risk-parity and CTA funds that amplify trends. Returns are negatively skewed relative to equities, making TSMOM an effective portfolio hedge in crisis periods.

**Typical instrument universe:** 20–30 liquid futures across FX, rates, equity indices, and commodities — global developed markets, with selective EM exposure in liquid instruments only.

**AUM capacity ceiling:** $500M–$2B depending on instrument universe breadth. Capacity is primarily constrained by market impact in smaller commodity and EM futures contracts. A concentrated 10-instrument universe hits the ceiling well below $500M; a diversified 30-instrument universe can scale toward $2B before significant alpha erosion.

**Best for:** New funds wanting a well-documented, academically-validated systematic strategy with liquid instruments and a clear backtesting benchmark (SG Trend Index).

---

### 2. Carry (`strategies/carry/`)

A systematic carry-harvesting strategy across FX, rates, and commodities. The edge is compensation for crash risk — carry strategies earn a steady premium that periodically reverses sharply during risk-off events. Diversification across asset classes and dynamic drawdown controls are critical to managing the left-tail exposure.

**Typical instrument universe:** G10 FX futures, rates futures across 6+ jurisdictions, commodity futures with positive roll yield. Primarily developed markets, with EM FX only for highly liquid pairs.

**AUM capacity ceiling:** $1–5B for diversified carry across all three asset classes. FX carry alone is highly capacity-constrained below $1B in EM exposure; developed-market rates carry scales to the upper end of the range.

**Best for:** Funds wanting a complementary strategy to TSMOM (carry and trend are historically uncorrelated at the strategy level) or a standalone lower-volatility systematic approach.

---

### 3. Macro Discretionary (`strategies/macro-discretionary/`)

A regime-based positioning strategy that takes concentrated directional views across asset classes, driven by macro regime identification. The "systematic" aspect is the regime framework and falsifiability requirements — position decisions remain judgment-based but must pass a documented pre-trade checklist. This prevents post-hoc rationalization and makes the strategy auditable.

**Typical instrument universe:** Broader than pure systematic strategies — futures as the primary vehicle, with potential OTC (swaps, forwards) if licensed. Opportunistic across equities, rates, FX, and commodities with no fixed allocation.

**AUM capacity ceiling:** Unconstrained at small AUM ($0–$100M). Liquidity limitations in concentrated macro themes emerge above $500M. True macro funds managing $1B+ require significant OTC access to avoid moving listed futures markets.

**Best for:** PMs with strong macro views who want a systematic framework around their decision-making process — the Crucible agents are especially valuable here to pressure-test discretionary views before execution.
