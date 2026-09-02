# Experiment 18: CI/CD Pipeline Setup using Jenkins and Docker

## Objective
Set up a Continuous Integration and Continuous Deployment (CI/CD) pipeline using Jenkins to automate:
1. **Source Code Checkout** from Git SCM.
2. **Automated Unit Testing** using `pytest`.
3. **Containerization** by building Docker images.
4. **Registry Push** to Docker Hub.
5. **Deployment** of the containerized application to a local/cloud target.

---

## Directory Structure
```text
experiment-18/
├── app.py              # Main Flask application
├── test_app.py         # Pytest unit tests for automated CI stage
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container creation instructions
├── .dockerignore       # Docker build exclusion file
├── Jenkinsfile         # Declarative Jenkins CI/CD pipeline script
├── README.md           # Step-by-step setup and execution guide
└── experiment-18.md    # Lab report document with full output
```

---

## Prerequisites
- **Jenkins** installed locally or running in Docker (`http://localhost:8080`).
- **Docker Engine** installed and running.
- **Python 3.10+** and `pytest`.
- **Docker Hub** account and credentials configured in Jenkins.

---

## Step-by-Step Execution Guide

### Task 1: Local Testing & Container Build Verification
```bash
cd experiment-18

# 1. Install dependencies
pip install -r requirements.txt

# 2. Execute unit tests
pytest test_app.py

# 3. Build Docker container locally
docker build -t flask-cicd-app:v1 .

# 4. Run Docker container
docker run -d -p 5000:5000 --name flask-cicd-container flask-cicd-app:v1

# 5. Verify application endpoint
curl http://localhost:5000/
curl http://localhost:5000/api/health
```

---

### Task 2: Configure Jenkins Pipeline

1. **Install Required Jenkins Plugins**:
   - Docker Pipeline Plugin
   - Git Plugin
   - JUnit Plugin

2. **Add Docker Hub Credentials**:
   - Go to `Jenkins Dashboard` -> `Manage Jenkins` -> `Credentials` -> `System` -> `Global credentials`.
   - Click `Add Credentials`.
   - **Kind**: Username with password
   - **ID**: `docker-hub-credentials`
   - **Username**: Your Docker Hub Username
   - **Password**: Docker Hub Access Token / Password

3. **Create Jenkins Pipeline Job**:
   - Click **New Item** -> Enter `Experiment-18-Pipeline` -> Select **Pipeline** -> Click **OK**.
   - Under **Pipeline Definition**:
     - Select **Pipeline script from SCM** (or paste `Jenkinsfile` directly).
     - **SCM**: Git
     - **Repository URL**: `https://github.com/<your-username>/CSA1012.git`
     - **Script Path**: `experiment-18/Jenkinsfile`

4. **Automate Build Triggers**:
   - Under **Build Triggers**, select **GitHub hook trigger for GITHUB SCM polling** OR **Poll SCM** (`H/5 * * * *`).

5. **Build & Monitor**:
   - Click **Build Now**.
   - Open **Console Output** to verify all 6 pipeline stages pass successfully!
