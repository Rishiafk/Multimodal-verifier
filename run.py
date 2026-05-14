from flask import Flask, render_template, request
from config.settings import Config
from services.ai_service import AIService
from services.verification_service import VerificationService

app = Flask(__name__)
app.config.from_object(Config)

ai_service = AIService()
verification_service = VerificationService(ai_service)
@app.route("/", methods=["GET", "POST"])
def index():
    result = explanation = color = None

    if request.method == "POST":
        claim = request.form["claim"]
        evidence = request.form["evidence"]
        
        result, explanation, color = verification_service.verify_claim(claim, evidence)

    return render_template("index.html", result=result, explanation=explanation, color=color)

if __name__ == "__main__":
    app.run(debug=True)
