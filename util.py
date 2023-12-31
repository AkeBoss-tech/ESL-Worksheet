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

def random_story_level(level=1):
    files = os.listdir("ESL-stuff/level")
    print(files)

    choices = [file for file in files if file.startswith("file-" + level)]
    print(choices)
    with open("ESL-stuff/level/" + choice(choices), "r") as f:
        story = f.readlines()
        # get rid of empty lines
        story = [line for line in story if line != "\n"]
    return story

def get_random_sentence(story):
    """Get a random sentence from a story."""
    paragraph = split_into_sentences(choice(story))
    sentence = choice(paragraph)
    if len(sentence) < 4:
        return get_random_sentence(story)

    if sentence[0].islower():
        return get_random_sentence(story)

    return sentence

# function to split a paragarph into proper sentences
# returns a list of strings
import re
def split_into_sentences(paragraph):
    if '\n' in paragraph: paragraph = paragraph.replace('\n', ' ')

    sentences = []
    if type(paragraph) != str:
        print("Paragraph must be a string.")
        paragraph = " ".join(paragraph)
    
    # Split the string based on . ? and !
    punctuation_split = re.split(r"(\.|\?|!)", paragraph)

    # check to make sure that things inside of quotes don't get split based on periods.
    """ for i in range(len(punctuation_split)):
        if punctuation_split[i] not in [".", "?", "!"]:
            continue
        if i < len(punctuation_split) - 1:
            if re.search(r"[A-Za-z0-9]\s+\"", punctuation_split[i]):
                continue
        if i > 0:
            if re.search(r"\"\s+[A-Za-z0-9]", punctuation_split[i-1]):
                continue
        sentences.append(punctuation_split[i]) """

    punctuation_marks = [thing for thing in punctuation_split if thing in [".", "?", "!"]]
    everything_else = [thing for thing in punctuation_split if thing not in [".", "?", "!"] and len(thing.strip()) > 0]
    
    if len(punctuation_marks) != len(everything_else):
        # add extra periods to counteract the split
        if len(punctuation_marks) > len(everything_else):
            for i in range(len(punctuation_marks) - len(everything_else)):
                everything_else.append("")
        else:
            for i in range(len(everything_else) - len(punctuation_marks)):
                punctuation_marks.append(".")

    # Write the code to check if sentences are proper
    # check for capitalization and length
    # If not, combine the sentences until they are proper
    # Make sure exclamation points and questions marks are treated as ends of sentences also.
    # You may assume that any given paragraph will be less than 500 characters in length.
    # Remove all extra spaces.
    for i, sentence in enumerate(everything_else):
        if len(sentence) > 1:
            if sentence[0] == " " and (sentence.strip()[0].isupper() or sentence[1] == '"'):
                sentences.append(sentence + punctuation_marks[i])
                continue
            if sentence[0].isupper() and len(sentence) > 3:
                sentences.append(sentence + punctuation_marks[i])
            else:  
                sentences[-1] += sentence + punctuation_marks[i]

    sentences = [s.strip() for s in sentences]
    return sentences

def find_verb(sentence):
    verbs = []
    pos_tags = pos_tag(word_tokenize(sentence))
    
    for word, tag in pos_tags:
        if tag.startswith("VBD") or tag.startswith("VBP"):
            verbs.append(word)

    if len(verbs) == 0:
        for word, tag in pos_tags:
            if tag.startswith("VBZ") or tag.startswith("VB"):
                verbs.append(word)
    return verbs

def separate_words(sentence):
    words = sentence.split(" ")
    shuffle(words)
    return words

def create_shuffle_question(sentence):
    words = separate_words(sentence)
    return " / ".join(words)

def generate_rearrange_worksheet(story=random_story(), num=10):
    sentences = split_into_sentences(" ".join(story))

    if num > len(sentences):
        num = len(sentences)
    
    shuffle(sentences)
    sentences = sentences[:num]
    
    worksheet = "## Rearrange the Sentence\n\n"
    for index, sentence in enumerate(sentences):
        worksheet += f"{index + 1}. {create_shuffle_question(sentence)}\n"
    
    worksheet += "\n\n## Answer Key\n\n"
    for index, sentence in enumerate(sentences):
        worksheet += f"{index + 1}. {sentence}\n"
    
    print(worksheet)
    return worksheet

def keep_trying_rearrange_worksheet(num=10):
    try:
        return generate_rearrange_worksheet(random_story(), num)
    except:
        return keep_trying_rearrange_worksheet(num)

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

# Function to calculate lexical score based on word frequency
def calculate_lexical_score(word):
    word = word.lower()
    synsets = wordnet.synsets(word)
    if synsets:
        # Consider the number of synsets (senses) for the word
        return len(synsets) * 10 * len(word) / (corpus_freq[word] + 1)
    else:
        # Assign a low score to words not found in WordNet
        return 0  # You can adjust this as needed

