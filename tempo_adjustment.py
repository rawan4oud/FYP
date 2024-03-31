import mido
from mido import MidiFile


def adjust_tempo(file_path, new_tempo_bpm):
    # Load the MIDI file
    midi = MidiFile(file_path)

    # Calculate new tempo (microseconds per beat)
    new_tempo = mido.bpm2tempo(new_tempo_bpm)

    # Modify tempo by adjusting set_tempo events
    for track in midi.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                msg.tempo = new_tempo

    # Overwrite the original MIDI file with the modified content
    midi.save(file_path)

