# 🎵 AI Background Music Generator
 
An AI Music Generation system that trains an LSTM neural network on classical piano MIDI data to compose original, royalty-free background music — packaged as an interactive Streamlit web application.

---

## 📖 Overview
 
This project implements a complete **AI Music Generation pipeline**:
 
1. Collect MIDI music data (classical piano)
2. Preprocess MIDI into note/chord sequences using `music21`
3. Build and train an LSTM deep learning model to learn musical patterns
4. Generate new, original note sequences from the trained model
5. Convert generated sequences back into MIDI, then render to audio (WAV)
It's then wrapped in a **Streamlit web app** that lets a user pick a mood and track length, generate a track, listen to it in-browser, and download it — framed as an **AI Background Music Generator** for videos, streams, and creative projects.

---
 
## 🗂️ Dataset
 
- **Source:** [Classical Music MIDI Dataset (Kaggle)](https://www.kaggle.com/datasets/soumikrakshit/classical-music-midi)
- **Content:** Solo classical piano MIDI files

---
 
## 🧪 Model Training Pipeline 
 
1. **Data extraction** — MIDI dataset uploaded to Google Drive, extracted and parsed with `music21`
2. **Sequence preparation** — notes converted into a vocabulary and fixed-length training sequences, saved as `notes.pkl` / `mappings.pkl`
3. **Model training** — LSTM trained for up to 100 epochs with checkpointing, early stopping, and learning rate reduction
4. **Generation testing** — verified output quality across multiple temperature settings before finalizing the model
5. **Export** — `final_model.keras`, `mappings.pkl`, and `seeds.pkl` downloaded from Drive into the app's `model_files/` directory
---


## ⚙️ Setup & Installation
 
### 1. Install FluidSynth (system-level dependency)
 
FluidSynth must be installed and accessible from the command line — it's used to render MIDI into playable audio.
 
**Windows:**
Run PowerShell as Administrator

Run the install command:
```bash
choco install fluidsynth -y
```
 
Verify installation:
```bash
fluidsynth --version
```
 
### 2. Download a SoundFont
 
#### Option A — Download via PowerShell

```powershell
Invoke-WebRequest -Uri "https://github.com/FluidSynth/fluidsynth/raw/master/sf2/VintageDreamsWaves-v2.sf2" -OutFile "soundfont/FluidR3_GM.sf2"
```
#### Option B — download manually in your browser:

1. Go to: https://github.com/FluidSynth/fluidsynth/tree/master/sf2
2. Download VintageDreamsWaves-v2.sf2 (or any .sf2 file listed there)
3. Move it into your project's soundfont/ folder
4. Rename it to FluidR3_GM.sf2
 
### 3. Install Python dependencies
 
```bash
python -m venv venv
venv\Scripts\activate        
pip install -r requirements.txt
```
 
**`requirements.txt`:**
```
streamlit
tensorflow
music21
numpy
```
 
### 4. Run the app
 
```bash
streamlit run app.py
```
 
