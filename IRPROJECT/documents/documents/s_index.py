import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup

class HTMLIndexer:
    def __init__(self, directory):
        self.directory = directory
        self.vectorizer = TfidfVectorizer(stop_words='english', token_pattern=r"(?u)\b[a-zA-Z]+\b")
        self.documents = []
        self.filenames = []

    def read_html_files(self):
        """Read HTML files from the directory and extract text."""
        for filename in os.listdir(self.directory):
            if filename.endswith('.html'):
                filepath = os.path.join(self.directory, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    soup = BeautifulSoup(file, 'html.parser')
                    text = soup.get_text()
                    self.documents.append(text)
                    self.filenames.append(filename)
        print(f"Loaded {len(self.documents)} documents.")

    def build_index(self):
        """Build TF-IDF matrix for the documents."""
        self.tfscores = self.vectorizer.fit_transform(self.documents)

    def save_index(self, filepath):
        """Save the TF-IDF vectorizer, matrix, and filenames to a pickle file."""
        with open(filepath, 'wb') as file:
            pickle.dump({
                'vectorizer': self.vectorizer,
                'tfscores': self.tfscores,
                'filenames': self.filenames
            }, file)
        print(f"Index and filenames have been saved to {filepath}")

    def print_terms_with_tfidf_scores(self):
        """Print terms with the documents they appear in and their TF-IDF scores."""
        feature_names = self.vectorizer.get_feature_names_out()
        dense_matrix = self.tfscores.todense()

        for col in range(len(feature_names)):
            term = feature_names[col]
            print(f"Term: {term}")
            for doc_id in range(len(self.filenames)):
                score = dense_matrix[doc_id, col]
                if score > 0:  # Only print if the term appears in the document
                    print(f"\tDocument: {self.filenames[doc_id]}, TF-IDF Score: {score}")

    def print_document_similarities(self):
        """Print each document and the documents it is similar to along with cosine similarity."""
        similarities = cosine_similarity(self.tfscores)
        for idx, doc_similarities in enumerate(similarities):
            print(f"Document: {self.filenames[idx]}")
            for other_idx, sim_score in enumerate(doc_similarities):
                if idx != other_idx and sim_score > 0.1:  # Exclude self and low similarities
                    print(f"\tSimilar to: {self.filenames[other_idx]}, Cosine Similarity: {sim_score}")

if __name__ == "__main__":
    indexer = HTMLIndexer('output')
    indexer.read_html_files()
    indexer.build_index()
    indexer.save_index('index.pickle')
    indexer.print_terms_with_tfidf_scores()
    indexer.print_document_similarities()
