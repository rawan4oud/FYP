import re
import nltk
from nltk import ngrams
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Download the NLTK Punkt tokenizer model
nltk.download('punkt')

# Download NLTK stop words
nltk.download('stopwords')
from nltk.corpus import stopwords

def custom_tokenizer(text):
    # Split the text into tokens using regex, preserving special characters
    tokens = re.findall(r'\b\w+\b|.', text)
    return tokens


# Function to extract N-grams from a string
def extract_ngrams(text, n):
    # Use the custom tokenizer
    tokenized_text = custom_tokenizer(text)
    ngrams_list = list(ngrams(tokenized_text, n))
    return [''.join(gram) for gram in ngrams_list]


# Function to compute similarity between a captured string and a reference string based on N-grams
def compute_similarity(captured_string, reference_string, n):
    captured_ngrams = extract_ngrams(captured_string, n)
    reference_ngrams = extract_ngrams(reference_string, n)

    # Combine the N-grams from both strings
    all_ngrams = captured_ngrams + reference_ngrams

    # Check if all N-grams are empty or contain only stop words
    if all(not ngram for ngram in all_ngrams):
        print(f"Warning: All N-grams are empty or contain only stop words.")
        return 0.0

    # Create a CountVectorizer to convert N-grams into a matrix of token counts
    vectorizer = CountVectorizer(ngram_range=(n, n), tokenizer=custom_tokenizer)
    try:
        ngram_matrix = vectorizer.fit_transform(all_ngrams)
    except ValueError as e:
        print(f"Error: {e}")
        return 0.0

    # Filter out stop words
    stop_words = set(stopwords.words('english'))
    feature_names = vectorizer.get_feature_names_out()
    filtered_feature_names = [word for word in feature_names if word.lower() not in stop_words]

    # Filter the ngram_matrix
    filtered_ngram_matrix = ngram_matrix[:, [vectorizer.vocabulary_[word] for word in filtered_feature_names]]

    # Check if the filtered_ngram_matrix is empty
    if filtered_ngram_matrix.shape[1] == 0:
        print("Warning: After filtering, the N-gram matrix is empty.")
        return 0.0

    # Compute cosine similarity
    similarity = cosine_similarity(filtered_ngram_matrix, filtered_ngram_matrix)[0, 1]
    print(similarity)
    return similarity
    
compute_similarity('ABCDEFG', 'ABCDEFG', 2)
