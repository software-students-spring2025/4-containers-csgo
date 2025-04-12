"""Unit tests for API routes and behavior."""

from unittest.mock import patch
import werkzeug
from app.api import app

# Workaround: set dummy version if missing (for pytest compatibility with werkzeug)
if not hasattr(werkzeug, "__version__"):
    werkzeug.__version__ = "dummy-version"


def test_analyze_happy_path():
    """Check if the path is good."""
    with app.test_client() as c, patch("app.api.analyzer") as mock_an, patch(
        "app.api.DB_CONNECTED", False
    ):  # skip Mongo
        mock_an.polarity_scores.return_value = {
            "compound": 0.9,
            "pos": 1,
            "neg": 0,
            "neu": 0,
        }
        r = c.post("/analyze", json={"text": "hi"})
        data = r.get_json()
        assert r.status_code == 200
        assert data["color"] == "orange"
        assert "interpretation" in data


def test_api_analyze_success():
    """Happy_path test for /analyze route (no real DB)."""
    from app import api  # pylint: disable=import-outside-toplevel

    with patch.object(api, "DB_CONNECTED", False), patch.object(
        api.analyzer,
        "polarity_scores",
        return_value={"pos": 0.7, "neg": 0.0, "neu": 0.3, "compound": 0.7},
    ):

        client = api.app.test_client()
        resp = client.post("/analyze", json={"text": "great"})
        data = resp.get_json()

        assert resp.status_code == 200
        assert data["color"] == "orange"
        assert data["interpretation"].startswith("🟧")


def test_api_analyze_missing_text():
    """/analyze should return 400 when no text is provided."""
    from app import api  # pylint: disable=import-outside-toplevel

    client = api.app.test_client()
    resp = client.post("/analyze", json={})

    assert resp.status_code == 400
    assert resp.get_json()["error"] == "No text provided"


def test_analyze_db_connected_stores_data():
    """Check that if DB_CONNECTED is True, we store data and no errors."""
    from app import api  # pylint: disable=import-outside-toplevel

    with patch.object(api, "DB_CONNECTED", True), patch.object(
        api.analyses, "insert_one"
    ) as mock_insert, patch.object(
        api.analyzer,
        "polarity_scores",
        return_value={"pos": 0.3, "neg": 0.0, "neu": 0.7, "compound": 0.3},
    ):
        mock_insert.return_value.inserted_id = "fake_id"

        client = api.app.test_client()
        resp = client.post("/analyze", json={"text": "db test"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["text"] == "db test"


def test_analyze_db_error():
    """Force an exception storing data in DB to cover the except block."""
    from app import api  # pylint: disable=import-outside-toplevel

    with patch.object(api, "DB_CONNECTED", True), patch.object(
        api.analyses, "insert_one", side_effect=Exception("Mock DB fail")
    ), patch.object(
        api.analyzer,
        "polarity_scores",
        return_value={"pos": 0.3, "neg": 0.0, "neu": 0.7, "compound": 0.3},
    ):
        client = api.app.test_client()
        resp = client.post("/analyze", json={"text": "trigger db error"})
        # The route returns 200 still, but logs "Error storing in database"
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["text"] == "trigger db error"
