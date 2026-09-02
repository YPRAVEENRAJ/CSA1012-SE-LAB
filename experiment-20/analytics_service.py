"""
Module 4: Business Analytics and Metrics Service
Team Project - Experiment 20
Developed on branch: module/analytics
"""
from typing import Dict

class AnalyticsService:
    def __init__(self):
        self._revenue = 0.0
        self._order_count = 0

    def track_order(self, amount: float) -> Dict[str, float]:
        if amount < 0:
            raise ValueError("Order amount cannot be negative")
        self._revenue += amount
        self._order_count += 1
        return self.get_metrics()

    def get_metrics(self) -> Dict[str, float]:
        avg_order = (self._revenue / self._order_count) if self._order_count > 0 else 0.0
        return {
            "total_orders": self._order_count,
            "total_revenue": round(self._revenue, 2),
            "average_order_value": round(avg_order, 2)
        }
