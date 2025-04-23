from transformers import TFAutoModelForSequenceClassification, AutoTokenizer
import tensorflow as tf
import numpy as np

# Load pre-trained model and tokenizer
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = TFAutoModelForSequenceClassification.from_pretrained(model_name)

# Define sentiment labels
labels = ["Negative", "Positive"]


def analyze_sentiment(text):
    # Tokenize input
    inputs = tokenizer(text, return_tensors="tf", truncation=True, padding=True)

    # Run the model
    outputs = model(**inputs)
    logits = outputs.logits

    # Convert logits to probabilities
    probs = tf.nn.softmax(logits, axis=-1)
    predicted_class = np.argmax(probs, axis=1).item()
    confidence = probs[0][predicted_class].numpy()

    return labels[predicted_class], confidence


if __name__ == "__main__":
    user_input = input("Enter a sentence for sentiment analysis: ")
    sentiment, confidence = analyze_sentiment(user_input)

    print(f"\nSentiment: {sentiment}")
    print(f"Confidence: {confidence:.2f}")
