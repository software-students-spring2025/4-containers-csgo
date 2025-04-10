"""API endpoints for the sentiment analysis service."""
from datetime import datetime, timezone

# Standard library imports
import os
import datetime

# Third-party imports
from flask import Flask, request, jsonify
from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)

# MongoDB connection settings
MONGO_URI = os.environ.get("MONGODB_URI", "mongodb://root:example@mongodb:27017/")
DB_NAME = os.environ.get("MONGODB_DB", "sentiment_analysis")

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    analyses = db.analyses
    print("Successfully connected to MongoDB")
    DB_CONNECTED = True
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    DB_CONNECTED = False

# Initialize the analyzer
analyzer = SentimentIntensityAnalyzer()


# Mapping functions
def score_to_color(score):
    """Maps a compound sentiment score to a color representation."""
    if score <= -0.6:
        return "black"
    if score <= -0.2:
        return "red"
    if score < 0.2:
        return "green"
    if score < 0.6:
        return "blue"
    return "orange"


def sentiment_to_interpretation(score):
    """Maps a compound sentiment score to an interpretation with emoji and emotion labels."""
    if score <= -0.6:
        return "⬛️ Very Negative - Shame, Powerlessness"
    if score <= -0.2:
        return "🟥 Negative - Anger, Anxiety, Blame"
    if score < 0.2:
        return "🟩 Neutral - Calm, Relaxed, Apathy"
    if score < 0.6:
        return "🟦 Positive - Hope, Motivation, Optimism"
    return "🟧 Very Positive - Joy, Gratitude, Love"


@app.route("/analyze", methods=["POST"])
def analyze():
    """Analyze sentiment of text received in request."""
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Get sentiment scores
    scores = analyzer.polarity_scores(text)
    compound_score = scores["compound"]

    # Get color and interpretation
    color = score_to_color(compound_score)
    interpretation = sentiment_to_interpretation(compound_score)

    # Store in database if connected
    if DB_CONNECTED:
        try:
            analysis_id = analyses.insert_one(
                {
                    "text": text,
                    "scores": scores,
                    "color": color,
                    "interpretation": interpretation,
                    "timestamp": datetime.now(timezone.utc),
                }
            ).inserted_id
            print(f"Stored analysis with ID: {analysis_id}")
        except Exception as storage_error:
            print(f"Error storing in database: {storage_error}")

    return jsonify(
        {
            "text": text,
            "scores": scores,
            "color": color,
            "interpretation": interpretation,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
