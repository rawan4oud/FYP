def compute_lps_array(pattern):
    m = len(pattern)
    lps = [0] * m
    j = 0

    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]

        if pattern[i] == pattern[j]:
            j += 1

        lps[i] = j

    return lps

def kmp_lcs(string1, string2):
    n, m = len(string1), len(string2)
    lps_table = compute_lps_array(string2)
    lcs_lengths = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if string1[i - 1] == string2[j - 1]:
                lcs_lengths[i][j] = lcs_lengths[i - 1][j - 1] + 1
            else:
                lcs_lengths[i][j] = max(lcs_lengths[i - 1][j], lcs_lengths[i][j - 1])

    return lcs_lengths[n][m]

def compute_similarity_matrix(strings1, strings2):
    # Compute similarity matrix
    similarity_matrix = []

    for i, sequence1 in enumerate(strings1):
        row = []
        for j, sequence2 in enumerate(strings2):
            lcs_length = kmp_lcs(sequence1, sequence2)
            similarity = lcs_length / max(len(sequence1), len(sequence2))
            row.append(similarity)
        similarity_matrix.append(row)

    return similarity_matrix

if __name__ == "__main__":
    # Example usage:
    strings1 = ["ABCDGH", "XYZ", "123"]
    strings2 = ["ABCDGH", "XYZ", "123"]


    matrix = compute_similarity_matrix(strings1, strings2)

    # Print or use the similarity matrix as needed
    for i, row in enumerate(matrix):
        print(f"String {i + 1} Similarity Values: {row}")
