# Village - spawn point
# Forest - kill random things
# Arena - pvp
from enum import Enum


class Location(Enum):
    VILLAGE = 1, 'village', 'You are in the village\n', ['arena', 'forest']
    FOREST = 2, 'forest', 'You are in the forest\n', ['village']
    ARENA = 3, 'arena', 'You are in the arena\n', ['village']
    def __init__(self, key, string, text, paths):
        self.key = key
        self.text = text
        self.string = string
        self.paths = paths
    @staticmethod
    def toEnum(string):
        for loc in Location:
            if loc.string == string:
                return loc

actionsin = {}
actionsin[Location.VILLAGE] = [['Stand in the middle of the village and do nothing'], ['Go somewhere']]
actionsin[Location.ARENA] = [['Look around'], ['Go somewhere'] ]
actionsin[Location.FOREST] = [['Bam bam, I am in the forest.'], ['Fight monsters'], ['Go somewhere']]

pathkeyboards = {}
for location in Location:
    path = location.paths
    pathkeyboards[location] = []
    for place in path:
        pathkeyboards[location].append([place])
