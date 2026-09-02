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
    """Calculates discounted price with discount rate range validation."""
    if not 0.0 <= discount_rate <= 1.0:
        raise ValueError("Discount rate must be between 0.0 and 1.0")
    return round(price * (1 - discount_rate), 2)
