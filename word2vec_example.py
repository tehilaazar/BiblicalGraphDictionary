import gensim

# Load Google's pre-trained Word2Vec model.
model = gensim.models.KeyedVectors.load_word2vec_format('c:/josh/GoogleNews-vectors-negative300.bin', binary=True)
print(model.most_similar('king', 10))