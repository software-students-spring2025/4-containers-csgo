"""Simple Flask app for Docker example with sentiment analysis integration."""

from flask import Flask, render_template, request, jsonify
import subprocess
import sys

app = Flask(__name__)

@app.route("/")
def index():
    """Route that returns the index page using render_template."""
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    """Endpoint that calls main.py to perform sentiment analysis."""
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Call main.py as a subprocess and pass the text (plus newline) as input.
        process = subprocess.run(
            [sys.executable, "main.py"],
            input=text + "\n",
            capture_output=True,
            text=True,
            timeout=10
        )
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Processing timeout"}), 500

    # Process the output from main.py
    output = process.stdout.strip().splitlines()
    # Expected output lines:
    # "Raw scores: {...}"
    # "Color: <color>"
    # "Interpretation: <interpretation>"
    color = None
    interpretation = None
    for line in output:
        if line.startswith("Color:"):
            color = line[len("Color:"):].strip()
        elif line.startswith("Interpretation:"):
            interpretation = line[len("Interpretation:"):].strip()

    if color and interpretation:
        return jsonify({"color": color, "interpretation": interpretation})
    else:
        return jsonify({"error": "Failed to parse sentiment output"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
