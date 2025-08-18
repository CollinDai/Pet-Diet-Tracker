import smtplib
from email.mime.text import MIMEText
from src.config import SMTP_SERVER, SMTP_PORT, EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER

class NotificationService:
    def send_notification(self, subject, body):
        """
        Sends a notification.
        """
        raise NotImplementedError

class EmailNotificationService(NotificationService):
    def send_notification(self, subject, body):
        """
        Sends an email notification.
        """
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
            print("Email sent successfully.")
        except Exception as e:
            print(f"Error sending email: {e}")

class PushNotificationService(NotificationService):
    def send_notification(self, subject, body):
        """
        Placeholder for sending push notifications.
        """
        print(f"Sending push notification: Subject: {subject}, Body: {body}")
        # In the future, you would implement the logic to send a push notification
        # to your companion app here.
        pass
