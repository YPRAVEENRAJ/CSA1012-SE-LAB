# ── Build stage ──────────────────────────────────────────────────────────────
FROM python:3.10-slim AS builder

WORKDIR /app

# Install dependencies in an isolated layer for cache efficiency
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Runtime stage ─────────────────────────────────────────────────────────────
FROM python:3.10-slim

WORKDIR /app

# Copy pre-installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy application source code
COPY app.py .
COPY test_app.py .

# Expose Flask port
EXPOSE 5000

# Default app version label (overridden by GitHub Actions at build time)
ARG APP_VERSION=2.0.0
ENV APP_VERSION=${APP_VERSION}

# Labels for image metadata
LABEL org.opencontainers.image.title="flask-cd-github-actions" \
      org.opencontainers.image.description="Experiment 19: Flask app with GitHub Actions CD pipeline" \
      org.opencontainers.image.version="${APP_VERSION}" \
      org.opencontainers.image.source="https://github.com/ypravin/CSA1012"

# Run using Gunicorn production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
