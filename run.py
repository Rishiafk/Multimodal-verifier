from flask import Flask, render_template, request
from config.settings import Config
from services.ai_service import AIService

app = Flask(__name__)
app.config.from_object(Config)
ai_service = AIService()

@app.route("/", methods=["GET", "POST"])
def index():
    result = explanation = color = None

    if request.method == "POST":
        claim = request.form["claim"]
        evidence = request.form["evidence"]

        prompt = f"""
        Given the following claim and a related evidence, determine whether the claim is:
        - Supported
        - Partially Supported
        - Not Supported

        Then provide a short explanation.

        Claim: "{claim}"
        Evidence: "{evidence}"

        Provide a response in this format:
        Verdict: <Supported/Partially Supported/Not Supported>
        Explanation: <brief explanation>
        """

        try:
            answer = ai_service.generate_response(prompt)

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
            else:
                result = "Error"
                explanation = "Unable to parse the model response."
                color = "error"

        except Exception as e:
            result = "Error"
            explanation = f"Something went wrong: {str(e)}"
            color = "error"

    return render_template("index.html", result=result, explanation=explanation, color=color)

if __name__ == "__main__":
    app.run(debug=True)
