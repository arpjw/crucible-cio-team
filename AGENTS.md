# Crucible CIO Team — Agent Registry

37 agents across 6 layers. Each entry: invocation command, one-sentence function, and the exact verdict or stamp the agent produces.

---

## Layer 0 — Governance

Pre-trade decision review. Five independent adversarial agents plus one full-panel meta-command. Run before any trade, strategy deployment, or portfolio change.

| Agent | Command | Function | Key Output |
|---|---|---|---|
| Compliance Officer | `/compliance` | Checks trade permissibility against fund mandate, regulatory limits, LP alignment, and disclosure obligations. | `COMPLIANCE VERDICT: VIOLATION \| WARNING \| CLEAR` |
| Risk Officer | `/risk` | Evaluates position sizing, VaR contribution, drawdown headroom, correlation clustering, and tail scenarios. | `RISK VERDICT: BLOCKED \| FLAGGED \| APPROVED` |
| Macro Analyst | `/macro` | Challenges macro thesis coherence, regime identification, cross-asset consistency, and historical analog quality. | `MACRO VERDICT: OPPOSED \| CONDITIONAL \| ALIGNED` |
| Signal Researcher | `/signal` | Stress-tests signal statistical validity, overfitting exposure, regime robustness, and live/backtest parity. | `SIGNAL VERDICT: REJECTED \| FLAGGED \| VALIDATED` |
| Systems Architect | `/systems` | Audits execution infrastructure, data pipeline integrity, latency budget, and deployment readiness. | `SYSTEMS VERDICT: BLOCKED \| CONDITIONAL \| CLEAR` |
| **Full Panel** | `/crucible` | Runs all five governance agents in sequence and synthesizes a binding panel verdict. | `NO-GO \| CONDITIONAL GO \| GO` |

**Panel sequence:** Compliance → Risk → Macro → Signal → Systems. Compliance runs first because a mandate violation is not a risk management question.

---

## Layer 1 — Operations

Continuous monitoring. These agents run in parallel to the rest of the stack — daily, intra-day, or at end-of-month as noted.

| Agent | Command | Function | Key Output |
|---|---|---|---|
| Drawdown Monitor | `/drawdown-monitor` | Tracks drawdown velocity, depth, and correlation profile to trigger circuit breakers at four escalation levels. | `DRAWDOWN STATUS: MONITOR \| WARN \| SUSPEND \| HALT` |
| Vendor Monitor | `/vendor-monitor` | Monitors data feed health, staleness, silent failure patterns, and switchover risk across all market data sources. | `FEED STATUS` per instrument: `LIVE \| STALE \| FAILED \| SWITCHOVER` |
| Audit Logger | `/audit-logger` | Enforces five required elements of a complete pre-trade record and gates trades on completeness. | `COMPLETE \| INCOMPLETE` |
| Cash Manager | `/cash-manager` | Tracks margin utilization, per-position headroom, cash drag, and margin call triggers across the portfolio. | `MARGIN STATUS: OK \| WARNING \| CRITICAL` |
| NAV Calculator | `/nav-calculator` | Verifies daily NAV integrity by checking price sources, staleness, corporate actions, and cross-source consistency. | `STAMP: VERIFIED \| VERIFIED WITH NOTES \| UNVERIFIED` |
| LP Reporter | `/lp-reporter` | Drafts the LP letter with period return attribution, drawdown narrative, risk metrics, and disclosure scan. | `DRAFT` stamp + disclosure checklist |
| Tax Tracker | `/tax-tracker` | Monitors tax lot holding periods, wash sale exposure, harvest opportunities, and after-tax return impact. | `TAX STATUS` with lot-level harvest flags |
| Macro Scanner | `/macro-scanner` | Produces a daily four-dimension regime state digest with Kalshi overlay and portfolio implications. | Regime state machine output + `REGIME CHANGE DETECTED` flag |
| Event Calendar | `/event-calendar` | Builds a 30-day event risk calendar with ATR-based impact models and sizing recommendations for critical windows. | `EVENT RISK — REVIEW POSITION \| EVENT RISK — MONITOR \| NO MATERIAL EVENT RISK` |
| Kalshi Reader | `/kalshi-reader` | Reads prediction market signals, flags consensus divergence ≥15pp, and converts to regime-weighted signals. | `HIGH SIGNAL \| NO SIGNAL`; `POLICY SHIFT SIGNAL` |

---

## Layer 2 — Intelligence

Market context generation. These agents produce structured outputs consumed by Governance agents — particularly the Regime Classifier's `REGIME_STATE` block, which feeds the Macro Analyst directly.

