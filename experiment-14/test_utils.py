"""
Unit tests for utils module.
Used to verify code quality before submitting Pull Request.
"""
import pytest
from utils import reverse_string, is_palindrome, word_count, add, multiply

def test_reverse_string():
    assert reverse_string("devops") == "spoved"
    assert reverse_string("") == ""
    with pytest.raises(TypeError):
        reverse_string(12345)

def test_is_palindrome():
    assert is_palindrome("Racecar") is True
    assert is_palindrome("A man a plan a canal Panama") is True
    assert is_palindrome("hello") is False

def test_word_count():
    assert word_count("Collaborative Git Workflow with Pull Requests") == 6
    assert word_count("   ") == 0

def test_math_operations():
    assert add(10, 25) == 35
    assert multiply(6, 7) == 42
