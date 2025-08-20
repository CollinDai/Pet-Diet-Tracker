import json
import os
from datetime import datetime
from logger_config import get_logger

class MonitorHistory:
    def __init__(self, log_file="monitoring_events.json"):
        self.logger = get_logger(__name__)
        self.log_file = log_file
        self.logger.info(f"Initializing monitor history with log file: {log_file}")
        
    def record_check(self, status, error=None, notification_sent=False):
        self.logger.debug(f"Recording check event: status={status}, error={error is not None}, notification_sent={notification_sent}")
        
        event = {
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "notification_sent": notification_sent,
            "error": str(error) if error else None
        }
        
        try:
            events = []
            if os.path.exists(self.log_file):
                try:
                    with open(self.log_file, 'r') as f:
                        events = json.load(f)
                    self.logger.debug(f"Loaded {len(events)} existing events from {self.log_file}")
                except (json.JSONDecodeError, FileNotFoundError) as e:
                    self.logger.warning(f"Could not load existing events: {e}, starting fresh")
                    events = []
            
            events.append(event)
            
            with open(self.log_file, 'w') as f:
                json.dump(events, f, indent=2)
            
            self.logger.debug(f"Event recorded successfully to {self.log_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to record check event: {e}", exc_info=True)