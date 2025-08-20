from datetime import datetime
from logger_config import get_logger

class Notifier:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.logger.info("Initializing notifier")
        
        self.last_status = None
        self.last_notification_time = None
        
        self.logger.debug("Notifier initialization completed")
    
    def should_notify(self, current_status):
        self.logger.debug(f"Checking if notification needed: current={current_status}, last={self.last_status}")
        
        if self.last_status != current_status:
            self.logger.info(f"Status changed from {self.last_status} to {current_status}, notification needed")
            self.last_status = current_status
            return True
        
        self.logger.debug("No status change, notification not needed")
        return False
    
    def send_notification(self, status):
        self.logger.debug(f"Preparing notification for status: {status}")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        messages = {
            'EMPTY': f"🍽️ Pet bowl is EMPTY! Time to refill. ({timestamp})",
            'PARTIAL': f"🥄 Pet bowl is PARTIALLY full. ({timestamp})",
            'FULL': f"✅ Pet bowl is FULL. ({timestamp})",
            'UNKNOWN': f"❓ Could not determine bowl status. ({timestamp})"
        }
        
        message = messages.get(status, f"Bowl status: {status} ({timestamp})")
        self.logger.info(f"Sending notification: {message}")
        
        try:
            print(message)
            self.last_notification_time = timestamp
            self.logger.debug(f"Notification sent successfully at {timestamp}")
            return message
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}", exc_info=True)
            return None