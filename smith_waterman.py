import numpy as np
from ngrams_preprocessing import string_sequences1, string_sequences2


def smith_waterman(alignment1, alignment2, match_score=2, mismatch_score=-1, gap_penalty=-1):
    # Initialize matrix for dynamic programming
    matrix = np.zeros((len(alignment1) + 1, len(alignment2) + 1))

    # Fill the matrix
    for i in range(1, len(alignment1) + 1):
        for j in range(1, len(alignment2) + 1):
            match = matrix[i - 1][j - 1] + (match_score if alignment1[i - 1] == alignment2[j - 1] else mismatch_score)
            delete = matrix[i - 1][j] + gap_penalty
            insert = matrix[i][j - 1] + gap_penalty
            matrix[i][j] = max(match, delete, insert, 0)

    # Find the maximum score in the matrix
    max_score = np.max(matrix)

    # Find the position of the maximum score
    max_indices = np.argwhere(matrix == max_score)

    # Backtrack to find the alignment
    alignments = []
    for idx in max_indices:
        i, j = idx
        alignment1_chars, alignment2_chars = [], []
        source_chars = []  # Sources for the characters in alignment2
        while i > 0 and j > 0:  # Adjusted loop condition
            if matrix[i][j] == matrix[i - 1][j - 1] + (
            match_score if alignment1[i - 1] == alignment2[j - 1] else mismatch_score):
                alignment1_chars.insert(0, alignment1[i - 1])
                alignment2_chars.insert(0, alignment2[j - 1])
                source_chars.insert(0, 'Match' if alignment1[i - 1] == alignment2[j - 1] else 'Mismatch')
                i -= 1
                j -= 1
            elif matrix[i][j] == matrix[i - 1][j] + gap_penalty:
                alignment1_chars.insert(0, alignment1[i - 1])
                alignment2_chars.insert(0, '-')
                source_chars.insert(0, 'Gap in seq2')
                i -= 1
            else:
                alignment1_chars.insert(0, '-')
                alignment2_chars.insert(0, alignment2[j - 1])
                source_chars.insert(0, 'Extra notes in seq2')
                j -= 1

        # Handle the remaining characters in alignment1 or alignment2
        while i > 0:
            alignment1_chars.insert(0, alignment1[i - 1])
            alignment2_chars.insert(0, '-')
            source_chars.insert(0, 'Extra notes in seq1')
            i -= 1
        while j > 0:
            alignment1_chars.insert(0, '-')
            alignment2_chars.insert(0, alignment2[j - 1])
            source_chars.insert(0, 'Extra notes in seq2')
            j -= 1

    return max_score, alignment1_chars, alignment2_chars, source_chars


def sliding():
    sliding_list = []
    for i, s in enumerate(sources):
        if s == 'Mismatch':
            if ord(alignment1_chars[i+1]) == ord(alignment2_chars[i+1]) and abs(int(ord(alignment1_chars[i]))-int(ord(alignment2_chars[i]))) <= 2:
                sliding_list.append("Sliding1")
            else:
                sliding_list.append(s)
        elif s == "Gap in seq2" or s == "Gap in seq1":
            if abs(int(ord(alignment2_chars[i]))-int(ord(alignment2_chars[i+1]))) <= 2:
                sliding_list.append("Sliding")
            else:
                sliding_list.append(s)
        else:
            sliding_list.append(s)
    print("-----------------------")
    print(sliding_list)

    return sliding_list

max_score, alignment1_chars, alignment2_chars, sources = smith_waterman(string_sequences1, string_sequences2)