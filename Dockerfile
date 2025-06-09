# Use the official Python 3.10.12 image
FROM python:3.10.12-slim

# Set the working directory
WORKDIR /app

# Copy only requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 5001
EXPOSE 5001

# Use this command for development (with reload)
 CMD ["python", "main.py"]

# Use this command for production (no reload)
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001", "--log-level", "info"]
