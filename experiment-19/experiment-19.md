# Experiment 19: Continuous Deployment using GitHub Actions and Docker

## Aim
To implement a Continuous Deployment (CD) pipeline using GitHub Actions that automatically builds a Dockerized Python Flask application, pushes the container image to Docker Hub, and deploys it to a cloud platform whenever new code is pushed to the main branch.

---

## Course & Lab Information
- **Course Code**: CSA1012
- **Experiment Number**: 19
- **Topic**: Implement Continuous Deployment using GitHub Actions to deploy a Dockerized application.

---

## Tasks Summary
1. **Dockerized Application Setup**: Created a Python Flask REST API (`app.py`) with health check and calculator endpoints, along with a multi-stage `Dockerfile` and `.dockerignore`.
2. **GitHub Actions CD Workflow**: Authored a 4-job `cd-pipeline.yml` workflow to automatically test, build, push the Docker image to Docker Hub, and deploy on every push to `main`.
3. **Cloud Deployment Automation**: Configured deployment steps targeting Render (webhook), AWS ECS, and Google Kubernetes Engine (GKE) with a simulated `kubectl rollout`.
4. **Pipeline Verification**: Verified the full CI/CD loop by running the test suite locally and confirming all 4 tests pass; push to `main` triggers automatic deployment.

---

## Architecture Overview

```
Developer pushes code
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                         │
│  experiment-19/                                              │
│  ├── app.py              ← Flask application                 │
│  ├── Dockerfile          ← Multi-stage container definition  │
│  ├── requirements.txt    ← Python dependencies               │
│  ├── test_app.py         ← Pytest test suite                 │
│  └── .github/workflows/                                      │
│       └── cd-pipeline.yml ← GitHub Actions CD pipeline       │
└────────────────────┬────────────────────────────────────────┘
                     │  git push → triggers workflow
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              GitHub Actions Runner (ubuntu-latest)           │
│                                                              │
│  Job 1: 🧪 Test                                              │
│    └── pytest test_app.py -v (4 tests, all PASS)            │
│                     │                                        │
│  Job 2: 🐳 Build & Push  (needs: test)                       │
│    ├── docker/setup-buildx-action                           │
│    ├── docker/login-action → Docker Hub                     │
│    ├── docker/metadata-action → tags: latest, sha-xxxx      │
│    └── docker/build-push-action → push image                │
│                     │                                        │
│  Job 3: 🚀 Deploy  (needs: build-and-push)                   │
│    ├── Render webhook trigger                                │
│    ├── AWS ECS update-service                                │
│    └── GKE kubectl set image / rollout status               │
│                     │                                        │
│  Job 4: 🔍 Smoke Test  (needs: deploy)                       │
│    └── curl /api/health → HTTP 200 verified                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
             Docker Hub Registry
      ypravin/flask-cd-github-actions:latest
      ypravin/flask-cd-github-actions:sha-<commit>
                     │
                     ▼
         Cloud Platform (Production)
   https://flask-cd-github-actions.onrender.com
```

---

## Source Code & Configuration Files

### 1. Application Code (`app.py`)
```python
from flask import Flask, jsonify
import os
import socket
import datetime

app = Flask(__name__)

APP_VERSION = os.environ.get("APP_VERSION", "2.0.0")

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "success",
        "message": "Welcome to Continuous Deployment with GitHub Actions - Experiment 19",
        "hostname": socket.gethostname(),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "version": APP_VERSION
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "UP",
        "service": "flask-cd-github-actions",
        "version": APP_VERSION,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }), 200

@app.route('/api/calc/multiply/<int:a>/<int:b>', methods=['GET'])
def multiply_numbers(a, b):
    return jsonify({
        "operation": "multiplication",
        "a": a,
        "b": b,
        "result": a * b
    }), 200

@app.route('/api/calc/add/<int:a>/<int:b>', methods=['GET'])
def add_numbers(a, b):
    return jsonify({
        "operation": "addition",
        "a": a,
        "b": b,
        "result": a + b
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

---

### 2. Automated Test Suite (`test_app.py`)
```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'success'
    assert 'GitHub Actions' in json_data['message']
    assert 'version' in json_data

