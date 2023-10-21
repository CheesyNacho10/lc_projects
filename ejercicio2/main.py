from nltk.corpus import cess_esp
from nltk.tag import hmm, tnt
from sklearn.model_selection import train_test_split
from random import shuffle
import os
import matplotlib.pyplot as plt
import numpy as np

def compute_ic(data):
    n = len(data)
    std_err = np.std(data) / np.sqrt(n)
    ic = 1.96 * std_err
    return ic

def save_plot(results, ic, model_name):
    x = [i for i in range(10)]
    y = results
    min_y = round(min(y) * 20) / 20
    max_y = round(max(y) * 20) / 20
    plt.axis([-1, 10, max(min_y - 0.1, 0), min(max_y + 0.1, 1)])
    plt.ylabel('Accuracy')
    plt.xlabel('Fold')
    plt.title(f'Ten-fold cross validation - {model_name}')
    plt.plot(x, y, 'ro')
    plt.errorbar(x, y, yerr=ic, linestyle='None')
    filename = f"ten_fold_validation_{model_name}.png"
    plt.savefig(filename)
    plt.clf()

RESULTS_PATH = './results.txt'

if os.path.exists(RESULTS_PATH):
    with open(RESULTS_PATH, "r") as file:
        lines = file.readlines()
    
    results_hmm = [float(line.strip()) for line in lines[1:11]]
    results_tnt = [float(line.strip()) for line in lines[13:23]]
    
    ic_hmm = compute_ic(results_hmm)
    print(f"IC HMM: {ic_hmm:.5f}")
    save_plot(results_hmm, ic_hmm, "HMM")

    ic_tnt = compute_ic(results_tnt)
    print(f"IC TNT: {ic_tnt:.5f}")
    save_plot(results_tnt, ic_tnt, "TNT")

    exit()

CORPUS_PATH = './corpus.txt'

# Leer o descargar el corpus
if os.path.exists(CORPUS_PATH):
    infile = open(CORPUS_PATH, 'r')
    corpus_sentences = []
    for line in infile:
        word_tag_pairs = line.strip('\n').split(' ')
        corpus_sentences.append([(pair.split('/')[0], pair.split('/')[1]) for pair in word_tag_pairs])
    infile.close()
else:
    corpus_sentences = cess_esp.tagged_sents()    
    outfile = open(CORPUS_PATH, 'w')
    for s in corpus_sentences:
        str_sent = ''
        for x in s:
            str_sent += '/'.join(x) + ' '
        outfile.write(str_sent.strip() + '\n')
    outfile.close()

def transform_tags(tagged_sentence):
    transformed = []
    for word, tag in tagged_sentence:
        if word == '*0*' or tag.startswith('sn'):
            continue
        elif tag.startswith('v') or tag.startswith('F'):
            new_tag = tag[:3]
        else:
            new_tag = tag[:2]
        transformed.append((word, new_tag))
    return transformed

# Transformar las etiquetas del corpus
transformed_corpus = [transform_tags(sentence) for sentence in corpus_sentences]

# Dividir el corpus en entrenamiento y prueba
train_corpus, test_corpus = train_test_split(transformed_corpus, train_size=0.9, test_size=0.1)

# Etiquetadores
trainer_hmm = hmm.HiddenMarkovModelTrainer()
tagger_hmm = trainer_hmm.train(train_corpus)

trainer_tnt = tnt.TnT()
trainer_tnt.train(train_corpus)

# Evaluar etiquetadores
accuracy_hmm = tagger_hmm.accuracy(test_corpus)
accuracy_tnt = trainer_tnt.accuracy(test_corpus)

print(f"Accuracy HMM: {accuracy_hmm*100:.2f}%")
print(f"Accuracy TNT: {accuracy_tnt*100:.2f}%")

fold_size = len(transformed_corpus) // 10
shuffled_corpus = transformed_corpus.copy()
shuffle(shuffled_corpus)

results_hmm = []
results_tnt = []

for i in range(10):
    test_data = shuffled_corpus[i*fold_size:(i+1)*fold_size]
    train_data = shuffled_corpus[:i*fold_size] + shuffled_corpus[(i+1)*fold_size:]
    
    # Entrenar etiquetadores
    tagger_hmm = trainer_hmm.train(train_data)
    trainer_tnt.train(train_data)
    
    # Evaluar etiquetadores
    accuracy_hmm = tagger_hmm.accuracy(test_data)
    accuracy_tnt = trainer_tnt.accuracy(test_data)

    results_hmm.append(accuracy_hmm)
    results_tnt.append(accuracy_tnt)

    print(f"Fold {i+1} Accuracy HMM: {accuracy_hmm*100:.2f}%")
    print(f"Fold {i+1} Accuracy TNT: {accuracy_tnt*100:.2f}%")

with open("results.txt", "w") as file:
    file.write("Results for HMM:\n")
    for result in results_hmm:
        file.write(f"{result:.5f}\n")
    file.write("\nResults for TNT:\n")
    for result in results_tnt:
        file.write(f"{result:.5f}\n")

ic_hmm = compute_ic(results_hmm)
print(f"IC HMM: {ic_hmm:.5f}")
save_plot(results_hmm, ic_hmm, "HMM")

ic_tnt = compute_ic(results_tnt)
print(f"IC TNT: {ic_tnt:.5f}")
save_plot(results_tnt, ic_tnt, "TNT")
