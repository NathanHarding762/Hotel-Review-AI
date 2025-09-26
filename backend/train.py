# backend/app.py

import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

# ----------------------------
# 1. Load model & tokenizer once at startup
# ----------------------------
print("Loading model and tokenizer...")
model = tf.keras.models.load_model("hotel_model.h5")
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Parameters used during training
max_length = 300
padding_type = 'post'
trunc_type = 'post'
print("Model and tokenizer loaded!")

# ----------------------------
# 2. Flask setup
# ----------------------------
app = Flask(__name__)
CORS(app, origins=["http://10.200.67.161:8081"])

# ----------------------------
# 3. API endpoint
# ----------------------------
@app.route("/review", methods=["POST"])
def analyze_review():
    data = request.get_json()
    user_review = data.get("review", "")

    if not user_review:
        return jsonify({"error": "No review text provided"}), 400

    # Tokenize + pad
    sequences = tokenizer.texts_to_sequences([user_review])
    padded_input = pad_sequences(sequences, maxlen=max_length,
                                 padding=padding_type, truncating=trunc_type)

    # Predict sentiment
    result = model.predict(padded_input, verbose=False)[0][0]

    # Map result to sentiment
    if result > 0.8:
        sentiment = "positive"
    elif result < 0.8 and result > 0.35:
        sentiment = "neutral"
    else:
        sentiment = "negative"

    # Scale result to 0-5 rating
    score = float(result * 5)

    # ----------------------------
    # Rule-based issue detection
    # ----------------------------
    issues = []
    review_lower = user_review.lower()

    if any(word in review_lower for word in ["dirty", "smelly", "gross", "unclean", "messy", "shabby"]):
        issues.append("Cleanliness")
    if any(word in review_lower for word in ["rude", "unhelpful", "staff"]):
        issues.append("Staff")
    if any(word in review_lower for word in ["expensive", "overpriced", "cost"]):
        issues.append("Price")
    if any(word in review_lower for word in ["food", "breakfast", "dinner", "restaurant"]):
        issues.append("Food")
    if any(word in review_lower for word in ["location", "distance", "far", "close"]):
        issues.append("Location")

    # ----------------------------
    # Construct response message
    # ----------------------------
    if sentiment == "negative":
        if issues:
            response = f"We’re sorry to hear about the {', '.join(issues)}. Your feedback helps us improve."
        else:
            response = "We’re sorry your experience wasn’t great. Your feedback helps us improve."
    elif sentiment == "positive":
        response = "We’re so glad you enjoyed your stay! Thank you for your kind words."
    else:
        response = "Thanks for your feedback. We’ll keep working to improve."

    return jsonify({
        "score": score,
        "sentiment": sentiment,
        "issues": issues,
        "response": response,
    })

# ----------------------------
# 4. Run Flask
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
