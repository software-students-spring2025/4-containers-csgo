import pytest
import requests
from app import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """Test if the index route (/) renders correctly and returns status code 200."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"<html" in response.data


def test_index_route_has_textarea_and_button(client):
    """Ensure that index page contains the textarea and analyze button."""
    response = client.get('/')
    html = response.get_data(as_text=True)
    assert "<textarea" in html, "Page should contain a textarea for input"
    assert "Analyze Sentiment" in html, "Page should contain Analyze button text"


def test_analyze_route_success(client):
    """Test /analyze endpoint for successful sentiment analysis using mocked ML client."""
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


def test_analyze_route_no_text(client):
    """Test /analyze endpoint returns 400 error when no text is provided in request."""
    response = client.post('/analyze', json={})
    data = response.get_json()

    assert response.status_code == 400
    assert "No text provided" in data["error"]


def test_analyze_route_timeout(client):
    """Test /analyze endpoint handles ML client timeout properly."""
    with patch('requests.post', side_effect=requests.exceptions.Timeout()):
        response = client.post('/analyze', json={"text": "Timeout test"})
        data = response.get_json()

        assert response.status_code == 500
        assert "Connection error" in data["error"]


def test_analyze_route_connection_error(client):
    """Test /analyze endpoint handles connection error to ML client."""
    with patch('requests.post', side_effect=requests.exceptions.ConnectionError("Mocked connection error")):
        response = client.post('/analyze', json={"text": "Error test"})
        data = response.get_json()

        assert response.status_code == 500
        assert "Connection error" in data["error"]


def test_history_route_with_mocked_data(client):
    """Test /history route renders sentiment history properly from mocked database."""
    mock_analyses = [
        {
            "text": "Test text",
            "color": "blue",
            "interpretation": "Positive",
            "scores": {"pos": 0.5, "neg": 0.1, "neu": 0.4, "compound": 0.6},
            "timestamp": None
        }
    ]

    with patch('app.SentimentDB') as MockDB:
        mock_instance = MockDB.return_value
        mock_instance.get_recent_analyses.return_value = mock_analyses

        response = client.get('/history')
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert "Test text" in html
        assert "Positive" in html
        assert "Compound" in html or "compound" in html


def test_analyze_route_when_ml_service_fails(client):
    """Test when ML service responds with an error."""
    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.ok = False  # Simulate a 500 from ML client
        mock_post.return_value = mock_response

        response = client.post("/analyze", json={"text": "Something"})
        assert response.status_code == 500
        assert "ML service error" in response.get_json()["error"]


def test_history_route_handles_exception(client):
    """Test when DB throws an exception during /history."""
    with patch("app.SentimentDB") as mock_db:
        mock_db.side_effect = Exception("mock db failure")

        response = client.get("/history")
        assert response.status_code == 500
        assert "mock db failure" in response.get_json()["error"]