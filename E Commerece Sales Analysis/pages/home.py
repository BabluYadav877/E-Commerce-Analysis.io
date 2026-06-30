"""
pages/home.py
-------------
Home / Dashboard page — KPI cards, sales trend overview, quick
category/region breakdown, and final summary insights.
"""

import streamlit as st
import plotly.express as px

from utils.theme import apply_theme, style_chart, section_header, PRIMARY, CHART_PALETTE
from utils.data_loader import load_data
from utils.metrics import (
    compute_kpis, format_currency, format_number,
    best_performing_category, peak_sales_period, generate_recommendations,
)

apply_theme()

df = st.session_state.get("df")
if df is None:
    df = load_data(None)
    st.session_state["df"] = df

# ----------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------
st.title("🏠 FlipMart Sales Dashboard")
st.markdown(
    "Welcome to the **FlipMart Analytics Dashboard** — a complete view of sales performance, "
    "customer activity, and business health at a glance."
)
st.markdown("---")

# ----------------------------------------------------------------------
# KPI Cards
# ----------------------------------------------------------------------
kpis = compute_kpis(df)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("💰 Total Sales", format_currency(kpis["total_sales"]))
c2.metric("🧾 Total Orders", format_number(kpis["total_orders"]))
c3.metric("👥 Total Customers", format_number(kpis["total_customers"]))
c4.metric("📈 Total Profit", format_currency(kpis["total_profit"]), f"{kpis['profit_margin']:.1f}% margin")
c5.metric("🔄 Orders / Customer", f"{kpis['conversion_rate']:.2f}")

st.markdown("")

# ----------------------------------------------------------------------
# Sales trend overview
# ----------------------------------------------------------------------
section_header("📈 Sales Trend Overview", "Monthly sales performance across the full dataset")

monthly = df.groupby("Year-Month", as_index=False)["Sales"].sum().sort_values("Year-Month")
fig = px.line(
    monthly,
    x="Year-Month",
    y="Sales",
    markers=True,
    color_discrete_sequence=[PRIMARY],
)
fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales ($)",
    margin=dict(t=10, b=10),
)
fig.update_traces(line=dict(width=3), fill="tozeroy", fillcolor="rgba(30,136,229,0.20)")
style_chart(fig)
st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------
# Quick breakdown row: category split + region split
# ----------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    section_header("🗂️ Sales by Category")
    cat_sales = df.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig_cat = px.pie(
        cat_sales, names="Category", values="Sales", hole=0.45,
        color_discrete_sequence=CHART_PALETTE,
    )
    fig_cat.update_layout(margin=dict(t=10, b=10))
    style_chart(fig_cat)
    st.plotly_chart(fig_cat, use_container_width=True)

with col2:
    section_header("🌍 Top 10 Regions by Sales")
    region_sales = (
        df.dropna(subset=["Region"])
        .groupby("Region", as_index=False)["Sales"].sum()
        .sort_values("Sales", ascending=False)
        .head(10)
    )
    fig_reg = px.bar(
        region_sales.sort_values("Sales"), x="Sales", y="Region", orientation="h",
        color="Sales", color_continuous_scale="Blues",
    )
    fig_reg.update_layout(margin=dict(t=10, b=10), coloraxis_showscale=False)
    style_chart(fig_reg)
    st.plotly_chart(fig_reg, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------------------
# Final Summary Insights
# ----------------------------------------------------------------------
section_header("🧠 Final Summary & Insights", "Quick takeaways and data-driven recommendations")

i1, i2 = st.columns(2)
i1.metric("🏆 Best-Performing Category", best_performing_category(df))
i2.metric("📅 Peak Sales Period", peak_sales_period(df))

st.markdown("#### 💡 Business Recommendations")
for rec in generate_recommendations(df):
    st.markdown(f"- {rec}")

st.markdown("")
st.download_button(
    "⬇️ Download Full Sales Report (CSV)",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="flipmart_sales_report.csv",
    mime="text/csv",
)

st.markdown("---")
st.info("👈 Use the sidebar menu to explore **Sales Analysis**, **Product Performance**, **Forecasting**, and **Feedback** pages.")
