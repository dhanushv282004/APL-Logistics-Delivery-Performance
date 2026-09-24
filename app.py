import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from analysis import load_data, prepare_delivery_data, delivered_only, overall_kpis, group_kpis, categorical_association


st.set_page_config(
    page_title="APL Logistics Delivery Analytics",
    page_icon="🚚",
    layout="wide",
)

st.title("🚚 Delivery Performance, Delay Risk, and Logistics Efficiency")
st.caption(
    "Interactive analysis of delivery gaps, shipping modes, markets, regions and customer segments."
)


@st.cache_data
def get_data():
    df = load_data()
    return prepare_delivery_data(df)


df = get_data()

# Core rows used for filters and delivery KPIs.
core = df.dropna(
    subset=[
        "Days for shipping (real)",
        "Days for shipment (scheduled)",
        "Late_delivery_risk",
        "Delivery Status",
        "Shipping Mode",
        "Order Region",
        "Market",
        "Customer Segment",
    ]
).copy()


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("Filters")

    shipping_modes = st.multiselect(
        "Shipping mode",
        sorted(core["Shipping Mode"].unique()),
        default=sorted(core["Shipping Mode"].unique()),
    )

    regions = st.multiselect(
        "Order region",
        sorted(core["Order Region"].unique()),
        default=sorted(core["Order Region"].unique()),
    )

    markets = st.multiselect(
        "Market",
        sorted(core["Market"].unique()),
        default=sorted(core["Market"].unique()),
    )

    segments = st.multiselect(
        "Customer segment",
        sorted(core["Customer Segment"].unique()),
        default=sorted(core["Customer Segment"].unique()),
    )

    statuses = st.multiselect(
        "Delivery status",
        sorted(core["Delivery Status"].unique()),
        default=sorted(core["Delivery Status"].unique()),
    )

    risk_options = st.multiselect(
        "Late delivery risk",
        ["Risk = 1", "Risk = 0"],
        default=["Risk = 1", "Risk = 0"],
    )

    st.info(
        "Date range selector: unavailable because the provided dataset does not contain a date field."
    )


risk_values = []
if "Risk = 1" in risk_options:
    risk_values.append(1)
if "Risk = 0" in risk_options:
    risk_values.append(0)


filtered = core[
    core["Shipping Mode"].isin(shipping_modes)
    & core["Order Region"].isin(regions)
    & core["Market"].isin(markets)
    & core["Customer Segment"].isin(segments)
    & core["Delivery Status"].isin(statuses)
    & core["Late_delivery_risk"].isin(risk_values)
].copy()


if filtered.empty:
    st.warning("No records match the selected filters. Please broaden your selection.")
    st.stop()


valid_delivered = delivered_only(filtered)
kpis = overall_kpis(filtered)


# -----------------------------
# KPI cards
# -----------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("Orders", f"{len(filtered):,}")
c2.metric("On-Time / Early", f"{kpis['on_time_delivery_rate_pct']:.2f}%")
c3.metric("Avg Delivery Gap", f"{kpis['average_delivery_gap_days']:.2f} days")
c4.metric("Late Risk Ratio", f"{kpis['late_delivery_risk_ratio_pct']:.2f}%")


# -----------------------------
# 1. Delivery Performance Overview
# -----------------------------
st.subheader("1. Delivery Performance Overview")

col1, col2 = st.columns(2)

