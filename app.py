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

st.set_page_config(page_title="LexiQuest | NLP Quiz", page_icon="📘", layout="centered")
st.html("<style>" + Path(__file__).with_name("ui.css").read_text(encoding="utf-8") + "</style>")
PAGES = ["Take a Quiz", "Study & Revise", "Syllabus", "Word Explorer", "My Results"]


def navigate(page):
    st.session_state["page"] = page


def begin_quiz(questions, title):
    st.session_state["attempt_id"] = st.session_state.get("attempt_id", 0) + 1
    st.session_state["active_quiz"] = {"questions": questions, "title": title}
    st.session_state["submitted"] = False


def show_quiz():
    st.title("NLP Quiz")
    st.caption("Choose a quiz. Test yourself. Learn from every answer.")
    active = st.session_state.get("active_quiz")
    if not active:
        with st.container(border=True):
            st.subheader("Start a quiz")
            kind = st.selectbox("Quiz type", ["NLP syllabus", "WordNet synonyms", "WordNet antonyms"])
            if kind == "NLP syllabus":
                module = st.selectbox("Module", ["All modules", *[item["module"] for item in SYLLABUS]])
                available = sum(len(item["topics"]) for item in SYLLABUS if module == "All modules" or item["module"] == module)
                count = st.slider("Number of questions", 1, available, min(5, available))
                st.caption(f"{available} original questions available, aligned with your seventh-semester syllabus.")
            else:
                count = st.select_slider("Number of questions", options=[5, 10, 15], value=5)
                st.caption("Vocabulary practice using the local WordNet database.")
            if st.button("Start quiz", type="primary", width="stretch"):
                if kind == "NLP syllabus":
                    questions = syllabus_questions(None if module == "All modules" else module, count)
                    title = module
                else:
                    ready, message = wordnet_status()
                    if not ready:
                        st.error(message)
                        return
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
                st.markdown(f"#### {index + 1}. {question['question']}")
                answers[index] = st.radio("Choose one answer", question["options"], index=None,
                                          key=f"answer_{attempt}_{index}", label_visibility="collapsed")
                if index < len(questions) - 1:
                    st.divider()
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
    module = st.selectbox("Module", [item["module"] for item in SYLLABUS])
    item = next(item for item in SYLLABUS if item["module"] == module)
    topic = st.selectbox("Topic", item["topics"])
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
    ready, message = wordnet_status()
    if not ready:
        st.error(message)
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
    st.dataframe(history, hide_index=True, width="stretch")


def main():
    st.session_state.setdefault("page", "Take a Quiz")
    with st.sidebar:
        st.title("LexiQuest")
        st.caption("NLP quizzes made simple")
        with st.container(key="simple_nav", gap="small"):
            for page in PAGES:
                st.button(page, key=f"nav_{page}", width="stretch",
                          type="primary" if st.session_state["page"] == page else "secondary",
                          on_click=navigate, args=(page,))
        st.divider()
        st.caption("AI401 · Semester VII")
    {"Take a Quiz": show_quiz, "Study & Revise": show_study, "Syllabus": show_syllabus,
     "Word Explorer": show_explorer, "My Results": show_results}[st.session_state["page"]]()


if __name__ == "__main__":
    main()
