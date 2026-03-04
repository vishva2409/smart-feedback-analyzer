from ai_engine import SmartFeedbackAnalyzer

analyzer = SmartFeedbackAnalyzer()

sample_feedbacks = [
    "Delivery was late and support was rude.",
    "The product quality is amazing, I love it!",
    "Pricing is too high compared to competitors.",
    "Website experience is smooth and fast."
]

feedback_results = []

for text in sample_feedbacks:
    sentiment = analyzer.analyze_sentiment(text)
    categories = analyzer.categorize_issue(text)

    feedback_results.append({
        "sentiment": sentiment["label"],
        "categories": [c["label"] for c in categories]
    })

insights = analyzer.aggregate_insights(feedback_results)
recommendations = analyzer.generate_recommendations(insights)

print("Insights:")
print(insights)

print("\nRecommendations:")
print(recommendations)