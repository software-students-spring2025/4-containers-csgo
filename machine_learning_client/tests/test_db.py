"""Unit tests for db_connector.py"""

from unittest.mock import patch, MagicMock
from app.db_connector import SentimentDB


def _mock_db_with_analyses():
    """mock the database to analyze."""
    mock_coll = MagicMock()
    mock_coll.insert_one.return_value.inserted_id = "fake_id"
    mock_coll.find.return_value.sort.return_value.limit.return_value = ["doc"]

    mock_db = MagicMock()
    mock_db.analyses = mock_coll
    return mock_db


def test_store_analysis_inserts_document():
    """Should insert a document into the mocked collection."""
    with patch("app.db_connector.MongoClient") as mock_client:
        mock_client.return_value.__getitem__.return_value = _mock_db_with_analyses()
        db = SentimentDB()
        _id = db.store_analysis("text", {"pos": 1}, "green", "joy")
        assert _id == "fake_id"


def test_get_recent_analyses_returns_list():
    """Check if analysis results can be returned."""
    with patch("app.db_connector.MongoClient") as mock_client:
        mock_client.return_value.__getitem__.return_value = _mock_db_with_analyses()
        db = SentimentDB()
        docs = db.get_recent_analyses(5)
        assert docs == ["doc"]
