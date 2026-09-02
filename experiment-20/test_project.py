"""
Unit and Integration Tests for Experiment 20 Modular Platform
"""
import pytest
from user_auth import UserAuthService
from order_processor import OrderProcessor
from notification_service import NotificationService
from analytics_service import AnalyticsService

def test_user_auth():
    auth = UserAuthService()
    assert auth.register("alice", "Password123!") is True
    assert auth.register("alice", "DuplicatePass") is False
    assert auth.login("alice", "Password123!") is True
    assert auth.login("alice", "WrongPass") is False

def test_order_processor():
    processor = OrderProcessor(tax_rate=0.10)
    items = [{"price": 50.0, "quantity": 2}]
    # 100 + 10% = 110
    total = processor.calculate_total(items)
    assert total == 110.0
    order = processor.place_order("ORD-1", "alice", items)
    assert order["status"] == "CONFIRMED"
    assert order["total_amount"] == 110.0

def test_notification_service():
    notifier = NotificationService()
    notif = notifier.send_notification("test@domain.com", "Welcome!")
    assert notif["status"] == "SENT"
    assert notifier.get_notification_count() == 1

def test_analytics_service():
    analytics = AnalyticsService()
    metrics = analytics.track_order(100.0)
    assert metrics["total_orders"] == 1
    assert metrics["total_revenue"] == 100.0
    analytics.track_order(200.0)
    metrics = analytics.get_metrics()
    assert metrics["total_orders"] == 2
    assert metrics["total_revenue"] == 300.0
    assert metrics["average_order_value"] == 150.0
