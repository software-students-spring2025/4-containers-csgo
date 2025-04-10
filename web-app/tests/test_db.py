"""Unit tests for db_connector.py."""

import os
import sys
from unittest.mock import MagicMock
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db_connector import SentimentDB


def test_store_analysis_inserts_correct_document():
    """Test that store_analysis() inserts the correct document and returns its ID."""
    with patch("db_connector.MongoClient") as mock_client:
        mock_collection = MagicMock()
        mock_collection.insert_one.return_value.inserted_id = "mock_id"

        mock_db_instance = MagicMock()
        mock_db_instance.analyses = mock_collection
        mock_client.return_value.__getitem__.return_value = mock_db_instance

        db = SentimentDB()
        result = db.store_analysis("Hello", {"pos": 1}, "green", "Happy")

        assert result == "mock_id"
        mock_collection.insert_one.assert_called_once()
        inserted_doc = mock_collection.insert_one.call_args[0][0]
        assert inserted_doc["text"] == "Hello"
        assert inserted_doc["color"] == "green"
        assert inserted_doc["interpretation"] == "Happy"
        assert "timestamp" in inserted_doc


def test_get_recent_analyses_returns_expected_list():
    """Test that get_recent_analyses() returns a limited sorted list of analyses."""
    with patch("db_connector.MongoClient") as mock_client:
        mock_collection = MagicMock()
        mock_cursor = [{"text": "recent analysis"}]
        mock_collection.find.return_value.sort.return_value.limit.return_value = mock_cursor

        mock_db_instance = MagicMock()
        mock_db_instance.analyses = mock_collection
        mock_client.return_value.__getitem__.return_value = mock_db_instance

        db = SentimentDB()
        result = db.get_recent_analyses(1)

        assert result == mock_cursor
        mock_collection.find.assert_called_once()
        mock_collection.find.return_value.sort.assert_called_once_with("timestamp", -1)
        mock_collection.find.return_value.sort.return_value.limit.assert_called_once_with(1)


def test_get_analysis_by_id_calls_find_one():
    """Test that get_analysis_by_id() converts string ID and queries MongoDB properly."""
    with patch("db_connector.MongoClient") as mock_client:
        with patch("bson.objectid.ObjectId") as mock_objectid:
            mock_objectid.return_value = "mock_obj_id"

            mock_collection = MagicMock()
            mock_collection.find_one.return_value = {"text": "single analysis"}

            mock_db_instance = MagicMock()
            mock_db_instance.analyses = mock_collection
            mock_client.return_value.__getitem__.return_value = mock_db_instance

            db = SentimentDB()
            result = db.get_analysis_by_id("abc123")

            mock_objectid.assert_called_once_with("abc123")
            mock_collection.find_one.assert_called_once_with({"_id": "mock_obj_id"})
            assert result["text"] == "single analysis"
