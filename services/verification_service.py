from services.ai_service import AIService
from services.parser_service import ParserService

class VerificationService:
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
        self.parser_service = ParserService()

    def verify_claim(self, claim: str, evidence: str) -> tuple:
        """
        Takes a claim and evidence, queries the AI, and parses the response.
        Returns a tuple: (result, explanation, color)
        """
        prompt = f"""
        Given the following claim and a related evidence, determine whether the claim is:
        - Supported
        - Partially Supported
        - Not Supported

        Then provide a short explanation.

        Claim: "{claim}"
        Evidence: "{evidence}"

        Provide a response in valid JSON format with the following keys:
        - "verdict": <"Supported" | "Partially Supported" | "Not Supported">
        - "explanation": <brief explanation>
        - "confidence": <float between 0.0 and 1.0>
        
        Ensure your entire response is just the JSON object and nothing else.
        """

        try:
            answer = self.ai_service.generate_response(prompt)
            return self.parser_service.parse_verdict_response(answer)
        except Exception as e:
            return "Error", f"Something went wrong: {str(e)}", "error"
