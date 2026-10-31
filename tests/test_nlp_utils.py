import random

import pytest

from nlp_utils import (
    calculate_score,
    generate_quiz_questions,
    get_antonyms,
    get_synonyms,
    normalize_word,
)


class FakeLemma:
    def __init__(self, name, antonyms=()):
        self._name = name
        self._antonyms = [FakeLemma(item) for item in antonyms]

    def name(self):
        return self._name

    def antonyms(self):
        return self._antonyms


class FakeSynset:
    def __init__(self, words, antonyms=()):
        self._lemmas = [FakeLemma(word, antonyms if index == 0 else ()) for index, word in enumerate(words)]

    def lemmas(self):
        return self._lemmas

    def definition(self):
        return "A test definition."

    def examples(self):
        return []

    def pos(self):
        return "n"


class FakeCorpus:
    def __init__(self):
        self.items = [
            FakeSynset(["happy", "glad"], ["sad"]),
            FakeSynset(["sad", "unhappy"], ["happy"]),
            FakeSynset(["bright", "shiny"]),
        ]

    def synsets(self, word):
        return [item for item in self.items if word in [lemma.name() for lemma in item.lemmas()]]

    def all_synsets(self):
        return iter(self.items)


@pytest.fixture
def corpus():
    return FakeCorpus()


def test_normalize_word():
    assert normalize_word("  Happy   ") == "happy"


def test_synonyms_remove_duplicates(corpus):
    assert get_synonyms("HAPPY", corpus) == ["glad"]


def test_antonyms(corpus):
    assert get_antonyms("happy", corpus) == ["sad"]


def test_missing_word_returns_empty(corpus):
    assert get_synonyms("unknown", corpus) == []


def test_synonym_quiz_has_correct_answer(corpus):
    questions = generate_quiz_questions("synonym", 1, corpus, random.Random(2))
    assert len(questions) == 1
    assert questions[0]["answer"] in questions[0]["options"]


def test_antonym_quiz_has_correct_answer(corpus):
    questions = generate_quiz_questions("antonym", 1, corpus, random.Random(2))
    assert len(questions) == 1
    assert questions[0]["answer"] in questions[0]["options"]


def test_invalid_quiz_type_and_insufficient_data(corpus):
    assert generate_quiz_questions("homonym", 5, corpus) == []


def test_score_calculation():
    questions = [{"answer": "glad"}, {"answer": "sad"}]
    assert calculate_score(questions, {0: "glad", 1: "wrong"}) == 1
    assert calculate_score(questions, {0: "glad", 1: "sad"}) == 2


def test_quiz_distractors_are_not_other_valid_relationships(corpus):
    corpus.items[0] = FakeSynset(["happy", "glad", "cheerful"], ["sad"])
    for kind, retrieve in [("synonym", get_synonyms), ("antonym", get_antonyms)]:
        questions = generate_quiz_questions(kind, 5, corpus, random.Random(2))
        assert questions
        for question in questions:
            distractors = set(question["options"]) - {question["answer"]}
            assert distractors.isdisjoint(retrieve(question["word"], corpus))
            assert "sense:" in question["question"]
            assert question["answer"] in question["explanation"]


def test_real_quiz_path_never_scans_corpus_and_reuses_templates(monkeypatch, corpus):
    import nlp_utils
    calls = []
    original_lookup = corpus.synsets
    def lookup(word):
        calls.append(word)
        return original_lookup(word)
    monkeypatch.setattr(corpus, "synsets", lookup)
    monkeypatch.setattr(corpus, "all_synsets", lambda: (_ for _ in ()).throw(AssertionError("Full corpus scan")))
    monkeypatch.setattr(nlp_utils, "wn", corpus)
    monkeypatch.setattr(nlp_utils, "QUIZ_WORDS", ("happy", "glad", "sad", "bright", "shiny"))
    monkeypatch.setattr(nlp_utils, "_real_synsets", lambda word: tuple(corpus.synsets(word)))
    nlp_utils._real_question_pool.cache_clear()
    try:
        first = generate_quiz_questions("synonym", 2, corpus, random.Random(1))
        assert first
        pool_calls = len([word for word in calls if word != "example"])
        second = generate_quiz_questions("synonym", 2, corpus, random.Random(2))
        assert second
        assert len([word for word in calls if word != "example"]) == pool_calls
        first[0]["options"].clear()
        assert all(len(q["options"]) >= 2 for q in second)
    finally:
        nlp_utils._real_question_pool.cache_clear()

