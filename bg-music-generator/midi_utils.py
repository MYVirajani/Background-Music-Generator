from music21 import stream, note, chord, instrument
from midi2audio import FluidSynth
import subprocess
import os

def create_midi(prediction_output, output_path, note_duration=0.5):
    offset = 0
    output_notes = []

    for pattern in prediction_output:
        if ('.' in pattern) or pattern.isdigit():
            chord_notes_str = pattern.split('.')
            notes_in_chord = []
            for current_note in chord_notes_str:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = instrument.Piano()
                notes_in_chord.append(new_note)
            new_chord = chord.Chord(notes_in_chord)
            new_chord.offset = offset
            output_notes.append(new_chord)
        else:
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)

        offset += note_duration

    midi_stream = stream.Stream(output_notes)
    midi_stream.write('midi', fp=output_path)
    return output_path




def midi_to_wav(midi_path, wav_path, soundfont_path='soundfont/FluidR3_GM.sf2', timeout=60):
    midi_path = os.path.abspath(midi_path)
    wav_path = os.path.abspath(wav_path)
    soundfont_path = os.path.abspath(soundfont_path)

    if not os.path.exists(midi_path):
        raise FileNotFoundError(f"MIDI file not found: {midi_path}")
    if not os.path.exists(soundfont_path):
        raise FileNotFoundError(f"Soundfont not found: {soundfont_path}")

    cmd = [
        "fluidsynth", "-ni",
        "-a", "file",
        "-F", wav_path,
        "-r", "44100",
        soundfont_path,
        midi_path
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            stdin=subprocess.DEVNULL
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"FluidSynth timed out after {timeout}s")

    if result.returncode != 0:
        raise RuntimeError(f"FluidSynth conversion failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")

    if not os.path.exists(wav_path) or os.path.getsize(wav_path) == 0:
        raise RuntimeError("FluidSynth ran but produced no valid WAV output")

    return wav_path


def estimate_duration_seconds(num_notes, note_duration):
    """Rough estimate of track length for display purposes."""

    return round(num_notes * note_duration * 0.5, 1)