"""
metrics.py
----------
Helper functions for computing KPIs and summary statistics
used on the Home page and elsewhere.
"""

import pandas as pd


def compute_kpis(df: pd.DataFrame) -> dict:
    """Compute the core KPI set for the dashboard header cards."""
    total_sales = df["Sales"].sum()
    total_orders = df["Order ID"].nunique()
    total_customers = df["Customer ID"].nunique() if "Customer ID" in df.columns else 0
    total_profit = df["Profit"].sum() if "Profit" in df.columns else 0
    profit_margin = (total_profit / total_sales * 100) if total_sales else 0

    # "Conversion rate" proxy: orders per unique customer (since we don't have
    # site-visit/session data, this approximates repeat-purchase / order density)
    conversion_rate = (total_orders / total_customers) if total_customers else 0

    return {
        "total_sales": total_sales,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "total_profit": total_profit,
        "profit_margin": profit_margin,
        "conversion_rate": conversion_rate,
    }


def format_currency(value: float) -> str:
    """Format a number as a compact currency string, e.g. $1.2M."""
    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:,.0f}"


def format_number(value: float) -> str:
    """Format a number compactly, e.g. 12.3K."""
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{value:,.0f}"


def best_performing_category(df: pd.DataFrame) -> str:
    if "Category" not in df.columns or df.empty:
        return "N/A"
    return df.groupby("Category")["Sales"].sum().idxmax()


def peak_sales_period(df: pd.DataFrame) -> str:
    if df.empty:
        return "N/A"
    monthly = df.groupby("Year-Month")["Sales"].sum()
    return monthly.idxmax()


def generate_recommendations(df: pd.DataFrame) -> list:
    """Generate a few simple, data-driven business recommendations."""
    recs = []
    if df.empty:
        return ["Not enough data to generate recommendations."]

    cat_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    if len(cat_sales) > 1:
        recs.append(
            f"**{cat_sales.index[0]}** drives the most revenue — consider expanding "
            f"inventory and marketing spend in this category."
        )
        recs.append(
            f"**{cat_sales.index[-1]}** is the weakest category — review pricing, "
            f"promotions, or assortment to lift its performance."
        )

    if "Profit" in df.columns:
        profit_by_cat = df.groupby("Category")["Profit"].sum().sort_values()
        if len(profit_by_cat) and profit_by_cat.iloc[0] < 0:
            recs.append(
                f"**{profit_by_cat.index[0]}** is operating at a loss overall — "
                f"audit discounting and shipping costs in this category."
            )

    if "Region" in df.columns and df["Region"].notna().any():
        top_region = df.groupby("Region")["Sales"].sum().idxmax()
        recs.append(f"**{top_region}** is the top-performing region — prioritize logistics and stock availability there.")

    monthly = df.groupby("Year-Month")["Sales"].sum()
    if len(monthly) > 1:
        trend = "growing 📈" if monthly.iloc[-1] >= monthly.iloc[0] else "declining 📉"
        recs.append(f"Overall sales trend over the selected period is **{trend}** — adjust inventory planning accordingly.")

    return recs
