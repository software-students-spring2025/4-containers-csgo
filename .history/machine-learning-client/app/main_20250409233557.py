"""
A simple sentiment analysis script using VADER.

This script takes user input, analyzes the sentiment using VADER,
and outputs the raw sentiment scores, a color representation, and
a human-readable interpretation with emotion labels.
"""

# Standard library imports
import sys

# Third-party imports
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Import database connector
sys.path.append('/app')
try:
    from db_connector import SentimentDB
    DB_ENABLED = True
except ImportError:
    print("Database connector not found, running without database storage")
    DB_ENABLED = False

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


def main():
    """Main function to run the sentiment analysis."""
    # Take user input
    text = input("Enter a sentence for sentiment analysis: ")

    # Get sentiment scores
    scores = analyzer.polarity_scores(text)
    compound_score = scores["compound"]

    # Output in three lines
    print(f"Raw scores: {scores}")
    result_color = score_to_color(compound_score)
    print(f"Color: {result_color}")
    result_interpretation = sentiment_to_interpretation(compound_score)
    print(f"Interpretation: {result_interpretation}")

    # Store in database if enabled
    if DB_ENABLED:
        try:
            db = SentimentDB()
            result_id = db.store_analysis(text, scores, result_color, result_interpretation)
            print(f"Analysis stored in database with ID: {result_id}")
        except Exception as storage_error:
            print(f"Error storing in database: {storage_error}")


# Execute main function when run as a script
if __name__ == "__main__":
    main()
