"""LexiQuest: simple syllabus and WordNet quizzes."""

from pathlib import Path
import importlib
import streamlit as st
import content as course_content

if not all(hasattr(course_content, name) for name in ("COURSE", "TEXTBOOKS")):
    importlib.reload(course_content)

from content import COURSE, TEXTBOOKS, SYLLABUS, TOPIC_GUIDES
from nlp_utils import (calculate_score, generate_quiz_questions, wordnet_status,
                       get_definitions, get_synonyms, get_antonyms, get_examples)
from quiz_bank import syllabus_questions
from wordnet_setup import install_wordnet, register_wordnet_path

register_wordnet_path()

st.set_page_config(page_title="LexiQuest | NLP Quiz", page_icon="📘", layout="centered", initial_sidebar_state="auto")
st.html("<style>" + Path(__file__).with_name("ui.css").read_text(encoding="utf-8") + "</style>")
PAGES = ["Take a Quiz", "Study & Revise", "Syllabus", "Word Explorer", "My Results"]


def navigate(page):
    st.session_state["page"] = page


def navigate_mobile():
    navigate(st.session_state["mobile_page"])


def wordnet_ready():
    """Offer cloud-compatible setup instead of a terminal-only instruction."""
    ready, _ = wordnet_status()
    if ready:
        return True
    st.info("WordNet needs a one-time download on this server. The NLP syllabus quiz works without it.")
    if st.button("Set up WordNet", key="setup_wordnet", type="primary"):
        with st.spinner("Downloading the English WordNet dictionary..."):
            success, message = install_wordnet()
        if success:
            st.rerun()
        else:
            st.error(message)
    return False


def begin_quiz(questions, title):
    st.session_state["attempt_id"] = st.session_state.get("attempt_id", 0) + 1
    st.session_state["active_quiz"] = {"questions": questions, "title": title}
    st.session_state["submitted"] = False


