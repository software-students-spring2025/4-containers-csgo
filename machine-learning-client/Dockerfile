# Use a lightweight base image
FROM python:3.11-slim

WORKDIR /app

# Copy the shell script from local machine into the container
# COPY app/main.sh .
COPY app/ .

# Make sure the script is executable
# RUN chmod +x main.sh

# Run the script when the container starts
CMD ["python", "main.py"]

