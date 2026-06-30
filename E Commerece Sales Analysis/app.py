"""
app.py
------
FlipMart E-commerce Analytics Dashboard
Main entry point — sets global page config, applies the Blue theme,
builds explicit sidebar page navigation (using Streamlit's st.Page /
st.navigation API for maximum reliability across platforms), manages
the shared dataset (with optional upload override) in session state,
and dispatches to the selected page.

Run with:  streamlit run app.py
"""

import streamlit as st

from utils.theme import apply_theme
from utils.data_loader import load_data

# ----------------------------------------------------------------------
# Page configuration (must be the first Streamlit call, only once)
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="FlipMart Analytics Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

# ----------------------------------------------------------------------
# Sidebar — branding & data upload (shown above the page navigation)
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown("# 🛍️ FlipMart")
    st.markdown("##### E-commerce Analytics Dashboard")
    st.markdown("---")
    st.markdown("### 📁 Dataset")
    uploaded_file = st.file_uploader(
        "Upload your own sales data (CSV/XLSX)",
        type=["csv", "xlsx"],
        help="Optional — leave empty to use the bundled FlipMart sample dataset.",
    )
    st.caption("Using the FlipMart sample dataset by default." if uploaded_file is None else f"Using: {uploaded_file.name}")
    st.markdown("---")

# Load data once and share across all pages via session_state
df = load_data(uploaded_file)
st.session_state["df"] = df

# ----------------------------------------------------------------------
# Explicit page navigation (renders as clickable buttons in the sidebar)
# ----------------------------------------------------------------------
home_page = st.Page("pages/home.py", title="Home", icon="🏠", default=True)
sales_page = st.Page("pages/sales.py", title="Sales Analysis", icon="📊")
products_page = st.Page("pages/products.py", title="Product Performance", icon="📦")
prediction_page = st.Page("pages/prediction.py", title="Prediction / Forecast", icon="🤖")
feedback_page = st.Page("pages/feedback.py", title="Feedback & Reviews", icon="⭐")

pg = st.navigation(
    {
        "Dashboard": [home_page, sales_page, products_page],
        "Insights": [prediction_page, feedback_page],
    }
)

pg.run()
