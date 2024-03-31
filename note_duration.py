import mido
from ngrams_preprocessing import midi_file_path1, midi_file_path2
from smith_waterman import sliding


note_durations = {
        "half": (0.9, 1.1),        # Representing 0.9 to 1.1 seconds
        "quarter": (0.4, 0.6),     # Representing 0.4 to 0.6 seconds
        "eighth": (0.2, 0.3),      # Representing 0.2 to 0.3 seconds
        "sixteenth": (0.1, 0.19),  # Representing 0.1 to 0.19 seconds
        "thirtytwo": (0, 0.09)     # Representing 0 to 0.09 seconds
    }


def get_note_durations(midifile):
    # Open the MIDI file
    mid = mido.MidiFile(midifile)

    # Initialize variables
    note_durations = []
    current_notes = {}  # Dictionary to keep track of active notes and their timestamps

    # Iterate through each message in the MIDI file
    for msg in mid:
        # Handle note-on and note-off events
        if msg.type == 'note_on' and msg.velocity > 0:
            current_notes[msg.note] = msg.time

        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            note_on_time = current_notes.pop(msg.note, None)
            if note_on_time is not None:
                duration = msg.time + note_on_time
                note_durations.append((msg.note, duration))

    for note, duration in note_durations:
        print(f"Note {note} duration: {duration} ticks")
    print(len(note_durations))

    return note_durations


def compare_durations_with_match(sliding_list, durations1, durations2, note_durations):
    compared_durations = []
    for i, char in enumerate(sliding_list):
        if char == 'Match' and i < len(durations1) and i < len(durations2):
            duration1 = durations1[i][1]
            duration2 = durations2[i][1]
            same_range = any(
                start <= duration1 <= end and start <= duration2 <= end for start, end in note_durations.values())
            compared_durations.append((i, duration1, duration2, "Same Range" if same_range else "Different Ranges"))
    return compared_durations


# durations1 = get_note_durations(midi_file_path1)
# durations2 = get_note_durations(midi_file_path2)

