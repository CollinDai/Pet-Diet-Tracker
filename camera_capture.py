from picamera2 import Picamera2
from PIL import Image
import io

class CameraCapture:
    def __init__(self):
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_still_configuration())
        
    def capture_image(self):
        self.camera.start()
        try:
            image_data = self.camera.capture_array()
            image = Image.fromarray(image_data)
            return image
        finally:
            self.camera.stop()
    
    def capture_to_bytes(self):
        image = self.capture_image()
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        return buffer.getvalue()