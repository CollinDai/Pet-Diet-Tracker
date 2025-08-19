import os
import uuid
from typing import Optional
from PIL import Image

from src.services.image_analysis_service import ImageAnalysisService

class EventDetector:
    def __init__(self, image_analysis_service: ImageAnalysisService, temp_image_dir: str = "temp_images"):
        self.image_analysis_service = image_analysis_service
        self.temp_image_dir = temp_image_dir
        if not os.path.exists(self.temp_image_dir):
            os.makedirs(self.temp_image_dir)

    def detect_events(self, frame) -> Optional[str]:
        """
        Analyzes a single frame to detect events using an image analysis service.
        """
        image_path = self._save_frame_to_disk(frame)
        try:
            description = self.image_analysis_service.analyze_image(image_path)
        finally:
            os.remove(image_path)
        
        return self._description_to_event(description)

    def _save_frame_to_disk(self, frame) -> str:
        """
        Saves a video frame to a temporary image file.
        """
        filename = f"{uuid.uuid4()}.png"
        image_path = os.path.join(self.temp_image_dir, filename)
        img = Image.fromarray(frame)
        img.save(image_path)
        return image_path

    def _description_to_event(self, description: str) -> Optional[str]:
        """
        Converts a text description of the food bowl scene into a specific event.
        """
        description = description.lower()
        if "empty" in description or "all gone" in description:
            return "dog food from the bowl is all gone"
        elif "full" in description or "refilled" in description:
            return "dog food is refilled"
        elif "partially" in description or "some food" in description:
            return "dog has eaten the food but did not finish all"
        else:
            return None
