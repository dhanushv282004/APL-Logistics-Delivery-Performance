# Research Report
## Delivery Performance, Delay Risk, and Logistics Efficiency Analysis in Global Supply Chain Operations

### Abstract

This study analyzes delivery performance and delay risk using the provided APL Logistics supply-chain dataset. The analysis calculates the delivery delay gap as actual shipping days minus scheduled shipping days, classifies deliveries as Early, On-time or Delayed, and compares performance across shipping modes, regions, markets and customer segments.

The dataset contains **180,519 orders and 40 fields**. The required delivery fields contain no missing values, and there are no duplicate rows. For delivery-time KPIs, **7,754 cancelled orders (4.30%)** are excluded because they were not completed deliveries. Across the **172,765 non-cancelled deliveries**, **42.71% were on-time or early** and **57.29% were delayed** under the project's gap-based definition. The mean delivery gap was **0.565 days**, while the mean positive delay among delayed deliveries was **1.618 days**. The dataset's `Late_delivery_risk` indicator was 54.83%, which is analyzed separately from the calculated delay gap.

Shipping mode showed a substantial difference in calculated delay performance. First Class had a 100% delay rate in this dataset, Second Class 79.83%, Same Day 47.93%, and Standard Class 39.77%. The observed association between shipping mode and calculated delivery class was strong relative to the other categorical variables examined (Cramér's V ≈ 0.402). By contrast, customer segment showed only a small association (Cramér's V ≈ 0.005). These findings are descriptive and do not establish causal effects.

### 1. Background and Context

In large-scale global logistics operations, delivery delays can cause service-level problems, increase operational cost and reduce customer satisfaction. Comparing actual delivery time with scheduled delivery time creates a simple diagnostic measure of where logistics performance is meeting or missing planned timelines.

This project applies operational analytics to identify delay patterns across shipping modes, regions, markets and customer segments.

### 2. Problem Statement

The project addresses the need to:

- measure on-time versus delayed deliveries;
- understand shipping-mode differences;
- identify regions and markets with higher delay intensity;
- compare delay exposure across customer segments; and
- provide an operational dashboard for drill-down analysis.

### 3. Dataset Description

The dataset `APL_Logistics.csv` contains **180,519 observations and 40 columns** covering payment/order type, delivery timing, financial values, customer information, geography, market, order status, product information and shipping mode.

Key analytical fields include:

- Days for shipping (real)
- Days for shipment (scheduled)
- Delivery Status
- Late_delivery_risk
- Shipping Mode
- Order Region
- Order Country
- Market
- Customer Segment
- Latitude / Longitude
- Sales
- Order Profit Per Order

No missing values were found in the core delivery and grouping fields used for the analysis. The dataset contains **0 duplicate rows**. A total of 11 missing cells exist elsewhere in the dataset, but they do not affect the core delivery calculations.

### 4. Methodology

#### 4.1 Data cleaning and validation

The CSV was loaded and validated for required fields, missing values and duplicates. The dataset uses a Windows-compatible character encoding, so the analysis loader supports UTF-8, CP1252 and Latin-1.

#### 4.2 Delivery gap calculation

For each order:

**Delay Gap = Days for shipping (real) − Days for shipment (scheduled)**

The resulting classification is:

- **Delayed:** gap > 0
- **On-time:** gap = 0
- **Early:** gap < 0

For delivery-time KPIs, cancelled shipments are excluded because they were not completed deliveries. The `Late_delivery_risk` field is retained and analyzed separately rather than treated as identical to the calculated delivery class.

#### 4.3 Overall delivery performance

The study calculates:

- on-time-or-early delivery rate;
- calculated delayed-delivery rate;
- average delivery gap;
- average positive delay among delayed deliveries;
- `Late_delivery_risk` ratio; and
- cancelled-order rate.

#### 4.4 Shipping-mode efficiency

Delivery performance is compared by Shipping Mode. The **Shipping Mode Efficiency Index** is defined as the percentage of non-cancelled shipments whose actual shipping time is less than or equal to the scheduled time.

#### 4.5 Regional and market diagnostics

The analysis compares delay rates by Order Region, Order Country and Market.

The **Regional Delay Index** is:

**Regional Delay Index = Regional delay rate / Overall delay rate × 100**

A value of 100 represents the overall delay rate for the selected dataset.

#### 4.6 Customer segment analysis

Delay rates are compared across Consumer, Corporate and Home Office customer segments.

#### 4.7 Statistical diagnostics

Chi-square tests and Cramér's V are used to quantify the association between the calculated Delivery_Class and selected categorical variables.

