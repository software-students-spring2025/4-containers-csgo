# Use a lightweight base image
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir vaderSentiment pymongo flask requests

# Copy the application code
COPY app/ .

# Run the API service
CMD ["python", "api.py"]