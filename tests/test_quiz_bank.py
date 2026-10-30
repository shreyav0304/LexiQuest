import random
import pytest
from content import SYLLABUS, TOPIC_GUIDES
from quiz_bank import syllabus_questions
from quiz_bank import result_feedback


@pytest.mark.parametrize("score,total,expected", [
    (5, 5, "Perfect score"), (4, 5, "Great work"),
    (3, 5, "Nice effort"), (1, 5, "chance to learn"),
    (0, 5, "chance to learn"), (0, 0, "chance to learn"),
])
def test_result_encouragement(score, total, expected):
    title, message, icon = result_feedback(score, total)
    assert expected in title
    assert message and icon


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
