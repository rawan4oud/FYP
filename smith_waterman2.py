from combine_notes import linked_notes1, adjusted_note_durations_list2
import numpy as np


def smith_waterman(seq1, seq2, match_score=10, mismatch_score=5, gap_penalty=1):
    # Initialize matrix for dynamic programming
    matrix = np.zeros((len(seq1) + 1, len(seq2) + 1))

    # Initialize matrices to store traceback pointers
    traceback = np.zeros((len(seq1) + 1, len(seq2) + 1, 3), dtype=int)  # 0: diagonal, 1: up, 2: left

    # Fill the matrix
    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):
            # Calculate the score based on pitch and duration
            seq1_pitch, seq1_duration = seq1[i - 1][0][1], seq1[i - 1][0][2]
            seq2_pitch, seq2_duration = seq2[j - 1][0][1], seq2[j - 1][0][2]
            match = matrix[i - 1][j - 1] + (
                match_score if (seq1_pitch == seq2_pitch or seq1_duration == seq2_duration) else mismatch_score)
            delete = matrix[i - 1][j] + gap_penalty
            insert = matrix[i][j - 1] + gap_penalty

            # Update matrix and traceback pointers
            matrix[i][j] = max(match, delete, insert, 0)
            if matrix[i][j] == match:
                traceback[i][j] = [i - 1, j - 1, 0]  # Diagonal
            elif matrix[i][j] == delete:
                traceback[i][j] = [i - 1, j, 1]  # Up
            elif matrix[i][j] == insert:
                traceback[i][j] = [i, j - 1, 2]  # Left

    # Find the maximum score in the matrix
    max_score = np.max(matrix)

    # Find the position of the maximum score
    max_indices = np.argwhere(matrix == max_score)
    i, j = max_indices[-1]  # Select the last maximum score position

    # Backtrack to find the alignment for the highest score
    alignment1_chars, alignment2_chars = [], []
    aligned_tuples = []  # To store tuples aligned between seq1 and seq2
    while i > 0 or j > 0:  # Continue until both i and j become zero
        if i > 0 and j > 0 and traceback[i][j][2] == 0:  # Diagonal
            alignment1_chars.insert(0, seq1[i - 1][0])
            alignment2_chars.insert(0, seq2[j - 1][0])
            aligned_tuples.append((seq1[i - 1][0], seq2[j - 1][0]))
            i, j = traceback[i][j][0], traceback[i][j][1]
        elif i > 0 and traceback[i][j][2] == 1:  # Up
            alignment1_chars.insert(0, seq1[i - 1][0])
            alignment2_chars.insert(0, None)
            i = traceback[i][j][0]
        else:  # Left
            alignment1_chars.insert(0, None)
            alignment2_chars.insert(0, seq2[j - 1][0])
            j = traceback[i][j][1]

    return max_score, alignment1_chars, alignment2_chars, aligned_tuples


max_score, alignment1, alignment2, aligned_tuples = smith_waterman(linked_notes1, adjusted_note_durations_list2)

print("_______________")
print("Alignments:")
for i in range(len(alignment1)):
    if alignment1[i] is not None and alignment2[i] is not None:
        print(f"Tuple from seq1: {alignment1[i]}, Tuple from seq2: {alignment2[i]}")
    elif alignment1[i] is not None:
        print(f"Tuple from seq1: {alignment1[i]}, No matching tuple from seq2")
    elif alignment2[i] is not None:
        print(f"No matching tuple from seq1, Tuple from seq2: {alignment2[i]}")
