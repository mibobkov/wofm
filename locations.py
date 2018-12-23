# Village - spawn point
# Forest - kill random things
# Arena - pvp
from enum import Enum


class Location(Enum):
    VILLAGE = 1
    FOREST = 2
    ARENA = 3

    # def text(self):



locationtexts = {}
locationtexts['village'] = "You are in the village\n"
locationtexts['forest'] = "You are in the forest\n"
locationtexts['arena'] = "You are in the arena\n"

actionsin = {}
actionsin['village'] = [['Stand in the middle of the village and do nothing'], ['Go somewhere']]
actionsin['arena'] = [['Look around'], ['Go somewhere'] ]
actionsin['forest'] = [['Bam bam, I am in the forest.'], ['Fight monsters'], ['Go somewhere']]

paths = {}
paths['village'] = ['arena', 'forest']
paths['forest'] = ['village']
paths['arena'] = ['village']

pathkeyboards = {}
for path in paths:
    pathkeyboards[path] = []
    for place in paths[path]:
        pathkeyboards[path].append([place])
