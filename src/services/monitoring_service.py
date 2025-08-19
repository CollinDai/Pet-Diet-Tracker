import time
import logging
from typing import Optional, Tuple
from dataclasses import dataclass

from src.event_detector import EventDetector
from src.services.image_analysis_service import GeminiImageAnalysisService
from src.services.notification_service import NotificationService
from src.services.event_history_service import EventHistoryService

logger = logging.getLogger(__name__)

@dataclass
class MonitoringResult:
    """Result of a single monitoring cycle."""
    event_detected: Optional[str]
    frame_captured: bool
    timestamp: float
    error: Optional[str] = None

class MonitoringService:
    """Service that handles the core pet food monitoring flow."""
    
    def __init__(
        self,
        notification_service: NotificationService,
        event_history_service: EventHistoryService,
        debounce_time: float = 3600  # 1 hour in seconds
    ):
        self.notification_service = notification_service
        self.event_history_service = event_history_service
        self.debounce_time = debounce_time
        self.image_analysis_service = GeminiImageAnalysisService()
        self.detector = EventDetector(self.image_analysis_service)
        self.last_event: Optional[str] = None
        self.last_event_time: float = 0
    
    def run_monitoring_cycle(self, camera) -> MonitoringResult:
        """
        Run a single monitoring cycle: capture -> analyze -> detect -> handle event.
        
        Args:
            camera: Camera object with read() method that returns (ret, frame)
            
        Returns:
            MonitoringResult with details of what happened during this cycle
        """
        timestamp = time.time()
        
        # Capture frame
        ret, frame = camera.read()
        if not ret or frame is None:
            error_msg = "Failed to capture frame from camera"
            logger.error(error_msg)
            return MonitoringResult(
                event_detected=None,
                frame_captured=False,
                timestamp=timestamp,
                error=error_msg
            )
        
        # Detect events
        try:
            event = self.detector.detect_events(frame)
        except Exception as e:
            error_msg = f"Failed to detect events: {e}"
            logger.error(error_msg)
            return MonitoringResult(
                event_detected=None,
                frame_captured=True,
                timestamp=timestamp,
                error=error_msg
            )
        
        # Handle event if detected and not debounced
        if event and self._should_handle_event(event, timestamp):
            try:
                self._handle_event(event)
                self.last_event = event
                self.last_event_time = timestamp
                logger.info(f"Event detected and handled: {event}")
            except Exception as e:
                error_msg = f"Failed to handle event: {e}"
                logger.error(error_msg)
                return MonitoringResult(
                    event_detected=event,
                    frame_captured=True,
                    timestamp=timestamp,
                    error=error_msg
                )
        
        return MonitoringResult(
            event_detected=event,
            frame_captured=True,
            timestamp=timestamp
        )
    
    def _should_handle_event(self, event: str, timestamp: float) -> bool:
        """Check if event should be handled based on debouncing logic."""
        return (
            event != self.last_event or 
            timestamp - self.last_event_time > self.debounce_time
        )
    
    def _handle_event(self, event: str) -> None:
        """Handle a detected event by sending notification and logging."""
        self.notification_service.send_notification(
            f"Dog Food Alert: {event}", 
            f"An event has been detected: {event}"
        )
        self.event_history_service.log_event(event)