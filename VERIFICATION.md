# Verification — 30 October 2026

## Submission simplification

Replaced the twelve-page dashboard with five focused screens: Take a Quiz,
Study & Revise, Syllabus, Word Explorer and My Results. The app opens on quiz
setup, uses a centered native Streamlit layout and removes the oversized hero,
redundant navigation and decorative animations. Hover feedback and reduced-motion
support remain.

Added 39 original, automatically scored syllabus MCQs: one for every recorded
topic, with four choices and an explained answer. Questions and options shuffle;
module filtering and question counts respect the available topic pool. Students
must answer every question before submission. Results show score, percentage,
correct answers and explanations, with retry-incorrect and new-quiz actions.
Completed attempts appear in session-local history without duplicate entries on
reruns. Each retry gets fresh widget keys so previous selections are cleared.

The five-module syllabus, topic order and prescribed textbook references remain
unchanged. All original teaching guides and 5/10-mark model answers remain
available under Study & Revise. No Drive material was accessed or integrated.

WordNet exploration and both vocabulary quiz types remain. WordNet questions now
include sense context and explanations; distractors exclude other relationships
retrieved for the source word. Missing corpora and unknown words are handled.
The README, project requirements, dependency floor and viva overview were updated
to describe the simplified application.

## Checks

Command: `.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider`.

Final result: **29 passed in 19.99 seconds**, process exit code 0. Tests for the
removed dashboard were replaced with tests for the new quiz workflow.

Coverage includes:

- All five navigation screens and every study module.
- All 39 MCQs, four distinct choices, correct-answer membership, module filtering
  and deterministic shuffling under a seeded random generator.
- Incomplete submissions, automatic scoring, answer review, retry-incorrect,
  fresh answers, switching quizzes and session history without duplicate results.
- Both WordNet UI modes using deterministic fixtures, missing-corpus messages,
  retrieval helpers and exclusion of valid relationships from distractors.
- Preserved syllabus chapter references, topic counts and course metadata.
- Previously implemented pure n-gram, regex, ranking and progress utilities.
- Recovery when an old cached content module lacks course metadata.

Separately verified the installed WordNet corpus reports ready and generates five
synonym and five antonym questions with the updated generator.

## Limits

AppTest checks behaviour without a browser. No live browser inspection of this
final layout was performed. Structural question-bank tests do not independently
certify the wording of every educational statement. Windows reports a temporary
directory cleanup permission error after successful test completion; assertion
results and process exit status are recorded separately.
