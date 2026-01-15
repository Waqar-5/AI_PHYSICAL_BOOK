# Base Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend code
COPY . .

# Run FastAPI on HF Spaces port 7860
# Tell Uvicorn that the FastAPI app is called `app` inside app.py
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
