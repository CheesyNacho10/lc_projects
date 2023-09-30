cadena = "El/DT perro/N come/V carne/N de/P la/DT carnicería/N y/C de/P la/DT nevera/N y/C canta/V el/DT la/N la/N la/N ./Fp"

# 1. Frecuencia de categorías
tokens = cadena.split()
categories = [token.split("/")[1] for token in tokens]
category_freq = {}
for category in categories:
    category_freq[category] = category_freq.get(category, 0) + 1

sorted_category_freq = dict(sorted(category_freq.items()))

print("1) Frecuencia de categorías:")
for category, freq in sorted_category_freq.items():
    print(f"{category} {freq}")
print()

# 2. Frecuencia de palabras y sus categorías
word_category_freq = {}
for token in tokens:
    word, category = token.split("/")
    word = word.lower()
    if word not in word_category_freq:
        word_category_freq[word] = {}
    word_category_freq[word][category] = word_category_freq[word].get(category, 0) + 1

sorted_word_category_freq = dict(sorted(word_category_freq.items()))

print("2) Frecuencia de palabras y sus categorías:")
for word, categories in sorted_word_category_freq.items():
    print(f"{word} {sum(categories.values())}", end=" ")
    for cat, freq in categories.items():
        print(f"{cat} {freq}", end=" ")
    print()
print()

# 3. Frecuencia de bigramas
bigrams = [('<S>', tokens[0].split("/")[1])]
for i in range(len(tokens) - 1):
    bigrams.append((tokens[i].split("/")[1], tokens[i+1].split("/")[1]))
bigrams.append((tokens[-1].split("/")[1], '</S>'))

bigram_freq = {}
for bigram in bigrams:
    bigram_freq[bigram] = bigram_freq.get(bigram, 0) + 1

print("3) Frecuencia de bigramas:")
for bigram, freq in bigram_freq.items():
    print(bigram, freq)
print()

# 4. Probabilidades léxicas y de emisión
def probabilities(w):
    if w not in word_category_freq:
        return "La palabra es desconocida"
    total_word = sum(word_category_freq[w].values())
    results = []
    for category, freq in word_category_freq[w].items():
        p_c_given_w = freq / total_word
        p_w_given_c = freq / sorted_category_freq[category]
        results.append((category, p_c_given_w, p_w_given_c))
    return results

word = "la"
probs = probabilities(word)

print(f"4) Probabilidades léxicas y de emisión para la palabra '{word}':")
for category, p_c_given_w, p_w_given_c in probs:
    print(f"P( {category} | {word} )= {p_c_given_w:.6f}")
    print(f"P( {word} | {category} )= {p_w_given_c:.6f}")
