#from shoresh_neo import Shoresh
from sys import exit
from typing import List, Dict, Set
import math
import csv
import pickle
from numpy import dot
from numpy.linalg import norm
from os import path
from datetime import datetime

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


def cosine_similarity2(shoreshMatrix, shoresh1, shoresh2):
    return dot_product(shoreshMatrix[shoresh1], shoreshMatrix[shoresh2]) / (
                magnitude(shoreshMatrix[shoresh1]) * shoreshMatrix(shoreshMatrix[shoresh2]))

norm_cache = dict()
def cosine_similarity(matrix, shoresh1, shoresh2):
    a = matrix[shoresh1]
    b = matrix[shoresh2]
    if shoresh1 in norm_cache:
        normA = norm_cache[shoresh1]
    else:
        normA = norm(a)
        norm_cache[shoresh1] = normA

    if shoresh2 in norm_cache:
        normB = norm_cache[shoresh2]
    else:
        normB = norm(b)
        norm_cache[shoresh2] = normB

    return dot(a, b)/(normA*normB)

romanization = None
def unromanize(shoresh: str) -> str:
    global romanization
    if romanization is None: # load the first time
        fin = open("romanization.txt", encoding='utf-8')
        romanization = {}
        for line in fin:
            enLetter, heLetter = line.strip().split("\t")
            romanization[enLetter] = heLetter
        fin.close()

    hebrew = ""
    for letter in shoresh:
        if letter in romanization:
            hebrew += romanization[letter]
    return hebrew

def main():
    print('Started at ', datetime.now())
    write_to_csv = False
    write_to_neo = True
    WINDOW = 10

    print('Checkpoint 1: Calculating / Loading pesukim to know shoresh set', datetime.now())
    if path.exists("pesukim.p"): # get from pickled version if it exists
        allPasukim, shoreshSet, shoreshDict, iToS, sToi = pickle.load(open("pesukim.p", "rb"))
    else: # generate these from scratch
        # opens the file with every pasuk in Tanach and each word per pasuk and its shoresh
        fin = open("shorashim.out.txt", encoding='utf-8')

        # creates a set for all the shorashim
        shoreshSet: Set[str] = set()

        # goes through each pasuk
        for line in fin:

            # gets a list of tuples of the words and shoresh in each pasuk
            pasuk = eval((line.split(":"))[1])

            # loops through word and its shorash in each pasuk
            for _, shoresh in pasuk:

                # adds the shoresh to a set so can later add to a dictionary of all the shorashim
                # and each shoresh in dictionary will have its own dictionary of all the shorashim
                # to keep track of which shorashim are related to each other
                shoreshSet.add(shoresh)

        #close file so when reopen will be at top again
        fin.close()

        iToS: List[str] = sorted(list(shoreshSet)) # to ensure consistent ordering across runs
        sToi: Dict[str, int] = {shoresh : pos for pos, shoresh in enumerate(iToS)}

        # now trying different method based on concatenating the pesukim and
        # looking at the 10 shorashim before and after

        # create a list to hold all the pasukim to concatenate
        allPasukim = []

        fin = open("shorashim.out.txt", encoding='utf-8')

        # concatenate all the pasukim without the name of each pasuk
        for line in fin:
            # gets all the words and shorash in each pasuk
            pasuk = eval(line.split(":")[1])
            allPasukim.extend(pasuk)

        fin.close()

        shoreshDict: Dict[str, str] = dict.fromkeys(shoreshSet, "")

        for englishShoresh in shoreshDict:
            shoreshDict[englishShoresh] = (unromanize(englishShoresh))

        pickle.dump([allPasukim, shoreshSet, shoreshDict, iToS, sToi], open("pesukim.p", "wb"))

    N = len(shoreshSet)

    print('Checkpoint 2: Calculating / Loading shoresh matrix to know distributional vectors', datetime.now())
    if path.exists("shoreshMatrix." + str(WINDOW) + ".p"): # get from pickled version if it exists
        shoreshMatrix = pickle.load(open("shoreshMatrix." + str(WINDOW) + ".p", "rb"))
    else:
        shoreshMatrix: List[List[int]] = [[0] * N for _ in range(N)]
        # now creates a list of all the tuples of word and shorash
        #allPasukim = eval(allPasukim)

        # now loop through each tuple to check the a certain amount of shorashim before
        # it and the same number of shorashim behind it and increase the count for
        # each shoresh by the shorashim surrounding it
        #WINDOW to check for certain number of shorashim above and below it


        for i in range(len(allPasukim)):

            # get each shorash to look at its surrounding shorashim
            word, shoresh = allPasukim[i]

            # first look at lower words

            # if the shorash is among the first shoreshcount shorashim in tanach then
            # only look at the number of shorashim before it
            if 0 < i < WINDOW:
                for j in range(i):

                    #increase the count for that shorash by 1
                    shoreshMatrix[sToi[shoresh]][sToi[allPasukim[j][1]]] += 1

            # if the shorash is not one of the first threshold, then can look at
            # all shoreshcount amount of the shorashim below it
            if i >= WINDOW:
                for j in range(WINDOW):
                    shoreshMatrix[sToi[shoresh]][sToi[allPasukim[i-j-1][1]]] += 1

            # now looking at higher words

            # if the shorash is among the last shoreshcount amount in tanach, then only
            # look at the words above it
            if len(allPasukim)-1 > i > len(allPasukim)-WINDOW:
                for j in range(len(allPasukim)-i-1):
                    shoreshMatrix[sToi[shoresh]][sToi[allPasukim[-1-j][1]]] += 1

            # if it's not among the last shoreshcount , then can look at at amount of WINDOW
            # above it
            if i < len(allPasukim)-WINDOW:
                for j in range(WINDOW):
                    shoreshMatrix[sToi[shoresh]][sToi[allPasukim[i+j+1][1]]] += 1

        pickle.dump(shoreshMatrix, open("shoreshMatrix." + str(WINDOW) + ".p", "wb"))

    #calculatePpmi
    ppmiMatrix = [[0] * N for i in range(N)]
    #sum of all words in all contexts
    sumWords = sum([sum(shoreshMatrix[i]) for i in range(len(shoreshMatrix))])
    pj = [(sum([shoreshMatrix[row][j] for row in range(len(shoreshMatrix))]))/sumWords for j in range(N)]
    for i in range(N):
        # probability of row
        pi = (sum(shoreshMatrix[i])) / sumWords
        print('i', i)
        for j in range(N):
            #joint probability of i and j
            pij = (shoreshMatrix[i][j])/sumWords
            #probability of column
            x = pij / (pi * pj[j])
            pmi = math.log(x,2) if x > 0 else 0
            ppmiMatrix[i][j] = pmi if pmi > 0 else 0

    i = sToi['>MR']
    j = sToi["DBR"]
    k = sToi["KBD"]
    cs = cosine_similarity(ppmiMatrix, i, j)
    print(cs)
    cs = cosine_similarity(ppmiMatrix, i, k)
    print(cs)
    cs = cosine_similarity(ppmiMatrix, j, k)
    print(cs)
    cs = cosine_similarity(ppmiMatrix, k, k)
    print(cs)

main()