from mido import MidiFile
from fastdtw import fastdtw
import numpy as np

def extract_rhythmic_features(midi_file):
    midi = MidiFile(midi_file)

    note_onsets = []
    note_durations = []

    current_time = 0

    for i, track in enumerate(midi.tracks):
        for msg in track:
            current_time += msg.time

            if msg.type == 'note_on':
                note_onsets.append(current_time)
            elif msg.type == 'note_off':
                note_durations.append(current_time - note_onsets[-1])

    return note_onsets, note_durations

def preprocess_features(features):
    return (np.array(features) - np.mean(features)) / np.std(features)

midi_file1 = 'Queen - Bohemian Rhapsody.mid'
midi_file2 = 'Queen - Bohemian Rhapsody.mid'

features1 = extract_rhythmic_features(midi_file1)
features2 = extract_rhythmic_features(midi_file2)

performance1_features = preprocess_features(features1)
performance2_features = preprocess_features(features2)

# Ensure that both feature arrays are of the same length
min_length = min(len(performance1_features[0]), len(performance2_features[0]))
performance1_features = performance1_features[:, :min_length]
performance2_features = performance2_features[:, :min_length]

# Calculate the DTW distance
distance, path = fastdtw(performance1_features, performance2_features)

# Calculate similarity based on the aligned features
similarity = 1 / (1 + distance)
print("Rhythmic Similarity:", similarity)