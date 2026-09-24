# Delivery Performance, Delay Risk, and Logistics Efficiency Analysis

## Project objective

This project analyzes delivery performance in a global supply-chain dataset by comparing actual shipping duration with scheduled duration. It identifies delay patterns across shipping modes, regions, markets and customer segments and provides an interactive Streamlit dashboard.

> **Research note:** statistical association does not prove causation. The analysis is descriptive and observational.

## Dataset

`data/APL_Logistics.csv`

- Rows: **180,519**
- Columns: **40**
- Duplicate rows: **0**
- Missing values in core delivery/grouping fields: **0**
- Encoding handled in Python: UTF-8 / CP1252 / Latin-1 fallback

## Delivery-gap definition

**Delay Gap = Days for shipping (real) − Days for shipment (scheduled)**

- Delayed: gap > 0
- On-time: gap = 0
- Early: gap < 0

Cancelled shipments are retained for operational status analysis but excluded from completed-delivery timing KPIs.

## Main KPIs

- On-Time Delivery Rate (%)
- Average Delivery Delay (Days)
- Late Delivery Risk Ratio (%)
- Shipping Mode Efficiency Index
- Regional Delay Index

## Key observed results

- On-time-or-early rate: **42.71%**
- Calculated delayed-delivery rate: **57.29%**
- Average delivery gap: **0.565 days**
- Average delay among delayed deliveries: **1.618 days**
- Late delivery risk indicator: **54.83%**
- Shipping Mode Cramér's V: **0.4020**
- Order Region Cramér's V: **0.0219**
- Market Cramér's V: **0.0074**
- Customer Segment Cramér's V: **0.0048**

## Streamlit dashboard

`app.py` contains:

1. Delivery Performance Overview
2. Delay Risk Analysis
3. Shipping Mode Comparison
4. Regional & Market Diagnostics
5. Customer Segment Impact
6. Statistical Diagnostics
7. Filtered-data download

Filters include shipping mode, order region, market, customer segment, delivery status and `Late_delivery_risk`.

**Date range:** the provided dataset has no explicit date column, so the dashboard documents this limitation instead of creating a synthetic time filter.

## Google Colab

Notebook: `notebooks/APL_Logistics_Delivery_Analysis.ipynb`

The notebook supports direct CSV upload and automatically tries common encodings.

## Project structure

```text
APL_Logistics_Delivery_Performance_Project/
├── data/
│   └── APL_Logistics.csv
├── notebooks/
│   └── APL_Logistics_Delivery_Analysis.ipynb
├── results/
│   ├── kpi_summary.csv
│   ├── delivery_status_summary.csv
│   ├── shipping_mode_summary.csv
│   ├── order_region_summary.csv
│   ├── market_summary.csv
│   ├── customer_segment_summary.csv
│   ├── order_country_summary.csv
│   ├── association_tests.csv
│   ├── risk_vs_delivery_class.csv
│   └── figures/
├── analysis.py
├── app.py
├── requirements.txt
├── README.md
├── research_report.md
├── executive_summary.md
└── .gitignore
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
