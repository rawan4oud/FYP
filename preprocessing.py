import mido 
from mido import MidiFile

def parse_midi(file_path):
    midi_file = MidiFile(file_path)
    notes_stream = []

    for i, track in enumerate(midi_file.tracks):
        for msg in track:
            if msg.type == 'note_on':
                note = {
                    'channel': i,
                    'start': msg.time,
                    'duration': None,
                    'pitch': msg.note,
                    'velocity': msg.velocity
                }
                notes_stream.append(note)
            elif msg.type == 'note_off':
                for note in reversed(notes_stream):
                    if note['pitch'] == msg.note and note['channel'] == i and note['duration'] is None:
                        note['duration'] = msg.time - note['start']
                        break

    return notes_stream
# def separate_tracks(notes_stream):
#     tracks = [[] for _ in range(16)]

#     for note in notes_stream:
#         tracks[note['channel']].append(note)

#     return tracks

def separate_tracks(notes_stream):
    tracks = [[] for _ in range(16)]

    for note in notes_stream:
        # Subtract 1 from channel to make it 0-indexed
        tracks[note['channel'] - 1].append(note)

    return tracks

def merge_notes(track):
    merged_track = []

    for i, note in enumerate(track):
        if i == 0 or note['start'] - track[i-1]['start'] > 50:
            merged_track.append(note)
        else:
            # Check if the current note has a higher pitch than the previous one
            if note['pitch'] > merged_track[-1]['pitch']:
                merged_track[-1] = note

    return merged_track

def get_pitch_sequence(track):
    pitch_sequence = [note['pitch'] for note in track]
    return pitch_sequence

def compute_difference(pitch_sequence):
    difference_sequence = [pitch_sequence[i+1] - pitch_sequence[i] for i in range(len(pitch_sequence)-1)]
    return difference_sequence

def get_string_sequence(difference_sequence):
    string_sequence = [chr(pitch + 65) for pitch in difference_sequence]  # Convert pitch to ASCII character
    return ''.join(string_sequence)

def main(file_path):
    # Step 1: Parse MIDI file
    notes_stream = parse_midi(file_path)

    # Step 2: Separate tracks by Channel
    tracks = separate_tracks(notes_stream)

    # Step 3: Merge notes in each track
    merged_tracks = [merge_notes(track) for track in tracks]

    # Steps 4 and 5: Get pitch sequence and compute difference
    string_sequences = []
    for i, track in enumerate(merged_tracks):
        pitch_sequence = get_pitch_sequence(track)
        difference_sequence = compute_difference(pitch_sequence)

        # Step 6: Get string sequence
        string_sequence = get_string_sequence(difference_sequence)
        string_sequences.append(string_sequence)

        # print(f"Track {i+1} String Sequence: {string_sequence}")
    return string_sequences

if __name__ == "__main__":
    midi_file_path = "Queen - Bohemian Rhapsody.mid"
    print(main(midi_file_path))
