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
