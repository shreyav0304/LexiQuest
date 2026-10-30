from content import (
    SYLLABUS,
    TOPIC_GUIDES,
    ngram_counts,
    ngram_probability,
    rank_documents,
    regex_matches,
    search_content,
    update_progress,
)


def test_every_syllabus_topic_has_complete_guide():
    required = {
        "definition", "intuitive_explanation", "step_by_step", "example",
        "calculation", "diagram",
        "terminology", "common_mistakes", "exam_tip", "revision",
        "practice_questions", "model_answer_5", "model_answer_10",
    }
    topics = [topic for item in SYLLABUS for topic in item["topics"]]
    assert set(TOPIC_GUIDES) == set(topics)
    for topic in topics:
        guide = TOPIC_GUIDES[topic]
        assert required <= set(guide)
        assert len(guide["practice_questions"]) == 3
        assert all({"question", "answer", "explanation"} <= set(question) for question in guide["practice_questions"])


def test_search_ranks_matching_topic():
    results = search_content("TF-IDF ranking")
    assert results
    assert results[0]["topic"] == "Information Retrieval"


def test_progress_is_immutable_and_accumulates():
    original = {"activities": {"quizzes": 2}, "total_actions": 2}
    updated = update_progress(original, "quizzes")
    assert original["activities"]["quizzes"] == 2
    assert updated["activities"]["quizzes"] == 3
    assert updated["total_actions"] == 3


def test_ngram_counts_and_probability():
    assert ngram_counts("one fish, two fish", 2)[("fish", "two")] == 1
    assert ngram_probability("one fish, two fish", "fish two", 2) == 1 / 3


def test_regex_and_ir_ranking():
    assert regex_matches(r"\d+", "a12 b3") == ("12", "3")
    ranked = rank_documents("retrieval", ["WordNet stores words.", "Retrieval ranks results."])
    assert ranked[0][2].startswith("Retrieval")


def test_lessons_are_specific_and_evaluation_domains_are_distinct():
    assert len(TOPIC_GUIDES) == 39
    assert len({guide["definition"] for guide in TOPIC_GUIDES.values()}) == 39
    assert "precision=6/10" in TOPIC_GUIDES["Evaluation of the IR System"]["example"]
    assert "modified unigram precision=2/4" in TOPIC_GUIDES["MT Evaluation"]["example"]
    assert "perplexity" in TOPIC_GUIDES["Evaluating Large Language Models"]["example"]
    assert "karana" in TOPIC_GUIDES["Karaka theory"]["example"]
    assert "0.12" in TOPIC_GUIDES["Probabilistic Parsing"]["example"]
    for guide in TOPIC_GUIDES.values():
        assert "foundational concept" not in guide["definition"]
        assert "classroom example of" not in guide["example"]


def test_supplied_syllabus_references_and_course_metadata():
    from content import COURSE, TEXTBOOKS

    assert COURSE["code"] == "AI401"
    assert COURSE["contact_hours"] == sum(module["hours"] for module in SYLLABUS) == 40
    assert [len(module["topics"]) for module in SYLLABUS] == [11, 12, 6, 6, 4]
    assert [module["textbook_chapters"] for module in SYLLABUS] == [
        ["Textbook 1 — Chapter 1: Sections 1.1–1.9", "Textbook 1 — Chapter 2: Sections 2.1–2.3"],
        ["Textbook 1 — Chapter 3: Sections 3.1–3.7", "Textbook 1 — Chapter 4: Sections 4.1–4.6"],
        ["Textbook 1 — Chapter 9: Sections 9.1–9.7"],
        ["Textbook 2 — Chapter 13: Sections 13.1–13.7"],
        ["Textbook 2 — Chapter 10: Sections 10.1–10.6"],
    ]
    assert SYLLABUS[4]["rbt_levels"] == ["L1", "L2"]
    assert all(module["rbt_levels"] == ["L1", "L2", "L3"] for module in SYLLABUS[:4])
    assert "Siddiqui" in TEXTBOOKS[1] and "2023" in TEXTBOOKS[2]