# function that returns sorted lexical scores
def get_lexical_scores(story):
    sentence = ""

    for sent in story:
        sentence += sent + " "

    words = word_tokenize(sentence.lower())
    # remove duplicate words in sentence
    words = list(dict.fromkeys(words))

    lexical_scores = {word: calculate_lexical_score(word) for word in words}
    return sorted(lexical_scores.items(), key=lambda x: x[1], reverse=True)


from nltk.stem import WordNetLemmatizer

# Initialize the WordNetLemmatizer
lemmatizer = WordNetLemmatizer()


def get_infinitive_form(word):
    return "to " + lemmatizer.lemmatize(word, pos="v")

def generate_fill_worksheet(problems=None):
    sentences = []
    if problems is None:
        problems = int(input("Enter the number of questions"))
    while len(sentences) < problems:
        random_sentence = get_random_sentence(random_story())
        verbs = find_verb(random_sentence)

        if len(verbs) > 1 or len(verbs) == 0:
            continue

        new = random_sentence.replace(verbs[0], "_" * len(verbs[0]), 1)

        if new not in sentences:
            sentences.append([new + f" ({get_infinitive_form(verbs[0])})", verbs[0]])

    worksheet = "## Fill in the Verb\n\n"

    for index, sentence in enumerate(sentences):
        worksheet += f"{index + 1}. {sentence[0]}\n"

    worksheet += "\n\n## Answer Key\n\n"

    for index, sentence in enumerate(sentences):
        worksheet += f"{index + 1}. {sentence[1]}\n"

    print(worksheet)
    return worksheet

from random import shuffle
def generate_vocab_worksheet(story=random_story(), word_limit=20):
    # get a random story and create a function to get the 10 hardest words in it and create a worksheet with those words and their definitions
    
    hardest_words = [word[0] for word in get_lexical_scores(story)[:word_limit]]
    definitions = [wordnet.synsets(word)[0].definition() for word in hardest_words]

    # remove duplicate definitions and words
    for definition in definitions:
        if definitions.count(definition) > 1:
            index = definitions.index(definition)
            definitions.pop(index)
            hardest_words.pop(index)

    answers = ""

    for index, word in enumerate(hardest_words):
        answers += f"{index + 1}. {word} - {definitions[index]}\n"

    shuffle(definitions)

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()

    worksheet = "## Vocabulary Worksheet\n\n"
    # create a table with the words and possible definitions
    worksheet += "| Answer | Word | Definition |\n| --- | --- | --- |\n"
    for index, word in enumerate(hardest_words):
        worksheet += f"| | {word} | {alphabet[index]}. {definitions[index]} |\n"
    worksheet += "| | | |"

    worksheet += "\n\n## Answer Key\n\n"
    worksheet += answers
    return worksheet

def generate_vocab_worksheet_interactive(story=random_story()):
    # get a random story and create a function to get the 10 hardest words in it and create a worksheet with those words and their definitions
    # keep asking user for story till they say yes
    print(story)
    while input("Is this story okay? (y/n)") != "y":
        story = random_story()
        print(story)

    hardest_words = [word[0] for word in get_lexical_scores(story)[:20]]
    definitions = [wordnet.synsets(word)[0].definition() for word in hardest_words]

    # remove duplicate definitions and words
    for definition in definitions:
        if definitions.count(definition) > 1:
            index = definitions.index(definition)
            definitions.pop(index)
            hardest_words.pop(index)

    # ask users if a word should be included and allow them to stop any time
    to_remove = []
    for index, word in enumerate(hardest_words):
        print(f"{index + 1 - len(to_remove)}. {word} - {definitions[index]}")
        response = input(f"Should {word} be included? (y/n/stop)")
        
        if response == "n":
            to_remove.append(index)
        elif response == "stop":
            for remaining_index in range(index, len(hardest_words)):
                to_remove.append(remaining_index)
            break
    
    for index in reversed(to_remove):
        definitions.pop(index)
        hardest_words.pop(index)

    answers = ""

    for index, word in enumerate(hardest_words):
        answers += f"{index + 1}. {word} - {definitions[index]}\n"

    shuffle(definitions)

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()

    worksheet = "## Vocabulary Worksheet\n\n"
    for index, word in enumerate(hardest_words):
        worksheet += f"{index + 1}. {word}\t\t\t{alphabet[index]}. {definitions[index]}\n"

    worksheet += "\n\n## Answer Key\n\n"
    worksheet += answers

    return worksheet

def get_definitions(word):
    return [syn.definition() for syn in wordnet.synsets(word)]

