"""
Module 2: Order Processing Service
Team Project - Experiment 20
"""
from typing import List, Dict

class OrderProcessor:
    def __init__(self, tax_rate: float = 0.08):
        self.tax_rate = tax_rate
        self.orders = []

    def calculate_total(self, items: List[Dict[str, float]]) -> float:
        if not items:
            return 0.0
        subtotal = sum(item.get("price", 0.0) * item.get("quantity", 1) for item in items)
        tax = subtotal * self.tax_rate
        return round(subtotal + tax, 2)

    def place_order(self, order_id: str, customer: str, items: List[Dict[str, float]]) -> Dict:
        if not items:
            raise ValueError("Cannot place an order with zero items")
        total = self.calculate_total(items)
        order = {
            "order_id": order_id,
            "customer": customer,
            "items_count": len(items),
            "total_amount": total,
            "status": "CONFIRMED"
        }
        self.orders.append(order)
        return order
