# LexiQuest submission requirements

Updated 30 October 2026 following the user's request to simplify the project for
Monday submission and focus on quizzes. This supersedes the earlier twelve-page
dashboard and study-buddy navigation requirements.

## Core workflow

Open directly on the quiz screen. Choose a quiz type, optional syllabus module
and question count. Start, answer all questions and submit. Show an automatic
score, correct answers and explanations. Permit retrying incorrect questions,
restarting and changing the quiz. Clear previous answers for each new attempt.
Do not count incomplete submissions or duplicate a result during reruns.

Provide five navigation items only: Take a Quiz, Study & Revise, Syllabus,
Word Explorer and My Results. Use a restrained native Streamlit interface with
readable labels and a centered content area. Avoid large decorative dashboards,
timers, complicated animation or redundant screens.

## Content authority

The user's supplied seventh-semester AI401 syllabus controls all five modules,
their order, topic coverage and textbook chapter/section references. Preserve
`content.SYLLABUS` and `SYLLABUS_SOURCE.md`. No chapter numbering may be inferred
from a different textbook edition or an online manuscript.

Google Drive notes are reference material only. Students have their own copies.
No upload, Drive folder connection, private-note access or redistribution is
required. Do not claim to have read unavailable notes or textbook chapters.

## Quiz and study material

Provide 117 original syllabus MCQs, three per recorded topic, each with four distinct
choices, one intended correct answer and an explanation. Allow selection from a
module or all modules without repeated questions within an attempt. Cover different
topics before revisiting one, and limit rendered attempts to 20 questions. Shuffle questions
and choices. Clearly label them as original practice, not official exam questions.

Keep topic explanations, intuition, ordered teaching steps, terminology, worked
examples, mistakes, revision notes and structured 5/10-mark model answers available
in Study & Revise. Model answers and mark allocations are illustrative.

Keep the working WordNet synonym and antonym quiz modes, word definitions,
examples and related-word lookup. Do not use another valid retrieved relationship
as a distractor. Include word sense context where available. Handle missing corpus
and unknown-word cases clearly; never download data silently at startup.

Keep vocabulary quiz generation bounded to a beginner-friendly word pool rather
than scanning the whole corpus per attempt. Cache reusable lexical templates and
lookup results without caching a fixed shuffled quiz or a missing-corpus error.

## Results and submission

Results are session-local and must be described as such. No authentication,
database, external API or LLM is needed. Document setup, one-time WordNet download,
test commands and a short demonstration in README.md. Run logic and interaction
tests; state exactly what was checked and distinguish that from browser visual
verification. Retain the original syllabus and WordNet case-study viva notes.
