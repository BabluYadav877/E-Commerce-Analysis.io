# 🛍️ FlipMart E-commerce Analytics Dashboard

A full-stack, portfolio-ready **Streamlit** analytics dashboard built on top of the
FlipMart sales dataset (51K+ orders, 2019–2022, global markets). Features a clean
**Light Green** UI theme, interactive Plotly visuals, a working Linear Regression
sales forecast, and a feedback/review module with lightweight sentiment analysis.

## ✨ Features

| Page | What it does |
|---|---|
| 🏠 Home | KPI cards (Sales, Orders, Customers, Profit, Conversion), sales trend, category/region snapshot, business insights & recommendations |
| 📊 Sales Analysis | Date/Category/Region filters, monthly & yearly trends, category & region breakdowns, category × sub-category heatmap |
| 📦 Product Performance | Top/bottom selling products, category contribution pie chart, searchable & downloadable product table |
| 🤖 Prediction / Forecast | Polynomial Linear Regression forecast (30–60 days), actual vs predicted chart, R² / MAE accuracy metrics |
| ⭐ Feedback & Reviews | Star-rating + comment form, CSV storage, rating/sentiment charts, recent reviews feed |

## 🗂️ Project Structure

```
flipmart_dashboard/
├── app.py                  # Main entry point (Home page)
├── pages/
│   ├── 1_📊_Sales.py
│   ├── 2_📦_Products.py
│   ├── 3_🤖_Prediction.py
│   └── 4_⭐_Feedback.py
├── utils/
│   ├── data_loader.py       # Data loading, cleaning, filtering
│   ├── metrics.py           # KPI & insight calculations
│   └── theme.py             # Light Green theme + UI helpers
├── models/
│   └── forecast.py          # Linear Regression forecasting model
├── data/
│   ├── FlipMart_Sales_Data.csv
│   └── feedback.csv         # created automatically after first submission
└── requirements.txt
```

## 🚀 Getting Started

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`. Use the sidebar to navigate between
pages, or upload your own CSV/XLSX file to override the bundled sample dataset.

## 📁 Dataset

The bundled dataset (`data/FlipMart_Sales_Data.csv`) contains order-level e-commerce
transactions with columns such as `Order Date`, `Category`, `Sub-Category`, `Region`,
`Market`, `Sales`, `Profit`, `Quantity`, and `Customer ID`. You can replace it at any
time via the **Upload your own sales data** control in the sidebar — the app expects
the same column names.

## 🤖 Forecasting Model

The Prediction page aggregates sales to a daily time series and fits a
**Polynomial Linear Regression** model (`scikit-learn`) on the day index. Users can
choose the polynomial degree (1–3) to control trend curvature and the forecast
horizon (30–60 days). Accuracy is reported via R² and Mean Absolute Error on a
held-out test split.

## ⭐ Feedback & Sentiment

Feedback is stored in `data/feedback.csv`. Sentiment is computed with a lightweight,
dependency-free lexicon match (no model download required) so the app works fully
offline.

## 🎨 Theming

All colors and shared CSS live in `utils/theme.py` — edit `PRIMARY`, `ACCENT`, and
`CHART_PALETTE` there to retheme the entire app consistently.

---
Built with Python, Streamlit, Pandas, Plotly, and scikit-learn.
