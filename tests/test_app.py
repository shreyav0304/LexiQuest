from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")


def app():
    result = AppTest.from_file(APP, default_timeout=30).run()
    assert not result.exception
    return result


def button(ui, label):
    return next(button for button in ui.button if button.label == label)


@pytest.mark.parametrize("page", ["Take a Quiz", "Study & Revise", "Syllabus", "Word Explorer", "My Results"])
def test_navigation(page):
    ui = app()
    ui.sidebar.button(key=f"nav_{page}").click().run()
    assert ui.session_state["page"] == page
    assert not ui.exception


def test_compact_menu_stays_synchronized_with_desktop_navigation():
    ui = app()
    ui.selectbox(key="mobile_page").select("Study & Revise").run()
    assert ui.session_state["page"] == "Study & Revise"
    assert ui.tabs
    ui.sidebar.button(key="nav_My Results").click().run()
    assert ui.selectbox(key="mobile_page").value == "My Results"
    ui.selectbox(key="mobile_page").select("Take a Quiz").run()
    button(ui, "Start quiz").click().run()
    assert ui.radio
    assert not ui.exception


def test_incomplete_attempt_then_score_review_retry_and_history():
    ui = app()
    button(ui, "Start quiz").click().run()
    button(ui, "Submit answers").click().run()
    assert ui.warning
    assert not ui.session_state["submitted"]
    questions = ui.session_state["active_quiz"]["questions"]
    for index, question in enumerate(questions):
        answer = question["answer"] if index else next(option for option in question["options"] if option != question["answer"])
        ui.radio[index].set_value(answer)
    button(ui, "Submit answers").click().run()
    assert ui.session_state["last_score"] == len(questions) - 1
    assert len(ui.session_state["history"]) == 1
    assert len(ui.get("toast")) == 1
    ui.run()
    assert not ui.get("toast")
    assert len(ui.session_state["history"]) == 1
    assert any(question["explanation"] in item.value for question in questions for item in ui.markdown)
    button(ui, "Retry incorrect").click().run()
    assert len(ui.radio) == 1
    assert ui.radio[0].value is None
    ui.radio[0].set_value(ui.session_state["active_quiz"]["questions"][0]["answer"])
    button(ui, "Submit answers").click().run()
    assert ui.session_state["last_score"] == 1
    button(ui, "New quiz").click().run()
    assert ui.selectbox(key="quiz_type").value == "NLP syllabus"
    ui.sidebar.button(key="nav_My Results").click().run()
    assert len(ui.session_state["history"]) == 2
    assert not ui.exception


def test_module_five_selection_and_change_quiz():
    ui = app()
    ui.selectbox(key="quiz_module").select("Module 5 Large Language Models").run()
    button(ui, "Start quiz").click().run()
    assert len(ui.radio) == 4
    assert all("Large Language Models" in q["topic"] or q["topic"] == "Sampling for LLM Generation" for q in ui.session_state["active_quiz"]["questions"])
    button(ui, "Change quiz").click().run()
    assert not ui.radio
    assert not ui.exception


@pytest.mark.parametrize("kind", ["WordNet synonyms", "WordNet antonyms"])
def test_wordnet_modes(monkeypatch, kind):
    import nlp_utils
    monkeypatch.setattr(nlp_utils, "wordnet_status", lambda: (True, "Ready"))
    monkeypatch.setattr(nlp_utils, "generate_quiz_questions", lambda mode, count: [
        {"question": mode, "options": ["correct", "wrong"], "answer": "correct"}
    ])
    ui = app()
    ui.selectbox(key="quiz_type").select(kind).run()
    button(ui, "Start quiz").click().run()
    ui.radio[0].set_value("correct")
    button(ui, "Submit answers").click().run()
    assert ui.session_state["last_score"] == 1
    button(ui, "Try again").click().run()
    assert ui.radio[0].value is None
    assert not ui.exception


def test_missing_wordnet_is_actionable(monkeypatch):
    import nlp_utils
    monkeypatch.setattr(nlp_utils, "wordnet_status", lambda: (False, "Run python setup_nltk.py"))
    ui = app()
    ui.selectbox(key="quiz_type").select("WordNet synonyms").run()
    assert button(ui, "Start quiz").disabled
    assert button(ui, "Set up WordNet")
    assert "one-time download" in ui.info[0].value
    assert not ui.exception


def test_hosted_setup_failure_is_retryable(monkeypatch):
    import nlp_utils
    import wordnet_setup
    monkeypatch.setattr(nlp_utils, "wordnet_status", lambda: (False, "Missing"))
    monkeypatch.setattr(wordnet_setup, "install_wordnet", lambda: (False, "Please retry the download."))
    ui = app()
    ui.selectbox(key="quiz_type").select("WordNet synonyms").run()
    button(ui, "Set up WordNet").click().run()
    assert "retry" in ui.error[0].value
    assert button(ui, "Set up WordNet")
    assert not ui.exception


def test_hosted_setup_success_enables_quiz(monkeypatch):
    import nlp_utils
    import wordnet_setup
    ready = [False]
    monkeypatch.setattr(nlp_utils, "wordnet_status", lambda: (ready[0], "Status"))
    def install():
        ready[0] = True
        return True, "Ready"
    monkeypatch.setattr(wordnet_setup, "install_wordnet", install)
    ui = app()
    ui.selectbox(key="quiz_type").select("WordNet synonyms").run()
    button(ui, "Set up WordNet").click().run()
    assert not button(ui, "Start quiz").disabled
    assert not ui.exception


def test_study_syllabus_and_cached_metadata(monkeypatch):
    import content
    monkeypatch.delattr(content, "COURSE")
    ui = app()
    ui.sidebar.button(key="nav_Study & Revise").click().run()
    assert [tab.label for tab in ui.tabs] == ["Learn", "Quick revision", "Exam answers"]
    for module in content.SYLLABUS:
        ui.selectbox(key="study_module").select(module["module"]).run()
        ui.selectbox(key="study_topic").select(module["topics"][-1]).run()
        assert not ui.exception
    ui.sidebar.button(key="nav_Syllabus").click().run()
    assert len(ui.expander) == 6
    assert not ui.exception
