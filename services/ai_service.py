import cohere
import logging
from config.settings import Config

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.client = cohere.Client(Config.COHERE_API_KEY)

    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.chat(
                model="command-a-03-2025",
                message=prompt,
                temperature=0.3,
                max_tokens=300
            )
            return response.text
        except Exception as e:
            error_type = e.__class__.__name__
            logger.error(f"AI Generation Error [{error_type}]: {str(e)}")
            
            if "ApiError" in error_type or "Cohere" in error_type:
                raise RuntimeError("Verification temporarily unavailable.")
            else:
                raise RuntimeError("Unable to generate grounded verification.")