def is_verb(word):
    return len(find_verb(word)) > 0

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
""" story = random_story()
sentence = ""

for sent in story:
    sentence += sent + " "

print(sentence)

# Tokenize the sentence
words = word_tokenize(sentence)

# Calculate word frequency using NLTK's FreqDist
word_freq = FreqDist(words) """

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
""" lexical_scores = {word: calculate_lexical_score(word) for word in words}

# Print the lexical scores
for word, score in lexical_scores.items():
    print(f"{word}: {score:.2f}")

# Print top 5 words with highest lexical scores
print("\nTop 5 words with highest lexical scores:")
for word, score in sorted(lexical_scores.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"{word}: {score:.2f}")

 """
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
    return syllables_with_dots, len(syllables)


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
""" story = random_story()
sentence = " ".join(story)
print(sentence) """

def get_verb_types(sentence):
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
    """ print("Infinitive Verbs:", infinitive_verbs)
    print("Past Tense Verbs:", past_tense_verbs)
    print("Present Participle Verbs (Gerunds):", present_participle_verbs)
    print("Past Participle Verbs:", past_participle_verbs)
    print(
        "Present Simple Verbs (3rd person singular and present participle):",
        present_simple_verbs,
    ) """

    # VB, VBD, VBG, VBN, VBP or VBZ
    return infinitive_verbs, past_tense_verbs, present_participle_verbs, past_participle_verbs, present_simple_verbs

# get all sentences with VBD verbs
# get verb index from the return type of above function
# 1 is infinitive, 2 is past tense, 3 is present participle, 4 is past participle, 5 is present simple
def get_sentences_with_verb(story=random_story(), verb=1):
    text = " ".join(story)
    text = text.replace("\n", " ")
    
    sentences = []
    for sentence in split_into_sentences(text):
        if len(get_verb_types(sentence)[verb]) > 0:
            print(get_verb_types(sentence)[verb])
            sentences.append(sentence)
    return sentences

verb_types_str = ["infinitive", "past tense", "present participle", "past participle", "present simple"]

def generate_worksheets_for_verb(story=None, verb_type=1):
    if story is None:
        story = random_story()
    sentences = get_sentences_with_verb(story, verb_type)
    shuffle(sentences)

    sentence_with_blanks = []
    answers = []
    for sentence in sentences:
        verb = get_verb_types(sentence)[verb_type][0]
        answers.append(verb)
        sentence_with_blanks.append(sentence.replace(verb, "_" * 10 + ' (' + get_infinitive_form(verb) + ')', 1))
    
    if len(sentence_with_blanks) > 0:
        worksheet = f"## {verb_types_str[verb_type].title()} Practice\n\n"
        new_line = "\n"
        for index, sentence in enumerate(sentence_with_blanks):
            worksheet += f"{index + 1}. {sentence.replace(new_line, '')}\n"

        worksheet += "\n\n## Answer Key\n\n"
        for index, word in enumerate(answers):
            worksheet += f"{index + 1}. {word}\n"

        print(worksheet)
        return worksheet
    return ""

def generate_full_worksheet(story=random_story()):
    full_worksheet = '# Worksheet\n\n'
    for paragraph in story:
        full_worksheet += paragraph + '\n'

    full_worksheet += '\n\n'

    # add worksheets for two verb types
    for i in range(5):
        full_worksheet += generate_worksheets_for_verb(story, verb_type=i)
        full_worksheet += '\n\n'

    # add definition worksheet
    full_worksheet += generate_vocab_worksheet(story)

    full_worksheet += generate_rearrange_worksheet(story, num=10)

    print(full_worksheet)
    with open("worksheet.txt", "w") as f:
        f.write(full_worksheet)
    return full_worksheet

def get_nouns(sentence):
    words = word_tokenize(sentence)

    # Perform part-of-speech tagging
    pos_tags = pos_tag(words)

    # Initialize lists to categorize verbs by tense
    single_nouns = []
    plural_nouns = []
    proper_sing_noun = []
    proper_plur_noun = []

    # Iterate through the tagged words to categorize verbs by tense
    for word, tag in pos_tags:
        if tag == "NN":
            single_nouns.append(word)
        elif tag == "NNS":
            plural_nouns.append(word)
        elif tag == "NNP":
            proper_sing_noun.append(word)
        elif tag == "NNPS":
            proper_plur_noun.append(word)

    # Print the categorized verbs
    print("Single Nouns:", single_nouns)
    print("Plural Nouns:", plural_nouns)
    print("Proper Singular Nouns:", proper_sing_noun)
    print("Proper Plural Nouns:", proper_plur_noun)
    return single_nouns, plural_nouns, proper_sing_noun, proper_plur_noun
    
