"""
Utility functions module for collaborative development showcase.
Experiment 14 - Git Fork & Pull Request Workflow.
"""

def reverse_string(s: str) -> str:
    """Reverses a given string."""
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    return s[::-1]

def is_palindrome(s: str) -> bool:
    """Checks if a string is a palindrome (case and whitespace insensitive)."""
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    clean = "".join(c.lower() for c in s if c.isalnum())
    return clean == clean[::-1]

def word_count(text: str) -> int:
    """Counts the number of words in a text block."""
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    return len(text.strip().split())

def add(a: float, b: float) -> float:
    """Returns the sum of two numbers."""
    return a + b

def multiply(a: float, b: float) -> float:
    """Returns the product of two numbers."""
    return a * b
