"""Explicit, on-demand WordNet installation for local and hosted apps."""

from pathlib import Path
import threading
import nltk

_INSTALL_LOCK = threading.Lock()


def install_wordnet():
    """Download English WordNet, then verify a real corpus lookup succeeds.

    Triggered only by the user's setup button, never at application startup.
    NLTK accepts its standard ZIP corpus, so no manual extraction is needed.
    """
    data_dir = str(Path(__file__).resolve().parent / "nltk_data")
    with _INSTALL_LOCK:
        if data_dir not in nltk.data.path:
            nltk.data.path.insert(0, data_dir)
        try:
            nltk.corpus.wordnet.synsets("example")
            return True, "WordNet is ready."
        except LookupError:
            pass
        try:
            downloaded = nltk.download("wordnet", download_dir=data_dir, quiet=True, raise_on_error=True)
            if not downloaded:
                return False, "The download did not complete. Please try again."
            if not nltk.corpus.wordnet.synsets("example"):
                return False, "WordNet downloaded but could not be verified. Please retry."
        except Exception:
            return False, "Could not download WordNet. Check the server's internet connection and try again."
        return True, "WordNet is ready."


def register_wordnet_path():
    """Discover a prior on-demand installation without starting a download."""
    data_dir = str(Path(__file__).resolve().parent / "nltk_data")
    if data_dir not in nltk.data.path:
        nltk.data.path.insert(0, data_dir)
