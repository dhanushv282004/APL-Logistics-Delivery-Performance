# Executive Summary
## Delivery Performance, Delay Risk, and Logistics Efficiency Analysis in Global Supply Chain Operations

### Purpose

This project evaluates delivery performance and delay risk using the APL Logistics supply-chain dataset. It provides a diagnostic framework for monitoring actual versus scheduled shipping time across shipping modes, regions, markets and customer segments.

### Headline findings

- **180,519 orders** across **40 fields** were analyzed.
- **7,754 cancelled orders (4.30%)** were separated from completed-delivery KPIs.
- Among **172,765 non-cancelled deliveries**, **42.71% were on-time or early** and **57.29% were delayed**.
- The average delivery gap was **0.565 days**.
- The average positive delay among delayed deliveries was **1.618 days**.
- The `Late_delivery_risk` indicator was **54.83%**, showing that this predefined flag is not identical to the actual-vs-scheduled delay calculation.
- Shipping mode showed the largest observed association with calculated delivery class (**Cramér's V = 0.402**).
- Standard Class had a calculated efficiency index of **60.23**, Same Day **52.07**, Second Class **20.17**, and First Class **0.00**.
- Customer-segment differences were small (**Cramér's V = 0.0048**).

### Operational implications

The largest visible variation in this dataset occurs across shipping modes. This makes shipping-mode diagnostics an important monitoring layer for logistics operations. Regional differences exist but are narrower, while customer-segment differences are comparatively small.

The dashboard should be used to identify where investigation is needed rather than as proof that a shipping mode or region causes delays. Additional information such as route distance, carrier, capacity, congestion, customs and time-series data would improve operational diagnosis.

### Recommended monitoring framework

**1. Delivery gap:** monitor actual minus scheduled days.

**2. Late risk flag:** monitor the supplied `Late_delivery_risk` indicator separately.

**3. Shipping mode:** monitor delay rate and efficiency index by mode.

**4. Regional deviation:** monitor Regional Delay Index against the overall baseline.

**5. SLA exposure:** use customer and market breakdowns to identify where delayed orders may affect service commitments.

### Limitation

The supplied dataset contains no explicit date field, so this project does not claim to provide a true time-series trend analysis. The results are descriptive and observational.
