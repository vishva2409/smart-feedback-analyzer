import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Smart Feedback Analyzer", layout="wide")

# Initialize session state
if "feedback_list" not in st.session_state:
    st.session_state.feedback_list = []

if "sentiment_list" not in st.session_state:
    st.session_state.sentiment_list = []

if "category_list" not in st.session_state:
    st.session_state.category_list = []

# ---------------- HERO SECTION ----------------
st.title("Smart Feedback Analyzer")
st.subheader("AI-Powered Customer Intelligence Platform")
st.divider()

# ---------------- INPUT SECTION ----------------
st.header("Submit Customer Feedback")

feedback_text = st.text_area(
    "Enter customer feedback below:",
    placeholder="Example: Delivery was late and customer support was rude."
)

col1, col2 = st.columns(2)

with col1:
    analyze_btn = st.button("Analyze Feedback")

with col2:
    add_btn = st.button("Add to Dashboard")

st.divider()

# ---------------- AI OUTPUT PLACEHOLDERS ----------------
# ---------------- AI OUTPUT SECTION ----------------
st.header("AI Analysis Results")

result_col1, result_col2, result_col3 = st.columns(3)

with result_col1:
    st.subheader("Sentiment")
    sentiment_placeholder = st.empty()

with result_col2:
    st.subheader("Issue Categories")
    category_placeholder = st.empty()

with result_col3:
    st.subheader("Emotion")
    emotion_placeholder = st.empty()
# ---------------- DASHBOARD SECTION ----------------
st.header("Insights Dashboard")

metric_col1, metric_col2 = st.columns(2)

with metric_col1:
    st.metric("Total Feedback Count", len(st.session_state.feedback_list))

with metric_col2:
    if len(st.session_state.sentiment_list) > 0:
        positive_count = st.session_state.sentiment_list.count("Positive")
        health_score = int((positive_count / len(st.session_state.sentiment_list)) * 10)
        st.metric("Customer Health Score", f"{health_score}/10")
    else:
        st.metric("Customer Health Score", "0/10")

st.subheader("Sentiment Distribution")
chart_placeholder1 = st.empty()
if len(st.session_state.sentiment_list) > 0:
    sentiment_counts = pd.Series(st.session_state.sentiment_list).value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%')
    chart_placeholder1.pyplot(fig1)

st.subheader("Issue Category Distribution")
chart_placeholder2 = st.empty()
if len(st.session_state.category_list) > 0:
    flat_categories = [cat for sublist in st.session_state.category_list for cat in sublist]
    category_counts = pd.Series(flat_categories).value_counts()
    fig2, ax2 = plt.subplots()
    ax2.bar(category_counts.index, category_counts.values)
    chart_placeholder2.pyplot(fig2)

st.divider()

# ---------------- RECOMMENDATION SECTION ----------------
st.header("Business Recommendations")

recommendation_placeholder = st.empty()
if len(st.session_state.sentiment_list) > 0:
    negative_count = st.session_state.sentiment_list.count("Negative")
    total = len(st.session_state.sentiment_list)

    if negative_count / total > 0.4:
        st.error("High negative sentiment detected. Immediate attention required.")
    else:
        st.success("Customer sentiment is within healthy range.")
else:
    st.info("Recommendations will appear after feedback analysis.")