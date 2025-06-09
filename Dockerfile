# Dockerfile
# This file defines the steps to create a Docker image for the Flask application.

# 1. Start with an official Python base image.
# Using a specific version is good practice for reproducibility.
# The '-slim' variant is a smaller image, good for production.
FROM python:3.10-slim

# 2. Set the working directory inside the container.
# This is where your application code will live.
WORKDIR /app

# 3. Copy the dependencies file first.
# This leverages Docker's layer caching. If requirements.txt doesn't change,
# Docker won't re-run the pip install step on subsequent builds, speeding them up.
COPY requirements.txt .

# 4. Install the Python dependencies.
# --no-cache-dir: Disables the cache, which is not needed in a container image.
# -r: Specifies the requirements file.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code into the container.
COPY . .

# 6. Expose the port that Gunicorn will run on.
# This tells Docker that the container listens on this port.
EXPOSE 8000

# 7. Define the command to run the application.
# This is the command that will be executed when the container starts.
# It uses Gunicorn to serve the app via the wsgi.py entry point.
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "wsgi:app"]
