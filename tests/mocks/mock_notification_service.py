from src.services.notification_service import NotificationService

class MockNotificationService(NotificationService):
    def __init__(self):
        self.notifications = []

    def send_notification(self, subject, body):
        """
        Mocks sending a notification by storing it in a list.
        """
        print(f"Mock Notification: Subject='{subject}', Body='{body}'")
        self.notifications.append({"subject": subject, "body": body})
