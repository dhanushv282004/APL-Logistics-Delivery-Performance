"""Core analytics for Delivery Performance, Delay Risk, and Logistics Efficiency."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


REQUIRED_COLUMNS = [
    "Type",
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "Benefit per order",
    "Sales per customer",
    "Delivery Status",
    "Late_delivery_risk",
    "Category Id",
    "Category Name",
    "Customer City",
    "Customer Country",
    "Customer Fname",
    "Customer Id",
    "Customer Lname",
    "Customer Segment",
    "Customer State",
    "Customer Street",
    "Customer Zipcode",
    "Department Id",
    "Department Name",
    "Latitude",
    "Longitude",
    "Market",
    "Order City",
    "Order Country",
    "Order Customer Id",
    "Order Item Discount",
    "Order Item Discount Rate",
    "Order Item Product Price",
    "Order Item Profit Ratio",
    "Order Item Quantity",
    "Sales",
    "Order Item Total",
    "Order Profit Per Order",
    "Order Region",
    "Order State",
    "Order Status",
    "Product Name",
    "Product Price",
    "Shipping Mode",
]


def load_data(path: str = "data/APL_Logistics.csv") -> pd.DataFrame:
    """Load and validate the dataset; handles common Windows encodings."""
    last_error = None
    for encoding in ("utf-8", "cp1252", "latin1"):
        try:
            df = pd.read_csv(path, encoding=encoding)
            break
        except UnicodeDecodeError as exc:
            last_error = exc
    else:
        raise last_error

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df


def prepare_delivery_data(df: pd.DataFrame) -> pd.DataFrame:
    """Create delay gap and delivery class.

    Delivery class is defined from actual vs scheduled shipping days:
    - Delayed: actual > scheduled
    - Early: actual < scheduled
    - On-time: actual == scheduled

    Cancelled shipments remain in the full analytical frame but are excluded
    from delivery-time KPIs because they were not completed deliveries.
    """
    out = df.copy()

    out["Delay_Gap_Days"] = (
        out["Days for shipping (real)"]
        - out["Days for shipment (scheduled)"]
    )

    out["Delivery_Class"] = np.select(
        [
            out["Delay_Gap_Days"] > 0,
            out["Delay_Gap_Days"] < 0,
        ],
        ["Delayed", "Early"],
        default="On-time",
    )

    out["Is_Cancelled"] = out["Delivery Status"].eq("Shipping canceled")
    out["Is_Delayed"] = out["Delay_Gap_Days"] > 0
    out["Is_On_Time_or_Early"] = out["Delay_Gap_Days"] <= 0

    return out


def delivered_only(df: pd.DataFrame) -> pd.DataFrame:
    """Return non-cancelled records for delivery-time KPIs."""
    return df.loc[~df["Is_Cancelled"]].copy()


def overall_kpis(df: pd.DataFrame) -> dict:
    """Calculate project-level delivery KPIs."""
    valid = df.dropna(
        subset=[
            "Days for shipping (real)",
            "Days for shipment (scheduled)",
            "Late_delivery_risk",
            "Delivery Status",
        ]
    )
    delivered = delivered_only(valid)

    return {
        "on_time_delivery_rate_pct": float(
            delivered["Is_On_Time_or_Early"].mean() * 100
        ),
        "average_delivery_gap_days": float(delivered["Delay_Gap_Days"].mean()),
        "average_delay_delayed_only_days": float(
            delivered.loc[delivered["Is_Delayed"], "Delay_Gap_Days"].mean()
        ),
        "late_delivery_risk_ratio_pct": float(
            valid["Late_delivery_risk"].mean() * 100
        ),
        "delayed_rate_pct": float(
            delivered["Is_Delayed"].mean() * 100
        ),
    }


def group_kpis(df: pd.DataFrame, column: str, overall_delay_rate_pct: float) -> pd.DataFrame:
    """Group delivery performance by a categorical dimension."""
    valid = delivered_only(df)

    out = (
        valid.groupby(column, dropna=False)
        .agg(
            Orders=("Delay_Gap_Days", "size"),
            Delayed=("Is_Delayed", "sum"),
            On_Time_or_Early=("Is_On_Time_or_Early", "sum"),
            Avg_Delay_Gap_Days=("Delay_Gap_Days", "mean"),
        )
        .reset_index()
    )

    out["Delay_Rate"] = out["Delayed"] / out["Orders"] * 100
    out["On_Time_or_Early_Rate"] = out["On_Time_or_Early"] / out["Orders"] * 100
    out["Efficiency_Index"] = out["On_Time_or_Early_Rate"]

    if overall_delay_rate_pct > 0:
        out["Regional_Delay_Index"] = (
            out["Delay_Rate"] / overall_delay_rate_pct * 100
        )

    return out.sort_values("Delay_Rate", ascending=False)


def categorical_association(df: pd.DataFrame, column: str) -> dict:
    """Chi-square and Cramér's V against Delivery_Class."""
    valid = delivered_only(df)
    table = pd.crosstab(valid[column], valid["Delivery_Class"])

    if min(table.shape) < 2:
        return {
            "chi_square": np.nan,
            "p_value": np.nan,
            "degrees_of_freedom": np.nan,
            "cramers_v": np.nan,
            "table": table,
        }

    chi2, p, dof, expected = stats.chi2_contingency(table)
    n = table.values.sum()
    v = np.sqrt((chi2 / n) / min(table.shape[0] - 1, table.shape[1] - 1))

    return {
        "chi_square": float(chi2),
        "p_value": float(p),
        "degrees_of_freedom": int(dof),
        "cramers_v": float(v),
        "table": table,
    }
