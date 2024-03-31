from nltk import ngrams
from mido import MidiFile
from ngrams_preprocessing import midi_file_path1, midi_file_path2, string_sequences1, string_sequences2
from smith_waterman import smith_waterman, sliding, alignment1_chars, alignment2_chars
from notes_in_measures import measures
from note_duration import compare_durations_with_match, get_note_durations, note_durations


def compute_ngram_similarity(string_sequence1, string_sequence2, n):
    # Convert string sequences to n-grams
    ngrams1 = set(ngrams(string_sequence1, n))
    ngrams2 = set(ngrams(string_sequence2, n))

    # Calculate Jaccard similarity coefficient
    intersection = len(ngrams1.intersection(ngrams2))
    union = len(ngrams1.union(ngrams2))

    # Jaccard similarity coefficient ranges from 0 to 1
    similarity = intersection / union if union != 0 else 0.0
    return similarity

def compute_similarity_matrix(list1, list2, n):
    matrix = [[0.0 for _ in range(len(list2))] for _ in range(len(list1))]
    for i, seq1 in enumerate(list1):
        for j, seq2 in enumerate(list2):
            similarity = compute_ngram_similarity(seq1, seq2, n)
            matrix[i][j] = similarity
    return matrix

    return similarity_matrix

def mapping_to_measures(measures):
    mapped_measures = {}
    list_index = 0

    for i, measure in enumerate(measures):
        mapped_measures[f"Measure {i + 1}"] = sliding_list[list_index:list_index + len(measure)]
        list_index += len(measure)

    # Print mapped measures
    print("Mapped Measures:")
    for measure, notes in mapped_measures.items():
        print(f"{measure}: {notes}")

def print_match_score(matrix):
    counter = 0
    diagonal = []
    for i, row in enumerate(matrix):
        formatted_row = ["{:.2f}".format(value) for value in row]
        diagonal.append(row[i])
        if row[i] > 0.7:
            counter += 1
        # print(formatted_row)
    print(f"\nDiagonal Values: {diagonal}")
    print(f"Number of Diagonal Values greater than 0.7: {counter}/{len(diagonal)}")
    print("-----------------------")



if __name__ == "__main__":

    print(string_sequences1)
    print(string_sequences2)

    print("-----------------------")


    print(alignment1_chars)
    print(alignment2_chars)

    sliding_list = sliding()
    print("-----------------------")

    matrix = compute_similarity_matrix(alignment1_chars, alignment2_chars, 1)

    mapping_to_measures(measures)

    print_match_score(matrix)

    durations1 = get_note_durations(midi_file_path1)
    durations2 = get_note_durations(midi_file_path2)

    compared_durations = compare_durations_with_match(sliding_list, durations1, durations2, note_durations)
    for duration in compared_durations:
        print(duration)