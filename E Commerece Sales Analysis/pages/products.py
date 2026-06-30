"""
pages/2_📦_Products.py
------------------------
Product Performance page — top/least sellers, product-wise revenue,
category contribution pie chart, and a searchable product table.
"""

import streamlit as st
import plotly.express as px

from utils.theme import apply_theme, style_chart, section_header, CHART_PALETTE
from utils.data_loader import load_data
from utils.metrics import format_currency

apply_theme()

df = st.session_state.get("df")
if df is None:
    df = load_data(None)
    st.session_state["df"] = df

st.title("📦 Product Performance")
st.markdown("Identify your best and worst performing products and categories.")
st.markdown("---")

# ----------------------------------------------------------------------
# Product-wise revenue aggregation
# ----------------------------------------------------------------------
product_perf = (
    df.groupby("Product Name", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum"), Category=("Category", "first"))
    .sort_values("Sales", ascending=False)
)

n = st.slider("Number of products to display in charts", min_value=5, max_value=20, value=10)

col1, col2 = st.columns(2)

with col1:
    section_header(f"🏆 Top {n} Best-Selling Products", "Ranked by total revenue")
    top_products = product_perf.head(n)
    fig_top = px.bar(
        top_products.sort_values("Sales"), x="Sales", y="Product Name", orientation="h",
        color="Sales", color_continuous_scale="Blues"
    )
    fig_top.update_layout(coloraxis_showscale=False, height=450)
    style_chart(fig_top)
    st.plotly_chart(fig_top, use_container_width=True)

with col2:
    section_header(f"📉 Bottom {n} Least-Selling Products", "Lowest total revenue")
    bottom_products = product_perf.tail(n)
    fig_bottom = px.bar(
        bottom_products.sort_values("Sales", ascending=False), x="Sales", y="Product Name", orientation="h",
        color="Sales", color_continuous_scale="Reds"
    )
    fig_bottom.update_layout(coloraxis_showscale=False, height=450)
    style_chart(fig_bottom)
    st.plotly_chart(fig_bottom, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------------------
# Category contribution pie chart
# ----------------------------------------------------------------------
section_header("🥧 Category Contribution to Total Sales")
cat_contrib = df.groupby("Category", as_index=False)["Sales"].sum()
fig_pie = px.pie(
    cat_contrib, names="Category", values="Sales", hole=0.4,
    color_discrete_sequence=CHART_PALETTE
)
style_chart(fig_pie)
st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------------------
# Searchable product table
# ----------------------------------------------------------------------
section_header("🔎 Searchable Product Table", "Search by product name or filter by category")

s1, s2 = st.columns([2, 1])
search_term = s1.text_input("Search product name", "")
cat_filter = s2.multiselect("Filter by category", options=sorted(df["Category"].dropna().unique()))

table = product_perf.copy()
if search_term:
    table = table[table["Product Name"].str.contains(search_term, case=False, na=False)]
if cat_filter:
    table = table[table["Category"].isin(cat_filter)]

table_display = table.copy()
table_display["Sales"] = table_display["Sales"].map(lambda x: f"${x:,.2f}")
table_display["Profit"] = table_display["Profit"].map(lambda x: f"${x:,.2f}")

st.dataframe(
    table_display[["Product Name", "Category", "Sales", "Profit", "Quantity"]],
    use_container_width=True,
    height=400,
)
st.caption(f"Showing {len(table):,} of {len(product_perf):,} products.")

st.download_button(
    "⬇️ Download Product Performance (CSV)",
    data=table.to_csv(index=False).encode("utf-8"),
    file_name="product_performance.csv",
    mime="text/csv",
)
