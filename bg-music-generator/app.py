import streamlit as st
import pickle
import numpy as np
import os
import random
import time
import traceback
from tensorflow.keras.models import load_model

from generate import generate_notes
from midi_utils import create_midi, midi_to_wav, estimate_duration_seconds


st.set_page_config(page_title="Background Music Generator", page_icon="🎵", layout="centered")


MODEL_PATH = "model_files/final_model.keras"
MAPPINGS_PATH = "model_files/mappings.pkl"
SEEDS_PATH = "model_files/seeds.pkl"
SOUNDFONT_PATH = "soundfont/FluidR3_GM.sf2"
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


MOOD_PRESETS = {
    "Calm / Ambient":   {"temperature": 0.5, "note_duration": 0.8},
    "Classical / Balanced": {"temperature": 0.8, "note_duration": 0.5},
    "Dramatic / Energetic": {"temperature": 1.1, "note_duration": 0.35},
}

LENGTH_PRESETS = {
    "Short (~30s clip)": 120,
    "Medium (~1 min)": 240,
    "Long (~2 min)": 480,
}


@st.cache_resource
def load_resources():
    model = load_model(MODEL_PATH)
    with open(MAPPINGS_PATH, "rb") as f:
        mappings = pickle.load(f)
    seeds = None
    if os.path.exists(SEEDS_PATH):
        with open(SEEDS_PATH, "rb") as f:
            seeds = pickle.load(f)
    return model, mappings, seeds

model, mappings, seed_sequences = load_resources()
note_to_int = mappings["note_to_int"]
int_to_note = mappings["int_to_note"]
n_vocab = mappings["n_vocab"]
sequence_length = mappings["sequence_length"]


st.title("🎵 Background Music Generator")
st.markdown(
    "Generate original, royalty-free classical piano background music for your videos, "
    "streams, or projects."
)
st.divider()


col1, col2 = st.columns(2)
with col1:
    mood = st.selectbox("Choose a mood", list(MOOD_PRESETS.keys()))
with col2:
    length_label = st.selectbox("Track length", list(LENGTH_PRESETS.keys()))

with st.expander("Advanced settings (optional)"):
    override_temp = st.slider(
        "Fine-tune creativity", 0.3, 1.5,
        value=MOOD_PRESETS[mood]["temperature"], step=0.1,
        help="Overrides the mood preset if changed."
    )
    use_real_seed = st.checkbox(
        "Use a real musical excerpt as starting point (recommended)",
        value=True if seed_sequences else False,
        disabled=(seed_sequences is None)
    )

generate_btn = st.button("🎼 Generate Background Track", type="primary", use_container_width=True)


if generate_btn:
    
    mood_label = mood.split("/")[0].strip().lower()

    preset = MOOD_PRESETS[mood]
    temperature = override_temp
    note_duration = preset["note_duration"]
    num_notes = LENGTH_PRESETS[length_label]

    progress_text = st.empty()
    progress_bar = st.progress(0)

    try:
        
        progress_text.text("Preparing seed...")
        progress_bar.progress(10)

        if use_real_seed and seed_sequences:
            seed_sequence = random.choice(seed_sequences)
        else:
            seed_sequence = [random.randint(0, n_vocab - 1) for _ in range(sequence_length)]

        
        progress_text.text(f"Composing your {mood_label} track...")
        progress_bar.progress(30)

        prediction_output = generate_notes(
            model=model,
            seed_sequence=seed_sequence,
            int_to_note=int_to_note,
            n_vocab=n_vocab,
            num_notes=num_notes,
            temperature=temperature
        )

        if not prediction_output or len(prediction_output) == 0:
            raise ValueError("Generation produced an empty sequence — check the model/mappings.")

       
        progress_text.text("Rendering MIDI...")
        progress_bar.progress(65)

        timestamp = str(int(time.time()))
        midi_path = os.path.join(OUTPUT_DIR, f"bgmusic_{timestamp}.mid")
        wav_path = os.path.join(OUTPUT_DIR, f"bgmusic_{timestamp}.wav")

        create_midi(prediction_output, midi_path, note_duration=note_duration)

        if not os.path.exists(midi_path):
            raise FileNotFoundError(f"MIDI file was not created at {midi_path}")
        if os.path.getsize(midi_path) == 0:
            raise ValueError(f"MIDI file was created but is empty: {midi_path}")

     
        progress_text.text("Rendering audio...")
        progress_bar.progress(85)

        midi_to_wav(midi_path, wav_path, SOUNDFONT_PATH)

        if not os.path.exists(wav_path):
            raise FileNotFoundError(f"WAV file was not created at {wav_path}")

        progress_bar.progress(100)
        progress_text.empty()
        progress_bar.empty()

        duration = estimate_duration_seconds(num_notes, note_duration)
        st.success(f"Generated a {duration}s {mood_label} track!")

        with open(wav_path, "rb") as f:
            st.audio(f.read(), format="audio/wav")

        dl_col1, dl_col2 = st.columns(2)
        with dl_col1:
            with open(midi_path, "rb") as f:
                st.download_button("⬇️ Download MIDI", f, file_name="background_music.mid", use_container_width=True)
        with dl_col2:
            with open(wav_path, "rb") as f:
                st.download_button("⬇️ Download WAV", f, file_name="background_music.wav", use_container_width=True)

        st.info("This track is uniquely generated — safe to use without copyright/royalty concerns.")

        
    except Exception as e:
        progress_bar.empty()
        progress_text.empty()
        st.error(f"Something went wrong: {e}")
        with st.expander("Full error details (for debugging)"):
            st.code(traceback.format_exc())
