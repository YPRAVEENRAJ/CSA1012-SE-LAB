# Step 1: Use official Python slim image as base
FROM python:3.10-slim

# Step 2: Set working directory
WORKDIR /app

# Step 3: Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy application source code and tests
COPY app.py .
COPY test_app.py .

# Step 5: Expose Flask port 5000
EXPOSE 5000

# Step 6: Define default command to launch production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
