class ParserService:
    @staticmethod
    def parse_verdict_response(answer: str) -> tuple:
        """
        Parses the model's text response and extracts the verdict, explanation, and color.
        Returns a tuple: (result, explanation, color)
        """
        if "Verdict:" in answer and "Explanation:" in answer:
            verdict_line = [line for line in answer.split("\n") if "Verdict:" in line][0]
            explanation_line = [line for line in answer.split("\n") if "Explanation:" in line][0]

            result = verdict_line.replace("Verdict:", "").strip()
            explanation = explanation_line.replace("Explanation:", "").strip()

            if "Supported" in result:
                color = "supported"
            elif "Partially" in result:
                color = "partially-supported"
            else:
                color = "not-supported"
            
            return result, explanation, color
        else:
            return "Error", "Unable to parse the model response.", "error"
