from shoresh_neo import ClarkPhonemicClass, ClarkShoresh

def createNodes():
    fin = open("Clark_shorashim_dentals.csv", encoding='utf-8')

    phoneticGroups = set()
    shorashim = set()
    for line in fin:
        list = eval(str(line.split(",")))
        #only creates nodes from lines that aren't blank (and also are not first line)
        if list[0] != "" and list[1] != "Class":
            phoneticGroups.add((list[0], list[1]))
            shorashim.add((list[2], list[3]))
    fin.close()
    ClarkPhonemicClass.create_or_update(*[dict(group=t[0], name=t[1]) for t in phoneticGroups])
    ClarkShoresh.create_or_update(*[dict(root=t[0], meaning=t[1]) for t in shorashim])

def connectNodes():
    fin = open("Clark_shorashim_dentals.csv", encoding='utf-8')
    for line in fin:
        list = eval(str(line.split(",")))
        # only creates nodes from lines that aren't blank (and also are not first line)
        if list[0] != "" and list[1] != "Class":
            n1 = ClarkPhonemicClass.nodes.get(group=list[0],name=list[1])
            n2 = ClarkShoresh.nodes.get(root=list[2], meaning=list[3])
            n2.memberOf.connect(n1)

if __name__ == '__main__':
    createNodes()
    connectNodes()

