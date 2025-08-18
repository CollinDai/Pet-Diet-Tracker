from abc import ABC, abstractmethod
from google import genai
from PIL import Image


class ImageAnalysisService(ABC):
    """
    Abstract base class for an image analysis service.
    """
    @abstractmethod
    def analyze_image(self, image_path: str) -> str:
        """
        Analyzes an image and returns a description of the scene.
        This method should be implemented by concrete classes.
        """
        raise NotImplementedError

import os

class GeminiImageAnalysisService(ImageAnalysisService):
    """
    An implementation of ImageAnalysisService that uses the Google Gemini API.
    """
    def __init__(self):
        """
        Initializes the Gemini Image Analysis Service.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        self.client = genai.Client(api_key=api_key)

    def analyze_image(self, image_path: str) -> str:
        """
        Analyzes an image using the Gemini API and returns a description.
        """
        try:
            img = Image.open(image_path)
            prompt = "Describe the state of the stainless steel pet food bowl in the image. Is it full, empty, or partially eaten?"
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt, img]
            )
            return response.text
        except Exception as e:
            print(f"Error analyzing image with Gemini API: {e}")
            return "Could not analyze image."