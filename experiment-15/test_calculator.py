import pytest
from calculator import add, subtract, calculate_discount

def test_add():
    assert add(10, 5) == 15
    assert add(-3, 3) == 0

def test_subtract():
    assert subtract(20, 8) == 12

def test_calculate_discount():
    assert calculate_discount(100.0, 0.2) == 80.0
