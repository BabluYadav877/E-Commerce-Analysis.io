"""
pages/1_📊_Sales.py
--------------------
Sales Analysis page — trends, category breakdown, region breakdown,
with interactive date / category / region filters.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.theme import apply_theme, style_chart, section_header, PRIMARY, CHART_PALETTE
from utils.data_loader import load_data, get_filtered_data
from utils.metrics import format_currency

apply_theme()

# Reuse the already-loaded dataset if available, otherwise load fresh
df = st.session_state.get("df")
if df is None:
    df = load_data(None)
    st.session_state["df"] = df

st.title("📊 Sales Analysis")
st.markdown("Explore sales trends over time, broken down by category and region.")

# ----------------------------------------------------------------------
# Filters
# ----------------------------------------------------------------------
with st.expander("🔍 Filters", expanded=True):
    f1, f2, f3 = st.columns(3)

    min_date, max_date = df["Order Date"].min(), df["Order Date"].max()
    date_range = f1.date_input(
        "Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date
    )

    categories = f2.multiselect(
        "Category", options=sorted(df["Category"].dropna().unique()), default=[]
    )

    regions = f3.multiselect(
        "Region", options=sorted(df["Region"].dropna().unique()), default=[]
    )

filtered = get_filtered_data(
    df,
    date_range=date_range if isinstance(date_range, tuple) and len(date_range) == 2 else None,
    categories=categories or None,
    regions=regions or None,
)

st.caption(f"Showing **{len(filtered):,}** of {len(df):,} records based on current filters.")

if filtered.empty:
    st.warning("No data matches the selected filters. Try widening your date range or selections.")
    st.stop()

st.markdown("---")

# ----------------------------------------------------------------------
# Monthly / Yearly Sales Trend
# ----------------------------------------------------------------------
section_header("📈 Sales Trend", "Switch between monthly and yearly granularity")

trend_tab1, trend_tab2 = st.tabs(["Monthly", "Yearly"])

with trend_tab1:
    monthly = filtered.groupby("Year-Month", as_index=False)["Sales"].sum().sort_values("Year-Month")
    fig_m = px.line(monthly, x="Year-Month", y="Sales", markers=True, color_discrete_sequence=[PRIMARY])
    fig_m.update_layout(xaxis_title="Month", yaxis_title="Sales ($)")
    style_chart(fig_m)
    st.plotly_chart(fig_m, use_container_width=True)

with trend_tab2:
    yearly = filtered.groupby("Year", as_index=False)["Sales"].sum().sort_values("Year")
    fig_y = px.bar(yearly, x="Year", y="Sales", color_discrete_sequence=[PRIMARY], text_auto=".2s")
    fig_y.update_layout(xaxis_title="Year", yaxis_title="Sales ($)")
    style_chart(fig_y)
    st.plotly_chart(fig_y, use_container_width=True)

# ----------------------------------------------------------------------
# Category-wise & Region-wise breakdown
# ----------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    section_header("🗂️ Category-wise Sales")
    cat_sales = filtered.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig_cat = px.bar(
        cat_sales, x="Category", y="Sales", color="Category",
        color_discrete_sequence=CHART_PALETTE, text_auto=".2s"
    )
    fig_cat.update_layout(showlegend=False)
    style_chart(fig_cat)
    st.plotly_chart(fig_cat, use_container_width=True)

with col2:
    section_header("🌍 Region-wise Sales")
    region_sales = (
        filtered.dropna(subset=["Region"])
        .groupby("Region", as_index=False)["Sales"].sum()
        .sort_values("Sales", ascending=False)
    )
    fig_reg = px.bar(
        region_sales, x="Sales", y="Region", orientation="h",
        color="Sales", color_continuous_scale="Blues"
    )
    fig_reg.update_layout(
        coloraxis_showscale=False,
        yaxis={"categoryorder": "total ascending"}, height=500
    )
    style_chart(fig_reg)
    st.plotly_chart(fig_reg, use_container_width=True)

# ----------------------------------------------------------------------
# Sub-category heatmap-style table
# ----------------------------------------------------------------------
section_header("🧩 Category × Sub-Category Sales", "Drill down into where revenue is concentrated")
pivot = filtered.pivot_table(index="Category", columns="Sub-Category", values="Sales", aggfunc="sum", fill_value=0)
fig_heat = px.imshow(
    pivot, text_auto=".2s", aspect="auto", color_continuous_scale="Blues",
)
style_chart(fig_heat)
st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("---")
total_sales_filtered = filtered["Sales"].sum()
st.success(f"💰 **Total Sales (filtered selection):** {format_currency(total_sales_filtered)}")
