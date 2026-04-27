# Risk Limits

<!-- Fill in your fund's actual risk limits. These are hard constraints enforced by all agents. -->

## Portfolio-Level Limits

| Metric | Limit | Current | Status |
|---|---|---|---|
| Gross Leverage | [e.g., 5× NAV] | [PLACEHOLDER] | |
| Net Leverage | [e.g., 2× NAV] | [PLACEHOLDER] | |
| Daily VaR (95%) | [e.g., 1.5% NAV] | [PLACEHOLDER] | |
| Max Monthly Drawdown Trigger | [e.g., 5% NAV — halt new positions] | | |
| Max Portfolio Drawdown | [e.g., 15% NAV — reduce to 50% risk] | | |

## Position-Level Limits

| Metric | Limit |
|---|---|
| Max Single Position (% NAV) | [e.g., 3%] |
| Max Single Position (% Daily ADV) | [e.g., 10%] |
| Max Loss per Trade (% NAV) | [e.g., 0.5%] |
| Max Holding Period (if signal decays) | [e.g., 60 days] |

## Concentration Limits

| Bucket | Limit |
|---|---|
| Single Asset Class | [e.g., 40% gross exposure] |
| Single Country/Region | [e.g., 30% gross exposure] |
| Single Sector (equities) | [e.g., 20% gross exposure] |
| Single Currency | [e.g., 25% gross exposure] |
| Correlated Cluster (ρ > 0.6) | [e.g., treat as single position] |

## Liquidity Limits

| Metric | Limit |
|---|---|
| Max % NAV in instruments with > 5-day liquidation | [e.g., 15%] |
| Minimum bid-ask spread for new positions | [e.g., < 5 bps for rates; < 10 bps for FX] |

## Regulatory Reporting Thresholds

| Rule | Threshold | Action |
|---|---|---|
| CFTC Large Trader (futures) | [Applicable threshold per contract] | Report within 1 business day |
| SEC 13F (equities) | $100M AUM | Quarterly filing |
| Other | [PLACEHOLDER] | [PLACEHOLDER] |

## Escalation Protocol

- **Yellow**: Within 80% of any limit → notify PM, increase monitoring frequency
- **Orange**: Within 95% of any limit → halt new risk-adding trades in affected bucket
- **Red**: Limit breached → immediate risk reduction, notify CRO and investors per policy
