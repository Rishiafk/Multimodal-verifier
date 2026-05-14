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
                model="command-r",
                message=prompt,
                temperature=0.3,
                max_tokens=300
            )
            return response.text
        except cohere.CohereError as e:
            logger.error(f"Cohere API Error: {str(e)}")
            raise RuntimeError("Verification temporarily unavailable.")
        except Exception as e:
            logger.error(f"Unexpected AI Service Error: {str(e)}")
            raise RuntimeError("Unable to generate grounded verification.")
