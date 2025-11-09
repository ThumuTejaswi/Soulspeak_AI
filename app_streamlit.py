import streamlit as st
import re
# Function to detect emotion based on keywords
def detect_emotion(feeling_text):
    feeling_text = feeling_text.lower().strip()
    words = feeling_text.split()  # split input into words

    happy_words = ["happy", "joy", "excited", "glad"]
    sad_words = ["sad", "unhappy", "down", "depressed"]
    angry_words = ["angry", "mad", "furious", "annoyed"]
    stressed_words = ["stressed", "tired", "anxious", "overwhelmed"]

    if any(word in words for word in happy_words):
        return "😊"
    elif any(word in words for word in sad_words):
        return "😢"
    elif any(word in words for word in angry_words):
        return "😡"
    elif any(word in words for word in stressed_words):
        return "😔"
    else:
        return "😊"  # default

# Function to extract the main feeling word from user input
def extract_keyword(feeling_text):
    feeling_text = feeling_text.lower().strip()
    words = feeling_text.split()  # split into words

    # Ordered list: more specific/negative words first
    feelings = ["unhappy", "depressed", "down", "mad", "furious", "angry", 
                "annoyed", "stressed", "tired", "anxious", "overwhelmed",
                "happy", "joy", "excited", "glad"]

    for word in feelings:
        if word in words:
            return word
    return "good"  # default


# Function for supportive response
def supportive_response(name, emotion, actual_word):
    if emotion == "😊":
        return f"{name}, you're doing great! Keep smiling 💙"
    elif emotion == "😢":
        return f"{name}, it's okay to feel {actual_word}. Remember, you're not alone 💙"
    elif emotion == "😡":
        return f"{name}, I understand that you're feeling {actual_word}. Take a deep breath, you are stronger than this 💙"
    elif emotion == "😔":
        return f"{name}, it's okay to feel {actual_word}. Try to relax, you are capable 💙"
    else:
        return f"{name}, stay strong 💙"

# Streamlit app UI
st.title("💙 SoulSpeak.ai - Your Emotional Support AI")

# Input section
name = st.text_input("What's your name?")
if name:
    if not re.match("^[A-Za-z\s]+$", name):
        st.warning("Name should only contain letters and spaces 💙")
    else:
        # Capitalize first letter of each word
        name = name.title()
age = st.number_input("How old are you?", min_value=1, max_value=120, step=1)
feeling = st.text_area("How are you feeling today?")

if st.button("Submit"):
    if name and age and feeling:
        # Detect emoji for the feeling
        emotion = detect_emotion(feeling)
        # Extract main feeling word for personalized response
        actual_word = extract_keyword(feeling)
        # Generate supportive response
        response = supportive_response(name, emotion, actual_word)

        # Display results
        st.markdown(f"<h3 style='color:#4A90E2;'>Hi {name} 💙</h3>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{emotion}</h1>", unsafe_allow_html=True)
        st.success(response)
    else:
        st.warning("Please fill all fields before submitting 💙")