### 5. KPI Definitions

**On-Time Delivery Rate (%)**  
Percentage of non-cancelled shipments with actual shipping days less than or equal to scheduled shipping days.

**Average Delivery Delay (Days)**  
Mean of actual shipping days minus scheduled shipping days across non-cancelled deliveries.

**Average Delay (Delayed Orders Only)**  
Mean positive delivery gap among delayed non-cancelled shipments.

**Late Delivery Risk Ratio (%)**  
Mean value of the dataset's `Late_delivery_risk` indicator, expressed as a percentage.

**Shipping Mode Efficiency Index**  
Percentage of non-cancelled shipments in a shipping mode with actual shipping time less than or equal to scheduled time.

**Regional Delay Index**  
Regional delay rate relative to the overall delay rate, multiplied by 100.

### 6. Results

#### 6.1 Data quality and baseline performance

| Measure | Result |
|---|---:|
| Total orders | 180,519 |
| Total columns | 40 |
| Duplicate rows | 0 |
| Core delivery fields with missing values | 0 |
| Cancelled orders | 7,754 (4.30%) |
| Non-cancelled deliveries | 172,765 |
| On-time-or-early rate | **42.71%** |
| Calculated delayed-delivery rate | **57.29%** |
| Average delivery gap | **0.565 days** |
| Average positive delay among delayed orders | **1.618 days** |
| `Late_delivery_risk = 1` rate | **54.83%** |

The calculated delivery gap is positive on average, indicating that actual shipping time exceeded scheduled shipping time across the non-cancelled delivery population.

#### 6.2 Delivery class distribution

Among all core-valid records, the calculated delivery class was:

| Delivery Class | Orders | Share |
|---|---:|---:|
| Delayed | 103,400 | 57.28% |
| Early | 43,366 | 24.02% |
| On-time | 33,753 | 18.70% |

For the completed/non-cancelled delivery KPI population, the relevant combined on-time-or-early rate is **42.71%**, with a delayed rate of **57.29%**.

#### 6.3 Shipping mode performance

| Shipping Mode | Orders | Delay Rate | On-Time/Early Rate | Avg Gap (Days) | Efficiency Index |
|---|---:|---:|---:|---:|---:|
| Standard Class | 103,153 | 39.77% | 60.23% | -0.006 | 60.23 |
| Same Day | 9,293 | 47.93% | 52.07% | 0.479 | 52.07 |
| Second Class | 33,806 | 79.83% | 20.17% | 1.993 | 20.17 |
| First Class | 26,513 | 100.00% | 0.00% | 1.000 | 0.00 |

First Class and Second Class show much higher calculated delay rates than Same Day and Standard Class in this dataset. The First Class result is especially notable because every non-cancelled First Class record has a positive delay gap under the supplied values.

The chi-square test for Shipping Mode versus Delivery_Class yielded **χ² = 55,825.50, p < 0.001**, with **Cramér's V = 0.402**.

#### 6.4 Regional diagnostics

Using regions with at least 100 non-cancelled orders to avoid extremely small groups, **Central Africa** had the highest observed delay rate at approximately **60.15%**, while **Canada** had the lowest at approximately **51.60%**.

The corresponding Regional Delay Index values were approximately **104.99** and **90.07**, respectively. The results show variation across regions, but the absolute differences are much smaller than the differences observed across shipping modes.

Across all regions, the dataset's delivery-time performance should be interpreted in conjunction with shipping-mode composition because shipping mode and geography are not independent operational factors.

#### 6.5 Market diagnostics

| Market | Orders | Delay Rate | On-Time/Early Rate | Avg Gap (Days) |
|---|---:|---:|---:|---:|
| Africa | 11,154 | 56.84% | 43.16% | 0.562 |
| LATAM | 49,309 | 56.87% | 43.13% | 0.554 |
| Pacific Asia | 39,585 | 57.37% | 42.63% | 0.569 |
| USCA | 24,627 | 57.41% | 42.59% | 0.575 |
| Europe | 48,090 | 57.69% | 42.31% | 0.569 |

Market-level differences are relatively small. Europe has the highest observed delay rate at **57.69%**, while Africa has the lowest at **56.84%**.

The Market versus Delivery_Class association was statistically detectable but very small in effect size: **χ² = 18.856, p = 0.0157, Cramér's V = 0.0074**.

#### 6.6 Customer segment impact

