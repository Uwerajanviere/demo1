# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir reduces image size
# -r installs from requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY main.py .

# Expose port 8000 (FastAPI default)
EXPOSE 8000

# Command to run the application
# --host 0.0.0.0 makes it accessible from outside the container
# --port 8000 matches the exposed port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
