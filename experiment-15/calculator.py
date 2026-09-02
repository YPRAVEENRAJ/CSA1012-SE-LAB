"""
Collaborative Calculator Module
Experiment 15: Demonstrating Git Branches and Merge Conflict Resolution
"""

def add(a: float, b: float) -> float:
    """Returns the sum of two numbers."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Returns the difference between two numbers."""
    return a - b

def calculate_discount(price: float, discount_rate: float) -> float:
    """Calculates discounted price with negative price validation."""
    if price < 0.0:
        raise ValueError("Price cannot be negative")
    return price - (price * discount_rate)
