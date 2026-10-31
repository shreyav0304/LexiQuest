"""WordNet retrieval and quiz-generation helpers for LexiQuest."""

from __future__ import annotations

import random
from functools import lru_cache
from itertools import islice
from typing import Any, Iterable

from nltk.corpus import wordnet as wn

# Beginner-friendly seeds bound the work: quiz generation never walks the full
# production WordNet corpus. All answers still come from actual lexical data.
QUIZ_WORDS = tuple("""happy sad glad angry calm quiet loud bright dark light heavy
hot cold warm cool big small large little long short tall deep shallow wide narrow
good bad kind cruel brave afraid strong weak rich poor clean dirty full empty
early late fast slow young old new fresh stale easy hard simple difficult soft
rough smooth sweet bitter wet dry open closed safe dangerous true false right
wrong high low near far first last alive dead awake asleep busy idle active lazy
beautiful ugly clever foolish honest dishonest polite rude patient curious
clear cloudy modern ancient common rare generous selfish careful careless
comfortable lonely friendly free healthy ill possible impossible useful useless
accept reject agree disagree arrive depart begin end buy sell come go give take
love hate laugh cry win lose remember forget rise fall include exclude
build destroy push pull find search speak talk walk run read write learn teach
help assist work play enjoy admire create make start finish increase decrease
friend enemy child student teacher book home house car road water food bird dog cat
answer question idea story word language meaning success failure peace war hope fear""".split())


@lru_cache(maxsize=512)
def _real_synsets(word: str) -> tuple:
    # Lookup failures raise rather than being cached, so on-demand corpus setup
    # can immediately recover without restarting the app.
    return tuple(wn.synsets(word))


def normalize_word(word: str) -> str:
    """Return a trimmed, lower-case lookup word."""
    return " ".join(word.strip().lower().split())


def _wordnet_available() -> bool:
    try:
        _real_synsets("example")
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
    key = normalized.replace(" ", "_")
    return _real_synsets(key) if corpus is wn else corpus.synsets(key)


def get_synonyms(word: str, corpus: Any = wn) -> list[str]:
    """Retrieve distinct lemma names related to *word* by WordNet synsets."""
    if corpus is wn and not _wordnet_available():
        return []
    normalized = normalize_word(word)
    related = []
    for synset in _synsets(normalized, corpus):
        related.extend(lemma.name() for lemma in synset.lemmas())
    return [item for item in _unique_sorted(related) if item != normalized]


def get_antonyms(word: str, corpus: Any = wn) -> list[str]:
    """Retrieve direct antonym lemma names recorded by WordNet."""
    if corpus is wn and not _wordnet_available():
        return []
    normalized = normalize_word(word)
    related = []
    for synset in _synsets(normalized, corpus):
        for lemma in synset.lemmas():
            related.extend(antonym.name() for antonym in lemma.antonyms())
    return [item for item in _unique_sorted(related) if item != normalized]


def get_definitions(word: str, corpus: Any = wn) -> list[str]:
    """Retrieve distinct definitions from WordNet."""
    if corpus is wn and not _wordnet_available():
        return []
    return list(dict.fromkeys(synset.definition() for synset in _synsets(word, corpus)))


def get_examples(word: str, corpus: Any = wn) -> list[str]:
    """Retrieve distinct example sentences from WordNet."""
    if corpus is wn and not _wordnet_available():
        return []
    examples = (example for synset in _synsets(word, corpus) for example in synset.examples())
    return list(dict.fromkeys(examples))


def get_parts_of_speech(word: str, corpus: Any = wn) -> list[str]:
    """Retrieve the parts of speech represented by the word's synsets."""
    if corpus is wn and not _wordnet_available():
        return []
    return sorted({synset.pos() for synset in _synsets(word, corpus)})


def wordnet_status(corpus: Any = wn) -> tuple[bool, str]:
    """Return a user-friendly status for the local WordNet corpus."""
    try:
        _synsets("example", corpus)
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


@lru_cache(maxsize=2)
def _real_question_pool(quiz_type):
    """Cache immutable lexical templates, never a user's shuffled quiz."""
    templates = []
    retrieve = get_synonyms if quiz_type == "synonym" else get_antonyms
    for word in QUIZ_WORDS:
        related = frozenset(retrieve(word, wn))
        if not related:
            continue
        for synset in _synsets(word, wn):
            lemmas = _unique_sorted(lemma.name() for lemma in synset.lemmas())
            if word not in lemmas:
                continue
            answers = tuple(answer for answer in _unique_sorted(_relationship_candidates(quiz_type, synset)) if answer != word)
            if answers:
                templates.append((word, synset.definition(), answers, related))
    return tuple(templates)


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
    if quiz_type not in {"synonym", "antonym"} or num_questions <= 0 or max_options < 2:
        return []
    if corpus is wn and not _wordnet_available():
        return []
    randomizer = rng or random.Random()
    questions: list[dict[str, Any]] = []
    used_words: set[str] = set()
    if corpus is wn:
        templates = list(_real_question_pool(quiz_type))
        vocabulary = list(QUIZ_WORDS)
    else:
        # Injected/custom corpora have a bounded scan too. This path remains
        # deterministic under the supplied RNG and easy to test without data.
        synsets = list(islice(corpus.all_synsets(), 2000))
        vocabulary = _unique_sorted(lemma.name() for synset in synsets for lemma in synset.lemmas())
        templates = []
        for synset in synsets:
            lemmas = _unique_sorted(lemma.name() for lemma in synset.lemmas())
            if not lemmas:
                continue
            word = lemmas[0]
            answers = tuple(answer for answer in _unique_sorted(_relationship_candidates(quiz_type, synset)) if answer != word)
            related = frozenset(get_synonyms(word, corpus) if quiz_type == "synonym" else get_antonyms(word, corpus))
            if answers:
                templates.append((word, synset.definition(), answers, related))
    randomizer.shuffle(templates)

    for source_word, definition, correct_candidates, related in templates:
        if len(questions) >= num_questions:
            break
        if source_word in used_words:
            continue
        answer = randomizer.choice(correct_candidates)
        eligible = [candidate for candidate in vocabulary if candidate not in {source_word, answer} and candidate not in related]
        distractors = randomizer.sample(eligible, min(max_options - 1, len(eligible)))
        options = [answer, *distractors]
        if len(options) < 2:
            continue
        randomizer.shuffle(options)
        questions.append(
            {
                "word": source_word,
                "question": f"Which word is a {quiz_type} of '{source_word}' (sense: {definition})?",
                "options": options,
                "answer": answer,
                "explanation": f"WordNet records '{answer}' as a {quiz_type} for this sense of '{source_word}': {definition}.",
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

