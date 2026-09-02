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
