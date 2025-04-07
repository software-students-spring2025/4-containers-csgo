from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize the analyzer
analyzer = SentimentIntensityAnalyzer()

# Mapping functions
def score_to_color(score):
    if score <= -0.6:
        return "black"
    elif score <= -0.2:
        return "red"
    elif score < 0.2:
        return "green"
    elif score < 0.6:
        return "blue"
    else:
        return "orange"

def sentiment_to_interpretation(score):
    if score <= -0.6:
        return "⬛️ Very Negative - Shame, Powerlessness"
    elif score <= -0.2:
        return "🟥 Negative - Anger, Anxiety, Blame"
    elif score < 0.2:
        return "🟩 Neutral - Calm, Relaxed, Apathy"
    elif score < 0.6:
        return "🟦 Positive - Hope, Motivation, Optimism"
    else:
        return "🟧 Very Positive - Joy, Gratitude, Love"

# Take user input
text = input("Enter a sentence for sentiment analysis: ")

# Get sentiment scores
scores = analyzer.polarity_scores(text)
compound_score = scores['compound']

# Output in three lines
print("Raw scores:", scores)
print("Color:", score_to_color(compound_score))
print("Interpretation:", sentiment_to_interpretation(compound_score))
