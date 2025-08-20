import os
from dotenv import load_dotenv
import logging

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    if not GEMINI_API_KEY:
        logging.error("GEMINI_API_KEY environment variable is not set")
        raise ValueError("GEMINI_API_KEY environment variable is required")
    
    logging.info("Configuration loaded successfully")