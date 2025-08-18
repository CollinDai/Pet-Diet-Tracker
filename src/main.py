import cv2
import time
from src.event_detector import EventDetector
from src.services.notification_service import NotificationService
from src.services.event_history_service import EventHistoryService
from src.services.image_analysis_service import GeminiImageAnalysisService
from src.config import CAMERA_INDEX
from dotenv import load_dotenv
from src.services.camera_service import CameraService

load_dotenv()

def main_loop(cap, notification_service: NotificationService, event_history_service: EventHistoryService, last_event=None, last_event_time=0):
    """
    Main loop to run the pet food consumption monitor.
    """
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None, 0

    image_analysis_service = GeminiImageAnalysisService()
    detector = EventDetector(image_analysis_service)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break

        event = detector.detect_events(frame)

        if event and (event != last_event or time.time() - last_event_time > 3600):
            print(f"Event detected: {event}")
            notification_service.send_notification(f"Dog Food Alert: {event}", f"An event has been detected: {event}")
            event_history_service.log_event(event)
            last_event = event
            last_event_time = time.time()

        # Display the resulting frame (optional)
        # cv2.imshow('frame', frame)
        # if cv2.waitKey(1) == ord('q'):
        #     break
        
        # For testing, we'll just run for a few frames
        if isinstance(cap, object) and cap.__class__.__name__ == "MockCamera":
            if cap.frame_index >= len(cap.frames):
                break


    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return last_event, last_event_time

def main():
    """
    Main function to run the pet food consumption monitor.
    """
    cap = CameraService(CAMERA_INDEX)
    notification_service = NotificationService()
    event_history_service = EventHistoryService()
    main_loop(cap, notification_service, event_history_service)


if __name__ == "__main__":
    main()
