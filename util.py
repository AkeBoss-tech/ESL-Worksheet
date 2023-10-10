
import os
from random import choice
from nltk.tag import pos_tag
# find verb in sentence
from nltk.tokenize import word_tokenize
import nltk

nltk.download("averaged_perceptron_tagger")
from nltk.corpus import wordnet


# load random story
def random_story(folder=None):
    if folder is None:
        folder = choice(os.listdir("ESL-stuff"))

    story = choice(os.listdir("ESL-stuff/" + folder))
    print(folder + "/" + story)
    with open("ESL-stuff/" + folder + "/" + story, "r") as f:
        story = f.readlines()
        # get rid of empty lines
        story = [line for line in story if line != "\n"]
    return story



def get_random_sentence(story):
    """Get a random sentence from a story."""
    paragraph = choice(story).split(". ")
    sentence = choice(paragraph)
    if len(sentence) < 4:
        return get_random_sentence(story)

    if sentence[0].islower():
        return get_random_sentence(story)

    return sentence + "."




def find_verb(sentence):
    verbs = []
    pos_tags = pos_tag(word_tokenize(sentence))
    print(pos_tags)
    for word, tag in pos_tags:
        if tag.startswith("VBD") or tag.startswith("VBP"):
            verbs.append(word)

    if len(verbs) == 0:
        for word, tag in pos_tags:
            if tag.startswith("VBZ") or tag.startswith("VB"):
                verbs.append(word)
    return verbs






# nltk.download('brown')
text = nltk.Text(word.lower() for word in nltk.corpus.brown.words())



def create_similar_word_bank(words, num=4):
    bank = set()

    for word in words:
        # similar_words = wordnet.similar_tos('dog')
        for syn in wordnet.synsets(word):
            bank.add(syn.lemmas()[0].name())

        """ for word in similar_words:
            bank.append(word) """
        # bank.append(text.similar(word, num=num))

    return bank



# CC - coordinating conjunction
#
# CD - cardinal number
#
# DT - determiner
#
# E - existential there (e.g., "there is")
#
# FW - foreign word
#
# IN - preposition or subordinating conjunction
#
# JJ - adjective
#
# JJR - comparative adjective
#
# JJS - superlative adjective
#
# LS - list item marker
#
# MD - modal verb
#
# NN - noun, singular or mass
#
# NNS - noun, plural
#
# NNP - proper noun, singular
#
# NNPS - proper noun, plural
#
# PDT - predeterminer
#
# POS - possessive pronoun
#
# PRP - personal pronoun
#
# PRP$ - possessive pronoun
#
# RB - adverb
#
# RBR - comparative adverb
#
# RBS - superlative adverb
#
# 詞 - Japanese particle
#
# SYM - Chinese character
#
# TO - infinitive marker
#
# UH - interjection
#
# VB - infinitive marker
#
# VBD - past tense verb
#
# VBG - past participle verb
#
# VBN - past participle verb
#
# VBP - present tense, perfect, and past participle verb
#
# VBZ - present tense, present participle verb
#


from nltk.stem import WordNetLemmatizer

# Initialize the WordNetLemmatizer
lemmatizer = WordNetLemmatizer()


def get_infinitive_form(word):
    return "to " + lemmatizer.lemmatize(word, pos="v")



def generate_fill_worksheet():
    sentences = []
    problems = int(input("Enter the number of questions"))
    while len(sentences) < problems:
        random_sentence = get_random_sentence(random_story())
        verbs = find_verb(random_sentence)

        if len(verbs) > 1 or len(verbs) == 0:
            continue

        new = random_sentence.replace(verbs[0], "_" * len(verbs[0]), 1)
        print(verbs[0])

        if new not in sentences:
            sentences.append([new + f" ({get_infinitive_form(verbs[0])})", verbs[0]])


    worksheet = "\tFill in the Verb\n\n"

    for index, sentence in enumerate(sentences):
        worksheet += f"{index + 1}. {sentence[0]}\n"

    worksheet += "\n\n\tAnswer Key\n\n"

    for index, sentence in enumerate(sentences):
        worksheet += f"{index + 1}. {sentence[1]}\n"

    print(worksheet)
    return worksheet


