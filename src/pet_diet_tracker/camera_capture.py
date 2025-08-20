from picamera2 import Picamera2
from PIL import Image
import io
import os
from datetime import datetime
from .logger_config import get_logger

class CameraCapture:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.logger.info("Initializing camera capture")
        
        try:
            self.camera = Picamera2()
            self.camera.configure(self.camera.create_still_configuration())
            self.logger.info("Camera initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize camera: {e}", exc_info=True)
            raise
        
    def capture_image(self):
        self.logger.debug("Starting image capture")
        self.camera.start()
        try:
            image_data = self.camera.capture_array()
            image = Image.fromarray(image_data)
            self.logger.debug(f"Image captured successfully, size: {image.size}")
            return image
        except Exception as e:
            self.logger.error(f"Failed to capture image: {e}", exc_info=True)
            raise
        finally:
            self.camera.stop()
            self.logger.debug("Camera stopped")
    
    def capture_to_bytes(self):
        self.logger.debug("Converting image to bytes")
        try:
            image = self.capture_image()
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG')
            image_bytes = buffer.getvalue()
            self.logger.debug(f"Image converted to bytes, size: {len(image_bytes)} bytes")
            return image_bytes
        except Exception as e:
            self.logger.error(f"Failed to convert image to bytes: {e}", exc_info=True)
            raise
    
    def capture_and_save(self):
        self.logger.debug("Capturing and saving image")
        try:
            image = self.capture_image()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}.jpg"
            filepath = os.path.join("captured_images", filename)
            
            os.makedirs("captured_images", exist_ok=True)
            image.save(filepath, format='JPEG')
            self.logger.debug(f"Image saved to: {filepath}")
            
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG')
            image_bytes = buffer.getvalue()
            
            return image_bytes, filepath
        except Exception as e:
            self.logger.error(f"Failed to capture and save image: {e}", exc_info=True)
            raise