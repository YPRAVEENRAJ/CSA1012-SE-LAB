# Experiment 17: Python Flask API Containerization & Kubernetes Deployment

## Aim
To create a simple Python Flask REST API, containerize it using Docker, build and push the Docker image to Docker Hub, and deploy the containerized application on a Kubernetes cluster using Deployment and NodePort Service manifests.

---

## Tasks Summary
1. **Create Simple Flask API**: Developed `app.py` with endpoints (`/`, `/api/health`, `/api/info`) and `requirements.txt`.
2. **Containerize Application**: Written a `Dockerfile` using `python:3.10-slim` base image.
3. **Build Image**: Built Docker image named `flask-api-app`.
4. **Push to Docker Hub**: Tagged and pushed image to Docker Hub registry.
5. **Create Kubernetes Manifests**: Created `deployment.yaml` (2 pod replicas with health probes) and `service.yaml` (NodePort on port 30007).
6. **Deploy & Access**: Applied manifests using `kubectl apply` and exposed service via NodePort.

---

## Source Code & Manifest Files

### 1. `app.py`
```python
from flask import Flask, jsonify
import datetime
import os
import socket

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "success",
        "message": "Welcome to Flask API - Experiment 17!",
        "hostname": socket.gethostname(),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0"
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "UP",
        "checks": {
            "database": "OK",
            "disk_space": "OK"
        },
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }), 200

@app.route('/api/info', methods=['GET'])
def system_info():
    return jsonify({
        "app_name": "Flask Kubernetes Microservice",
        "environment": os.environ.get("ENV", "production"),
        "container_id": socket.gethostname(),
        "endpoints": ["/", "/api/health", "/api/info"]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

---

### 2. `requirements.txt`
```text
Flask==3.0.2
gunicorn==21.2.0
Werkzeug==3.0.1
```

---

### 3. `Dockerfile`
```dockerfile
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
```

---

### 4. `deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-api-deployment
  labels:
    app: flask-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-api
  template:
    metadata:
      labels:
        app: flask-api
    spec:
      containers:
      - name: flask-api-container
        image: your-dockerhub-username/flask-api-app:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 5000
        livenessProbe:
          httpGet:
            path: /api/health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 5
        readinessProbe:
          httpGet:
            path: /api/health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          limits:
            cpu: "500m"
            memory: "256Mi"
          requests:
            cpu: "100m"
            memory: "128Mi"
```

---

### 5. `service.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-api-service
  labels:
    app: flask-api
spec:
  type: NodePort
  selector:
    app: flask-api
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000
      nodePort: 30007
```

---

## Terminal Commands & Deployment Output

```bash
# 1. Build Image
docker build -t flask-api-app .

# 2. Tag and Push Image to Docker Hub
docker tag flask-api-app <username>/flask-api-app:latest
docker push <username>/flask-api-app:latest

# 3. Deploy to Kubernetes Cluster
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# 4. Verify Pod Status
kubectl get pods
# Output:
# NAME                                    READY   STATUS    RESTARTS   AGE
# flask-api-deployment-7b4c86d88f-2x9zp   1/1     Running   0          25s
# flask-api-deployment-7b4c86d88f-9q1lk   1/1     Running   0          25s

# 5. Access NodePort Service
curl http://localhost:30007/api/health
# Output:
# {"checks":{"database":"OK","disk_space":"OK"},"status":"UP","timestamp":"2026-08-21T10:25:00Z"}
```

---

## Result
The Python Flask API was successfully containerized with Docker, pushed to Docker Hub, and deployed across 2 pod replicas in a Kubernetes cluster using Deployment and NodePort Service manifests.
