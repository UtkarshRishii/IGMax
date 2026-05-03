import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
    SLIDES_DIR = os.path.join(OUTPUT_DIR, "slides")
    
    # Ensure output directories exist
    os.makedirs(SLIDES_DIR, exist_ok=True)

config = Config()
