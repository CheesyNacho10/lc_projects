import nltk
import matplotlib.pyplot as plt
import numpy as np
from nltk.corpus import conll2000
from nltk.tag import tnt
from sklearn.metrics import confusion_matrix, classification_report

nltk.download('conll2000')
conll_train = conll2000.chunked_sents('train.txt')
conll_test = conll2000.chunked_sents('test.txt')

train_chunks = [nltk.chunk.tree2conlltags(tree) for tree in conll_train]
test_chunks = [nltk.chunk.tree2conlltags(tree) for tree in conll_test]

train = [[(t, c) for (w, t, c) in chunk_tags] for chunk_tags in train_chunks]
test = [[(t, c) for (w, t, c) in chunk_tags] for chunk_tags in test_chunks]

tnt_chunker = tnt.TnT()
tnt_chunker.train(train)
tnt_accuracy = tnt_chunker.accuracy(test)
with open('accuracy.txt', 'w') as f:
    f.write(str(tnt_accuracy))
print('Accuracy: ', tnt_accuracy)

y_true, y_pred = [], []
for sent in test_chunks:
    words, tags, gold_chunks = zip(*sent)
    predicted_chunks = [tag for word, tag in tnt_chunker.tag(tags)]
    y_true.extend(gold_chunks)
    y_pred.extend(predicted_chunks)

report = classification_report(y_true, y_pred)
with open('classification_report.txt', 'w') as f:
    f.write(report)
print("Reporte de clasificación guardado como 'classification_report.txt'.")

labels = list(set(y_true))
cm = confusion_matrix(y_true, y_pred, labels=labels)
fig, ax = plt.subplots(figsize=(10, 10))
cax = ax.matshow(cm)
plt.title('Matriz de Confusión', pad=20)
fig.colorbar(cax)
ax.set_xticks(np.arange(len(labels)))
ax.set_yticks(np.arange(len(labels)))
ax.set_xticklabels(labels, rotation=45)
ax.set_yticklabels(labels)
plt.xlabel('Predicción')
plt.ylabel('Verdadero')
plt.savefig("confusion_matrix.png")
plt.close()
print("Matriz de confusión guardada como 'confusion_matrix.png'.")
