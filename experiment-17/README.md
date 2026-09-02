# Experiment 17: Simple Python Flask API Containerization & Kubernetes Deployment

## Objective
Create a Simple Python Flask API, Containerize the Application using Docker, Build & Push the Image to Docker Hub, and Deploy the Application using Kubernetes manifests (`Deployment` & `Service`).

---

## Task Execution Guide

### Task 1: Create Simple Flask API
Files created:
- `app.py`
- `requirements.txt`

### Task 2: Containerize the Application
File created:
- `Dockerfile`

### Task 3: Build the Docker Image
Run in terminal:
```bash
docker build -t flask-api-app .
```

### Task 4: Push the Image to Docker Hub
Replace `<dockerhub-username>` with your actual Docker Hub username:
```bash
# 1. Login to Docker Hub
docker login

# 2. Tag image with username
docker tag flask-api-app <dockerhub-username>/flask-api-app:latest

# 3. Push to registry
docker push <dockerhub-username>/flask-api-app:latest
```

### Task 5: Create Kubernetes Manifests
Files created:
- `deployment.yaml`
- `service.yaml`

Update `deployment.yaml` with your Docker Hub image name:
```yaml
image: <dockerhub-username>/flask-api-app:latest
```

### Task 6: Apply Manifests and Access API via NodePort
```bash
# 1. Apply Deployment and Service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# 2. Check Deployment and Pod status
kubectl get deployments
kubectl get pods
kubectl get services

# 3. Access API
# If using Minikube:
minikube service flask-api-service --url

# If accessing directly on host:
curl http://localhost:30007/
curl http://localhost:30007/api/health
curl http://localhost:30007/api/info
```