| Agent | Command | Function | Key Output |
|---|---|---|---|
| Flow Analyst | `/flow-analyst` | Analyzes CFTC COT data for net positioning percentile, OI rate-of-change, and mechanical squeeze severity. | `CROWDED \| ELEVATED \| NEUTRAL \| CONTRARIAN` per instrument |
| Sentiment Tracker | `/sentiment-tracker` | Scores news sentiment against a 30-day baseline and flags price-sentiment divergence and rapid narrative shifts. | `NARRATIVE SHIFT \| STABLE \| DIVERGENCE` |
| Earnings Watcher | `/earnings-watcher` | Monitors corporate event risk using implied vs. historical move, vol premium, and beat/miss rates. | `EARNINGS RISK HIGH \| MODERATE \| LOW` |
| Regime Classifier | `/regime-classifier` | Produces a machine-readable four-dimension regime state and confidence score, consumed by Governance agents. | `REGIME_STATE` block + `REGIME CLASSIFICATION` with confidence |

---

## Layer 3 — Research

Signal development and portfolio sizing. These agents validate new alpha ideas before they reach Governance, and produce target allocations that feed the Execution layer's Rebalancer.

| Agent | Command | Function | Key Output |
|---|---|---|---|
| Signal Generator | `/signal-generator` | Proposes regime-consistent, non-redundant alpha hypotheses grounded in mechanism — explicitly not validated. | `HYPOTHESIS — NOT VALIDATED` stamp |
| Backtest Designer | `/backtest-designer` | Runs a seven-check spec review covering universe, regime coverage, cost model, timing, holdout, benchmark, and power. | `SPEC APPROVED \| SPEC REQUIRES REVISION` |
| Correlation Mapper | `/correlation-mapper` | Audits eight-factor loadings, pairwise correlations under normal and stress regimes, and portfolio diversification score. | `APPROVED \| REDUNDANT \| CONCENTRATION WARNING` |
| Capacity Estimator | `/capacity-estimator` | Calculates AUM ceiling using the square-root impact model at 1/5/10% ADV and flags when AUM approaches that ceiling. | `CAPACITY CONSTRAINED` flag when AUM is within 3× of ceiling |
| Decay Tracker | `/decay-tracker` | Compares rolling 3m/6m/12m live vs. backtest Sharpe and classifies the signal's decay curve shape. | Health score 0–100 + decay curve: `linear \| exponential \| episodic` |
| Portfolio Optimizer | `/portfolio-optimizer` | Computes target allocations via risk parity or mean-variance, enforces hard constraints, and identifies binding constraints. | `ALLOCATION COMPLETE \| REBALANCE TRIGGER \| URGENT REBALANCE \| BINDING CONSTRAINT ACTIVE` |

---

## Layer 4 — Execution

Order management and fill quality. These agents receive verdicts from Governance and target allocations from Research, and produce the actual trade instructions.

| Agent | Command | Function | Key Output |
|---|---|---|---|
| Order Router | `/order-router` | Selects venue and order type by instrument class, applies VWAP window, and halts orders that exceed 10% ADV. | `APPROVED \| OUTSIZED ORDER — HALT` |
| Slippage Monitor | `/slippage-monitor` | Benchmarks fills against arrival price, computes realized vs. modeled slippage ratio, and classifies broker performance. | `ACCEPTABLE \| ELEVATED \| INVESTIGATE`; `FILL DEGRADATION` flag at ratio >1.5 for 3 consecutive trades |
| Position Reconciler | `/position-reconciler` | Runs three-way reconciliation across broker, OMS, and signal register and flags breaks by type and severity. | `CLEAN \| BREAKS DETECTED`; `ORDER ROUTING GATE: CLEARED \| SUSPENDED` |
| Rebalancer | `/rebalancer` | Generates the optimal trade list from Portfolio Optimizer targets, nets trades, sequences exits first, and flags uneconomic rebalances. | `REBALANCE APPROVED — FULL \| REBALANCE APPROVED — PARTIAL \| REBALANCE UNECONOMIC \| NO REBALANCE REQUIRED` |
| Roll Manager | `/roll-manager` | Maintains a 90-day futures expiry calendar, monitors roll cost vs. 30-day average, and issues urgent roll alerts within 3 days of first notice. | `URGENT ROLL \| ROLL NOW \| ROLL COST ELEVATED` |

---

## Layer 0 — Human Roles

Institutional expertise roles. These agents model the specialized knowledge domains that underpin fund operations — model validation, infrastructure quality, fund accounting, portfolio-wide risk, LP relationships, legal compliance, and execution management. Run for targeted domain reviews or as part of periodic fund audits. Not part of the pre-trade pipeline, but foundational to everything the pipeline depends on.