with col1:
    status = (
        filtered["Delivery_Class"]
        .value_counts()
        .rename_axis("Delivery Class")
        .reset_index(name="Orders")
    )
    fig = px.pie(
        status,
        names="Delivery Class",
        values="Orders",
        title="Early vs On-Time vs Delayed",
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.metric(
        "Average delay among delayed deliveries",
        f"{kpis['average_delay_delayed_only_days']:.2f} days"
        if not np.isnan(kpis["average_delay_delayed_only_days"])
        else "N/A",
    )
    st.metric("Delayed delivery rate", f"{kpis['delayed_rate_pct']:.2f}%")
    st.write(
        "Delivery gap = actual shipping days − scheduled shipping days. "
        "For delivery-time KPIs, cancelled shipments are excluded because they were not completed deliveries."
    )


# -----------------------------
# 2. Delay Risk Analysis
# -----------------------------
st.subheader("2. Delay Risk Analysis")

col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(
        filtered,
        x="Delay_Gap_Days",
        nbins=20,
        title="Distribution of Delivery Delay Gap",
        labels={"Delay_Gap_Days": "Actual − Scheduled days"},
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    risk = (
        filtered["Late_delivery_risk"]
        .map({0: "Risk = 0", 1: "Risk = 1"})
        .value_counts()
        .rename_axis("Risk")
        .reset_index(name="Orders")
    )
    fig = px.bar(
        risk,
        x="Risk",
        y="Orders",
        title="Late Delivery Risk Indicator",
    )
    st.plotly_chart(fig, use_container_width=True)

st.caption(
    "The dataset's Late_delivery_risk indicator is analyzed separately from the calculated delay gap."
)


# -----------------------------
# 3. Shipping Mode Comparison
# -----------------------------
st.subheader("3. Shipping Mode Comparison")

mode = group_kpis(
    filtered,
    "Shipping Mode",
    kpis["delayed_rate_pct"],
)

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        mode,
        x="Shipping Mode",
        y="Delay_Rate",
        text="Delay_Rate",
        title="Delay Rate by Shipping Mode",
        labels={"Delay_Rate": "Delay rate (%)"},
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        mode.sort_values("Efficiency_Index", ascending=False),
        x="Shipping Mode",
        y="Efficiency_Index",
        text="Efficiency_Index",
        title="Shipping Mode Efficiency Index",
        labels={"Efficiency_Index": "Efficiency index (%)"},
    )
    st.plotly_chart(fig, use_container_width=True)

st.dataframe(mode.round(3), use_container_width=True)


# -----------------------------
# 4. Regional & Market Diagnostics
# -----------------------------
st.subheader("4. Regional & Market Diagnostics")

col1, col2 = st.columns(2)

with col1:
    region = group_kpis(filtered, "Order Region", kpis["delayed_rate_pct"])
    fig = px.bar(
        region.head(15),
        x="Delay_Rate",
        y="Order Region",
        orientation="h",
        title="Top Regions by Delay Rate",
        labels={"Delay_Rate": "Delay rate (%)"},
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    market = group_kpis(filtered, "Market", kpis["delayed_rate_pct"])
    fig = px.bar(
        market,
        x="Market",
        y="Delay_Rate",
        text="Delay_Rate",
        title="Delay Rate by Market",
        labels={"Delay_Rate": "Delay rate (%)"},
    )
    st.plotly_chart(fig, use_container_width=True)


# Geographic scatter view using supplied coordinates.
geo = (
    filtered.groupby("Order Country", dropna=False)
    .agg(
        Latitude=("Latitude", "mean"),
        Longitude=("Longitude", "mean"),
        Delay_Rate=("Is_Delayed", "mean"),
        Orders=("Delay_Gap_Days", "size"),
    )
    .reset_index()
)
geo["Delay_Rate"] *= 100

geo = geo.dropna(subset=["Latitude", "Longitude"])

if not geo.empty:
    fig = px.scatter_geo(
        geo,
        lat="Latitude",
        lon="Longitude",
        size="Orders",
        color="Delay_Rate",
        hover_name="Order Country",
        projection="natural earth",
        title="Geographic Delay Visualization",
    )
    st.plotly_chart(fig, use_container_width=True)


# -----------------------------
# 5. Customer Segment Impact
# -----------------------------
st.subheader("5. Customer Segment Impact")

segment = group_kpis(
    filtered,
    "Customer Segment",
    kpis["delayed_rate_pct"],
)

fig = px.bar(
    segment,
    x="Customer Segment",
    y="Delay_Rate",
    text="Delay_Rate",
    title="Delay Rate by Customer Segment",
    labels={"Delay_Rate": "Delay rate (%)"},
)
st.plotly_chart(fig, use_container_width=True)

st.dataframe(segment.round(3), use_container_width=True)


# -----------------------------
# 6. Statistical Diagnostics
# -----------------------------
st.subheader("6. Statistical Diagnostics")

assoc_mode = categorical_association(filtered, "Shipping Mode")
assoc_market = categorical_association(filtered, "Market")
assoc_segment = categorical_association(filtered, "Customer Segment")

stats_rows = pd.DataFrame([
    ["Shipping Mode", assoc_mode["chi_square"], assoc_mode["p_value"], assoc_mode["cramers_v"]],
    ["Market", assoc_market["chi_square"], assoc_market["p_value"], assoc_market["cramers_v"]],
    ["Customer Segment", assoc_segment["chi_square"], assoc_segment["p_value"], assoc_segment["cramers_v"]],
], columns=["Variable", "Chi_Square", "P_Value", "Cramers_V"])

st.dataframe(stats_rows.round(5), use_container_width=True)

st.info(
    "Interpretation rule: statistical association does not prove causation. "
    "Use effect size, sample size and operational context together."
)


# -----------------------------
# Download
# -----------------------------
st.download_button(
    "Download filtered data",
    filtered.to_csv(index=False).encode("utf-8"),
    "filtered_apl_logistics_delivery.csv",
    "text/csv",
)
