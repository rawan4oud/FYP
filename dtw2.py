import numpy as np
from fastdtw import fastdtw
from ngrams_preprocessing import string_sequences1, string_sequences2


# Create a set of unique elements in both sequences
unique_elements = set(string_sequences1 + string_sequences2)

# Create a mapping from elements to numerical values
element_to_index = {element: index for index, element in enumerate(unique_elements)}

# Convert sequences to numerical format using one-hot encoding
seq1_numeric = np.array([[1 if element == char else 0 for char in unique_elements] for element in string_sequences1])
seq2_numeric = np.array([[1 if element == char else 0 for char in unique_elements] for element in string_sequences2])

# Perform DTW
distance, path = fastdtw(seq1_numeric, seq2_numeric)

# Retrieve aligned sequences
aligned_seq1 = [string_sequences1[i] for i, _ in path]
aligned_seq2 = [string_sequences2[j] for _, j in path]


print(string_sequences1)
print(string_sequences2)
print("__________")
print("Length:", len(aligned_seq1), "Aligned seq1:", aligned_seq1)
print("Length:", len(aligned_seq2), "Aligned seq2:", aligned_seq2)


