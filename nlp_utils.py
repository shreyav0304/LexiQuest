"""WordNet retrieval and quiz-generation helpers for LexiQuest."""

from __future__ import annotations

import random
from typing import Any, Callable, Iterable

from nltk.corpus import wordnet as wn
from nltk.corpus.reader import WordNetCorpusReader


def normalize_word(word: str) -> str:
    """Return a trimmed, lower-case lookup word."""
    return " ".join(word.strip().lower().split())


def _wordnet_available() -> bool:
    try:
        wn.synsets("example")
        return True
    except LookupError:
        return False


def _unique_sorted(words: Iterable[str]) -> list[str]:
    cleaned = {word.replace("_", " ").strip().lower() for word in words if word.strip()}
    return sorted(cleaned)


def _synsets(word: str, corpus: Any = wn) -> list[Any]:
    normalized = normalize_word(word)
    if not normalized:
        return []
    return corpus.synsets(normalized.replace(" ", "_"))


def get_synonyms(word: str, corpus: Any = wn) -> list[str]:
    """Retrieve distinct lemma names related to *word* by WordNet synsets."""
    if not _wordnet_available() and corpus is wn:
        return []
    normalized = normalize_word(word)
    related = []
    for synset in _synsets(normalized, corpus):
        related.extend(lemma.name() for lemma in synset.lemmas())
    return [item for item in _unique_sorted(related) if item != normalized]


def get_antonyms(word: str, corpus: Any = wn) -> list[str]:
    """Retrieve direct antonym lemma names recorded by WordNet."""
    if not _wordnet_available() and corpus is wn:
        return []
    normalized = normalize_word(word)
    related = []
    for synset in _synsets(normalized, corpus):
        for lemma in synset.lemmas():
            related.extend(antonym.name() for antonym in lemma.antonyms())
    return [item for item in _unique_sorted(related) if item != normalized]


def get_definitions(word: str, corpus: Any = wn) -> list[str]:
    """Retrieve distinct definitions from WordNet."""
    if not _wordnet_available() and corpus is wn:
        return []
    return list(dict.fromkeys(synset.definition() for synset in _synsets(word, corpus)))


def get_examples(word: str, corpus: Any = wn) -> list[str]:
    """Retrieve distinct example sentences from WordNet."""
    if not _wordnet_available() and corpus is wn:
        return []
    examples = (example for synset in _synsets(word, corpus) for example in synset.examples())
    return list(dict.fromkeys(examples))


def get_parts_of_speech(word: str, corpus: Any = wn) -> list[str]:
    """Retrieve the parts of speech represented by the word's synsets."""
    if not _wordnet_available() and corpus is wn:
        return []
    return sorted({synset.pos() for synset in _synsets(word, corpus)})


def wordnet_status(corpus: Any = wn) -> tuple[bool, str]:
    """Return a user-friendly status for the local WordNet corpus."""
    try:
        corpus.synsets("example")
    except LookupError:
        return False, "WordNet data is not installed. Run: python setup_nltk.py"
    return True, "WordNet is ready."


def _relationship_candidates(
    quiz_type: str,
    source_synset: Any,
) -> list[str]:
    if quiz_type == "synonym":
        return [lemma.name().replace("_", " ") for lemma in source_synset.lemmas()]
    if quiz_type == "antonym":
        return [
            antonym.name().replace("_", " ")
            for lemma in source_synset.lemmas()
            for antonym in lemma.antonyms()
        ]
    return []


def generate_quiz_questions(
    quiz_type: str,
    num_questions: int = 5,
    corpus: Any = wn,
    rng: random.Random | None = None,
    max_options: int = 4,
) -> list[dict[str, Any]]:
    """Generate questions from WordNet relationships.

    Each question contains ``word``, ``question``, ``options``, and ``answer``.
    The optional corpus and random generator make the function easy to test.
    """
    if quiz_type not in {"synonym", "antonym"} or num_questions <= 0:
        return []
    if corpus is wn and not _wordnet_available():
        return []
    randomizer = rng or random.Random()
    questions: list[dict[str, Any]] = []
    used_words: set[str] = set()
    all_synsets = list(corpus.all_synsets())
    randomizer.shuffle(all_synsets)

    for source_synset in all_synsets:
        if len(questions) >= num_questions:
            break
        source_lemmas = _unique_sorted(lemma.name() for lemma in source_synset.lemmas())
        if not source_lemmas:
            continue
        source_word = source_lemmas[0]
        correct_candidates = _unique_sorted(_relationship_candidates(quiz_type, source_synset))
        correct_candidates = [item for item in correct_candidates if item != source_word]
        if not correct_candidates or source_word in used_words:
            continue
        answer = correct_candidates[0]

        # Avoid using another valid relationship as a supposedly wrong option,
        # including relationships belonging to other senses of the source word.
        related = set(get_synonyms(source_word, corpus) if quiz_type == "synonym"
                      else get_antonyms(source_word, corpus))

        distractors: list[str] = []
        for candidate_synset in all_synsets:
            candidate_words = _unique_sorted(
                lemma.name() for lemma in candidate_synset.lemmas()
            )
            for candidate in candidate_words:
                if candidate not in {source_word, answer} and candidate not in related and candidate not in distractors:
                    distractors.append(candidate)
                if len(distractors) >= max_options - 1:
                    break
            if len(distractors) >= max_options - 1:
                break
        options = _unique_sorted([answer, *distractors])[:max_options]
        if answer not in options or len(options) < 2:
            continue
        randomizer.shuffle(options)
        questions.append(
            {
                "word": source_word,
                "question": f"Which word is a {quiz_type} of '{source_word}' (sense: {source_synset.definition()})?",
                "options": options,
                "answer": answer,
                "explanation": f"WordNet records '{answer}' as a {quiz_type} for this sense of '{source_word}': {source_synset.definition()}.",
            }
        )
        used_words.add(source_word)
    return questions


def calculate_score(questions: list[dict[str, Any]], answers: dict[int, str]) -> int:
    """Count answers that exactly match each question's stored answer."""
    return sum(
        1
        for index, question in enumerate(questions)
        if answers.get(index) == question.get("answer")
    )

