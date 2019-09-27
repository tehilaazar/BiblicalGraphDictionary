from pymongo import MongoClient
from bs4 import BeautifulSoup
#import re
from nltk.tokenize import word_tokenize
import string
import math
import nltk
#nltk.download('punkt')
#nltk.download('wordnet')
from typing import Dict, List


#word stemmer
from nltk.stem import PorterStemmer

# word Lemma:
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

def computeReviewTFDict(lexiconEntry):
    #     """ Returns a tf dictionary for each review whose keys are all
    #     the unique words in the review and whose values are their
    #     corresponding tf.
    #     """
    # Counts the number of times the word appears in review
    reviewTFDict = {}
    for word in lexiconEntry:
        if word in reviewTFDict:
            reviewTFDict[word] += 1
        else:
            reviewTFDict[word] = 1
    # Computes tf for each word
    for word in reviewTFDict:
        reviewTFDict[word] = reviewTFDict[word] / len(lexiconEntry)
    return reviewTFDict

def computeCountDict():
    #     """ Returns a dictionary whose keys are all the unique words in
    #     the dataset and whose values count the number of reviews in which
    #     the word appears.
    #     """
    countDict = {}
    # Run through each review's tf dictionary and increment countDict's (word, doc) pair
    for review in tfDict:
        for word in review:
            if word in countDict:
                countDict[word] += 1
            else:
                countDict[word] = 1
    return countDict

def computeIDFDict():
    #     """ Returns a dictionary whose keys are all the unique words in the
    #     dataset and whose values are their corresponding idf.
    #     """
    idfDict = {}
    for word in countDict:
        idfDict[word] = math.log(len(kleinDict) / countDict[word])
    return idfDict

def computeReviewTFIDFDict(reviewTFDict):
    #     """ Returns a dictionary whose keys are all the unique words in the
    #     review and whose values are their corresponding tfidf.
    #     """
    reviewTFIDFDict = {}
    # For each word in the review, we multiply its tf and its idf.
    for word in reviewTFDict:
        reviewTFIDFDict[word] = reviewTFDict[word] * idfDict[word]
    return reviewTFIDFDict


def computeTFIDFVector(review):
    tfidfVector = [0.0] * len(wordDict)

    # For each unique word, if it is in the review, store its TF-IDF value.
    for i, word in enumerate(wordDict):
        if word in review:
            tfidfVector[i] = review[word]
    return tfidfVector

# Cos Similarity:

def dot_product(vector_x, vector_y):
    dot = 0.0
    for e_x, e_y in zip(vector_x, vector_y):
        dot += e_x * e_y
    return dot

def magnitude(vector):
    mag = 0.0
    for index in vector:
        mag += math.pow(index, 2)
    return math.sqrt(mag)





client = MongoClient()
db = client.sefaria
words = db.lexicon_entry

kleinDict = {}
for each in words.find({'parent_lexicon': 'Klein Dictionary',
                        'language_code': {'$nin': ['PBH', 'MH', 'NH', 'FW']}}):
    headword = each['headword']
    senses = each['content']['senses']
    defNew = ""

    for sense in senses:
        if 'definition' in sense:
            definition = sense['definition']
            soup = BeautifulSoup(definition, features="html.parser")
            definition = soup.get_text()
            defNew += " " + definition
        elif 'senses' in sense:
            senses = sense['senses']
            for sense in senses:
                if 'definition' in sense:
                    definition = sense['definition']

                    soup = BeautifulSoup(definition, features="html.parser")
                    definition = soup.get_text()
                    defNew += " " + definition
    kleinDict[headword] = defNew

# each string is mapped to an integer
sToi: Dict[str, int] = {headword : pos for pos, headword in enumerate(kleinDict)}
# iToS: Dict[int, str] = {pos: shorash for pos, shorash in enumerate(list(shorashSet))}
# given an integer, tells us the headword
iToS: List[str] = list(kleinDict.keys())


# split into words
tfDict = []
for i, lexiconEntry in enumerate(kleinDict):
    tokens = word_tokenize(kleinDict[lexiconEntry])
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation from each word
    table = str.maketrans(' ', ' ', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words__def = [word for word in stripped if word.isalpha()]
    # filter out stop words
    stop_words = ["\'", ",",":","."]
    words__def = [w for w in words__def if not w in stop_words]
    lemmatizedWords = [wordnet_lemmatizer.lemmatize(word, pos="v") for word in words__def]
    #lemmatizedWords = words__def
    tfDict.append(computeReviewTFDict(lemmatizedWords))

# Stores the review count dictionary
countDict = computeCountDict()

# Stores the idf dictionary
idfDict = computeIDFDict()

# Stores the TF-IDF dictionaries
tfidfDict = [computeReviewTFIDFDict(review) for review in tfDict]



wordDict = sorted(countDict.keys())
tfidfVector = [computeTFIDFVector(review) for review in tfidfDict]

# jw
# you can only compute your offsets into the tfIdfVector for your
# lemmas once you establish their absolute order. That couldn't
# happen until you counted words for ALL entries, so that the offset
# will be there even if the word doesn't appear in a particular entry
# wordDict is really your "setLemmas".

# each string is mapped to an integer
LemmaToi: Dict[str, int] = {word: pos for pos, word in enumerate(wordDict)}
# iToS: Dict[int, str] = {pos: shorash for pos, shorash in enumerate(list(shorashSet))}
# given an integer, tells us the headword
iToLemma: List[str] = list(wordDict)


#print(tfidfVector[0])

#Cos Similarity:


# LOOP THROUGH COSIN SIMILIARITIES
# change to log. e ^ (log(expression) - log(exppresion))

for i in range(len(tfidfVector)):
    for j in range(i+1, len(tfidfVector)):
        definitionSimilarity = dot_product(tfidfVector[i], tfidfVector[j]) / (magnitude(tfidfVector[i]) * magnitude(tfidfVector[j]))
        if definitionSimilarity >=0.0:
            print(i,j, iToS[i], iToS[j])





#    print(i, iToS[i], definitionSimilarity)
# definitionSimilarity = dot_product(tfidfVector[495], tfidfVector[1703]) / (magnitude(tfidfVector[495]) * magnitude(tfidfVector[1703]))
# print(definitionSimilarity)
# print(iToS[495])
# print(tfidfVector[495])
# print(iToS[1703])
# print(tfidfVector[1703])

# print(tfidfVector[495][LemmaToi['say']])
# print(tfidfVector[1703][LemmaToi['say']])
# print(tfidfVector[495][LemmaToi['speak']])
# print(tfidfVector[1703][LemmaToi['speak']])

#i = 495
#j = 1703
#definitionSimilarity = dot_product(tfidfVector[i], tfidfVector[j]) / (magnitude(tfidfVector[i]) * magnitude(tfidfVector[j]))
#print(i, j, iToS[i], iToS[j], definitionSimilarity)

#from nltk.corpus import wordnet
#synset1 = wordnet.synsets('speak')
#synset2 = wordnet.synsets('say')
#print(synset1)
#print(synset2)
#print(wordnet.wup_similarity(synset1[0], synset1[0]))