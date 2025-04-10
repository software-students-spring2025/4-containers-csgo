// This script will run when the MongoDB container first starts
db = db.getSiblingDB('sentiment_analysis');

// Create collections
db.createCollection('analyses');

// Create indexes for efficient queries
db.analyses.createIndex({ "timestamp": -1 });
db.analyses.createIndex({ "compound_score": 1 });

// Insert a test document
db.analyses.insertOne({
  text: "This is a test sentiment analysis entry.",
  scores: {
    positive: 0.0,
    negative: 0.0,
    neutral: 1.0,
    compound: 0.0
  },
  color: "green",
  interpretation: "🟩 Neutral - Calm, Relaxed, Apathy",
  timestamp: new Date()
});

print("Database initialization completed!");