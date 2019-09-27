from neo4j.v1 import GraphDatabase, basic_auth

def findingRelationshipsBetweenTheRabbis():

    driver = GraphDatabase.driver("bolt://hobby-jhedjehadkjfgbkeaajelfal.dbs.graphenedb.com:24786", auth=basic_auth("mivami", "b.hsh2OnrThi0v.aPpsVUFV5tjE7dzw"))
    session = driver.session()

    query = 'match (r) where r:EncodedRabbi return r'
    #query = "match (r) where r.generation = 'A3' return r"
    result = session.run(query)
    encodedRabbis = []
    for record in result:
        name = record['r']['englishName']
        encodedRabbis += [name]


    encodedRel = dict()
    for name in encodedRabbis:
        query = 'match (:EncodedRabbi {englishName : "' + name + '" })-[m]->(r2:EncodedRabbi) return m, r2'
        result = session.run(query)
        allRel = []
        for record in result:
            type = record['m'].type
            start = record['m'].start
            end = record['m'].end
            rabbi = record['r2']['englishName']
            allRel.append((type, start, end, rabbi))
        encodedRel[name] = allRel
    #print(encodedRel)

    query = 'match (r:ComputedRabbi) return r'

    result = session.run(query)
    names = []

    for record in result:
        name = record['r']['name']
        id = record['r'].id
        names += [name]



    compRabbis = []
    rel = dict()
    #for i in range(400):
    for name in names:
        query = 'match (:ComputedRabbi {name : "' + name + '" })-[m]->(r2:ComputedRabbi) return m, r2'
        result = session.run(query)
        allRel = []
        for record in result:
            type = record['m'].type
            if type != 'spoke_to':
                start = record['m'].start
                end = record['m'].end
                rabbi = record['r2']['name']
                relation = None
                if type == 'inquires':
                    relation = 'student'
                elif type == 'cites':
                    relation = 'student'
                elif type == 'joint_statement':
                    relation = 'colleague'
                elif type == 'attributes':
                    relation = 'student'
                allRel.append((type, start, end, rabbi, relation))
        if len(allRel) > 0:
            rel[name] = allRel
            compRabbis += [name]


    allConnections = {}
    for rabbi in rel:
        g = []
        for allConn in rel[rabbi]:
            if allConn[4] and (allConn[3] not in g):
              g += (allConn[3], allConn[4])
        allConnections[rabbi] = g
    print(allConnections)


    sameR = []
    for name in compRabbis:
        for i in encodedRabbis:
            if name == i:
                sameR += [name]

    # print(sameR)
    # print(len(sameR))

    sameRel = {}
    for i in sameR:
        g = []
        for j in rel[i]:
            rav = j[3]
            relationship = j[4]
            for k in encodedRel[i]:
                if rav == k[3] and relationship == k[0]:
                    #g += j
                    #g += k
                    pair = (rav, relationship)
                    if rav not in g:
                        g += pair
                if len(g)>0:
                    sameRel[i] = g

    #print(sameRel)
    for r, value in sameRel.items():
        print(r + ": " + str(value))


    session.close()

def findingGenerationOfRabbis():
    from neo4j.v1 import GraphDatabase, basic_auth
    driver = GraphDatabase.driver("bolt://hobby-jhedjehadkjfgbkeaajelfal.dbs.graphenedb.com:24786",
                                  auth=basic_auth("mivami", "b.hsh2OnrThi0v.aPpsVUFV5tjE7dzw"))
    session = driver.session()

    query = 'match (r) where r:EncodedRabbi return r'
    # query = "match (r) where r.generation = 'A3' return r"
    result = session.run(query)
    encodedRabbis = []
    # eRabbisWithGen = {}
    eRabbisWithGenDict = {}
    for record in result:
        name = record['r']['englishName']
        gen = record['r']['generation']
        encodedRabbis += [name]
        eRabbisWithGenDict[name] = gen
        # if gen in eRabbisWithGen:
        #     eRabbisWithGen[gen] += [name]
        # else:
        #     eRabbisWithGen[gen] = [name]

    # print(eRabbisWithGenDict)

    query = 'match (r:ComputedRabbi) return r'

    result = session.run(query)
    names = []

    for record in result:
        name = record['r']['name']
        id = record['r'].id
        names += [name]

    compRabbis = []
    sameGen = []
    sameGenDict = {}
    for i in range(len(names)):
        # for i in range(200):
        if names[i] != 'Stipulating':
            query = 'match (:ComputedRabbi {name : "' + names[i] + '" })-[m]->(r2:ComputedRabbi) return m, r2'
            result = session.run(query)

            for record in result:
                type = record['m'].type
                start = record['m'].start
                end = record['m'].end
                rabbi = record['r2']['name']

                if type == 'spoke_to' or type == 'inquires' or type == 'joint_statement':
                    # they should be in the same generation
                    if names[i] in sameGenDict:
                        sameGenDict[names[i]] += [rabbi]
                    else:
                        sameGenDict[names[i]] = [rabbi]
                    sameGen += [(names[i], rabbi, type)]
                    if names[i] not in compRabbis:
                        compRabbis += [names[i]]
                # elif type == 'cites':
                #         relation = 'student'
                # elif type == 'attributes':
                #         relation = 'student'
    print(sameGenDict)
    sameR = []
    for name in compRabbis:
        for i in encodedRabbis:
            if name == i and name not in sameR:
                sameR += [name]
    print(compRabbis)
    print(encodedRabbis)
    print(sameR)
    allSameGens = []
    for name in sameR:
        genA = eRabbisWithGenDict[name]

        compareRabbi = sameGenDict[name]
        for rabbi in compareRabbi:
            if rabbi in eRabbisWithGenDict:
                genB = eRabbisWithGenDict[rabbi]
                if genA == genB:
                    r = (name, rabbi, genA)
                    if r not in allSameGens:
                        allSameGens += [r]

    for i in allSameGens:
        print('{} and {} in {}'.format(i[0], i[1], i[2]))
    # else:
    #    print(False)

    session.close()


#findingRelationshipsBetweenTheRabbis()
findingGenerationOfRabbis()