"""
A Docker-compatible version of the sentiment analysis script.
Instead of waiting for user input, it processes predefined text or
listens for API requests.
"""

# Standard library imports
import time
import json
import os
import sys
import datetime

# Third-party imports
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pymongo import MongoClient

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


def analyze_text(input_text):
    """Analyze the sentiment of given text."""
    # Get sentiment scores
    scores = analyzer.polarity_scores(input_text)
    compound_score = scores["compound"]

    # Get color and interpretation
    color = score_to_color(compound_score)
    interpretation = sentiment_to_interpretation(compound_score)

    # Store in database if connected
    if DB_CONNECTED:
        try:
            analysis_id = analyses.insert_one(
                {
                    "text": input_text,
                    "scores": scores,
                    "color": color,
                    "interpretation": interpretation,
                    "timestamp": datetime.datetime.utcnow(),
                }
            ).inserted_id
            print(f"Stored analysis with ID: {analysis_id}")
        except Exception as storage_error:
            print(f"Error storing in database: {storage_error}")

    return {
        "text": input_text,
        "scores": scores,
        "color": color,
        "interpretation": interpretation,
    }


# Demo texts to analyze when container starts
demo_texts = [
    "I'm feeling great today!",
    "This project is challenging but interesting.",
    "I'm so frustrated with this error.",
    "The weather is nice today.",
]

# Run some demo analyses
print("Starting sentiment analysis service")
print("=" * 50)
for text in demo_texts:
    result = analyze_text(text)
    print(f"Text: {text}")
    print(f"Scores: {result['scores']}")
    print(f"Color: {result['color']}")
    print(f"Interpretation: {result['interpretation']}")
    print("-" * 50)

# Keep the container running
print("Service is running. Container will stay alive.")
while True:
    # In a real app, this would be replaced with an API endpoint
    # that accepts requests from the web app
    time.sleep(60)
