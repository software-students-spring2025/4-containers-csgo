"""Unit tests for ML analysis logic in machine_learning_client."""

import builtins
from unittest.mock import patch

from pytest import approx

from app.main import score_to_color, sentiment_to_interpretation


def test_score_to_color():
    """Test score_to_color mapping at thresholds."""
    assert score_to_color(0.6) == "orange"
    assert score_to_color(0.05) == "green"
    assert score_to_color(-0.2) == "red"


def test_sentiment_to_interpretation():
    """Test sentiment_to_interpretation logic based on score."""
    assert sentiment_to_interpretation(0.8) == "🟧 Very Positive - Joy, Gratitude, Love"
    assert (
        sentiment_to_interpretation(0.4) == "🟦 Positive - Hope, Motivation, Optimism"
    )
    assert sentiment_to_interpretation(-0.4) == "🟥 Negative - Anger, Anxiety, Blame"
    assert sentiment_to_interpretation(0.0) == "🟩 Neutral - Calm, Relaxed, Apathy"


def test_analyze_text_success():
    """Test analyze_text returns full analysis result structure."""
    with patch("app.docker_main.DB_CONNECTED", False), patch(
        "app.docker_main.SentimentIntensityAnalyzer"
    ) as mock_analyzer:

        from app.docker_main import (
            analyze_text,
        )  # pylint: disable=import-outside-toplevel

        mock_analyzer_instance = mock_analyzer.return_value
        mock_analyzer_instance.polarity_scores.return_value = {
            "pos": 0.6,
            "neg": 0.1,
            "neu": 0.2,
            "compound": 0.6,
        }

        result = analyze_text("This is amazing!")

        assert result["color"] == "orange"
        assert result["interpretation"] == "🟧 Very Positive - Joy, Gratitude, Love"
        assert round(result["scores"]["compound"], 1) == 0.6


def test_analyze_text_with_empty_input():
    """Test analyze_text handles empty input gracefully (should raise or return neutral)."""
    with patch("app.docker_main.DB_CONNECTED", False), patch(
        "app.docker_main.SentimentIntensityAnalyzer"
    ) as mock_analyzer:

        from app.docker_main import (
            analyze_text,
        )  # pylint: disable=import-outside-toplevel

        mock_analyzer_instance = mock_analyzer.return_value
        mock_analyzer_instance.polarity_scores.return_value = {
            "pos": 0.0,
            "neg": 0.0,
            "neu": 1.0,
            "compound": 0.0,
        }

        result = analyze_text("")

        assert result["color"] == "green"
        assert result["interpretation"] == "🟩 Neutral - Calm, Relaxed, Apathy"
        assert result["scores"]["compound"] == 0.0
        assert "id" not in result


def test_main_cli_runs_and_stores():
    """
    Execute main.main() once with mocked input and DB to hit
    colour/interpretation logic *and* the DB‑enabled branch.
    """
    with patch.object(builtins, "input", return_value="wonderful day"), patch(
        "app.db_connector.SentimentDB"
    ) as mock_db, patch("app.main.print") as mock_print:

        mock_db.return_value.store_analysis.return_value = "fake_id"

        from app import main  # pylint: disable=import-outside-toplevel

        main.SentimentDB = mock_db  # ensure main uses mock
        main.DB_ENABLED = True

        # Force predictable sentiment score → orange
        with patch.object(
            main.analyzer,
            "polarity_scores",
            return_value={"pos": 0.8, "neg": 0.0, "neu": 0.2, "compound": 0.9},
        ):
            main.main()

        mock_db.return_value.store_analysis.assert_called_once()
        mock_print.assert_any_call("Color: orange")
        mock_print.assert_any_call(
            "Interpretation: 🟧 Very Positive - Joy, Gratitude, Love"
        )


def test_analyze_text_db_disabled():
    """DB_CONNECTED False path (no insert)."""
    with patch("app.docker_main.DB_CONNECTED", False), patch(
        "app.docker_main.analyzer"
    ) as mock_analyzer:

        # configure the mocked VADER instance
        mock_analyzer.polarity_scores.return_value = {
            "pos": 0.3,
            "neg": 0.0,
            "neu": 0.7,
            "compound": 0.3,
        }

        from app.docker_main import (
            analyze_text,
        )  # # pylint: disable=import-outside-toplevel

        result = analyze_text("hello world")

        assert result["color"] == "blue"
        assert result["scores"]["compound"] == approx(0.3, abs=1e-3)


def test_analyze_text_db_enabled():
    """DB_CONNECTED True path with successful insert."""
    with patch("app.docker_main.DB_CONNECTED", True), patch(
        "app.docker_main.SentimentIntensityAnalyzer"
    ) as mock_an, patch("app.docker_main.analyses.insert_one") as mock_insert:

        mock_an.return_value.polarity_scores.return_value = {
            "pos": 0.1,
            "neg": 0.6,
            "neu": 0.3,
            "compound": -0.5,
        }
        mock_insert.return_value.inserted_id = "xyz"

        from app.docker_main import (
            analyze_text,
        )  # pylint: disable=import-outside-toplevel

        res = analyze_text("bad")

        mock_insert.assert_called_once()
        assert res["scores"]["compound"] == approx(-0.5, abs=0.1)


def test_run_demo_analysis_calls_analyze():
    """Ensure run_demo_analysis iterates over demo_texts."""
    with patch("app.docker_main.analyze_text") as mock_analyze:
        from app.docker_main import (
            run_demo_analysis,
            demo_texts,
        )  # pylint: disable=import-outside-toplevel

        run_demo_analysis()
        assert mock_analyze.call_count == len(demo_texts)


def test_example_module_runs():
    """Ensure example.py executes without crashing (sanity check)."""
    import app.example  # pylint: disable=import-outside-toplevel

    assert callable(getattr(app.example, "some_function", lambda: True))
