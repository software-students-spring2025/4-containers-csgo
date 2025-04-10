"""
A Docker-compatible version of the sentiment analysis script.
Instead of waiting for user input, it processes predefined text or
listens for API requests.
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
import json
import os
import sys
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
    db_connected = True
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    db_connected = False

# Initialize the analyzer
analyzer = SentimentIntensityAnalyzer()


# Mapping functions from the original script
def score_to_color(score):
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
    if score <= -0.6:
        return "⬛️ Very Negative - Shame, Powerlessness"
    if score <= -0.2:
        return "🟥 Negative - Anger, Anxiety, Blame"
    if score < 0.2:
        return "🟩 Neutral - Calm, Relaxed, Apathy"
    if score < 0.6:
        return "🟦 Positive - Hope, Motivation, Optimism"
    return "🟧 Very Positive - Joy, Gratitude, Love"


def analyze_text(text):
    # Get sentiment scores
    scores = analyzer.polarity_scores(text)
    compound_score = scores["compound"]
    
    # Get color and interpretation
    color = score_to_color(compound_score)
    interpretation = sentiment_to_interpretation(compound_score)
    
    # Store in database if connected
    if db_connected:
        try:
            analysis_id = analyses.insert_one({
                "text": text,
                "scores": scores,
                "color": color,
                "interpretation": interpretation,
                "timestamp": datetime.datetime.utcnow()
            }).inserted_id
            print(f"Stored analysis with ID: {analysis_id}")
        except Exception as e:
            print(f"Error storing in database: {e}")
    
    return {
        "text": text,
        "scores": scores,
        "color": color,
        "interpretation": interpretation
    }


# Demo texts to analyze when container starts
demo_texts = [
    "I'm feeling great today!",
    "This project is challenging but interesting.",
    "I'm so frustrated with this error.",
    "The weather is nice today."
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