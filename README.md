# LexiQuest — NLP Quiz

A simple seventh-semester NLP quiz application built with Python, Streamlit and
NLTK WordNet. The supplied AI401 syllabus defines the five modules and their
textbook chapter references. No Google Drive integration or notes upload is needed.

## Run on Windows

From the project folder in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe setup_nltk.py
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local address printed by Streamlit, normally `http://localhost:8501`.
If an older copy is running, stop it with Ctrl+C before running the last command.
`setup_nltk.py` needs internet once for the WordNet corpora. The syllabus quiz
works without WordNet; the vocabulary quiz and explorer need those corpora.

For a hosted app, open a WordNet quiz or enter a word in Word Explorer and click
**Set up WordNet** if prompted. The app downloads the English dictionary on the
server and verifies it before enabling quizzes. No cloud terminal is needed.
The server needs internet access for this download; if it fails, retry the
button. Setup may be needed again if the hosting service replaces the server.
Corpus files are kept in ignored `nltk_data/`, not committed to GitHub.

## How to use

1. **Take a Quiz:** choose NLP syllabus, WordNet synonyms or WordNet antonyms.
2. For syllabus quizzes, choose one module or all modules and the question count.
3. Select an answer for every question, then submit for your score and explanations.
4. Retry incorrect questions or start a new quiz.

**Study & Revise** contains explanations, examples, revision notes and original
5/10-mark model answers for all 39 topics. **Syllabus** preserves the supplied
module organization and chapter ranges. **Word Explorer** retrieves meanings,
synonyms, antonyms and examples. **My Results** displays completed attempts.

There are 39 original syllabus MCQs, one per topic, with four answer choices.
Module question counts are 11, 12, 6, 6 and 4 respectively. Questions and options
are shuffled. These are practice questions, not official university exam questions.
Written model answers are study material, not automatically graded responses.

Results last only for the current Streamlit session. No account, database, API
key, trained model or LLM is required. WordNet coverage varies; the app reports
missing entries or unavailable corpus data rather than inventing results.

The layout adapts to narrow phones, tablets and desktop screens. On smaller
screens, use the **LexiQuest · Menu** selector above the page. Answer options
wrap, controls have touch-friendly targets, paired panels stack, and results
use cards instead of a wide table. The desktop sidebar remains available.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider
```

Tests cover syllabus coverage, filtering, scoring, incomplete attempts, answer
review, retries, results, navigation and WordNet behaviour. See
[VERIFICATION.md](VERIFICATION.md) for actual verification and limitations.

## Project files

| File | Purpose |
| --- | --- |
| `app.py` | Five-screen Streamlit quiz interface |
| `quiz_bank.py` | Original MCQ distractors and question selection |
| `content.py` | Supplied syllabus and pure study utilities |
| `lessons.py` | Original teaching material for all 39 topics |
| `nlp_utils.py` | WordNet retrieval, question generation and scoring |
| `setup_nltk.py` | One-time WordNet corpus download |
| `SYLLABUS_SOURCE.md` | Syllabus transcription and textbook references |
| `exam_notes.md` | Project viva and WordNet case-study notes |
| `tests/` | Logic and Streamlit interaction tests |

## Short demonstration

Start a five-question syllabus quiz, submit answers, show the explanations and
retry an incorrect question. Open Study & Revise to explain a topic, show its
chapter reference in Syllabus, then demonstrate a WordNet quiz and word lookup.
The application demonstrates quiz logic, syllabus-aligned learning and lexical
information retrieval; it does not train a machine-learning model.
