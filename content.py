"""Local syllabus and study logic for LexiQuest.

The content is deliberately data-first so the Streamlit UI can render it in
several places without duplicating teaching notes.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any, Iterable

COURSE = {
    "title": "Natural Language Processing",
    "code": "AI401",
    "semester": "VII",
    "department": "AIML",
    "credits": 3,
    "contact_hours": 40,
    "weekly_contact_hours": "3:0:0 (L:T:P)",
    "cia_marks": 50,
    "see_marks": 50,
    "total_marks": 100,
    "exam_duration": "3 Hours",
    "source": "User-provided two-page syllabus image, supplied 9 October 2026",
}

TEXTBOOKS = {
    1: 'Tanveer Siddiqui, U.S. Tiwary, "Natural Language Processing and Information Retrieval", Oxford University Press.',
    2: 'Daniel Jurafsky, James H. Martin, "Speech and Language Processing. An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition", Pearson Education, 2023.',
}

SYLLABUS: tuple[dict[str, Any], ...] = (
    {
        "module": "Module 1 Introduction to NLP",
        "topic": "Introduction to NLP",
        "summary": "The scope, history, applications, and challenges of Natural Language Processing.",
        "topics": ["What is Natural Language Processing?", "Origins of NLP", "Language and Knowledge", "Challenges of NLP", "Language and Grammar", "Processing Indian Languages", "NLP Applications", "Statistical Language Modelling", "N-gram model: unigram and bigram", "Paninian Framework", "Karaka theory"],
        "textbook_chapters": ["Textbook 1 — Chapter 1: Sections 1.1–1.9", "Textbook 1 — Chapter 2: Sections 2.1–2.3"],
        "notes": [
            "Natural Language Processing (NLP) combines linguistics and computing to work with text and speech.",
            "A pipeline commonly moves from raw text to tokens, features, a model or search step, and an interpretable result.",
            "Ambiguity is central: one spelling can have several meanings, and context helps select the intended sense.",
        ],
        "keywords": ["nlp", "language", "pipeline", "ambiguity", "linguistics", "introduction"],
    },
    {
        "module": "Module 2 Word Level and Syntactic Analysis",
        "topic": "Word Level and Syntactic Analysis",
        "summary": "Tokenization, morphology, tagging, parsing, and grammatical structure.",
        "topics": ["Word Level Analysis: Introduction", "Regular Expressions", "Finite-State Automata", "Morphological Parsing", "Spelling Error Detection and Correction", "Words and Word Classes", "Part-of-Speech Tagging", "Syntactic Analysis: Introduction", "Context-Free Grammar", "Constituency", "Parsing", "Probabilistic Parsing"],
        "textbook_chapters": ["Textbook 1 — Chapter 3: Sections 3.1–3.7", "Textbook 1 — Chapter 4: Sections 4.1–4.6"],
        "notes": [
            "Tokenization splits text into useful units; normalization makes comparable forms consistent.",
            "Stop-word removal can reduce noise, but should be used carefully when small words carry meaning.",
            "Stemming trims word endings roughly, while lemmatization uses vocabulary and grammar to find a base form.",
        ],
        "keywords": ["tokenization", "normalization", "stop words", "stemming", "lemmatization", "syntax", "parsing"],
    },
    {
        "module": "Module 3 Information Retrieval",
        "topic": "Information Retrieval",
        "summary": "Indexing, searching, ranking, and evaluating relevant documents.",
        "topics": ["Introduction to Information Retrieval", "Design Features of Information Retrieval Systems", "Information Retrieval Models: Classical models", "Information Retrieval Models: Non-classical models", "Information Retrieval Models: Alternative models", "Evaluation of the IR System"],
        "textbook_chapters": ["Textbook 1 — Chapter 9: Sections 9.1–9.7"],
        "notes": [
            "An inverted index maps terms to documents so a query can be answered without scanning every word in every document.",
            "TF-IDF combines term frequency with inverse document frequency to reward distinctive query terms.",
            "Precision measures the quality of retrieved results; recall measures coverage of the relevant collection.",
        ],
        "keywords": ["information retrieval", "ir", "indexing", "tf-idf", "ranking", "precision", "recall"],
    },
    {
        "module": "Module 4 Machine Translation",
        "topic": "Machine Translation",
        "summary": "Translating text between languages with statistical and neural approaches.",
        "topics": ["Language Divergences and Typology", "Machine Translation using Encoder–Decoder", "Details of the Encoder–Decoder Model", "Translating in Low-Resource Situations", "MT Evaluation", "Bias and Ethical Issues"],
        "textbook_chapters": ["Textbook 2 — Chapter 13: Sections 13.1–13.7"],
        "notes": [
            "Machine translation must handle word order, ambiguity, idioms, and differences in grammatical structure.",
            "Statistical systems learn translation probabilities from aligned bilingual text.",
            "Neural systems generate translations with encoder-decoder models; BLEU is one automatic evaluation measure.",
        ],
        "keywords": ["machine translation", "translation", "alignment", "statistical", "neural", "bleu"],
    },
    {
        "module": "Module 5 Large Language Models",
        "topic": "Large Language Models",
        "summary": "Transformer-based language models, pretraining, prompting, and responsible use.",
        "topics": ["Large Language Models with Transformers", "Sampling for LLM Generation", "Pretraining Large Language Models", "Evaluating Large Language Models"],
        "textbook_chapters": ["Textbook 2 — Chapter 10: Sections 10.1–10.6"],
        "notes": [
            "Large language models learn statistical patterns from very large text collections and generate likely continuations.",
            "Transformer attention lets a model relate tokens across a context window; pretraining is followed by adaptation or prompting.",
            "Good evaluation includes factuality, bias, robustness, privacy, and safety—not only fluent wording.",
        ],
        "keywords": ["large language models", "llm", "transformer", "attention", "pretraining", "prompting"],
    },
)

for _index, _module in enumerate(SYLLABUS):
    _module["hours"] = 8
    _module["rbt_levels"] = ["L1", "L2"] if _index == 4 else ["L1", "L2", "L3"]


from lessons import LESSONS, build_guide

_SYLLABUS_TOPICS = [topic for module in SYLLABUS for topic in module["topics"]]
if len(LESSONS) != len(_SYLLABUS_TOPICS):
    raise ValueError("Every syllabus topic must have an authored lesson")
TOPIC_GUIDES = {
    topic: build_guide(topic, lesson)
    for topic, lesson in zip(_SYLLABUS_TOPICS, LESSONS)
}


def get_topic_guide(topic: str) -> dict[str, Any]:
    """Return a topic guide, or an empty mapping for an unknown topic."""
    return TOPIC_GUIDES.get(topic, {})


def syllabus_items() -> list[dict[str, Any]]:
    """Return a copy suitable for UI code and callers."""
    return [
        dict(
            item,
            notes=list(item["notes"]),
            keywords=list(item["keywords"]),
            topics=list(item["topics"]),
            textbook_chapters=list(item["textbook_chapters"]),
            topic_guides={topic: dict(TOPIC_GUIDES[topic]) for topic in item["topics"]},
        )
        for item in SYLLABUS
    ]


def search_content(query: str, items: Iterable[dict[str, Any]] = SYLLABUS) -> list[dict[str, Any]]:
    """Rank local syllabus entries by simple term overlap.

    Search is intentionally deterministic and offline. Exact phrase matches
    receive a small boost, then results are ordered by score and syllabus order.
    """
    terms = re.findall(r"[a-z0-9]+", query.lower())
    if not terms:
        return []
    phrase = " ".join(terms)
    scored: list[tuple[int, int, dict[str, Any]]] = []
    for index, item in enumerate(items):
        haystack = " ".join(
            [item.get("module", ""), item.get("topic", ""), item.get("summary", ""),
             *item.get("keywords", []), *item.get("topics", []),
             *item.get("textbook_chapters", []), *item.get("notes", [])]
        ).lower()
        score = sum(haystack.count(term) for term in terms)
        if phrase in haystack:
            score += 2
        if score:
            scored.append((score, -index, item))
    return [item for _, _, item in sorted(scored, key=lambda row: (-row[0], row[1]))]


def update_progress(progress: dict[str, Any], activity: str, amount: int = 1) -> dict[str, Any]:
    """Return updated progress without mutating the supplied mapping."""
    result = dict(progress)
    result["activities"] = dict(result.get("activities", {}))
    result["activities"][activity] = result["activities"].get(activity, 0) + max(0, amount)
    result["total_actions"] = sum(result["activities"].values())
    return result


def ngram_counts(text: str, n: int) -> Counter[tuple[str, ...]]:
    """Count word n-grams using a small, punctuation-tolerant tokenizer."""
    if n < 1:
        raise ValueError("n must be at least 1")
    tokens = re.findall(r"[A-Za-z0-9']+", text.lower())
    return Counter(tuple(tokens[index:index + n]) for index in range(len(tokens) - n + 1))


def ngram_probability(text: str, ngram: str, n: int, smoothing: float = 0.0) -> float:
    """Estimate an n-gram probability, optionally with add-k smoothing."""
    target = tuple(re.findall(r"[A-Za-z0-9']+", ngram.lower()))
    if len(target) != n:
        raise ValueError(f"Expected {n} tokens in the n-gram")
    counts = ngram_counts(text, n)
    denominator = sum(counts.values())
    vocabulary = len(set(re.findall(r"[A-Za-z0-9']+", text.lower())))
    if denominator == 0:
        return 0.0
    if smoothing:
        if smoothing < 0:
            raise ValueError("smoothing must be non-negative")
        return (counts[target] + smoothing) / (denominator + smoothing * max(vocabulary ** n, 1))
    return counts[target] / denominator


def regex_matches(pattern: str, text: str) -> tuple[str, ...]:
    """Return matching snippets while turning invalid patterns into a clear error."""
    try:
        return tuple(match.group(0) for match in re.finditer(pattern, text))
    except re.error as exc:
        raise ValueError(f"Invalid regular expression: {exc}") from exc


def rank_documents(query: str, documents: Iterable[str]) -> list[tuple[int, float, str]]:
    """Rank local documents using a compact TF-IDF cosine-like score."""
    query_terms = Counter(re.findall(r"[a-z0-9]+", query.lower()))
    docs = list(documents)
    if not query_terms:
        return [(index, 0.0, doc) for index, doc in enumerate(docs)]
    tokenized = [Counter(re.findall(r"[a-z0-9]+", doc.lower())) for doc in docs]
    total = len(docs)
    scores: list[tuple[int, float, str]] = []
    for index, (doc, counts) in enumerate(zip(docs, tokenized)):
        score = 0.0
        for term, query_weight in query_terms.items():
            if counts[term]:
                idf = math.log((total + 1) / (sum(term in item for item in tokenized) + 1)) + 1
                score += query_weight * counts[term] * idf
        scores.append((index, score, doc))
    return sorted(scores, key=lambda row: (-row[1], row[0]))
