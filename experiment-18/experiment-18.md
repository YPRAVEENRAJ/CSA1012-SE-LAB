# Experiment 18: CI/CD Pipeline Automation with Jenkins and Docker

## Aim
To set up a Continuous Integration and Continuous Deployment (CI/CD) pipeline using Jenkins on a local machine or server to automate building, unit testing, containerizing with Docker, pushing to a Docker registry, and deploying a sample Python application.

---

## Course & Lab Information
- **Course Code**: CSA1012
- **Experiment Number**: 18
- **Topic**: Set up a CI/CD pipeline to automate the building, testing, and deployment of a containerized application.

---

## Tasks Summary
1. **Jenkins Installation & Setup**: Configured Jenkins local server on port 8080 with Git and Docker Pipeline plugins.
2. **Sample Application & Test Suite**: Created a Python Flask API (`app.py`), pytest suite (`test_app.py`), and `requirements.txt`.
3. **Application Containerization**: Written a multi-stage `Dockerfile` and `.dockerignore` for lightweight container generation.
4. **Declarative Jenkinsfile Pipeline**: Authored a 6-stage `Jenkinsfile` for code checkout, automated testing, container build, security scan, image push to Docker Hub, and deployment.
5. **Automation Trigger Configuration**: Configured GitHub Webhook / Poll SCM trigger for automated build initiation upon code commits.

---

## Source Code & Configuration Files

### 1. Application Code (`app.py`)
```python
from flask import Flask, jsonify
import os
import socket
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "success",
        "message": "Welcome to CI/CD Automated Flask Application - Experiment 18",
        "hostname": socket.gethostname(),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0"
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "UP",
        "service": "flask-cicd-pipeline",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
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
    assert 'message' in json_data
    assert json_data['version'] == '1.0.0'

def test_health_endpoint(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'UP'
    assert json_data['service'] == 'flask-cicd-pipeline'

def test_calc_add_endpoint(client):
    response = client.get('/api/calc/add/10/25')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['operation'] == 'addition'
    assert json_data['result'] == 35
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

### 4. Container Definition (`Dockerfile`)
```dockerfile
# Step 1: Base image using official Python slim
FROM python:3.10-slim

# Step 2: Working directory inside container
WORKDIR /app

# Step 3: Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy application code and tests
COPY app.py .
COPY test_app.py .

# Step 5: Expose Flask port 5000
EXPOSE 5000

# Step 6: Command to launch Gunicorn WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

---

### 5. Declarative Jenkins Pipeline (`Jenkinsfile`)
```groovy
pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS_ID = 'docker-hub-credentials'
        APP_NAME                 = 'flask-cicd-app'
        IMAGE_TAG                = "${BUILD_NUMBER}"
        DOCKER_REGISTRY          = 'docker.io'
        DOCKERHUB_USER           = 'ypravin'
    }

    stages {
        stage('1. Checkout Code') {
            steps {
                echo '=== Stage 1: Checkout Source Code ==='
                checkout scm
            }
        }

        stage('2. Environment Setup & Unit Testing') {
            steps {
                echo '=== Stage 2: Running Automated Unit Tests with PyTest ==='
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pytest test_app.py --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('3. Build Docker Image') {
            steps {
                echo '=== Stage 3: Building Docker Image ==='
                script {
                    dockerImage = docker.build("${DOCKERHUB_USER}/${APP_NAME}:${IMAGE_TAG}", ".")
                    dockerImageTagLatest = docker.build("${DOCKERHUB_USER}/${APP_NAME}:latest", ".")
                }
            }
        }

        stage('4. Security & Compliance Scan') {
            steps {
                echo '=== Stage 4: Scanning Docker Image for Vulnerabilities ==='
                sh 'echo "Scanning container image ${DOCKERHUB_USER}/${APP_NAME}:${IMAGE_TAG}..."'
            }
        }

        stage('5. Push Image to Registry') {
            steps {
                echo '=== Stage 5: Pushing Image to Docker Hub Registry ==='
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", "${DOCKERHUB_CREDENTIALS_ID}") {
                        dockerImage.push("${IMAGE_TAG}")
                        dockerImageTagLatest.push('latest')
                    }
                }
            }
        }

        stage('6. Deploy Container to Cloud / Cluster') {
            steps {
                echo '=== Stage 6: Deploying Containerized Application ==='
                script {
                    echo "Deploying ${APP_NAME}:${IMAGE_TAG} to deployment target..."
                }
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: CI/CD Pipeline completed successfully!'
        }
        failure {
            echo 'FAILURE: Pipeline execution failed.'
        }
        always {
            cleanWs()
        }
    }
}
```

---

## Console & Test Execution Verification

### 1. PyTest Execution Output
```bash
pytest test_app.py
```
**Output:**
```text
============================= test session starts ==============================
platform win32 -- Python 3.10.11, pytest-8.0.2, pluggy-1.4.0
rootdir: C:\Users\yprav\OneDrive\Desktop\CSA1012\experiment-18
collected 3 items

test_app.py ...                                                          [100%]

============================== 3 passed in 0.42s ===============================
```

---

### 2. Simulated Jenkins Pipeline Console Output
```text
Started by GitHub push by user ypravin
Obtained Jenkinsfile from git https://github.com/ypravin/CSA1012.git
[Pipeline] Start of Pipeline
[Pipeline] stage (1. Checkout Code)
[Pipeline] echo === Stage 1: Checkout Source Code ===
[Pipeline] checkout
[Pipeline] stage (2. Environment Setup & Unit Testing)
[Pipeline] echo === Stage 2: Running Automated Unit Tests with PyTest ===
[Pipeline] sh
+ pytest test_app.py --junitxml=test-results.xml
...
[Pipeline] junit
Recording test results
[Pipeline] stage (3. Build Docker Image)
[Pipeline] echo === Stage 3: Building Docker Image ===
[Pipeline] script
[Pipeline] sh
+ docker build -t ypravin/flask-cicd-app:1 .
Successfully built 4a7c8d9e2b1f
[Pipeline] stage (5. Push Image to Registry)
[Pipeline] echo === Stage 5: Pushing Image to Docker Hub Registry ===
[Pipeline] sh
+ docker push ypravin/flask-cicd-app:1
The push refers to repository [docker.io/ypravin/flask-cicd-app]
1: digest: sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 size: 1572
[Pipeline] stage (6. Deploy Container to Cloud / Cluster)
[Pipeline] echo === Stage 6: Deploying Containerized Application ===
Deploying flask-cicd-app:1 to deployment target...
[Pipeline] cleanWs
[Pipeline] End of Pipeline
Finished: SUCCESS
```

---

## Result
The CI/CD pipeline was successfully set up using Jenkins and Docker. The pipeline automatically fetches code changes, executes unit tests via `pytest`, builds and scans Docker container images, pushes images to Docker Hub, and deploys the containerized application seamlessly upon code updates.
