"""
Module 1: User Authentication Service
Team Project - Experiment 20
"""
import hashlib

class UserAuthService:
    def __init__(self):
        # In-memory user database: username -> hashed_password
        self._users = {}

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def register(self, username: str, password: str) -> bool:
        if not username or not password:
            raise ValueError("Username and password cannot be empty")
        if username in self._users:
            return False
        self._users[username] = self._hash_password(password)
        return True

    def login(self, username: str, password: str) -> bool:
        if username not in self._users:
            return False
        return self._users[username] == self._hash_password(password)

    def user_exists(self, username: str) -> bool:
        return username in self._users
