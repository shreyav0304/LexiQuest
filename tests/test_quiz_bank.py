import random
from content import SYLLABUS, TOPIC_GUIDES
from quiz_bank import syllabus_questions


def test_all_topics_have_structurally_complete_mcqs():
    questions = syllabus_questions(count=100, rng=random.Random(1))
    assert len(questions) == 39
    assert {question["topic"] for question in questions} == set(TOPIC_GUIDES)
    for question in questions:
        assert len(set(question["options"])) == 4
        assert question["options"].count(question["answer"]) == 1
        assert question["explanation"]


def test_filter_limits_and_randomization():
    for module in SYLLABUS:
        questions = syllabus_questions(module["module"], 100)
        assert {q["topic"] for q in questions} == set(module["topics"])
    assert syllabus_questions(count=0) == []
    assert syllabus_questions("invalid") == []
    first = syllabus_questions(count=5, rng=random.Random(1))
    assert first == syllabus_questions(count=5, rng=random.Random(1))
    assert first != syllabus_questions(count=5, rng=random.Random(2))
