# Use an official Python base image
FROM python:3.9-slim

# Working directory
WORKDIR /app

# Install system dependencies (if needed, e.g. for OCR)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Streamlit runs on port 8501 by default
EXPOSE 8501

# Run streamlit on container start
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