def show_quiz():
    active = st.session_state.get("active_quiz")
    if active:
        st.title("Your quiz results" if st.session_state.get("submitted") else "Let's put it into practice.")
    else:
        st.html('<section class="quiz-banner"><div class="banner-kicker">LEXIQUEST / NLP PRACTICE</div><h1>A little practice.<br>A lot more confidence.</h1><p>Your syllabus. Clear questions. A smarter way to revise.</p><div class="banner-line"><span>01 &nbsp; Choose</span><span>02 &nbsp; Challenge yourself</span><span>03 &nbsp; Learn & improve</span></div></section>')
    if not active:
        st.html('<div class="quiz-highlights"><span>5 syllabus modules</span><span>39 original questions</span><span>Instant explanations</span></div>')
        with st.container(border=True, key="quiz_setup"):
            st.html('<div class="card-kicker">YOUR NEXT CHALLENGE</div>')
            st.subheader("Start a quiz")
            type_column, module_column = st.columns(2, gap="medium")
            kind = type_column.selectbox("Quiz type", ["NLP syllabus", "WordNet synonyms", "WordNet antonyms"], key="quiz_type")
            if kind == "NLP syllabus":
                ready = True
                module = module_column.selectbox("Module", ["All modules", *[item["module"] for item in SYLLABUS]], key="quiz_module")
                available = sum(len(item["topics"]) for item in SYLLABUS if module == "All modules" or item["module"] == module)
                count = st.slider("Number of questions", 1, available, min(5, available))
                st.caption(f"{available} original questions available, aligned with your seventh-semester syllabus.")
            else:
                count = st.select_slider("Number of questions", options=[5, 10, 15], value=5)
                st.caption("Vocabulary practice using the local WordNet database.")
                ready = wordnet_ready()
            if st.button("Start quiz", type="primary", width="stretch", icon=":material/arrow_forward:", disabled=not ready):
                if kind == "NLP syllabus":
                    questions = syllabus_questions(None if module == "All modules" else module, count)
                    title = module
                else:
                    with st.spinner("Preparing your WordNet questions..."):
                        questions = generate_quiz_questions("synonym" if kind == "WordNet synonyms" else "antonym", count)
                    title = kind
                if not questions:
                    st.warning("No questions available. Try another quiz.")
                    return
                begin_quiz(questions, title)
                st.rerun()
        st.caption("Original practice questions, not official examination questions. No notes upload or Drive connection needed.")
        return
    questions = active["questions"]
    st.write(f"**{active['title']}** · {len(questions)} questions · 1 mark each")
    if st.button("Change quiz"):
        st.session_state.pop("active_quiz", None)
        st.rerun()
    if not st.session_state.get("submitted"):
        attempt = st.session_state["attempt_id"]
        with st.form(f"quiz_form_{attempt}"):
            answers = {}
            for index, question in enumerate(questions):
                with st.container(border=True, key=f"question_card_{index}"):
                    st.caption(f"QUESTION {index + 1:02d} OF {len(questions):02d}")
                    st.markdown(f"#### {question['question']}")
                    answers[index] = st.radio("Choose one answer", question["options"], index=None,
                                              key=f"answer_{attempt}_{index}", label_visibility="collapsed")
            submitted = st.form_submit_button("Submit answers", type="primary", width="stretch")
        if submitted:
            if any(answer is None for answer in answers.values()):
                missing = [str(index + 1) for index, answer in answers.items() if answer is None]
                st.warning("Please answer question(s): " + ", ".join(missing))
            else:
                score = calculate_score(questions, answers)
                st.session_state.update(submitted=True, last_answers=answers, last_score=score)
                st.session_state.setdefault("history", []).append({
                    "Quiz": active["title"], "Score": score, "Questions": len(questions),
                    "Percentage": round(100 * score / len(questions)),
                })
                st.rerun()
        return
    answers = st.session_state["last_answers"]
    score = st.session_state["last_score"]
    st.html(f'<div class="score-card"><div><div class="card-kicker">QUIZ COMPLETE</div><div class="score-title">Every attempt is progress.</div><div class="score-note">Review your answers below and keep building your understanding.</div></div><div class="score-circle">{score}<span>of {len(questions)}</span></div></div>')
    st.success(f"Your score: {score}/{len(questions)} ({score / len(questions):.0%})")
    st.progress(score / len(questions))
    st.subheader("Review your answers")
    wrong = []
    for index, question in enumerate(questions):
        correct = answers[index] == question["answer"]
        if not correct:
            wrong.append(question)
        with st.expander(f"{index + 1}. {'Correct' if correct else 'Review'} — {question['question']}", expanded=not correct):
            st.write(f"**Your answer:** {answers[index]}")
            st.write(f"**Correct answer:** {question['answer']}")
            st.write(question.get("explanation", "This relationship is recorded in WordNet. Different word senses may have different related words."))
            if question.get("topic"):
                st.caption("Revise in Study & Revise: " + question["topic"])
    retry, new = st.columns(2)
    if retry.button("Retry incorrect" if wrong else "Try again", width="stretch"):
        begin_quiz(wrong or questions, active["title"])
        st.rerun()
    if new.button("New quiz", type="primary", width="stretch"):
        st.session_state.pop("active_quiz", None)
        st.rerun()


def show_study():
    st.title("Study & Revise")
    st.caption("Pick a topic for a simple explanation, revision notes or an exam answer.")
    module = st.selectbox("Module", [item["module"] for item in SYLLABUS], key="study_module")
    item = next(item for item in SYLLABUS if item["module"] == module)
    topic = st.selectbox("Topic", item["topics"], key="study_topic")
    guide = TOPIC_GUIDES[topic]
    st.subheader(topic)
    learn, revise, exam = st.tabs(["Learn", "Quick revision", "Exam answers"])
    with learn:
        st.info(guide["definition"])
        st.write(guide["intuitive_explanation"])
        st.markdown("#### Step by step")
        st.markdown(guide["step_by_step"])
        st.markdown("#### Worked example")
        st.write(guide["example"])
        st.markdown("**Key terms:** " + "; ".join(guide["terminology"]))
        with st.expander("Common mistake"):
            st.write(guide["common_mistakes"])
    with revise:
        st.write(guide["revision"])
        st.info(guide["exam_tip"])
        for question in guide["practice_questions"]:
            with st.expander(question["question"]):
                st.write(question["answer"])
                st.caption(question["explanation"])
    with exam:
        st.caption("Original model answers and suggested marks, not official marking schemes.")
        with st.expander("5-mark answer"):
            st.markdown(guide["model_answer_5"])
        with st.expander("10-mark answer"):
            st.markdown(guide["model_answer_10"])
    st.caption(" · ".join(item["textbook_chapters"]))


