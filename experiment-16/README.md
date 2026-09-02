# Experiment 16: Static Website & Nginx Docker Containerization

## Overview
This experiment contains a static web application built using HTML5, CSS3, and JavaScript, containerized with an Nginx base image on Docker.

## Project Structure
- `index.html`: Main HTML5 website structure.
- `styles.css`: Glassmorphic styling, custom typography, dark & cyberpunk themes.
- `script.js`: Interactive elements, theme toggle, and server ping toast simulation.
- `Dockerfile`: Nginx configuration for building the Docker container image.
- `.dockerignore`: Exclusion list for Docker build context.

## How to Run

### 1. Build Docker Image
```bash
cd experiment-16
docker build -t static-web-app .
```

### 2. Run Docker Container
```bash
docker run -d -p 8080:80 --name my-static-website static-web-app
```

### 3. Access in Browser
Navigate to `http://localhost:8080`
