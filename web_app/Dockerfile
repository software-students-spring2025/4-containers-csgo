# Use the official Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file first, then install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application code
COPY . .

# Expose the Flask port (optional but good practice)
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]

