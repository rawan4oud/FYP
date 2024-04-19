from music21 import converter, expressions, layout, text
import os
from compare_notes import matches
from notes_in_measures import measures, mapping_to_measures
from ngrams_preprocessing import midi_file_path1_mxl
from smith_waterman import sliding

def generate_new_list(tuple_list):
    new_list = []
    for tup in tuple_list:
        if tup[0] == 'Pitch Match':
            if tup[1] == 'Dur. Mismatch':
                new_list.append(tup)
            else:
                new_list.append('Match')
        elif tup[0] == 'Sliding':
            new_list.append(tup[0])

        elif tup[0] == 'Pitch Mismatch':
            if tup[1] == 'Dur. Mismatch':
                new_list.append('No Match')
        else:
            new_list.append(tup[1])
    return new_list


def write_on_score():
    # Replace 'path_to_your_file.musicxml' with the actual path to your MusicXML file
    score = converter.parse(midi_file_path1_mxl)
    for part in score.parts:
        for measure_number, labels in mapped_measures.items():
            measure = part.measure(measure_number)
            notes = measure.notes
            for i, label in enumerate(labels):
                if i < len(notes):
                    if isinstance(label, tuple):
                        # For the first element of the tuple, we place it with the default setting
                        notes[i].addLyric(label[0])
                        # For the second element of the tuple, we specify it to be in a different verse
                        # by incrementing the number
                        notes[i].addLyric(label[1])
                    else:
                        notes[i].addLyric(label)

                    # Set the color based on the label type
                    if label == 'No Match' or label == 'Dur. Mismatch' or label == 'Pitch Mismatch':
                        notes[i].lyrics[-1].style.color = 'red'
                    elif label == 'Sliding':
                        notes[i].lyrics[-1].style.color = 'yellow'
                    elif label == 'Match' or label == 'Dur. Match' or label == 'Pitch Match':
                        notes[i].lyrics[-1].style.color = 'green'
                    else:
                        # Default color
                        notes[i].lyrics[-1].style.color = 'black'
    # Get the base name of the original MusicXML file
    base_name = os.path.splitext(os.path.basename(midi_file_path1_mxl))[0]

    # Compose the output file name with 'modified' appended
    output_file_name = base_name + '_modified.musicxml'

    # Specify the output file path in the "Test Files" directory
    output_file_path = os.path.join('Test Files', output_file_name)

    # Write the modified score to the output file
    score.write('musicxml', output_file_path)


def compute_pitch_score(tuple_list):
    pitch_counter = 0

    total_tuples = len(tuple_list)

    for item in tuple_list:
        if isinstance(item, tuple):

            if item[0] == 'Pitch Match' or item[0] == 'Match':
                pitch_counter += 1

        elif item == 'Match':
            pitch_counter += 1

    if total_tuples == 0:
        return 0  # Avoid division by zero

    score = pitch_counter / total_tuples
    return score*80


def compute_duration_score(tuple_list):
    match_counter = 0
    pitch_match_counter = 0

    for item in tuple_list:
        if isinstance(item, tuple) and item[0] == 'Pitch Match':
            pitch_match_counter += 1

        elif item == 'Match':
            match_counter += 1
            pitch_match_counter += 1

    if pitch_match_counter == 0:
        return 0  # Avoid division by zero

    score = match_counter / pitch_match_counter
    return score*10

def compute_sliding_score(tuple_list):
    sliding_counter = len(tuple_list)

    total_tuples = len(tuple_list)

    for item in tuple_list:

        if item == 'Sliding':
            sliding_counter -= 1

    if total_tuples == 0:
        return 0  # Avoid division by zero

    score = sliding_counter / total_tuples
    return score*10

def compute_total_score(tuple_list):
    return compute_pitch_score(tuple_list)+compute_duration_score(tuple_list)+compute_sliding_score(tuple_list)

result_sliding = sliding()
# Combine the results in the requested format
combined_results = list(zip(result_sliding, matches))
print(combined_results)

print("_______________")

new_list = generate_new_list(combined_results)
print(new_list)

print("_______________")

mapped_measures = mapping_to_measures(measures, new_list)
# Print mapped measures
print("Mapped Measures:")
for measure, notes in mapped_measures.items():
    print(f"{measure}: {notes}")

write_on_score()

print(compute_pitch_score(new_list))
print(compute_duration_score(new_list))
print(compute_sliding_score(new_list))

print('Total score: ', format(compute_total_score(new_list), ".2f"),"/ 100")
