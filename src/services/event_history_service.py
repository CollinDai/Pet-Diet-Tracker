import json
from datetime import datetime

class EventHistoryService:
    def __init__(self, log_file='event_log.json'):
        self.log_file = log_file

    def log_event(self, event):
        """Appends an event with a timestamp to the log file."""
        try:
            events = self.get_events()
        except FileNotFoundError:
            events = []
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event
        }
        events.insert(0, log_entry) # Insert at the beginning for chronological order
        
        with open(self.log_file, 'w') as f:
            json.dump(events, f, indent=4)

    def get_events(self):
        """Retrieves all events from the log file."""
        try:
            with open(self.log_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
