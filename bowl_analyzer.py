from google import genai
from config import Config
from logger_config import get_logger

class BowlAnalyzer:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.logger.info("Initializing bowl analyzer")
        
        try:
            self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
            self.logger.info("Gemini API client initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini API client: {e}", exc_info=True)
            raise
    
    def analyze_bowl_status(self, image_bytes):
        self.logger.debug(f"Starting bowl analysis for image of size: {len(image_bytes)} bytes")
        
        prompt = """
        Analyze this image of a pet food bowl and determine its status.
        Respond with only one of these exact words:
        - EMPTY: if the bowl is completely empty or has only tiny crumbs
        - PARTIAL: if the bowl has some food but is not full
        - FULL: if the bowl is completely full or nearly full
        
        Look carefully at the bowl contents and be precise in your assessment.
        """
        
        try:
            self.logger.debug("Sending request to Gemini API")
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    prompt,
                    genai.types.Part.from_bytes(
                        data=image_bytes, 
                        mime_type="image/jpeg"
                    )
                ]
            )
            
            raw_response = response.text.strip()
            self.logger.debug(f"Raw Gemini response: '{raw_response}'")
            
            status = raw_response.upper()
            
            if status not in ['EMPTY', 'PARTIAL', 'FULL']:
                self.logger.warning(f"Unexpected response from Gemini: '{raw_response}', returning UNKNOWN")
                return 'UNKNOWN'
            
            self.logger.info(f"Bowl analysis completed: {status}")
            return status
            
        except Exception as e:
            self.logger.error(f"Failed to analyze bowl status: {e}", exc_info=True)
            return 'UNKNOWN'