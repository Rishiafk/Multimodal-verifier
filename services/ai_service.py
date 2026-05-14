import cohere
from config.settings import Config

class AIService:
    def __init__(self):
        self.client = cohere.Client(Config.COHERE_API_KEY)

    def generate_response(self, prompt: str) -> str:
        response = self.client.chat(
            model="command-r",
            message=prompt,
            temperature=0.3,
            max_tokens=300
        )
        return response.text
