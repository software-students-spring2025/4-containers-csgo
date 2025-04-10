"""Unit tests for ML analysis logic in machine_learning_client."""

from unittest.mock import patch, MagicMock

from app.main import score_to_color, sentiment_to_interpretation


def test_score_to_color():
    """Test score_to_color mapping at thresholds."""
    assert score_to_color(0.6) == "orange"
    assert score_to_color(0.05) == "green"
    assert score_to_color(-0.2) == "red"


def test_sentiment_to_interpretation():
    """Test sentiment_to_interpretation logic based on score."""
    assert sentiment_to_interpretation(0.8) == "🟧 Very Positive - Joy, Gratitude, Love"
    assert sentiment_to_interpretation(0.4) == "🟦 Positive - Hope, Motivation, Optimism"
    assert sentiment_to_interpretation(-0.4) == "🟥 Negative - Anger, Anxiety, Blame"
    assert sentiment_to_interpretation(0.0) == "🟩 Neutral - Calm, Relaxed, Apathy"


def test_analyze_text_success():
    """Test analyze_text returns full analysis result structure."""
    with patch("app.docker_main.DB_CONNECTED", False), \
         patch("app.docker_main.SentimentIntensityAnalyzer") as mock_analyzer:

        from app.docker_main import analyze_text

        mock_analyzer_instance = mock_analyzer.return_value
        mock_analyzer_instance.polarity_scores.return_value = {
            "pos": 0.6,
            "neg": 0.1,
            "neu": 0.2,
            "compound": 0.6
        }

        result = analyze_text("This is amazing!")

        assert result["color"] == "orange"
        assert result["interpretation"] == "🟧 Very Positive - Joy, Gratitude, Love"
        assert round(result["scores"]["compound"], 1) == 0.6


def test_analyze_text_with_empty_input():
    """Test analyze_text handles empty input gracefully (should raise or return neutral)."""
    with patch("app.docker_main.DB_CONNECTED", False), \
         patch("app.docker_main.SentimentIntensityAnalyzer") as mock_analyzer:

        from app.docker_main import analyze_text

        mock_analyzer_instance = mock_analyzer.return_value
        mock_analyzer_instance.polarity_scores.return_value = {
            "pos": 0.0,
            "neg": 0.0,
            "neu": 1.0,
            "compound": 0.0
        }


        result = analyze_text("")

        assert result["color"] == "green"
        assert result["interpretation"] == "🟩 Neutral - Calm, Relaxed, Apathy"
        assert result["scores"]["compound"] == 0.0
        assert "id" not in result
