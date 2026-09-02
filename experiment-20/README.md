# Experiment 20: Team Project Version Control & Collaborative Workflow

## 📖 Project Overview
This project showcases an enterprise-style **Git & GitHub Version Control Workflow** for a multi-module team software engineering project.

## 🏗️ Architecture & Modules
The platform implements a modular e-commerce architecture divided across team branches:
1. **`user_auth.py`** (`module/auth` branch): User registration, password hashing (SHA-256), and login authentication.
2. **`order_processor.py`** (`module/order-processing` branch): Shopping cart calculation, tax calculation, and order placement.
3. **`notification_service.py`** (`module/notifications` branch): Real-time dispatching and audit logging of transaction notifications.
4. **`main.py`**: Core integration orchestrating all micro-modules.
5. **`test_project.py`**: Automated test suite ensuring quality gates prior to Pull Request merging.

## 🔄 Team Workflow & Version Control Standard
1. **Branching Model**: Trunk-based development with short-lived feature branches (`module/<feature-name>`).
2. **Code Reviews**: Every pull request requires review approval before merging into `main`.
3. **Continuous Integration**: Pytest test suite runs automatically before merge commits are accepted.
4. **Conflict Resolution**: Fast-forward or 3-way manual conflict resolution locally before concluding PR merge.

## 🚀 Running the Project Locally
```bash
# Run unit tests
pytest test_project.py -v

# Run the integrated system
python main.py
```
