r"""Verify local quiz and WordNet features while outgoing socket connections fail.

Run after initial dependency/corpus setup: .venv\Scripts\python.exe offline_check.py
This checks application logic; it does not emulate an offline web browser.
"""

from pathlib import Path
from unittest.mock import patch
import sys


def check():
    with patch("socket.socket.connect", side_effect=OSError("Network disabled for offline check")):
        import nltk
        nltk.data.path = [str(Path(__file__).resolve().parent / "nltk_data")]
        from content import SYLLABUS, TOPIC_GUIDES
        from quiz_bank import syllabus_questions
        from nlp_utils import (wordnet_status, get_definitions, get_synonyms,
                               get_antonyms, generate_quiz_questions, calculate_score)
        questions = syllabus_questions(count=100)
        if len(questions) != sum(len(module["topics"]) for module in SYLLABUS):
            raise RuntimeError("Syllabus question coverage is incomplete")
        if calculate_score(questions, {i: q["answer"] for i, q in enumerate(questions)}) != len(questions):
            raise RuntimeError("Quiz scoring failed")
        print(f"PASS: {len(questions)} syllabus questions, scoring and {len(TOPIC_GUIDES)} local study guides")
        ready, _ = wordnet_status()
        if not ready:
            raise RuntimeError("Project-local WordNet missing. While online, run python setup_nltk.py once.")
        if not (get_definitions("happy") and get_synonyms("happy") and get_antonyms("happy")):
            raise RuntimeError("WordNet lookup failed")
        print("PASS: Word Explorer definitions, synonyms and antonyms")
        for kind in ("synonym", "antonym"):
            if not generate_quiz_questions(kind, 5):
                raise RuntimeError(f"No {kind} quiz generated")
            print(f"PASS: {kind} quiz generation")
    print("Offline logic check passed with outgoing socket connections blocked.")


if __name__ == "__main__":
    try:
        check()
    except (ImportError, LookupError, RuntimeError, OSError) as error:
        print(f"Offline check failed: {error}")
        sys.exit(1)
