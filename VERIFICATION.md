# Verification — updated 31 October 2026

## Current result: optimization and question expansion

**47 tests passed in 8.92 seconds**, exit code 0, outside the sandbox. The
sandboxed UI runs were interrupted after a diagnostic traceback showed Windows
asyncio waiting in its local socket-pair setup before executing the app. The
unsandboxed run passed without the earlier temporary-directory cleanup error.

The bank now has **117 unique original questions**, three for each of the 39
unchanged syllabus topics. Module totals are 33, 36, 18, 18 and 12. Added
conceptual, terminology, algorithm and worked-calculation questions. Tests check
four distinct choices, answer membership, topic coverage, question uniqueness,
filtering, and independently calculated numerical answer keys. Short attempts
cover different topics before revisiting one. These are not official exam items.

A regression test also confirms that a running app can recover from the old
cached question-bank module when importing the new question-count helper.

Removed the full-corpus WordNet scan and shuffle. A bounded common-word pool
supplies real lexical senses; immutable templates are cached for two quiz modes,
and synset lookups have a 512-entry cache. Each quiz is still freshly shuffled.
The custom test-corpus path also has a bounded scan. Regression tests prohibit
full production-corpus enumeration and confirm reuse without mutable-option leaks.
Word Explorer now uses a submit form and a bounded 256-entry result cache.
Missing corpus errors are not permanently cached. The syllabus bank compiles
once; pages render at most 20 questions, and results initially show incorrect
answers with an optional full-review toggle.

Measured with perf_counter around generation calls in fresh Python processes,
excluding imports, using the installed local corpus:

| Operation | Before | After |
| --- | --- | --- |
| First five-question synonym quiz | 11.824 s | 2.7781 s |
| Following five-question antonym quiz | 0.863 s | 0.0368 s |
| Repeated 15-question synonym quiz | Not recorded | 0.0027 s |

These individual local measurements do not guarantee cloud latency. First use
still loads WordNet; server wake-up time is outside these timings. Vocabulary
quizzes use a beginner-friendly subset; Word Explorer still supports arbitrary
words in the full installed corpus. The network-blocked offline check passed
with 117 questions, scoring, 39 guides, word lookups and both quiz generators.
No new live browser visual or network-latency tests were performed.

## Original submission simplification (30 October)

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

Latest result before the October 31 performance update: **41 passed in 8.05 seconds**. Tests for the
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

## Responsive layout update

Added phone/tablet breakpoints at 360, 768 and 1024 CSS pixels, a compact menu
below 768 pixels synchronized with desktop navigation, wrapping answer text,
44-pixel minimum interactive targets, stacked paired columns, safe-area padding
and 16-pixel mobile input text. Results now use readable cards rather than a wide
table. The default sidebar uses Streamlit's auto-collapse behaviour.

Existing tests were updated to select controls by stable keys; a regression test
checks compact-menu navigation and synchronization with desktop navigation.
AppTest cannot validate viewport geometry. A live browser window was discovered,
but the automation returned unavailable input geometry and a screenshot from a
different foreground window, so live responsive visual inspection could not be
completed reliably. No claim of testing on every physical device is made.

## Visual polish

Added a compact brand mark and icon navigation, a white quiz setup card with
small course highlights, individual question cards, bordered answer choices with
hover/selection styling, and a score summary card. Refined the violet palette,
typography, spacing, metrics and expanders while preserving the mobile menu,
wrapping text, touch-target sizes and reduced-motion rules. Existing interaction
and content tests pass. This update has not received live browser visual QA;
the earlier browser automation limitations still apply.

## Teal quiz edition

The deployed page was inspected through Windows accessibility and a screenshot
after raising the Edge window. It contained the previous update's new brand and
quiz labels, confirming that deployment was current. The user still found it too
similar, so the design was changed to a dark navy sidebar, teal controls, compact
dark quiz banner, mint highlights and paired setup fields. A visible "QUIZ
EDITION · TEAL" sidebar label distinguishes this release from earlier versions.

## Hosted WordNet setup fix

The supplied screenshot shows a missing corpus on the hosted server. Added an
explicit Set up WordNet button shared by vocabulary quiz setup and Word Explorer.
It downloads only English WordNet into ignored server-local `nltk_data/`, adds
that path to NLTK discovery, and verifies a real lookup. No download runs at app
startup. Missing-data messages no longer require a terminal on the hosted app.
Failure remains retryable; the syllabus quiz remains available without WordNet.

The real installer was tested with NLTK restricted to the project data directory:
the sandbox proxy blocked the first network attempt, and the approved unsandboxed
download completed with `(True, 'WordNet is ready.')`. Tests also simulate setup
success/failure, ensure quizzes enable after setup, and check that an existing
corpus is reused without downloading again. Live hosted installation has not been
performed through the user's browser.

## Local offline use

Added start_offline.bat, a local-only Windows launcher using the existing virtual
environment. It binds Streamlit to 127.0.0.1, performs no package installation and
disables usage telemetry. The setup script now places WordNet in project-local
nltk_data/ and reports a failing exit status if preparation fails.

Executed offline_check.py with outgoing socket connections blocked: all 39
syllabus questions, perfect-answer scoring, 39 study guides, WordNet definitions,
synonyms, antonyms and both vocabulary generators passed using project-local
data. This is an application-logic check, not an offline browser test. The batch
launcher was not launched interactively. Initial dependencies and dictionary data
still require preparation before disconnecting. The hosted Streamlit URL requires
internet; no offline Android/iOS application or service worker is provided.

## Encouraging result pop-up

Added score-based native toast notifications for perfect scores, scores at least
80%, scores at least 50%, and lower scores. Messages are encouraging and include
a next step. A pending-event flag displays the toast once after a completed
submission, without repeating it on reruns or revisiting results. The result card
keeps the same message visible after the toast disappears. Tests cover score
boundaries and verify one toast on submission with none on the next rerun.