| Customer Segment | Orders | Delay Rate | On-Time/Early Rate | Avg Gap (Days) |
|---|---:|---:|---:|---:|
| Consumer | 89,420 | 57.31% | 42.69% | 0.566 |
| Corporate | 52,528 | 57.08% | 42.92% | 0.557 |
| Home Office | 30,817 | 57.59% | 42.41% | 0.579 |

Customer-segment delay rates are very close. The chi-square test gave **χ² = 7.913, p = 0.0948**, with **Cramér's V = 0.0048**, indicating a negligible association between Customer Segment and calculated Delivery_Class.

#### 6.7 Late-delivery risk indicator versus calculated delay

The dataset's `Late_delivery_risk` variable is not identical to the calculated delay class. All `Late_delivery_risk = 1` records were in the Delayed class, but **4,423 records with `Late_delivery_risk = 0` were still classified as delayed** by the actual-vs-scheduled calculation.

This difference is important: the project therefore reports `Late_delivery_risk` and the calculated delay gap as two distinct operational signals rather than assuming they are interchangeable.

#### 6.8 Statistical association summary

| Variable | Chi-square | p-value | Cramér's V |
|---|---:|---:|---:|
| Shipping Mode | 55,825.50 | <0.001 | **0.4020** |
| Order Region | 166.42 | <0.001 | **0.0219** |
| Market | 18.86 | 0.0157 | **0.0074** |
| Customer Segment | 7.91 | 0.0948 | **0.0048** |

The strongest association among the tested grouping variables is Shipping Mode. Region, Market and Customer Segment have much smaller effect sizes.

### 7. Discussion

The analysis identifies shipping mode as the clearest segmentation dimension associated with calculated delivery delay in the provided dataset. Standard Class and Same Day have higher on-time-or-early rates than Second Class and First Class, while First Class shows a 100% delayed rate under the supplied actual-versus-scheduled shipping-day values.

The regional results show much narrower differences. The highest regional delay rate among sufficiently sized regions is about 60%, compared with about 52% for the lowest. Market-level differences are similarly narrow, and customer-segment differences are small.

The distinction between `Late_delivery_risk` and the calculated delay gap is also operationally important. Because the two measures are not identical, a logistics dashboard should retain both as separate indicators. A risk flag may represent a predefined operational label, while the delay gap directly compares actual and planned shipping duration.

The findings are observational. The strong shipping-mode association does not, by itself, prove that a particular shipping mode causes delays. Shipping modes can be selected under different service commitments, routes, order characteristics, destinations and operational conditions.

### 8. Recommendations

1. Monitor actual-versus-scheduled delivery gaps alongside the `Late_delivery_risk` indicator rather than using either measure in isolation.
2. Investigate the large differences across shipping modes, especially First Class and Second Class, using route, service-level and order-level context.
3. Use Regional Delay Index values for monitoring regional deviations from the overall baseline.
4. Use customer-segment analysis primarily for monitoring because the observed segment-level effect is small in this dataset.
5. Retain cancelled shipments as a separate operational category instead of treating them as completed late deliveries.
6. Validate any shipping-mode or regional intervention using additional operational variables and longitudinal or controlled analysis.

### 9. Limitations

- The dataset does not contain an explicit date/time field, so a true date-range trend analysis could not be performed.
- The delivery KPIs exclude cancelled orders because they were not completed deliveries.
- The dataset contains both `Late_delivery_risk` and actual/scheduled shipping-day fields, and these two indicators are not identical.
- The analysis is observational and cannot establish causality.
- Some geographic groups are much smaller than others.
- The project does not incorporate route distance, carrier capacity, weather, customs clearance, congestion or other external logistics drivers.
- The Shipping Mode Efficiency Index is a project-specific descriptive KPI and is not a universal industry benchmark.

### 10. Conclusion

This project provides a diagnostic view of delivery performance using actual-versus-scheduled shipping duration. In the provided dataset, **57.29% of non-cancelled deliveries were delayed**, while **42.71% were on-time or early**, with an average delivery gap of **0.565 days**.

The strongest observed segmentation difference was associated with **Shipping Mode**, where delay rates ranged from **39.77% for Standard Class to 100% for First Class** under the supplied data. The Shipping Mode versus calculated delivery class association had **Cramér's V = 0.402**. By comparison, Customer Segment had a negligible association (**Cramér's V = 0.0048**), and market-level differences were small (**Cramér's V = 0.0074**).

The analysis therefore supports a logistics-monitoring approach that combines delivery-gap measurement, risk indicators, shipping-mode diagnostics and regional monitoring. Further operational data and causal designs would be needed before attributing delays to any single factor.
