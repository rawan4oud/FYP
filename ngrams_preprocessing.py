import mido
from mido import MidiFile

def parse_midi(file_path):
    midi_file = MidiFile(file_path)
    notes_stream = []

    for i, track in enumerate(midi_file.tracks):
        for msg in track:
            if msg.type == 'note_on' and msg.velocity!=0:
                note = {
                    'channel': i,
                    'start': msg.time,
                    'duration': None,
                    'pitch': msg.note,
                    'velocity': msg.velocity
                }
                notes_stream.append(note)
            # elif msg.type == 'note_off':
            #     for note in reversed(notes_stream):
            #         if note['pitch'] == msg.note and note['channel'] == i and note['duration'] is None:
            #             note['duration'] = msg.time - note['start']
            #             break
    #print(notes_stream)
    return notes_stream

def separate_tracks(notes_stream):
    tracks = []

    for note in notes_stream:
        tracks.append([note])
    #print(tracks)
    return tracks



# def merge_notes(tracks):
#     merged_track = []
#     for i, notes in enumerate(tracks):
#         if (i == 0 or (tracks[i][0]['start'] - tracks[i-1][0]['start']) > 50):
#             merged_track.append(notes)
#         else:
#             test = tracks[i][0]['pitch']
#             test2 = merged_track[-1][0]['pitch']
#             if tracks[i][0]['pitch'] > merged_track[-1]['pitch']:
#                 merged_track[-1] = notes
#     return merged_track



def get_pitch_sequence(tracks):
    pitch_sequence = []
    for track in tracks:
        for note in track:
            pitch_sequence.append(note["pitch"])
    #print(pitch_sequence)
    return pitch_sequence



def compute_difference(pitch_sequence, margin_of_error=0):
    difference_sequence = [abs(pitch_sequence[i + 1] - pitch_sequence[i]) for i in range(len(pitch_sequence) - 1)]
    #print(difference_sequence)
    return difference_sequence


def get_string_sequence(pitch_sequence):
    string_sequence = []
    for pitch in pitch_sequence:
        string_sequence.append(chr(pitch)) # Convert difference to ASCII character
    return string_sequence



def main(file_path):
    # Step 1: Parse MIDI file
    notes_stream = parse_midi(file_path)
    #print(len(notes_stream))
    #print(notes_stream)


    # Step 2: Separate tracks by Channel
    tracks = separate_tracks(notes_stream)

    # Step 3: Merge notes in each track
    #merged_tracks = merge_notes(tracks)
    #print(merged_tracks)
    #print("__________")

    # Steps 4 and 5: Get pitch sequence and compute difference

    pitch_sequence = get_pitch_sequence(tracks)
    #print(pitch_sequence)

    difference_sequence = compute_difference(pitch_sequence, margin_of_error=3)

    # Step 6: Get string sequence
    string_sequence = get_string_sequence(pitch_sequence)

        # print(f"Track {i+1} String Sequence: {string_sequence}")
    #print(string_sequence)
    #print(len(string_sequence))
    return string_sequence


midi_file_path1 = "Test Files/Au claire de la lune (part 1) ref.mid"
midi_file_path2 = "Test Files/Au claire de la lune (part 1) test.mid"

string_sequences1 = main(midi_file_path1)
string_sequences2 = main(midi_file_path2)
# string_sequences3 = main(midi_file_path3)