from preprocessing import main
from nltk import ngrams

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

def compute_similarity_matrix(string_sequences1, string_sequences2, n):
    # Compute similarity matrix
    similarity_matrix = []

    for i, sequence1 in enumerate(string_sequences1):
        row = []
        for j, sequence2 in enumerate(string_sequences2):
            similarity = compute_ngram_similarity(sequence1, sequence2, n)
            row.append(similarity)
        similarity_matrix.append(row)

    return similarity_matrix

if __name__ == "__main__":
    midi_file_path1 = "Star Wars - The Imperial March [MIDIfind.com].mid"
    midi_file_path2 = "Queen - Bohemian Rhapsody.mid"
    midi_file_path3 = "Star Wars - The Imperial March [MIDIfind.com].mid"
    string_sequences1 = main(midi_file_path1)
    string_sequences2 = main(midi_file_path2)
    string_sequences3 = main(midi_file_path3)

    strings1 = ["ABCDGH", "XYZ", "123"]
    strings2 = ["ABCDGH", "XYZ", "123"]
    n = 3  # Adjust the value of n for different n-grams

    matrix = compute_similarity_matrix(string_sequences1, string_sequences2, 3)

    # Print or use the similarity matrix as needed
    # for i, row in enumerate(matrix):
    #     print(f"Track {i + 1} Similarity Values: {row}\n")

counter = 0
diagonal = []
for i, row in enumerate(matrix):
        formatted_row = ["{:.2f}".format(value) for value in row]
        diagonal.append(row[i])
        if row[i]>0.7:
            counter += 1
        # print(formatted_row)
print(f"\nDiagonal Values: {diagonal}")
print(f"Number of Diagonal Values greater than 0.7: {counter}/{len(diagonal)}")
