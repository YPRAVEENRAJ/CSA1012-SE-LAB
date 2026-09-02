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
