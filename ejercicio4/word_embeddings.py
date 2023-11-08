import nltk
import gensim
from nltk.corpus import wordnet as wn
from nltk.data import find
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('word2vec_sample')

word2vec_sample = str(find('models/word2vec_sample/pruned.word2vec.txt'))
model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_sample, binary=False)

def lemmatization(tokens):
    sentence_lematized = []
    for token in tokens:
        lematized_token = wn.morphy(token)
        if lematized_token:
            sentence_lematized.append(lematized_token)
    return set(sentence_lematized)

def compute_similarity(signature, context):
    signature = signature - set(stopwords.words('english'))
    context = context - set(stopwords.words('english'))
    similarity = 0.0
    for token_s in signature:
        for token_c in context:
            if token_s in model.key_to_index and token_c in model.key_to_index:
                similarity += model.similarity(token_s, token_c)
    return similarity

def word_embedding(word, sentence):
    context = set(word_tokenize(sentence))
    context = lemmatization(context)

    best_sense = wn.synsets(word)[0] if wn.synsets(word) else None
    max_similarity = 0.0

    for sense in wn.synsets(word):
        signature = set(word_tokenize(sense.definition()))
        for example in sense.examples():
            signature = signature.union(set(word_tokenize(example)))
        signature = lemmatization(signature)

        similarity = compute_similarity(signature, context)
        
        if similarity > max_similarity:
            max_similarity = similarity
            best_sense = sense

    return best_sense

sentence = "Yesterday I went to the bank to withdraw the money and the credit card did not work"
word = "bank"
print(f"Word: '{word}'\nSentence: {sentence}\nDefinition: {word_embedding(word, sentence).definition()}")
