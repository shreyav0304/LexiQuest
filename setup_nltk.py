"""Prepare a project-local WordNet copy for later offline use."""

from pathlib import Path
import sys
import nltk
from wordnet_setup import install_wordnet


if __name__ == "__main__":
    # Restrict discovery so setup cannot accidentally succeed using a different
    # machine-wide corpus that would be missing when the project is copied.
    nltk.data.path = [str(Path(__file__).resolve().parent / "nltk_data")]
    ready, message = install_wordnet()
    print(message)
    if ready:
        print("Saved in nltk_data/. Word Explorer and vocabulary quizzes can now run offline.")
    sys.exit(0 if ready else 1)
