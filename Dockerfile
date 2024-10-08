# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev-compat \
    build-essential \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*  
    # Clean up after installing packages

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Set environment variables
ENV PORT=8080
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/meditation-credentials.json

# Run Gunicorn server (note the fix for the flag)
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
