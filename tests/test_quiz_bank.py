import random
import pytest
from content import SYLLABUS, TOPIC_GUIDES
from quiz_bank import syllabus_questions, question_count
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
    questions = syllabus_questions(count=1000, rng=random.Random(1))
    assert len(questions) == question_count() == 117
    assert len({question["question"] for question in questions}) == 117
    assert {question["topic"] for question in questions} == set(TOPIC_GUIDES)
    from collections import Counter
    assert set(Counter(question["topic"] for question in questions).values()) == {3}
    for question in questions:
        assert len(set(question["options"])) == 4
        assert question["options"].count(question["answer"]) == 1
        assert question["explanation"]


def test_filter_limits_and_randomization():
    for module in SYLLABUS:
        questions = syllabus_questions(module["module"], 1000)
        assert len(questions) == 3 * len(module["topics"]) == question_count(module["module"])
        assert {q["topic"] for q in questions} == set(module["topics"])
    assert syllabus_questions(count=0) == []
    assert syllabus_questions("invalid") == []
    first = syllabus_questions(count=5, rng=random.Random(1))
    assert first == syllabus_questions(count=5, rng=random.Random(1))
    assert first != syllabus_questions(count=5, rng=random.Random(2))


def test_different_topics_are_covered_before_revisiting():
    questions = syllabus_questions(count=40, rng=random.Random(4))
    assert len({question["topic"] for question in questions[:39]}) == 39
    assert len(syllabus_questions("Module 5 Large Language Models", 100)) == 12


def test_worked_calculation_answer_keys():
    questions = syllabus_questions(count=1000)
    def answer(fragment):
        return next(q["answer"] for q in questions if fragment in q["question"])
    assert float(answer("factors 0.5, 0.2 and 0.1")) == pytest.approx(0.5 * 0.2 * 0.1)
    assert float(answer("PCFG tree uses rules")) == pytest.approx(0.5 * 0.4 * 0.5)
    assert float(answer("There are 10 relevant documents overall")) == pytest.approx(6 / 10)
    assert float(answer("weights are 0.2 and 0.8")) == pytest.approx(0.2 * 10 + 0.8 * 20)
    assert float(answer("18 of 24 test items")) == pytest.approx(18 / 24)
