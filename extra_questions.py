"""Original syllabus practice: two additional questions per topic.

Each tuple is (question, correct answer, three distractors, explanation).
Examples are authored teaching cases, not official examination questions.
"""

ADDITIONAL = {
"What is Natural Language Processing?": [
    ("Which output belongs to sentiment classification?", "A positive/negative label", ("A translated sentence", "A parse tree", "A list of document identifiers"), "Sentiment classification predicts an attitude label; translation, parsing and retrieval produce different outputs."),
    ("What is a corpus in NLP?", "A collection of language data", ("A single grammar rule", "A hardware processor", "A list of model scores only"), "A corpus collects text or speech examples for analysis, training or evaluation."),
],
"Origins of NLP": [
    ("What is central to a rule-based NLP system?", "Explicitly written linguistic rules", ("Unlabelled random numbers", "Only next-token sampling", "Only image pixels"), "Symbolic systems encode rules and lexical knowledge explicitly rather than estimating everything from examples."),
    ("Which statement best describes the development of NLP?", "Rules, statistics and neural methods have overlapping uses", ("Every method before neural networks is unusable", "Statistical NLP never uses corpora", "Neural NLP does not learn from data"), "The approaches overlap; rules remain useful, and learned systems still benefit from linguistic analysis."),
],
"Language and Knowledge": [
    ("Which field studies meaning in context, including speaker intentions?", "Pragmatics", ("Character encoding", "Edit distance", "Alphabet sorting"), "Pragmatics concerns contextual interpretation; semantics studies meaning more generally."),
    ("In 'Asha arrived. She sat down', linking 'She' to Asha is an example of what?", "Coreference resolution", ("Stemming", "Machine translation", "Spelling correction"), "Coreference resolution identifies expressions that refer to the same entity."),
],
"Challenges of NLP": [
    ("The word 'bank' can refer to a financial institution or a river edge. What is the challenge?", "Lexical ambiguity", ("An invalid Unicode sequence", "A unique meaning in every context", "A missing sentence boundary only"), "One word form has different possible senses, which context can help distinguish."),
    ("Why should an NLP test set be separate from the training set?", "To measure generalization to unseen examples", ("To guarantee 100% accuracy", "To eliminate all ambiguity", "To ensure examples are memorized before testing"), "Independent evaluation estimates performance beyond the examples used to fit the model."),
],
"Language and Grammar": [
    ("Which grammar rule combines a noun phrase and a verb phrase into a sentence?", "S -> NP VP", ("NP -> S S", "V -> Det Det", "S -> N N N only"), "S is the sentence category, and NP and VP describe its major constituents in this simple grammar."),
    ("What does subject-verb agreement constrain?", "Compatible grammatical features such as number", ("The truth of a statement", "The document's file size", "The sentiment of every noun"), "Agreement relates grammatical features; for example, 'she runs' differs from 'they run'."),
],
"Processing Indian Languages": [
    ("Why is Unicode normalization useful in text processing?", "It makes equivalent character representations consistent", ("It translates every word into English", "It removes all inflections", "It guarantees correct sentiment"), "Visually equivalent text can use different character sequences, complicating comparison and tokenization."),
    ("A message uses Hindi and English in the same sentence. What is this called?", "Code-mixing", ("A context-free derivation", "An inverted index", "Beam search"), "Code-mixing combines material from multiple languages within an utterance."),
],
"NLP Applications": [
    ("Which task produces a shorter version of a document while retaining important information?", "Summarization", ("POS tagging", "Token counting", "Alphabetization"), "Summarization condenses content rather than assigning word tags or merely rearranging tokens."),
    ("Which task assigns grammatical labels such as noun and verb to tokens?", "Part-of-speech tagging", ("Document retrieval", "Translation evaluation", "Image segmentation"), "POS tagging predicts a grammatical category for each token in context."),
],
"Statistical Language Modelling": [
    ("If a toy sequence has conditional factors 0.5, 0.2 and 0.1, what is its probability?", "0.01", ("0.8", "0.1", "0.02"), "The chain rule multiplies the conditional factors: 0.5 × 0.2 × 0.1 = 0.01."),
    ("What problem does smoothing help address in count-based language models?", "Zero probability for unseen events", ("Every token having a different font", "Too many valid alphabets", "A compulsory increase in sentence length"), "Smoothing reserves probability for events absent from the training counts."),
],
"N-gram model: unigram and bigram": [
    ("How many adjacent bigrams occur in 'we learn NLP today', ignoring boundary tokens?", "3", ("2", "4", "6"), "The pairs are 'we learn', 'learn NLP' and 'NLP today': four tokens yield three bigrams."),
    ("How much history does a unigram model use to predict a token?", "No previous tokens", ("One previous token", "Two previous tokens", "The complete preceding document"), "A unigram approximation predicts each token independently of previous tokens."),
],
"Paninian Framework": [
    ("Which element is commonly the root in a Paninian dependency analysis?", "The main verb", ("The first character", "Every determiner", "The longest noun"), "The predicate organizes the participant relations in a typical computational Paninian analysis."),
    ("What does vibhakti provide evidence about in computational Paninian analysis?", "Relations between participants and a predicate", ("Only file encoding", "Only document relevance", "A guaranteed one-to-one role mapping in every sentence"), "Case markers and related grammatical information help infer relations but are not unconditional one-to-one role labels."),
],
"Karaka theory": [
    ("In 'Asha gives Ravi a book', which participant illustrates the recipient role?", "Ravi", ("Asha", "The book", "The giving action"), "Ravi receives the book, illustrating sampradana in this introductory role example."),
    ("Which introductory karaka gloss describes a source or point of separation?", "Apadana", ("Karana", "Sampradana", "Adhikarana"), "Apadana is associated with source/separation, unlike instrument, recipient and location respectively."),
],
"Word Level Analysis: Introduction": [
    ("Which process aims to return a dictionary base form using vocabulary and grammar?", "Lemmatization", ("Random deletion", "Document ranking", "Sentence translation"), "Lemmatization can map forms such as 'are' to 'be' using lexical and grammatical information."),
    ("What is tokenization?", "Splitting text into useful units", ("Assigning a final exam grade", "Translating every word", "Combining every document into one word"), "Tokens may be words, subwords or other units depending on the task and tokenizer."),
],
"Regular Expressions": [
    ("In a regular expression, what does the quantifier '*' mean?", "Zero or more repetitions", ("Exactly one repetition", "At least one repetition", "End of input only"), "For example, ab* matches a, ab and abb because b may occur zero or more times."),
    ("Which pattern matches an entire string of one or more ASCII digits?", "^[0-9]+$", ("[a-z]+", "^[0-9]$", "[0-9]*"), "The anchors cover the complete string, the class selects ASCII digits and + requires at least one digit."),
],
"Finite-State Automata": [
    ("When does a finite-state automaton accept an input?", "When the complete input is consumed in an accepting state", ("As soon as any state is visited", "Only when the string is empty", "Whenever the input contains a vowel"), "Acceptance depends on the state after reading all symbols, not an accepting state visited earlier."),
    ("In a deterministic finite automaton, how many next states are allowed for a state-symbol pair?", "Exactly one in a total transition function", ("Arbitrarily many without restriction", "Always zero", "One for each word in the corpus"), "A DFA's total transition function selects a single next state for each state and input symbol; partial drawings may omit a rejecting sink."),
],
"Morphological Parsing": [
    ("What is a morpheme?", "A smallest meaningful or grammatical unit", ("Any sequence of three letters", "A whole document only", "A probability distribution over sentences"), "A morpheme contributes meaning or grammatical information, such as plural -s."),
    ("Which analysis is appropriate for 'walked' in a regular past-tense use?", "walk + past tense", ("walk + plural noun", "wa + lked with no grammatical features", "walk + future tense"), "The regular ending -ed expresses past-tense information in this example."),
],
"Spelling Error Detection and Correction": [
    ("What is the standard Levenshtein distance from 'cat' to 'cats'?", "1", ("0", "2", "4"), "One insertion of s transforms cat into cats."),
    ("Which operations have unit cost in standard Levenshtein distance?", "Insertion, deletion and substitution", ("Only adjacent transposition", "Only case changes", "Translation and parsing"), "Standard Levenshtein uses these three edit operations; treating transposition as one edit requires another variant."),
],
"Words and Word Classes": [
    ("Which is typically an open word class in English?", "Nouns", ("Determiners", "Pronouns", "Coordinating conjunctions"), "Open classes readily acquire new words, whereas classes like determiners have relatively fixed membership."),
    ("What is the role of 'quickly' in 'She runs quickly'?", "Adverb modifying the verb", ("Determiner before a noun", "Main noun naming a person", "Auxiliary verb marking tense"), "Quickly describes the manner of running and functions as an adverb."),
],
"Part-of-Speech Tagging": [
    ("What is a tagset?", "The inventory of labels used by a tagger", ("A collection of search result URLs", "The number of training epochs", "A list of translated sentences"), "A tagset defines which categories the tagger can assign and their annotation conventions."),
    ("In an HMM tagger, what does Viterbi decoding typically find?", "The most probable tag sequence", ("Every possible spelling correction with equal probability", "The shortest document", "The alphabetically first noun"), "Viterbi uses dynamic programming to find the highest-scoring sequence under the model."),
],
"Syntactic Analysis: Introduction": [
    ("What does attachment ambiguity concern?", "Which phrase or head a modifier belongs to", ("Whether a file is attached to an email", "Which font a token uses", "Whether the corpus has any numbers"), "A modifier can attach to different parts of a structure, producing different readings."),
    ("In a dependency tree, what does a head-dependent edge encode?", "A grammatical relation between words", ("Only chronological document order", "A synonym set", "A machine translation quality score"), "Dependency analysis represents structural relations directly between head words and dependents."),
],
"Context-Free Grammar": [
    ("What is a terminal symbol in a grammar?", "A symbol that is not further expanded by productions", ("The final computer in a network", "Any category on a rule's left side", "A probability that must be zero"), "Terminals form the output strings; nonterminals expand through grammar productions."),
    ("When is a context-free grammar ambiguous?", "When some sentence has more than one distinct parse tree", ("When it contains more than one rule", "When it accepts no empty string", "When all terminals are lowercase"), "Ambiguity concerns alternative structural analyses of at least one generated sentence."),
],
"Constituency": [
    ("Which sequence is a noun phrase in 'the small bird sings'?", "the small bird", ("small bird sings", "the sings", "bird sings"), "The determiner, adjective and noun form the subject NP in this simple analysis."),
    ("Why use more than one constituency test?", "Individual tests can be imperfect or context-sensitive", ("All adjacent strings must be constituents", "One test always proves every structure", "Constituents cannot be nested"), "Substitution, movement and coordination provide converging evidence rather than infallible standalone decisions."),
],
"Parsing": [
    ("Which parsing strategy starts from the start symbol and expands grammar rules?", "Top-down parsing", ("Bottom-up parsing only", "Unigram counting", "Lexical database retrieval"), "Top-down search starts with a proposed sentence category and expands toward the input tokens."),
    ("What is a parse forest?", "A compact representation of multiple possible parses", ("A list of stop words", "A single spelling correction", "A bilingual dictionary"), "Shared substructures allow many candidate trees to be represented without duplicating every component."),
],
"Probabilistic Parsing": [
    ("For a PCFG, what must probabilities of alternative rules with the same left side sum to?", "1", ("0", "The number of input words", "Any arbitrary negative value"), "For each left-hand nonterminal, rule probabilities form a normalized distribution over its alternatives."),
    ("A toy PCFG tree uses rules with probabilities 0.5, 0.4 and 0.5. What is its probability?", "0.1", ("1.4", "0.25", "0.9"), "Under the PCFG factorization, multiply the applied rule probabilities: 0.5 × 0.4 × 0.5 = 0.1."),
],
"Introduction to Information Retrieval": [
    ("What is the user's information need?", "The information the user actually wants to find", ("Only the query's number of characters", "Only the document file type", "The search engine's RAM capacity"), "A query expresses a need imperfectly; relevance should be judged against the underlying task."),
    ("What does ranked retrieval return?", "Documents ordered by an estimated relevance score", ("Only sentences in alphabetical order", "A guaranteed true answer to every question", "Only randomly chosen document identifiers"), "Ranking orders candidates according to a relevance-oriented model rather than proving every result relevant."),
],
"Design Features of Information Retrieval Systems": [
    ("What does a posting list typically contain?", "Identifiers of documents containing a term", ("Only grammar production probabilities", "Only target-language translations", "Only spelling suggestions"), "An inverted index associates terms with document identifiers, often augmented by counts or positions."),
    ("Why store token positions in an index?", "To support phrase and proximity queries", ("To guarantee every query has one result", "To eliminate document identifiers", "To make relevance independent of the query"), "Positions let a search system check whether terms occur in a required order or close together."),
],
"Information Retrieval Models: Classical models": [
    ("What is the cosine similarity of nonzero orthogonal vectors?", "0", ("1", "-1 always", "The sum of their lengths"), "Orthogonal vectors have dot product zero, so their normalized dot product is zero."),
    ("Why does inverse document frequency favour a rare term?", "A term in fewer documents is often more discriminative", ("A rare term must always be misspelled", "It guarantees a document is relevant", "It ignores collection statistics"), "IDF reduces the influence of ubiquitous terms and gives more weight to terms that distinguish documents."),
],
"Information Retrieval Models: Non-classical models": [
    ("For a stated fuzzy OR operator max, what is OR(0.2, 0.7)?", "0.7", ("0.2", "0.9", "0.14"), "The max operator returns the greater membership value; the selected operator must be stated."),
    ("What does latent semantic indexing use to model term-document relationships?", "A lower-dimensional approximation of a term-document matrix", ("Only exact Boolean conjunction", "Only character sorting", "A perfect manually translated corpus"), "LSI uses a reduced-rank representation, commonly through singular value decomposition, to capture latent associations."),
],
"Information Retrieval Models: Alternative models": [
    ("In a toy fielded scorer, title matches weigh 3 and body matches weigh 1. What is one title plus two body matches worth?", "5", ("3", "2", "6"), "Apply the stated heuristic: 1 × 3 + 2 × 1 = 5. This is not a claim about a standard BM25 formula."),
    ("What is explicit relevance feedback?", "User judgments used to refine retrieval", ("A guarantee all initial results are correct", "Removing all query terms", "Translating every document into a new language"), "Users identify useful or unhelpful results, and the system uses that evidence to adjust search."),
],
"Evaluation of the IR System": [
    ("A system retrieves 8 documents, 6 relevant. There are 10 relevant documents overall. What is recall?", "0.6", ("0.75", "0.8", "1.25"), "Recall is relevant retrieved divided by all relevant: 6/10 = 0.6."),
    ("If precision and recall are both 0.5, what is F1?", "0.5", ("0.25", "1", "0"), "F1 = 2PR/(P+R) = 2 × 0.5 × 0.5 / 1 = 0.5."),
],
"Language Divergences and Typology": [
    ("Which word-order labels describe typical English and Hindi declarative orders respectively?", "SVO and SOV", ("SOV and SVO", "VSO and VSO", "OVS and OSV"), "English commonly uses subject-verb-object and Hindi subject-object-verb; these are dominant patterns, not universal rules."),
    ("What is lexical divergence in translation?", "Languages expressing a concept through different lexical choices", ("Every sentence having identical vocabulary", "A corpus containing only punctuation", "The removal of all word meanings"), "One source word may need several target words, or a target distinction may require additional context."),
],
"Machine Translation using Encoder–Decoder": [
    ("What is the encoder's role in sequence-to-sequence translation?", "Build contextual representations of the source", ("Always copy source words unchanged", "Assign the final human evaluation score", "Replace the target vocabulary with source spelling"), "The decoder conditions generation on encoded source information."),
    ("What usually signals completion of a generated translation?", "An end-of-sequence token", ("The first comma in the source", "A fixed source-to-target length equality", "The highest alphabetic letter"), "The decoder can generate an end token; source and target sequences need not have equal lengths."),
],
"Details of the Encoder–Decoder Model": [
    ("What does cross-attention connect in a Transformer translation decoder?", "Target-side decoder states to source encoder representations", ("Only adjacent source characters", "Only unrelated document titles", "The training loss directly to a file name"), "Cross-attention lets target generation consult encoded source information."),
    ("A correct target token has probability 0.5. What is its negative log-likelihood using natural logs?", "Approximately 0.693", ("Approximately -0.693", "Exactly 0.5", "Exactly 2"), "The loss is -ln(0.5), approximately 0.693, rather than the probability itself."),
],
"Translating in Low-Resource Situations": [
    ("What is a parallel corpus?", "Aligned text and translations in two or more languages", ("Any two unrelated collections of equal size", "A list of spelling errors only", "A grammar with no terminals"), "Alignment connects source units with corresponding translated target units."),
    ("What is a risk of relying heavily on synthetic translation pairs?", "Errors in generated translations may enter training", ("All linguistic bias disappears", "Human evaluation becomes unnecessary", "The data is guaranteed to be error-free"), "Synthetic examples can help coverage but inherit errors and biases from the generating system."),
],
"MT Evaluation": [
    ("What does BLEU's brevity penalty discourage?", "Translations that are too short relative to references", ("Every synonym substitution", "Long source documents only", "The presence of punctuation in references"), "A candidate can obtain high precision by omitting material; the brevity penalty counters that tendency."),
    ("Which pair is commonly assessed by human MT evaluation?", "Adequacy and fluency", ("CPU temperature and disk space", "Font size and line length", "Alphabet order and file extension"), "Adequacy concerns preserving source meaning; fluency concerns natural target-language expression."),
],
"Bias and Ethical Issues": [
    ("Which translation error can reinforce an occupational stereotype?", "Adding a male pronoun for a doctor without source evidence", ("Preserving an explicitly stated pronoun", "Keeping a named person's stated identity", "Flagging genuine ambiguity for review"), "Unsupported gender assumptions can misrepresent the source and reproduce stereotypes."),
    ("Why use human review for consequential translations?", "Subtle errors can have serious effects despite fluent output", ("Automatic output is always factually perfect", "Fluency guarantees legal accuracy", "Review removes the need to understand either language"), "Risk-sensitive review checks meaning, omissions and context rather than trusting surface fluency alone."),
],
"Large Language Models with Transformers": [
    ("Attention weights are 0.2 and 0.8; scalar values are 10 and 20. What is the weighted output?", "18", ("15", "30", "8"), "Compute 0.2 × 10 + 0.8 × 20 = 2 + 16 = 18."),
    ("What does multi-head attention allow?", "Several attention projections to capture different relationships", ("Every head to access forbidden future target tokens", "All token embeddings to be removed", "A guarantee that all generated claims are true"), "Different heads can learn complementary attention patterns; masking and evaluation remain necessary."),
],
"Sampling for LLM Generation": [
    ("For probabilities 0.5, 0.3, 0.2, what remains after top-k filtering with k=1?", "Only the highest-probability token", ("All tokens with unchanged probabilities", "Only the lowest-probability token", "No tokens"), "Top-k retains the k highest-probability candidates and renormalizes the remaining mass."),
    ("For fixed logits, increasing a positive temperature generally has what effect?", "It makes the probability distribution less concentrated", ("It always increases factual accuracy", "It guarantees greedy decoding", "It removes the need for softmax"), "Dividing logits by a larger temperature reduces their relative differences before softmax."),
],
"Pretraining Large Language Models": [
    ("How does autoregressive pretraining obtain its prediction targets?", "By shifting the token sequence to predict following tokens", ("By assigning random answer keys at inference", "Only from manually written user ratings", "By reading the future test answers"), "The training text supplies next-token targets through self-supervision."),
    ("Why deduplicate pretraining data?", "To reduce repeated material and its distortions", ("To ensure every statement becomes true", "To remove all possible privacy risks", "To make tokenization unnecessary"), "Deduplication reduces over-representation of repeated content but is not a complete privacy or quality solution."),
],
"Evaluating Large Language Models": [
    ("Mean next-token negative log-likelihood is ln(5). What is perplexity?", "5", ("ln(5)", "1/5", "25"), "Perplexity is exp(mean negative log-likelihood): exp(ln(5)) = 5."),
    ("A model answers 18 of 24 test items correctly. What is accuracy?", "0.75", ("0.18", "0.24", "1.333"), "Accuracy is correct predictions divided by the total: 18/24 = 0.75."),
],
}
