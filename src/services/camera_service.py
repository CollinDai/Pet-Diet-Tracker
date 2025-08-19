import logging
from typing import Tuple, Optional
import numpy as np

logger = logging.getLogger(__name__)

try:
    from picamera2 import Picamera2
    IS_RASPBERRY_PI = True
    logger.info("Picamera2 imported successfully")
except ImportError as e:
    IS_RASPBERRY_PI = False
    logger.error(f"Failed to import picamera2: {e}")

class CameraService:
    def __init__(self, camera_index: int = 0, width: int = 640, height: int = 480):
        if not IS_RASPBERRY_PI:
            raise RuntimeError("Picamera2 is not available. This service only works on a Raspberry Pi.")
        
        self.picam2: Optional[Picamera2] = None
        self.is_started = False
        self.frame: Optional[np.ndarray] = None
        
        try:
            self.picam2 = Picamera2()
            config = self.picam2.create_preview_configuration(
                main={"format": 'RGB888', "size": (width, height)}
            )
            self.picam2.configure(config)
            self.picam2.start()
            self.is_started = True
            logger.info(f"Camera initialized successfully with resolution {width}x{height}")
        except Exception as e:
            logger.error(f"Failed to initialize camera: {e}")
            self.is_started = False
            raise RuntimeError(f"Failed to initialize camera: {e}")

    def isOpened(self) -> bool:
        return self.is_started and self.picam2 is not None

    def read(self) -> Tuple[bool, Optional[np.ndarray]]:
        if not self.isOpened():
            logger.warning("Camera is not opened")
            return False, None
        
        try:
            # Capture a frame
            self.frame = self.picam2.capture_array()
            
            # Picamera2 captures in RGB format, but OpenCV uses BGR.
            # If you need to use OpenCV functions for processing, you might need to convert the color space.
            # For now, we assume the rest of the application can handle RGB.
            # frame_bgr = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
            
            return True, self.frame
        except Exception as e:
            logger.error(f"Failed to capture frame: {e}")
            return False, None

    def release(self) -> None:
        if self.isOpened() and self.picam2 is not None:
            try:
                self.picam2.stop()
                self.is_started = False
                logger.info("Camera released successfully")
            except Exception as e:
                logger.error(f"Error releasing camera: {e}")

    def __del__(self) -> None:
        try:
            if hasattr(self, 'is_started'):
                self.release()
        except:
            pass  # Ignore errors during cleanup
