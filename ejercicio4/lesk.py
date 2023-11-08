import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('wordnet')
nltk.download('stopwords')

def compute_overlap(signature, context):
    signature = signature - set(stopwords.words('english'))
    context = context - set(stopwords.words('english'))
    return len(signature.intersection(context))

def simplified_lesk(word, sentence):
    context = set(word_tokenize(sentence))

    best_sense = wn.synsets(word)[0]
    max_overlap = 0

    for sense in wn.synsets(word):
        signature = set(word_tokenize(sense.definition()))
        for ex in sense.examples():
            signature = signature.union(set(word_tokenize(ex)))

        overlap = compute_overlap(signature, context)

        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = sense

    return best_sense

sentence = "Yesterday I went to the bank to withdraw the money and the credit card did not work"
word = "bank"
print(f"Word: '{word}'\nSentence: {sentence}\nDefinition: {simplified_lesk(word, sentence).definition()}")
