"""Simple Flask app for Docker example with sentiment analysis integration."""

import subprocess
import sys
import json
from flask import Flask, render_template, request, jsonify
from db_connector import SentimentDB

app = Flask(__name__)


@app.route("/")
def index():
    """Route that returns the index page using render_template."""
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    """Endpoint that calls the ML client API to perform sentiment analysis."""
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Use requests to call the ML client API
        import requests

        response = requests.post(
            "http://ml-client:5000/analyze", json={"text": text}, timeout=10
        )

        if not response.ok:
            return jsonify({"error": "ML service error"}), 500

        result = response.json()

        return jsonify(
            {"color": result["color"], "interpretation": result["interpretation"]}
        )

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Connection error: {str(e)}"}), 500


@app.route("/history")
def history():
    """Display history of sentiment analyses."""
    try:
        db = SentimentDB()
        analyses = db.get_recent_analyses(20)

        # Convert any float timestamps to datetime objects
        for analysis in analyses:
            if isinstance(analysis.get("timestamp"), float):
                import datetime

                analysis["timestamp"] = datetime.datetime.fromtimestamp(
                    analysis["timestamp"]
                )

        return render_template("history.html", analyses=analyses)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
