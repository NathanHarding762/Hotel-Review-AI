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
CORS(app)

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

    # Predict
    result = model.predict(padded_input, verbose=False)[0][0]

    # Map result to sentiment
    if result > 0.8:
        sentiment = "positive"
    elif result < 0.8 and result > 0.35:
        sentiment = "neutral"
    else:
        sentiment = "negative"

    # Scale result to 0-5 rating and convert to native float
    score = float(result * 5)

    return jsonify({
        "score": score,
        "sentiment": sentiment,
        "confidence": 0.9
    })

# ----------------------------
# 4. Run Flask
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
