from ngrams_preprocessing import midi_file_path1, midi_file_path2
from tempo_adjustment import adjust_tempo
import mido


def calculate_note_durations(midi_file_path):
    midi = mido.MidiFile(midi_file_path)
    note_on_events = {}
    note_durations = []

    for track in midi.tracks:
        time_elapsed = 0  # Time elapsed in ticks
        for msg in track:
            time_elapsed += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:  # Note on
                note_on_events[(msg.note, msg.channel)] = time_elapsed
            elif (msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)) and (msg.note, msg.channel) in note_on_events:
                # Note off or note on with velocity 0 (also considered as note off in some cases)
                start_time = note_on_events[(msg.note, msg.channel)]
                duration = time_elapsed - start_time
                note_durations.append((start_time, msg.note, duration))
                del note_on_events[(msg.note, msg.channel)]

    return note_durations

def detect_linked_notes(note_durations, midi_file_path):
    midi = mido.MidiFile(midi_file_path)
    ticks_per_beat = midi.ticks_per_beat
    eighth_note_duration = ticks_per_beat / 2  # Assuming a quarter note is the beat

    linked_notes = []
    prev_note = None
    for start, pitch, duration in note_durations:
        # Ensure we do not link notes with a duration greater than 400
        if duration > 400:
            # If the current note's duration is greater than 400, we start a new group and skip the linking logic
            linked_notes.append([(start, pitch, duration)])
            prev_note = None  # Reset prev_note to ensure the next note is not incorrectly linked
        else:
            # Logic to determine if notes are "linked" based on their pitch, duration, and starting times
            if prev_note and pitch == prev_note[1] and duration == prev_note[2] and abs(start - (prev_note[0] + prev_note[2])) < eighth_note_duration:
                linked_notes[-1].append((start, pitch, duration))
            else:
                linked_notes.append([(start, pitch, duration)])
            prev_note = (start, pitch, duration)

    return linked_notes

def is_combinable(note_group, reference_list):
    """
    Check if the given note_group can be combined based on a matching entry in the reference list.
    Assumes note_group consists of linked notes with the same pitch and consecutive start times.
    """
    if len(note_group) <= 1:
        return False  # Single notes do not need to be combined based on this logic.

    # Calculate the combined duration of the note group
    combined_duration = sum(note[2] for note in note_group)
    start_time = note_group[0][0]
    pitch = note_group[0][1]

    # Check against each note in the reference list
    for ref_start, ref_pitch, ref_duration in reference_list:
        if (start_time == ref_start and pitch == ref_pitch
                and abs(combined_duration - ref_duration) <= 100):
            return True
    return False


def adjust_notes_based_on_reference(linked_notes, reference_list):
    adjusted_notes = []

    # Flatten the reference list
    flattened_reference_list = [item for sublist in reference_list for item in sublist]

    for note_group in linked_notes:
        if is_combinable(note_group, flattened_reference_list):
            # Combine the notes in the group
            combined_start = note_group[0][0]
            combined_pitch = note_group[0][1]
            combined_duration = sum(note[2] for note in note_group)+1
            adjusted_notes.append([(combined_start, combined_pitch, combined_duration)])
        else:
            adjusted_notes.extend([note_group])

    return adjusted_notes




# Example usage

adjust_tempo(midi_file_path1, 120)
note_durations1 = calculate_note_durations(midi_file_path1)
linked_notes1 = detect_linked_notes(note_durations1, midi_file_path1)
adjust_tempo(midi_file_path2, 120)
note_durations2 = calculate_note_durations(midi_file_path2)
linked_notes2 = detect_linked_notes(note_durations2, midi_file_path2)


print("Ref:", len(linked_notes1), linked_notes1)
print("_________________")
print("Test (before combining notes):", len(linked_notes2), linked_notes2)
print("_________________")


# Adjusted list2
adjusted_note_durations_list2 = adjust_notes_based_on_reference(linked_notes2, linked_notes1)

print("Test (after combining notes):", len(adjusted_note_durations_list2), adjusted_note_durations_list2)
