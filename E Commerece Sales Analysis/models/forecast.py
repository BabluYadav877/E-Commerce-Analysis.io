"""
forecast.py
-----------
Lightweight sales forecasting using scikit-learn Linear Regression
on daily aggregated sales, plus a polynomial feature option to
capture mild trend curvature. Kept intentionally simple/beginner
friendly while still being a genuine working ML model.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split


def prepare_daily_series(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales to a daily time series with a continuous date index."""
    daily = df.groupby("Order Date")["Sales"].sum().reset_index()
    daily = daily.sort_values("Order Date")

    full_range = pd.date_range(daily["Order Date"].min(), daily["Order Date"].max(), freq="D")
    daily = daily.set_index("Order Date").reindex(full_range, fill_value=0).rename_axis("Order Date").reset_index()
    daily["day_index"] = (daily["Order Date"] - daily["Order Date"].min()).dt.days
    return daily


def train_forecast_model(daily: pd.DataFrame, degree: int = 2):
    """Train a (polynomial) linear regression model on day_index -> Sales."""
    X = daily[["day_index"]].values
    y = daily["Sales"].values

    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)

    X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
        X_poly, y, daily.index, test_size=0.2, shuffle=False
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred_test = model.predict(X_test)
    r2 = r2_score(y_test, y_pred_test)
    mae = mean_absolute_error(y_test, y_pred_test)

    return model, poly, r2, mae


def forecast_future(model, poly, daily: pd.DataFrame, horizon_days: int = 30) -> pd.DataFrame:
    """Predict sales for the next `horizon_days` days beyond the dataset."""
    last_day_index = daily["day_index"].max()
    last_date = daily["Order Date"].max()

    future_day_idx = np.arange(last_day_index + 1, last_day_index + 1 + horizon_days)
    future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=horizon_days, freq="D")

    X_future_poly = poly.transform(future_day_idx.reshape(-1, 1))
    preds = model.predict(X_future_poly)
    preds = np.clip(preds, a_min=0, a_max=None)  # sales can't be negative

    return pd.DataFrame({"Order Date": future_dates, "Predicted Sales": preds})


def get_fitted_values(model, poly, daily: pd.DataFrame) -> pd.Series:
    """Get the model's fitted values over the historical range (for Actual vs Predicted plot)."""
    X_poly = poly.transform(daily[["day_index"]].values)
    return model.predict(X_poly)
