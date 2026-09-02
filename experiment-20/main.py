"""
Core Integration Application
Team Project - Experiment 20
Orchestrates UserAuthService, OrderProcessor, and NotificationService.
"""
from user_auth import UserAuthService
from order_processor import OrderProcessor
from notification_service import NotificationService

def run_e_commerce_flow():
    print("=== Initiating Collaborative E-Commerce Platform ===")
    
    # 1. User Registration & Auth
    auth = UserAuthService()
    auth.register("student_dev", "SecurePass@2026")
    is_authenticated = auth.login("student_dev", "SecurePass@2026")
    print(f"[Auth] User 'student_dev' authenticated: {is_authenticated}")

    # 2. Order Processing
    processor = OrderProcessor(tax_rate=0.08)
    cart = [
        {"name": "DevOps Handbook", "price": 40.0, "quantity": 1},
        {"name": "Cloud Computing Guide", "price": 25.0, "quantity": 2}
    ]
    order = processor.place_order("ORD-90210", "student_dev", cart)
    print(f"[Order] Placed: {order['order_id']} | Total: ${order['total_amount']}")

    # 3. Notification Dispatch
    notifier = NotificationService()
    notif = notifier.send_notification(
        "student_dev@university.edu",
        f"Order {order['order_id']} confirmed for ${order['total_amount']}.",
        channel="EMAIL"
    )
    print(f"[Notification] Dispatched via {notif['channel']} to {notif['recipient']}")
    print("=== Flow Completed Successfully ===")

if __name__ == '__main__':
    run_e_commerce_flow()
