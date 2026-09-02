"""
Module 3: Notification Service
Team Project - Experiment 20
"""
from datetime import datetime

class NotificationService:
    def __init__(self):
        self.sent_notifications = []

    def send_notification(self, recipient: str, message: str, channel: str = "EMAIL") -> dict:
        if not recipient or not message:
            raise ValueError("Recipient and message cannot be empty")
        
        notification = {
            "recipient": recipient,
            "channel": channel.upper(),
            "message": message,
            "status": "SENT",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        self.sent_notifications.append(notification)
        return notification

    def get_notification_count(self) -> int:
        return len(self.sent_notifications)