| Agent | Command | Function | Key Output |
|---|---|---|---|
| Quant Researcher | `/quant-researcher` | Validates model mathematics: distributional assumptions (Jarque-Bera, kurtosis, skewness), theoretical pricing consistency, parameter stability via rolling estimation, overfitting via deflated Sharpe and SR_in/SR_out ratio, and factor model residual structure via Ljung-Box. | `MODEL VERDICT: INVALID \| CONDITIONAL \| VALIDATED` per model component |
| Infrastructure Auditor | `/infrastructure-auditor` | Reviews code quality and engineering debt: race conditions on shared mutable state, idempotency of signal calculations, dependency version pinning, error handling coverage for every external call, and a 0–100 engineering debt score with prioritized remediation list. | `INFRASTRUCTURE VERDICT: NOT READY \| CONDITIONAL \| PRODUCTION READY` |
| Fund Accountant | `/fund-accountant` | Runs full fund accounting: P&L attribution reconciled to NAV change within 0.01%, fee calculation against LPA (management fee, performance fee, HWM integrity), expense allocation (fund-borne vs. manager-borne), trial balance with double-entry check, and Big 4 audit readiness. | `ACCOUNTING VERDICT: AUDIT FAILURE \| REQUIRES REMEDIATION \| AUDIT READY` |
| Chief Risk Officer | `/chief-risk-officer` | Portfolio-wide board-level risk: parametric and historical VaR at 95%/99%, five named historical crisis stress tests (GFC, COVID, 2022 Rate Shock, 1994 Bond Massacre, LTCM 1998), days-to-liquidate vs. redemption notice, stress-period correlation breakdown (ρ=0.85 floor), and Board Risk Report with RAG status per dimension. | `PORTFOLIO RISK STATUS: RED \| AMBER \| GREEN` |
| Investor Relations | `/investor-relations` | LP relationship and capital raise: eight-section DDQ simulation with gap scoring, quarterly call preparation with top-5 LP questions and proactive disclosure flags, capital raise readiness (track record ≥12 months, ops, regulatory), LP communication audit (monthly NAV, quarterly letters, material changes), and redemption risk (LP concentration, notice vs. liquidity, gate adequacy). | `IR VERDICT: NOT READY \| CONDITIONAL \| IR READY` |
| General Counsel | `/general-counsel` | Regulatory and legal risk: exemption filing currency and threshold monitoring (CPO 4.13(a)(3), IA registration), horizon scanning for SEC/CFTC/FCA/ESMA rules with >50% finalization probability, trade legal risk (sanctions, short sale compliance, insider trading, market manipulation), counterparty legal risk (ISDA termination events, margin acceleration, re-hypothecation), and litigation risk severity scoring. | `LEGAL VERDICT: LEGAL HOLD \| LEGAL REVIEW REQUIRED \| LEGAL CLEAR` |
| Head of Trading | `/head-of-trading` | Execution quality and broker management: five-dimension broker scorecard (IS, fill rate, rejection rate, latency, commissions) with PREFERRED/ACCEPTABLE/REVIEW/TERMINATE verdict per broker, commission audit as % AUM and % gross P&L with benchmarks, prime broker fit assessment (financing rates, sec lending split, technology), execution strategy review against the square-root impact model (EXECUTION INEFFICIENCY at >30% excess), and market structure risk (fragmentation, rule changes, liquidity migration). | `EXECUTION VERDICT: RESTRUCTURE NEEDED \| REVIEW REQUIRED \| EXECUTION OPTIMIZED` |

---

## Layer 0 Extension — Deep Fund Functions

Specialized institutional functions separating top-tier systematic funds from the rest. Run for targeted domain reviews: alternative data sourcing, derivatives risk, short selling infrastructure, factor attribution, multi-strategy capital allocation, counterparty credit, ESG compliance, and LP capital development.

