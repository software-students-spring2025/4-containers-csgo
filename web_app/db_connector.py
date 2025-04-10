"""MongoDB connector for sentiment analysis application."""

import os
import datetime
from pymongo import MongoClient

# Get MongoDB connection details from environment variables or use defaults
MONGO_URI = os.environ.get("MONGODB_URI", "mongodb://root:example@mongodb:27017/")
DB_NAME = os.environ.get("MONGODB_DB", "sentiment_analysis")


class SentimentDB:
    """Class to handle database operations for sentiment analysis."""

    def __init__(self):
        """Initialize the database connection."""
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.analyses = self.db.analyses

    def store_analysis(self, text, scores, color, interpretation):
        """Store a sentiment analysis result in the database."""
        document = {
            "text": text,
            "scores": scores,
            "color": color,
            "interpretation": interpretation,
            "timestamp": datetime.datetime.now(datetime.UTC), # Always use datetime objects
        }

        result = self.analyses.insert_one(document)
        return str(result.inserted_id)

    def get_recent_analyses(self, limit=10):
        """
        Retrieve recent sentiment analyses.

        Args:
            limit (int): Maximum number of records to return

        Returns:
            list: Recent analysis records
        """
        cursor = self.analyses.find().sort("timestamp", -1).limit(limit)
        return list(cursor)

    def get_analysis_by_id(self, analysis_id):
        """
        Retrieve a specific analysis by ID.

        Args:
            analysis_id (str): The ID of the analysis to retrieve

        Returns:
            dict: The analysis document
        """
        from bson.objectid import ObjectId

        return self.analyses.find_one({"_id": ObjectId(analysis_id)})
