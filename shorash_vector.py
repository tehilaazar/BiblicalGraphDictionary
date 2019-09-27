from shoresh_neo import Shoresh
from sys import exit
from typing import List, Dict, Set
import math
import csv

def main():
    # opens the file with every pasuk in Tanach and each word per pasuk and its shorash
    fin = open("shorashim.out.txt", encoding='utf-8')

    # creates a set for all the shorashim
    shorashSet: Set[str] = set()

    # goes through each pasuk
    for line in fin:

        # gets a list of tuples of the words and shorash in each pasuk
        pasuk = eval((line.split(":"))[1])

        # loops through word and its shorash in each pasuk
        for word, shorash in pasuk:

            # adds the shorash to a set so can later add to a dictionary of all the shorashim
            # and each shorash in dictionary will have its own dictionary of all the shorashim
            # to keep track of which shorashim are related to each other
            shorashSet.add(shorash)

    #close file so when reopen will be at top again
    fin.close()

    sToi: Dict[str, int] = {shorash : pos for pos, shorash in enumerate(list(shorashSet))}
    # iToS: Dict[int, str] = {pos: shorash for pos, shorash in enumerate(list(shorashSet))}
    iToS: List[str] = list(shorashSet)
    N = len(shorashSet)
    shoreshMatrix: List[List[int]] = [[0] * N for i in range(N)]

    # now trying different method based on concatenating the pesukim and
    # looking at the 10 shorashim before and after

    # create a list to hold all the pasukim to concatenate
    allPasukim = []

    fin = open("shorashim.out.txt", encoding='utf-8')

    # concatenate all the pasukim without the name of each pasuk
    for line in fin:
        # gets all the words and shorash in each pasuk
        pasuk = eval(line.split(":")[1])
        allPasukim += (pasuk)

    fin.close()

    # now creates a list of all the tuples of word and shorash
    #allPasukim = eval(allPasukim)

    # now loop through each tuple to check the a certain amount of shorashim before
    # it and the same number of shorashim behind it and increase the count for
    # each shorash by the shorashim surrounding it

    #shoresh count to check for certain number of shorashim above and below it
    shoreshCount = 10

    for i in range(len(allPasukim)):

        # get each shorash to look at its surrounding shorashim
        word, shorash = allPasukim[i]

        # first look at lower words

        # if the shorash is among the first shoreshcount shorashim in tanach then
        # only look at the number of shorashim before it
        if 0 < i < shoreshCount:
            for j in range(i):

                #increase the count for that shorash by 1
                shoreshMatrix[sToi[shorash]][sToi[allPasukim[j][1]]] += 1

        # if the shorash is not one of the first threshold, then can look at
        # all shoreshcount amount of the shorashim below it
        if i >= shoreshCount:
            for j in range(shoreshCount):
                shoreshMatrix[sToi[shorash]][sToi[allPasukim[i-j-1][1]]] += 1

        # now looking at higher words

        # if the shorash is among the last shoreshcount amount in tanach, then only
        # look at the words above it
        if len(allPasukim)-1 > i > len(allPasukim)-shoreshCount:
            for j in range(len(allPasukim)-i-1):
                shoreshMatrix[sToi[shorash]][sToi[allPasukim[-1-j][1]]] += 1

        # if it's not among the last shoreshcount , then can look at at amount of shoreshcount
        # above it
        if i < len(allPasukim)-shoreshCount:
            for j in range(10):
                shoreshMatrix[sToi[shorash]][sToi[allPasukim[i+j+1][1]]] += 1

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

    def cosine_similarity(shoresh1, shoresh2):
        return dot_product(shoreshMatrix[shoresh1], shoreshMatrix[shoresh2])/ (magnitude(shoreshMatrix[shoresh1]) * magnitude(shoreshMatrix[shoresh2]))

    shoresh_similarity1 = cosine_similarity(sToi['>MR'], sToi['DBR'])
    print(shoresh_similarity1)
    shoresh_similarity2 = cosine_similarity(sToi['JHWH'], sToi['MCH'])
    print(shoresh_similarity2)

    # function that will turn the romanized shorashim back into hebrew
    def unromanize(shoresh):
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

    print(unromanize(">MR"))
    print(unromanize('BN'))
    print(unromanize('<DD'))
    print(unromanize('JRWCLM'))
    shorashSetHebrew = set()

    print(sToi['>MR'])
    print(sToi["DBR"])

    shorashDict: Dict[str, str] = dict.fromkeys(shorashSet, "")

    for englishShorash in shorashDict:
        shorashDict[englishShorash] = (unromanize(englishShorash))

    with open('shoresh_matrix.out.csv', mode='w', encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(shorashDict.keys())
        writer.writerow(shorashDict.values())
        writer.writerow([] + list(shorashSet))
        writer.writerow([] + list(shorashSetHebrew))
        for i in range(N):
            writer.writerow([iToS[i]] + shoreshMatrix[i])

    #1545 Amar
    #4760 Daber


    for i in range(N):
        s = Shoresh(enName=iToS[i], heName=shorashDict[iToS[i]]).save()

    for i in range(N):
        for j in range(i + 1, N):
            if cosine_similarity(i, j) > .9:
                s1 = Shoresh.nodes.get(enName=iToS[i])
                s2 = Shoresh.nodes.get(enName=iToS[j])
                s1.similarity.connect(s2)


if __name__ == '__main__':
    main()
    exit(0)

#old code below

# create dictionary of all the shorashim
shorashDict1: Dict[str, Dict[str, int]] = dict.fromkeys(shorashSet, dict.fromkeys(shorashSet, 0))

# goes through each shorash in dictionary and deletes the data of the shorash
# that is the same as the current shorash
for key1, value1 in shorashDict1.items():
    for key2, value2 in value1.items():
        if key1 == key2: del key2

# first way

# now reopens file of pasukim with shorashim and increases count for
# all the shorashim each shorash shares a pasuk with
fin = open("shorashim.out.txt", encoding='utf-8')

# goes thorugh each pasuk
for line in fin:

    # gets a list of tuples of the words and shorash in each pasuk
    pasuk = eval((line.split(":"))[1])

    # loops through word and its shorash in each pasuk
    for word1, shorash1 in pasuk:

        # loops a second time through each word and shorash to increase
        # count in shorash1
        for word2, shorash2 in pasuk:

            # when the two shorashim are not the same increase data by 1
            if shorash1 != shorash2:
                shorashDict1[shorash1][shorash2] += 1

fin.close()

# second way

# now trying different method based on concatenating the pesukim and
# looking at the 10 shorashim before and after

# create another dictionary of all the shorashim
shorashDict2 = dict.fromkeys(shorashSet, dict.fromkeys(shorashSet, 0))

# create a string to hold all the pasukim to concatenate
allPasukim = []

fin = open("shorashim.out.txt", encoding='utf-8')

# concatenate all the pasukim without the name of each pasuk
for line in fin:
    # gets all the words and shorash in each pasuk
    pasuk = eval(line.split(":")[1])
    allPasukim += (pasuk)

fin.close()

# now creates a list of all the tuples of word and shorash
#allPasukim = eval(allPasukim)

fin = open("shorashim.out.txt", encoding='utf-8')

# now loop through each tuple to check the 10 shorashim before
# it and the 10 shorashim behind it and increase the count for
# each shorash by the shorashim surrounding it
for i in range(len(allPasukim)):

    # get each shorash to look at its surrounding shorashim
    word, shorash = allPasukim[i]

    # first look at 10 lower words

    # if the shorash is among the first 10 shorashim in tanach then
    # only look at the number of shorashim before it
    if 0<i<10:
        for j in range(i):

            #if the shorash below it is not equal to the current shorash
            if shorash != allPasukim[j][1]:

                #increase the count for that shorash by 1
                shorashDict2[shorash][allPasukim[j][1]] += 1

    # if the shorash is not one of the first 10, then can look at
    # all 10 of the shorashim below it
    if i>=10:
        for j in range(10):
            if shorash != allPasukim[i-j-1][1]:
                shorashDict2[shorash][allPasukim[i-j-1][1]] += 1

    # now looking at higher 10 words

    # if the shorash is among the last 10 in tanach, then only
    # look at the words above it
    if len(allPasukim)-1>i>len(allPasukim)-10:
        for j in range(len(allPasukim)-i-1):
            if shorash != allPasukim[-1-j][1]:
                shorashDict2[shorash][allPasukim[-1-j][1]] += 1

    # if it's not among the last 10, then can look at all 10
    # above it
    if i<len(allPasukim)-10:
        for j in range(10):
            if shorash != allPasukim[i+j+1][1]:
                shorashDict2[shorash][allPasukim[i+j+1][1]] += 1

fin.close()

fout = open("shorashDictionary.out.txt","w")
fout.write("First Shorash Dictionary looking at just the other words in the pesukim: ")
fout.write(str(shorashDict1))
fout.write("Second Shorash Dictionary looking at the 10 words above and below: ")
fout.write(str(shorashDict2))
fout.close()

print("done")

