# Use a slim Python 3.12 image as the base
FROM python:3.12.3-slim

# Set a working directory for the application
WORKDIR /app

# Copy requirements.txt file
COPY requirements.txt .

# Install Python dependencies (mode: quiet)
RUN pip install -q -r requirements.txt

# Copy application code
COPY . .

# Expose the port where  Django application listens (default: 8000)
EXPOSE 8000

# Run the Gunicorn web server to serve Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
