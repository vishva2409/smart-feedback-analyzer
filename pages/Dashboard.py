import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard", layout="wide")

# -------- CHECK MODEL --------
if "analyzer" not in st.session_state:
    st.error("Please go to Analyzer page first.")
    st.stop()

analyzer = st.session_state.analyzer

# -------- SIDEBAR --------
st.sidebar.title("Smart Feedback AI")
st.sidebar.write("Customer Intelligence Platform")
st.sidebar.markdown("---")

st.title("Insights Dashboard")

if "feedback_data" not in st.session_state or not st.session_state.feedback_data:
    st.info("No feedback added yet.")
    st.stop()

insights = analyzer.aggregate_insights(st.session_state.feedback_data)
recommendations = analyzer.generate_recommendations(insights)

# -------- RESET BUTTON --------
if st.button("Reset Dashboard"):
    st.session_state.feedback_data = []
    st.success("Dashboard cleared!")
    st.stop()

# -------- METRICS --------
col1, col2 = st.columns(2)

negative_percent = insights["sentiment_distribution"].get("NEGATIVE", 0)
health_score = round(100 - negative_percent, 1)

col1.metric("Total Feedback", insights["total_feedback"])
col2.metric("Customer Health Score", f"{health_score}%")

# -------- SENTIMENT PIE --------
st.markdown("### Sentiment Distribution")

sentiment_data = {
    k: v for k, v in insights["sentiment_distribution"].items() if v > 0
}

fig1, ax1 = plt.subplots(figsize=(4,4))
ax1.pie(
    sentiment_data.values(),
    labels=sentiment_data.keys(),
    autopct='%1.1f%%',
    startangle=90
)
ax1.axis('equal')
st.pyplot(fig1)

# -------- ISSUE BAR --------
st.markdown("### Issue Distribution")

category_data = insights["category_distribution"]

if category_data:
    fig2, ax2 = plt.subplots(figsize=(6,3))
    ax2.bar(category_data.keys(), category_data.values())
    ax2.set_xticklabels(category_data.keys(), rotation=25)
    st.pyplot(fig2)

# -------- RECOMMENDATIONS --------
st.markdown("### Business Recommendations")

for rec in recommendations:
    st.markdown(
        f"""
        <div style='padding:10px;
                    border-radius:8px;
                    background-color:#1e2a38;
                    margin-bottom:8px;'>
        {rec}
        </div>
        """,
        unsafe_allow_html=True
    )

# -------- EXPORT CSV --------
st.markdown("### Export Data")

df = pd.DataFrame(st.session_state.feedback_data)
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Feedback Data as CSV",
    data=csv,
    file_name="feedback_data.csv",
    mime="text/csv"
)