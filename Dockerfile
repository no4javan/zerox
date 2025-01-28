FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    ghostscript \
    graphicsmagick \
    libreoffice \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

# requirements.txt
fastapi==0.100.0
uvicorn==0.22.0
python-multipart==0.0.6
py-zerox==0.1.0
python-dotenv==1.0.0
pydantic==2.0.0
