"""Original syllabus practice MCQs, with explicitly authored distractors.

Questions and explained correct answers come from the authored topic guides.
These are practice questions, not official university examination questions.
"""

import random
from content import SYLLABUS, TOPIC_GUIDES

# One application question for each of the 39 syllabus topics, in source order.
DISTRACTORS = (
    ("No, translation only changes the font.", "No, NLP only processes numbers.", "Only when each word has one meaning."),
    ("They remove the need for evaluation.", "They make every sentence unambiguous.", "They replace all grammatical structure."),
    ("Only the number of letters in each noun.", "Only capitalization rules.", "The nearest noun must always be selected."),
    ("Informal messages always have no grammar.", "News models cannot process any short sentence.", "A larger vocabulary guarantees identical accuracy everywhere."),
    ("Yes, any grammatical statement must be true.", "Yes, a parse tree verifies scientific facts.", "Yes, nouns determine whether a statement is true."),
    ("Transliteration always changes the language's meaning.", "Translation changes only the alphabet.", "Both operations only correct spelling."),
    ("Document ranking.", "Machine translation.", "Sentence tokenization."),
    ("Only that factor is ignored.", "The whole product becomes one.", "The probability becomes negative."),
    ("4.", "0.75.", "12."),
    ("It requires every language to use a fixed word order.", "It removes all grammatical roles.", "It ignores relations between participants and verbs."),
    ("Ravi.", "The act of writing itself.", "The sentence's word order."),
    ("Two tokens and three types.", "Three tokens and three types.", "Two tokens and two types."),
    ("Only a and b.", "The entire string as one digit sequence.", "No matches because digits follow letters."),
    ("No, at least one b is required.", "No, only the empty string is accepted.", "Only if a is an accepting state name."),
    ("Derivational, because it creates a verb.", "Neither: cats contains no morphemes.", "Derivational, because every suffix changes word class."),
    ("Dictionary lookup always catches contextual errors.", "The words have different lengths.", "A dictionary contains only verbs."),
    ("Noun.", "Determiner.", "Adjective."),
    ("Its spelling alone fixes its tag forever.", "Every occurrence must be a noun.", "Word length determines the tag."),
    ("Parsing only assigns a sentiment label.", "POS tagging always produces a complete parse tree.", "Parsing and tagging are identical tasks."),
    ("Yes, any rule with an arrow is context-free.", "Yes, because its right side has one terminal.", "Only if A and B are both terminals."),
    ("The sentence has no phrase structure.", "Every adjacent pair is a noun phrase.", "The sequence must be a verb phrase."),
    ("To guarantee that every sentence is unambiguous.", "To avoid using a grammar at all.", "To make every partial parse equally probable."),
    ("The tree with probability 0.06.", "Both trees must be rejected.", "Always the tree with fewer words, regardless of probability."),
    ("Retrieval assigns only fixed class labels.", "Classification ranks documents for every new query.", "Both always generate a new answer sentence."),
    ("It guarantees every match is relevant.", "It translates every query automatically.", "It removes the need to store document identifiers."),
    ("A unigram language model.", "A constituency grammar.", "A morphological transducer."),
    ("0.9.", "1.3.", "0."),
    ("It guarantees all passages are relevant.", "It removes the need to know the query.", "It works only when every document has one sentence."),
    ("Precision 0.5; recall 0.8.", "Precision 0.8; recall 0.8.", "Precision 0.5; recall 0.5."),
    ("Every language has exactly the same word order.", "Words always have a single translation.", "Translation requires preserving source word order exactly."),
    ("Only the source sentence length.", "Only the first source token.", "Future reference tokens that are unavailable at inference."),
    ("To ensure the model sees the answer before predicting it.", "To prevent the encoder from reading the source.", "To make every output token equally likely."),
    ("The target side; the source must always be authentic.", "Both sides must always be synthetic.", "Neither side: only manually translated pairs are used."),
    ("No, fluency guarantees preserved meaning.", "No, adequacy is identical to spelling accuracy.", "Only if the translation has no verbs."),
    ("To replace all human judgment with one average.", "To guarantee identical grammar in every language.", "To avoid testing low-resource languages."),
    ("To eliminate the need for token embeddings.", "To guarantee generated facts are correct.", "To make all token orderings equivalent."),
    ("Only the first token.", "All three tokens.", "Only the second token."),
    ("Only manually assigned sentiment labels.", "The model's future deployment users.", "A dictionary's alphabetical ordering."),
    ("To reward memorization as independent test performance.", "To remove the need for held-out data.", "To ensure every benchmark question appears in training."),
)

TOPICS = [topic for module in SYLLABUS for topic in module["topics"]]
if len(TOPICS) != len(DISTRACTORS):
    raise ValueError("Each syllabus topic needs its own MCQ distractors")


def syllabus_questions(module=None, count=5, rng=None):
    """Return a shuffled set without repeated topics; None covers all modules."""
    randomizer = rng or random.Random()
    eligible = {topic for item in SYLLABUS if module is None or item["module"] == module for topic in item["topics"]}
    questions = []
    for topic, distractors in zip(TOPICS, DISTRACTORS):
        if topic not in eligible:
            continue
        practice = TOPIC_GUIDES[topic]["practice_questions"][1]
        options = [practice["answer"], *distractors]
        randomizer.shuffle(options)
        questions.append({"topic": topic, "question": practice["question"], "options": options,
                          "answer": practice["answer"], "explanation": practice["explanation"]})
    randomizer.shuffle(questions)
    return questions[:max(0, count)]


def result_feedback(score, total):
    """Encouraging feedback based on the exact score, not rounded percentages."""
    ratio = score / total if total else 0
    if total and score == total:
        return "Hurray! Perfect score!", "You got every question right. Ready for another challenge?", "🎉"
    if ratio >= 0.8:
        return "Hurray! Great work!", "You're doing really well. Review the few you missed and keep going.", "🌟"
    if ratio >= 0.5:
        return "Nice effort! Keep building.", "You've got a good start. A quick review can turn those mistakes into marks.", "💪"
    return "Oops! A chance to learn.", "This score is a starting point. Read the explanations and try again — you can improve!", "🌱"