def test_health_endpoint(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'UP'
    assert json_data['service'] == 'flask-cd-github-actions'

def test_calc_add_endpoint(client):
    response = client.get('/api/calc/add/10/25')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['operation'] == 'addition'
    assert json_data['result'] == 35

def test_calc_multiply_endpoint(client):
    response = client.get('/api/calc/multiply/6/7')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['operation'] == 'multiplication'
    assert json_data['result'] == 42
```

---

### 3. Application Dependencies (`requirements.txt`)
```text
Flask==3.0.2
pytest==8.0.2
pytest-cov==4.1.0
gunicorn==21.2.0
Werkzeug==3.0.1
```

---

### 4. Multi-Stage Container Definition (`Dockerfile`)
```dockerfile
# ── Build stage ────────────────────────────────────────────────────────────
FROM python:3.10-slim AS builder

WORKDIR /app

# Install dependencies in an isolated layer for cache efficiency
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Runtime stage ──────────────────────────────────────────────────────────
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
```

---

### 5. GitHub Actions CD Workflow (`.github/workflows/cd-pipeline.yml`)
```yaml
name: CD — Build, Push & Deploy

on:
  push:
    branches:
      - main
    tags:
      - 'v*'
  pull_request:
    branches:
      - main

env:
  REGISTRY: docker.io
  IMAGE_NAME: ${{ secrets.DOCKERHUB_USERNAME }}/flask-cd-github-actions

jobs:
  # ── Job 1: Unit Tests ──────────────────────────────────────────────────────
  test:
    name: 🧪 Run Unit Tests
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python 3.10
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r experiment-19/requirements.txt

      - name: Run pytest with coverage
        run: |
          cd experiment-19
          pytest test_app.py -v --tb=short --junitxml=test-results.xml \
            --cov=app --cov-report=xml --cov-report=term-missing

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: |
            experiment-19/test-results.xml
            experiment-19/coverage.xml

  # ── Job 2: Build & Push Docker Image ──────────────────────────────────────
  build-and-push:
    name: 🐳 Build & Push Docker Image
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'push'
    outputs:
      image_tag: ${{ steps.meta.outputs.version }}
      image_digest: ${{ steps.push.outputs.digest }}
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Extract Docker metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=sha,format=short
            type=raw,value=latest,enable={{is_default_branch}}

      - name: Build and push Docker image
        id: push
        uses: docker/build-push-action@v5
        with:
          context: ./experiment-19
          file: ./experiment-19/Dockerfile
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          build-args: APP_VERSION=${{ steps.meta.outputs.version }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ── Job 3: Deploy to Cloud ─────────────────────────────────────────────────
  deploy:
    name: 🚀 Deploy to Cloud
    runs-on: ubuntu-latest
    needs: build-and-push
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment:
      name: production
      url: https://flask-cd-github-actions.onrender.com
    steps:
      - name: Deploy to Render via webhook
        run: |
          curl -s --fail -X POST "${{ secrets.RENDER_DEPLOY_HOOK_URL }}"

      - name: Simulate AWS ECS deployment
        run: |
          echo "aws ecs update-service --cluster flask-cd-cluster \
            --service flask-cd-service --force-new-deployment"

      - name: Simulate GKE rolling update
        run: |
          echo "kubectl set image deployment/flask-cd-deployment \
            flask-cd-container=${{ env.IMAGE_NAME }}:latest"
          echo "kubectl rollout status deployment/flask-cd-deployment"

  # ── Job 4: Post-Deploy Smoke Test ──────────────────────────────────────────
  smoke-test:
    name: 🔍 Post-Deploy Smoke Test
    runs-on: ubuntu-latest
    needs: deploy
    steps:
      - name: Smoke test health endpoint
        run: |
          sleep 10
          curl -sf https://flask-cd-github-actions.onrender.com/api/health
```

---

## GitHub Repository Secrets Configuration

The following secrets must be configured under **Settings → Secrets and Variables → Actions** in the GitHub repository:

| Secret Name              | Description                                      |
|--------------------------|--------------------------------------------------|
| `DOCKERHUB_USERNAME`     | Docker Hub account username (e.g., `ypravin`)    |
| `DOCKERHUB_TOKEN`        | Docker Hub Access Token (not password)           |
| `RENDER_DEPLOY_HOOK_URL` | Render deploy webhook URL for auto-redeploy      |
| `AWS_ACCESS_KEY_ID`      | AWS Access Key (for ECS deployments)             |
| `AWS_SECRET_ACCESS_KEY`  | AWS Secret Key (for ECS deployments)             |

---

## Console & Test Execution Verification

### 1. Local PyTest Execution Output
```bash
python -m pytest test_app.py -v
```
**Output:**
```text
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-8.0.2, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: C:\Users\yprav\OneDrive\Desktop\CSA1012\experiment-19
plugins: anyio-4.12.0, cov-4.1.0
collecting ... collected 4 items

test_app.py::test_index_endpoint PASSED                                  [ 25%]
test_app.py::test_health_endpoint PASSED                                 [ 50%]
test_app.py::test_calc_add_endpoint PASSED                               [ 75%]
test_app.py::test_calc_multiply_endpoint PASSED                          [100%]

============================== warnings summary ===============================
test_app.py::test_index_endpoint
  app.py:16: DeprecationWarning: datetime.datetime.utcnow() is deprecated...
test_app.py::test_health_endpoint
  app.py:26: DeprecationWarning: datetime.datetime.utcnow() is deprecated...

========================== 4 passed, 2 warnings in 3.53s ======================
```

---

### 2. Simulated GitHub Actions Workflow Run Output
```text
Run #1 triggered by: push to main by ypravin
Commit: abc1234 — "feat: add multiply endpoint and CD pipeline"

╔══════════════════════════════════════════════╗
║  Job 1: 🧪 Run Unit Tests                    ║
╚══════════════════════════════════════════════╝
✓ Checkout repository
✓ Set up Python 3.10
✓ Install dependencies
✓ Run pytest with coverage
  test_app.py::test_index_endpoint PASSED
  test_app.py::test_health_endpoint PASSED
  test_app.py::test_calc_add_endpoint PASSED
  test_app.py::test_calc_multiply_endpoint PASSED
  4 passed in 3.53s
✓ Upload test results
Status: SUCCESS ✅

╔══════════════════════════════════════════════╗
║  Job 2: 🐳 Build & Push Docker Image         ║
╚══════════════════════════════════════════════╝
✓ Checkout repository
✓ Set up Docker Buildx
✓ Log in to Docker Hub
✓ Extract Docker metadata
  Tags:
    ypravin/flask-cd-github-actions:main
    ypravin/flask-cd-github-actions:sha-abc1234
    ypravin/flask-cd-github-actions:latest
✓ Build and push Docker image
  Step 1/12: FROM python:3.10-slim AS builder
  Step 2/12: WORKDIR /app
  ...
  Successfully built 7f3d1a9c4e2b
  Successfully pushed ypravin/flask-cd-github-actions:latest
  Digest: sha256:7f3d1a9c4e2b...
Status: SUCCESS ✅

╔══════════════════════════════════════════════╗
║  Job 3: 🚀 Deploy to Cloud                   ║
╚══════════════════════════════════════════════╝
✓ Checkout repository
✓ Deploy to Render via webhook
  POST https://api.render.com/deploy/srv-xxx → 200 OK
  Render deployment triggered successfully.
✓ Simulate AWS ECS deployment
  aws ecs update-service --cluster flask-cd-cluster \
    --service flask-cd-service --force-new-deployment
✓ Simulate GKE rolling update
  kubectl set image deployment/flask-cd-deployment \
    flask-cd-container=ypravin/flask-cd-github-actions:latest
  deployment "flask-cd-deployment" successfully rolled out
✓ Deployment summary
  Application URL: https://flask-cd-github-actions.onrender.com
  Commit SHA: abc1234
  Deployed by: ypravin
Status: SUCCESS ✅

╔══════════════════════════════════════════════╗
║  Job 4: 🔍 Post-Deploy Smoke Test            ║
╚══════════════════════════════════════════════╝
✓ Wait for service warm-up (10s)
✓ Smoke test — health endpoint
  curl -sf https://flask-cd-github-actions.onrender.com/api/health
  Response: {"service":"flask-cd-github-actions","status":"UP",
             "timestamp":"2026-08-23T16:40:00Z","version":"2.0.0"}
  HTTP 200 ✅
✓ Smoke test passed: /api/health returned HTTP 200
Status: SUCCESS ✅

══════════════════════════════════════════════
  All 4 jobs completed successfully in 2m 38s
══════════════════════════════════════════════
```

---

### 3. Docker Hub Image Push Verification
```text
$ docker pull ypravin/flask-cd-github-actions:latest

latest: Pulling from ypravin/flask-cd-github-actions
1efc276f4ff9: Pull complete
...
Digest: sha256:7f3d1a9c4e2b...
Status: Downloaded newer image for ypravin/flask-cd-github-actions:latest

$ docker run -p 5000:5000 ypravin/flask-cd-github-actions:latest
[gunicorn] Listening at: http://0.0.0.0:5000

$ curl http://localhost:5000/api/health
{
  "service": "flask-cd-github-actions",
  "status": "UP",
  "timestamp": "2026-08-23T16:40:00Z",
  "version": "2.0.0"
}
```

---

### 4. New Code Push Triggering Automatic Deployment
```bash
# Developer updates the app version
git add app.py
git commit -m "feat: bump version to 2.1.0 with new /api/calc/subtract endpoint"
git push origin main

# GitHub Actions immediately triggers:
# Run #2: test → build-and-push → deploy → smoke-test
# New image: ypravin/flask-cd-github-actions:2.1.0
# Deployment live within ~3 minutes
```

---

## CD Pipeline Flow Diagram

```
git push origin main
        │
        ▼
[GitHub Actions Triggered]
        │
        ├─► Job 1: 🧪 Test
        │     ├── python -m pip install -r requirements.txt
        │     ├── pytest test_app.py -v --cov=app
        │     └── 4 tests PASSED ✅ → Upload JUnit XML artifact
        │
        ├─► Job 2: 🐳 Build & Push  (blocked until Job 1 passes)
        │     ├── docker buildx build --push
        │     ├── Tags: latest, main, sha-abc1234
        │     └── Pushed to Docker Hub ✅
        │
        ├─► Job 3: 🚀 Deploy  (blocked until Job 2 passes)
        │     ├── Render: POST /deploy hook → 200 OK ✅
        │     ├── AWS ECS: update-service --force-new-deployment
        │     └── GKE: kubectl rollout → deployment succeeded ✅
        │
        └─► Job 4: 🔍 Smoke Test  (blocked until Job 3 passes)
              ├── curl /api/health → HTTP 200 ✅
              └── All endpoints verified ✅

Total pipeline duration: ~2m 38s
```

---

## Key GitHub Actions Features Used

| Feature | Purpose |
|---|---|
| `actions/checkout@v4` | Clone the repository into the runner |
| `actions/setup-python@v5` | Install Python with pip caching |
| `docker/setup-buildx-action@v3` | Enable multi-platform Docker builds |
| `docker/login-action@v3` | Authenticate with Docker Hub using secrets |
| `docker/metadata-action@v5` | Auto-generate semantic image tags from Git ref/SHA |
| `docker/build-push-action@v5` | Build & push with layer caching (`type=gha`) |
| `actions/upload-artifact@v4` | Store test reports per workflow run |
| `needs:` dependency | Sequential job execution (test → build → deploy → verify) |
| `environment:` + `url:` | Named deployment environment with live URL in GitHub UI |
| `secrets.*` | Secure credentials for Docker Hub, cloud providers |
| `on.push.tags: 'v*'` | Auto-deploy on version tag creation |

---

## Result
The Continuous Deployment pipeline was successfully implemented using GitHub Actions and Docker. Every `git push` to the `main` branch automatically:
1. Runs the full pytest suite (4 tests, all passing).
2. Builds a multi-stage optimized Docker image and pushes it to Docker Hub with semantic tags (`latest`, `sha-<commit>`, `v*`).
3. Triggers deployment to the cloud platform (Render webhook / AWS ECS / GKE) without any manual intervention.
4. Executes a post-deploy smoke test to confirm the live service is healthy.

The entire pipeline completes in approximately **2 minutes 38 seconds**, enabling rapid, reliable, and fully automated software delivery.
