"""Unit tests for Flask app routes."""

import pytest
import requests
from unittest.mock import patch, MagicMock

from app import app


@pytest.fixture
def client():
    """Provide a Flask test client."""
    with app.test_client() as client:
        yield client


def test_index_route(client_):
    """Test if the index route renders successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"<html" in response.data


def test_index_route_has_textarea_and_button(client_):
    """Test that index page includes textarea and analyze button."""
    response = client.get('/')
    html = response.get_data(as_text=True)
    assert "<textarea" in html
    assert "Analyze Sentiment" in html


def test_analyze_route_success(client_):
    """Test analyze route with valid text and successful ML response."""
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "color": "Green",
            "interpretation": "Positive sentiment"
        }
        mock_post.return_value = mock_response

        response = client.post('/analyze', json={"text": "I love Python!"})
        data = response.get_json()

        assert response.status_code == 200
        assert data["color"] == "Green"
        assert data["interpretation"] == "Positive sentiment"


def test_analyze_route_no_text(client_):
    """Test analyze route with missing text input."""
    response = client.post('/analyze', json={})
    data = response.get_json()

    assert response.status_code == 400
    assert "No text provided" in data["error"]


def test_analyze_route_timeout(client_):
    """Test analyze route when ML client times out."""
    with patch('requests.post', side_effect=requests.exceptions.Timeout()):
        response = client.post('/analyze', json={"text": "Timeout test"})
        data = response.get_json()

        assert response.status_code == 500
        assert "Connection error" in data["error"]


def test_analyze_route_connection_error(client_):
    """Test analyze route when ML client is unreachable."""
    with patch('requests.post', 
               side_effect=requests.exceptions.ConnectionError("Mocked connection error")):
        response = client.post('/analyze', json={"text": "Error test"})
        data = response.get_json()

        assert response.status_code == 500
        assert "Connection error" in data["error"]


def test_analyze_route_when_ml_service_fails(client_):
    """Test analyze route when ML service responds with an error."""
    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.ok = False
        mock_post.return_value = mock_response

        response = client.post("/analyze", json={"text": "Something"})
        assert response.status_code == 500
        assert "ML service error" in response.get_json()["error"]


def test_history_route_with_mocked_data(client_):
    """Test history route rendering with mocked DB results."""
    mock_analyses = [
        {
            "text": "Test text",
            "color": "blue",
            "interpretation": "Positive",
            "scores": {"pos": 0.5, "neg": 0.1, "neu": 0.4, "compound": 0.6},
            "timestamp": None
        }
    ]

    with patch('app.SentimentDB') as mock_db:
        mock_instance = mock_db.return_value
        mock_instance.get_recent_analyses.return_value = mock_analyses

        response = client.get('/history')
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert "Test text" in html
        assert "Positive" in html
        assert "Compound" in html or "compound" in html


def test_history_route_handles_exception(client_):
    """Test history route when database throws an exception."""
    with patch("app.SentimentDB") as mock_db:
        mock_db.side_effect = Exception("mock db failure")

        response = client.get("/history")
        assert response.status_code == 500
        assert "mock db failure" in response.get_json()["error"]
