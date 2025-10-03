# backend/app.py

import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import json
import os


# ----------------------------
# 1. Load model & tokenizer once at startup
# ----------------------------
print("Loading model and tokenizer...")
model = tf.keras.models.load_model("hotel_model.h5")
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

max_length = 300
padding_type = 'post'
trunc_type = 'post'
print("Model and tokenizer loaded!")

# ----------------------------
# 2. Flask setup
# ----------------------------
app = Flask(__name__)
CORS(app)

# ----------------------------
# 3. JSON file for storing issues
# ----------------------------
ISSUE_FILE = "issues.json"
if not os.path.exists(ISSUE_FILE):
    with open(ISSUE_FILE, "w") as f:
        json.dump([], f)

def save_issues(review, issues):
    if not issues:
        return
    with open(ISSUE_FILE, "r") as f:
        data = json.load(f)
    data.append({"review": review, "issues": issues})
    with open(ISSUE_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ----------------------------
# 4. POST endpoint: analyze review
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

    if result > 0.8:
        sentiment = "positive"
    elif result < 0.8 and result > 0.35:
        sentiment = "neutral"
    else:
        sentiment = "negative"

    score = float(result * 5)

    # ----------------------------
    # Rule-based issue detection
    # ----------------------------
    issues = []
    review_lower = user_review.lower()

    if any(word in review_lower for word in ["dirty","smelly","gross","unclean","messy","shabby"]):
        issues.append("cleanliness")
    if any(word in review_lower for word in ["rude", "unhelpful", "staff"]):
        issues.append("staff")
    if any(word in review_lower for word in ["expensive", "overpriced", "cost"]):
        issues.append("price")
    if any(word in review_lower for word in ["food", "breakfast", "dinner", "restaurant"]):
        issues.append("food")
    if any(word in review_lower for word in ["location", "distance", "far", "close"]):
        issues.append("location")

    save_issues(user_review, issues)

    # Response message
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
# 5. GET endpoint: view all stored issues
# ----------------------------
@app.route("/issues", methods=["GET"])
def get_issues():
    with open(ISSUE_FILE, "r") as f:
        data = json.load(f)
    return jsonify(data)

# ----------------------------
# 6. Run Flask
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
