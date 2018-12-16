# Village - spawn point
# Forest - kill random things
# Arena - pvp

locationtexts = {}
locationtexts['village'] = "You are in the village\n"
locationtexts['forest'] = "You are in the forest\n"
locationtexts['arena'] = "You are in the arena\n"

actionsin = {}
actionsin['village'] = [['Stand in the middle of the village and do nothing\n'], ['Go somewhere']]
actionsin['arena'] = [['Look around\n'], ['Go somewhere'] ]
actionsin['forest'] = [['Bam bam, I am in the forest.\n'], ['Go somewhere']]

paths = {}
paths['village'] = ['arena', 'forest']
paths['forest'] = ['village']
paths['arena'] = ['village']

pathkeyboards = {}
for path in paths:
    pathkeyboards[path] = []
    for place in paths[path]:
        pathkeyboards[path].append([place])
