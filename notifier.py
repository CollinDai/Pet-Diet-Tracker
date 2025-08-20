from datetime import datetime

class Notifier:
    def __init__(self):
        self.last_status = None
        self.last_notification_time = None
    
    def should_notify(self, current_status):
        if self.last_status != current_status:
            self.last_status = current_status
            return True
        return False
    
    def send_notification(self, status):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        messages = {
            'EMPTY': f"🍽️ Pet bowl is EMPTY! Time to refill. ({timestamp})",
            'PARTIAL': f"🥄 Pet bowl is PARTIALLY full. ({timestamp})",
            'FULL': f"✅ Pet bowl is FULL. ({timestamp})",
            'UNKNOWN': f"❓ Could not determine bowl status. ({timestamp})"
        }
        
        message = messages.get(status, f"Bowl status: {status} ({timestamp})")
        print(message)
        
        return message