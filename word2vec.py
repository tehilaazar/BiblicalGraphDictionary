romanization = None
def unromanize(shoresh):
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

fin = open("shorashim.out.txt", encoding='utf-8')

listofPerakim = []
perek = ""
prevPerek = 1
prevPasuk = 0
# goes through each pasuk
for line in fin:

    curPerek = int(line.split(" ")[1])
    curPasuk = int((line.split(" ")[2]).strip(":"))

    if curPerek == prevPerek and prevPasuk+1 == curPasuk:

        pasuk = eval((line.split(":"))[1])
        for word, shoresh in pasuk:
            perek += unromanize(shoresh) + " "

    else:
        perek += "."
        listofPerakim.append(perek)
        if curPerek != 1:
            prevPerek +=1
        else:
            prevPerek = 1
        perek = ""
        pasuk = eval((line.split(":"))[1])
        for word, shoresh in pasuk:
            perek += unromanize(shoresh) + " "
    prevPasuk = curPasuk

fin.close()

fout = open("list_of_perakim.txt", "w", encoding="utf-8")
for perek in listofPerakim:
    fout.write(perek + "\n")
fout.close()

