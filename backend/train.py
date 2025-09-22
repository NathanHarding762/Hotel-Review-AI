import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# ----------------------------
# 1. Load dataset
# ----------------------------
_URL = 'https://codehs.com/uploads/279b78388d2b10e580abee0346148472'
zip_dir = tf.keras.utils.get_file('reviews.csv', origin=_URL, extract=True)

zip_dir_base = os.path.dirname(zip_dir)
data_path = os.path.join(zip_dir_base, 'reviews.csv')

dataset = pd.read_csv(data_path)

# Expect dataset columns: "text" (review) and "sediment" (label 0/1)
sentences = dataset['text'].tolist()
labels = dataset['sediment'].tolist()

# Ensure all reviews are strings
sentences = [str(s) for s in sentences]

# Split train/test
training_size = int(len(sentences) * 0.8)

training_sentences = sentences[0:training_size]
testing_sentences = sentences[training_size:]
training_labels = labels[0:training_size]
testing_labels = labels[training_size:]

training_labels_final = np.array(training_labels)
testing_labels_final = np.array(testing_labels)

print("Training Size:", len(training_sentences))
print("Testing Size:", len(testing_sentences))

# ----------------------------
# 2. Tokenizer
# ----------------------------
vocab_size = 10000
max_length = 300
padding_type = 'post'
trunc_type = 'post'

tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
tokenizer.fit_on_texts(training_sentences)

# Save tokenizer
with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

# Convert text to padded sequences
train_sequences = tokenizer.texts_to_sequences(training_sentences)
train_padded = pad_sequences(train_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

test_sequences = tokenizer.texts_to_sequences(testing_sentences)
test_padded = pad_sequences(test_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

# ----------------------------
# 3. Model
# ----------------------------
embedding_dim = 64
num_epochs = 10

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(6, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

print("Training model...")
model.fit(train_padded, training_labels_final, epochs=num_epochs,
          validation_data=(test_padded, testing_labels_final))

# Save model
model.save("hotel_model.h5")
print("✅ Model and tokenizer saved!")
