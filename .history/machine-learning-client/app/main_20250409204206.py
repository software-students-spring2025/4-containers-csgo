<<<<<<< HEAD
"""
A simple sentiment analysis script using VADER.

This script takes user input, analyzes the sentiment using VADER,
and outputs the raw sentiment scores, a color representation, and
a human-readable interpretation with emotion labels.
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize the analyzer
analyzer = SentimentIntensityAnalyzer()


# Mapping functions
def score_to_color(score):
    """
    Maps a compound sentiment score to a color representation.

    Args:
        score: Compound sentiment score ranging from -1 (very negative) to 1 (very positive).

    Returns:
        str: Color string representing sentiment intensity.
    """
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
    """
    Maps a compound sentiment score to an interpretation with emoji and emotion labels.

    Args:
        score (float): Compound sentiment score ranging from -1 to 1.

    Returns:
        str: Human-readable interpretation of the sentiment score.
    """
    if score <= -0.6:
        return "⬛️ Very Negative - Shame, Powerlessness"
    if score <= -0.2:
        return "🟥 Negative - Anger, Anxiety, Blame"
    if score < 0.2:
        return "🟩 Neutral - Calm, Relaxed, Apathy"
    if score < 0.6:
        return "🟦 Positive - Hope, Motivation, Optimism"
    return "🟧 Very Positive - Joy, Gratitude, Love"


# Take user input
text = input("Enter a sentence for sentiment analysis: ")

# Get sentiment scores
scores = analyzer.polarity_scores(text)
compound_score = scores["compound"]

# Output in three lines
print(f"Raw scores: {scores}")
print(f"Color: {score_to_color(compound_score)}")
print(f"Interpretation: {sentiment_to_interpretation(compound_score)}")
=======
"""
A simple sentiment analysis script using VADER.

This script takes user input, analyzes the sentiment using VADER,
and outputs the raw sentiment scores, a color representation, and
a human-readable interpretation with emotion labels.
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sys
import os

# Import database connector
sys.path.append('/app')
try:
    from db_connector import SentimentDB
    db_enabled = True
except ImportError:
    print("Database connector not found, running without database storage")
    db_enabled = False

# Initialize the analyzer
analyzer = SentimentIntensityAnalyzer()


# Mapping functions
def score_to_color(score):
    """
    Maps a compound sentiment score to a color representation.

    Args:
        score: Compound sentiment score ranging from -1 (very negative) to 1 (very positive).

    Returns:
        str: Color string representing sentiment intensity.
    """
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
    """
    Maps a compound sentiment score to an interpretation with emoji and emotion labels.

    Args:
        score (float): Compound sentiment score ranging from -1 to 1.

    Returns:
        str: Human-readable interpretation of the sentiment score.
    """
    if score <= -0.6:
        return "⬛️ Very Negative - Shame, Powerlessness"
    if score <= -0.2:
        return "🟥 Negative - Anger, Anxiety, Blame"
    if score < 0.2:
        return "🟩 Neutral - Calm, Relaxed, Apathy"
    if score < 0.6:
        return "🟦 Positive - Hope, Motivation, Optimism"
    return "🟧 Very Positive - Joy, Gratitude, Love"


# Take user input
text = input("Enter a sentence for sentiment analysis: ")

# Get sentiment scores
scores = analyzer.polarity_scores(text)
compound_score = scores["compound"]

# Output in three lines
print(f"Raw scores: {scores}")
color = score_to_color(compound_score)
print(f"Color: {color}")
interpretation = sentiment_to_interpretation(compound_score)
print(f"Interpretation: {interpretation}")

# Store in database if enabled
if db_enabled:
    try:
        db = SentimentDB()
        analysis_id = db.store_analysis(text, scores, color, interpretation)
        print(f"Analysis stored in database with ID: {analysis_id}")
    except Exception as e:
        print(f"Error storing in database: {e}")
>>>>>>> nick
