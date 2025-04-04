"""Simple Flask app for Docker example."""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    """Route that returns a hello message."""
    return "Hello from Flask in Docker!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
