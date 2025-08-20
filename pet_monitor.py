import time
from camera_capture import CameraCapture
from bowl_analyzer import BowlAnalyzer
from notifier import Notifier

class PetMonitor:
    def __init__(self, check_interval=300):
        self.camera = CameraCapture()
        self.analyzer = BowlAnalyzer()
        self.notifier = Notifier()
        self.check_interval = check_interval
        
    def check_bowl_status(self):
        try:
            image_bytes = self.camera.capture_to_bytes()
            status = self.analyzer.analyze_bowl_status(image_bytes)
            
            if self.notifier.should_notify(status):
                self.notifier.send_notification(status)
            
            return status
            
        except Exception as e:
            print(f"Error checking bowl status: {e}")
            return None
    
    def start_monitoring(self):
        print("Starting pet food bowl monitoring...")
        print(f"Checking every {self.check_interval} seconds")
        
        while True:
            try:
                status = self.check_bowl_status()
                if status:
                    print(f"Current bowl status: {status}")
                
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                print("\nMonitoring stopped by user")
                break
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(60)