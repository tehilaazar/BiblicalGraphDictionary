import sys

def main(argv):
    # defaults
    if len(argv) == 0:
        argv.append("dev")
    elif len(argv) < 2:
        print('USAGE: python transliterate.py train')
        exit(0)

    m = open('mapping.txt', encoding="utf-8")
    hebrew = ''
    latin = ''
    mapping = {}
    for line in m:
        line = line.strip().split('\t')
        mapping[line[0]] = line[1]
        hebrew += line[0]
        latin += line[1]
    m.close()

    trantab = str.maketrans(hebrew, latin)

#    print(mapping)
    f = open(argv[0], encoding='utf-8')
    f2 = open(argv[0] + '.out', 'w', encoding='utf-8')
    for line in f:
        f2.write(line.translate(trantab))

    f.close()
    f2.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        main([])

