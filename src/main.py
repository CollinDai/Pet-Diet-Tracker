import logging
from dotenv import load_dotenv

from src.services.camera_service import CameraService
from src.services.event_history_service import EventHistoryService
from src.services.notification_service import NotificationService
from src.services.monitoring_service import MonitoringService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def main_loop(camera, monitoring_service: MonitoringService) -> None:
    """
    Main loop to run the pet food consumption monitor.
    """
    if not camera.isOpened():
        logger.error("Camera is not opened or failed to initialize")
        return

    logger.info("Starting monitoring loop...")
    
    while True:
        result = monitoring_service.run_monitoring_cycle(camera)
        
        if result.error:
            logger.error(f"Monitoring cycle error: {result.error}")
            if not result.frame_captured:
                break
        
        # For testing, we'll just run for a few frames
        if isinstance(camera, object) and camera.__class__.__name__ == "MockCamera":
            if hasattr(camera, 'frame_index') and hasattr(camera, 'frames'):
                if camera.frame_index >= len(camera.frames):
                    break

    # When everything done, release the capture
    camera.release()

def main() -> None:
    """
    Main function to run the pet food consumption monitor.
    """
    try:
        camera = CameraService()
        notification_service = NotificationService()
        event_history_service = EventHistoryService()
        monitoring_service = MonitoringService(notification_service, event_history_service)
        
        logger.info("Starting pet food consumption monitor...")
        main_loop(camera, monitoring_service)
        
    except RuntimeError as e:
        logger.error(f"Camera initialization failed: {e}")
        logger.info("Make sure you're running on a Raspberry Pi with camera module enabled")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        logger.info("Pet food consumption monitor stopped")


if __name__ == "__main__":
    main()
