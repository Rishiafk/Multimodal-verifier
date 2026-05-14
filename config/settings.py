import os
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()

class Config:
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
