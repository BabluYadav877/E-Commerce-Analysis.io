"""
theme.py
--------
Blue visual theme (white text) for the FlipMart Analytics Dashboard.
Contains shared CSS, color palette, and small UI helper components
(KPI cards, section headers) used across every page so the look and
feel stays consistent.
"""

import streamlit as st

# ----------------------------------------------------------------------
# Color palette - Blue theme with white text
# ----------------------------------------------------------------------
PRIMARY = "#1E88E5"        # vivid blue - primary accents
PRIMARY_LIGHT = "#42A5F5"  # lighter blue - secondary accents / hover
BACKGROUND = "#0D2B4E"     # deep navy blue page background
CARD_BG = "#123B6B"        # slightly lighter navy for cards
ACCENT = "#1E88E5"         # blue accent for borders/highlights
TEXT_DARK = "#FFFFFF"      # primary text is white
MUTED = "#CFE3FA"          # soft light-blue/white for secondary text

# A reusable categorical palette for charts (blues + complementary tones)
CHART_PALETTE = [
    "#1E88E5", "#42A5F5", "#90CAF9", "#0D47A1",
    "#64B5F6", "#1565C0", "#BBDEFB", "#2196F3",
]


def apply_theme():
    """Inject global CSS for the Blue theme (white text). Call once per page."""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {BACKGROUND};
            color: {TEXT_DARK};
        }}

        /* Make all general text white by default */
        .stApp, .stApp p, .stApp span, .stApp label, .stApp li,
        .stApp div, .stMarkdown, .stCaption, .stText {{
            color: {TEXT_DARK};
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background-color: #0A2240;
            border-right: 1px solid {ACCENT};
        }}
        section[data-testid="stSidebar"] * {{
            color: {TEXT_DARK} !important;
        }}

        /* Headings */
        h1, h2, h3, h4, h5, h6 {{
            color: {TEXT_DARK} !important;
            font-weight: 700 !important;
        }}

        /* Metric cards (st.metric) */
        div[data-testid="stMetric"] {{
            background-color: {CARD_BG};
            border: 1px solid {ACCENT};
            border-radius: 14px;
            padding: 16px 18px 10px 18px;
            box-shadow: 0 2px 8px rgba(30, 136, 229, 0.25);
        }}
        div[data-testid="stMetricLabel"] {{
            color: {MUTED} !important;
            font-weight: 600 !important;
        }}
        div[data-testid="stMetricValue"] {{
            color: {TEXT_DARK} !important;
        }}
        div[data-testid="stMetricDelta"] {{
            color: {MUTED} !important;
        }}

        /* Buttons */
        .stButton > button, .stDownloadButton > button {{
            background-color: {PRIMARY};
            color: white;
            border-radius: 10px;
            border: none;
            padding: 0.5em 1.2em;
            font-weight: 600;
            transition: background-color 0.2s ease-in-out;
        }}
        .stButton > button:hover, .stDownloadButton > button:hover {{
            background-color: {PRIMARY_LIGHT};
            color: white;
        }}

        /* Tabs */
        button[data-baseweb="tab"] {{
            font-weight: 600;
            color: {MUTED} !important;
        }}
        button[data-baseweb="tab"] p {{
            color: {MUTED} !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            color: {TEXT_DARK} !important;
            border-bottom: 3px solid {PRIMARY} !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] p {{
            color: {TEXT_DARK} !important;
        }}

        /* Expander */
        details {{
            background-color: {CARD_BG};
            border: 1px solid {ACCENT};
            border-radius: 10px;
        }}
        details summary {{
            color: {TEXT_DARK} !important;
        }}

        /* Inputs (text, number, select, textarea, date, slider labels) */
        .stTextInput input, .stTextArea textarea, .stNumberInput input {{
            background-color: {CARD_BG};
            color: {TEXT_DARK};
            border: 1px solid {ACCENT};
        }}
        .stSelectbox div[data-baseweb="select"] > div,
        .stMultiSelect div[data-baseweb="select"] > div {{
            background-color: {CARD_BG};
            color: {TEXT_DARK};
            border-color: {ACCENT};
        }}

        /* Dataframe / table */
        div[data-testid="stDataFrame"] {{
            background-color: {CARD_BG};
        }}

        /* Custom card class used inside markdown blocks */
        .fm-card {{
            background-color: {CARD_BG};
            border: 1px solid {ACCENT};
            border-radius: 16px;
            padding: 18px 20px;
            box-shadow: 0 2px 10px rgba(30, 136, 229, 0.25);
            margin-bottom: 10px;
            color: {TEXT_DARK};
        }}
        .fm-card h3 {{
            margin: 0 0 6px 0;
            font-size: 1.05rem;
            color: {TEXT_DARK} !important;
        }}
        .fm-card p {{
            color: {MUTED} !important;
        }}
        .fm-badge {{
            display: inline-block;
            background-color: {PRIMARY};
            color: white;
            border-radius: 999px;
            padding: 2px 12px;
            font-size: 0.8rem;
            font-weight: 600;
        }}

        /* Alerts (info/success/warning) keep readable white text */
        div[data-testid="stAlert"] p {{
            color: {TEXT_DARK} !important;
        }}

        /* Hide default Streamlit footer/menu clutter for a cleaner portfolio look */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_chart(fig):
    """Apply consistent dark-blue/white-text styling to a Plotly figure."""
    fig.update_layout(
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font_color=TEXT_DARK,
        legend_font_color=TEXT_DARK,
        xaxis=dict(gridcolor="#1E4A7A", color=TEXT_DARK),
        yaxis=dict(gridcolor="#1E4A7A", color=TEXT_DARK),
    )
    return fig


def section_header(title: str, subtitle: str = ""):
    """Render a consistent styled section header across pages."""
    st.markdown(f"## {title}")
    if subtitle:
        st.markdown(f"<p style='color:{MUTED};margin-top:-10px;'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown("---")


def info_card(title: str, value: str, badge: str = ""):
    """Render a simple styled info card using HTML/CSS (for non-metric content)."""
    badge_html = f"<span class='fm-badge'>{badge}</span>" if badge else ""
    st.markdown(
        f"""
        <div class="fm-card">
            <h3>{title} {badge_html}</h3>
            <p style="font-size:1.4rem;font-weight:700;color:{TEXT_DARK};margin:0;">{value}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
