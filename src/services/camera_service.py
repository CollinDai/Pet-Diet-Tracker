import time
import cv2

try:
    from picamera2 import Picamera2
    IS_RASPBERRY_PI = True
except ImportError:
    IS_RASPBERRY_PI = False

class CameraService:
    def __init__(self, camera_index=0):
        if not IS_RASPBERRY_PI:
            raise RuntimeError("Picamera2 is not available. This service only works on a Raspberry Pi.")
        
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
        self.picam2.start()
        self.frame = None

    def isOpened(self):
        return self.picam2.started

    def read(self):
        if not self.isOpened():
            return False, None
        
        # Capture a frame
        self.frame = self.picam2.capture_array()
        
        # Picamera2 captures in RGB format, but OpenCV uses BGR.
        # If you need to use OpenCV functions for processing, you might need to convert the color space.
        # For now, we assume the rest of the application can handle RGB.
        # frame_bgr = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
        
        return True, self.frame

    def release(self):
        if self.isOpened():
            self.picam2.stop()

    def __del__(self):
        self.release()
