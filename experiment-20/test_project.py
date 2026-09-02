"""
Unit and Integration Tests for Experiment 20 Modular Platform
"""
import pytest
from user_auth import UserAuthService
from order_processor import OrderProcessor
from notification_service import NotificationService

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
