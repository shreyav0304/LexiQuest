"""Download the WordNet resources required by LexiQuest."""

import nltk


if __name__ == "__main__":
    print("Downloading WordNet data...")
    nltk.download("wordnet")
    nltk.download("omw-1.4")
    print("WordNet setup complete.")

