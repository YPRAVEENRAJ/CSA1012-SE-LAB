# Step 1: Base image using official Python slim
FROM python:3.10-slim

# Step 2: Set working directory inside container
WORKDIR /app

# Step 3: Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy application code
COPY app.py .

# Step 5: Expose Flask port 5000
EXPOSE 5000

# Step 6: Command to run application using Gunicorn WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
