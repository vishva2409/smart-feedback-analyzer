# ai_engine.py

import torch
from transformers import pipeline
import re


class SmartFeedbackAnalyzer:
    def __init__(self):
        """
        Initialize AI models only once.
        """
        self.device = 0 if torch.cuda.is_available() else -1

        # Sentiment Model (Fast & Accurate)
        self.sentiment_model = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=self.device
        )

        # Zero-Shot Classification Model
        self.zero_shot_model = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=self.device
        )

        # Business Categories
        self.categories = [
            "Delivery",
            "Customer Support",
            "Product Quality",
            "Pricing",
            "Website Experience",
            "Refund and Returns"
        ]

    def analyze_sentiment(self, text):
        try:
            result = self.sentiment_model(text)[0]
            return {
                "label": result["label"],
                "score": round(result["score"], 3)
            }
        except Exception:
            return {"label": "UNKNOWN", "score": 0.0}

    def categorize_issue(self, text):
        try:
            result = self.zero_shot_model(
                text,
                self.categories,
                multi_label=True
            )

            categories_with_scores = []
            for label, score in zip(result["labels"], result["scores"]):
                if score > 0.35:  # slightly lower threshold for better recall
                    categories_with_scores.append({
                        "label": label,
                        "score": round(score, 3)
                    })

            return categories_with_scores

        except Exception:
            return []

    def map_emotion(self, text, sentiment_label):
        """
        Smarter emotion detection using keywords + sentiment.
        """
        text = text.lower()

        if sentiment_label == "NEGATIVE":
            if re.search(r"angry|furious|outraged", text):
                return "Anger"
            elif re.search(r"disappointed|bad|poor|late|rude", text):
                return "Frustration"
            else:
                return "Dissatisfaction"

        elif sentiment_label == "POSITIVE":
            if re.search(r"love|excellent|amazing|great", text):
                return "Delight"
            else:
                return "Satisfaction"

        else:
            return "Neutral"


    def aggregate_insights(self, feedback_results):
        """
        feedback_results = list of dicts like:
        {
            "sentiment": "POSITIVE",
            "categories": ["Delivery", "Pricing"]
        }
        """

        total = len(feedback_results)
        if total == 0:
            return {}

        sentiment_count = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
        category_count = {}

        for item in feedback_results:
            sentiment = item["sentiment"]
            sentiment_count[sentiment] += 1

            for cat in item["categories"]:
                category_count[cat] = category_count.get(cat, 0) + 1

        # Calculate percentages
        sentiment_percent = {
            key: round((value / total) * 100, 2)
            for key, value in sentiment_count.items()
        }

        return {
            "total_feedback": total,
            "sentiment_distribution": sentiment_percent,
            "category_distribution": category_count
        }



    def generate_recommendations(self, insights):
        recommendations = []

        if not insights:
            return recommendations

        sentiment_dist = insights["sentiment_distribution"]
        category_dist = insights["category_distribution"]

        # High negative alert
        if sentiment_dist.get("NEGATIVE", 0) > 40:
            recommendations.append(
                "High negative sentiment detected. Immediate review required."
            )

        # Check top issue
        if category_dist:
            top_issue = max(category_dist, key=category_dist.get)

            if top_issue == "Delivery":
                recommendations.append(
                    "Frequent delivery complaints detected. Review logistics process."
                )
            elif top_issue == "Customer Support":
                recommendations.append(
                    "Customer support issues trending. Consider staff training."
                )
            elif top_issue == "Product Quality":
                recommendations.append(
                    "Product quality concerns rising. Initiate quality audit."
                )
            elif top_issue == "Pricing":
                recommendations.append(
                    "Pricing dissatisfaction observed. Evaluate pricing strategy."
                )

        if not recommendations:
            recommendations.append("Overall feedback trend is stable.")

        return recommendations