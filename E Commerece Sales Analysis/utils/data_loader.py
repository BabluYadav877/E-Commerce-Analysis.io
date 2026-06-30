"""
data_loader.py
---------------
Centralized data loading & cleaning utilities for the FlipMart
E-commerce Analytics Dashboard.

Keeping all data logic in one place makes the rest of the app
(the pages) much simpler and easier to maintain.
"""

import os
import pandas as pd
import streamlit as st

# Path to the bundled sample dataset (used if the user doesn't upload one)
DEFAULT_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "FlipMart_Sales_Data.csv")


@st.cache_data(show_spinner="Loading sales data...")
def load_data(uploaded_file=None) -> pd.DataFrame:
    """
    Load the FlipMart sales dataset.

    If the user has uploaded their own file (CSV or Excel) via the
    sidebar uploader, that file is used. Otherwise we fall back to the
    bundled sample dataset shipped with the project.
    """
    if uploaded_file is not None:
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(DEFAULT_DATA_PATH)

    return clean_data(df)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column types and drop unusable rows."""
    df = df.copy()

    # Drop rows that are missing critical identifiers
    required_cols = [c for c in ["Order ID", "Order Date"] if c in df.columns]
    if required_cols:
        df = df.dropna(subset=required_cols)

    # Parse dates
    for col in ["Order Date", "Ship Date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Make sure numeric fields are numeric
    for col in ["Sales", "Profit", "Quantity", "Shipping Cost"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Order Date"])

    # Helpful derived columns used across pages
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Month Name"] = df["Order Date"].dt.strftime("%b")
    df["Year-Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Quarter"] = df["Order Date"].dt.quarter

    return df


def get_filtered_data(df: pd.DataFrame, date_range=None, categories=None, regions=None) -> pd.DataFrame:
    """Apply common sidebar filters (date range, category, region) to a dataframe."""
    filtered = df.copy()

    if date_range and len(date_range) == 2:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered = filtered[(filtered["Order Date"] >= start) & (filtered["Order Date"] <= end)]

    if categories:
        filtered = filtered[filtered["Category"].isin(categories)]

    if regions:
        filtered = filtered[filtered["Region"].isin(regions)]

    return filtered
