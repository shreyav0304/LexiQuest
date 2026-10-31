# LexiQuest exam notes

## Submission overview

LexiQuest is a quiz application for the supplied seventh-semester NLP syllabus.
Its main workflow is choosing a module, answering multiple-choice questions,
receiving an automatic score and reviewing explanations. There are 117 original
syllabus questions, three per topic, plus WordNet synonym and antonym quizzes.
Students can retry incorrect questions and view session results.

Syllabus questions are selected from an original local question bank; WordNet
questions are generated from retrieved lexical relationships. Neither feature
trains an ML model or calls an LLM. The syllabus quiz demonstrates application
logic and course revision; WordNet demonstrates lexical information retrieval.

The five screens are Take a Quiz, Study & Revise, Syllabus, Word Explorer and
My Results. Google Drive notes are not uploaded, integrated or distributed.
Model answers and questions are original practice, not official exam material.

The following sections explain the WordNet case study for viva discussion.

## Core definitions

- **NLP:** Natural Language Processing is the area of computing that processes human language.
- **Information retrieval:** finding relevant information from a collection in response to a query.
- **WordNet:** an English lexical database that groups related words into synonym sets called synsets.
- **Synonym:** a word with a similar meaning, such as *happy* and *glad*.
- **Antonym:** a word with an opposite meaning, such as *hot* and *cold*.

## Problem and objectives

People may need a simple way to revise vocabulary and inspect lexical relationships. LexiQuest retrieves WordNet data and generates a small quiz without pretending that missing relationships exist. Its objectives are to demonstrate information retrieval, explain WordNet, and provide educational practice.

## Requirements and architecture

Software: Python 3, NLTK, WordNet, Streamlit, and Pytest. Hardware: an ordinary Windows laptop with internet access for the one-time corpus download.

Architecture: user interface (`app.py`) → utility functions (`nlp_utils.py`) → local NLTK WordNet corpus → displayed results or quiz feedback.

## Algorithm

1. Read and trim the user's word.
2. Convert it to lower case.
3. Check that WordNet is installed.
4. Retrieve synsets for the word.
5. Collect and deduplicate requested relationships.
6. For a quiz, choose real WordNet relationships and distinct distractors.
7. Shuffle the options.
8. Compare submitted answers with stored answers.
9. Display the score and explanations.

```text
Start
  ↓
Enter word or quiz type
  ↓
Normalize input and check WordNet
  ↓
Retrieve synsets and relationships
  ↓
Enough data? ── No → Explain limitation → Try again
  ↓ Yes
Display results / generate quiz
  ↓
Submit answers → Calculate score → Show feedback
  ↓
End or restart
```

## Important functions

- `normalize_word`: trims extra whitespace and lowercases input.
- `get_synonyms`: collects lemma names from matching synsets and removes duplicates.
- `get_antonyms`: follows WordNet's direct antonym links.
- `get_definitions` and `get_examples`: retrieve explanatory text.
- `generate_quiz_questions`: selects actual relationships and distinct answer options.
- `calculate_score`: counts exact matches once from submitted answer data.

## Working example

Input: `happy`. WordNet may return `glad` as a synonym and `sad` as an antonym. A quiz question stores one verified answer and compares the student's selected option with it.

## Advantages, limitations, and applications

Advantages: explainable, local, inexpensive, simple, and suitable for demonstrations. Limitations: WordNet is incomplete, word senses can differ, and some questions have too little data. Applications include vocabulary revision and introductory NLP teaching.

Future enhancements could include progress history, difficulty levels, more relationship types, and multilingual resources. These are proposed, not implemented.

## Conclusion

LexiQuest demonstrates retrieval of lexical information and quiz generation using a real lexical database. It supports SDG 4's educational purpose by offering an accessible learning activity, without claiming measured learning improvement.

## Viva questions

1. **What is NLP?** Processing human language with computers.
2. **What is WordNet?** A lexical database of English word relationships.
3. **What is a synset?** A group of words expressing one concept.
4. **What is a synonym?** A word with a similar meaning.
5. **What is an antonym?** A word with an opposite meaning.
6. **Why use WordNet?** It provides structured lexical relationships.
7. **Is a model trained?** No; the project retrieves existing lexical data.
8. **Why remove duplicates?** To keep results and options clear.
9. **Why can a quiz have fewer than five questions?** Some WordNet relationships lack enough safe data.
10. **Why check the corpus?** WordNet is a separately installed local resource.
11. **What does Streamlit do?** It creates the interactive web interface.
12. **What does Pytest do?** It runs automated correctness checks.

## Five-mark answer

LexiQuest is a Python NLP case study that uses NLTK WordNet for information retrieval. A user enters a word, and the system retrieves its synonyms, antonyms, definitions, examples, and parts of speech. It cleans duplicates and handles missing data. The same relationships generate a multiple-choice quiz, and submitted answers are scored. Streamlit provides the interface. The project is explainable and educational, but WordNet is incomplete and no machine-learning model is trained.

## Ten-mark answer

LexiQuest solves the problem of making lexical revision interactive. It uses Python, NLTK, WordNet, Streamlit, and Pytest. The interface accepts a word, normalizes it, checks the local WordNet corpus, retrieves matching synsets, and displays definitions and relationships. For quizzes, it selects actual synonym or antonym links, avoids duplicate options, shuffles them, and compares submitted answers to the verified answer. The architecture separates UI code from NLP utility functions. Testing covers normalization, retrieval, missing words, quiz answers, insufficient data, and score calculation. Advantages are simplicity, low cost, and explainability. Limitations include incomplete WordNet coverage and ambiguous word senses. Future enhancements include progress tracking and multiple languages. It supports SDG 4 as an educational practice tool.