def show_syllabus():
    st.title("Your NLP syllabus")
    st.caption(f"{COURSE['code']} · Semester {COURSE['semester']} · 5 modules · 40 hours")
    for item in SYLLABUS:
        with st.expander(item["module"]):
            st.caption(f"{item['hours']} hours · RBT: {', '.join(item['rbt_levels'])}")
            for topic in item["topics"]:
                st.markdown(f"- {topic}")
            st.write("**Textbook references**")
            for reference in item["textbook_chapters"]:
                st.write(reference)
    with st.expander("Prescribed textbooks"):
        for number, reference in TEXTBOOKS.items():
            st.write(f"{number}. {reference}")
    st.caption("Module order and chapter references follow your supplied syllabus. Students use their own course notes.")


def show_explorer():
    st.title("Word Explorer")
    st.caption("Look up a word before taking a synonym or antonym quiz.")
    word = st.text_input("Enter an English word", placeholder="For example: happy").strip().lower()
    if not word:
        return
    if not wordnet_ready():
        return
    definitions = get_definitions(word)
    if not definitions:
        st.info("No WordNet entry found. Try another word.")
        return
    st.subheader(word.title())
    for definition in definitions:
        st.markdown(f"- {definition}")
    left, right = st.columns(2)
    left.markdown("**Synonyms**")
    left.write(", ".join(get_synonyms(word)) or "No direct synonyms recorded.")
    right.markdown("**Antonyms**")
    right.write(", ".join(get_antonyms(word)) or "No direct antonyms recorded.")
    with st.expander("Example sentences"):
        examples = get_examples(word)
        for example in examples:
            st.write(example)
        if not examples:
            st.caption("No example sentences recorded.")


def show_results():
    st.title("My Results")
    st.caption("Results are saved for this session only and reset when it ends.")
    history = st.session_state.get("history", [])
    if not history:
        st.info("Take a quiz to see your results here.")
        st.button("Take a quiz", on_click=navigate, args=("Take a Quiz",), type="primary")
        return
    left, right = st.columns(2)
    left.metric("Quizzes completed", len(history))
    right.metric("Best result", f"{max(row['Percentage'] for row in history)}%")
    st.subheader("Completed quizzes")
    for index, result in reversed(list(enumerate(history, 1))):
        with st.container(border=True):
            st.markdown(f"**Attempt {index} · {result['Quiz']}**")
            st.write(f"{result['Score']}/{result['Questions']} correct · {result['Percentage']}%")


def main():
    st.session_state.setdefault("page", "Take a Quiz")
    # Keep both navigation surfaces synchronized. CSS shows this compact menu
    # only on narrow screens, without relying on detecting a browser user agent.
    st.session_state["mobile_page"] = st.session_state["page"]
    with st.container(key="mobile_navigation"):
        st.selectbox("LexiQuest · Menu", PAGES, key="mobile_page", on_change=navigate_mobile)
    with st.sidebar:
        st.html('<div class="app-brand"><div class="brand-mark">L</div><div><div class="brand-name">LexiQuest</div><div class="brand-tagline">A curious mind starts here.</div></div></div>')
        st.caption("YOUR WORKSPACE")
        with st.container(key="simple_nav", gap="small"):
            icons = ["quiz", "menu_book", "format_list_bulleted", "search", "bar_chart"]
            for page, icon in zip(PAGES, icons):
                st.button(page, key=f"nav_{page}", width="stretch",
                          icon=f":material/{icon}:",
                          type="primary" if st.session_state["page"] == page else "secondary",
                          on_click=navigate, args=(page,))
        st.divider()
        st.caption("AI401 · Semester VII")
        st.caption("QUIZ EDITION · TEAL")
    {"Take a Quiz": show_quiz, "Study & Revise": show_study, "Syllabus": show_syllabus,
     "Word Explorer": show_explorer, "My Results": show_results}[st.session_state["page"]]()


if __name__ == "__main__":
    main()
