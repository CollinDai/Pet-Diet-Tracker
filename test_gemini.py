import argparse
import os
from src.services.image_analysis_service import GeminiImageAnalysisService
from dotenv import load_dotenv

load_dotenv()

def test_image_analysis(image_path: str):
    """
    Tests the GeminiImageAnalysisService with a single image.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image path does not exist: {image_path}")
        return

    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is not set.")
        return

    print("Initializing Gemini Image Analysis Service...")
    analysis_service = GeminiImageAnalysisService()
    
    print(f"Analyzing image: {image_path}")
    description = analysis_service.analyze_image(image_path)
    
    print("\n--- Analysis Result ---")
    print(description)
    print("-----------------------\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the Gemini Image Analysis Service.")
    parser.add_argument("image_path", type=str, help="The absolute or relative path to the image file.")
    args = parser.parse_args()
    
    test_image_analysis(args.image_path)
