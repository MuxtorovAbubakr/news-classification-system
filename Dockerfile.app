# Start with Python
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy and install frontend dependencies
COPY requirements-app.txt .
RUN pip install --no-cache-dir -r requirements-app.txt

# Copy Streamlit application
COPY app/ ./app/

# Streamlit uses port 8501 by default
EXPOSE 8501

# Start Streamlit
CMD ["streamlit", "run", "app/streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]