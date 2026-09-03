# 🎵 AI Background Music Generator
 
An AI Music Generation system that trains an LSTM neural network on classical piano MIDI data to compose original, royalty-free background music — packaged as an interactive Streamlit web application.

## 📖 Overview
 
This project implements a complete **AI Music Generation pipeline**:
 
1. Collect MIDI music data (classical piano)
2. Preprocess MIDI into note/chord sequences using `music21`
3. Build and train an LSTM deep learning model to learn musical patterns
4. Generate new, original note sequences from the trained model
5. Convert generated sequences back into MIDI, then render to audio (WAV)
It's then wrapped in a **Streamlit web app** that lets a user pick a mood and track length, generate a track, listen to it in-browser, and download it — framed as an **AI Background Music Generator** for videos, streams, and creative projects.
