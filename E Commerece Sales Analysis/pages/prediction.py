"""
pages/3_🤖_Prediction.py
--------------------------
Sales Forecasting page using a polynomial Linear Regression model
on daily aggregated sales. Shows actual vs predicted performance,
model accuracy, and a future forecast for a user-selected horizon.
"""

import streamlit as st
import plotly.graph_objects as go

from utils.theme import apply_theme, style_chart, section_header, PRIMARY
from utils.data_loader import load_data
from utils.metrics import format_currency
from models.forecast import prepare_daily_series, train_forecast_model, forecast_future, get_fitted_values

apply_theme()

df = st.session_state.get("df")
if df is None:
    df = load_data(None)
    st.session_state["df"] = df

st.title("🤖 Sales Forecast")
st.markdown(
    "A simple, transparent **Linear Regression** model trained on historical daily sales "
    "is used to project future revenue. Use this as a directional planning tool, not a guarantee."
)
st.markdown("---")

# ----------------------------------------------------------------------
# Controls
# ----------------------------------------------------------------------
c1, c2 = st.columns(2)
horizon = c1.slider("Forecast horizon (days)", min_value=30, max_value=60, value=30, step=5)
degree = c2.selectbox("Trend complexity (polynomial degree)", options=[1, 2, 3], index=1,
                       help="1 = straight-line trend, 2-3 = allows curvature for growth/decline.")

# ----------------------------------------------------------------------
# Train model
# ----------------------------------------------------------------------
with st.spinner("Training forecasting model..."):
    daily = prepare_daily_series(df)
    model, poly, r2, mae = train_forecast_model(daily, degree=degree)
    daily["Fitted Sales"] = get_fitted_values(model, poly, daily)
    future = forecast_future(model, poly, daily, horizon_days=horizon)

# ----------------------------------------------------------------------
# Model accuracy
# ----------------------------------------------------------------------
section_header("📐 Model Accuracy")
m1, m2, m3 = st.columns(3)
m1.metric("R² Score (test set)", f"{r2:.3f}")
m2.metric("Mean Absolute Error", format_currency(mae))
m3.metric("Training Data Points", f"{len(daily):,} days")

if r2 < 0.3:
    st.warning(
        "⚠️ Daily sales are highly volatile, so the R² score is naturally low for a simple "
        "linear model. The forecast still captures the overall trend direction."
    )

st.markdown("---")

# ----------------------------------------------------------------------
# Actual vs Predicted (historical fit)
# ----------------------------------------------------------------------
section_header("📊 Actual vs Predicted Sales (Historical)")

fig_fit = go.Figure()
fig_fit.add_trace(go.Scatter(
    x=daily["Order Date"], y=daily["Sales"], mode="lines", name="Actual Sales",
    line=dict(color="#90CAF9", width=1.5)
))
fig_fit.add_trace(go.Scatter(
    x=daily["Order Date"], y=daily["Fitted Sales"], mode="lines", name="Model Trend",
    line=dict(color="#FFFFFF", width=3)
))
fig_fit.update_layout(
    xaxis_title="Date", yaxis_title="Sales ($)", legend=dict(orientation="h", y=1.1)
)
style_chart(fig_fit)
st.plotly_chart(fig_fit, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------------------
# Future forecast
# ----------------------------------------------------------------------
section_header(f"🔮 Next {horizon} Days Forecast")

fig_fc = go.Figure()
fig_fc.add_trace(go.Scatter(
    x=daily["Order Date"].tail(120), y=daily["Sales"].tail(120), mode="lines",
    name="Recent Actual Sales", line=dict(color="#90CAF9", width=1.5)
))
fig_fc.add_trace(go.Scatter(
    x=future["Order Date"], y=future["Predicted Sales"], mode="lines+markers",
    name="Forecasted Sales", line=dict(color="#FFFFFF", width=3, dash="dash")
))
fig_fc.update_layout(
    xaxis_title="Date", yaxis_title="Sales ($)", legend=dict(orientation="h", y=1.1)
)
style_chart(fig_fc)
st.plotly_chart(fig_fc, use_container_width=True)

total_forecast = future["Predicted Sales"].sum()
avg_daily_forecast = future["Predicted Sales"].mean()

f1, f2 = st.columns(2)
f1.metric(f"Projected Total Sales (next {horizon} days)", format_currency(total_forecast))
f2.metric("Projected Average Daily Sales", format_currency(avg_daily_forecast))

with st.expander("📋 View forecast data table"):
    table = future.copy()
    table["Predicted Sales"] = table["Predicted Sales"].map(lambda x: f"${x:,.2f}")
    st.dataframe(table, use_container_width=True, height=300)

    st.download_button(
        "⬇️ Download Forecast (CSV)",
        data=future.to_csv(index=False).encode("utf-8"),
        file_name=f"sales_forecast_{horizon}_days.csv",
        mime="text/csv",
    )
