import streamlit as st
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import tempfile
import os

st.title("🎙️ Speech to Text Converter")
st.write("Record your voice or upload a `.wav` file to get transcription.")

option = st.radio("Choose input method:", ["🎤 Record with Microphone", "📁 Upload Audio File"])

recognizer = sr.Recognizer()

def transcribe_audio(file_path):
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "❗ Could not understand the audio."
        except sr.RequestError as e:
            return f"❗ API error: {e}"

if option == "🎤 Record with Microphone":
    duration = st.slider("Recording duration (seconds)", 3, 30, 5)
    if st.button("🔴 Record"):
        st.info("Recording... Speak now!")
        fs = 44100  # Sample rate
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        
        # Save to temp WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
            wav.write(temp_wav.name, fs, recording)
            st.success("✅ Recording complete!")
            st.audio(temp_wav.name, format="audio/wav")
            st.write("📝 Transcription:")
            st.write(transcribe_audio(temp_wav.name))

elif option == "📁 Upload Audio File":
    uploaded_file = st.file_uploader("Upload a `.wav` file", type=["wav"])
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name
        st.audio(temp_path, format='audio/wav')
        st.write("📝 Transcription:")
        st.write(transcribe_audio(temp_path))