| Agent | Command | Function | Key Output |
|---|---|---|---|
| Alternative Data Analyst | `/alternative-data-analyst` | Evaluates data source differentiation (four-tier classification), legality (MNPI, ToS, anonymization), signal half-life via McLean & Pontiff decay model, data quality (survivorship, look-ahead from revision schedules), and break-even AUM ROI. | `DIFFERENTIATED EDGE \| COMMODITIZED EDGE \| SHORT RUNWAY \| LEGAL REVIEW REQUIRED` |
| Derivatives Desk | `/derivatives-desk` | Evaluates options overlays (IV/RV ratio, Greeks, breakeven), minimum variance hedge ratio (h* = ρσ_spot/σ_futures), OTC audit (CVA, ISDA hard block, margin), portfolio net Greeks, and 90-day expiration calendar. | `HEDGE APPROVED \| OVERPRICED HEDGE \| UNDERHEDGED \| HARD BLOCK` |
| Securities Lending | `/securities-lending` | Audits short selling infrastructure: borrow cost (GC/warm/hot/special classification, adjusted Sharpe), locate availability (SI%, DTC, institutional ownership), recall risk, dividend exposure, and short squeeze scenario with portfolio P&L impact. | `SHORT APPROVED \| BORROW COST DRAG \| LOCATE RISK HIGH \| RECALL IMMINENT \| SHORT UNECONOMIC` |
| Factor Attribution | `/factor-attribution` | Decomposes returns via Fama-French 5-factor + momentum + carry regression (R² > 70% = ALPHA ILLUSION), monitors factor loading drift (>0.3 shift), HHI factor concentration, factor-regime mismatch from REGIME_STATE, and passive replication test (>80% = REPLICABLE BY PASSIVE). | `ALPHA CONFIRMED \| ALPHA ILLUSION \| FACTOR DRIFT \| FACTOR-REGIME MISMATCH \| REPLICABLE BY PASSIVE` |
| Capital Allocator | `/capital-allocator` | Allocates risk budget across strategies (risk parity + mean-variance, flags >30% deviation), monitors cross-strategy P&L correlation (spikes >0.6), evaluates pod Sharpe (<0.3 for two quarters = UNDERPERFORMING), issues REALLOCATE/WATCH/SHUTDOWN decisions, and monitors aggregate capacity ceiling. | `OPTIMALLY ALLOCATED \| MISALLOCATED \| REBALANCE REQUIRED \| STRATEGY SHUTDOWN RECOMMENDED` |
| Counterparty Risk | `/counterparty-risk` | Maps prime broker concentration (>60% = flag, full rehypothecation = flag), computes OTC CVA (EAD × PD × LGD, >0.5% NAV = flag, no ISDA = HARD BLOCK), assesses clearing house default fund adequacy, monitors settlement fails and Herstatt FX risk, and models Lehman-style PB failure NAV impact. | `COUNTERPARTY EXPOSURE CLEAN \| CONCENTRATION WARNING \| ELEVATED COUNTERPARTY RISK \| HARD BLOCK` |
| ESG Analyst | `/esg-analyst` | Screens exclusion list (weapons, tobacco, coal >30% revenue, OFAC — HARD BLOCK on breach), computes portfolio-weighted MSCI ESG score (< BBB = POOR), calculates WACI carbon intensity (>150 tCO2e/$M = HIGH), audits governance red flags (3+ = GOVERNANCE RISK), and checks LP ESG mandate compatibility. | `ESG COMPLIANT \| EXCLUSION LIST BREACH \| POOR ESG EXPOSURE \| HIGH CARBON INTENSITY \| LP ESG INCOMPATIBILITY` |
| Business Development | `/business-development` | Audits LP pipeline (>45 days in same stage = STALLING), LP base concentration (>20% single LP = HIGH CONCENTRATION), capital raise readiness gate (10 required items), emerging manager program qualification (Fidelity, Schwab, iCapital, Deutsche Bank), and pitch effectiveness (12-point LP checklist, <3.5/5.0 = NOT READY). | `RAISE READY \| RAISE NOT READY \| PIPELINE HEALTHY \| PIPELINE STALLING` |

---

## Verdict Reference

| Verdict / Stamp | Agent | Meaning |
|---|---|---|
| `NO-GO` | Full Panel | Hard block — do not proceed |
| `CONDITIONAL GO` | Full Panel | Proceed with specified conditions |
| `GO` | Full Panel | Cleared — mandatory post-trade monitoring required |
| `VIOLATION` | Compliance | Mandate or regulatory breach — hard stop |
| `BLOCKED` | Risk / Systems | Hard stop at risk or infrastructure layer |
| `HALT` | Drawdown Monitor | Maximum circuit breaker — suspend all activity |
| `SUSPEND` | Drawdown Monitor | Reduce all positions, no new trades |
| `UNVERIFIED` | NAV Calculator | Do not distribute or report until resolved |
| `OUTSIZED ORDER — HALT` | Order Router | Order exceeds 10% ADV — do not route |
| `BREAKS DETECTED` | Position Reconciler | Reconciliation gate suspended pending resolution |
| `REBALANCE UNECONOMIC` | Rebalancer | Cost > 50% of expected Sharpe benefit — partial rebalance only |
| `SPEC REQUIRES REVISION` | Backtest Designer | Backtest may not proceed until spec deficiencies resolved |
| `HYPOTHESIS — NOT VALIDATED` | Signal Generator | Idea only — no capital allocation until /signal clears |
| `FILL DEGRADATION` | Slippage Monitor | Broker on formal review — consider reducing order flow |
| `NARRATIVE SHIFT` | Sentiment Tracker | 5-day sentiment drift > 0.3 — escalate for positioning review |
| `EARNINGS RISK HIGH` | Earnings Watcher | Hedge required before expiry |
| `CROWDED` | Flow Analyst | Extreme same-direction speculative positioning — squeeze risk elevated |
| `CAPACITY CONSTRAINED` | Capacity Estimator | AUM within 3× of ceiling — do not raise without impact model revision |
| `URGENT ROLL` | Roll Manager | ≤3 days to first notice — execute immediately |
