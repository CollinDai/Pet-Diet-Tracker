import time
import logging
from typing import Optional, Tuple, Any
from dotenv import load_dotenv

from src.event_detector import EventDetector
from src.services.camera_service import CameraService
from src.services.event_history_service import EventHistoryService
from src.services.image_analysis_service import GeminiImageAnalysisService
from src.services.notification_service import NotificationService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def main_loop(
    cap: Any, 
    notification_service: NotificationService, 
    event_history_service: EventHistoryService, 
    last_event: Optional[str] = None, 
    last_event_time: float = 0
) -> Tuple[Optional[str], float]:
    """
    Main loop to run the pet food consumption monitor.
    """
    if not cap.isOpened():
        logger.error("Camera is not opened or failed to initialize")
        return None, 0

    image_analysis_service = GeminiImageAnalysisService()
    detector = EventDetector(image_analysis_service)

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            logger.error("Failed to capture frame from camera")
            break

        event = detector.detect_events(frame)

        if event and (event != last_event or time.time() - last_event_time > 3600):
            logger.info(f"Event detected: {event}")
            try:
                notification_service.send_notification(f"Dog Food Alert: {event}", f"An event has been detected: {event}")
                event_history_service.log_event(event)
                last_event = event
                last_event_time = time.time()
            except Exception as e:
                logger.error(f"Failed to send notification or log event: {e}")

        # For testing, we'll just run for a few frames
        if isinstance(cap, object) and cap.__class__.__name__ == "MockCamera":
            if hasattr(cap, 'frame_index') and hasattr(cap, 'frames'):
                if cap.frame_index >= len(cap.frames):
                    break


    # When everything done, release the capture
    cap.release()
    return last_event, last_event_time

def main() -> None:
    """
    Main function to run the pet food consumption monitor.
    """
    try:
        cap = CameraService()
        notification_service = NotificationService()
        event_history_service = EventHistoryService()
        
        logger.info("Starting pet food consumption monitor...")
        main_loop(cap, notification_service, event_history_service)
        
    except RuntimeError as e:
        logger.error(f"Camera initialization failed: {e}")
        logger.info("Make sure you're running on a Raspberry Pi with camera module enabled")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        logger.info("Pet food consumption monitor stopped")


if __name__ == "__main__":
    main()
