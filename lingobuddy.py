import openai
import streamlit as st
import pyttsx3
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit UI setup
st.set_page_config(page_title="LingoBuddy", page_icon="🗣️")
st.title("🗣️ LingoBuddy: Practice English A1–A2")

# Text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def ask_bot(user_input, level="A1"):
    prompt = f"You are a friendly English teacher chatbot helping students at {level} level. Keep responses simple. Correct mistakes and explain gently.\nStudent: {user_input}\nBot:"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def correct_grammar(sentence):
    prompt = f"Correct this sentence and explain the mistake simply for A1 level:\n'{sentence}'"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def generate_quiz(topic="food"):
    prompt = f"Create a 3-question multiple choice quiz for A1 level English learners about {topic}. Include answers and explanations."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Streamlit interface
mode = st.radio("Choose a mode:", ["Conversation", "Grammar Correction", "Vocabulary Quiz", "Listening Practice"])

if mode == "Conversation":
    user_input = st.text_input("Say something in English:")
    if user_input:
        reply = ask_bot(user_input)
        st.write("Bot:", reply)

elif mode == "Grammar Correction":
    sentence = st.text_input("Enter a sentence to correct:")
    if sentence:
        correction = correct_grammar(sentence)
        st.write("Correction:", correction)

elif mode == "Vocabulary Quiz":
    topic = st.text_input("Enter a topic (e.g., food, animals, weather):")
    if topic:
        quiz = generate_quiz(topic)
        st.write("Quiz:", quiz)

elif mode == "Listening Practice":
    prompt = st.text_input("Enter a sentence to hear:")
    if prompt:
        st.write("Speaking...")
        speak(prompt)
