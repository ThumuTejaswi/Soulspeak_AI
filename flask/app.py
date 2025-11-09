from flask import Flask, render_template, request
from transformers import pipeline
import re
from functools import lru_cache

app = Flask(__name__)

# --- Load Hugging Face emotion detection model with caching ---
@lru_cache(maxsize=1)
def load_pipeline():
    return pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=None
    )

emotion_pipeline = load_pipeline()


# --- Advanced Emotion Detection with manual correction ---
def detect_emotions(feeling_text):
    feeling_text = feeling_text.lower().strip()
    results = emotion_pipeline(feeling_text)
    emotions = {}

    # Flatten model output if nested
    if isinstance(results, list) and len(results) > 0:
        if isinstance(results[0], list):
            results = results[0]
        for item in results:
            emotions[item['label'].lower()] = round(item['score'], 3)

    # --- Manual correction for clear emotional keywords ---
    happy_keywords = ["happy", "excited", "joy", "glad", "delighted", "cheerful"]
    sad_keywords = ["sad", "unhappy", "depressed", "down", "heartbroken"]
    angry_keywords = ["angry", "furious", "mad", "annoyed", "irritated"]
    fear_keywords = ["scared", "afraid", "nervous", "worried", "terrified"]

    for word in happy_keywords:
        if word in feeling_text:
            emotions = {"joy": 1.0}
            break
    for word in sad_keywords:
        if word in feeling_text:
            emotions = {"sadness": 1.0}
            break
    for word in angry_keywords:
        if word in feeling_text:
            emotions = {"anger": 1.0}
            break
    for word in fear_keywords:
        if word in feeling_text:
            emotions = {"fear": 1.0}
            break

    return emotions


# --- Supportive Response based on detected emotion ---
def supportive_response_multi(name, emotions_dict):
    if not emotions_dict:
        return 'neutral', f"{name}, I’m here for you 💖. Tell me more."

    # Pick emotion with highest confidence
    main_emotion = max(emotions_dict, key=emotions_dict.get)
    confidence = emotions_dict[main_emotion]

    if main_emotion == "joy":
        text = f"{name}, you're doing great! 🌸 Keep enjoying this positive energy 💙 (confidence: {confidence})"
    elif main_emotion == "sadness":
        text = f"{name}, it's okay to feel low 💜. Remember, you're not alone. (confidence: {confidence})"
    elif main_emotion == "anger":
        text = f"{name}, I understand your anger 💔. Take a deep breath, you are stronger than this 💙 (confidence: {confidence})"
    elif main_emotion == "fear":
        text = f"{name}, it's natural to feel worried 😔. I'm here with you 💙 (confidence: {confidence})"
    elif main_emotion == "disgust":
        text = f"{name}, I sense your discomfort 😕. Let’s try focusing on something uplifting 💙 (confidence: {confidence})"
    elif main_emotion == "surprise":
        text = f"Wow {name}, that must have been unexpected! 🌟 (confidence: {confidence})"
    else:
        text = f"{name}, I’m here for you 💖. Tell me more. (confidence: {confidence})"

    return main_emotion, text


# --- Flask Routes ---
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    name = request.form.get("name")
    age = request.form.get("age")
    feeling = request.form.get("feeling")

    # --- Backend validation ---
    if not re.match("^[A-Za-z\s]+$", name):
        return "Invalid name. Please use only letters.", 400
    else:
        name = name.title()

    if not age.isdigit():
        return "Invalid age. Please enter numbers only.", 400

    # --- Emotion detection and response ---
    emotions = detect_emotions(feeling)
    main_emotion, response = supportive_response_multi(name, emotions)

    return render_template("index.html",
                           name=name,
                           emotion=main_emotion,
                           response=response)


if __name__ == "__main__":
    app.run(debug=True)
