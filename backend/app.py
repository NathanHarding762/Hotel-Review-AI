from flask import Flask, request, jsonify
from textblob import TextBlob
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from React frontend

@app.route("/review", methods=["POST"])
def analyze_review():
    data = request.get_json()
    review_text = data.get("review", "")

    if not review_text:
        return jsonify({"error": "No review text provided"}), 400

    # Simple sentiment analysis using TextBlob
    analysis = TextBlob(review_text)
    polarity = analysis.sentiment.polarity  # -1 (negative) to +1 (positive)

    # Map polarity to rating (1-5)
    score = round(((polarity + 1) / 2) * 4 + 1, 1)  # Converts -1..1 -> 1..5

    # Determine sentiment label
    if polarity > 0.2:
        sentiment = "positive"
    elif polarity < -0.2:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return jsonify({
        "score": score,
        "sentiment": sentiment,
        "confidence": 0.9
    })

if __name__ == "__main__":
    app.run(debug=True)
