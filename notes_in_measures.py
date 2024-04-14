import subprocess
import os
import warnings
import soundfile as sf
import librosa
import numpy as np
from ngrams_preprocessing import midi_file_path1, midi_file_path2
from smith_waterman import sliding

def convert_midi_to_wav(midi_file):
    # Get the base name of the MIDI file
    midi_base_name = os.path.basename(midi_file)

    # Change the extension to '.wav' for the output file
    wav_file_name = os.path.splitext(midi_base_name)[0] + '.wav'

    # Check if the WAV file already exists
    wav_file_path = os.path.join(r'C:\Users\Sara\OneDrive\Desktop\FYP\Test Files', wav_file_name)

    # Compose the command to convert MIDI to WAV
    command = [
        r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe',
        '-o', wav_file_path,
        midi_file
    ]

    # Execute the command
    subprocess.run(command)


def adjust_tempo(audio_file_path, new_tempo):
    # Load audio file
    y, sr = librosa.load(audio_file_path, sr=None)

    # Calculate the current tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # Calculate tempo ratio
    tempo_ratio = new_tempo / tempo

    # Adjust the tempo of the audio
    y_stretched = librosa.effects.time_stretch(y, tempo_ratio)

    # Save adjusted audio file (overwrite original)
    sf.write(audio_file_path, y_stretched, sr)


# Function to detect notes from audio file
def detect_notes(audio_file):
    # Load audio file
    y, sr = librosa.load(audio_file)

    # Extract onset times and their corresponding notes
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

    # Identify note frequencies
    note_freqs = []
    for frame in range(pitches.shape[1]):
        max_magnitude_index = np.argmax(magnitudes[:, frame])
        if magnitudes[max_magnitude_index, frame] > 0:  # Ensure magnitude is not zero
            note_freqs.append(pitches[max_magnitude_index, frame])

    # Convert frequencies to note names
    note_names = [librosa.hz_to_note(freq) for freq in note_freqs]

    return onset_times, note_names

# Function to calculate measures
def calculate_measures(onset_times, note_names):
    beats_per_measure = 4
    beats_per_minute = 120  # Assuming a default tempo of 120 beats per minute
    beat_duration = 60 / beats_per_minute
    measure_duration = beats_per_measure * beat_duration

    measures = []
    current_measure = []
    current_measure_start_time = 0

    for i, onset_time in enumerate(onset_times):
        if onset_time - current_measure_start_time >= measure_duration:
            measures.append(current_measure)
            current_measure = []
            current_measure_start_time += measure_duration

        current_measure.append(note_names[i])

    # Add the last measure if it's not complete
    if current_measure:
        measures.append(current_measure)

    return measures

def mapping_to_measures(measures, list):
    mapped_measures = {}
    list_index = 0

    for i, measure in enumerate(measures):
        mapped_measures[f"Measure {i + 1}"] = list[list_index:list_index + len(measure)]
        list_index += len(measure)

    return mapped_measures

warnings.filterwarnings("ignore")


# Convert MIDI to WAV
convert_midi_to_wav(midi_file_path1)
audio_file = os.path.join(os.path.splitext(midi_file_path1)[0]  + '.wav')

adjust_tempo(audio_file, 120)
onset_times, note_names = detect_notes(audio_file)
measures = calculate_measures(onset_times, note_names)