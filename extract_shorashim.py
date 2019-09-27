from tf.fabric import Fabric
import collections
import sys
# https://etcbc.github.io/bhsa/features/hebrew/4b/features/comments/g_lex_utf8.html

#TF = Fabric(locations='/home/chaim/github/text-fabric-data', modules=['hebrew/etcbc4c'])
TF = Fabric(locations='c:/josh/text-fabric-data/text-fabric-data', modules=['hebrew/etcbc4c'])
api = TF.load('qere_utf8 qere lex0 g_word_utf8 g_word')
api.makeAvailableIn(globals())

F = api.F
T = api.T
C = api.C
L = api.L

def print_original_words():

    for i in range(1, 12):
        print(api.T.text([i], 'text-orig-full'))
# for w in F.otype.s('word'):
#     word, part_of_speech = F.g_word.v(w), F.sp.v(w)
#     print(word, part_of_speech)
#     if w == 14:
#         break

import sys

# uncomment this if want to print to screen
# outfile=sys.stdout

# uncomment this if want to print to file
#outfile = open('POSAndTaamPairsForAllOfTanakh_1.txt', 'w')

outfile_name = 'shorashim.out.txt'

outfile = open(outfile_name, 'w', encoding='utf8')
print('Output file name:', outfile_name)

def extract_shorashim():
    for verse in F.otype.s('verse'):
        book = T.sectionFromNode(verse)[0]
        print(T.sectionFromNode(verse)[0], T.sectionFromNode(verse)[1], str(T.sectionFromNode(verse)[2]) + ':', end=' ', file=outfile)
        pasuk = []
        s = ''  # type: str
        aggregate_lex = []

        parts = L.d(verse, 'half_verse')
        for hv, half_verse in enumerate(parts):
            words = L.d(half_verse, 'word')

            for w in words:
                lex = F.g_word_utf8.v(w)
                simple_lex = F.lex0.v(w)
                qere_utf8, qere = F.qere_utf8.v(w), F.qere.v(w)
                word = F.g_word.v(w)
                if qere is not None:
                    lex = qere_utf8
                    word = qere

                trupsymbols = '֑֖֛֢֣֤֥֦֧֪֚֭֮֒֓֔֕֗֘֙֜֝֞֟֠֡֨֩֫֬֯׀'
                for c in trupsymbols:
                    lex = lex.replace(c, '')

                s += word

                # we don't output anything yet, since this is a sub-word unit
                # just aggregate it until we reach the actual end of the word
                aggregate_lex.append(lex)

                # perhaps this is also the end of an actual full word,
                # in which case we should also output all we have aggregated
                if s != '' and s[-1] != '-':
                    pasuk.append(('_'.join(aggregate_lex), simple_lex))
                    aggregate_lex = []
                    s = ''
            # end for w in words
        # end hv, half_verse in enumerate(parts)
        print(pasuk, file=outfile)



extract_shorashim()
