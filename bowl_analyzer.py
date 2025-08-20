from google import genai
from config import Config

class BowlAnalyzer:
    def __init__(self):
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
    
    def analyze_bowl_status(self, image_bytes):
        prompt = """
        Analyze this image of a pet food bowl and determine its status.
        Respond with only one of these exact words:
        - EMPTY: if the bowl is completely empty or has only tiny crumbs
        - PARTIAL: if the bowl has some food but is not full
        - FULL: if the bowl is completely full or nearly full
        
        Look carefully at the bowl contents and be precise in your assessment.
        """
        
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                prompt,
                {"mime_type": "image/jpeg", "data": image_bytes}
            ]
        )
        
        status = response.text.strip().upper()
        
        if status not in ['EMPTY', 'PARTIAL', 'FULL']:
            return 'UNKNOWN'
        
        return status