# Use the official Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /app

# Expose the Flask port (optional but good practice)
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]
