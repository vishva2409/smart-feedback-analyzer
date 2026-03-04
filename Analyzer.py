import streamlit as st
from ai_engine import SmartFeedbackAnalyzer

st.set_page_config(page_title="Smart Feedback Analyzer", layout="wide")

# -------- LOAD MODEL ONCE --------
if "analyzer" not in st.session_state:
    st.session_state.analyzer = SmartFeedbackAnalyzer()

analyzer = st.session_state.analyzer

# -------- SESSION STORAGE --------
if "feedback_data" not in st.session_state:
    st.session_state.feedback_data = []

# -------- SIDEBAR --------
st.sidebar.title("Smart Feedback AI")
st.sidebar.write("Customer Intelligence Platform")
st.sidebar.markdown("---")

# -------- HEADER --------
st.markdown("""
<h1 style='text-align: center;'>Smart Feedback Analyzer</h1>
<p style='text-align: center; color: #9aa0a6;'>
AI-Powered Customer Intelligence Platform
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# -------- FORM SECTION --------
st.subheader("Submit Customer Feedback")

with st.form("feedback_form", clear_on_submit=True):

    feedback_text = st.text_area(
        "Enter feedback:",
        height=120,
        placeholder="Example: Delivery was late and support was rude."
    )

    col1, col2 = st.columns(2)
    analyze_btn = col1.form_submit_button("Analyze")
    add_btn = col2.form_submit_button("Add to Dashboard")

# -------- ANALYSIS --------
if analyze_btn and feedback_text:

    sentiment = analyzer.analyze_sentiment(feedback_text)
    categories = analyzer.categorize_issue(feedback_text)
    emotion = analyzer.map_emotion(feedback_text, sentiment["label"])

    st.markdown("### AI Analysis Result")

    c1, c2, c3 = st.columns(3)
    c1.metric("Sentiment", sentiment["label"])
    c2.metric("Confidence", sentiment["score"])
    c3.metric("Emotion", emotion)

    st.markdown("**Detected Categories:**")
    for cat in categories:
        st.write(f"- {cat['label']} ({cat['score']})")

# -------- ADD TO DASHBOARD --------
if add_btn and feedback_text:

    sentiment = analyzer.analyze_sentiment(feedback_text)
    categories = analyzer.categorize_issue(feedback_text)

    st.session_state.feedback_data.append({
        "text": feedback_text,
        "sentiment": sentiment["label"],
        "categories": [c["label"] for c in categories]
    })

    st.success("Feedback added successfully!")

# -------- NAVIGATION --------
if st.button("View Dashboard"):
    st.switch_page("pages/Dashboard.py")