from nltk.corpus import wordnet


def get_definitions(word):
    return [syn.definition() for syn in wordnet.synsets(word)]

# get all complex nouns in sentence
# input: sentence
# output: list of complex nouns
def get_complex_nouns(sentence):
    nouns = []
    for chunk in sentence.noun_chunks:
        if len(chunk.text.split()) > 1:
            nouns.append(chunk.text)
    return nouns



import nltk
from nltk.corpus import wordnet
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize

# Download NLTK resources (if not already downloaded)
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("words")

# Sample sentence
# sentence = "This is a complicated sentence with various intricate words and powerful emotions."
story = random_story()
sentence = ""

for sent in story:
    sentence += sent + " "

print(sentence)

# Tokenize the sentence
words = word_tokenize(sentence)

# Calculate word frequency using NLTK's FreqDist
word_freq = FreqDist(words)

corpus = nltk.corpus.brown.words()  # Replace with your own corpus if available
corpus_freq = FreqDist(corpus)


# Function to calculate lexical score based on word frequency
def calculate_lexical_score(word):
    synsets = wordnet.synsets(word)
    if synsets:
        # Consider the number of synsets (senses) for the word
        return len(synsets) * 10 * len(word) / (corpus_freq[word] + 1)
    else:
        # Assign a low score to words not found in WordNet
        return 0  # You can adjust this as needed


# Calculate lexical scores for each word in the sentence
lexical_scores = {word: calculate_lexical_score(word) for word in words}

# Print the lexical scores
for word, score in lexical_scores.items():
    print(f"{word}: {score:.2f}")

# Print top 5 words with highest lexical scores
print("\nTop 5 words with highest lexical scores:")
for word, score in sorted(lexical_scores.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"{word}: {score:.2f}")



import nltk
from nltk.tokenize import SyllableTokenizer

# Initialize the SyllableTokenizer
tokenizer = SyllableTokenizer()


def get_syllables(word):
    # Use the SyllableTokenizer to break the word into syllables
    syllables = tokenizer.tokenize(word)

    # Join the syllables with a dot (·)
    syllables_with_dots = " · ".join(syllables)

    # Print the word with syllables separated by dots
    return syllables_with_dots






from nltk.corpus import cmudict

nltk.download("cmudict")


def get_sounds(text):
    d = cmudict.dict()

    phonetics = d[text.lower()]

    sounds = [sound[:-1] if sound[-1] in "0123" else sound for sound in phonetics[0]]
    line = " ".join(sounds)
    return line



import nltk
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

# Download NLTK resources (if not already downloaded)
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

# Sentence containing verbs with different tenses
story = random_story()
sentence = " ".join(story)
print(sentence)

# Tokenize the sentence
words = word_tokenize(sentence)

# Perform part-of-speech tagging
pos_tags = pos_tag(words)

# Initialize lists to categorize verbs by tense
infinitive_verbs = []
past_tense_verbs = []
present_participle_verbs = []
past_participle_verbs = []
present_simple_verbs = []

# Iterate through the tagged words to categorize verbs by tense
for word, tag in pos_tags:
    if tag == "VB":
        infinitive_verbs.append(word)
    elif tag == "VBD":
        past_tense_verbs.append(word)
    elif tag == "VBG":
        present_participle_verbs.append(word)
    elif tag == "VBN":
        past_participle_verbs.append(word)
    elif tag == "VBP" or tag == "VBZ":
        present_simple_verbs.append(word)

# Print the categorized verbs
print("Infinitive Verbs:", infinitive_verbs)
print("Past Tense Verbs:", past_tense_verbs)
print("Present Participle Verbs (Gerunds):", present_participle_verbs)
print("Past Participle Verbs:", past_participle_verbs)
print(
    "Present Simple Verbs (3rd person singular and present participle):",
    present_simple_verbs,
)
