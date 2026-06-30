"""
pages/4_⭐_Feedback.py
------------------------
Feedback & Review page — collects user feedback (name, star rating,
comments), stores it in a local CSV file, and displays aggregate
rating stats plus recent reviews with simple lexicon-based sentiment
analysis (no heavy NLP downloads required).
"""

import os
import pandas as pd
import streamlit as st
import plotly.express as px

from utils.theme import apply_theme, style_chart, section_header, PRIMARY

apply_theme()

FEEDBACK_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "feedback.csv")


def load_feedback() -> pd.DataFrame:
    if os.path.exists(FEEDBACK_PATH):
        return pd.read_csv(FEEDBACK_PATH, parse_dates=["Timestamp"])
    return pd.DataFrame(columns=["Timestamp", "Name", "Rating", "Comment", "Sentiment"])


def save_feedback(row: dict):
    df = load_feedback()
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(FEEDBACK_PATH, index=False)


# Simple, dependency-free lexicon-based sentiment analysis
POSITIVE_WORDS = {
    "good", "great", "excellent", "amazing", "love", "fantastic", "awesome", "best",
    "happy", "easy", "smooth", "fast", "helpful", "nice", "wonderful", "perfect",
    "satisfied", "recommend", "impressive", "reliable",
}
NEGATIVE_WORDS = {
    "bad", "poor", "terrible", "worst", "hate", "slow", "difficult", "broken",
    "disappointing", "awful", "confusing", "buggy", "delay", "delayed", "unhappy",
    "issue", "problem", "frustrating", "late", "crash",
}


def analyze_sentiment(text: str) -> str:
    if not text or not isinstance(text, str):
        return "Neutral"
    words = set(text.lower().replace(",", " ").replace(".", " ").split())
    pos = len(words & POSITIVE_WORDS)
    neg = len(words & NEGATIVE_WORDS)
    if pos > neg:
        return "Positive 😊"
    if neg > pos:
        return "Negative 😞"
    return "Neutral 😐"


st.title("⭐ Feedback & Reviews")
st.markdown("We'd love to hear what you think about the FlipMart dashboard experience.")
st.markdown("---")

# ----------------------------------------------------------------------
# Feedback form
# ----------------------------------------------------------------------
section_header("📝 Leave Your Feedback")

with st.form("feedback_form", clear_on_submit=True):
    fc1, fc2 = st.columns([2, 1])
    name = fc1.text_input("Your Name", placeholder="e.g. Priya Sharma")
    rating = fc2.slider("Rating", min_value=1, max_value=5, value=5, format="%d ⭐")
    comment = st.text_area("Comments", placeholder="Tell us what you liked or what could be improved...")
    submitted = st.form_submit_button("Submit Feedback")

    if submitted:
        if not name.strip():
            st.error("Please enter your name before submitting.")
        else:
            sentiment = analyze_sentiment(comment)
            save_feedback({
                "Timestamp": pd.Timestamp.now(),
                "Name": name.strip(),
                "Rating": rating,
                "Comment": comment.strip(),
                "Sentiment": sentiment,
            })
            st.success(f"Thank you, {name.strip()}! Your feedback has been recorded. (Sentiment: {sentiment})")
            st.rerun()

st.markdown("---")

# ----------------------------------------------------------------------
# Aggregate stats
# ----------------------------------------------------------------------
feedback_df = load_feedback()

section_header("📊 Feedback Summary")

if feedback_df.empty:
    st.info("No feedback has been submitted yet. Be the first to share your thoughts above!")
else:
    avg_rating = feedback_df["Rating"].mean()
    total_reviews = len(feedback_df)
    pos_pct = (feedback_df["Sentiment"].str.contains("Positive").sum() / total_reviews) * 100

    s1, s2, s3 = st.columns(3)
    s1.metric("⭐ Average Rating", f"{avg_rating:.2f} / 5")
    s2.metric("🗣️ Total Reviews", f"{total_reviews}")
    s3.metric("😊 Positive Sentiment", f"{pos_pct:.0f}%")

    col1, col2 = st.columns(2)
    with col1:
        rating_counts = feedback_df["Rating"].value_counts().sort_index()
        fig_rating = px.bar(
            x=rating_counts.index, y=rating_counts.values,
            labels={"x": "Rating", "y": "Count"}, color_discrete_sequence=[PRIMARY],
            title="Rating Distribution"
        )
        style_chart(fig_rating)
        st.plotly_chart(fig_rating, use_container_width=True)

    with col2:
        sentiment_counts = feedback_df["Sentiment"].value_counts()
        fig_sent = px.pie(
            names=sentiment_counts.index, values=sentiment_counts.values,
            title="Sentiment Breakdown", hole=0.4,
            color_discrete_sequence=["#66BB6A", "#FFB74D", "#E57373"]
        )
        style_chart(fig_sent)
        st.plotly_chart(fig_sent, use_container_width=True)

    st.markdown("---")
    section_header("🕒 Recent Reviews")
    recent = feedback_df.sort_values("Timestamp", ascending=False).head(10)
    for _, row in recent.iterrows():
        stars = "⭐" * int(row["Rating"])
        st.markdown(
            f"""
            <div class="fm-card">
                <h3>{row['Name']} — {stars}</h3>
                <p style="margin:0;color:#CFE3FA;">{row['Comment'] if row['Comment'] else '<i>No comment</i>'}</p>
                <span class="fm-badge">{row['Sentiment']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.download_button(
        "⬇️ Download All Feedback (CSV)",
        data=feedback_df.to_csv(index=False).encode("utf-8"),
        file_name="flipmart_feedback.csv",
        mime="text/csv",
    )
