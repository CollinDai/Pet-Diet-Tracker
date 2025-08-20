import time
from camera_capture import CameraCapture
from bowl_analyzer import BowlAnalyzer
from notifier import Notifier
from monitor_history import MonitorHistory
from logger_config import get_logger

class PetMonitor:
    def __init__(self, check_interval=300, log_file="monitoring_events.json"):
        self.logger = get_logger(__name__)
        self.logger.info(f"Initializing PetMonitor with check_interval={check_interval}s")
        
        self.camera = CameraCapture()
        self.analyzer = BowlAnalyzer()
        self.notifier = Notifier()
        self.history = MonitorHistory(log_file)
        self.check_interval = check_interval
        
        self.logger.info("PetMonitor initialization completed")
        
    def check_bowl_status(self):
        self.logger.debug("Starting bowl status check")
        image_path = None
        try:
            self.logger.debug("Capturing and saving image from camera")
            image_bytes, image_path = self.camera.capture_and_save()
            self.logger.debug(f"Image captured and saved, size: {len(image_bytes)} bytes, path: {image_path}")
            
            self.logger.debug("Analyzing bowl status with AI")
            status = self.analyzer.analyze_bowl_status(image_bytes)
            self.logger.info(f"Bowl status analyzed: {status}")
            
            notification_sent = False
            if self.notifier.should_notify(status):
                self.logger.info(f"Status changed, sending notification for: {status}")
                self.notifier.send_notification(status)
                notification_sent = True
            else:
                self.logger.debug(f"No notification needed, status unchanged: {status}")
            
            self.history.record_check(status, notification_sent=notification_sent, image_path=image_path)
            self.logger.debug("Bowl status check completed successfully")
            return status
            
        except Exception as e:
            self.logger.error(f"Error checking bowl status: {e}", exc_info=True)
            self.history.record_check(None, error=e, image_path=image_path)
            return None
    
    def start_monitoring(self):
        self.logger.info("Starting pet food bowl monitoring")
        self.logger.info(f"Monitoring interval: {self.check_interval} seconds")
        
        while True:
            try:
                status = self.check_bowl_status()
                if status:
                    self.logger.info(f"Current bowl status: {status}")
                
                self.logger.debug(f"Sleeping for {self.check_interval} seconds")
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                self.logger.info("Monitoring stopped by user (KeyboardInterrupt)")
                break
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}", exc_info=True)
                self.logger.info("Waiting 60 seconds before retry")
                time.sleep(60)