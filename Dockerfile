
# Use Python 3.11
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application and trained model
COPY app.py .
COPY mnist_digit_model.keras .

# Expose Streamlit port
EXPOSE 8501

# Start Streamlit application
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]

