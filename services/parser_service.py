import json
import logging

logger = logging.getLogger(__name__)

class ParserService:
    @staticmethod
    def parse_verdict_response(answer: str) -> tuple:
        """
        Parses the model's JSON response and extracts the verdict, explanation, and color.
        Returns a tuple: (result, explanation, color)
        """
        try:
            # Clean up potential markdown formatting around JSON
            clean_answer = answer.strip()
            if clean_answer.startswith("```json"):
                clean_answer = clean_answer[7:]
            elif clean_answer.startswith("```"):
                clean_answer = clean_answer[3:]
            if clean_answer.endswith("```"):
                clean_answer = clean_answer[:-3]
            clean_answer = clean_answer.strip()
            
            data = json.loads(clean_answer)
            
            result = data.get("verdict", "Error")
            explanation = data.get("explanation", "No explanation provided.")
            confidence = data.get("confidence", 0.0)

            if "Supported" in result and "Partially" not in result and "Not" not in result:
                color = "supported"
            elif "Partially" in result:
                color = "partially-supported"
            elif "Not Supported" in result:
                color = "not-supported"
            else:
                color = "error"
                if result == "Error":
                    explanation = "Invalid verdict returned."
            
            return result, explanation, color
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode Error in model response: {str(e)}")
            return "Error", "Unable to parse the model response as JSON.", "error"
        except Exception as e:
            logger.error(f"Unexpected parsing error: {str(e)}")
            return "Error", "Unable to generate grounded verification.", "error"
